---
tags: [paper, game-benchmark, llm-agent, evaluation, long-horizon, generalization]
aliases: [Game-Benchmarks-Latest-2025-2026]
created: 2026-07-20
---

# 方向五：游戏 Agent 基准与评估（2025–2026 最新论文）

> **核心问题**：如何设计能真实度量 LLM/VLM Agent 游戏能力的 benchmark？如何防止数据泄漏、隔离延迟与 scaffolding 干扰、评估 long-horizon 自主性与 generalization？
> **技术栈**：Real-time Game Benchmark + MCP 接口 + Procedural Generation + GUI Agent 评估 + Long-horizon Reasoning
> **关联**：[[01a-LLM-Agent-in-Games]], [[01d-sandbox-latest]], [[Agent-Harness-Game-AI-2026-06-29]], [[01-Game-AI-研究库总览]]

---

## 核心问题定义

```
问题形式化：给定 Agent π_θ 与游戏环境 G=(S, A, P, R, Ω)，benchmark 的设计目标是度量函数 M: π → 指标向量：
1. 观测空间 Ω：原始像素（VideoGameBench）/ 文本（TextQuests）/ ASCII（GVGAI-LLM）/ GUI 截图（FlashAdventure）
2. 动作空间 A：模拟器按键 / 文本命令 / GUI 操作（点击、拖拽）
3. 进度度量 M：checkpoint 占比 / milestone 完成率 / meaningful step ratio / Mean Harm
4. 隔离变量：inference latency（Lite 设置）、scaffolding（禁攻略）、泄漏（保密游戏 / canary GUID / 程序化生成）

Benchmark 设计的核心矛盾：
- 真实感 vs 可控性：完整通关最真实，但评估成本高、进度粒度粗
- 防泄漏 vs 可复现：保密游戏防污染，但无法公开审计；程序化生成可无限刷新，但有 domain gap
- 去 scaffolding vs 公平比较：移除辅助信息暴露真实能力，但与早期工作不可比
- 实时性 vs 推理深度：实时设置测部署可行性，暂停设置测纯智能上限
```

**游戏 Benchmark 在 Agent 评估生态中的位置**：
- **能力探针**：把 perception、spatial reasoning、memory、planning 形式化为可测指标
- **防污染前线**：保密游戏、程序化生成、canary GUID 是对抗 benchmark overfitting 的三条路线
- **瓶颈定位器**：Lite 设置、模态消融、模块消融帮助定位失败原因（latency？记忆？推理？）
- **训练信号源**：专家轨迹 SFT（Orak）、meaningful step ratio（GVGAI-LLM）从评估指标走向训练奖励

---

## 关键论文

### 1. VideoGameBench: Can Vision-Language Models Complete Popular Video Games?

- **作者**：Alex L. Zhang, Thomas L. Griffiths, Karthik R. Narasimhan, Ofir Press (Princeton University)
- **来源**：arXiv:2505.18134（v1 2025-05-23；v3 2026-05-14）
- **链接**：https://arxiv.org/abs/2505.18134
- **项目**：videogamebench 官网（论文内提供）

#### AI 预读（150 字）

> VideoGameBench 由 10 款 1990 年代经典视频游戏（含 3 款保密游戏）组成的实时 benchmark，VLM 只能看原始画面和一段高层目标/操作说明，直接以按键操作通关完整游戏。结果显示最强模型 Gemini 2.5 Pro 与 Claude 3.7 Sonnet 在实时设置下仅完成 0.48% 的游戏进度；在暂停等推理的 Lite 设置下也仅 1.6%，而人类可轻松通关。论文指出 inference latency 是实时游戏的主要瓶颈，并把 perception、spatial navigation、memory management 等"人类直觉能力"形式化为可测指标。

#### 3 个引导问题

1. **保密游戏 split 与 scaffolding 规则能否真正防止预训练泄漏？** dev/test split + 3 款保密游戏是主动防御，但网络上的攻略、通关视频仍可能进入训练语料。如何审计一个闭源模型是否"见过"某款游戏？canary GUID（TextQuests 方案）能否推广到视觉模态？

