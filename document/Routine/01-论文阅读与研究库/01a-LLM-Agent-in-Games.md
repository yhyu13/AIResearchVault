---
tags: [paper, game-ai, llm-agent, agent-harness, voyager, minedojo]
aliases: [LLM-Agent-in-Games]
created: 2026-07-02
---

# 方向一：LLM / Agent in Games

> **核心问题**：如何让 LLM Agent 在复杂游戏环境中可靠执行？
> **技术栈**：RL + LLM + Tool Use + Code Generation + Harness Engineering
> **关联**：[[01-Game-AI-研究库总览]], [[Agent-Harness-Game-AI-2026-06-29]]

---

## 核心问题定义

```
问题形式化：给定游戏环境 G=(S, A, P, R)，LLM Agent π_θ 需要
1. 观察：o_t = Obs(s_t)  — 多模态（像素 + 结构化状态 + 文本）
2. 推理：plan_t = LLM(o_{≤t}, goal)  — 长期规划 + 任务分解
3. 动作：a_t = Action(plan_t)  — 异构（键盘/鼠标/代码/自然语言）
4. 验证：V(a_t, s_t) → {pass, fail, retry}  — 可执行性 + 安全性
```

**Game 场景的特殊性**（vs. 代码/浏览器 Agent）：
- **动作空间异构**：离散命令 + 连续控制 + 自然语言 + 代码生成
- **状态表示多模态**：像素 + 结构化数据（坐标/ID）+ 文本聊天
- **长程依赖**：100+ 步任务，需要记忆和技能组合
- **实时性约束**：部分游戏需要实时响应（帧率敏感）
- **创造性评估**：成功标准模糊（"好建筑"没有标准答案）

---

## 关键论文

### 1. Voyager — 终身学习 Minecraft Agent

- **作者**：Guanzhi Wang et al. (NVIDIA, Caltech, Stanford, etc.)
- **来源**：NeurIPS 2023
- **链接**：https://voyager.minedojo.org
- **代码**：https://github.com/MineDojo/Voyager

#### AI 预读（150 字）

> Voyager 提出"自动课程（Automatic Curriculum）+ 技能库（Skill Library）+ 迭代提示机制（Iterative Prompting）"的三模块架构，让 LLM Agent 在 Minecraft 中实现终身学习。核心创新是将动作空间设为**代码生成**（Python/Mineflayer API），使 Agent 可以组合原子技能形成复杂行为。通过自动课程发现新任务，通过技能库存储和检索可复用代码片段，通过迭代提示从执行错误中自动修复代码。无需梯度更新，纯提示工程实现开放世界的持续能力增长。

#### 3 个引导问题

1. **代码生成动作空间 vs 低层 API 动作空间**：代码生成（Voyager）的抽象层次更高，但延迟更大；低层 API（MineDojo）的响应更快，但探索空间更大。在实时游戏（如 FPS）中，哪种更合适？是否可以通过分层控制器（高层 LLM 规划 + 低层 RL 执行）结合两者？

2. **Voyager 的技能库是一个代码片段检索系统。这本质上是一个"外化记忆"机制。** 与 RAG（检索增强生成）相比，技能库的优势是**可执行性**（检索到的代码可以直接运行验证）。但如果代码片段之间存在依赖关系（技能 A 依赖技能 B），如何保证检索和组合的正确性？

3. **自动课程（Automatic Curriculum）由 LLM 根据当前状态和目标生成。** 这是否会导致课程偏向于 LLM 先验知识中的"常见任务"？如何量化课程的多样性、难度梯度和覆盖度？

#### 重点章节标记

1. **Section 3.1**：自动课程生成机制（curriculum prompt 设计）
2. **Section 3.2**：技能库的存储与检索（embedding + 代码执行验证）
3. **Section 3.3**：迭代提示机制（从执行错误到代码修复的闭环）
4. **Figure 3**：技能库增长曲线（终身学习的证据）
5. **Figure 5**：与 GPT-4 基线和 AutoGPT 的对比（Voyager 的关键优势在哪里？）

#### 面试谈资

- **30 秒**：Voyager 是 Minecraft 中的终身学习 Agent，用代码生成作为动作空间，通过自动课程、技能库和迭代提示实现持续能力增长，无需梯度更新。
- **2 分钟**：核心设计是**三层架构**：自动课程（根据当前能力动态生成任务）→ 技能库（用代码执行验证的可复用技能）→ 迭代提示（从错误中自动修复）。关键洞察是：在开放世界游戏中，**动作空间应该是可执行的代码**而非低层控制，因为代码天然具有组合性和可验证性。但局限也很明显：延迟高（每次动作需要 LLM 生成代码）、依赖 Minecraft 的确定性 API、且对实时游戏不适用。

---

### 2. Ghost in the Minecraft — 代码生成即动作

- **来源**：arXiv 2023
- **相关**：与 Voyager 同期，类似思路

