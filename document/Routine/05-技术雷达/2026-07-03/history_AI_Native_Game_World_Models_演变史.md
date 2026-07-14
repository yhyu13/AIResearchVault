# AI-Native Game / World Models 技术演变史（2018→2026）

> **撰写对象**：AI-Native Game / World Model 技术研究者
> **核心问题**：这条技术线是怎么走到今天的？关键转折点是什么？
> **阅读建议**：本文不罗列现状，而是按时间线追踪技术路线的生灭与分叉，标注每步的数学/架构本质。

---

## 0. 导论：两个平行宇宙的交汇

要理解 AI-Native Game 的演变，必须先看清楚两条独立发展的技术谱系是如何在 2024 年前后发生交汇的：

- **谱系 A — 游戏 AI 与程序化生成（PCG）**：从 1980 年代的 Rogue-like 地牢生成、2000 年代的 L-system 植物建模，到 2010 年代基于搜索的 PCG（如 Feasible Infeasible Two-Population, FI-2Pop），其核心是**用算法替代人工资产生产**，但每一行逻辑仍由人类编写。
- **谱系 B — 深度学习 World Model**：从 2018 年 Ha & Schmidhuber 的奠基性论文开始，核心假设是**神经网络可以直接学习环境的转移动力学**，无需显式物理引擎或手工规则。

这两条谱系在 2024 年的交汇点，标志着"游戏"的定义从"运行在传统引擎上的确定性系统"向"由神经网络实时生成的可交互体验"迁移。本文按时间线展开。

---

## 1. 奠基期（2018—2019）：World Model 概念的诞生

### 1.1 Ha & Schmidhuber (2018)：World Model 的数学框架

2018 年，David Ha 与 Jürgen Schmidhuber 在 NeurIPS 发表《Recurrent World Models Facilitate Policy Evolution》[^1]，首次将 "World Model" 定义为可学习的内部环境模拟器。

**架构分解**（精确到模块）：

```
观测 x_t → [VAE Encoder] → 隐变量 z_t ~ q(z_t | x_t)
                    ↓
              [MDN-RNN] → 预测下一隐态 (z_{t+1}, h_{t+1})
                    ↓
              [VAE Decoder] → 重构观测 x̂_t ~ p(x_t | z_t)
                    ↓
              [Controller] → 输出动作 a_t = W[z_t; h_t]
```

其中 MDN-RNN（Mixture Density Network + RNN）用高斯混合分布建模隐态转移：

$$
p(z_{t+1} | z_t, a_t, h_t) = \sum_{k=1}^{K} \pi_k \cdot \mathcal{N}(z_{t+1}; \mu_k, \sigma_k)
$$

这里的核心洞察是：**将感知（VAE）、动力学（MDN-RNN）与控制（线性控制器）显式分离**，使得策略可以在 learned latent space 中通过进化算法（CMA-ES）高效优化，而不必在原始像素空间试错。

**局限性**：该模型仅在 2D CarRacing 和 3D VizDoom 环境中验证，分辨率低、动作空间离散，且 RNN 的长期记忆能力有限。但它确立了一个范式——**世界可以被压缩进一个可微分的隐态空间**。

### 1.2 AI Dungeon (2019)：LLM 首次成为"游戏引擎"

几乎在同一时间轴的另一端，2019 年 12 月，Nick Walton 发布的 AI Dungeon[^2] 以 GPT-2 为叙事引擎，开创了"生成式文字冒险"这一品类。

虽然 AI Dungeon 没有训练任何世界动力学模型，但它验证了一个关键假设：**足够大的语言模型可以在零样本条件下扮演"游戏主（GM）"角色**，维持世界观一致性和开放式叙事分支。这直接启发了后续将 LLM 与虚拟环境结合的工作（如 2023 年的 Voyager）。

---

## 2. 方法论分化期（2020—2023）：三条技术路线的确立

### 2.1 路线 I：基于隐态动力学的 Model-Based RL（Dreamer 系列）

Ha & Schmidhuber 之后，DeepMind 的 Danijar Hafner 团队在 2019—2023 年间推动了 RSSM（Recurrent State-Space Model）架构的迭代：

