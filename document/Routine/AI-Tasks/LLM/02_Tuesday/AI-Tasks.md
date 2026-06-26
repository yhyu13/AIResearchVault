---
tags: [routine/AI-tasks, topic/LLM, day/Tuesday]
aliases: []
---

# Tuesday：AI 任务清单 — LLM 专项技能突破

> **人类目标**：算法推导 + 数学基础
> **AI 任务**：提供脚手架、解释障碍、生成问题，绝不替代核心工作。

---

## 任务 1：算法推导辅助（AI 执行：逐步推导 + 符号检查 + 边界条件）

**推导目标**：CoT 提示下的条件概率分解与误差分析

**AI 输出**：

> **Step 1: 问题建模**
> 设输入问题 $x$，目标答案 $y$。传统生成模型直接估计 $P(y|x)$。CoT 引入中间推理步骤 $z = (z_1, z_2, ..., z_n)$，目标变为估计 $P(y, z|x)$，然后边缘化得到 $P(y|x)$。

> **Step 2: 链式分解**
> 通过概率的链式法则：
> $$P(y|x) = \sum_z P(y|x, z)P(z|x) = \sum_z P(y|z_n) \prod_{i=1}^n P(z_i|z_{i-1}, x)$$
> 其中 $z_0 = x$（初始条件）。

> **Step 3: 与直接生成的对比**
> - 直接：$P(y|x)$，单步决策，误差集中在"理解→回答"这一步
> - CoT：$\prod_{i=1}^n P(z_i|z_{i-1}, x)$，多步决策，每步误差较小但累积
> - 关键洞察：CoT 有效的前提是每步条件概率 $P(z_i|z_{i-1}, x)$ 比 $P(y|x)$ 更容易估计，即每步语义更"简单"

> **Step 4: 误差分析**
> 设每步误差 $\epsilon_i = 1 - P(z_i^{\text{correct}}|z_{i-1}, x)$。假设各步独立：
> - 正确路径概率：$P_{\text{CoT}} = \prod_{i=1}^n (1 - \epsilon_i)$
> - 直接生成正确概率：$P_{\text{direct}} = 1 - \epsilon_{\text{total}}$
> - 当 $n\epsilon \ll 1$ 时：$P_{\text{CoT}} \approx 1 - n\epsilon$，而 $P_{\text{direct}}$ 中 $\epsilon_{\text{total}}$ 可能很大
> - **边界条件**：如果 $\epsilon_i > 1/n$，CoT 可能更差（错误累积）

> **Step 5: 为什么模型规模重要**
> 大模型有更精确的 $P(z_i|z_{i-1}, x)$ 估计（更低的 $\epsilon_i$），使得 $P_{\text{CoT}} > P_{\text{direct}}$。小模型 $\epsilon_i$ 太高，累积误差导致 CoT 不如直接生成。

> **符号检查**：$x$ = 问题，$y$ = 答案，$z_i$ = 第 $i$ 个推理步骤，$n$ = 步骤数，$\epsilon_i$ = 第 $i$ 步错误率。注意 $z$ 是离散的 token 序列，严格来说应使用 $P(z|x) = \prod_t P(z_t|z_{<t}, x)$，但这里做了步骤级抽象。

> **边界条件**：
> 1. 短问题（$n=1$）：CoT 无收益，甚至有害（额外噪声）
> 2. 模型过小：$\epsilon_i$ 太大，累积误差 > 单步误差
> 3. 步骤不独立：实际中 $P(z_i|z_{i-1}, x)$ 依赖前面所有步骤，上述分析是近似

**你必须做**：
- 在纸上或 LaTeX 中重新推导一遍
- 检查每一步的符号和假设
- 尝试改变假设（如相关步骤），看结论如何变化

---

## 任务 2：数学基础补漏（AI 执行：缺失知识点识别 + 补充材料）

**AI 输出**：

> **基于 CoT 推导的缺失知识检查**：

