# 01-论文阅读与研究库

> **用途**：存放 AI 论文精读笔记、前沿追踪、文献综述
> **输入**：Arxiv、会议论文、博客、演讲
> **输出**：结构化笔记、知识图谱、面试素材

---

## 笔记格式

```markdown
---
tags: [paper, <topic>]
aliases: [<paper-short-name>]
created: YYYY-MM-DD
---

# 论文标题

- **作者**：...
- **来源**：Arxiv / NeurIPS / ICML / ICLR / CVPR / ...
- **链接**：...
- **主题**：[[LLM]] / [[RL]] / ...

## 核心贡献

1. ...
2. ...

## 方法概述

## 关键实验

## 局限性与思考

## 相关论文
- [[...]]

## 面试谈资
- 30秒：...
- 2分钟：...
```

---

## 分类索引

| 主题 | 论文数 | 最近更新 |
|------|--------|----------|
| Game-AI | 1 | 2026-07-02 |
| Agent Harness | 1 | 2026-06-29 |
| Sandbox | 6 | 2026-07-15 |
| Tool Calling | 6 | 2026-07-15 |
| Memory | 8 | 2026-07-15 |
| LLM | 0 | - |
| RL | 0 | - |
| Multi-Modal | 0 | - |
| AIGC | 0 | - |
| AI-Theory | 0 | - |
| AI-Training | 0 | - |
| AI-Optimization | 0 | - |
| AI-Math | 0 | - |
| NeRF | 0 | - |
| time-series | 0 | - |

---

## 阅读 Pipeline

1. **预读**（周一）：AI 生成 150 字摘要 + 3 个引导问题
2. **精读**（周一晚）：你阅读，标记难点
3. **讨论**（周二）：AI 解释难点，你验证理解
4. **笔记**（周二晚）：整理到本库
5. **复习**（周五）：AI 生成测验，你回答

---

## Game AI 研究库（2026-07-02 新建）

覆盖 **LLM/Agent in Games**、**Native AI Games**、**Human-AI-Game Interaction** 三大方向。

| 文件 | 内容 | 方向 |
|------|------|------|
| [[01-Game-AI-研究库总览]] | 全景文献地图、概念速查、面试谈资 | 总览 |
| [[01a-LLM-Agent-in-Games]] | Voyager, MineDojo, OSWorld, Harness 执行层 | 执行层 |
| [[01b-Native-AI-Games]] | Genie, Infinigen, AI Dungeon, 世界模型设计 | 设计层 |
| [[01c-Human-AI-Game-Interaction]] | Cicero, Generative Agents, Companion AI, 人机交互 | 交互层 |

---

## Agent 基础设施研究库（2026-07-15 新建）

覆盖 **Harness 系统**、**Memory 记忆**、**Tool Calling 工具调用**、**Sandbox 沙箱安全** 四大基础设施方向。

| 文件 | 内容 | 方向 |
|------|------|------|
| [[01d-memory-latest]] | Mem0, Zep/Graphiti, A-MEM, Memory-R1, HiMem, MemP, LEGOMem, MemAgent | 记忆系统 |
| [[01d-tool_calling-latest]] | When2Tool, Atomix, PASTE/SPORK, ReTool, ToolACE-R, Tool Use Survey | 工具调用 |
| [[01d-sandbox-latest]] | LLM-in-Sandbox, Crab, SafeArena, ceLLMate, EnvSimBench, Agent-World | 沙箱安全 |

---