- **DreamerV1 (2019)**[^3]：引入确定性路径 + 随机路径的混合隐态表示：
  $$
  h_t = f(h_{t-1}, z_{t-1}, a_{t-1}) \quad 	ext{(deterministic)}
  $$
  $$
  z_t \sim q(z_t | x_t, h_t) \quad 	ext{(stochastic)}
  $$
  这一设计解决了 Ha & Schmidhuber 模型中 encoder 无记忆的问题——编码器现在以 RNN 隐态 $h_t$ 为条件，实现 history-conditioned inference。

- **DreamerV3 (2023)**[^4]：在 Nature 上发表，掌握 150+ 任务，证明 world model 的样本效率可以远超 model-free RL。

**技术本质**：这条路线始终围绕**隐态空间中的预测与控制**，不生成像素，而是生成紧凑的隐态转移。它的优势是数据效率极高；劣势是隐态不可解释，且难以直接用于视觉内容生成。

### 2.2 路线 II：扩散模型与神经游戏引擎（2022—2024）

2022 年，Stable Diffusion 的开源释放了扩散模型（Diffusion Models）的工业化潜力。游戏领域很快意识到：如果扩散模型可以生成图像，那么它也可以生成**下一帧游戏画面**。

这一思路的数学本质是：将世界建模视为条件扩散过程

$$
p(x_{t+1} | x_{t}, x_{t-1}, ..., a_t) = \int p(x_{t+1}^{(k-1)} | x_{t+1}^{(k)}, c) \, dq
$$

其中条件 $c$ 包含历史帧与玩家动作。关键突破在于如何将"动作"注入扩散去噪过程。

### 2.3 路线 III：LLM 驱动的 Agent 与 NPC（2023）

2023 年，大语言模型（GPT-4）的能力跃升催生了第三条路线——**将 LLM 作为游戏中的自主 agent "大脑"**。

**Voyager (2023)**[^5] 是这一方向的里程碑。由 NVIDIA 与多家机构合作，Voyager 是首个基于 GPT-4 的 Minecraft 终身学习 agent：

- **自动课程（Automatic Curriculum）**：GPT-4 根据当前状态生成 progressively harder 的任务目标
- **技能库（Skill Library）**：将成功执行的 Python 代码以 embedding 索引存储，支持未来检索与组合
- **迭代提示（Iterative Prompting）**：结合环境反馈、执行错误与自验证机制精炼代码

```python
# Voyager 的核心循环示意（概念性）
for iteration:
    task = curriculum.get_next_goal(state)      # GPT-4 提出任务
    code = llm.generate_code(task, context)     # 生成动作代码
    obs, success = env.execute(code)            # Minecraft 执行
    if self_verify(obs, task):
        skill_lib.store(code, embedding(code))  # 存入技能库
```

Voyager 解锁了关键科技树里程碑的速度比此前 SOTA 快 **15.3×**[^5]，证明 LLM 可以在开放世界游戏中进行 long-horizon planning 与 skill composition。

同期，**斯坦福 Generative Agents (2023)**[^6] 在小城镇沙盒中模拟了 25 个 AI NPC 的社会行为，进一步证明 LLM 可以驱动多智能体社会模拟。

---

## 3. 爆发期（2024）：World Model 成为游戏引擎

2024 年是技术路线的决定性交汇点。三条路线中的前两条（隐态动力学 + 扩散生成）在这一年融合，产生了多个"纯神经网络游戏引擎"。

### 3.1 Genie (DeepMind, ICML 2024)：Foundation World Model 的诞生

**论文**：Bruce et al., "Genie: Generative Interactive Environments", ICML 2024[^7]

Genie 是一个 **11B 参数**的 foundation world model，其架构可分解为三件套：

1. **Spatiotemporal Video Tokenizer**：将视频帧压缩为离散 token，降低序列建模的计算复杂度
2. **Latent Action Model**：关键创新——**无需动作标签**，从视频帧对 $(x_t, x_{t+1})$ 中推断 latent action $a_t$。这通过自监督学习实现：
   $$
   a_t = 	ext{LatentActionModel}(x_t, x_{t+1})
   $$
3. **Autoregressive Dynamics Model**：基于 MaskGIT 的自回归帧预测，以 tokenized 历史帧 + latent action 为条件：
   $$
   p(x_{t+1} | x_{\leq t}, a_{\leq t})
   $$

**历史意义**：Genie 首次证明，**从 20 万小时无标签互联网游戏视频中，模型可以自监督学习出可交互的 2D 平台游戏世界**，且 latent action space 足够支持从 unseen videos 中推断策略（zero-shot imitation）。

