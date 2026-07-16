# 调研简报：Speculative Decoding 的蒙特卡洛框架分析

- **调研日期**：2026-07-16
- **用途**：供下游写作者撰写《04-性能优化备忘录》speculative decoding 章节
- **范围**：两篇原始论文的算法与数学框架；rejection sampling / Monte Carlo 形式化；期望产出与加速比公式；无偏性证明；工程实测数据（含减速工况）；主要变体对比；与经典 Monte Carlo 方法对照
- **方法**：只读调研，优先一手来源（arXiv 原论文、官方仓库、官方 benchmark / 博客）。所有关键数据点附来源；未能核实的数字在第十节集中列出并标注「未核实」

---

## 一、核心结论摘要

1. **Speculative sampling 本质是逐 token 的 modified rejection sampling**：以 draft 分布 $q$ 为 proposal、target 分布 $p$ 为目标，接受概率 $\min(1, p(x)/q(x))$；拒绝时从残差分布 $\mathrm{norm}(\max(0, p-q))$ 重采样。单步恒等式 $\min(p,q) + (p-q)_+ = p$ 保证输出分布**严格等于** target 分布（精确无损，非近似）。[Leviathan et al. 2023 §2.3 与 App A.1；Chen et al. 2023 Theorem 1]
2. **单 token 接受率有闭式解**：$\beta = \sum_x \min(p(x), q(x)) = 1 - D_{\mathrm{TV}}(p,q)$。这正是 $p$ 与 $q$ 的 maximal coupling 中两样本相等的最大概率——即该接受规则达到了任何「把 $q$ 样本当作 $p$ 样本接受」方案的理论上限；后续改进只能在提高 $q$（缩小 $D_{\mathrm{TV}}$）与降低 draft 成本 $c$ 两个方向。[Leviathan et al. 2023 Theorem 3.5]
3. **期望产出与加速比**：在 i.i.d. 接受率 $\alpha$ 假设下，单轮期望产出 $E[\#\text{tokens}] = \frac{1-\alpha^{\gamma+1}}{1-\alpha}$（capped geometric），期望 wall-clock 加速比 $= \frac{1-\alpha^{\gamma+1}}{(1-\alpha)(\gamma c + 1)}$，其中 $c$ 为 draft/target 单步耗时比。理论上界 $1/(1-\alpha)$（$c\to 0$ 或大 $\gamma$ / oracle-$\gamma$）。[Leviathan et al. 2023 §3]
4. **实测加速比**：Leviathan T5-XXL 2.3–3.4x；Chen Chinchilla 70B 2–2.5x；EAGLE MT-bench ~3x；EAGLE-3 达 3.0–6.5x。但加速强依赖工况：vLLM 实测低 QPS 下 1.5–2.8x，**高 QPS（compute-bound）下反而 1.4–1.8x 减速**；MoE 模型上可至 1.5x 减速。[Leviathan 2023 Table 2；Chen 2023；EAGLE-3 2025；vLLM 官方博客 2024-10-17；Cascade 2025]
5. **变体演进主线 = 提高 $\alpha$（或接受长度 $\tau$）× 压低 $c$**：独立 draft model → n-gram / prompt lookup（$c\approx 0$）→ Medusa 多头 → EAGLE 特征层草稿（draft accuracy ≈0.8）→ EAGLE-2/3 动态树 + training-time test → MTP 把草稿能力内化进主模型预训练（DeepSeek-V3 第二 token 接受率 85–90%，1.8x TPS）。
6. **与经典 Monte Carlo 的关系**：共享 $\min(1,\cdot)$ 接受核与 likelihood ratio，但机制不同——classic rejection sampling 需要包络常数 $M$ 且拒绝即废弃；importance sampling 产出加权样本而非无加权精确样本；Metropolis-Hastings 拒绝时驻留原状态（相关样本、渐近精确）。Speculative sampling 拒绝时从残差分布重采样，每轮产出精确服从 $p$ 的样本且至少前进 1 token，是「带残差补偿的一步精确采样」。

---

## 二、两篇原始论文：算法描述与数学框架

### 2.1 Leviathan, Kalman & Matias 2023（Google Research，ICML 2023）

来源：*Fast Inference from Transformers via Speculative Decoding*，arXiv:2211.17192（v1 2022-11-30，v2 2023-05-18），PMLR 202:19274–19286。https://arxiv.org/abs/2211.17192

**记号**（本简报统一采用此文记号）：$M_p$ 为 target model，$p(x_t \mid x_{<t})$ 为 target 分布；$M_q$ 为 approximation（draft）model，$q(x_t \mid x_{<t})$ 为 draft 分布。argmax / top-k / nucleus / temperature 均可归一化为「从调整后的分布做标准采样」，故框架只讨论标准采样（§2.2）。

**算法（Algorithm 1, SpeculativeDecodingStep）**：

1. $M_q$ 自回归采样 $\gamma$ 个猜测 $x_1, \dots, x_\gamma$，逐步记录 $q_i(x) = M_q(\mathrm{prefix} + [x_1,\dots,x_{i-1}])$；
2. $M_p$ **一次并行前向**算出 $\gamma+1$ 个分布 $p_1(x), \dots, p_{\gamma+1}(x)$（分别对应 prefix, prefix+$x_1$, …, prefix+$x_1..x_\gamma$）；
3. 采样 $r_i \sim U(0,1)$，确定接受数 $n \leftarrow \min\left(\{i-1 \mid 1 \le i \le \gamma,\ r_i > \tfrac{p_i(x_i)}{q_i(x_i)}\} \cup \{\gamma\}\right)$，即从左到右首个被拒绝位置之前；
4. 若 $n < \gamma$：从修正分布 $p'(x) = \mathrm{norm}(\max(0, p_{n+1}(x) - q_{n+1}(x)))$ 采样 $t$；若 $n = \gamma$：从 $p_{\gamma+1}$ 正常采样 $t$；
5. 返回 $\mathrm{prefix} + [x_1,\dots,x_n, t]$，每轮产出 $1$ 到 $\gamma+1$ 个 token。

关键性质：每轮**至少**产出 1 个 token（拒绝时重采样兜底），因此串行调用 $M_p$ 的次数最坏情况也不多于标准自回归解码。

### 2.2 Chen et al. 2023（DeepMind）

来源：*Accelerating Large Language Model Decoding with Speculative Sampling*，arXiv:2302.01318（v1 2023-02-02）。https://arxiv.org/abs/2302.01318

与 Leviathan 独立同期工作，称 **speculative sampling (SpS)**。注意此文记号相反：$q$ = target，$p$ = draft。要点：

- 提出 lookahead $K$ 与 **modified rejection sampling**：接受 $\tilde{x}$ 的概率 $\min\big(1, \tfrac{q(\tilde{x}\mid \cdot)}{p(\tilde{x}\mid \cdot)}\big)$；拒绝则从 $(q-p)_+$ 归一化后的分布重采样；$K$ 个 draft 全部接受时从 target 的下一组 logits 正常采样第 $K+1$ 个 token。每轮产出 1 到 $K+1$ 个 token。
- 系统分析「为何短 continuation 的并行 scoring 与单 token 采样延迟相当」：linear layers（小 batch 下 memory-bound）、attention（KV-cache 大小不随 $K$ 变）、all-reduce（小消息 latency-bound）三个时间构成在小 $K$ 下均不随 $K$ 显著增长。
- 分布式 serving 工程：为 Chinchilla 70B（16×TPU v4，14.1 ms/token）专门训练**宽而浅**的 4B draft（8 层、同 16×TPU v4 拓扑，1.8 ms/token，$c \approx 0.128$）；指出朴素选小模型当 draft 会因其最优拓扑不同而浪费硬件（7B 在 4×TPU v4 上 5 ms/token 但搬上 16×TPU 反而更慢）。
- 实测：batch 1、$K=4$，XSum（11,305 序列，nucleus $p=0.8$）与 HumanEval（16,400 样本，$p=0.95$）总体 2–2.5x，HumanEval 接近 2.5x，benchmark 指标与自回归采样持平；XSum 最优 $K=3$；$K$ 增大则序列级延迟方差上升（P90/P99 风险）。

### 2.3 异同

- **同**：接受规则与残差重采样完全一致；均证明输出分布不变；均立足 memory-bandwidth-bound 前提，用并发换延迟。
- **异**：Leviathan 给出完整的 $\alpha$ / 期望 token 数 / walltime / 算力放大理论（本简报第三、四节）与 T5-XXL 端到端 walltime 实测；Chen 侧重分布式 serving 工程与 modified rejection sampling 的命名和证明。
- 概念前身：Stern et al. 2018 *Blockwise Parallel Decoding*（arXiv:1811.03115）——仅支持 greedy、需改训练与模型结构、不保证同分布。

---

## 三、Monte Carlo 形式化：接受概率与 $\alpha$ 的推导

### 3.1 逐 token 接受规则即 rejection sampling 核

给定 prefix（以下省略条件记号），draft 给出 $x \sim q$。接受规则：

$$A(x) = \min\!\Big(1,\ \frac{p(x)}{q(x)}\Big)$$

这正是 rejection sampling 的接受核。区别在于：经典 RS 要求包络 $M \cdot q(x) \ge p(x)$ 并以 $p(x)/(M q(x))$ 接受；此处允许 $q$ 在部分支撑集上低于 $p$，「欠采样」部分由拒绝后的残差重采样精确补偿（见第五节无偏性证明）。

### 3.2 接受率闭式：$\beta = \sum_x \min(p,q) = 1 - D_{\mathrm{TV}}(p,q)$

推导（Leviathan Theorem 3.5 + Lemma 3.3）：

$$\beta = E_{x\sim q}\Big[\min\Big(1,\frac{p(x)}{q(x)}\Big)\Big] = \sum_x q(x)\min\Big(1,\frac{p(x)}{q(x)}\Big) = \sum_x \min\big(p(x), q(x)\big)$$

利用恒等式 $\min(a,b) = \tfrac{a+b-|a-b|}{2}$ 与 $\sum_x p = \sum_x q = 1$：

$$\sum_x \min(p,q) = \tfrac{1}{2}\sum_x (p+q) - \tfrac{1}{2}\sum_x |p-q| = 1 - \tfrac{1}{2}\lVert p - q \rVert_1 = 1 - D_{\mathrm{TV}}(p,q)$$

其中 $D_{\mathrm{TV}}(p,q) = \tfrac{1}{2}\lVert p-q\rVert_1$ 为 total variation distance。Leviathan 原文以 $D_{LK}(p,q) = \sum_x |p(x) - \tfrac{p(x)+q(x)}{2}|$ 定义（Definition 3.2），数值上恰等于 $D_{\mathrm{TV}}$；Corollary 3.4：$D_{LK} \in [0,1]$，$=0 \iff p=q$，$=1 \iff$ 支撑集不交。

对 prefix 取期望得整体接受率（Corollary 3.6）：

$$\alpha = E\big[\beta\big] = E_{\text{prefix}}\Big[1 - D_{\mathrm{TV}}\big(p(\cdot\mid \text{prefix}),\ q(\cdot\mid \text{prefix})\big)\Big]$$

即 **$\alpha$ 是 draft 与 target 逐步分布重叠度的期望**；$\alpha \to 1$ 当且仅当 $q \to p$。

### 3.3 Maximal coupling 视角（本简报的分析性注记）

耦合不等式：对任意满足 $X \sim q$、$Y \sim p$ 的联合分布，$P(X = Y) \le 1 - D_{\mathrm{TV}}(p,q)$，等号由 maximal coupling 达到。Maximal coupling 的构造正是：以概率 $\sum_x \min(p,q)$ 从归一化的 $\min(p,q)$ 采一个公共值；否则分别从 $(q-p)_+$ 与 $(p-q)_+$ 采样。Speculative sampling 的接受-重采样流程就是该耦合的算法化：**接受事件恰好对应 coupling 中 $X = Y$ 的分支**。因此 $1 - D_{\mathrm{TV}}$ 不仅是本方案的接受率，也是任何「把 $q$ 样本直接当作 $p$ 样本接受」方案的概率上限——在这个意义上 speculative sampling 的接受概率已是最优；工程改进空间只在 (i) 让 $q$ 更接近 $p$（缩小 $D_{\mathrm{TV}}$，即 EAGLE/MTP/蒸馏路线）与 (ii) 降低 $c$（n-gram、特征层小 draft 路线）。

---

## 四、期望产出与期望加速比

### 4.1 期望 token 数（capped geometric）

假设各位置接受率 i.i.d. 为 $\alpha$（Leviathan §3.1 的简化假设）。记 $N$ 为单轮产出 token 数，$N \in \{1, \dots, \gamma+1\}$：

$$P(N > k) = P(\text{前 } k \text{ 个 draft 全被接受}) = \alpha^k,\quad 0 \le k \le \gamma$$

$$E[N] = \sum_{k=0}^{\gamma} P(N > k) = \sum_{k=0}^{\gamma} \alpha^k = \frac{1 - \alpha^{\gamma+1}}{1 - \alpha} \quad\text{—— Leviathan Eq. (1)}$$

（等价表述：$N$ 是「成功率 $1-\alpha$、截断于 $\gamma+1$」的几何变量；$\gamma \to \infty$ 时 $E[N] \to \frac{1}{1-\alpha}$。）

### 4.2 期望 wall-clock 加速比

设 $M_p$ 单步耗时 $T$，$c$ 为 $M_q$ 与 $M_p$ 单步耗时之比（Definition 3.7；Leviathan 实验中 $c < 0.05$）。单轮成本 $T(\gamma c + 1)$（$\gamma$ 次 draft 串行 + 1 次 target 并行验证），期望产出 $E[N]$：

$$\text{期望加速比} = \frac{1 - \alpha^{\gamma+1}}{(1 - \alpha)\,(\gamma c + 1)} \quad\text{—— Leviathan Theorem 3.8}$$

- **推论（Corollary 3.9）**：只要 $\alpha > c$ 就存在使加速 $>1$ 的 $\gamma$，且加速至少为 $\dfrac{1+\alpha}{1+c}$（$\gamma = 1$ 时取得该下界）。
- **极限**：$c \to 0$ 且 $\gamma$ 大时加速 $\to E[N] \to \dfrac{1}{1-\alpha}$；若能预知每步最优 $\gamma$（oracle-$\gamma$），$E[\#\text{tokens}] = \frac{1}{1-\alpha}$，论文估计 walltime 改善可比固定 $\gamma$ 再高约 60%（§3.5，假设算力无限）。
- **最优 $\gamma$**：最大化上式的整数解，论文 Figure 3 给出数值搜索曲线。
- 理论示例（$c = \hat{c} = 0$，Table 1）：$\alpha=0.8, \gamma=5 \Rightarrow 3.69\text{x}$；$\alpha=0.9, \gamma=10 \Rightarrow 6.86\text{x}$。

### 4.3 算力放大与内存访问缩减（Theorem 3.11 与 §3.4）

$$\text{总算力期望放大因子} = \frac{(1-\alpha)(\gamma\hat{c} + \gamma + 1)}{1 - \alpha^{\gamma+1}}$$

$\hat{c}$ 为 $M_q$ 与 $M_p$ 单 token 算力之比。$\alpha$ 低时总算力浪费显著——这是高 QPS 下减速的理论根源（第六节）。相反，$M_p$ 权重与 KV cache 的读取次数按 $E[N]$ 倍缩减。**Speculative decoding 的经济学本质：用更多 FLOPs 换更少 memory access，仅当系统处于 memory-bound 工况时才是净收益。**

---

## 五、无偏性证明：输出分布 $\equiv p$

### 5.1 单 token 恒等式

**定理**（Leviathan App A.1；Chen Theorem 1）：按 §3.1 规则产生的样本 $X$ 满足 $X \sim p$。

**证明**（采用本简报记号 $p$=target、$q$=draft；Chen 原文记号相反，已换算；该恒等式推导与 Chen 原文 Theorem 1 逐步对应）：

$$P(X = x) = \underbrace{P(\tilde{x} = x)\,P(\text{接受} \mid \tilde{x} = x)}_{\text{分支一：采到并接受的}}+ \underbrace{P(\text{拒绝})\,P(X = x \mid \text{拒绝})}_{\text{分支二：拒绝后从残差重采}}$$

分支一：$q(x)\min\big(1, \tfrac{p(x)}{q(x)}\big) = \min\big(p(x), q(x)\big)$。

拒绝概率：

$$P(\text{拒绝}) = 1 - \sum_{x'}\min(p,q) = \sum_{x'}\big(q(x') - \min(p,q)\big) = \sum_{x'}\big(q(x') - p(x')\big)_+$$

由 $\sum_x (p - q) = 0$ 知 $\sum_x (p-q)_+ = \sum_x (q-p)_+ = D_{\mathrm{TV}}(p,q)$，即 **拒绝概率 $= D_{\mathrm{TV}}$**。

分支二：残差分布 $r(x) = \dfrac{(p(x)-q(x))_+}{\sum_{x'} (p-q)_+}$，故

$$P(\text{拒绝}) \cdot r(x) = \Big(\sum_{x'}(q-p)_+\Big) \cdot \frac{(p(x)-q(x))_+}{\sum_{x'}(p-q)_+} = \big(p(x) - q(x)\big)_+$$

合计：

$$P(X = x) = \min\big(p(x), q(x)\big) + \max\big(0,\ p(x) - q(x)\big) = p(x) \qquad \blacksquare$$

### 5.2 序列层面

每轮的修正分布 $p'$ 都以**已接受 prefix 为条件**，单步恒等式对每个位置成立；由链式法则归纳，整条轨迹的联合分布等于 target 模型的自回归分布。两篇论文均声明输出分布「identical within hardware numerics」：浮点数值误差与 PRNG 使用差异意味着实现上输出序列可能不逐 token 相同，但**分布**相同（Chen et al. 以 XSum/HumanEval 指标持平做了经验验证）。

### 5.3 关于 change of variables 的注记

严格说本框架**不需要**连续变量的 Jacobian 换元——它是离散测度分解：

$$p = \underbrace{\min(p,q)}_{\text{被 proposal 覆盖的部分}} + \underbrace{(p - q)_+}_{\text{残差部分}}$$

接受分支与重采样分支分别精确实现这两个测度分量，两者权重由拒绝概率 $D_{\mathrm{TV}}$ 自动配平。这是逐点的测度恒等式，且比连续换元更宽松：**不要求 $q$ 的支撑覆盖 $p$ 的支撑**（$q(x) = 0$ 处自然落入残差分支）。

---

## 六、工程现实：实测加速比与减速工况

### 6.1 原论文报告值

**Leviathan et al. 2023**（T5-XXL 11B 为 $M_p$，单 TPU-v4，batch 1；Table 2 实测 walltime，基线为 T5X 实现）：

| 任务 | $M_q$ | 采样 | $\gamma$ | $\alpha$ | 加速比 |
|---|---|---|---|---|---|
| EnDe 翻译 | T5-small (77M) ★ | argmax (T=0) | 7 | 0.75 | **3.4X** |
| EnDe 翻译 | T5-base (250M) | argmax | 7 | 0.80 | 2.8X |
| EnDe 翻译 | T5-large (800M) | argmax | 7 | 0.82 | 1.7X |
| EnDe 翻译 | T5-small ★ | 标准采样 (T=1) | 7 | 0.62 | **2.6X** |
| EnDe 翻译 | T5-base | 标准采样 | 5 | 0.68 | 2.4X |
| EnDe 翻译 | T5-large | 标准采样 | 3 | 0.71 | 1.4X |
| CNN/DM 摘要 | T5-small ★ | argmax | 5 | 0.65 | **3.1X** |
| CNN/DM 摘要 | T5-base | argmax | 5 | 0.73 | 3.0X |
| CNN/DM 摘要 | T5-large | argmax | 3 | 0.74 | 2.2X |
| CNN/DM 摘要 | T5-small ★ | 标准采样 | 5 | 0.53 | **2.3X** |
| CNN/DM 摘要 | T5-base | 标准采样 | 3 | 0.55 | 2.2X |
| CNN/DM 摘要 | T5-large | 标准采样 | 3 | 0.56 | 1.7X |

（★ 为各设置下最优。观察：$\alpha$ 随 draft 变大而升，但 $c$ 上升更快——T5-large 的 $\alpha$ 最高却加速最低，印证 $\alpha$ 与 $c$ 的 trade-off；argmax 的 $\alpha$ 与加速均高于标准采样。）

**Leviathan Table 3（10K token 上实测的 $\alpha$ 值，节选）**：GPT-like 97M/6M：0.88（T=0）/0.89（T=1）；EnDe bigram：0.20（T=0，$c\approx 0$，$\gamma=3$ 时 1.25X）；CNN/DM bigram：0.23；LaMDA 137B 配 LaMDA-100M / 2B / 8B：T=0 时 0.61 / 0.71 / 0.75，T=1 时 0.57 / 0.71 / 0.74。结论：小两个数量级的 draft 通常给出 $\alpha \in [0.5, 0.9]$；分布越尖锐（低温/argmax）$\alpha$ 越高；即使 unigram/bigram 也有非零 $\alpha$。

**一致性验算（本简报自行计算）**：EnDe T5-small T=0 一行，公式给出 $\frac{1-0.75^8}{0.25(7c+1)} = \frac{3.6}{7c+1}$，代入实测 3.4X 反解 $c \approx 0.8\%$，与论文「$c < 0.05$」自洽。注意 i.i.d. 假设是近似，个别行实测值略高于 $c=0$ 的理论值，论文归因于实现细节（§A.3）。

**Chen et al. 2023**：Chinchilla 70B + 4B draft，$K=4$，batch 1，XSum 与 HumanEval 总体 **2–2.5x**；接受率随域变化（代码域显著更高：公共子序列多、token 更短、低温使分布更尖锐）；XSum 延迟最优 $K=3$；$K$ 增大则均值加速趋于平台甚至回退、且全序列生成时间方差上升。

### 6.2 Spec-Bench（Xia et al. 2024）

来源：*Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding*（含 Spec-Bench），arXiv:2401.07851，ACL 2024。https://arxiv.org/abs/2401.07851

设置：6 子任务 × 80 样本（MT-bench / WMT14 DE-EN / CNN-DM / Natural Questions / GSM8K / DPR-RAG），Vicuna-7B FP16，单 RTX 3090，batch 1：

- greedy（T=0）：**EAGLE 总体最快，1.8–2.4x**（数学推理子任务 ~2.4x）；PLD 在摘要等输入-输出高重叠任务 ~2.4x，但翻译/QA 仅 1.1–1.3x；
- 温度升高时所有方法加速比下降（EAGLE 1.7–2.1x）：高温使分布变平、$D_{\mathrm{TV}}$ 增大、$\alpha$ 下降，与 §3.2 公式一致。

### 6.3 高 QPS / 大 batch 下的减速（1.4–1.8x）及原因

**vLLM 官方博客实测**（*How Speculative Decoding Boosts vLLM Performance by up to 2.8x*，2024-10-17，Llama3-70B，4×H100。https://vllm-project.github.io/2024/10/17/spec-decode.html）：

| 工况 | 数据集 / 方法 | 结果 |
|---|---|---|
| QPS=1 | ShareGPT，draft model（turboderp/Qwama-0.5B-Instruct） | **1.5x 加速** |
| QPS=1 | CNN/DailyMail，n-gram（prompt lookup） | **2.8x 加速** |
| 高 QPS | ShareGPT，draft model | **1.4x 减速** |
| 高 QPS | CNN/DailyMail，n-gram | **1.8x 减速** |

**减速原因分析**（综合以下来源）：

- **(a) 工况翻转（memory-bound → compute-bound）**：低 batch 时 decode 受 memory bandwidth 限制，并行验证 $\gamma$ 个 token 几乎免费；高 QPS 下 continuous batching 已把 GPU 打满为 compute-bound，验证的额外 FLOPs 直接转化为延迟（vLLM 博客原文；Nightjar, arXiv:2512.22420, 2025：RTX 4090 + DeepSeek-R1-Distill-Qwen-7B，$\gamma=3$ 在 15 QPS 提升吞吐 15.5%，高负载下最多退化 30.25%）。
- **(b) 算力放大**：Theorem 3.11 的放大因子在 $\alpha$ 中等时 $>1$；吞吐导向场景中总 FLOPs 就是成本，speculation 变成「throughput tax」。
- **(c) batch 内接受稀释**：朴素实现中 batch 内任一序列在某位置拒绝即全体停止接受，等效 per-position 接受率变为 $\alpha^b$（Amazon BASS 论文 *Batched Attention-optimized Speculative Sampling*：$\alpha=0.8$、$b=5$ 时降至 $0.8^5 \approx 33\%$，期望前进仅 ~1.5 token）。需要 per-sequence 可变接受 + KV cache 裁剪，工程复杂度高。
- **(d) MoE 病理**：draft token 集合激活更多 expert，验证阶段权重搬运量上升、验证耗时增加 2–3x；speculation 在 MoE 上可致最多 **1.5x 减速**（Cascade: *Utility-Driven Speculative Decoding for Mixture-of-Experts*，arXiv:2506.20675，MICRO 2025；对照组 dense LLaMA-3-8B n-gram speculation 开销仅 5–10%，TPOT 加速 1.4–1.8x）。
- **(e) 长 prompt + 大 batch 组合**：Amazon *Accelerating Production LLMs with Combined Token/Embedding Speculators*（arXiv:2404.19124）报告该工况下 speculative decoding 可比非投机解码**慢 2 倍以上**（验证把每步 token 数从 $b$ 放大到 $b(\gamma+1)$，超出 A100 甜区）。
- **(f) 可复现性争议**：vLLM GitHub issue #10318（2024-11-14）报告按博客设置复现，batch 1 下最高仅 1.4x 加速，且 E2E 延迟远差于博客数字，要求公开完整实验配置。引用 vLLM 数据时应注明此争议。
- **对策方向**：动态 speculative length（vLLM roadmap、Nightjar、SmartSpec）、按负载启停 speculation（Cascade 的 utility-driven 方案：utility < 1 即关闭，将 MoE 减速限制在 5% 内并提升吞吐 7–14%）。

---

## 七、主要变体对比

| 变体 | 来源（年份） | 草稿机制 | 接受率 / 接受长度 | 训练成本 | 报告加速比 |
|---|---|---|---|---|---|
| 独立 draft model（SpS 原始形态） | Leviathan 2023；Chen 2023 | 同系列小模型自回归产出 $\gamma$ token | $\alpha \approx 0.53$–$0.89$（任务/draft 规模相关） | 可用现成 checkpoint；Chen 专门训练 4B draft（同数据、同 tokenizer，宽浅拓扑） | T5-XXL 2.3–3.4x；Chinchilla 2–2.5x |
| n-gram / bigram | Leviathan 2023 §4.2 | 查表，$c \approx 0$ | EnDe bigram $\alpha \approx 0.20$ | 0 | 1.25x（$\gamma=3$）；vLLM n-gram CNN/DM 2.8x @QPS=1 |
| Prompt Lookup / LLMA | Saxena 2023（GitHub）；Yang et al. 2023 | 从输入 / 参考文档复制匹配 span 当 draft | 任务依赖（高重叠场景高） | 0（免训练） | LLMA >2x（重叠场景，greedy 无损）；Spec-Bench 摘要 ~2.4x |
| Medusa 多头 | Cai et al. 2024 | 冻结/联合微调 backbone 上加多个 decoding head，tree attention 同时验证多条候选 | 引入 typical acceptance 放宽接受条件（T>0 时**不保证无损**） | Medusa-1：冻结 backbone 只训 heads；Medusa-2：联合微调（需保护 backbone 的 recipe）；支持 self-distillation | Medusa-1 >2.2x；Medusa-2 2.3–3.6x |
| EAGLE | Li et al. 2024 | 单层 Transformer decoder 在 **second-top-layer 特征**上自回归，并输入超前一步的 token 消除特征不确定性 | draft accuracy ≈ 0.8；平均每次前向产出近 4 token | ShareGPT ~68k–70k 对话（2–4B token），可训练参数 0.24B(7B)–0.99B(70B)，4×A100(40G) 训 1–2 天（70B） | MT-bench greedy ~3x（2x Lookahead、1.6x Medusa）；gpt-fast LLaMA2-Chat 7B 24.5 → 160.4 tok/s（RTX 3090） |
| EAGLE-2 | Li et al. 2024 | EAGLE + context-aware **dynamic draft tree**（按 draft 置信度扩展与重排） | 接受长度高于 EAGLE（draft 置信度 well-calibrated，近似接受率） | 同 EAGLE | 3.05–4.26x（比 EAGLE-1 快 20–40%），保持无损 |
| EAGLE-3 | Li et al. 2025 | **training-time test**（训练时模拟推理期的多层特征输入）+ 多层特征融合 | 接受长度至 7.5（HumanEval）；接受率不随 draft 自回归步数衰减 | 同族，训练数据规模扩大（如 DeepSeek-R1-Distill-LLaMA-8B 用 OpenThoughts-114k-math） | 3.0–6.5x（比 EAGLE-2 快 20–40%），HumanEval 达 6.5x |
| MTP（Multi-Token Prediction） | Gloeckle et al. 2024；DeepSeek-V3 2024 | 主模型内嵌 MTP 模块（每个仅 1 层）预测未来 token，推理时作 self-draft | DeepSeek-V3 第二 token 接受率 **85–90%** | 预训练时与主模型联合训练（不可事后插装） | DeepSeek-V3：**1.8x TPS** |
| Self-speculative（early exit） | Elhoushi et al. 2024（LayerSkip） | 前 $L$ 层提前退出当 draft，全层验证 | 一手数字未核实（二手称 0.5–0.65） | 0（可选 self-distillation 微调） | 一手数字未核实 |
| Token tree 验证 | Miao et al. 2023（SpecInfer） | 多 draft / 树状候选 + tree-based parallel verification | —（推广单链为树） | collective boost-tuning 微调小模型 | —（见第八节注记） |

**变体分述要点**：

- **独立 draft model**：$\alpha$ 与 $c$ 的直接 trade-off，Leviathan 建议 draft 比 target 小约两个数量级；分布式场景下 draft 的硬件拓扑需与 target 匹配（Chen 的教训）。
- **n-gram / prompt lookup**：$c \approx 0$ 的极端路线，免训练免部署第二个模型；收益完全取决于输入-输出重叠度（摘要、RAG、多轮对话、代码编辑强，开放生成弱）。
- **Medusa**：单模型工件、运维最简单；但头间独立预测忽略 token 间依赖，且 typical acceptance 在非 greedy 下牺牲严格无损性（EAGLE-3 论文据此只在 T=0 与 Medusa 比较）。
- **EAGLE 系**：核心洞见是「特征层自回归比 token 层更容易」（one-layer draft 上特征路线准确率比 token 路线高约 30%），加上「超前一步 token 消除特征不确定性」；EAGLE-2 发现 draft 置信度是 well-calibrated 的接受率近似，据此做动态树；EAGLE-3 用 training-time test 消除训练-推理输入分布失配，接受率不再随 draft 步数衰减。
- **MTP**：把草稿能力内化进预训练目标，$c$ 极低（单层）且与主模型深度对齐；代价是与主模型权重耦合，无法即插即用，仅适用于自研模型。

---

## 八、与经典 Monte Carlo 方法的同构与差异

| 维度 | Classic rejection sampling | Importance sampling | Metropolis-Hastings | **Speculative sampling** |
|---|---|---|---|---|
| Proposal | $q$，且需包络 $M q \ge p$ | $q$（支撑覆盖即可） | 依赖当前状态的转移核 $q(\cdot \mid x)$ | draft 模型 $q$（逐 token 条件分布） |
| 接受概率 | $\frac{p(x)}{M q(x)}$ | 无接受/拒绝（全保留，赋权 $w = p/q$） | $\min\Big(1, \frac{p(x')q(x\mid x')}{p(x)q(x'\mid x)}\Big)$ | $\min\big(1, \frac{p(x)}{q(x)}\big)$ |
| 拒绝行为 | 样本废弃重抽（期望 $M$ 次/样本） | 无 | **驻留**当前状态（样本相关） | 从残差分布 $\mathrm{norm}((p-q)_+)$ **重采样**，当轮必有产出 |
| 输出性质 | i.i.d. 精确 $\sim p$ | 加权样本（估计无偏，样本本身不服从 $p$） | 相关样本，渐近精确 | 每轮精确 $\sim p$，轮间由链式法则保证全序列精确 |
| 接受率 | $1/M$ | — | 依赖核设计 | $1 - D_{\mathrm{TV}}(p,q)$（= maximal coupling 上界） |
| 计算结构 | 串行 | 串行/并行皆可 | 串行 Markov chain | draft 串行 + target **并行验证**（空间换时间） |
| 关键恒等式 | $p \le M q$ | $E_p[f] = E_q[f \cdot p/q]$ | detailed balance $p(x)T(x\to x') = p(x')T(x'\to x)$ | $p = \min(p,q) + (p-q)_+$ |

**同构**：

- 与 RS 共享 likelihood ratio 接受核 $\min(1, p/q)$；可以认为 speculative sampling 是「在 $q$ 覆盖区域内取 $M=1$ 的 RS + 对拒绝事件的精确回收」——经典 RS 把拒绝视为浪费，speculative 把拒绝事件本身用作切换到残差测度的随机信号。
- 与 MH 共享 $\min(1,\cdot)$ 接受形式；两者都是「proposal + 接受校正到目标分布」的 Monte Carlo 构造。

**差异**：

- **vs RS**：无需包络常数 $M$（对高维 LLM 词表，可用 $M$ 通常巨大导致 RS 接受率 $1/M$ 不可接受）；拒绝不浪费——拒绝概率恰为 $D_{\mathrm{TV}}$，且拒绝分支产出残差分布的精确样本。
- **vs IS**：IS 保留全部样本并赋权 $w = p/q$，给出加权（自归一化）估计，不产出服从 $p$ 的无加权样本；speculative 产出无权重精确样本，其「随机性代价」体现为每轮接受 token 数的 capped-geometric 波动而非权重方差。
- **vs MH**：MH 是渐近理论（burn-in、自相关、detailed balance），拒绝 = 驻留导致有效样本量下降；speculative 是**有限步精确**，拒绝 = 残差重采样，每轮至少前进 1 token，无驻留、无 burn-in。MH 的 proposal 依赖链当前状态，speculative 的 proposal 是条件独立的 draft 分布。
- **最优性**：speculative 的接受率 $1 - D_{\mathrm{TV}}$ 等于 maximal coupling 概率，是「以 $q$ 为 proposal 接受为 $p$ 样本」的理论上限（见 §3.3）；经典 RS 在给定 $M$ 下接受率 $1/M$ 一般远低于此。

**注记（树推广）**：SpecInfer（Miao et al. 2023）、EAGLE-2/3 与 Hu & Huang 2024（*Accelerated Speculative Sampling Based on Tree Monte Carlo*，ICML 2024）把单链 draft 推广为树状 proposal，对应 Monte Carlo 中 multi-proposal / 并行 MCMC 的推广方向；接受规则相应推广为树上的路径选择 + 分布校正。

---

## 九、参考文献

1. Leviathan, Y., Kalman, M., Matias, Y. *Fast Inference from Transformers via Speculative Decoding*. ICML 2023 (PMLR 202:19274–19286). arXiv:2211.17192. https://arxiv.org/abs/2211.17192
2. Chen, C., Borgeaud, S., Irving, G., Lespiau, J.-B., Sifre, L., Jumper, J. *Accelerating Large Language Model Decoding with Speculative Sampling*. 2023. arXiv:2302.01318. https://arxiv.org/abs/2302.01318
3. Cai, T., Li, Y., Geng, Z., Peng, H., Lee, J. D., Chen, D., Dao, T. *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*. ICML 2024. arXiv:2401.10774. https://arxiv.org/abs/2401.10774
4. Li, Y., Wei, F., Zhang, C., Zhang, H. *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty*. ICML 2024. arXiv:2401.15077. https://arxiv.org/abs/2401.15077
5. Li, Y., Wei, F., Zhang, C., Zhang, H. *EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees*. EMNLP 2024. arXiv:2406.16858. https://arxiv.org/abs/2406.16858
6. Li, Y., Wei, F., Zhang, C., Zhang, H. *EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test*. 2025. arXiv:2503.01840. https://arxiv.org/abs/2503.01840
7. Xia, H., Yang, Z., Dong, Q., Wang, P., Li, Y., Ge, T., Liu, T., Li, W., Sui, Z. *Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding*（含 Spec-Bench）. ACL 2024. arXiv:2401.07851. https://arxiv.org/abs/2401.07851
8. Yang, N., Ge, T., Wang, L., Jiao, B., Jiang, D., Yang, L., Majumder, R., Wei, F. *Inference with Reference: Lossless Acceleration of Large Language Models*（LLMA）. 2023. arXiv:2304.04487. https://arxiv.org/abs/2304.04487
9. Saxena, A. *Prompt Lookup Decoding*. 2023. GitHub: https://github.com/apoorvumang/prompt-lookup-decoding
10. DeepSeek-AI. *DeepSeek-V3 Technical Report*. 2024. arXiv:2412.19437（§5.4.3 MTP 评估）. https://arxiv.org/abs/2412.19437
11. Gloeckle, F., Idrissi, B. Y., Rozière, B., Lopez-Paz, D., Synnaeve, G. *Better & Faster Large Language Models via Multi-token Prediction*. Meta, 2024. arXiv:2404.19737（编号凭记忆，见第十节）
12. vLLM Team. *How Speculative Decoding Boosts vLLM Performance by up to 2.8x*. 2024-10-17. https://vllm-project.github.io/2024/10/17/spec-decode.html
13. vLLM GitHub Issue #10318: *Results from the vLLM Blog article "How Speculative Decoding Boosts vLLM Performance by up to 2.8x" are unreproducible*. 2024-11-14. https://github.com/vllm-project/vllm/issues/10318
14. Jeon, W., et al. *Utility-Driven Speculative Decoding for Mixture-of-Experts*（Cascade）. MICRO 2025. arXiv:2506.20675. https://arxiv.org/abs/2506.20675
15. Amazon Science. *BASS: Batched Attention-optimized Speculative Sampling*. 2024. https://cdn.amazon.science/01/a8/0d859c084dd7815ec8103a9025fb/bass-batched-attention-optimized-speculative-sampling.pdf
16. *Accelerating Production LLMs with Combined Token/Embedding Speculators*. 2024. arXiv:2404.19124. https://arxiv.org/abs/2404.19124
17. Miao, X., Oliaro, G., Zhang, Z., Cheng, X., Wang, Z., Wong, R. Y. Y., Chen, Z., Arfeen, D., Abhyankar, R., Jia, Z. *SpecInfer: Accelerating Generative LLM Serving with Speculative Inference and Token Tree Verification*. 2023. arXiv:2305.09781. https://arxiv.org/abs/2305.09781
18. Elhoushi, M., et al. *LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding*. ACL 2024. arXiv:2404.16710. https://arxiv.org/abs/2404.16710
19. *Nightjar: Dynamic Adaptive Speculative Decoding for Large Language Models Serving*. 2025. arXiv:2512.22420. https://arxiv.org/abs/2512.22420
20. Stern, M., Shazeer, N., Uszkoreit, J. *Blockwise Parallel Decoding for Deep Autoregressive Models*. NeurIPS 2018. arXiv:1811.03115. https://arxiv.org/abs/1811.03115
21. Hu, Z., Huang, H. *Accelerated Speculative Sampling Based on Tree Monte Carlo*. ICML 2024.（经 SpecHub 论文参考文献确认存在；arXiv 编号未核）

---

## 十、未能核实 / 存疑的点

1. **Chen et al. 2023 Table 1 的具体数值**（XSum / HumanEval 各自的精确加速比与接受率）：本轮仅核到摘要级「2–2.5x」与正文「HumanEval almost 2.5x」；表格数字未抓取到。**未核实**。
2. **Leviathan App A.1 的证明行文**：正文引用了该附录结论（「采样所得 $x$ 服从 $p$」），抓取在附录前截断；本简报第五节的证明是按标准恒等式补全的，与 Chen Theorem 1 逐步对应，结论与正文引用一致。
3. **EAGLE 的精确接受长度 $\tau$**（其 Table 1 的 MT-bench 数值）：抓取被截断，仅核到「nearly four tokens per forward pass」与「draft accuracy ≈ 0.8」的文字描述。表格数字**未核实**。
4. **EAGLE §3.2 消除特征不确定性后的精确加速比**（原文「from 1.9x to …」）：原文截断，终值**未核实**。
5. **Gloeckle et al. 2024（MTP 原始论文）的 arXiv 编号 2404.19737**：凭记忆填写，本轮未在一手页面核实。**未核实**。
6. **Self-speculative / LayerSkip 的接受率 0.5–0.65**：来自二手技术博客，一手论文数字**未核实**。
7. **Medusa 分模型、分任务的加速比明细**：仅核到摘要级 Medusa-1 >2.2x、Medusa-2 2.3–3.6x。
8. **DeepSeek-V3 MTP 接受率的两个版本**：DeepSeek-V3 Technical Report §5.4.3 写 85–90%（本简报采用）；后续 *Insights into DeepSeek-V3* 写 80–90%。以技术报告为准，差异原因不明。
9. **Spec-Bench 2024 之后的数据更新**（如 EAGLE-3 在 Spec-Bench 协议下的官方数字、最新排行榜）：未系统核查。
10. **Hu & Huang 2024（Tree Monte Carlo）的 arXiv 编号**：存在性经第三方论文参考文献确认，编号**未核实**。
11. **Leviathan Table 2 中个别行实测加速略高于 $c=0$ 理论值**（如 CNN/DM T5-small T=0：理论 2.64x vs 实测 3.1x）：i.i.d. 假设的近似性与实现细节所致（论文 §A.3），引用时建议同时给出公式值与实测值。