2. **checkpoint 进度度量 vs 连续进度信号**：VideoGameBench 用自动检测的 checkpoint 占比度量进度（无需读游戏内存），粒度较粗。离散 checkpoint 与连续进度信号（如血量、金币、探索面积）哪个更适合做 RL 奖励？粗粒度信号是否会导致 reward hacking（agent 学会"刷 checkpoint"而非真正推进游戏）？

3. **实时设置下 latency 与智能的 trade-off**：实时版 0.48% vs Lite 版 1.6% 的落差说明延迟是主要瓶颈。是否存在"足够快的弱模型胜过慢强模型"的区间？这对端侧部署（如游戏 NPC、机器人控制）的模型选型意味着什么——应该优化 tokens/s 还是单步推理质量？

#### 重点章节标记

1. **Benchmark 设计章节**：严格 scaffolding 规则——禁止模型访问攻略等辅助信息，只给原始像素 + 高层目标说明
2. **Dev/Test split 与保密游戏**：3 款保密游戏专门测 generalization、防数据泄漏
3. **Lite 设置**：等待模型输出时暂停游戏时钟，隔离 latency 因素
4. **关键结果**：实时版最高 0.48% 进度，Lite 版最高 1.6%；所有模型都无法越过大多数游戏的开局阶段
5. **自动 checkpoint 检测机制**：无需读游戏内存的进度度量方法

#### 面试谈资

- **30 秒**：普林斯顿的 benchmark 让 VLM 只靠看屏幕通关 90 年代游戏，最强模型只完成 0.48%——AI 在数学上超越人类，却在人类小孩的直觉能力上惨败。
- **2 分钟**：核心设计三点——去 scaffolding（只给原始像素+目标说明）、保密游戏防泄漏（dev/test split）、Lite 设置隔离 latency。关键数字：Gemini 2.5 Pro / Claude 3.7 Sonnet 实时版 0.48% 进度，Lite 版也仅 1.6%，而人类轻松通关。它把 Moravec 悖论做成了可测的 benchmark：模型在数学奥赛上超人类，却在 perception/memory/实时交互这些"人类直觉能力"上全军覆没。对工程的启示是 latency 和智能同样重要——实时场景下推理再强，来不及按键也是零分。

---

### 2. Orak: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games

- **作者**：Dongmin Park, Minkyu Kim, Beongjun Choi, …, Bilal Kartal, Yoshi Suhara, Kangwook Lee, Jaewoong Cho 等（KRAFTON、威斯康星大学麦迪逊分校等机构合作，以论文署名页为准）
- **来源**：arXiv:2506.03610（v1 2025-06-04；v3 2026-04-14）
- **链接**：https://arxiv.org/abs/2506.03610
- **代码**：论文提供 GitHub 代码与 fine-tuning 数据集链接

#### AI 预读（150 字）

> Orak 针对现有游戏基准三大缺陷——游戏类型覆盖不全、缺乏对 agentic module 的系统消融、缺少 fine-tuning 数据——提出覆盖全部主流游戏类型的 12 款热门游戏 LLM agent 基准，是 BALROG 的直接后继与扩展。基于 MCP（Model Context Protocol）构建 plug-and-play 接口，支持记忆、规划、反思等 agentic 策略模块的即插即用替换与可复现消融。同时发布专家 LLM 游戏轨迹 fine-tuning 数据集，并提供 leaderboard 与 LLM battle arena 统一评估框架。

#### 3 个引导问题

1. **MCP 抽象的信息损失**：MCP 把每款游戏封装为标准 server，agent 通过统一 tool 接口读写 observation/action。这种抽象会不会把游戏特有的状态结构（如 RTS 的小地图、格斗游戏的帧数据）压平成统一 schema，损失关键信息？统一接口的便利性与信息保真度如何权衡？

2. **LLM 专家轨迹 SFT 的天花板**：fine-tuning 数据集由强 LLM 在多 genre 游戏中的专家轨迹构成，但教师模型本身的游戏能力有限（VideoGameBench 显示前沿模型进度 <2%）。用弱教师的轨迹做 SFT，学生能否超越教师？与 RL 在游戏环境直接训练相比，behavior cloning 的天花板在哪里？

