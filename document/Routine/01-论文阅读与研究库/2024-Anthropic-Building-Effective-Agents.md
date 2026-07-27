---
tags: [paper, agent-harness, agentic-systems, workflow, llm-agent, multi-agent, anthropic, engineering-best-practices, AI-harness]
aliases: [Anthropic-Building-Effective-Agents, Building-Effective-Agents, 2024-Anthropic-Agent-Patterns]
created: 2026-07-27
updated: 2026-07-27
---

# Anthropic — Building Effective Agents: 首个 LLM 工业界对 agentic systems 的系统化分类 (2024-12)

| 字段 | 内容 |
|------|------|
| **博客/论文标题** | Building effective agents |
| **作者/机构** | Anthropic Engineering（Erik Blyakher 等） |
| **发布** | 2024-12-19 |
| **类型** | Engineering Blog Post（非 arXiv 论文，工业界最佳实践） |
| **链接** | https://www.anthropic.com/engineering/building-effective-agents |
| **配套资源** | Claude Agent SDK / Cookbook `patterns-agents-basic-workflows` |
| **同源 paper note** | 综述 [[01e-agent-harness-latest]] 第 8 篇；GameDevVault AI Harness 主题补完（第 7 篇，对位 Anthropic Computer Use） |
| **阅读日期** | 2026-07-27 |
| **精读时长** | ~30 min |

---

## 一句话总结

> Anthropic 在 2024-12-19 发布 **Building effective agents** 工程博客——**首次由 LLM 工业界头部厂商对"agentic systems"做系统化分类**：把 **workflows（5 个模式：prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer）** 和 **autonomous agents（1 个模式）** 明确切分，并主张**"成功的实现都用 simple, composable patterns 而不是 complex frameworks"**。**核心论断**："**find the simplest solution possible, and only increase complexity when needed**"——这是对 LangChain / AutoGen 等复杂框架路线的**官方反共识判断**。**对 day-job 的启发**：**Mac Game Harness 必须从单 LLM call + retrieval + in-context examples 开始**（**不是直接上 multi-agent framework**），**需要 workflow 时按 5 个模式选型**（不是全用 autonomous），**5 个模式 + 1 个 agent = 6 个原语**作为 harness 选型分类法。

---

## 核心创新点

1. **"Workflows vs Agents" 二元架构切分**。Anthropic 把 agentic systems 切成两类：
   - **Workflows** = LLMs + tools 通过**预定义代码路径**编排（人类设计 control flow）
   - **Agents** = LLM **动态指导**自身流程和工具使用（LLM 自己决定 control flow）
   
   **关键判断**：这两类**不是"高级 vs 低级"的关系**，而是"**确定性 vs 灵活性**"的 trade-off。Workflows 适合**任务清晰、可预测**的场景；Agents 适合**任务开放、不可预测**的场景。**绝大多数应用应优先 workflows**。**对 day-job 启发**：**Mac Game Harness 95% 场景应该是 workflow**（build / 编译 / 测试 / 部署 / 调试，每步流程明确），**5% 场景是 agent**（比如"在没文档的 UE 工程里自动找 bug"这种开放任务）。

2. **5 个 workflow 模式 + 1 个 agent 模式 = 6 个原语**。这是博客最具体的工业贡献：

   | # | 模式 | 控制流 | 何时用 |
   |---|------|--------|--------|
   | 1 | **Prompt chaining** | 串行 LLM call，可加 programmatic gate | 任务可清晰分解为固定子任务（如 outline → 写文档 → 检查 → 重写）|
   | 2 | **Routing** | 分类输入 → 派发到专门子任务 | 复杂任务有 distinct categories（客服：一般 / 退款 / 技术支持）|
   | 3 | **Parallelization** | Sectioning（独立子任务并行）/ Voting（同一任务多次跑） | 子任务可并行（guardrail + 主响应）/ 需要多视角（code review）|
   | 4 | **Orchestrator-workers** | 中心 LLM 动态分解 → 委派 worker | 子任务**不可预测**（coding：改几个文件、每个改什么 depends on 任务）|
   | 5 | **Evaluator-optimizer** | 一个 LLM 生成、另一个 LLM 评估，迭代 | 有明确评估标准（翻译质量 / 检索 relevance）|
   | 6 | **Autonomous agent** | LLM 完全自主决定 control flow + tool use | 不可预测的多步任务（SWE-bench / Voyager 类）|
   
   **对 day-job 启发**：**Mac Game Harness 6 个模式都备齐**——每个模式作为 harness 的"模块"，根据任务类型选。**不要先选框架再选模式**，**要先选模式再看框架是否必要**。

