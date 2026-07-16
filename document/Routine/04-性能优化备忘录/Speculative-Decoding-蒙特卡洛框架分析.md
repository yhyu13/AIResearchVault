---
tags: [optimization, LLM, inference, speculative-decoding, monte-carlo, rejection-sampling]
aliases: [SpecDec-Monte-Carlo, Speculative-Sampling-蒙特卡洛框架]
---

# Speculative Decoding 的蒙特卡洛框架分析

> **研究日期**: 2026-07-16
> **定位**: 「先猜后验」采样策略的深度附录（W29 P2），姊妹篇见 [[AI-Infra-性能优化全景]] §2.4/§3.5
> **核心问题**: speculative sampling 为什么精确无偏？接受率的理论上界是多少？期望加速比怎么推？什么工况下反而变慢？

---

## 优化场景

- **问题**：自回归 decode 逐 token 串行，每步都要把全量权重 + KV cache 从 HBM 搬一遍，batch 较小时 GPU 处于 memory-bandwidth-bound，大量算力闲置。能否用「小模型先猜 $\gamma$ 个 token、大模型一次并行验证」把串行步数压下来——并且**输出分布严格不变**？
- **主题**：[[LLM]] / [[Inference]] / [[Monte Carlo]] / [[ReSTIR]]

## 优化前：自回归 decode 的瓶颈画像

| 维度 | 特征 | 瓶颈 | 量化 |
|------|------|------|------|
| 单步耗时 | 加载全量权重 + KV cache，算 $\gamma+1$ 个位置与算 1 个位置延迟几乎相同 | HBM 带宽，不是 FLOPS | Chinchilla 70B 在 16×TPU v4 上 14.1 ms/token（Chen et al., 2023） |
| 并行度 | 序列维度因 autoregressive 依赖无法并行 | 串行步数 = 输出长度 | batch=1 时 GPU compute 大量闲置 |
| 线性层 | 小 batch 下 weight loading 主导 | memory-bound | linear / attention / all-reduce 三部分耗时在小 $K$ 下均不随 $K$ 显著增长（Chen et al., 2023） |
| 加速前提 | 只有 memory-bound 工况下「并行验证」才近似免费 | 工况依赖 | 高 QPS compute-bound 时前提失效（见下文第五节） |

**经济学本质**（Leviathan et al., 2023, §3.4）：speculative decoding 用更多 FLOPs 换更少 memory access，仅当系统 memory-bound 时是净收益。

---

## 优化方法

### 一、形式化：逐 token 的 modified rejection sampling

**设定**（Leviathan et al., 2023, §2.3 记号）：target model $M_p$ 给出分布 $p(x_t \mid x_{<t})$，draft model $M_q$ 给出 $q(x_t \mid x_{<t})$。argmax / top-k / nucleus / temperature 均可归一化为「从调整后的分布做标准采样」，故只需讨论标准采样（§2.2）。

**算法**（Leviathan et al., 2023, Algorithm 1；Chen et al., 2023 独立同期提出，称 speculative sampling）：

1. $M_q$ 自回归采样 $\gamma$ 个猜测 $x_1, \dots, x_\gamma$，逐位记录 $q_i$；
2. $M_p$ **一次并行前向**算出 $\gamma+1$ 个分布 $p_1, \dots, p_{\gamma+1}$；
3. 逐位采样 $r_i \sim U(0,1)$，$x_i$ 被接受当且仅当
$$r_i \le A(x_i) = \min\!\Big(1,\ \frac{p_i(x_i)}{q_i(x_i)}\Big)$$
记 $n$ 为首个拒绝位置之前的接受数；
4. $n < \gamma$：从残差分布 $p'(x) = \mathrm{norm}\big(\max(0,\ p_{n+1}(x) - q_{n+1}(x))\big)$ 采样兜底 token $t$；$n = \gamma$：从 $p_{\gamma+1}$ 正常采样 $t$；
5. 返回 $\mathrm{prefix} + [x_1, \dots, x_n, t]$，每轮产出 $1$ 到 $\gamma+1$ 个 token。

**关键性质**：每轮**至少**产出 1 个 token（拒绝时残差重采样兜底），故串行调用 $M_p$ 的次数不多于标准自回归解码；接受核 $\min(1, p/q)$ 正是 rejection sampling 的接受核，但有两点不同：无包络常数 $M$、拒绝不废弃而是切换到残差测度（证明见第三节）。

> 注：$q(x)=0$ 处接受概率的形式写法 $p/q$ 无定义，但该事件在 $x \sim q$ 下概率为零，不影响任何期望；数学上只需约定 $q(x)\min(1, p/q) = \min(p,q)$ 在 $q(x)=0$ 处取 $0$，下式逐步成立。

### 二、接受率闭式：$\beta = 1 - D_{\mathrm{TV}}(p,q)$ 与 maximal coupling 上界

