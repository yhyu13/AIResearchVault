---
tags: [routine/AI-tasks, topic/LLM, day/Monday]
aliases: []
---

# Monday：AI 任务清单 — LLM 前沿技术输入

> **人类目标**：精读论文 + 追踪前沿进展
> **AI 任务**：提供脚手架、解释障碍、生成问题，绝不替代核心工作。

---

## 任务 1：论文预读引导（AI 执行：150字摘要 + 3个引导问题 + 重点章节标记）

**论文**：*Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (Wei et al., NeurIPS 2022)

**AI 输出**：

> **150字摘要**：本文提出链式思考（Chain-of-Thought, CoT）提示方法，通过在示例中加入中间推理步骤，显著提升了大语言模型在算术、常识和符号推理任务上的表现。实验表明，CoT 对参数规模超过 ~100B 的模型效果尤为显著，且结合传统投票集成（self-consistency）可进一步提升准确率。这一发现揭示了 LLM 的 emergent reasoning 能力可以通过提示工程被激活。

> **3 个引导问题**：
> - Q1: CoT 为什么只对足够大的模型（~100B+）有效？小模型为什么不能从中间步骤中受益？
> - Q2: CoT 的"中间推理步骤"本质上是在做什么？是改变了模型的计算路径，还是仅仅改变了输出分布的采样？
> - Q3: CoT 与 few-shot prompting 的核心区别是什么？如果 few-shot 示例本身已经包含推理过程，CoT 是否还有额外收益？

> **重点章节标记**：
> 1. **先读 Section 2 (Method)**：CoT 的两种变体（Few-shot-CoT vs Zero-shot-CoT）
> 2. **再读 Section 3 (Experiments)**：GSM8K 数学推理结果表（Figure 3）
> 3. **最后读 Section 4 (Discussion)**：为什么 CoT 只在大型模型上有效（emergent abilities 讨论）
> 4. **附录 B**：全部 prompt 模板，可复现实验

**你必须做**：
- 通读论文全文，标记你的批注
- 在 Obsidian 中创建 [[Chain-of-Thought-Wei-2022]] 笔记
- 回答上面 3 个问题，写在笔记中

---

## 任务 2：核心概念解释（AI 执行：概念拆解 + 直觉解释，你验证）

**概念**：Chain-of-Thought (CoT) 提示

**AI 输出**：

> **直觉解释**：CoT 就像你让朋友解数学题时，不只要最终答案，而是要求他把"怎么想的说出来"。LLM 在生成中间推理步骤时，被迫分步思考，减少了从问题直接跳到答案时的"跳步错误"。

> **数学直觉**：设问题为 $x$，答案为 $y$。传统 prompting 直接建模 $P(y|x)$；CoT 引入中间步骤 $z_1, z_2, ... z_n$，建模 $P(y|x) = \sum_z P(y|z_n)P(z_n|z_{n-1})...P(z_1|x)$。分解降低了每步的难度，但累积了误差。

> **为什么只对大模型有效**：小模型的表示能力不足以同时维持"当前步骤的语义"和"下一步的逻辑关系"。大模型有足够的 capacity 来 internalize 多步推理的语义结构。

> **与相关概念的区别**：
> - **vs Few-shot**：CoT 是 few-shot 的一种特例，但强调推理步骤必须显式写出来
> - **vs Scratchpad**：Scratchpad 是训练时的方法，CoT 是推理时的提示方法
> - **vs Self-Consistency**：Self-Consistency 是 CoT 的增强技术，多次采样后投票

**你必须做**：
- 用你自己的话重新解释 CoT（写在笔记中）
- 在 [[02-算法复现与源码库]] 中尝试手写一个简单的 CoT 示例

---

## 任务 3：面试谈资生成（AI 执行：30秒/2分钟版本 + 追问）

**AI 输出**：

> **30秒版本**：Chain-of-Thought 是 2022 年 Google 提出的提示方法，核心是在 few-shot 示例中加入中间推理步骤。它在 PaLM 540B 上把 GSM8K 数学推理从 17% 提升到 56%，揭示了 LLM 的 emergent reasoning 能力可以通过显式分解被激活。后续 work 如 self-consistency、Tree of Thoughts 都是在此基础上发展的。