### 3.2 GameNGen (Google Research, 2024)：扩散模型 = 实时 DOOM 引擎

**论文**：Valevski et al., "Diffusion Models Are Real-Time Game Engines", arXiv:2408.14837[^8]

GameNGen 回答了一个更激进的问题：**能否用纯扩散模型替代整个游戏引擎？**

其训练分为两阶段：

- **Phase 1**：RL agent（PPO）学习玩 DOOM，记录 7000 万帧 $(x_t, a_t)$ 数据
- **Phase 2**：以 Stable Diffusion v1.4 为骨干，训练条件扩散模型：
  $$
  p(x_{t+1} | x_t, x_{t-1}, ..., x_{t-N}, a_t)
  $$
  其中条件替换掉了 SD 原本的 text prompt，改为**历史帧序列 + 按键输入**。

**关键工程技巧**：
- **Conditioning Augmentations**：在训练时对条件帧加入噪声与 dropout，防止自回归推理时的误差累积
- **Distillation**：将多步扩散蒸馏为 1-step 生成，使推理速度从 20 FPS 提升至 50 FPS（TPUv5）

**结果**：PSNR 达到 29.4（与有损 JPEG 同级），人类评估者几乎无法区分真实游戏与模拟画面。

### 3.3 DIAMOND (NeurIPS 2024 Spotlight)：在扩散世界中训练 Agent

**论文**：Alonso et al., "Diffusion for World Modeling: Visual Details Matter in Atari", NeurIPS 2024 Spotlight[^9]

DIAMOND 的核心贡献是证明了：**agent 可以完全在 diffusion world model 中训练，无需真实环境交互**。

其 loss 函数是标准的扩散训练目标：

$$
\mathcal{L} = \mathbb{E}_{x_0, \epsilon, t} \left[ \| \epsilon - \epsilon_	heta(x_t, t, c) \|^2 ight]
$$

其中条件 $c$ 包含历史帧与动作。DIAMOND 在 Atari 100k 基准上首次超过人类均值，并在 CS:GO 上构建了可玩的神经模拟环境。

### 3.4 Oasis (Decart + Etched, 2024)：实时 Minecraft 世界

Oasis[^10] 采用 **Spatial Autoencoder + Latent Diffusion Transformer (DiT)** 架构：

- Autoencoder 基于 ViT，将帧压缩到 latent space
- Backbone 基于 DiT（Diffusion Transformer），以用户键盘/鼠标输入为条件
- 使用 **Diffusion Forcing** 训练：对每个 token 独立施加噪声，允许灵活的解码策略

为解决自回归模型的误差累积问题，Oasis 引入了 **Dynamic Noising**——在推理时主动注入噪声再逐步去噪，使模型对不完美输入更具鲁棒性。

### 3.5 技术路线的分叉：Autoregressive vs. Diffusion

到 2024 年底，world model 的游戏引擎路线已明确分为两派：

| 维度 | Autoregressive 派 (Genie, MineWorld) | Diffusion 派 (GameNGen, DIAMOND, Oasis) |
|------|-------------------------------------|----------------------------------------|
| 核心操作 | Next-token prediction | Iterative denoising |
| 训练稳定性 | 高（教师强制） | 中（需处理 exposure bias） |
| 推理速度 | 快（单次前向） | 慢（多步/需蒸馏） |
| 视觉保真度 | 中 | 高 |
| 代表工作 | Genie, iVideoGPT, MineWorld | GameNGen, DIAMOND, Matrix-Game |

---

## 4. 产业化加速期（2025）：从实验室到 Demo 再到基础设施

### 4.1 Genie 3 (DeepMind, 2025)：720p@24fps 的通用世界模型

2025 年 8 月，DeepMind 发布 Genie 3[^11]，实现了：

- **720p 分辨率 @ 24 FPS 实时交互**
- **数分钟级别的世界一致性**（Genie 2 仅维持 10-20 秒）
- **Promptable World Events**：用户可通过文本实时修改世界（如"改变天气""召唤角色"）
- **约 1 分钟的视觉记忆窗口**：物体离开视野后重新出现仍保持一致

**架构演进**：Genie 3 从 2D 平台游戏扩展到 3D 环境，支持第一/第三人称视角、载具驾驶等。虽然具体技术细节未完全公开，但从 DeepMind 的披露可知其核心是**自回归生成 + Veo 3 级别的视频生成骨干**，并引入了显式的记忆机制。

