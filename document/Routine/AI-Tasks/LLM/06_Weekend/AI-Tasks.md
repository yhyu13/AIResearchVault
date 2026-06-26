---
tags: [routine/AI-tasks, topic/LLM, day/Weekend]
aliases: []
---

# Weekend：AI 任务清单 — LLM 项目实战

> **人类目标**：Demo 制作 + 博客输出
> **AI 任务**：提供脚手架、解释障碍、生成问题，绝不替代核心工作。

---

## 任务 1：Demo 设计（AI 执行：功能拆解 + 技术选型 + 架构草图）

**AI 输出**：

> **Demo 主题**：CoT Math Solver — 一个可视化数学推理过程的网页 Demo
> 
> **功能拆解**：
> 1. 输入框：用户输入数学问题
> 2. 推理展示：模型生成 CoT 步骤，逐行显示，每步有动画
> 3. 答案展示：高亮最终答案
> 4. 对比模式：切换 "直接生成" vs "CoT 生成" 看效果差异
> 5. 历史记录：保存用户问过的问题和答案
> 
> **技术选型**：
> | 组件 | 选项 | 理由 |
> |------|------|------|
> | 前端 | Streamlit / Gradio | 快速原型，Python 生态 |
> | 后端 | 本地 Llama 3 8B / API | 演示用，成本可控 |
> | CoT 生成 | 自建 prompt + 解析 | 已在前几天实现 |
> | 部署 | Hugging Face Spaces | 免费、易分享 |
> 
> **架构草图**：
> ```
> [用户输入] → [Prompt Builder] → [LLM API] → [CoT Parser]
>                                         ↓
> [前端展示] ← [Step-by-step Renderer] ← [结构化输出]
>                                         ↓
>                                   [History DB]
> ```
> 
> **MVP 范围**（周末可完成）：
> - 只支持 5-10 个预设问题（避免输入解析复杂度）
> - 只做 CoT 展示，不做对比模式（对比可后续加）
> - 用 Streamlit，30 行代码可跑通
> 
> **代码骨架**：
> ```python
> import streamlit as st
> from cot_manager import CoTPromptManager  # 你周四写的工具
> 
> st.title("🧮 CoT Math Solver")
> 
> # 预设问题
> preset_questions = [
>     "Roger has 5 tennis balls...",
>     # ... 更多
> ]
> 
> question = st.selectbox("选择问题", preset_questions)
> 
> if st.button("Solve with CoT"):
>     # TODO: 调用 CoT 生成
>     # TODO: 解析步骤
>     # TODO: 逐行展示，每行延迟 0.5s
>     pass
> 
> st.markdown("### 历史记录")
> # TODO: 展示历史
> ```

**你必须做**：
- 按 MVP 范围实现，不要过度工程
- 部署到 Hugging Face Spaces 或本地运行
- 截图保存到 [[03-实验案例与代码集]]

---

## 任务 2：博客大纲（AI 执行：标题优化 + 结构建议 + 配图指引）

**AI 输出**：

> **博客主题**：Chain-of-Thought: 从论文到代码的完整实践
> 
> **标题选项**：
> - A. "Chain-of-Thought 提示：让 LLM 学会分步思考"
> - B. "我复现了 CoT 论文：从 17% 到 56% 的数学推理提升"
> - C. "LLM 推理的秘密武器：CoT 实战指南"
> 
> **推荐**：B（有数据、有故事性、有实操）
> 
> **结构建议**：
> ```
> 1. 引言（200字）
>    - 问题：LLM 数学推理差（举例）
>    - 解决：CoT 提示方法
>    - 承诺：本文从论文到代码完整实践
> 
> 2. 论文速读（400字）
>    - Wei et al. 2022 的核心贡献
>    - 关键结果：GSM8K 56%（PaLM 540B + CoT）
>    - 我的批注：为什么只对大模型有效？
> 
> 3. 原理推导（600字）
>    - 概率分解：P(y|x) = Σ P(y|z)P(z|x)
>    - 直觉解释：分步思考降低每步难度
>    - 误差分析：累积误差 vs 单步大误差
> 
> 4. 代码实践（800字 + 代码块）
>    - 环境搭建
>    - Few-shot CoT 实现
>    - 测试结果（对比直接 few-shot）
>    - 遇到的坑和解决
> 
> 5. 进阶扩展（400字）
>    - Self-consistency
>    - Tree of Thoughts
>    - OpenAI o1 的 test-time scaling
> 
> 6. 总结（200字）
>    - CoT 的本质：用显式分解激活隐式推理
>    - 关键洞察：模型规模 + 提示工程 =  emergent ability
>    - 下一步：尝试 Tree of Thoughts
> ```
> 
> **配图指引**：
> - 图 1：CoT 示意图（问题 → 步骤1 → 步骤2 → 答案）
> - 图 2：GSM8K 结果对比柱状图（直接 vs CoT vs Self-consistency）
> - 图 3：你的 Demo 截图（Streamlit 界面）
> - 图 4：文献演进时间线（2020 few-shot → 2022 CoT → 2023 ToT → 2024 o1）
> 
> **字数建议**：2500-3500 字（含代码），阅读时间 8-10 分钟
> 
> **发布平台**：
> - 首选：知乎 / 公众号（中文社区）
> - 次选：个人博客 / Medium
> - 代码：GitHub + Hugging Face Space

