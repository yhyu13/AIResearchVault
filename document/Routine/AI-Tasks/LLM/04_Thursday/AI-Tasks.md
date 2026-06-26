---
tags: [routine/AI-tasks, topic/LLM, day/Thursday]
aliases: []
---

# Thursday：AI 任务清单 — LLM 工程化与工具链

> **人类目标**：复现代码 + 工具开发
> **AI 任务**：提供脚手架、解释障碍、生成问题，绝不替代核心工作。

---

## 任务 1：代码复现辅助（AI 执行：README 理解 + 依赖安装 + 环境排错）

**AI 输出**：

> **复现目标**：用已有代码库跑通 CoT 在 GSM8K 上的实验
> 
> **推荐代码库**：
> - 官方（无）：Wei et al. 2022 无官方代码，但社区有复现
> - 推荐：OpenAI 的 `evals` 库中有 GSM8K 评估代码
> - 备选：Hugging Face `lm-evaluation-harness` 支持 GSM8K + CoT
> 
> **环境搭建步骤**：
> ```bash
> # 1. 创建环境
> python -m venv venv-cot
> source venv-cot/bin/activate  # Windows: venv-cot\Scripts\activate
> 
> # 2. 安装依赖
> pip install openai datasets transformers torch
> 
> # 3. 下载 GSM8K
> python -c "from datasets import load_dataset; load_dataset('gsm8k', 'main', cache_dir='./data')"
> 
> # 4. 验证安装
> python -c "import openai; print(openai.__version__)"
> python -c "import datasets; print('datasets OK')"
> ```
> 
> **常见错误**：
> | 错误 | 原因 | 解决 |
> |------|------|------|
> | `ModuleNotFoundError: openai` | 未安装或环境未激活 | `pip install openai` |
> | `API key not found` | 未设置环境变量 | `export OPENAI_API_KEY=...` |
> | `datasets` 下载慢 | 网络问题 | 使用镜像或本地缓存 |
> | `CUDA out of memory` | GPU 显存不足 | 使用 CPU 或更小的 batch |
> 
> **复现检查清单**：
> - [ ] 环境已创建并激活
> - [ ] GSM8K 数据集已下载
> - [ ] 至少能运行 10 个测试样本
> - [ ] 输出格式与论文描述一致

**你必须做**：
- 按步骤搭建环境
- 运行至少 10 个 GSM8K 样本
- 对比你的结果与论文 reported 结果（~56% for PaLM 540B with CoT）
- 记录环境版本到 [[03-实验案例与代码集]]

---

## 任务 2：调试诊断（AI 执行：错误分析 + 修复建议 + 回归验证）

**AI 输出**：

> **常见 CoT 复现错误及诊断**：
> 
> **错误 1：CoT 效果不如论文**
> - 根因：你的 few-shot 示例质量差、模型不够大、温度设置不对
> - 诊断：检查 temperature 是否为 0（论文用 greedy decoding），检查示例是否包含完整推理步骤
> - 修复：从论文 Appendix 复制 exact prompt，使用 greedy decoding
> 
> **错误 2：格式不一致（模型不输出 "The answer is X"）**
> - 根因：few-shot 示例的格式与模型输出不匹配
> - 诊断：检查 prompt 是否明确要求 "The answer is" 格式
> - 修复：在 prompt 末尾添加 "Let's think step by step. The answer is"
> 
> **错误 3：数值计算错误**
> - 根因：模型算术能力差（尤其是 7B-13B 模型）
> - 诊断：检查是否用了足够大的模型（100B+）或需要外部计算器
> - 修复：使用 tool-augmented CoT（Python interpreter）或更大的模型
> 
> **错误 4：API 调用失败/超时**
> - 根因：网络、配额限制、请求过大
> - 诊断：检查 API 响应码、重试机制、并发数
> - 修复：添加指数退避重试、降低并发、使用本地模型
> 
> **调试流程**：
> 1. 隔离：先测试单个样本，确认基础功能正常
> 2. 对比：用同样的 prompt 对比不同模型（GPT-3.5 vs GPT-4）
> 3. 日志：记录每次 API 调用的输入/输出/延迟
> 4. 回归：修复后重新运行，验证无 regression

**你必须做**：
- 如果你遇到了错误，按上述流程诊断
- 记录错误和修复到 [[03-实验案例与代码集]]
- 如果你没有遇到错误，故意制造一个错误（如删除推理步骤），观察行为变化

---

## 任务 3：工具开发（AI 执行：需求分析 → 设计 → 骨架代码，你实现核心逻辑）

**AI 输出**：