> | 知识点 | 你在推导中是否需要？ | 掌握程度 | 补充材料 |
> |--------|---------------------|----------|----------|
> | 条件概率链式法则 | ✅ 必须 | 自检 | 任意概率论教材 Ch.3 |
> | 乘积概率的泰勒展开 | ✅ 近似分析 | 自检 | 微积分，$\ln(1-x) \approx -x$ |
> | 信息论：困惑度 (Perplexity) | 可选 | 自检 | 交叉熵与模型置信度 |
> | 自回归模型的概率分解 | 可选 | 自检 | GPT 原始论文 / 任一 NLG 教材 |
> | EM 算法的近似思想 | 类比理解 | 自检 | Bishop PRML Ch.9 |

> **补充材料推荐**：
> 1. **快速补漏**（30 min）：看 3Blue1Brown 的 "Bayes' Theorem" 和 "Probability" 系列视频
> 2. **深入理解**（2 hr）：读《Probability and Statistics for Engineers》Ch.2-3
> 3. **与 LLM 关联**：读 "The Statistical Mechanics of Language" (arXiv:2301.000) 的前 10 页

> **你的知识缺口自查**：
> - [ ] 我能独立写出 $P(A|B) = P(A,B)/P(B)$ 的完整推导
> - [ ] 我理解为什么 $\prod(1-\epsilon_i) \approx 1 - \sum\epsilon_i$（当 $\epsilon_i$ 很小时）
> - [ ] 我知道自回归语言模型中 $P(y|x)$ 实际是如何分解的

**你必须做**：
- 勾选你自信的知识点，标记不自信的
- 对不自信的，花 30-60 min 看补充材料
- 在笔记中记录你的理解

---

## 任务 3：代码骨架生成（AI 执行：伪代码 → 可运行代码，你填充核心逻辑）

**AI 输出**：

> **需求**：实现一个 CoT 提示生成器，接收问题列表，构造 few-shot CoT 示例，调用 LLM API 生成推理结果。

> **代码骨架**：

```python
"""
CoT Prompt Generator & Executor
- 输入：问题列表 + few-shot CoT 示例
- 输出：每个问题的推理过程和答案
- 依赖：openai >= 1.0 (或任何兼容 OpenAI API 的客户端)
"""

import os
from typing import List, Tuple
from openai import OpenAI

# TODO: 配置你的 API key 和 base URL
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-key-here"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

# ── Few-shot CoT 示例库（你填充具体例子） ──
FEW_SHOT_EXAMPLES: List[Tuple[str, str]] = [
    # (问题, 包含推理过程的答案)
    # TODO: 从论文 Appendix B 复制至少 3 个示例
    # 示例格式：
    # ("Roger has 5 tennis balls. He buys 2 more cans. Each can has 3 balls. How many?",
    #  "Roger starts with 5 balls. 2 cans of 3 balls each is 6 balls. 5 + 6 = 11. The answer is 11."),
]

def build_cot_prompt(question: str, examples: List[Tuple[str, str]]) -> str:
    """
    构造 CoT 提示字符串。
    
    TODO: 实现提示拼接逻辑
    - 将 examples 拼接成 "Q: ...\nA: ...\n\n" 的格式
    - 最后附加当前问题
    - 返回完整 prompt
    """
    # YOUR CODE HERE
    pass

def call_llm(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    调用 LLM API。
    
    TODO: 使用 client.chat.completions.create() 发送请求
    - temperature 建议 0（确定性推理）
    - max_tokens 根据问题复杂度调整
    """
    # YOUR CODE HERE
    pass

def parse_cot_response(response: str) -> Tuple[str, str]:
    """
    解析 LLM 输出，提取推理过程和最终答案。
    
    TODO: 实现解析逻辑
    - 如果响应包含 "The answer is"，提取后面的数字
    - 返回 (推理过程, 最终答案)
    """
    # YOUR CODE HERE
    pass

def evaluate(
    questions: List[str],
    answers: List[str],
    examples: List[Tuple[str, str]]
) -> float:
    """
    在测试集上评估准确率。
    
    TODO: 对每个问题：
    1. build_cot_prompt
    2. call_llm
    3. parse_cot_response
    4. 与 ground truth 对比
    5. 计算准确率
    """
    # YOUR CODE HERE
    pass

# ── 主程序 ──
if __name__ == "__main__":
    # TODO: 加载 GSM8K 测试集（或你自己构造的 5-10 题）
    # TODO: 运行 evaluate()
    # TODO: 打印结果，对比直接 few-shot（无 CoT）的准确率
    pass
```