3. **"Foundations: The Augmented LLM" 作为最小构建块**。Anthropic 强调：**所有 agentic systems 的基础是 augmented LLM**——LLM + retrieval（search / RAG）+ tools（function calling）+ memory（conversation / long-term）。**MCP (Model Context Protocol) 作为 augmented LLM 的标准化实现**。**对 day-job 启发**：**Mac Game Harness 的"原子 LLM call"必须 augmented**——任何一次 LLM 调用都应该**有 RAG 检索 + 工具调用 + 短期记忆**这三个 augmentations。**裸 LLM call（即 prompt only）不应该是 harness 里的合法 op**——这是对 harness 架构的硬约束。

4. **"Simple, Composable Patterns > Complex Frameworks" 反共识判断**。这是博客的核心论断：
   > "Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."
   
   **Anthropic 的论据**：
   - 复杂框架（如 LangChain）**隐藏了底层 prompt 和 response**，debug 困难
   - 复杂框架**鼓励过度工程**（"tempting to add complexity when a simpler setup would suffice"）
   - 复杂框架**底层错误假设是常见错误源**（"incorrect assumptions about what's under the hood"）
   - 简单 pattern **几行代码就能实现**
   
   **Anthropic 推荐**：**先用 LLM API 直接写**（direct API calls），**用 framework 前先理解底层**。**对 day-job 启发**：**day-job Mac Game Harness 不要用 LangChain / AutoGPT 类框架**——直接用 **Claude Agent SDK + Anthropic API + MCP** 写 plain Python script，**每个 pattern 是独立的小函数**（`chain()` / `route()` / `parallel()` / `orchestrate()` / `evaluate_optimize()`），**harness 主循环 = dispatcher，根据任务类型选 pattern**。

5. **"When (and when not) to use agents" — 何时不用**。博客明确说**很多应用不需要 agent**：
   > "This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense."
   
   **三层递进**：
   1. **单 LLM call + retrieval + in-context examples** → 够用就停
   2. **Workflow**（5 个模式）→ 任务清晰可分解
   3. **Autonomous agent** → 任务开放、不可预测
   
   **判断标准**：
   - **任务是否能被清晰分解为固定步骤？** → workflow
   - **任务是否需要动态决策？** → agent
   - **延迟和成本敏感？** → 优先单 LLM call
   - **评估标准是否明确？** → 可以加 evaluator-optimizer
   
   **对 day-job 启发**：**day-job Mac Game Harness 决策表**——80% 任务用单 LLM call + RAG 解决（"这个 build 错误是什么？" "怎么写这段 shader？"），15% 任务用 workflow（"完整 UE build + test + report" = orchestrator-workers），5% 任务用 autonomous agent（"在这个陌生 UE 工程里自动 refactor 性能瓶颈"）。**反对"全 agent 化"的过度工程**。

6. **MCP (Model Context Protocol) 作为 augmented LLM 的官方实现路径**。Anthropic 明确把 MCP 列为"an approach" for integrating tools：
   > "One approach is through our recently released Model Context Protocol, which allows developers to integrate with a growing ecosystem of third-party tools with a simple client implementation."
   
   **关键判断**：**MCP 不是另一个框架**——它是**工具集成的协议层**，**比 LangChain 工具集成更标准、更轻量**。**对 day-job 启发**：**Mac Game Harness 的工具集成 = MCP 协议 + 自定义 MCP servers**——MCP 是 augmented LLM 的"工具"这一维度的标准化实现。**配合 Anthropic Computer Use (论文 6) 的"GUI fallback"，MCP-first + GUI-fallback 双轨制**已在 GameDevVault AI Harness 主题确立。

