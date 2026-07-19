---
tags: [paper, world-model, interactive-video, ai-native-game, neural-game-engine, playable-world-model]
aliases: [World-Models-Latest-2025-2026]
created: 2026-07-20
---

# 方向五：世界模型与 AI 原生游戏（2025–2026 最新论文）

> **核心问题**：如何让生成式模型从"生成视频"进化为"生成可玩世界"？实时性、长时一致性、动作可控性三大瓶颈各自的最优技术路线是什么？
> **技术栈**：Playable World Model + Interactive Generative Video + Causal Diffusion + Self-Forcing Distillation + Explicit 3D Memory + Neural Game Engine
> **关联**：[[01a-LLM-Agent-in-Games]], [[01d-sandbox-latest]], [[01-Game-AI-研究库总览]]

---

## 核心问题定义

```
问题形式化：给定动作序列 a_1..a_t 和初始条件 x_0，学习世界模型 p_θ(x_t+1 | x_≤t, a_≤t)，要求：
1. 实时性：生成延迟 ≤ 1/FPS 帧预算（ playable 门槛 ~10 FPS，流畅门槛 ~24 FPS）
2. 长时一致性：场景重访（revisit）时 x 的结构不漂移，时间跨度 ≥ 分钟级
3. 动作可控性：生成帧对动作的跟随精度（action-following accuracy）足够支撑 gameplay
4. 泛化性：跨场景/跨风格/跨游戏不显著退化

世界模型的三重矛盾：
- 质量 vs 速度：多步扩散质量高但慢；少步蒸馏/并行解码快但有误差累积
- 隐式 vs 显式记忆：纯自回归上下文容量有限；显式 3D 记忆有构建成本且难处理动态场景
- 通用 vs 可复现：闭源大模型（Genie 3）赢在通用性；开源路线赢在可复现与可控注入
```

**世界模型在游戏生态中的位置**：
- **替代 simulator**：世界模型即环境，为 agent 训练提供无限可交互环境（Genie 3 + SIMA 范式）
- **神经游戏引擎**：GameNGen → Genie 3 → Matrix-Game 2.0 谱系，逐步替代传统渲染管线
- **内容生产**：程序化生成为玩法服务（PGC-for-gameplay），按需生成关卡与场景
- **评估新层**：WBench / WorldMark 等交互世界模型专用 benchmark 出现

---

## 关键论文

### 1. Genie 3: A New Frontier for World Models

- **作者**：Google DeepMind Genie 团队
- **来源**：官方技术博客（无 arXiv 论文），2025-08-05
- **链接**：https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/
- **项目**：无公开代码/权重，仅 limited research preview

#### AI 预读（150 字）

> Genie 3 是 DeepMind 第三代通用世界模型，可从文本 prompt 生成可实时交互的 3D 世界：720p @ 24 FPS 流式输出，环境一致性维持数分钟（远长于 Genie 2 的 10–20 秒），并支持 promptable world events——生成过程中用文本触发环境事件。模型无显式 3D 表征（non-NeRF/non-Gaussian），纯靠自回归上下文涌现出物体恒存性、直觉物理与场景记忆。官方将其定位为通往 AGI 的基础设施：为 agent（如 SIMA）提供无限可交互训练环境。第三方基准 WorldMark 评测中其世界一致性为受测最强。

#### 3 个引导问题

1. **无显式 3D 表征的分钟级一致性机制**：Genie 3 没有 NeRF/Gaussian 之类的显式场景表征，也没有外部 memory 模块，仅靠自回归上下文维持数分钟的世界状态。这种纯隐式记忆的有效容量上限在哪里？它与 WorldPlay 的显式 3D 几何记忆路线，哪条更可能 scale 到开放世界？

2. **promptable world events 的架构实现**：生成中在线文本干预（如"开始下雪"）可能如何实现——cross-attention 注入、token 拼接、还是 control signal 分支？每种实现对生成连续性的扰动程度如何？

3. **闭源世界模型的公平评测**：Genie 3 完全闭源，学界只能通过 WorldMark 类第三方基准评测。这类基准的协议设计要点是什么——如何防止模型对基准过拟合、如何定义可复现的"世界一致性"指标？

#### 重点章节标记

1. **博客 Demo 部分**：自然景观、物理现象、城市导航、历史场景的多样性展示（通用性证据）
2. **Agent 段落**：SIMA 在 Genie 3 生成的世界中执行长程任务（世界模型即环境的实证）
3. **规格声明**：720p / 24 FPS / 分钟级一致性——与 Genie 2 的 10–20 秒对比
4. **局限性声明**：动作空间仅导航类；一致性数分钟后退化；promptable events 可控性有限
5. **WorldMark 第三方评测**：闭源模型一致性排名的唯一公开参照

