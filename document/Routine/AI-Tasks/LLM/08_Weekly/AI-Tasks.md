---
tags: [routine/AI-tasks, topic/LLM, day/Weekly]
aliases: []
---

# Weekly：AI 任务清单 — LLM 外部接触

> **人类目标**：技术社交 + 开源贡献
> **AI 任务**：提供脚手架、解释障碍、生成问题，绝不替代核心工作。

---

## 任务 1：技术问题润色（AI 执行：知乎/Reddit/Discord 多版本）

**AI 输出**：

> **你的 raw 问题**："cot 的 self-consistency 是怎么工作的？为什么投票就能提升准确率？"
> 
> **知乎版**（详细、结构化）：
> > **标题**：Chain-of-Thought 的 Self-Consistency：为什么"多次采样投票"能提升推理准确率？
> > 
> > 正文：
> > 最近在读 Wei et al. 2022 的 CoT 论文，对 Self-Consistency（Wang et al., 2022）有些困惑。
> > 
> > 已知 CoT 通过分步推理提升准确率，但 Self-Consistency 在此基础上进一步对同一问题采样多次（如 temperature=0.7，生成 10 条推理链），然后取答案的多数投票。
> > 
> > 我的问题是：
> > 1. 为什么投票能提升准确率？直觉上，如果模型本身有偏见，多次采样会不会只是重复同样的错误？
> > 2. 采样次数（如 10 次 vs 40 次）和准确率提升的关系是怎样的？有 diminishing returns 吗？
> > 3. 在实际部署中，Self-Consistency 的延迟和成本如何权衡？
> > 
> > 期待大佬们的解答！
> 
> **Reddit r/MachineLearning 版**（简洁、直接）：
> > Why does self-consistency improve CoT performance? Intuitively, if the model has a systematic bias, wouldn't multiple samples just repeat the same mistake? Any papers analyzing the sample-accuracy trade-off?
> 
> **Discord / 群聊版**（ casual ）：
> > 问个 CoT 的问题：self-consistency 就是同一个问题让模型答好几次然后投票，这为啥有效？如果模型本身就爱犯某个错，投票不也是重复犯错吗？有没有分析采样次数和效果关系的 paper？
> 
> **Twitter/X 版**（极简）：
> > Q: Why does self-consistency work for CoT? If the model is biased, more samples = more bias, right? What's the theoretical justification? @karpathy @ylecun
> 
> **AI 建议**：
> - 知乎版适合深度讨论，预期获得详细回答
> - Reddit 适合快速获取 paper 链接
> - Discord 适合 casual 交流，降低社交压力
> - Twitter 适合向大 V 提问，但可能无回应
> 
> **推荐**：先发知乎，积累回答后整理成博客素材。

**你必须做**：
> - 选择一个平台，粘贴对应版本
> - 根据你的语气微调措辞（不要完全照搬）
> - 自己发帖，不要代发

---

## 任务 2：冷消息起草（AI 执行：礼貌模板 + 个性化建议）

**AI 输出**：
> 
> **场景 A：向论文作者请教**
> 
> **模板**：
> > 尊敬的 X 老师，您好！
> > 
> > 我是 [你的身份/学校/公司]，最近在深入学习您的论文 "Chain-of-Thought Prompting..."（NeurIPS 2022）。在复现过程中，我对 Self-Consistency 的采样策略有个具体的问题：
> > 
> > [你的具体问题，1-2 句话]
> > 
> > 冒昧打扰，期待您的指点。无论是否有时间回复，都非常感谢您的杰出工作对我的启发！
> > 
> > [你的名字]
> > [LinkedIn / GitHub / 个人主页]
> 
> **个性化建议**：
> - 先关注作者 Twitter/GitHub，互动 1-2 次后再私信
> - 问题要具体（不要问"能讲讲 CoT 吗"）
> - 提及你读了论文并尝试了复现（显示诚意）
> - 不要期待回复，但做好回复的准备
> 
> **场景 B：向社区大佬请教**
> 
> **模板**：
> > 大佬好！最近在学习 CoT 相关的技术，看到您在 [GitHub 项目 / 知乎回答 / 博客] 中分享了很多宝贵经验。
> > 
> > 我在尝试用 Llama 3 复现 GSM8K 上的 CoT 效果时遇到了 [具体问题]，想请教您：
> > 
> > [问题描述，1-2 句话]
> > 
> > 如果方便的话，期待您的建议。无论如何，感谢您的分享！
> 
> **场景 C：寻求合作/指导**
> 
> **模板**：
> > [对方名字] 您好，
> > 
> > 我是 [你的名字]，目前在 [学校/公司] 从事 [方向] 的研究。关注到您在 [具体项目/论文] 中的工作，非常受启发。
> > 
> > 我最近在 [相关方向] 做一个小项目，希望能有机会向您请教或探讨合作可能。如果您有 15 分钟时间，我非常期待能有一次简短的交流。
> > 
> > 附件是我的项目简介 [或 GitHub 链接]。
> > 
> > 感谢您的时间，期待回复！