3. **battle arena 排名的统计可靠性**：LLM battle arena 用 pairwise 对战产生 Elo 式排名，但游戏对战有先手优势、随机种子、采样方差。需要多少局对战才能让排名置信区间收敛？开局先手优势如何校准？

#### 重点章节标记

1. **12 款游戏的 genre 覆盖**：action、RTS、RPG、sports、puzzle 等全主流类型
2. **MCP plug-and-play 架构**：游戏封装为 MCP server，agentic 模块可替换消融
3. **消融实验**：输入模态（text vs vision）、agentic 策略开关、fine-tuning 前后对比
4. **Leaderboard + Battle Arena**：统一评估框架（具体分数见论文表格）
5. **Fine-tuning 数据集**：跨 genre 专家 LLM 游戏轨迹

#### 面试谈资

- **30 秒**：BALROG 的下一代——12 款全 genre 游戏 + MCP 标准接口，第一次能系统消融"记忆/规划模块到底有没有用"，还附带 fine-tuning 数据集。
- **2 分钟**：Orak 针对游戏基准三大缺陷：genre 覆盖不全、无法消融 agentic 模块、没有训练数据。三个卖点——12 款游戏覆盖全部主流类型；MCP 把游戏封装成标准 server，memory/planner/self-reflection 模块即插即用，第一次能严谨回答"反思模块到底有没有用"；发布专家 LLM 轨迹 SFT 数据集。它把游戏 agent 研究从"刷分"转向"模块化科学"。但软肋是教师模型质量决定 SFT 上限——前沿模型自己游戏都玩不好，专家轨迹的"专家"含金量存疑。battle arena 的 Elo 排名对采样方差和先手优势敏感，引用排名时要看置信区间。

---

### 3. TextQuests: How Good are LLMs at Text-Based Video Games?

- **作者**：Long Phan, Mantas Mazeika, Andy Zou, Dan Hendrycks (Center for AI Safety / Carnegie Mellon University / Gray Swan AI)
- **来源**：arXiv:2507.23701（2025-07-31）
- **链接**：https://arxiv.org/abs/2507.23701
- **项目**：https://www.textquests.ai/
- **代码**：https://github.com/centerforaisafety/textquests（评测脚本在 simple-evals）

#### AI 预读（150 字）

> TextQuests 基于 Infocom 25 款经典文字冒险游戏构建 long-horizon benchmark，是 Jericho 的精神续作。这些游戏人类需 30 小时以上、数百步精确操作才能通关。benchmark 禁止使用外部工具，专测模型的 intrinsic long-context reasoning 与 trial-and-error 学习能力。指标为专家标注 checkpoint 的 Game Progress 与 Mean Harm 伤害指标，并引入 autosave 机制可控研究试错学习，数据集带 canary GUID 防训练污染。实验显示 SOTA LLM 无提示时几乎无法取得实质进度、无模型能完整通关任何一款游戏；提供结构化 clue 与 autosave 后性能显著提升，说明瓶颈在动态长上下文推理而非知识。

#### 3 个引导问题

1. **Game Progress 标注的一致性与自动化**：专家标注 checkpoint 存在主观性，跨标注者一致性如何保证？能否用类似 FlashAdventure 的 CUA-as-a-Judge 思路自动标注？自动标注的误差会如何影响模型排名？

2. **autosave 与真实任务的映射**：autosave/restore 相当于给 agent 免费的 backtracking——现实中多数任务不可逆（发了的邮件收不回）。autosave 设置下测得的 trial-and-error 学习能力，有多少能迁移到不可逆任务？是否应设计"有限次存档"或"存档代价"机制？

3. **Mean Harm 作为通用 agent 安全维度**：TextQuests 把伤害指标纳入游戏评估（agent 在游戏中的危险/破坏性操作）。这个指标能否迁移为通用 agent 安全评估维度——比如编码 agent 误删文件、Web agent 误下单的"harm 计数"？游戏内的 harm 与现实 harm 的严重性如何对齐？

#### 重点章节标记