7. **附录 "Agents in Practice" — 2 个真实工业案例**。博客附录给出 2 个验证过效果的应用领域：
   
   - **Customer Support**：典型应用场景是 **Routing + Evaluator-optimizer 组合**：
     - Routing：分类问题（一般 / 退款 / 技术支持）→ 不同下游 prompt + tool
     - Evaluator-optimizer：第一次回复 → LLM-as-judge 打分 → 不够好就重写
     - 优势：**确定性高**（不容易胡说）、**易评估**（回复质量评分可量化）
   
   - **Coding Agents**：典型应用场景是 **Autonomous agent**：
     - LLM 自主决定：读哪些文件 / 改哪些代码 / 跑哪些测试
     - 工具：file edit / shell / test runner / search
     - 优势：**处理开放任务**（没见过的新 codebase 也能 work）
     - 风险：成本高、慢、需要 sandbox 隔离
   
   **对 day-job 启发**：**Mac Game Harness 客户支持模式** = "AI 辅助 UE 调试问答"——用户问问题 → routing 到专门 prompt（"编译错误" / "性能问题" / "shader 错误" / "打包失败"）→ evaluator 检查答案 → 不够好重试。**Coding agent 模式** = "AI 自动在陌生 UE 工程里找 bug"——autonomous agent + sandbox + 工具（UE Editor API / file system / test runner）。

8. **5 个 workflow 模式 + autonomous agent 的工程边界**。博客没有详细 benchmark，但给出了**经验性边界**：
   
   - **Prompt chaining** 适合**输出质量有中间验证点**的任务（写文档 / 翻译）
   - **Routing** 适合**分类准确率高（>95%）**的场景，分类错则全错
   - **Parallelization (sectioning)** 适合**子任务完全独立**（guardrail + 主响应；多 aspect eval）
   - **Parallelization (voting)** 适合**单次 LLM 答案波动大**的任务（code review / 内容审核）
   - **Orchestrator-workers** 适合**任务结构依赖于输入**（coding: 改几个文件 depends on bug）
   - **Evaluator-optimizer** 适合**评估标准可量化**（翻译质量 / 检索 relevance）
   - **Autonomous agent** 适合**任务不可预测、LLM 需要动态决策**（SWE-bench / 开放问题）
   
   **对 day-job 启发**：**Mac Game Harness 模式选型表**——把每个 UE 开发任务映射到 6 个模式之一。**禁止"用 autonomous agent 实现一切"的过度工程**。

---

## 方法概述

### 6 个原语的实现模板（伪代码）