#### 面试谈资

- **30 秒**：Genie 3 把世界模型从生成短片推进到实时可玩世界：720p/24fps、分钟级一致性、生成中可文本触发事件，是神经游戏引擎的里程碑，但完全闭源。
- **2 分钟**：三代 Genie 的演进线索清晰：Genie 1 从视频学潜动作（latent action），Genie 2 单图生成 10–20 秒可玩世界，Genie 3 做到 720p/24fps 分钟级流式交互。核心技术问题是无显式 3D 表征下如何维持空间一致性——模型在自回归上下文中"记住"了世界，涌现出物体恒存性和场景记忆。与开源阵营（Matrix-Game 2.0、MineWorld）对比：闭源赢在通用性与一致性，开源赢在可复现与可控注入。对 agent 训练的意义是范式级的：世界模型即环境，可以替代手工 simulator，SIMA 在其中执行长程任务就是实证。但局限也明显：动作仅导航类、闭源无法复现、小时级连贯世界仍是开放问题。

---

### 2. MineWorld: a Real-Time and Open-Source Interactive World Model on Minecraft

- **作者**：Junliang Guo 等（Microsoft Research Asia）
- **来源**：arXiv:2504.08388, 2025-04-11
- **链接**：https://arxiv.org/abs/2504.08388
- **代码**：https://github.com/microsoft/mineworld

#### AI 预读（150 字）

> MineWorld 是 Minecraft 上的实时开源交互世界模型。采用 visual-action autoregressive Transformer：游戏画面经 VQ tokenizer 离散化，键鼠动作编码为 action tokens，交错排列后以因果 Transformer 做 next-token prediction，将动作控制与画面生成统一在 NTP 框架内。提出 parallel decoding 方法，利用帧内 token 间的条件独立假设同时预测多个 token，实现 4–7 FPS 生成（对比扩散基线 <1 FPS），并设计针对世界模型的新评测协议，在视觉保真度与动作跟随精度上显著超过 Oasis 等开源扩散模型。

#### 3 个引导问题

1. **并行解码的误差累积**：parallel decoding 打破自回归的严格串行依赖后，帧内同时预测的 token 之间存在条件独立假设的近似误差。这种误差如何在帧内累积？在长 rollout 中会不会与跨帧误差叠加，导致一致性加速退化？

2. **自回归 vs 因果扩散的最优点**：自回归离散 token 路线（MineWorld）与因果化扩散路线（Matrix-Game 2.0）在延迟-质量曲线上各自的最优点在哪？token 化损失（VQ 重建误差）是否构成自回归路线的质量天花板？

3. **动作跟随精度的量化**：世界模型的 action-following 指标应如何设计——能否借鉴 RL 中的 inverse dynamics 一致性（从相邻帧反推动作与输入动作比对）？这与 FVD 类视觉质量指标的相关性有多强？

#### 重点章节标记

1. **Method**：visual-action token 交错排列 + NTP 的架构细节
2. **Parallel Decoding**：帧内 token 条件独立假设与加速比分析
3. **Evaluation Protocol**：动作跟随精度与视觉质量的新指标定义
4. **对比实验**：vs Oasis 等开源扩散模型——4–7 FPS vs <1 FPS
5. **开源资产**：模型权重与代码（研究复现起点）

#### 面试谈资

- **30 秒**：微软的 MineWorld 用纯自回归 Transformer + 并行解码在 Minecraft 上做到 4–7 FPS 实时交互，证明非扩散路线也能做可玩世界模型，且完全开源。
- **2 分钟**：MineWorld 的意义在于给出世界模型的第三条路线：不是扩散因果化，也不是闭源大模型，而是经典的"一切皆可 token"——画面 VQ 离散化、动作编码为 action tokens，交错后做 next-token prediction，动作控制与画面生成统一在一个 NTP 框架里。关键工程创新是 parallel decoding：帧内 token 近似条件独立，可以同时预测，把自回归推到 4–7 FPS，而同期扩散方案（Oasis）不到 1 FPS。代价是 VQ token 化的质量天花板和并行假设的误差。它还贡献了动作跟随精度的评测协议——世界模型好不好，不只看 FVD，还要看"按了前进键画面真的往前走"。作为完全开源的 Minecraft 世界模型，它是 agent 训练中"可微环境替身"的最佳起点之一。

---

### 3. Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model