**你必须做**：
> - 按大纲写作，不要偏离结构
> - 所有代码必须可运行
> - 配图用你自己的实验结果，不要抄论文图
> - 发布前 AI 辅助润色（但你自己做最终修改）

---

## 任务 3：代码 Review（AI 执行：可读性 + 健壮性 + 文档检查）

**AI 输出**：

> **Review 对象**：你本周写的 CoT 相关代码（`cot_prompt_manager.py` + `streamlit_app.py`）
> 
> **可读性检查**：
> - [ ] 函数名是否清晰？（如 `build_prompt` 比 `bp` 好）
> - [ ] 是否有类型注解？（`def f(x: str) -> int:`）
> - [ ] 是否有 docstring？（每个函数 1-2 行说明）
> - [ ] 代码是否分块？（每个函数 < 30 行）
> - [ ] 是否有 Magic Number？（如 `k=3` 应改为常量）
> 
> **健壮性检查**：
> - [ ] API 调用是否有重试？（网络不稳定）
> - [ ] 输入是否验证？（空字符串、过长输入）
> - [ ] 错误处理是否完善？（try-except 关键路径）
> - [ ] 是否有超时机制？（防止 API 挂起）
> - [ ] 日志是否足够？（关键步骤打印）
> 
> **文档检查**：
> - [ ] README 是否包含安装步骤？
> - [ ] 是否有使用示例？
> - [ ] 是否说明依赖版本？
> - [ ] 是否有 LICENSE？
> - [ ] 是否有 CONTRIBUTING（如计划开源）？
> 
> **快速修复建议**（如果存在）：
> 1. 添加 `requirements.txt`
> 2. 添加 `.env.example`（说明需要的 API key）
> 3. 将硬编码的示例抽离到 JSON 文件
> 4. 添加 `pytest` 测试（至少 3 个）
> 5. 添加 GitHub Actions CI（可选）
> 
> **Review 结论模板**：
> ```markdown
> ## 代码 Review 结论
> - 评分：X/10
> - 最大优点：...
> - 最大问题：...
> - 必须修复：...
> - 建议改进：...
> - 是否可发布：是/否（条件：...）
> ```

**你必须做**：
> - 按检查清单逐项审查
> - 修复至少 3 个明显问题
> - 将代码 Review 记录保存到 [[03-实验案例与代码集]]
> - 如果满意，push 到 GitHub

---

## 今日 AI 禁区

- ❌ 让 AI 替读论文
- ❌ 让 AI 替写笔记
- ❌ 让 AI 生成代码路径不验证
- ❌ 让 AI 替准备面试回答

---

## 完成检查清单

- [ ] Demo 设计 已完成（AI 已生成，人类需实现）
> - [ ] 博客大纲 已完成（AI 已生成，人类需写作）
> - [ ] 代码 Review 已完成（AI 已生成，人类需审查）
> - [ ] 所有内容已写入 Obsidian 笔记（**人类必须执行**）
> 
> ---
> 
> *AI 执行时间：约 15 分钟*
> *人类执行时间：约 4-6 小时（周末）*
> 