1. **禁工具设定**：隔离 intrinsic reasoning——无搜索、无计算器、无代码执行
2. **Game Progress + Mean Harm 双指标**：进度与安全性联合评估
3. **Autosave 机制**：可控研究 trial-and-error 学习的实验设计
4. **关键结果**：无模型完整通关任何一款游戏；结构化 clue + autosave 显著提升 → 瓶颈在动态长上下文推理而非知识
5. **Canary GUID**：数据集的防训练污染设计

#### 面试谈资

- **30 秒**：CAIS 出的文字游戏 benchmark，人类 30 小时通关的游戏，最强 LLM 一个都通不了关——long-horizon 自主性仍是硬伤。
- **2 分钟**：TextQuests 是 Infocom 文字冒险（Jericho 的精神续作）升级为前沿 LLM 的 long-horizon 评测。设计亮点有三：禁工具的"自包含"设定，隔离 intrinsic reasoning，不许用搜索和代码执行；autosave 机制可以可控地研究试错学习；Mean Harm 把安全纳入游戏指标。最关键的结论是诊断性的：给结构化 clue 和 autosave 后性能显著提升，说明模型缺的不是知识——80 年代游戏的知识早就在训练语料里——缺的是长上下文状态管理：记住自己试过什么、当前 inventory 有什么、谜题之间的依赖关系。canary GUID 防污染的设计也值得所有 benchmark 借鉴。

---

### 4. GVGAI-LLM: Evaluating Large Language Model Agents with Infinite Games

- **作者**：Yuchen Li 等（GVGAI 框架社区；提交者 Yuchen Li，机构以论文署名页为准）
- **来源**：arXiv:2508.08501（v1 2025-08-11；v3 2026-05-16）
- **链接**：https://arxiv.org/abs/2508.08501

#### AI 预读（150 字）

> GVGAI-LLM 基于 General Video Game AI 框架构建，包含 118 款街机风格游戏，场景用紧凑 ASCII 字符表示以便 LLM 处理，是当前最大规模的游戏 LLM 基准之一。关键创新是利用 VGDL（Video Game Description Language）程序化生成新游戏规则与关卡，可无限刷新评测集，天然抵抗 benchmark 过拟合。定义 meaningful step ratio、step efficiency、overall score 等可解释指标。Zero-shot 评测显示当前模型持续出现空间与逻辑错误；structured prompting 与 spatial grounding 技术带来部分提升，但 benchmark 远未被解决。

#### 3 个引导问题

1. **程序化生成的难度与多样性控制**：VGDL 可无限生成新游戏，但如何保证生成游戏的难度分布可控、多样性充分？随机生成的规则组合可能产生不可解或平庸的游戏。是否需要"生成-验证"闭环（用求解器确认可解性）？

2. **meaningful step ratio 作为训练信号**：该指标度量 agent 每一步是否"有意义"（推进游戏状态）。能否从评估指标转化为 RL 奖励或 SFT 数据筛选标准？用 step ratio 做奖励会不会鼓励 agent 采取短视的"每步都有反馈"策略，牺牲长期规划？

3. **ASCII vs 像素观测的能力解耦**：GVGAI-LLM 用 ASCII 表征把 spatial reasoning 从视觉感知中解耦出来。同一模型在 ASCII 与像素观测下的 spatial reasoning 差距有多大？如果 ASCII 下依然犯错，说明问题是推理而非感知——这个实验是否已经在论文中完成？

#### 重点章节标记

1. **118 款游戏 zero-shot 大规模评测**：当前最大规模游戏 LLM 基准之一
2. **VGDL 程序化生成**：无限刷新的 anti-overfitting benchmark 机制
3. **ASCII 紧凑表征**：无需视觉模态即可测 spatial reasoning
4. **可解释指标体系**：meaningful step ratio / step efficiency / overall score
5. **关键发现**：prompting 技术只带来部分提升 → 暗示是模型能力短板而非提示问题

#### 面试谈资

