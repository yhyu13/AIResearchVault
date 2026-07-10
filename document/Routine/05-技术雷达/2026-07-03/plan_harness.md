# Agent Harness 架构演变研究 — 执行计划

## 目标
基于 awesome-agent-harness 仓库，研究 LLM Agent Harness 的架构演变历程，产出一份含历史脉络、关键特性、未来预测的深度报告。

## 输入素材
- `README.md` (695 行): curated reading list，含 5 大章节
- `Agent_Systems_with_Harness_Engineering.pdf` (2.2MB): 原始论文
- `figures/`: 论文中的架构图

## 仓库结构
```
1. Evolution of Harness Engineering          ← 架构演变（核心）
2. The Design of the Harness                   ← Harness 设计
   2.1 Agent Workflow (感知/规划/执行)
   2.2 Memory Systems (短期/长期)
   2.3 Skill Libraries (获取/管理/维护)
   2.4 Multi-agent Orchestration (协调/通信)
3. Model Adaptation for Harness                ← 模型适配
   3.1 Context Engineering (设计/管理)
   3.2 Agentic Training (环境/奖励/训练/基础设施)
4. Representative Benchmarks by Task Domain    ← 基准测试
5. Future Directions                             ← 未来方向
```

## 阶段 1：并行研究（Research Swarm）
启动 4 个 explore 子代理，分别研究不同维度：

1. **Harness 架构演变史**（研究员_A）
   - 从仓库 Section 1 "Evolution of Harness Engineering" 出发
   - 追踪三层演变：Action Interface → Workflow Infrastructure → User-Centric Persistence
   - 关键论文：ReAct (ICLR 2023), Toolformer (NeurIPS 2023), SWE-agent (NeurIPS 2024), AIOS (COLM 2025), OpenClaw (Blog 2026)
   - 产出：时间线 + 关键转折点 + 技术根因分析

2. **Harness 核心设计组件**（研究员_B）
   - 从仓库 Section 2 "The Design of the Harness" 出发
   - 研究四个子系统：Agent Workflow (感知→规划→执行闭环)、Memory Systems (Working/Conversational/Structured/Unstructured)、Skill Libraries (获取→表示→检索→维护)、Multi-agent Orchestration (Centralized/Decentralized + Debate/Collaboration)
   - 关键论文：MemGPT, Voyager, AutoGen, MetaGPT, ChatDev
   - 产出：各组件的架构演变 + 设计权衡 + 与 ReSTIR/GI 的潜在关联

3. **Agentic Training 与模型适配**（研究员_C）
   - 从仓库 Section 3 "Model Adaptation for Harness" 出发
   - 研究：Context Engineering (Prompt/Retrieval/Processing/Updating)、Agentic Training (环境构造/奖励设计/训练算法/基础设施)
   - 关键论文：Chain-of-Thought, DSPy, DeepSeek-R1, PPO/DPO/RLHF 系列
   - 产出：训练范式的演变 + 从 SFT 到 RL 的 transition + 基础设施演进

4. **Benchmark 生态与未来预测**（研究员_D）
   - 从仓库 Section 4 & 5 出发
   - 研究：Deep Research / Software Engineering / Tool Use / Web Agent / 科学发现等 benchmark 的演进
   - 结合 Section 5 "Future Directions" 做预测
   - 关键：SWE-bench, AgentBench, GAIA, BrowseComp
   - 产出：benchmark 设计哲学演变 + 未来方向预测（2026-2028）

## 阶段 2：整合与报告写作
- 汇总 4 份研究报告
- 撰写最终报告：`history_LLM_Agent_Harness_架构演变.md`
- 结构：
  1. 导论：什么是 Harness Engineering
  2. 时间线（2018→2026）关键里程碑
  3. 架构演变的三层模型（Action Interface → Workflow → Persistence）
  4. 核心组件深度分析（Workflow / Memory / Skills / Multi-agent）
  5. 训练范式演变（SFT → RL → Agentic RL）
  6. Benchmark 生态与评估哲学
  7. 未来预测（2026-2028）
  8. 对实时图形学从业者的关联分析
  9. 参考文献

## 质量约束
- 所有关键论文必须标注作者、会议、年份
- 架构演变必须有明确的时间线逻辑，避免只列现状
- 预测部分必须有技术根因支撑，不能是模糊猜测
- 与 ReSTIR/GI 的关联：agent harness 中的 planning/execution loop 与渲染管线的相似性、memory system 与 GI cache 的对比

## 输出
- `C:/Git-repo-my/AIResearchVault/document/Routine/05-技术雷达/2026-07-03/history_LLM_Agent_Harness_架构演变.md`
- 预计字数：≥ 5,000 字