- **作者**：Xianglong He, Chunli Peng, Zexiang Liu, Boyang Wang, Yifan Zhang 等（Skywork AI，昆仑万维/天工）
- **来源**：arXiv:2508.13009, 2025-08-18
- **链接**：https://arxiv.org/abs/2508.13009
- **代码**：GitHub 开源权重（SkyworkAI/Matrix-Game）

#### AI 预读（150 字）

> Matrix-Game 2.0 是开源的实时流式交互世界模型，在 1280x720 分辨率下实现 25 FPS 流式生成、时长数分钟，追平 Genie 3 的实时性规格且 open weights。三大组件：基于 Unreal Engine 与 GTA5 的可扩展数据管线（约 1200 小时带动作标注视频）；帧级键鼠输入的 action injection 模块；基于因果架构的 Self-Forcing 少步蒸馏——双向扩散教师蒸馏为因果少步学生，学生在自己生成的 rollout 上计算分布匹配损失，避免 exposure bias，把采样压到 1–4 步。

#### 3 个引导问题

1. **Self-Forcing 的理论位置**：Self-Forcing 与 Diffusion Forcing、一致性蒸馏（consistency distillation）的理论关系是什么？学生在自己 rollout 上算分布匹配损失，近似的是哪种散度？为什么这能解决 exposure bias？

2. **KV cache 长度与漂移的权衡**：因果化改造后流式推理依赖 KV cache。cache 越长记忆越好但注意力成本越高、且早期帧的表征可能过时（漂移源）。这条权衡曲线长什么样？是否存在最优 cache 长度？

3. **数据管线的可控性上限**：1200 小时 UE + GTA5 带动作标注数据中，动作标注（键鼠信号与画面的对齐）质量如何影响最终可控性上限？UE 合成数据与 GTA5 录制数据的领域差异如何处理？

#### 重点章节标记

1. **Data Pipeline**：UE + GTA5 约 1200 小时带标注数据的构建流程
2. **Action Injection**：帧级键鼠条件的注入位置与方式
3. **Self-Forcing Distillation**：双向教师 → 因果少步学生的训练框架（核心章节）
4. **Streaming Inference**：chunk-wise 因果注意力 + KV cache 的流式管线
5. **对比实验**：vs Oasis / MineWorld——25 FPS 720p 与质量双优

#### 面试谈资

- **30 秒**：Skywork 的 Matrix-Game 2.0 是第一个追平 Genie 3 实时性（720p/25fps 流式）的开源世界模型，核心是 Self-Forcing 少步蒸馏 + UE/GTA5 千小时数据管线。
- **2 分钟**：双向视频扩散质量高但不能实时——每帧要等未来帧、采样要几十步。Matrix-Game 2.0 的三板斧是：因果化改造（chunk-wise 因果注意力 + KV cache，帧只依赖历史）、Self-Forcing 蒸馏（双向教师蒸馏成 1–4 步的因果学生，关键让学生在自己生成的 rollout 上算分布匹配损失，从而避免训练-推理分布失配即 exposure bias）、以及 1200 小时 UE/GTA5 带动作标注数据管线。结果是 720p/25fps 分钟级流式生成，实时性与质量同时超过 Oasis 和 MineWorld，且权重开源——任何人都能 fine-tune 自己的可玩世界。剩余瓶颈：长时空间一致性（场景重访仍漂移）、物理因果链模拟有限、极端动作下蒸馏鲁棒性待验证。2025 下半年开源主流路线（因果扩散 + 蒸馏）正是由它确立的。

---

### 4. Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation with Hybrid History Condition

- **作者**：Jiaqi Li, Junshu Tang, Zhiyong Xu, Longhuang Wu, Yuan Zhou, Shuai Shao, Tianbao Yu, Zhiguo Cao, Qinglin Lu（Tencent Hunyuan）
- **来源**：arXiv:2506.17201, 2025-06
- **链接**：https://arxiv.org/abs/2506.17201
- **代码**：https://github.com/Tencent-Hunyuan/Hunyuan-GameCraft-1.0

#### AI 预读（150 字）

> Hunyuan-GameCraft 是腾讯混元的高动态交互式游戏视频生成模型，基于预训练 HunyuanVideo（MMDiT）微调，13B 级开源。核心创新是 hybrid history condition：历史上下文分两级——近期帧高分辨率 token + 远期帧压缩 token，拼接进条件序列，使注意力成本随历史长度亚线性增长，在长序列一致性与计算开销间取得平衡。配合统一的键盘+鼠标动作编码器（cross-attention 注入），支持高动态场景与 3A 风格画面的精细相机控制，支持分钟级连续生成。续作 GameCraft-2（arXiv:2511.23429）扩展 instruction-following。

