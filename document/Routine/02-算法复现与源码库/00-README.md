# 02-算法复现与源码库

> **用途**：核心算法推导、伪代码 → 代码、源码阅读、数学验证
> **输入**：论文算法、开源代码、教科书
> **输出**：可运行代码、推导笔记、调试记录

---

## 复现格式

```markdown
---
tags: [implementation, <topic>]
aliases: [<algorithm-name>]
---

# 算法名称

- **来源论文**：[[...]]
- **参考实现**：GitHub 链接
- **主题**：[[LLM]] / [[RL]] / ...

## 算法推导

### 数学基础
### 算法步骤
### 复杂度分析

## 代码实现

```python
# 你的实现
```

## 与参考实现对比

| 维度 | 论文 | 官方实现 | 你的实现 |
|------|------|----------|----------|
| 正确性 | | | |
| 效率 | | | |
| 可读性 | | | |

## 调试记录

## 经验教训
```

---

## 复现索引

| 算法 | 主题 | 状态 | 代码 | 笔记 |
|------|------|------|------|------|
| Agent Harness 六组件架构 | LLM Agent × Game AI | ✅ 完成 | `agent_harness_game/` | [[02-Agent-Harness-Game-AI-2026-07-01]] |
| Agent Harness v2：Verification/Evaluation 深化 | Agent Verification × 评测协议 | ✅ 完成（2026-07-20） | `agent_harness_game/evaluation.py`、`verifier.py`（扩展）、`demo/craft_item.py`、`demo/run_benchmark.py`、`research/R1~R4-*.md`、`plan-v2-verification-eval.md` | [[02-Agent-Harness-Game-AI-2026-07-01]]（第八节）、[[01e-agent-verification-eval-latest]] |
| | | ☐ 待开始 / 🔄 进行中 / ✅ 完成 | | |

---

## 复现 Pipeline

1. **理解**（周二）：AI 辅助推导，你手写推导过程
2. **骨架**（周二晚）：AI 生成代码骨架，你填充核心逻辑
3. **测试**（周二晚）：AI 设计测试用例，你运行验证
4. **对比**（周四）：与官方实现对比，找差异
5. **优化**（周四）：AI 建议优化方向，你实现