- **30 秒**：用游戏描述语言无限生成新游戏的 benchmark——天然免疫 benchmark 污染，118 款游戏证明 LLM 连基础空间推理都不稳。
- **2 分钟**：GVGAI-LLM 的核心思路是用 VGDL（Video Game Description Language）程序化生成新游戏——评测集可以无限刷新，从根本上解决 benchmark 被刷穿的问题，这与 VideoGameBench 的保密游戏、TextQuests 的 canary GUID 是三条不同的防污染路线。第二个巧思是 ASCII 紧凑表征，把 spatial reasoning 从视觉感知中解耦出来单测——不需要 VLM，纯文本 LLM 就能测。118 款游戏的 zero-shot 评测发现模型持续犯空间与逻辑错误，而 structured prompting 只能部分缓解，这暗示是模型能力短板。meaningful step ratio 这个可解释指标很有潜力从评估走向训练信号。

---

### 5. FlashAdventure: A Benchmark for GUI Agents Solving Full Story Arcs in Diverse Adventure Games

- **作者**：Jaewoo Ahn 等（EMNLP 2025 Main；机构以论文署名页为准）
- **来源**：arXiv:2509.01052（v1 2025-09-01；EMNLP 2025 Main）
- **链接**：https://arxiv.org/abs/2509.01052
- **项目**：有项目主页

#### AI 预读（150 字）

> FlashAdventure 由 34 款 Flash 冒险游戏组成，是首个以"完整故事线通关"（full story arc completion）为评估目标的游戏 GUI 基准。论文形式化了 observation-behavior gap 概念——agent 观测到信息 ≠ 在行为上利用信息，记住并利用早前游戏信息是核心困难。同时提出 CUA-as-a-Judge 自动游戏评估器（用 computer-use agent 评估进度，免人工标注）与 COAST 框架（长期 clue memory 驱动的序列任务规划）。实验显示当前 GUI agent 普遍无法完成完整故事线；COAST 通过弥合 observation-behavior gap 显著提升 milestone 完成率，但与人类仍有显著差距。

#### 3 个引导问题

1. **observation-behavior gap 的归因**：信息进入了 context 却没进入决策——这是 memory 容量问题（信息被淹没）还是 credit assignment 问题（不知道该信息对当前决策有用）？如何设计实验区分两者？例如给 agent 显式提示"回忆第 N 步看到的信息"能否消除 gap？

2. **CUA-as-a-Judge 的评估有效性**：用 computer-use agent 自动判断游戏进度，judge 本身的评估误差会传递给被测 agent 的排名。judge 与 agent 若是同源模型，会不会产生系统性偏置（比如 judge 认不出自己同类犯的错误）？需要多少人工抽检来校准 judge？

3. **clue memory 结构的自动学习**：COAST 的 clue memory 依赖人工设计的 memory schema（存什么、怎么组织）。能否让 agent 自动学习"什么该存、什么该忘"？这与 RAG 中的检索策略学习、RL 中的 experience replay 优先级有何异同？

#### 重点章节标记

1. **Full story arc 评估目标**：从"单任务完成"升级为"完整故事线通关"
2. **Observation-behavior gap 形式化**：观测到信息 ≠ 行为上利用信息
3. **CUA-as-a-Judge**：computer-use agent 自动评估游戏进度
4. **COAST 框架**：长期 clue memory 驱动规划，提升 milestone 完成率
5. **关键结果**：当前 GUI agent 普遍无法完成完整故事线，与人类差距显著

#### 面试谈资

- **30 秒**：让 GUI agent 完整通关冒险游戏故事线，发现它们"看到了但用不上"——observation-behavior gap 是长程 agent 的核心瓶颈。
- **2 分钟**：FlashAdventure（EMNLP 2025 Main）用 34 款 Flash 冒险游戏测 GUI agent 的完整故事线通关能力。三个创新：full story arc 评估目标、CUA-as-a-Judge 自动裁判、COAST 的 clue memory 规划框架。最有价值的概念是 observation-behavior gap：信息进了 context 不等于进了决策——agent 在第 5 步看到密码，第 50 步需要时却用不上。这直接解释了为什么单纯增大 context window 收益递减，也说明长程 agent 的关键不是"记住一切"而是"知道什么值得记、何时该回忆"。COAST 用 clue memory 弥合这个 gap，提升了 milestone 完成率，但 memory schema 仍是人工设计——自动学习记忆结构是下一步。

---

### 6. VisEscape: A Benchmark for Evaluating Exploration-driven Decision-making in Virtual Escape Rooms