#### 3 个引导问题

1. **混合历史条件 vs 显式 3D 记忆**：hybrid history condition 本质是对历史帧的有损压缩（近高远低）。与 WorldPlay 的显式 3D 几何记忆相比，两者在"保留对一致性真正重要的信息"上的理论下界差多少？压缩 token 会不会恰好丢掉场景重访需要的低频结构信息？

2. **高动态崩坏的根因**：快速运动时交互视频生成容易崩坏——根因是训练数据中运动模糊样本的偏差，还是历史条件在注意力中被稀释？hybrid history condition 缓解的是哪一层？

3. **13B 基座蒸馏到实时的代价**：GameCraft 仍是多步扩散、非严格实时。若用 Self-Forcing 类蒸馏把它推到 25 FPS，需要牺牲哪些能力——动态范围的鲁棒性、风格的多样性、还是动作跟随精度？

#### 重点章节标记

1. **Hybrid History Condition**：两级历史表征的设计与成本分析（核心章节）
2. **Action Encoder**：键盘+鼠标统一编码与 cross-attention 注入
3. **实验**：vs GameFactory / Matrix-Game 1.0 的长序列与动态场景指标
4. **FVD + 动作一致性 + 人工评测**的三轨评估设计
5. **GameCraft-2 续作**：instruction-following 方向（arXiv:2511.23429，2025-11）

#### 面试谈资

- **30 秒**：腾讯混元 GameCraft 用混合历史条件解决交互视频生成的长时一致性：近帧高清、远帧压缩拼条件，13B 开源模型支持键鼠控制的高动态游戏画面。
- **2 分钟**：交互视频生成的核心矛盾是"记忆多贵"——把所有历史帧高清拼进条件，注意力成本爆炸；全压缩又记不住。GameCraft 的 hybrid history condition 是个务实的工程答案：近期帧保留高分辨率 token（决定即时画质与动作响应），远期帧压缩成低成本 token（维持场景级一致性），注意力成本随历史亚线性增长。与 Matrix-Game 2.0 的因果化 + 蒸馏路线对比：GameCraft 选择保留多步扩散的质量、用条件设计换记忆，Matrix-Game 选择用蒸馏换实时。它基于开源 HunyuanVideo 微调，13B 模型完整开源，支持键鼠精细相机控制和高动态场景，分钟级连续生成。续作 GameCraft-2 转向 instruction-following——从"按键控制"走向"自然语言指挥世界"，和 Genie 3 的 promptable events 方向汇合。

---

### 5. Vid2World: Crafting Video Diffusion Models into Interactive World Models

- **作者**：清华大学（软件学院 Mingsheng Long 组）与重庆大学等（作者名单以 arXiv 页面为准）
- **来源**：arXiv:2505.14357, 2025-05；ICLR 2026 接收
- **链接**：https://arxiv.org/abs/2505.14357
- **项目**：ICLR 2026 接收版 PDF：https://ise.thss.tsinghua.edu.cn/~mlong/doc/Vid2World-ICLR26.pdf

#### AI 预读（150 字）

> Vid2World 提出将预训练视频扩散模型系统改造为交互式世界模型的通用框架，免从头训练。两大技术：diffusion causalization——把双向时间注意力改为因果掩码并重设计逐帧去噪调度，使帧 t 只依赖 ≤t 的历史；causal action guidance——在反向采样每步以动作条件修正 score 方向（classifier guidance 的因果版本），增强动作可控性。关键直觉是预训练视频扩散已具备强世界先验，缺的只是因果性与动作条件。在机器人操控、3D 游戏仿真、开放世界导航三个域验证，视频预测质量与下游决策性能均优于从头训练基线。

#### 3 个引导问题

1. **因果化后的去噪时间表设计**：双向扩散所有帧共享同一去噪进度；因果化后帧 t 去噪时历史帧已确定，每帧的 noise schedule 有哪些合理选择（同步推进 / 逐帧完成 / 滑窗）？各自对误差累积与采样效率的影响？

2. **采样期引导 vs 训练期注入**：causal action guidance 在采样阶段注入动作，Matrix-Game 在训练阶段做 action injection。前者的优势是免训练、可插拔，代价是引导强度需调参且过强损画质。两种路线各自适用什么场景？

3. **世界模型的 value-aware 评测**：Vid2World 用"生成 rollout 对下游 planning / policy 的收益"评估世界模型。如何系统度量世界模型对决策的价值——视觉质量高但动态不准的模型会不会反而误导 policy？