> **工具需求**：CoT Prompt Manager — 一个管理 few-shot CoT 示例、自动生成提示、评估效果的小工具
> 
> **功能设计**：
> 1. 示例库管理（CRUD few-shot 示例）
> 2. 自动提示生成（根据问题选择最合适的示例）
> 3. 批量评估（在数据集上运行并统计准确率）
> 4. 结果对比（对比不同示例集/参数的效果）
> 
> **骨架代码**（已保存到 [[03-实验案例与代码集]]）：
> 
> ```python
> # cot_prompt_manager.py
> from dataclasses import dataclass
> from typing import List, Dict, Tuple
> import json
> 
> @dataclass
> class CoTExample:
>     question: str
>     reasoning: str
>     answer: str
>     
>     def to_prompt(self) -> str:
>         return f"Q: {self.question}\nA: {self.reasoning} The answer is {self.answer}.\n\n"
> 
> class CoTPromptManager:
>     def __init__(self, examples: List[CoTExample] = None):
>         self.examples = examples or []
>     
>     def add_example(self, ex: CoTExample) -> None:
>         # TODO: 实现
>         pass
>     
>     def select_examples(self, question: str, k: int = 3) -> List[CoTExample]:
>         # TODO: 实现示例选择（随机 / 语义相似度 / 难度匹配）
>         pass
>     
>     def build_prompt(self, question: str, k: int = 3) -> str:
>         # TODO: 选择 k 个示例 + 拼接 + 附加问题
>         pass
>     
>     def evaluate(self, test_set: List[Tuple[str, str]], 
>                  llm_fn, k: int = 3) -> Dict:
>         # TODO: 批量评估，返回准确率 / 每题结果
>         pass
>     
>     def save(self, path: str) -> None:
>         # TODO: JSON 序列化
>         pass
>     
>     @classmethod
>     def load(cls, path: str) -> "CoTPromptManager":
>         # TODO: JSON 反序列化
>         pass
> 
> # ── 使用示例 ──
> if __name__ == "__main__":
>     # TODO: 加载 GSM8K 数据
>     # TODO: 创建 CoTPromptManager
>     # TODO: 运行 evaluate()
>     # TODO: 对比不同 k 值的效果
>     pass
> ```
> 
> **核心逻辑需要你实现**（约 50-80 行）：
> - `select_examples`：最简实现用随机选择，进阶用 embedding 相似度
> - `build_prompt`：拼接示例 + 当前问题
> - `evaluate`：循环调用 LLM，解析结果，统计指标
> 
> **扩展方向**：
> - 自动示例选择（Auto-CoT 风格：用聚类选代表性示例）
> - 动态示例数量（根据问题难度自动调整 k）
> - 多轮评估（Self-consistency 集成）

**你必须做**：
- 填充 TODO 部分
- 让工具能在 GSM8K 上跑通
- 将完整工具保存到 [[03-实验案例与代码集]]

---

## 任务 4：性能剖析（AI 执行：瓶颈识别 + 优化方向 + 对标分析）

**AI 输出**：

> **性能指标（你的 CoT 实现 vs 理想）**：
> 
> | 维度 | 你的实现 | 论文/业界 | 差距 | 优化方向 |
> |------|----------|----------|------|----------|
> | 准确率 (GSM8K) | ？ | 56% (PaLM 540B) | 模型差距 | 换更大模型或优化 prompt |
> | 延迟 (单题) | ？ | 1-3s | ？ | 流式输出、缓存、并行 |
> | Token 消耗 | ？ | ~200-500/题 | ？ | 缩短示例、压缩推理 |
> | 成本 ($/1K题) | ？ | 取决于模型 | ？ | 使用更便宜的模型、本地部署 |
> | 并发能力 | ？ | 无限制（本地） | ？ | 批处理、异步 |
> 
> **瓶颈识别框架**：
> 1. **模型层**：模型是否足够大？是否有更好的开源替代？（Llama 3 70B vs GPT-4）
> 2. **Prompt 层**：示例是否最优？是否可以用 Zero-shot-CoT 减少 token？
> 3. **推理层**：是否用了 greedy decoding？温度是否合适？
> 4. **工程层**：是否批量处理？是否缓存了重复请求？
> 
> **对标分析**：
> - 对标 1：GPT-4 + CoT（商业标杆）
> - 对标 2：Llama 3 70B + CoT（开源标杆）
> - 对标 3：专用数学模型（如 Mathstral、Qwen2-Math）
> 
> **优化优先级**：
> 1. P0：换更好的模型（影响最大）
> 2. P1：优化 prompt 质量（示例选择）
> 3. P2：工程优化（批处理、缓存）
> 4. P3：算法优化（self-consistency、Tree of Thoughts）

**你必须做**：
- 测量你当前的性能指标（准确率、延迟、token、成本）
- 填入上表
- 识别当前最大瓶颈
- 尝试至少一个优化方向，记录效果

---

## 今日 AI 禁区

- ❌ 让 AI 替读论文
- ❌ 让 AI 替写笔记
- ❌ 让 AI 生成代码路径不验证
- ❌ 让 AI 替准备面试回答

---

## 完成检查清单

- [ ] 代码复现辅助 已完成（AI 已生成，人类需搭建环境）
- [ ] 调试诊断 已完成（AI 已生成，人类需排错）
- [ ] 工具开发 已完成（AI 已生成，人类需填充实现）
- [ ] 性能剖析 已完成（AI 已生成，人类需测量）
- [ ] 所有内容已写入 Obsidian 笔记（**人类必须执行**）

---

*AI 执行时间：约 15 分钟*
*人类执行时间：约 2-3 小时*
