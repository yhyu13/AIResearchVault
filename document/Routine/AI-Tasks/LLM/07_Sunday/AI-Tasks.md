---
tags: [routine/AI-tasks, topic/LLM, day/Sunday]
aliases: []
---

# Sunday：AI 任务清单 — LLM 项目收尾

> **人类目标**：集成测试 + 复盘
> **AI 任务**：提供脚手架、解释障碍、生成问题，绝不替代核心工作。

---

## 任务 1：集成测试（AI 执行：测试计划 + 用例生成 + 覆盖率分析）

**AI 输出**：

> **测试范围**：本周全部产出（代码 + Demo + 博客）
> 
> **测试计划**：
> 1. **单元测试**：CoT Prompt Manager 的每个函数
> 2. **集成测试**：端到端流程（输入 → prompt → API → 解析 → 展示）
> 3. **回归测试**：确认本周修复没有破坏原有功能
> 4. **性能测试**：延迟、token 消耗、并发
> 5. **兼容性测试**：不同模型（GPT-3.5 vs GPT-4 vs Llama）
> 
> **测试用例生成**：
> 
> **单元测试**（`pytest`）：
> ```python
> def test_build_prompt_includes_examples():
>     manager = CoTPromptManager(examples=[...])
>     prompt = manager.build_prompt("1+1=？", k=2)
>     assert len(prompt.split("Q:")) == 4  # 2 examples + 1 question + header
> 
> def test_select_examples_returns_k_items():
>     manager = CoTPromptManager(examples=[...])
>     selected = manager.select_examples("test", k=3)
>     assert len(selected) == 3
> 
> def test_parse_response_extracts_answer():
>     text = "Reasoning... The answer is 42."
>     reasoning, answer = parse_cot_response(text)
>     assert answer == "42"
> ```
> 
> **集成测试**（手动）：
> | 用例 | 输入 | 预期输出 | 状态 |
> |------|------|----------|------|
> | 简单算术 | "2+3=？" | 推理步骤 → 5 | 待测试 |
> | 多步问题 | "农场问题..." | 多步推理 → 正确答案 | 待测试 |
> | 边界问题 | "0/5=？" | 正确识别 0 | 待测试 |
> | Demo 全流程 | 点击 Streamlit 按钮 | 显示推理动画 | 待测试 |
> | 博客链接 | 点击 GitHub 链接 | 可访问 | 待测试 |
> 
> **覆盖率目标**：
> - 代码覆盖率：> 60%（核心函数全覆盖）
> - 功能覆盖率：100%（所有功能至少手动测一次）
> - 场景覆盖率：至少 3 类场景（简单、复杂、边界）
> 
> **测试报告模板**：
> ```markdown
> ## 集成测试报告
> - 日期：YYYY-MM-DD
> - 测试人：
> - 范围：CoT 工具 + Demo + 博客
> - 通过率：X/Y
> - 阻塞问题：
> - 建议：
> ```

**你必须做**：
> - 运行全部测试用例
> - 修复失败用例
> - 填写测试报告
> - 保存到 [[03-实验案例与代码集]]

---

## 任务 2：文档补全（AI 执行：API 文档 + 使用示例 + 常见问题）