#### 重点章节标记

1. **Diffusion Causalization**：注意力掩码改造 + 逐帧去噪调度重设计（核心章节）
2. **Causal Action Guidance**：采样期动作引导的数学形式与实现
3. **三域实验**：robotics / game / navigation 的跨域验证
4. **下游决策评估**：生成 rollout 用于 planning / policy 的收益
5. **与从头训练基线的对比**：预训练先验的迁移价值

#### 面试谈资

- **30 秒**：Vid2World 给出一个配方：把预训练视频扩散改造成因果交互世界模型，靠注意力因果化和采样期动作引导，三个域验证还能提升下游决策。
- **2 分钟**：Vid2World 回答了一个资源问题：没有 DeepMind 的算力，能不能有世界模型？答案是把预训练视频扩散"改装"——它已经见过海量视频、具备强世界先验，缺的只有两样：因果性（双向注意力会偷看未来帧）和动作条件。causalization 把时间注意力改成因果掩码并重设计逐帧去噪调度；causal action guidance 在反向采样每步用动作条件修正 score 方向，相当于 classifier guidance 的因果版本。整个改造免从头训练，在机器人、游戏、导航三个域都超过从头训练基线，还验证了生成 rollout 对下游 planning 的收益。把它放进路线地图：从头训练（MineWorld）、蒸馏加速（Matrix-Game 2.0）、预训练改装（Vid2World）——三条路线分别对应"从零定制"、"质量换速度"、"先验迁移"三种资源约束。局限：仍多步采样非实时，引导强度需调参，能力上限取决于基座。

---

### 6. A Survey of Interactive Generative Video（IGV 综述）

- **作者**：多机构综述团队（名单以 arXiv 页面为准）
- **来源**：arXiv:2504.21853, 2025-04
- **链接**：https://arxiv.org/abs/2504.21853

#### AI 预读（150 字）

> 首篇系统性梳理 interactive generative video（IGV）的综述，统一了可交互视频生成与世界模型的概念框架。从动作条件类型（键盘/文本/轨迹/多模态）、架构路线（自回归 vs 扩散 vs 混合）、记忆机制、实时性工程、评测协议到应用场景（游戏、机器人、自动驾驶、影视）全链条覆盖，包含 Genie 系列、GameNGen、Oasis、Sora 衍生等主要系统的能力对比表，并指出长时一致性、实时性与物理正确性是三大核心瓶颈，评测协议缺失统一标准。

#### 3 个引导问题

1. **taxonomy 的时效性**：该综述发表于 2025-04，早于 Genie 3、Matrix-Game 2.0、WorldPlay 这波爆发。它的"条件 x 架构 x 记忆 x 应用"分类框架在 2025 下半年新工作冲击下，哪些类目需要修订或增补（如 promptable events、显式 3D 记忆、Self-Forcing 蒸馏）？

2. **评测缺失的弥补进度**：综述指出 IGV 缺乏统一评测协议。在 WBench（多轮交互视频世界模型基准）、WorldMark 出现后，这个问题解决了多少？还有哪些维度（如物理正确性、下游决策价值）仍无标准？

3. **自回归 vs 扩散之争的 2026 证据**：综述对比了两条架构路线的 trade-off。加入 2025 下半年的证据（MineWorld 的 4–7 FPS、Matrix-Game 2.0 的 25 FPS）后，天平偏向哪边？是否其实是"扩散因果化 + 蒸馏"统一了实时性，自回归只剩 token 化的简洁性？

#### 重点章节标记

1. **Taxonomy 章节**：条件模态 x 架构 x 记忆 x 应用的分类框架（建领域地图用）
2. **架构对比**：自回归 vs 扩散 vs 混合的延迟-质量-可控性 trade-off
3. **评测协议梳理**：FVD / 动作一致性 / 人评 / 下游任务的现状与缺口
4. **开放问题清单**：长时记忆、物理 grounding、泛化、实时-质量前沿
5. **系统对比表**：Genie 系列、GameNGen、Oasis、Sora 衍生的能力矩阵

#### 面试谈资