**单 token 接受率**（Leviathan et al., 2023, Theorem 3.5 + Lemma 3.3）：

$$\beta = E_{x\sim q}\Big[\min\Big(1,\frac{p(x)}{q(x)}\Big)\Big] = \sum_x q(x)\min\Big(1,\frac{p(x)}{q(x)}\Big) = \sum_x \min\big(p(x), q(x)\big)$$

第二步是逐点恒等式 $q\cdot\min(1, p/q) = \min(q, p)$。再利用 $\min(a,b) = \tfrac{a+b-|a-b|}{2}$ 与 $\sum_x p = \sum_x q = 1$：

$$\beta = \sum_x \min(p,q) = \frac{1}{2}\sum_x (p+q) - \frac{1}{2}\sum_x |p-q| = 1 - \frac{1}{2}\lVert p - q \rVert_1 = 1 - D_{\mathrm{TV}}(p,q)$$

其中 $D_{\mathrm{TV}}(p,q) = \tfrac{1}{2}\lVert p-q\rVert_1$ 为 total variation distance。Leviathan 原文以 $D_{LK}(p,q) = \sum_x \big|p(x) - \tfrac{p(x)+q(x)}{2}\big|$ 定义（Definition 3.2），数值上恰等于 $D_{\mathrm{TV}}$；Corollary 3.4：$D_{LK} \in [0,1]$，$=0 \iff p=q$，$=1 \iff$ 支撑集不交。

**对 prefix 取期望**得整体接受率（Corollary 3.6）：

$$\alpha = E_{\text{prefix}}\Big[1 - D_{\mathrm{TV}}\big(p(\cdot\mid \text{prefix}),\ q(\cdot\mid \text{prefix})\big)\Big]$$

即 $\alpha$ 是 draft 与 target **逐步分布重叠度的期望**；$\alpha \to 1 \iff q \to p$。

**Maximal coupling 视角（理论上界）**：对任意满足 $X \sim q$、$Y \sim p$ 的耦合，

$$P(X = Y) = \sum_x P(X = Y = x) \le \sum_x \min\big(P(X=x),\ P(Y=x)\big) = \sum_x \min(p,q) = 1 - D_{\mathrm{TV}}(p,q)$$

不等式逐点成立（$P(X=Y=x)$ 同时 $\le P(X=x)$ 与 $\le P(Y=x)$）。Maximal coupling 的构造——以概率 $\sum_x \min(p,q)$ 从归一化的 $\min(p,q)$ 采公共值，否则分别从 $(q-p)_+$ 与 $(p-q)_+$ 采样——达到等号。Speculative sampling 的「接受 ⇔ 残差重采样」流程正是该耦合的算法化：**接受事件恰好对应 coupling 中 $X = Y$ 的分支**。因此 $1 - D_{\mathrm{TV}}$ 不只是本方案的接受率，而是任何「把 $q$ 样本直接当作 $p$ 样本接受」方案的概率上限。改进空间只剩两个方向：(i) 让 $q$ 更接近 $p$（缩小 $D_{\mathrm{TV}}$，EAGLE / MTP / 蒸馏路线）；(ii) 降低 draft 相对成本 $c$（n-gram、特征层小 draft 路线）。

### 三、无偏性证明：离散测度分解，而非 Jacobian 换元

**定理**（Leviathan et al., 2023, App A.1；Chen et al., 2023, Theorem 1）：按第一节规则产生的单 token 样本 $X$ 满足 $X \sim p$。

**证明**（本笔记采用 $p$=target、$q$=draft 记号；Chen 原文记号相反，已换算）。把 $P(X=x)$ 按两个互斥分支展开：

$$P(X = x) = \underbrace{P(\tilde{x} = x)\,P(\text{接受} \mid \tilde{x} = x)}_{\text{分支一：采到并接受}} + \underbrace{P(\text{拒绝})\,P(X = x \mid \text{拒绝})}_{\text{分支二：拒绝后残差重采}}$$

分支一：$q(x)\min\big(1, \tfrac{p(x)}{q(x)}\big) = \min\big(p(x), q(x)\big)$。

拒绝概率：