```python
# 0. Augmented LLM (Foundations)
def augmented_llm(prompt: str, *, tools: list = None, memory: list = None, retrieval_query: str = None) -> str:
    """所有 agentic system 的最小调用单元。永远不调用裸 LLM。"""
    context = build_context(
        prompt=prompt,
        tools=tools or [],
        memory=memory or [],
        rag_results=retrieve(retrieval_query) if retrieval_query else None,
    )
    return llm_call(context)  # Claude API + tools

# 1. Prompt Chaining
def chain(steps: list[Callable[[str], str]], input: str, gates: list[Callable[[str], bool]] = None) -> str:
    """串行 LLM call + 编程检查 gate。"""
    result = input
    for i, step in enumerate(steps):
        result = augmented_llm(step(result))
        if gates and not gates[i](result):
            return "FAILED: gate {} returned False".format(i)
    return result

# 2. Routing
def route(input: str, routes: dict[str, Callable[[str], str]]) -> str:
    """分类 → 派发。"""
    category = augmented_llm(classify_prompt(input))
    if category not in routes:
        return "FAILED: unknown category {}".format(category)
    return routes[category](input)

# 3. Parallelization
def parallel_sectioning(input: str, subtasks: list[Callable[[str], str]]) -> list[str]:
    """子任务并行。"""
    return [augmented_llm(subtask(input)) for subtask in subtasks]

def parallel_voting(input: str, task: Callable[[str], str], n: int = 5) -> str:
    """同任务多次跑 + 投票。"""
    outputs = [task(input) for _ in range(n)]
    return vote(outputs)  # majority / LLM-as-judge

# 4. Orchestrator-Workers
def orchestrate(input: str, worker: Callable[[str], str]) -> str:
    """中心 LLM 动态分解 → 委派。"""
    subtasks = augmented_llm(decompose_prompt(input))  # 返回 ["subtask1", "subtask2", ...]
    results = [worker(task) for task in subtasks]
    return synthesize(results)  # 中心 LLM 合并

# 5. Evaluator-Optimizer
def eval_optimize(input: str, generator: Callable, evaluator: Callable, max_iter: int = 3) -> str:
    """生成 + 评估，迭代。"""
    for _ in range(max_iter):
        output = generator(input)
        score = evaluator(output)
        if score > threshold:
            return output
        input = improve_prompt(input, output, feedback_from_evaluator)
    return output

# 6. Autonomous Agent
def autonomous_agent(goal: str, tools: list, max_steps: int = 50) -> str:
    """LLM 自主决定 control flow + tool use。"""
    memory = []
    for step in range(max_steps):
        screenshot = tools['observe']()  # 感知环境
        action = augmented_llm(plan_prompt(goal, memory, screenshot, tools))  # 推理
        if action == "DONE":
            return memory[-1].result
        result = tools[action['tool']](*action['args'])
        memory.append({'step': step, 'observation': screenshot, 'action': action, 'result': result})
    return "FAILED: max_steps exceeded"
```

### Claude Agent SDK 配套

Anthropic 提供 **Claude Agent SDK** 作为官方实现，封装了：
- LLM call (Anthropic API)
- Tool definition + calling
- Memory (conversation / long-term)
- MCP client
- Sandbox (用于 autonomous agent)

**对 day-job 启发**：**Mac Game Harness 的 v0 = Claude Agent SDK + 自定义 MCP servers + 6 个原语的 Python 实现**。不直接用 LangChain / AutoGen。

---

## 关键实验 / 案例

### 附录 1 的 2 个工业案例

| 领域 | 模式组合 | 关键优势 | 关键风险 |
|------|----------|----------|----------|
| **Customer Support** | Routing + Evaluator-optimizer | 确定性高 / 评估可量化 / 不容易胡说 | Routing 分类错则全错；LLM-as-judge 自身有偏 |
| **Coding Agents** | Autonomous agent (Claude Code) | 处理开放任务 / 见过没见过都能 work | 成本高 / 慢 / 必须 sandbox 隔离 / 容易跑飞 |

**Anthropic 自己用 Claude Code**（基于 Claude Agent SDK 的 autonomous coding agent）作为**附录 2 之外的真实生产案例**（博客发布时 Claude Code 还在 preview，2025 年初 GA）。

### 配合 GameDevVault AI Harness 主题的 6 篇 GDC + 1 arxiv 对位

| GameDevVault 论文 | 在 Building Effective Agents 框架中的对位 |
|------------------|------------------------------------------|
| GDC 2026 Microsoft VS 2026 + Copilot Agent Mode | **Augmented LLM** + **Orchestrator-workers** + MCP |
| GDC 2026 DeepMind SIMA 2 | **Autonomous agent**（理解未见过的环境，self-improvement loop）|
| arxiv 2024 Anthropic Computer Use | **Autonomous agent**（GUI-tool 版）的特殊化 |
| GDC 2026 Tencent 天美 (98% 自动化) | **Orchestrator-workers**（中心 LLM 委派 8 个 agent）|
| GDC 2026 Glass Bead (4 人 + 8 agents) | **Orchestrator-workers** + **Evaluator-optimizer** |
| GDC 2026 Bitmagic (AI-Native 引擎) | **Autonomous agent**（"prompt-玩-迭代" 闭环 UX）|
| GDC 2026 Google DeepMind Genie 3 (playable worlds) | 不直接对位（world model 是另一议题）|