- **30 秒**：这是 IGV 方向第一篇系统综述，给出条件 x 架构 x 记忆的分类框架，适合建立领域地图，但要注意它早于 Genie 3 那波爆发。
- **2 分钟**：建领域地图时这篇综述是最好的起点：它把 interactive generative video 统一成"动作条件的视频生成"，按条件模态（键盘/文本/轨迹/多模态）、架构（自回归/扩散/混合）、记忆机制、应用四个轴分类，覆盖了 2023–2025 的 Genie 系列、GameNGen、Oasis 等主要系统，并明确点出三大瓶颈：长时一致性、实时性、物理正确性。用它的框架给 2025 下半年新工作归位很有意思：Genie 3 属于闭源通用实时 + 隐式记忆；Matrix-Game 2.0 是开源因果扩散 + 蒸馏；WorldPlay 开创了显式 3D 记忆这个新类目——恰好补上综述里"记忆机制"轴的空白。阅读时要带着时间意识：它指出的评测缺失正被 WBench/WorldMark 部分弥补，它没覆盖的蒸馏路线已成为开源主流。能说清一篇综述"哪里过时了"，本身就是对领域演进速度最好的判断力展示。

---

### 7. WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling

- **作者**：Wenxiu Sun, Hao Zhang, Han Wang, Jialong Wu, Zihan Wang, Ziyu Wang, Yuwei Wang 等（单位以论文页为准）
- **来源**：arXiv:2512.14614, 2025-12
- **链接**：https://arxiv.org/abs/2512.14614

#### AI 预读（150 字）

> WorldPlay 针对实时交互世界模型的长时几何一致性瓶颈——玩家离开后返回同一地点时场景结构漂移。方案是将显式 3D 几何记忆引入流式视频世界模型：生成过程中把已观测区域沉淀为持久化的 3D 场景表征（点云/体素/Gaussian 类结构），后续帧生成时按相机位姿检索相关几何记忆作为条件，等效于给自回归模型外挂可寻址的长期世界状态。场景重访一致性指标大幅优于纯上下文/隐式记忆基线，同时维持实时帧率，代表"隐式上下文记忆 → 显式 3D 记忆"的范式转向。

#### 3 个引导问题

1. **显式 vs 隐式记忆的 scale 之争**：WorldPlay 的显式 3D 记忆与 Genie 3 式纯隐式上下文记忆，哪种更可能 scale 到开放世界？显式路线的记忆构建/更新成本随探索范围线性增长，隐式路线的上下文容量有硬上限——两者的失效模式分别在什么规模触发？

2. **动态场景下的几何记忆失效**：显式几何记忆假设场景静态。动态物体（移动的车辆）、可破坏环境（炸掉一面墙）与持久化几何记忆冲突时的失效模式有哪些？如何检测"记忆已过时"并触发修复？

3. **与 SLAM/NeRF 的边界**：WorldPlay 的几何记忆构建与传统 SLAM/NeRF 场景重建的技术边界在哪里？它是否可以理解为"可生成的 SLAM"——地图由重建与生成共同维护？这对游戏引擎的混合架构（显式几何 + 生成式外观）有什么启示？

#### 重点章节标记

1. **Geometric Memory**：持久化 3D 场景表征的构建与更新机制（核心章节）
2. **融合架构**：几何记忆按相机位姿检索并注入流式生成的设计
3. **Revisit Consistency 评测**：场景重访一致性指标的定义与对比实验
4. **实时性分析**：外挂记忆对帧率的影响
5. **相关工作谱系**：Context-as-Memory、Long-term Spatial Memory（2506.05284）等同期潮流

#### 面试谈资

- **30 秒**：WorldPlay 给实时世界模型挂上显式 3D 几何记忆，玩家绕一圈回来场景不漂移——解决纯自回归上下文记不住的硬伤，代表显式记忆范式。
- **2 分钟**：长时一致性是世界模型从"炫技 demo"到"可玩游戏"的最后一公里：玩家绕房子走一圈回来，房子不能变样。Genie 3 靠隐式上下文记忆只能撑几分钟，WorldPlay 的答案是外挂显式 3D 几何记忆——生成过程中把看过的区域沉淀为持久化 3D 表征（点云/Gaussian 类结构），生成新帧时按相机位姿检索相关记忆作为条件。等效于给自回归模型一个可寻址的长期世界状态，场景重访一致性大幅优于纯上下文基线，且实时帧率不受损。它与 Context-as-Memory、Long-term Spatial Memory 等工作同期出现，标志着范式从"隐式上下文"转向"结构化外部记忆"。对游戏 AI 的意义：持久世界状态是可玩性的前提，显式记忆让世界模型第一次接近"游戏存档"的语义。开放问题是动态场景——可破坏环境与静态几何记忆天然冲突，以及记忆规模随探索范围的扩展性。这条路线的终点可能是"可生成的 SLAM"：地图由重建与生成共同维护。

---

## 技术栈对比