### 4.2 NVIDIA Cosmos (CES 2025)：物理 AI 的 World Foundation Model 平台

NVIDIA 在 CES 2025 发布的 Cosmos[^12] 是一个面向 Physical AI（机器人、自动驾驶）的 world foundation model 平台：

- **训练数据**：9000 万亿 token，包含 2000 万小时的自动驾驶、机器人交互视频
- **模型族**：Diffusion 系（7B/14B）+ Autoregressive 系（4B/12B），分 Nano/Super/Ultra 三档
- **Tokenizer**：Cosmos-1.0-Tokenizer-CV8x8x8（连续 token）与 DV8x16x16（离散 token）
- **开源协议**：NVIDIA Open Model License，允许商业使用

Cosmos 的关键设计是**Text2World / Image2World / Video2World / Action-conditioned World** 的统一接口，使其成为机器人训练的数据生成基础设施。

### 4.3 Matrix-Game 系列 (Skywork AI, 2025-2026)：开源路线的急先锋

Skywork AI 的 Matrix-Game 是 2025-2026 年开源世界模型中最具工程完整性的项目：

- **Matrix-Game 2.0 (2025)**[^13]：基于因果自回归扩散（Causal Autoregressive Diffusion），通过 Distribution Matching Distillation (DMD) 实现 **25 FPS 实时推理**，1.8B 参数，MIT 开源
- **Matrix-Game 3.0 (2026)**[^14]：引入**显式长程记忆机制**：
  - **Camera-aware Memory Retrieval**：根据相机位姿与视场重叠检索历史帧
  - **Plücker 编码**：对当前目标与记忆帧的相对相机几何进行显式编码
  - **Error-aware Training**：在训练时将模型自身生成的不完美帧重新注入，学习自校正
  - 5B 模型达 **40 FPS @ 720p**，28B 模型进一步提升质量与泛化性

### 4.4 MineWorld (Microsoft Research, 2025)：开源 Minecraft World Model

Microsoft Research 发布的 MineWorld[^15] 是一个开源的 Minecraft 交互世界模型，采用 autoregressive 架构，支持 4-7 FPS 推理。虽然速度不及商业系统，但其开源性质使其成为学术界复现与扩展的重要基线。

---

## 5. 产业应用与游戏内 AI（2023—2026）

### 5.1 AI NPC：从对话树到 LLM 驱动

**网易《逆水寒》手游（2023）**[^16]：国内首个在主流游戏中部署游戏版 GPT 的产品，为 400+ NPC 配置智能 AI 系统，NPC 能基于对话历史自主生成行为反馈。

**育碧 NEO NPC（2024 GDC）**[^17]：基于 NVIDIA Audio2Face + Inworld AI LLM 技术，实现 NPC 的实时即兴对话。核心设计原则是"角色由作家塑造，对话由 AI 生成"——确保叙事一致性不丢失。

**技术本质**：这些系统并非 world model，而是**LLM + RAG + 记忆模块**的组合：

```
玩家输入 → [Intent Parser] → 查询向量数据库(角色设定/历史对话)
                ↓
         [LLM + System Prompt(性格/背景)] → 生成回复
                ↓
         [Audio2Face / 动作系统] →  lipsync + 表情
```

### 5.2 生成式资产生产

2025-2026 年，生成式 AI 已渗透到游戏开发的每个环节：
- **美术**：概念图、纹理、角色原画（Stable Diffusion / Midjourney 工作流）
- **3D 资产**：Mesh 生成（如 Meshy, Rodin）、材质合成
- **动画**：Motion matching + 生成式动作补全
- **代码**：GitHub Copilot 辅助游戏脚本编写

根据 Steam 数据，2025 年披露使用生成式 AI 的游戏约占总数的 7%，而 2025 年新发行游戏中这一比例高达 20%[^18]。

---

## 6. 当前瓶颈与技术矛盾

### 6.1 时序一致性与误差累积

所有自回归 world model 面临一个根本性的数学矛盾：

$$
\hat{x}_{t+1} = f_	heta(\hat{x}_t, \hat{x}_{t-1}, ..., a_t)
$$

其中 $\hat{x}_t$ 是模型自身的生成输出，而非真实观测。这意味着**每一步推理都在 compound 分布漂移**。