**AI 输出**：
> 
> **README 补全建议**：
> 
> ```markdown
> # CoT Math Solver
> 
> ## 快速开始
> ```bash
> pip install -r requirements.txt
> export OPENAI_API_KEY=your_key
> python streamlit_app.py
> ```
> 
> ## 功能
> - 使用 Chain-of-Thought 提示解决数学问题
> - 可视化推理过程
> - 对比直接生成 vs CoT 生成
> 
> ## 项目结构
> ```
> ├── cot_prompt_manager.py   # 核心工具
> ├── streamlit_app.py         # 网页 Demo
> ├── tests/                   # 测试
> └── data/                    # 示例数据
> ```
> 
> ## 常见问题
> **Q: 为什么我的准确率比论文低？**
> A: 模型规模差异。论文用 PaLM 540B，你可能用 GPT-3.5 或 Llama 3 8B。换更大的模型或优化 prompt。
> 
> **Q: API 费用太高怎么办？**
> A: 使用本地模型（Llama 3 via Ollama）或更便宜的 API（如 Together AI、Groq）。
> 
> **Q: 支持中文吗？**
> A: 代码支持，但 few-shot 示例需要换成中文。效果取决于模型的中文推理能力。
> ```
> 
> **API 文档**（如果有模块）：
> ```python
> """
> CoTPromptManager
> ================
> 
> Methods
> -------
> add_example(ex: CoTExample)
>     添加示例到库中。
> 
> select_examples(question: str, k: int = 3) -> List[CoTExample]
>     选择 k 个最相关的示例。
>     当前实现：随机选择（可替换为语义相似度）。
> 
> build_prompt(question: str, k: int = 3) -> str
>     构造完整的 CoT prompt。
> 
> evaluate(test_set, llm_fn, k=3) -> Dict
>     在测试集上评估，返回 {"accuracy": float, "details": List}。
> """
> ```
> 
> **CHANGELOG 模板**：
> ```markdown
> ## Changelog
> 
> ### v0.1 (YYYY-MM-DD)
> - 基础 CoT 功能
> - GSM8K 评估
> - Streamlit Demo
> 
> ### Roadmap
> - [ ] Self-consistency
> - [ ] Tree of Thoughts
> - [ ] Auto-CoT 示例选择
> ```

**你必须做**：
> - 补充 README 和文档
> - 确保陌生人能按 README 跑通
> - 让朋友测试一遍，收集反馈

---

## 任务 3：周复盘（AI 执行：成就总结 + 问题分析 + 改进建议）

**AI 输出**：
> 
> **复盘框架**：
> 
> **1. 成就总结**（本周你做了什么？）
> - 读了 1 篇核心论文（Chain-of-Thought, Wei et al. 2022）
> - 完成了概率推导（CoT 的链式法则分解）
> - 实现了 CoT 提示工具（Python，~100 行）
> - 在 GSM8K 上测试了效果（对比直接 few-shot）
> - 搭建了 Streamlit Demo
> - 写了博客大纲
> 
> **2. 问题分析**（遇到什么障碍？）
> | 问题 | 根因 | 是否解决 | 下次如何避免 |
> |------|------|----------|-------------|
> | 模型效果不如论文 | 模型规模差距 | 部分（换 GPT-4） | 预期管理，对标同规模模型 |
> | API 延迟高 | 网络/模型 | 是（加流式输出） | 准备本地模型备选 |
> | 代码结构混乱 | 开始时没规划 | 部分（周末重构） | 先设计再编码 |
> 
> **3. 时间分析**（时间花在哪？）
> - 论文阅读：X hr（预期 2-3，实际 ？）
> - 推导：X hr（预期 2-3，实际 ？）
> - 代码：X hr（预期 6-8，实际 ？）
> - 博客：X hr（预期 2-3，实际 ？）
> - **下周调整**：如果某部分超时，减少范围或增加缓冲
> 
> **4. 改进建议**
> - 如果论文读得慢：用 AI 预读更充分，减少精读时间
> - 如果代码 Bug 多：增加单元测试，先写测试再写实现
> - 如果博客难产：先写大纲，分块写作，不要追求完美
> 
> **5. 下周计划确认**
> - 主题：Self-Consistency & Advanced CoT
> - 目标：复现 Self-Consistency，集成到现有工具
> - 预期输出：升级版 CoT 工具 + 博客发布
> 
> **情绪检查**：
> - 本周能量：1-10（？）
> - 最兴奋的 moment：？
> - 最沮丧的 moment：？
> - 是否需要调整节奏？

**你必须做**：
> - 填写上述框架（诚实面对问题）
> - 将复盘保存到 [[06-研究复盘日志]]
> - 更新 [[07-日记]]
> - 给自己一个奖励（完成了一周！）

---

## 今日 AI 禁区

- ❌ 让 AI 替读论文
- ❌ 让 AI 替写笔记
- ❌ 让 AI 生成代码路径不验证
- ❌ 让 AI 替准备面试回答

---

## 完成检查清单

- [ ] 集成测试 已完成（AI 已生成，人类需执行）
> - [ ] 文档补全 已完成（AI 已生成，人类需补充）
> - [ ] 周复盘 已完成（AI 已生成，人类需填写）
> - [ ] 所有内容已写入 Obsidian 笔记（**人类必须执行**）
> 
> ---
> 
> *AI 执行时间：约 15 分钟*
> *人类执行时间：约 2-3 小时*
> 