**关键判断**：**Building Effective Agents 的 6 原语**可作为对 **GameDevVault 7 篇 AI Harness papers** 的**统一分类法**。每篇 paper 都可映射到 1-2 个原语，形成"工业案例 → 6 原语"的 cross-ref 表。

---

## 局限性与思考

1. **"6 个原语"不是穷举**。Anthropic 自己说"this is not a definitive list"，**实践中可能混用、嵌套**（如 orchestrator-workers + evaluator-optimizer）。**对 day-job 启发**：**6 原语是选型起点**，**不是约束**。新模式如果浮现（如 hierarchical agent、recursive agent）应该加进去。

2. **"Simple > Complex" 是反共识，但有反例**。博客的简单优先论断**对小团队 / 早期产品正确**，**对大规模生产可能过于简化**。**对 day-job 启发**：**day-job Mac Game Harness 早期用 simple pattern**，**当 6 原语都覆盖不完时**再考虑加框架。**不预设"必须用 LangChain"**。

3. **没有 benchmark / 量化对比**。博客是**经验性最佳实践**，**没有 SWE-bench / HumanEval 类的硬数据**支持。**6 原语的相对优劣没有 paper-grade 证据**。**对 day-job 启发**：**实际效果由 harness 工程团队自己跑 benchmark 决定**——不应该无脑相信 "prompt chaining 最简单所以最好"。

4. **Anthropic 商业 bias**。博客是 Anthropic 官方出品，**推荐 Anthropic 自家 SDK / API**。**对 day-job 启发**：**6 原语是 vendor-neutral**（任何 LLM 都能用），**但 SDK 推荐 Claude Agent SDK**——可作为**默认实现**，但要保留**切换 OpenAI / 开源 LLM 的能力**。

5. **MCP 锁定风险**。MCP 虽然是 Anthropic 主导的开源协议，但**生态绑定 Claude**。**对 day-job 启发**：**Mac Game Harness 工具层用 MCP-first**，**但要保留 direct tool calling 兜底**（万一 MCP server 不可用）。

6. **"Autonomous agent" 模式的成本/延迟爆炸**。博客承认 agentic systems 换的是"latency and cost for better task performance"。**对 day-job 启发**：**day-job Mac Game Harness 的 autonomous agent 模式必须有 token budget cap + timeout + human-in-loop 兜底**——不能无限循环。

---

## 相关论文

### GameDevVault (AI Harness 主题 6 篇 + 本篇 = 7)

- [[GameDevVault/GDC/2026-Tencent-Timi-AgenticAI-GameDev-98pct]] — Tencent 天美 98% 自动化（Orchestrator-workers）
- [[GameDevVault/GDC/2026-Bitmagic-AINativeGameEngine]] — Bitmagic AI-Native 引擎（Autonomous agent）
- [[GameDevVault/GDC/2026-GlassBeadGames-MultiAgentGameStudio]] — Glass Bead 4 人 + 8 agents（Orchestrator-workers + Evaluator-optimizer）
- [[GameDevVault/GDC/2026-Microsoft-VS2026-Copilot-GameDev]] — Microsoft VS 2026 + Copilot Agent Mode + MCP（Augmented LLM + Orchestrator-workers）
- [[GameDevVault/GDC/2026-GoogleDeepMind-SIMA2-GenericGameAgent]] — DeepMind SIMA 2（Autonomous agent）
- [[GameDevVault/arxiv/2024-Anthropic-ComputerUse-OSAgent]] — Anthropic Computer Use（Autonomous agent 特殊化：GUI-tool 版）

### AIResearchVault (本库)