Matrix-Game 3.0 的解决方案是 error-aware training（将自生成帧注入训练分布），Self-Forcing[^19] 的解决方案是在训练时进行 autoregressive rollout。但根本问题——**确定性动力系统与随机生成模型的不匹配**——尚未完全解决。

### 6.2 长程记忆的有限性

Genie 3 的记忆窗口约为 1 分钟[^11]，Matrix-Game 3.0 通过显式记忆检索扩展到分钟级[^14]，但对于 RPG 动辄数十小时的游戏流程而言，这仍是数量级差距。

### 6.3 物理正确性与可交互性的权衡

Diffusion world model 擅长生成视觉上合理的帧，但**无法保证物理一致性**：
- 物体离开视野后可能消失或变形
- 复杂因果关系（如"点燃炸药→炸开墙壁→露出通道"）难以稳定复现
- 数值状态（HP、弹药、分数）没有显式表示，全靠像素层面的隐式学习

### 6.4 推理成本与实时性的矛盾

| 系统 | 分辨率/FPS | 推理硬件 | 估计每帧成本 |
|------|-----------|---------|------------|
| GameNGen | 320×240 / 20 FPS | TPUv5 | ~$0.001 |
| Oasis | 360p / 20 FPS | Sohu ASIC | ~$0.002 |
| Genie 3 | 720p / 24 FPS | TPU cluster | 未公开（高） |
| Matrix-Game 3.0 | 720p / 40 FPS | H100 | ~$0.005 |

对于消费者级实时游戏而言，这一成本结构仍不经济。本地推理（如 NVIDIA RTX 50 系列的 AI 加速器）可能是突破口。

---

## 7. 可预见的下一步（2026 及以后）

### 7.1 混合架构：神经渲染 + 传统引擎

纯粹的"模型即引擎"路线短期内难以支撑 AAA 级游戏。更现实的演进是**混合架构**：
- **传统引擎**负责物理、碰撞、数值系统、确定性逻辑
- **World Model**负责视觉生成、NPC 行为、叙事动态展开
- 两者通过共享的隐态空间（latent space）或结构化接口通信

### 7.2 3D 高斯溅射与 World Model 的融合

3D Gaussian Splatting (3DGS)[^20] 提供了显式的场景表示方式，其参数化形式（各向异性高斯）比神经辐射场（NeRF）更适合实时渲染。将 3DGS 作为 world model 的场景记忆载体，可能解决长程一致性问题：

$$
	ext{Scene Memory} = \{ (\mu_i, \Sigma_i, c_i, lpha_i) \}_{i=1}^{N}
$$

其中 $(\mu, \Sigma)$ 为高斯中心与协方差，$(c, lpha)$ 为颜色与不透明度。

### 7.3 Agent-Native 游戏设计

2026 年的前沿方向不再是"用 AI 制作传统游戏"，而是**为 AI Agent 设计原生游戏**。这类游戏的核心玩法围绕：
- 多智能体社会模拟（如斯坦福 Generative Agents 的扩展）
- 玩家与 AI 的开放式协商、欺骗、合作
- 动态经济系统与涌现叙事

---

## 8. 对 AI-Native Game 开发者的建议

### 8.1 你的现有技能如何迁移

| 你的专长 | 与 World Model 的交集 | 建议行动 |
|---------|---------------------|---------|
| **神经渲染 / 场景表示** | World model 需要物理正确的视觉作为训练先验；神经场景表示可与生成模型结合 | 关注 "Neural Radiance Transfer" 与 "Differentiable Rendering" 方向 |
| **实时渲染管线** | World model 的推理管线本身就是新型渲染管线 | 学习 CUDA / Triton 优化，理解 Transformer 推理的 memory-bound 特性 |
| **Shader / 材质** | Diffusion model 的 texture 生成正在替代手工材质 | 掌握 ControlNet / IP-Adapter 等条件控制技术 |
| **引擎架构** | 混合引擎（传统 + 神经）需要新的中间件抽象 | 研究 Omniverse / Cosmos 的 USD-based 工作流 |

### 8.2 具体技术切入点

1. **Differentiable Simulation**：将传统物理引擎（如 PhysX, Havok）与可微分层结合，为 world model 提供物理先验。相关论文：DiffTaichi (Hu et al., 2019), NVIDIA Warp (2022)。