#### 核心贡献

> 将 Minecraft 的动作空间完全交给代码生成，LLM 生成 Python 脚本控制游戏。与 Voyager 的区别在于更强调**代码的可组合性**和**沙箱执行安全**。

---

### 3. MineDojo — 大规模 Minecraft 任务基准

- **作者**：Linxi Fan et al. (NVIDIA)
- **来源**：NeurIPS 2022
- **链接**：https://minedojo.org

#### 核心贡献

> 构建了 3000+ 个多样化的 Minecraft 任务，涵盖建造、生存、战斗、探索。提供了多模态观察（像素 + 库存 + 文本）和分层动作空间（低层 API + 高层脚本）。是后续 Voyager 等工作的基础设施。

#### 关键问题

1. MineDojo 的 3000+ 任务从何而来？是手工设计还是程序化生成？
2. 任务的难度分布如何？是否存在"容易的容易，难的极难"的鸿沟？
3. 作为 Harness，MineDojo 提供了环境接口，但缺少安全沙箱和验证器——这在 Voyager 中是如何补充的？

---

### 4. OSWorld — 通用 GUI Agent 环境（含游戏）

- **来源**：ICML 2024
- **链接**：https://osworld.github.io

#### 核心贡献

> 将 Agent 环境扩展到整个操作系统（Ubuntu），游戏只是其中一种应用。关键创新是**像素级统一接口**：所有操作都基于屏幕截图和鼠标/键盘控制，无需游戏专用 API。这使得 Agent 可以操作任何游戏，但挑战是像素理解的可靠性。

---

### 5. Generative Worldcrafting — 多模态内容生成

- **来源**：CECIIS 2025
- **详情**：见 [[Agent-Harness-Game-AI-2026-06-29]]

---

### 6. Agent Harness Survey — 六组件架构

- **来源**：Preprints 2026
- **详情**：见 [[Agent-Harness-Game-AI-2026-06-29]]

---

## 技术栈对比

| 维度 | Voyager | MineDojo | OSWorld | Agent Harness |
|------|---------|----------|---------|---------------|
| 动作空间 | 代码生成 | 低层 API + 脚本 | 像素级鼠标/键盘 | 抽象接口 |
| 观察模态 | 结构化 + 像素 | 结构化 + 像素 | 纯像素 | 多模态统一 |
| 环境范围 | Minecraft | Minecraft | 任意 GUI | 通用 |
| 终身学习 | ✓ 技能库 | ✗ 单次任务 | ✗ 单次任务 | 框架支持 |
| 安全沙箱 | 代码执行 | 有限 | 系统级隔离 | 核心组件 |
| 实时性 | 低（LLM 延迟） | 中 | 低（像素处理） | 依赖实现 |
| 评估方式 | 任务完成度 | 奖励函数 | 目标检查 | 多维度 V |

---

## 开放问题（面试追问）

1. **分层控制**：在需要实时响应的游戏（如 RTS/FPS）中，是否应该设计"高层 LLM 规划 + 低层 RL/脚本执行"的分层架构？接口如何设计？

2. **代码生成的延迟**：Voyager 每次动作需要一次 LLM 调用，延迟秒级。如何通过缓存、预测、或技能编译（将常用代码预编译为低层指令）降低延迟？

3. **评估标准**：Minecraft 中"建了一个好房子"如何评估？结构完整性、美观、功能、创意——能否设计多维度评估 Harness？

4. **从 Minecraft 到通用游戏**：Minecraft 的方块世界有清晰的物理规则和离散状态空间。在开放世界 RPG（如 Skyrim）或实时竞技游戏（如 Dota 2）中，Agent Harness 需要哪些额外组件？

---

## 相关资源

| 资源 | 类型 | 链接 | 备注 |
|------|------|------|------|
| Voyager | 项目 | https://voyager.minedojo.org | 终身学习 Minecraft Agent |
| MineDojo | 项目 | https://minedojo.org | 大规模任务基准 |
| OSWorld | 项目 | https://osworld.github.io | 通用 GUI Agent |
| awesome-agent-harness | GitHub | https://github.com/RUCAIBox/awesome-agent-harness | 论文列表 |
| Voyager 精读 | 笔记 | [[Agent-Harness-Game-AI-2026-06-29]] | 预读笔记 |

---

## 人类执行任务

- [ ] 精读 Voyager 论文 Section 3（三模块架构）+ Figure 3（30 min）
- [ ] 精读 MineDojo 论文 Section 3（任务设计与观察空间）（20 min）
- [ ] 运行 Voyager GitHub 的 minimal example，观察代码生成过程（30 min）
- [ ] 回答上述引导问题，写入笔记
- [ ] 在 Obsidian 中创建 [[Voyager]], [[MineDojo]], [[OSWorld]] 笔记卡片

---

*创建时间：2026-07-02*
*维护者：AIResearchVault*