**你必须做**：
> - 选择 1 个场景，填入你的具体信息
> - 发送前再读一遍，确保语气自然
> - 不要同时给太多人发，一次 1-2 个
> - 记录回复到 [[06-研究复盘日志]]

---

## 任务 3：开源贡献匹配（AI 执行：技能 → 项目匹配 + Issue 推荐）

**AI 输出**：
> 
> **你的技能画像**（基于本周学习）：
> - Chain-of-Thought prompting 理解与实现
> - Python 工具开发（prompt management）
> - Streamlit 快速 Demo 搭建
> - GSM8K 等推理基准测试经验
> 
> **匹配项目**：
> 
> | 项目 | 相关技能 | 适合贡献 | 难度 | 链接 |
> |------|----------|----------|------|------|
> | lm-evaluation-harness | 基准测试 | 添加 CoT 评估配置 | 低 | EleutherAI |
> | langchain | 工具链 | CoT prompt template | 中 | LangChain |
> | guidance | 结构化生成 | CoT 结构化输出 | 中 | Microsoft |
> | text-generation-webui | 推理 UI | CoT 可视化展示 | 低 | oobabooga |
> | transformers | 模型推理 | CoT 示例 notebook | 低 | Hugging Face |
> 
> **推荐 Issue 搜索关键词**：
> - "chain-of-thought" / "CoT"
> - "reasoning"
> - "GSM8K"
> - "few-shot prompt"
> - "self-consistency"
> 
> **贡献路径**：
> 1. **最容易**：给项目提文档改进（typo、 clarification、中文翻译）
> 2. **入门**：给项目添加 CoT 的 example notebook / cookbook
> 3. **进阶**：实现一个新功能（如 Auto-CoT 示例选择）并提 PR
> 4. **高阶**：发现并修复与 CoT 相关的 bug
> 
> **本周具体行动**：
> - [ ] 在 Hugging Face transformers 中找一个 CoT 相关的 notebook，运行并报告问题
> - [ ] 给 lm-evaluation-harness 的 GSM8K 评估添加 CoT 配置（参考论文 prompt）
> - [ ] 给 langchain 的 prompt hub 提交一个 CoT math prompt 模板
> 
> **贡献记录模板**：
> ```markdown
> ## 开源贡献记录
> - 日期：YYYY-MM-DD
> - 项目：
> - 类型：Issue / PR / Comment / 文档
> - 链接：
> - 收获：
> ```

**你必须做**：
> - 选择 1 个项目，找到 1 个可做的贡献（从最简单的开始）
> - 阅读项目的 CONTRIBUTING.md
> - 执行贡献，记录到 [[06-研究复盘日志]]
> - 如果找不到合适的，先 star 项目并关注动态

---

## 今日 AI 禁区

- ❌ 让 AI 替读论文
- ❌ 让 AI 替写笔记
- ❌ 让 AI 生成代码路径不验证
- ❌ 让 AI 替准备面试回答

---

## 完成检查清单

- [ ] 至少发了 1 个技术问题（**人类必须执行**）
> - [ ] 至少与 1 位行业人士交流（**人类必须执行**）
> - [ ] 至少给 1 个开源项目提了 Issue/PR（**人类必须执行**）
> - [ ] 交流收获已整理到 Obsidian（**人类必须执行**）
> 
> ---
> 
> *AI 执行时间：约 15 分钟*
> *人类执行时间：约 2-3 小时*
> 