2. **Neural Texture / Material Compression**：用隐式神经表示压缩游戏资产，减少 world model 的内存占用。参考：InstantNGP (Müller et al., SIGGRAPH 2022), 3D Gaussian Splatting (Kerbl et al., SIGGRAPH 2023)。

3. **Temporal Consistency in Video Generation**：这是 graphics 社区的核心能力。将传统 TAA（Temporal Anti-Aliasing）/ Motion Vector 的概念引入 diffusion world model 的采样过程，可能显著改善长程一致性。

### 8.3 警惕的陷阱

- **不要低估传统引擎的价值**：确定性、可调试性、精确物理是 world model 短期内无法替代的。Neural engine 不是银弹。
- **关注评估指标**：World model 目前缺乏像 PSNR/SSIM 之于渲染那样统一的评估标准。建议关注 2025 年涌现的 world model benchmark（如 GameFactory 的 GF-Minecraft 数据集）。
- **推理成本是硬约束**：再漂亮的模型，如果无法在消费级 GPU 上跑到 60 FPS，就很难成为游戏引擎。

---

## 参考文献

[^1]: Ha, D., & Schmidhuber, J. (2018). Recurrent World Models Facilitate Policy Evolution. *NeurIPS 31*, 2451–2463. https://papers.nips.cc/paper/7512-recurrent-world-models-facilitate-policy-evolution

[^2]: Walton, N. (2019). AI Dungeon. Latitude. https://aidungeon.io

[^3]: Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., & Davidson, J. (2019). Learning Latent Dynamics for Planning from Pixels. *ICML 2019*, 2555–2565.

[^4]: Hafner, D., Pasukonis, J., Ba, J., & Lillicrap, T. (2023). Mastering Diverse Domains through World Models. *Nature*, 640(8059), 647–653.

[^5]: Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., & Anandkumar, A. (2023). Voyager: An Open-Ended Embodied Agent with Large Language Models. *NeurIPS 2023*. https://voyager.minedojo.io

[^6]: Park, J. S., O'Brien, J., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023*.

[^7]: Bruce, J., et al. (2024). Genie: Generative Interactive Environments. *ICML 2024*. https://arxiv.org/abs/2402.15391

[^8]: Valevski, D., Leviathan, Y., Arar, M., & Fruchter, S. (2024). Diffusion Models Are Real-Time Game Engines. *arXiv:2408.14837*. https://gamengen.github.io

[^9]: Alonso, E., et al. (2024). Diffusion for World Modeling: Visual Details Matter in Atari. *NeurIPS 2024 (Spotlight)*. https://arxiv.org/abs/2405.12399

[^10]: Decart AI & Etched AI. (2024). Oasis: A Universe in a Transformer. Technical Report. https://oasis-model.github.io

[^11]: Ball, P. J., et al. (2025). Genie 3: A New Frontier for World Models. Google DeepMind Blog, August 2025. https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/

[^12]: Agarwal, N., et al. (2025). Cosmos World Foundation Model Platform for Physical AI. *arXiv:2501.03575*. https://github.com/nvidia-cosmos

[^13]: Skywork AI. (2025). Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model. Technical Report. https://matrix-game-v2.github.io

[^14]: Wang, Z., et al. (2026). Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory. *arXiv:2604.08995*. https://matrix-game-v3.github.io

[^15]: Guo, J., et al. (2025). MineWorld: A Real-Time and Open-Source Interactive World Model on Minecraft. *arXiv:2504.08388*.

[^16]: 网易. (2023). 逆水寒手游智能 NPC 系统. https://h.163.com/news/official/

[^17]: Ubisoft. (2024). NEO NPC Prototype. GDC 2024 Presentation.

[^18]: Lambe, I. (2025). Steam AI Disclosure Survey. Industry Report.

[^19]: Huang, R., et al. (2025). Self-Forcing: Training with Autoregressive Rollout for World Models. *NeurIPS 2025*.

[^20]: Kerbl, B., Kopanas, G., Leimkühler, T., & Drettakis, G. (2023). 3D Gaussian Splatting for Real-Time Radiance Field Rendering. *SIGGRAPH 2023*, 1–16.

---

> **文档信息**
> - 撰写日期：2026-07-03
> - 目标读者：AI-Native Game / World Model 技术研究者 / 游戏引擎开发者
> - 更新策略：每季度根据 arXiv/NeurIPS/ICML/SIGGRAPH 新论文更新里程碑