> **2分钟版本**：
> 背景：传统 few-shot prompting 在复杂推理任务上表现差，因为模型被迫从问题直接跳到答案。
> 方法：CoT 在示例中加入"思考过程"，如"问：小明天天吃 3 个苹果，5 天吃多少？答：每天吃 3 个，5 天就是 3 × 5 = 15 个。答案是 15。"
> 关键发现：效果随模型规模急剧提升，在 ~100B 参数处出现相变（emergent ability）。
> 后续：Self-consistency（多次采样投票）、Least-to-Most prompting（先分解再求解）、Auto-CoT（自动构造示例）。

> **3 个追问**：
> 1. "CoT 效果与模型规模的关系是线性的还是相变的？你在什么规模上观察到？"
> 2. "Zero-shot-CoT 的 'Let's think step by step' 为什么有效？它改变了模型的什么？"
> 3. "CoT 对中文推理任务是否同样有效？多语言场景下的 CoT 有什么挑战？"

**你必须做**：
- 对着镜子或录音 rehearse 30秒和2分钟版本
- 准备你自己的追问回答

---

## 任务 4：文献地图绘制（AI 执行：关键论文 + 引用链 + 演进脉络）

**AI 输出**：

```
CoT 文献演进链

├── 前身/基础
│   ├── GPT-3 (Brown et al., 2020) — Few-shot prompting 范式
│   ├── Scratchpad (Nye et al., 2021) — 训练时显式推理
│   └── Compositional Generalization (_KEYSAR_ 2017) — 分步推理的心理学基础
│
├── 核心论文
│   └── Chain-of-Thought Prompting (Wei et al., 2022) ← 你正在读
│       ├── 前身：LAMBADA (Paperno et al., 2016) — 长程推理评估
│       └── 并行：Least-to-Most (Drozdov et al., 2022)
│
├── 直接扩展
│   ├── Self-Consistency (Wang et al., 2022) — 多次采样投票
│   ├── Zero-shot-CoT (Kojima et al., 2022) — "Let's think step by step"
│   ├── Auto-CoT (Zhang et al., 2022) — 自动构造示例
│   ├── Complexity-based CoT (Fu et al., 2022) — 用更复杂示例提升效果
│   └── Tree of Thoughts (Yao et al., 2023) — 从链到树，搜索推理路径
│
├── 2023+ 后续
│   ├── Graph of Thoughts (Besta et al., 2023)
│   ├── Program-of-Thought (Chen et al., 2022)
│   ├── ReAct (Yao et al., 2022) — CoT + 工具使用
│   └── Chain-of-Verification (Dhuliawala et al., 2023)
│
└── 当前热点
    ├── Multi-step reasoning agents (2024)
    └── Test-time compute scaling (OpenAI o1, 2024) — CoT 的终极扩展
```

> **关键演进脉络**：Few-shot → CoT → Self-Consistency → Tree of Thoughts → Test-time compute scaling。核心趋势是：从单次推理到多路径搜索，从固定提示到自适应推理。

**你必须做**：
- 在 Obsidian 中创建文献地图页面
- 至少找到并下载 2 篇扩展论文的 PDF
- 验证引用链的准确性（Google Scholar 检查）

---

## 今日 AI 禁区

- ❌ 让 AI 替读论文
- ❌ 让 AI 替写笔记
- ❌ 让 AI 生成代码路径不验证
- ❌ 让 AI 替准备面试回答

---

## 完成检查清单

- [ ] 论文预读引导 已完成（AI 已生成）
- [ ] 核心概念解释 已完成（AI 已生成）
- [ ] 面试谈资生成 已完成（AI 已生成）
- [ ] 文献地图绘制 已完成（AI 已生成）
- [ ] 所有内容已写入 Obsidian 笔记（**人类必须执行**）

---

*AI 执行时间：约 15 分钟*
*人类执行时间：约 2-3 小时*