| 维度 | Genie 3 | MineWorld | Matrix-Game 2.0 | Hunyuan-GameCraft | Vid2World | WorldPlay |
|------|---------|-----------|-----------------|-------------------|-----------|-----------|
| **架构路线** | 闭源自回归 | 自回归 token | 因果扩散 + 蒸馏 | 扩散 + 混合条件 | 扩散因果化改造 | 流式生成 + 显式 3D 记忆 |
| **实时性** | 24 FPS | 4–7 FPS | 25 FPS | 非严格实时 | 非实时 | 实时（数字见论文） |
| **分辨率** | 720p | 有限 | 720p | 高（13B 基座） | 依基座 | 见论文 |
| **一致性** | 分钟级 | 未系统解决 | 分钟级（重访仍漂移） | 分钟级 | 未专门解决 | 长时重访一致（核心卖点） |
| **动作空间** | 仅导航 | 键鼠 | 键鼠 | 键鼠 | 域相关动作 | 导航类 |
| **记忆机制** | 隐式上下文 | 隐式上下文 | KV cache | hybrid history（近高远低） | KV cache | 显式 3D 几何记忆 |
| **训练方式** | 未公开 | 从头 NTP | Self-Forcing 蒸馏 | HunyuanVideo 微调 | 预训练改装 | 流式训练 + 记忆 |
| **开源** | ✗（limited preview） | ✓ 完全 | ✓ 权重 | ✓ 13B | 待确认 | 待确认 |

---

## 方向横向观察

1. **三条技术路线的收敛**：(a) 自回归 token（MineWorld）；(b) 因果化扩散 + 少步蒸馏（Matrix-Game 2.0、Vid2World、Hunyuan-GameCraft）；(c) 闭源大规模自回归（Genie 3）。2025 下半年 (b) 成为开源主流，核心使能技术是 Self-Forcing 类蒸馏 + KV cache 流式推理；自回归路线仅剩 token 化简洁性优势，实时性竞赛已被蒸馏扩散终结。

2. **记忆成为新前线**：长时一致性从上下文窗口转向结构化外部记忆——WorldPlay（显式 3D 几何）、Context-as-Memory、Long-term Spatial Memory（2506.05284）、Matrix-Game 3.0（2604.08995，long-horizon memory）同期涌现。隐式 vs 显式记忆之争是 2026 年最值得追踪的路线分歧。

3. **评测层成形**：WBench（多轮交互视频世界模型基准，2605.25874）、WorldMark 出现，领域开始有自己的 benchmark 层；动作跟随精度、revisit consistency、下游决策价值成为 FVD 之外的新指标轴。

4. **闭源-开源对照实验**：Genie 3（闭源、通用、强一致性）与 Matrix-Game 2.0（开源、同规格实时性）构成天然对照组——证明实时流式世界模型的关键不在算力垄断，而在数据管线（千小时带标注游戏视频）+ 蒸馏算法。

5. **从按键到自然语言**：Genie 3 的 promptable world events、GameCraft-2 的 instruction-following 指向同一方向——世界模型的控制接口正从低层动作（键鼠）走向语义指令，为"程序化生成为玩法服务"铺路。

## 开放问题（面试追问）

1. **世界模型的物理正确性边界**：当前所有系统（含 Genie 3）的物理都是"表象级"（看起来合理，算起来不对）。要做到可交互物理（碰撞、破坏、流体），是继续靠 scale 涌现，还是必须引入显式物理引擎混合架构？

2. **世界模型作为 agent 训练环境的可信度**：Genie 3 + SIMA 展示了 agent 在生成世界中训练的前景，但如果世界模型本身有系统性偏差（类似 EnvSimBench 对 LLM 模拟器的警告），agent 会不会在"幻觉世界"中学到错误策略？如何为世界模型建立 sim-to-real 的可信度保证？

3. **显式记忆与可破坏世界的根本冲突**：WorldPlay 的持久几何记忆假设世界静态，而游戏乐趣恰恰来自可改变的世界（挖掘、建造、破坏）。是否存在"可编辑的显式记忆"架构——几何记忆本身支持写操作与版本管理？

4. **评测的 Goodhart 风险**：WBench/WorldMark 类基准出现后，模型会不会针对基准的过场动画式一致性过拟合，而真实 gameplay 中的长尾交互（极端动作、反常操作）依然崩坏？如何设计对抗性交互评测？

5. **神经游戏引擎的经济学**：720p/25fps 的生成成本 vs 传统渲染管线的成本曲线何时交叉？云游戏 + 世界模型的组合（渲染即推理）会不会比本地 GPU 渲染更便宜？这将决定神经游戏引擎是研究玩具还是产业方向。

---