- **作者**：Seungwon Lim 等（提交者 Seungwon Lim，机构以论文署名页为准）
- **来源**：arXiv:2503.14427（v1 2025-03-18；v3 2025-05-27）
- **链接**：https://arxiv.org/abs/2503.14427

> ⚠️ 注：本方向的调研简报在本文档截断（仅有元信息与核心摘要），以下从简整理，其余内容以论文页面为准。

#### AI 预读（150 字）

> VisEscape 由 20 个虚拟密室逃脱组成，唯一指令是"逃出房间"，考察 exploration-driven planning：agent 必须主动搜索环境、收集信息、反复试错，并在动态变化的环境中迭代构建与修正 spatial-temporal 知识。与其他给定明确任务清单的 benchmark 不同，VisEscape 的目标发现本身就是挑战的一部分。实验显示 SOTA 多模态模型基本无法逃脱。（更详细的贡献、实验数字与局限分析以论文页面为准。）

#### 3 个引导问题

1. **开放式目标 vs 给定目标**：唯一指令"逃出房间"意味着 agent 必须自己发现子目标（找钥匙→解密码→开门）。这种 exploration-driven 设定与 VideoGameBench 的"高层目标说明"相比，额外考察了什么能力？目标发现（goal discovery）能否单独量化？

2. **动态环境中的知识修正**：密室环境会动态变化（谜题解开后出现新道具），agent 需要迭代修正已建立的 spatial-temporal 知识。这与 FlashAdventure 的 observation-behavior gap 有何关联——看到环境变化后，agent 能否在行为上体现知识更新？

3. **密室逃脱作为微缩的 embodied AI 测试**：密室逃脱浓缩了搜索、记忆、推理、工具使用——它是否是评估通用 embodied agent 的高性价比代理任务？与真实机器人任务相比，虚拟密室缺少了哪些维度（物理交互、连续控制、安全约束）？

#### 重点章节标记

- 详细章节结构与实验数字请直接参考论文页面（简报截断，未提供）。

#### 面试谈资

- **30 秒**：20 个虚拟密室逃脱，只给 agent 一句"逃出房间"，考察探索驱动的规划——SOTA 多模态模型基本都逃不出来。
- **2 分钟**：VisEscape 的独特之处在于目标的最小化：不给任务清单、不给攻略提示，就一句"逃出去"。agent 必须主动搜索环境、收集信息、反复试错，并在动态变化的环境中迭代构建和修正 spatial-temporal 知识。它考察的是 exploration-driven planning——目标发现本身就是挑战的一部分，这与给足说明书的 benchmark 形成互补。结果同样不乐观：SOTA 多模态模型基本无法逃脱，再次印证 long-horizon 自主性是当前多模态 agent 的硬伤。（本文简报对该论文的整理截断，深度细节建议精读原文。）

---

## 方向横向观察

### 技术栈对比

| 维度 | VideoGameBench | Orak | TextQuests | GVGAI-LLM | FlashAdventure | VisEscape |
|------|---------------|------|------------|-----------|----------------|-----------|
| **游戏类型** | 90 年代经典视频游戏 | 12 款全 genre | Infocom 文字冒险 | 118 款街机 | 34 款 Flash 冒险 | 20 个虚拟密室 |
| **观测模态** | 原始像素（VLM） | text + vision | 纯文本 | ASCII 文本 | GUI 截图 | 多模态 |
| **评估目标** | 完整通关进度 | 模块化消融 + 排名 | long-horizon 通关 + Harm | zero-shot 大规模 | full story arc | exploration-driven 逃脱 |
| **防污染机制** | 保密游戏 split | — | canary GUID | 程序化生成（无限刷新） | — | — |
| **关键发现** | 实时版仅 0.48% 进度 | MCP 接口支持模块消融 | 无模型通关任何游戏 | prompting 仅部分缓解 | observation-behavior gap | SOTA 模型基本无法逃脱 |
| **独特贡献** | Lite 设置隔离 latency | fine-tuning 数据集 + battle arena | autosave + Mean Harm | meaningful step ratio | CUA-as-a-Judge + COAST | 最小化目标设定 |