- [[01e-agent-harness-latest]] — Agent Harness 综述（覆盖 Context Engineering / ACE / MAST / AFlow / Confucius / GCC / RepoST 7 篇）—— **本篇作为第 8 篇补完"工业界 6 原语"维度**
- [[01d-tool_calling-latest]] — Tool Calling 综述（MCP / Function Calling 底层）
- [[01d-memory-latest]] — Memory 系统综述（Augmented LLM 的 memory 维度）
- [[01d-sandbox-latest]] — Sandbox 综述（Autonomous agent 必备）
- [[01e-agent-verification-eval-latest]] — Agent Verification/Eval（6 原语的效果评估协议）

### 学术 cross-ref

- **AFlow** (arXiv:2410.10762) — 论文 4 in 01e-agent-harness，**workflow = 代码图** 的形式化正好对应 Anthropic 5 个 workflow 模式
- **MAST / Why Do Multi-Agent LLM Systems Fail** (arXiv:2507.18320) — 论文 3 in 01e-agent-harness，**多 agent 失败归因** 对应 Anthropic "Workflow > Agent 默认" 主张的反向证据
- **MemGPT / Letta** — Augmented LLM 的 memory 维度的工业实现

---

## 面试谈资

### 30 秒（"你熟悉 Anthropic 的 agent 框架吗？"）

> "Anthropic 2024-12 发了 Building effective agents，把 agentic systems 切成 **workflows** 和 **autonomous agents** 两类，5 个 workflow pattern（**prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer**）加 1 个 autonomous agent pattern。核心论断是**'simple, composable patterns > complex frameworks'**——找最简单方案，**只增加必要复杂度**。MCP 作为 augmented LLM 的工具集成协议层。**实践上 95% 任务应该用 workflow 而不是 autonomous agent**。"

### 2 分钟（"你怎么用这个框架做 harness？"）

> "我用 Building Effective Agents 的 **6 原语**作为 harness 的**模式选型表**：
> 1. **Augmented LLM**（retrieval + tools + memory）—— harness 任何 LLM call 都不能裸调
> 2. **Prompt chaining**——任务可分解为固定步骤（如 build → test → report），可加 gate
> 3. **Routing**——任务有明显分类（编译错误 / 性能 / shader / 打包），分类 → 专门 prompt
> 4. **Parallelization**——子任务独立（guardrail + 主响应），或多视角（code review 投票）
> 5. **Orchestrator-workers**——任务结构 depends on 输入（UE coding：改几个文件 depends on bug）
> 6. **Evaluator-optimizer**——评估标准可量化（翻译 / retrieval relevance）
> 7. **Autonomous agent**——任务开放不可预测（陌生 UE 工程 refactor / 探索性 bug hunt）
>
> **关键设计原则**：
> - **不要先选框架**（LangChain / AutoGen）**再选模式**——要先选模式再看框架是否必要
> - **80% 任务用 augmented LLM + 简单 workflow**，**15% 用复杂 workflow**，**5% 用 autonomous agent**
> - **autonomous agent 模式必须有 budget cap + timeout + human-in-loop + sandbox**——不能无限循环
> - **MCP 作为工具集成标准**，**保留 direct tool calling 兜底**（vendor-neutral 兜底）
>
> **和现有 GDC 工业案例的对位**：
> - Microsoft Copilot Agent Mode = Augmented LLM + Orchestrator-workers
> - SIMA 2 = Autonomous agent + self-improvement loop
> - Tencent 天美 98% 自动化 = Orchestrator-workers（中心 LLM 委派 8 agent）
> - Computer Use = Autonomous agent 特殊化（GUI-tool 版）
>
> 6 原语是 vendor-neutral 的**模式选型法**，不绑死任何框架或 LLM。"

---

## Changelog

- **2026-07-27 (v1.0)**: 初版 paper note。覆盖 Anthropic Building Effective Agents 工程博客全文（2024-12-19），提炼 6 原语（5 workflow + 1 agent）+ 8 个核心创新点 + 2 工业案例 + 6 局限 + GameDevVault 6 篇 AI Harness 对位。