## 面试谈资

### 30 秒

> 2025–2026 年世界模型领域的核心进展：Genie 3 实现 720p/24fps 分钟级可玩世界但闭源；Matrix-Game 2.0 用 Self-Forcing 蒸馏 + 千小时数据管线追平其实时性且开源；MineWorld 证明自回归 token 路线可行；Hunyuan-GameCraft 用混合历史条件平衡记忆与成本；Vid2World 给出预训练视频扩散的通用改造配方；WorldPlay 引入显式 3D 记忆解决场景重访漂移。共同趋势：实时性已被蒸馏扩散解决，战场转向长时记忆与物理正确性。

### 2 分钟

> 三个里程碑：
> 1. **实时性突破**（Matrix-Game 2.0 / Genie 3）：720p/25fps 流式生成达成，开源与闭源同月到岗。核心技术是因果化改造（chunk-wise 因果注意力 + KV cache）+ Self-Forcing 少步蒸馏（学生在自己 rollout 上算分布匹配损失，消除 exposure bias）。
> 2. **记忆范式转向**（WorldPlay）：长时一致性的答案从"更长的上下文"转向"结构化外部记忆"——显式 3D 几何表征让场景重访不漂移，代表隐式 → 显式记忆的范式转向，与 Hunyuan-GameCraft 的混合历史条件（近高远低有损压缩）形成光谱两端。
> 3. **路线地图清晰化**（Vid2World + IGV 综述）：从头训练（MineWorld）、蒸馏加速（Matrix-Game 2.0）、预训练改装（Vid2World）三条路线对应不同资源约束；IGV 综述提供 taxonomy，而 2025 下半年的爆发（Genie 3、显式记忆、promptable events）正在改写它。
>
> 未来的关键问题：
> - **物理正确性**：表象级物理 → 可交互物理，靠涌现还是混合引擎？
> - **agent 训练可信度**：世界模型即环境，但幻觉环境会教出错误策略，sim-to-real 保证怎么做？
> - **控制接口语义化**：从键鼠到自然语言（promptable events / instruction-following），世界模型正在变成"可对话的游戏引擎"。

---

## 相关链接

| 资源 | 类型 | 链接 | 备注 |
|------|------|------|------|
| Genie 3 | 博客 | https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/ | 无 arXiv 论文，数字以官方声明为准 |
| MineWorld | 论文+代码 | https://arxiv.org/abs/2504.08388 | MSRA，完全开源 |
| Matrix-Game 2.0 | 论文+权重 | https://arxiv.org/abs/2508.13009 | Skywork AI，Self-Forcing 蒸馏 |
| Hunyuan-GameCraft | 论文+代码 | https://arxiv.org/abs/2506.17201 | 腾讯混元，13B 开源 |
| Vid2World | 论文 | https://arxiv.org/abs/2505.14357 | ICLR 2026，清华龙明盛组 |
| IGV Survey | 综述 | https://arxiv.org/abs/2504.21853 | 领域地图，注意时效 |
| WorldPlay | 论文 | https://arxiv.org/abs/2512.14614 | 显式 3D 几何记忆 |
| Hunyuan-GameCraft-2 | 论文 | https://arxiv.org/abs/2511.23429 | instruction-following 续作 |
| Long-term Spatial Memory | 论文 | https://arxiv.org/abs/2506.05284 | 显式记忆谱系 |
| Matrix-Game 3.0 | 论文 | https://arxiv.org/abs/2604.08995 | long-horizon memory 续作 |
| WBench | 基准 | https://arxiv.org/abs/2605.25874 | 多轮交互世界模型 benchmark |

---

## 人类执行任务

- [ ] 精读 Matrix-Game 2.0 的 Self-Forcing 蒸馏章节，推导分布匹配损失与 exposure bias 的关系（45 min）
- [ ] 精读 Vid2World 的 causalization 章节，对比其去噪调度与 Matrix-Game 的异同（30 min）
- [ ] 浏览 Genie 3 官方博客 demo，记录 promptable events 的交互案例（15 min）
- [ ] 思考并回答："显式 3D 记忆（WorldPlay）与隐式上下文记忆（Genie 3）在 10 倍 scale 下各自的失效模式是什么？"（写 200 字）（20 min）
- [ ] 在 Obsidian 中创建 [[Genie-3]], [[MineWorld]], [[Matrix-Game-2.0]], [[Hunyuan-GameCraft]], [[Vid2World]], [[WorldPlay]], [[IGV-Survey]] 笔记卡片

---

*创建时间：2026-07-20*
*维护者：AIResearchVault*