### 横向趋势

1. **防污染三条路线的汇合**：保密游戏（VideoGameBench）、canary GUID（TextQuests）、程序化生成（GVGAI-LLM）分别代表"藏、标记、造"三种对抗 benchmark overfitting 的哲学。程序化生成是唯一可持续的方案，但 domain gap 未定。

2. **从"刷分"到"诊断"**：新一代 benchmark 的共同转向——不再只报一个总分，而是设计隔离变量的实验（Lite 设置、禁工具设定、模块消融、ASCII 解耦），定位失败的具体原因（latency？记忆？推理？）。

3. **observation-behavior gap 成为核心概念**：FlashAdventure 形式化的"看到 ≠ 用上"现象，在 TextQuests（clue 一给就好转）和 GVGAI-LLM（spatial grounding 部分有效）中反复出现，可能是长程 agent 的统一瓶颈。

4. **评估与训练的边界消融**：Orak 的 SFT 数据集、GVGAI-LLM 的 step ratio、TextQuests 的 autosave 机制，都显示 benchmark 设计正在向训练基础设施演化——评估指标即训练信号。

---

## 面试谈资

### 30 秒

> 2025-2026 游戏 Agent 基准的核心结论：VideoGameBench 显示 VLM 实时通关率仅 0.48%；TextQuests 显示无模型能通关任何一款文字冒险；Orak 用 MCP 接口实现 agentic 模块系统消融；GVGAI-LLM 用程序化生成对抗 benchmark 污染；FlashAdventure 发现 observation-behavior gap 是长程瓶颈；VisEscape 证明探索驱动规划仍未解决。AI 的短板不在知识，在 long-horizon 自主性。

### 2 分钟

> 三个里程碑式发现：
> 1. **Moravec 悖论的可测化**（VideoGameBench）：最强 VLM 实时通关 90 年代游戏仅 0.48% 进度，Lite 设置（暂停等推理）也仅 1.6%——数学奥赛超人类的 AI，在儿童级游戏直觉上全军覆没，latency 与智能同样重要。
> 2. **长上下文状态管理是瓶颈**（TextQuests + FlashAdventure）：TextQuests 发现给 clue 就好转 → 缺的不是知识是状态管理；FlashAdventure 形式化 observation-behavior gap → 信息进 context 不等于进决策，解释了 context window 收益递减。
> 3. **Benchmark 防污染军备竞赛**：保密游戏（藏）、canary GUID（标记）、VGDL 程序化生成（造）三条路线并行，程序化生成是唯一可持续方案。
>
> 未来关键问题：
> - **评估即训练**：Orak 的 SFT 数据集、GVGAI-LLM 的 step ratio 预示 benchmark 与训练基础设施融合
> - **observation-behavior gap 的统一解释**：memory 容量问题还是 credit assignment 问题？跨论文交叉验证
> - **从游戏到现实**：Mean Harm、autosave、judge 自动化等游戏评估技术向通用 agent 评估迁移

---

## 相关链接

| 资源 | 类型 | 链接 | 备注 |
|------|------|------|------|
| VideoGameBench | 论文 | https://arxiv.org/abs/2505.18134 | VLM 实时通关 benchmark |
| Orak | 论文 | https://arxiv.org/abs/2506.03610 | BALROG 后继，MCP 接口 |
| TextQuests | 项目 | https://www.textquests.ai/ | Infocom 文字冒险 benchmark |
| TextQuests 代码 | GitHub | https://github.com/centerforaisafety/textquests | CAIS 官方实现 |
| GVGAI-LLM | 论文 | https://arxiv.org/abs/2508.08501 | 程序化生成游戏 benchmark |
| FlashAdventure | 论文 | https://arxiv.org/abs/2509.01052 | EMNLP 2025 Main |
| VisEscape | 论文 | https://arxiv.org/abs/2503.14427 | 虚拟密室逃脱 benchmark |
| BALROG | 论文 | （库中已收录） | Orak 的前作 |
| Jericho | 项目 | （库中已收录） | TextQuests 的精神前作 |

---

*创建时间：2026-07-20*
*维护者：AIResearchVault*