> **需要你填充的部分**：
> 1. `FEW_SHOT_EXAMPLES`：从 Wei et al. 2022 的 Appendix B 复制 3-8 个示例
> 2. `build_cot_prompt`：拼接逻辑（约 10 行）
> 3. `call_llm`：API 调用（约 5 行）
> 4. `parse_cot_response`：解析逻辑（约 5-10 行）
> 5. `evaluate`：评估循环（约 15 行）
> 6. `__main__`：加载数据 + 运行

> **预期总代码量**：约 80-120 行（骨架已提供 ~60 行，你填充 ~40-60 行）

**你必须做**：
- 填充 TODO 部分
- 运行至少 5 个测试用例
- 对比直接 few-shot vs CoT 的准确率差异
- 将代码保存到 [[03-实验案例与代码集]]

---

## 任务 4：测试用例设计（AI 执行：边界条件 + 异常输入 + 对比基准）

**AI 输出**：

> **测试用例设计**：

> **正常用例**（必须全部通过）：
> | 编号 | 问题 | 预期答案 | 难度 |
> |------|------|----------|------|
> | 1 | 1+1=？ | 2 |  trivial |
> | 2 | 23 × 4 = ？ | 92 |  easy |
> | 3 | 一个农场有 2 只鸡，每只每天下 3 个蛋，一周下多少个？ | 42 |  medium |
> | 4 | 小明有 15 元，买了 3 支铅笔每支 2 元，还剩多少？ | 9 |  medium |
> | 5 | 一个水池 5 小时注满，8 小时排空，同时打开多久满？ | 40/3 ≈ 13.33 |  hard |

> **边界条件**（检验鲁棒性）：
> | 编号 | 问题 | 预期行为 | 测试目的 |
> |------|------|----------|----------|
> | B1 | "0 除以 5 等于多少？" | 正确回答 0 | 零值处理 |
> | B2 | "5 除以 0 等于多少？" | 指出未定义/错误 | 除零错误处理 |
> | B3 | "30 个苹果分给 4 个人，每人几个？剩几个？" | 商 7 余 2 | 多部分答案 |
> | B4 | "如果昨天是 3 号，明天是几号？" | 5 号 | 常识推理干扰 |
> | B5 | "999999999 × 999999999 = ？" | 大数正确 | 数值溢出/精度 |

> **异常输入**（检验错误处理）：
> | 编号 | 输入 | 预期行为 |
> |------|------|----------|
> | E1 | 空字符串 "" | 拒绝回答或提示输入问题 |
> | E2 | 非数学问题 "讲个笑话" | 不强行数学推理，正常回答 |
> | E3 | 模糊问题 "这个答案是什么？" | 请求澄清 |
> | E4 | 超长问题（>500 tokens） | 不崩溃，尽量处理 |
> | E5 | 含无关信息的问题 | 能提取关键信息，忽略噪音 |

> **对比基准**：
> - 基准 1：直接 few-shot（无 CoT 中间步骤）
> - 基准 2：Zero-shot CoT（"Let's think step by step"）
> - 基准 3：你的 few-shot CoT 实现
> - 对比维度：准确率、token 消耗、响应时间

**你必须做**：
- 运行全部测试用例
- 记录 pass/fail 结果
- 分析失败用例的根因
- 更新代码修复 bug

---

## 今日 AI 禁区

- ❌ 让 AI 替读论文
- ❌ 让 AI 替写笔记
- ❌ 让 AI 生成代码路径不验证
- ❌ 让 AI 替准备面试回答

---

## 完成检查清单

- [ ] 算法推导辅助 已完成（AI 已生成，人类需推导验证）
- [ ] 数学基础补漏 已完成（AI 已生成，人类需自查）
- [ ] 代码骨架生成 已完成（AI 已生成，人类需填充实现）
- [ ] 测试用例设计 已完成（AI 已生成，人类需运行测试）
- [ ] 所有内容已写入 Obsidian 笔记（**人类必须执行**）

---

*AI 执行时间：约 15 分钟*
*人类执行时间：约 2-3 小时*