$$P(\text{拒绝}) = 1 - \sum_{x'}\min(p,q) = \sum_{x'}\big(q(x') - \min(p,q)\big) = \sum_{x'}\big(q(x') - p(x')\big)_+$$

由 $\sum_x (p - q) = 0$ 知 $\sum_x (p-q)_+ = \sum_x (q-p)_+ = D_{\mathrm{TV}}(p,q)$，即**拒绝概率恰好等于 $D_{\mathrm{TV}}$**。

分支二：残差分布 $r(x) = \dfrac{(p(x)-q(x))_+}{\sum_{x'} (p-q)_+}$，故

$$P(\text{拒绝}) \cdot r(x) = \Big(\sum_{x'}(q-p)_+\Big) \cdot \frac{(p(x)-q(x))_+}{\sum_{x'}(p-q)_+} = \big(p(x) - q(x)\big)_+$$

合计，用到逐点恒等式 $\min(a,b) + (a-b)_+ = a$（$a \ge b$ 时左式 $= b + (a-b) = a$；$a < b$ 时左式 $= a + 0 = a$）：

$$P(X = x) = \min\big(p(x), q(x)\big) + \big(p(x) - q(x)\big)_+ = p(x) \qquad \blacksquare$$

**序列层面**：每轮的修正分布 $p'$ 都以已接受 prefix 为条件，单步恒等式对每个位置成立；由链式法则归纳，整条轨迹的联合分布等于 target 的自回归分布。两论文均声明输出分布「identical within hardware numerics」——浮点误差与 PRNG 差异意味着实现上序列可能不逐 token 相同，但**分布**相同（Chen et al., 2023 以 XSum / HumanEval 指标持平做了经验验证）。

**与经典 rejection sampling 的本质差异**（易被面试官追问的点）：

- 经典 RS 要求包络 $M q(x) \ge p(x)$ 处处成立（蕴含 $\mathrm{supp}(q) \supseteq \mathrm{supp}(p)$），接受率 $p/(Mq)$，拒绝即废弃，期望 $M$ 次提议才产出一个样本；对 LLM 词表这种高维空间，可用 $M$ 通常巨大，接受率 $1/M$ 不可接受。
- Speculative sampling **不要求 $q$ 的支撑覆盖 $p$**：$q(x) = 0$ 而 $p(x) > 0$ 的位置自然全部落入残差分支（$(p-q)_+ = p$），由重采样精确补上。它根本不是「带包络的接受-废弃」，而是**离散测度分解**
$$p = \underbrace{\min(p,q)}_{\text{被 proposal 覆盖的部分}} + \underbrace{(p - q)_+}_{\text{残差部分}}$$
接受分支与重采样分支分别精确实现这两个测度分量，两者权重由拒绝概率 $D_{\mathrm{TV}}$ 自动配平。
- 这是逐点的测度恒等式，**不涉及连续变量的 Jacobian 换元**——没有双射、没有密度变换，只有「同一点处概率质量的两分」。与我熟悉的 rendering 里 change-of-variables / Jacobian 路线（如 ReSTIR shift mapping 的 $|\partial x'/\partial x|$）是完全不同的数学机制：那边是连续空间积分换元，这边是离散分布的加法分解。

### 四、期望产出与 wall-clock 加速比

**单轮期望 token 数**（Leviathan et al., 2023, Eq. (1)）。假设各位置接受率 i.i.d. 为 $\alpha$（§3.1 的简化假设；$\alpha$ 本身是 Corollary 3.6 意义下对 prefix 的期望，i.i.d. 是近似）。记 $N$ 为单轮产出 token 数，$N \in \{1, \dots, \gamma+1\}$。对 $0 \le k \le \gamma$：

$$P(N > k) = P(\text{前 } k \text{ 个 draft 全被接受}) = \alpha^k$$

（$N > k$ 当且仅当前 $k$ 个全接受；$k = \gamma$ 时全接受则 bonus token 使 $N = \gamma+1 > \gamma$。）用正整值随机变量的 survival function 求和公式 $E[N] = \sum_{k \ge 0} P(N > k)$：

$$E[N] = \sum_{k=0}^{\gamma} P(N > k) = \sum_{k=0}^{\gamma} \alpha^k = \frac{1 - \alpha^{\gamma+1}}{1 - \alpha}$$

即 $N$ 是「成功率 $1-\alpha$、截断于 $\gamma+1$」的 capped geometric 变量；$\gamma \to \infty$ 时 $E[N] \to \dfrac{1}{1-\alpha}$。

**期望 wall-clock 加速比**（Leviathan et al., 2023, Theorem 3.8）。设 $M_p$ 单步耗时 $T$，$c$ 为 $M_q$ 与 $M_p$ 单步耗时之比（Definition 3.7）。单轮成本 $T(\gamma c + 1)$（$\gamma$ 次 draft 串行 + 1 次 target 并行验证），基线产出 $E[N]$ 个 token 需 $E[N]\cdot T$：

$$\text{期望加速比} = \frac{1 - \alpha^{\gamma+1}}{(1 - \alpha)\,(\gamma c + 1)}$$

- **Corollary 3.9**：只要 $\alpha > c$ 就存在使加速 $>1$ 的 $\gamma$；$\gamma = 1$ 时加速至少为 $\dfrac{1+\alpha}{1+c}$。
- **极限**：$c \to 0$ 且 $\gamma$ 大时加速 $\to \dfrac{1}{1-\alpha}$；oracle-$\gamma$（每步预知最优 $\gamma$）下 $E[N] = \frac{1}{1-\alpha}$，论文估计可比固定 $\gamma$ 再高约 60%（§3.5，假设算力无限）。
- **理论示例**（Table 1，$c = \hat{c} = 0$）：$\alpha=0.8, \gamma=5 \Rightarrow 3.69\text{x}$；$\alpha=0.9, \gamma=10 \Rightarrow 6.86\text{x}$。

**例题：从 Leviathan Table 2 反解 $c$（自洽性验算）**。取 EnDe 翻译、$M_q$ = T5-small、argmax（T=0）一行：$\gamma = 7$，$\alpha = 0.75$，实测加速 3.4X。先算分子：$0.75^8 = 0.10011$，

$$E[N] = \frac{1 - 0.10011}{0.25} = 3.5996 \text{ tokens/轮}, \qquad S = \frac{3.5996}{7c + 1} = 3.4 \Rightarrow 7c + 1 = 1.0587 \Rightarrow c \approx 0.0084$$

反解得 $c \approx 0.8\%$，与论文声明的「实验中 $c < 0.05$」自洽。注意个别行实测值甚至略高于 $c = 0$ 的理论值——如 CNN/DM T5-small T=0 行（$\alpha=0.65, \gamma=5$）：理论 $\frac{1-0.65^6}{0.35} = 2.64\text{x}$ vs 实测 3.1X。论文归因于 i.i.d. 假设的近似性与实现细节（Leviathan et al., 2023, §A.3）；引用时公式值与实测值应并列。

**算力放大**（Theorem 3.11）：总算力期望放大因子

$$\frac{(1-\alpha)(\gamma\hat{c} + \gamma + 1)}{1 - \alpha^{\gamma+1}}$$

$\hat{c}$ 为 $M_q$ 与 $M_p$ 单 token 算力之比。按公式自算示例：$\hat{c} \approx 0$、$\gamma = 7$、$\alpha = 0.75$ 时放大 $\frac{0.25 \times 8}{0.9} \approx 2.2\times$。$\alpha$ 中等时总 FLOPs 浪费显著——这是高 QPS 减速的理论根源（下一节 (b)）。

### 五、工程现实：低 QPS 加速 vs 高 QPS 减速

**原论文与基准报告值**（均 batch 1）：

| 来源 | 设置 | 加速比 |
|------|------|--------|
| Leviathan et al., 2023, Table 2 | T5-XXL 11B，单 TPU-v4；EnDe T5-small T=0 $\gamma=7$ $\alpha=0.75$ | **3.4X**（全表 2.3–3.4x，标准采样 2.3–2.6x） |
| Leviathan et al., 2023, Table 3 | 小两个数量级的 draft | $\alpha \in [0.5, 0.9]$；低温/argmax 使 $\alpha$ 更高；bigram 也有 $\alpha \approx 0.2$ |
| Chen et al., 2023 | Chinchilla 70B + 专门训练的宽浅 4B draft（$c \approx 0.128$），$K=4$，XSum / HumanEval | 总体 **2–2.5x**，HumanEval 接近 2.5x；XSum 最优 $K=3$；$K$ 增大则 P90/P99 延迟方差上升 |
| Xia et al., 2024（Spec-Bench, arXiv:2401.07851） | Vicuna-7B FP16，单 RTX 3090，6 子任务 | greedy：**EAGLE 1.8–2.4x**（数学 ~2.4x）；PLD 摘要 ~2.4x 但翻译/QA 仅 1.1–1.3x；升温全线下滑（EAGLE 1.7–2.1x），与 $\alpha = 1 - D_{\mathrm{TV}}$ 公式一致 |

**vLLM 生产实测**（vLLM 官方博客，2024-10-17，Llama3-70B，4×H100）：

| 工况 | 方法 | 结果 |
|------|------|------|
| QPS = 1 | draft model（ShareGPT） | **1.5x 加速** |
| QPS = 1 | n-gram / prompt lookup（CNN/DailyMail） | **2.8x 加速** |
| 高 QPS | draft model | **1.4x 减速** |
| 高 QPS | n-gram | **1.8x 减速** |

**减速 / 失效的六条原因**（全部带来源）：

1. **工况翻转（memory-bound → compute-bound）**：低 batch 时并行验证几乎免费；高 QPS 下 continuous batching 已把 GPU 打满，验证的额外 FLOPs 直接变延迟（vLLM 博客原文；Nightjar, arXiv:2512.22420, 2025：RTX 4090 + DeepSeek-R1-Distill-Qwen-7B，$\gamma=3$ 在 15 QPS 提升吞吐 15.5%，高负载下最多退化 30.25%）。
2. **算力放大**：Theorem 3.11 的放大因子在 $\alpha$ 中等时 $>1$；吞吐导向场景里总 FLOPs 就是成本，speculation 变成「throughput tax」（Leviathan et al., 2023, §3.4）。
3. **batch 内接受稀释**：朴素实现中 batch 内任一序列在某位置拒绝即全体停止，等效 per-position 接受率变为 $\alpha^b$——$\alpha=0.8$、$b=5$ 时降至 $0.8^5 \approx 33\%$，期望前进仅 ~1.5 token（Amazon BASS 论文，2024）；修复需 per-sequence 可变接受 + KV cache 裁剪，工程复杂度高。
4. **MoE 病理**：draft token 集合激活更多 expert，验证阶段权重搬运量上升、验证耗时增加 2–3x，MoE 上 speculation 可致最多 **1.5x 减速**（Cascade, arXiv:2506.20675, MICRO 2025；对照组 dense LLaMA-3-8B n-gram 开销仅 5–10%，TPOT 加速 1.4–1.8x）。
5. **长 prompt + 大 batch 组合**：验证把每步 token 数从 $b$ 放大到 $b(\gamma+1)$，超出 A100 甜区，该工况下可比非投机解码**慢 2 倍以上**（Amazon, arXiv:2404.19124, 2024）。
6. **可复现性争议**：vLLM GitHub issue #10318（2024-11-14）报告按博客设置复现，batch 1 下最高仅 1.4x 加速，E2E 延迟远差于博客数字，要求公开完整配置。引用 vLLM 数据必须注明此争议。

**对策方向**：动态 speculative length（vLLM roadmap、Nightjar、SmartSpec）、按负载启停（Cascade 的 utility-driven 方案：utility < 1 即关闭，将 MoE 减速限制在 5% 内并提升吞吐 7–14%）。

### 六、变体对比：提高 $\alpha$ × 压低 $c$ 的两条主线

| 变体 | 来源 | 草稿机制 | 接受率 / 接受长度 | 报告加速比 | 训练成本 | 严格无损 |
|------|------|----------|-------------------|------------|----------|----------|
| 独立 draft model | Leviathan 2023；Chen 2023 | 同系列小模型自回归产 $\gamma$ token | $\alpha \approx 0.53$–$0.89$ | T5-XXL 2.3–3.4x；Chinchilla 2–2.5x | 可用现成 checkpoint；Chen 专门训练 4B（宽浅拓扑匹配硬件） | ✅ |
| n-gram / bigram | Leviathan 2023 §4.2 | 查表，$c \approx 0$ | EnDe bigram $\alpha \approx 0.20$ | 1.25x（$\gamma=3$）；vLLM n-gram CNN/DM 2.8x @QPS=1 | 0 | ✅（验证步骤兜底） |
| Prompt Lookup / LLMA | Saxena 2023；Yang et al. 2023 (arXiv:2304.04487) | 从输入/参考文档复制匹配 span | 任务依赖（高重叠场景高） | LLMA >2x（重叠场景）；Spec-Bench 摘要 ~2.4x | 0 | ✅ |
| Medusa 多头 | Cai et al. 2024 (arXiv:2401.10774) | backbone 上加多 decoding head + tree attention | typical acceptance 放宽接受条件 | Medusa-1 >2.2x；Medusa-2 2.3–3.6x | M1：冻结 backbone 只训 heads；M2：联合微调 | ⚠️ T=0 无损；T>0 typical acceptance **不保证无损** |
| EAGLE | Li et al. 2024 (arXiv:2401.15077) | 单层 Transformer 在 second-top-layer **特征**上自回归 + 超前一步 token | draft accuracy ≈ 0.8；平均每次前向近 4 token | MT-bench greedy ~3x；gpt-fast 7B 24.5 → 160.4 tok/s（RTX 3090） | ShareGPT ~68k 对话，可训练参数 0.24B(7B)–0.99B(70B)，4×A100 训 1–2 天（70B） | ✅ |
| EAGLE-2 | Li et al. 2024 (arXiv:2406.16858) | + context-aware **dynamic draft tree**（draft 置信度扩展重排） | 接受长度高于 EAGLE（置信度 well-calibrated 近似接受率） | 3.05–4.26x（比 EAGLE 快 20–40%） | 同 EAGLE | ✅ |
| EAGLE-3 | Li et al. 2025 (arXiv:2503.01840) | **training-time test** + 多层特征融合 | 接受长度至 7.5（HumanEval）；接受率不随 draft 步数衰减 | 3.0–6.5x（比 EAGLE-2 快 20–40%），HumanEval 6.5x | 同族，数据规模扩大 | ✅ |
| MTP | Gloeckle et al. 2024；DeepSeek-V3 2024 (arXiv:2412.19437) | 主模型内嵌单层 MTP 模块，推理时 self-draft | DeepSeek-V3 第二 token 接受率 **85–90%**（技术报告 §5.4.3） | DeepSeek-V3：**1.8x TPS** | 预训练联合训练，不可事后插装 | ✅ |

**要点**：

- 独立 draft：$\alpha$ 与 $c$ 的直接 trade-off——Leviathan Table 2 中 T5-large 的 $\alpha$ 最高（0.82）却加速最低（1.7X），因为 $c$ 上升更快；Leviathan 建议 draft 比 target 小约两个数量级；分布式场景 draft 的硬件拓扑需与 target 匹配（Chen 的教训：7B 在 4×TPU 上 5 ms/token，搬上 16×TPU 反而更慢）。
- n-gram / prompt lookup：$c \approx 0$ 极端路线，收益完全取决于输入-输出重叠度（摘要、RAG、多轮对话、代码编辑强，开放生成弱）。
- Medusa：单模型工件、运维最简单；但头间独立预测忽略 token 依赖，且 typical acceptance 在非 greedy 下牺牲严格无损性（EAGLE-3 论文据此只在 T=0 与 Medusa 比较）。
- EAGLE 系：核心洞见「特征层自回归比 token 层容易」（one-layer draft 上特征路线准确率比 token 路线高约 30%）+「超前一步 token 消除特征不确定性」；EAGLE-2 发现 draft 置信度是 well-calibrated 的接受率近似，据此做动态树；EAGLE-3 用 training-time test 消除训练-推理输入分布失配。
- MTP：把草稿能力内化进预训练目标，$c$ 极低且与主模型深度对齐；代价是与权重耦合，仅适用于自研模型。

### 七、与经典 Monte Carlo 家族（含 RIS）的同构对照

| 维度 | Classic rejection sampling | Importance sampling | Metropolis-Hastings | RIS（ReSTIR 重采样） | **Speculative sampling** |
|------|---------------------------|---------------------|---------------------|----------------------|--------------------------|
| Proposal | $q$，需包络 $Mq \ge p$ | $q$（支撑覆盖即可） | 依赖当前状态的转移核 $q(\cdot \mid x)$ | $q$，$M$ 个候选 | draft 模型 $q$（逐 token 条件分布） |
| 接受 / 校正机制 | 接受概率 $\frac{p(x)}{Mq(x)}$ | 无接受/拒绝，赋权 $w = p/q$ | $\min\big(1, \frac{p(x')q(x\mid x')}{p(x)q(x'\mid x)}\big)$ | 按 $w_i/\sum_j w_j$ 重采样 | 接受概率 $\min\big(1, \frac{p(x)}{q(x)}\big)$ |
| 拒绝 / 补偿行为 | 废弃重抽（期望 $M$ 次/样本） | 无（全保留） | **驻留**当前状态（样本相关） | 以 $1/(M \cdot \hat{p})$ 类权重补偿进估计量 | 从残差分布 $\mathrm{norm}((p-q)_+)$ **重采样**，当轮必有产出 |
| 输出性质 | i.i.d. 精确 $\sim p$ | 加权样本（估计无偏，样本本身不服从 $p$） | 相关样本，渐近精确 | 有限 $M$ 下重采样样本仅**近似** $\sim p$（$M \to \infty$ 收敛）；配合权重使积分估计无偏 | 每轮精确 $\sim p$，轮间链式法则保证全序列精确 |
| 接受率 | $1/M$ | — | 依赖核设计 | — | $1 - D_{\mathrm{TV}}(p,q)$（= maximal coupling 上界） |
| 关键恒等式 | $p \le Mq$ | $E_p[f] = E_q[f \cdot p/q]$ | detailed balance | RIS 权重补偿 | $p = \min(p,q) + (p-q)_+$ |

**结构同构**（渲染视角）：speculative sampling 与 RIS 共享「**proposal → 基于 likelihood ratio 的校正 → 对 proposal 未覆盖部分的补偿**」三段式骨架。可以把 speculative sampling 看作「在 $q$ 覆盖区域内取 $M=1$ 的 RS + 对拒绝事件的精确回收」：经典 RS 把拒绝视为浪费，speculative 把拒绝事件本身用作切换到残差测度的随机信号——这与 RIS 用权重把「没被采中的区域」折算回估计量在精神上相似。

**本质差异**：

- **精确 vs 近似**：RIS 在有限 $M$ 下重采样出的样本分布只是近似 $p$，要靠 $M \to \infty$ 收敛或配合权重做无偏积分估计；speculative sampling 单轮即产出**无权重、精确服从 $p$** 的样本，是**无偏的精确采样而非加权近似**。其「随机性代价」不体现为权重方差，而体现为每轮接受 token 数的 capped-geometric 波动。
- **vs MH**：MH 是渐近理论（burn-in、自相关、detailed balance），拒绝 = 驻留导致有效样本量下降；speculative 是**有限步精确**，拒绝 = 残差重采样，每轮至少前进 1 token，无驻留、无 burn-in。每步条件精确 + 链式法则即可归纳出全序列精确，无需任何渐近论证——这一点比 MCMC / RIS 家族的校正逻辑都干净。
- **vs RS**：无需包络常数 $M$，且接受率 $1 - D_{\mathrm{TV}}$ 达到 maximal coupling 上界；经典 RS 在给定 $M$ 下接受率 $1/M$ 一般远低于此。
- **计算结构**：RS / IS / MH / RIS 都是串行（或样本间并行）构造；speculative 的独特之处是 draft 串行 + target **并行验证**的空间换时间——Monte Carlo 校正逻辑第一次被用来压缩 wall-clock 而不是降低估计方差。

**注记（树推广）**：SpecInfer（Miao et al., 2023, arXiv:2305.09781）、EAGLE-2/3 与 Hu & Huang 2024（*Accelerated Speculative Sampling Based on Tree Monte Carlo*，ICML 2024；arXiv 编号未核实）把单链 draft 推广为树状 proposal，对应 Monte Carlo 中 multi-proposal 的推广方向；接受规则相应推广为树上路径选择 + 分布校正。概念前身：Stern et al. 2018 *Blockwise Parallel Decoding*（arXiv:1811.03115）——仅支持 greedy、需改训练、不保证同分布。

---

## 优化后：基准画像

| 场景 | 配置 | 指标 | 来源 |
|------|------|------|------|
| T5-XXL EnDe 翻译 | T5-small draft，argmax，$\gamma=7$ | **3.4X** walltime | Leviathan et al., 2023, Table 2 |
| T5-XXL CNN/DM 摘要 | T5-small draft，argmax，$\gamma=5$ | **3.1X**（理论 $c=0$ 值 2.64x，见 §A.3 归因） | Leviathan et al., 2023, Table 2 |
| Chinchilla 70B serving | 4B 宽浅 draft，$K=4$，16×TPU v4 | 2–2.5x，benchmark 指标与自回归持平 | Chen et al., 2023 |
| Vicuna-7B 单卡 | EAGLE，greedy，RTX 3090 | 1.8–2.4x（数学 ~2.4x） | Xia et al., 2024, Spec-Bench |
| LLaMA2-Chat 7B | EAGLE + gpt-fast，RTX 3090 | 24.5 → 160.4 tok/s | Li et al., 2024 |
| 通用 chat 大模型 | EAGLE-3 | 3.0–6.5x | Li et al., 2025 |
| DeepSeek-V3 | MTP self-draft | 第二 token 接受率 85–90%，**1.8x TPS** | DeepSeek-V3 技术报告 §5.4.3 |
| Llama3-70B 服务 | vLLM，低 QPS | 1.5–2.8x 加速（复现性存疑，issue #10318） | vLLM 官方博客 2024-10-17 |
| Llama3-70B 服务 | vLLM，高 QPS | **1.4–1.8x 减速** | vLLM 官方博客 2024-10-17 |
| MoE 模型 | 朴素 speculation | 最多 **1.5x 减速**；utility-driven 可限制在 5% 内 | Cascade, arXiv:2506.20675 |

---

## 经验教训

### 1. 接受率已被钉死在 maximal coupling 上界

$\beta = 1 - D_{\mathrm{TV}}(p,q)$ 不只是本方案的成绩，而是任何「以 $q$ 为 proposal 接受为 $p$ 样本」方案的概率上限。工程改进只剩两个自由度：让 $q$ 更接近 $p$（EAGLE / MTP / 蒸馏），或让 $c$ 更接近 0（n-gram / 特征层小 draft）。任何宣称「改进接受规则本身」的工作都值得先怀疑。

### 2. 无偏性的来源是测度分解，不是换元

$p = \min(p,q) + (p-q)_+$ 是逐点恒等式，整个证明只需要它 + 拒绝概率 $= D_{\mathrm{TV}}$ 的配平。不要求 $\mathrm{supp}(q) \supseteq \mathrm{supp}(p)$，没有 Jacobian——把它和连续空间 change-of-variables 混为一谈是面试常见错误。

### 3. i.i.d. 假设是近似，公式值与实测值必须并列引用

Leviathan Table 2 存在实测高于 $c=0$ 理论值的行（2.64x vs 3.1x），论文归因于 i.i.d. 近似与实现细节（§A.3）。用 $\frac{1-\alpha^{\gamma+1}}{(1-\alpha)(\gamma c+1)}$ 做容量规划时，注意 $\alpha$ 本身是 Corollary 3.6 意义下的 prefix 期望，逐位独立性并不严格成立。

### 4. memory-bound 前提决定盈亏，高 QPS 下会翻转成减速

低 QPS 1.5–2.8x 加速 vs 高 QPS 1.4–1.8x 减速（vLLM 博客），根源是 Theorem 3.11 的算力放大在 compute-bound 工况下无处隐藏。生产部署必须配动态 speculative length 或 utility-driven 启停（Cascade：utility < 1 即关闭）。

### 5. $\alpha$ 与 $c$ 的 trade-off 不能被「更大的 draft」骗过

Leviathan Table 2 中 T5-large draft 的 $\alpha$ 最高（0.82）但加速最低（1.7X）——$c$ 涨得比 $\alpha$ 快。选 draft 看的是加速比公式的整体，不是单看接受率。分布式场景还要匹配硬件拓扑（Chen 的 4B 宽浅 draft 教训）。

### 6. 无损性是卖点也是约束：放松它就换到接受率

Medusa 的 typical acceptance 在 T>0 时不保证无损（EAGLE-3 据此只在 T=0 与其比较）。凡是「放宽接受条件提高接受率」的变体，都要问一句：输出分布还是严格等于 $p$ 吗？

### 7. 可复现性警示（本主题数据的水分）

- vLLM 官方博客的 1.5–2.8x 被 issue #10318（2024-11-14）质疑不可复现（复现者 batch 1 最高仅 1.4x）——引用必须附带争议说明。
- DeepSeek-V3 MTP 接受率存在两个版本：技术报告 §5.4.3 写 85–90%（本笔记采用），后续 *Insights into DeepSeek-V3* 写 80–90%，差异原因不明。
- 二手来源数字（如 LayerSkip 接受率 0.5–0.65）未核实，不入库。

### 8. Monte Carlo 校正逻辑可以压缩 wall-clock，不只是降方差

对渲染背景的人：speculative sampling 是「proposal → accept/reject → residual 补偿」骨架在采样精确性要求下的最强形态——每轮精确、无权重、无渐近。它提示 RIS/ReSTIR 家族的另一条演化方向：把校正机制从「降低估计方差」转用于「消除串行依赖的延迟」。

---

## 参考

1. Leviathan, Kalman, Matias. *Fast Inference from Transformers via Speculative Decoding*. ICML 2023. arXiv:2211.17192. https://arxiv.org/abs/2211.17192
2. Chen et al. *Accelerating Large Language Model Decoding with Speculative Sampling*. 2023. arXiv:2302.01318. https://arxiv.org/abs/2302.01318
3. Cai et al. *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*. ICML 2024. arXiv:2401.10774. https://arxiv.org/abs/2401.10774
4. Li et al. *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty*. ICML 2024. arXiv:2401.15077. https://arxiv.org/abs/2401.15077
5. Li et al. *EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees*. EMNLP 2024. arXiv:2406.16858. https://arxiv.org/abs/2406.16858
6. Li et al. *EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test*. 2025. arXiv:2503.01840. https://arxiv.org/abs/2503.01840
7. Xia et al. *Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding*（Spec-Bench）. ACL 2024. arXiv:2401.07851. https://arxiv.org/abs/2401.07851
8. DeepSeek-AI. *DeepSeek-V3 Technical Report*（§5.4.3 MTP 评估）. 2024. arXiv:2412.19437. https://arxiv.org/abs/2412.19437
9. Gloeckle et al. *Better & Faster Large Language Models via Multi-token Prediction*. Meta, 2024.（arXiv 编号二手来源，未核实）
10. Yang et al. *Inference with Reference: Lossless Acceleration of Large Language Models*（LLMA）. 2023. arXiv:2304.04487. https://arxiv.org/abs/2304.04487
11. Saxena. *Prompt Lookup Decoding*. 2023. https://github.com/apoorvumang/prompt-lookup-decoding
12. vLLM Team. *How Speculative Decoding Boosts vLLM Performance by up to 2.8x*. 2024-10-17. https://vllm-project.github.io/2024/10/17/spec-decode.html
13. vLLM GitHub Issue #10318（复现性质疑）. 2024-11-14. https://github.com/vllm-project/vllm/issues/10318
14. Jeon et al. *Utility-Driven Speculative Decoding for Mixture-of-Experts*（Cascade）. MICRO 2025. arXiv:2506.20675. https://arxiv.org/abs/2506.20675
15. Amazon Science. *BASS: Batched Attention-optimized Speculative Sampling*. 2024. https://cdn.amazon.science/01/a8/0d859c084dd7815ec8103a9025fb/bass-batched-attention-optimized-speculative-sampling.pdf
16. Amazon. *Accelerating Production LLMs with Combined Token/Embedding Speculators*. 2024. arXiv:2404.19124. https://arxiv.org/abs/2404.19124
17. *Nightjar: Dynamic Adaptive Speculative Decoding for Large Language Models Serving*. 2025. arXiv:2512.22420. https://arxiv.org/abs/2512.22420
18. Miao et al. *SpecInfer: Accelerating Generative LLM Serving with Speculative Inference and Token Tree Verification*. 2023. arXiv:2305.09781. https://arxiv.org/abs/2305.09781
19. Stern, Shazeer, Uszkoreit. *Blockwise Parallel Decoding for Deep Autoregressive Models*. NeurIPS 2018. arXiv:1811.03115. https://arxiv.org/abs/1811.03115
20. Hu & Huang. *Accelerated Speculative Sampling Based on Tree Monte Carlo*. ICML 2024.（存在性经第三方参考文献确认，arXiv 编号未核实）
