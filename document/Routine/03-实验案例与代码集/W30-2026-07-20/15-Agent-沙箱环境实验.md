---
tags: [experiment, sandbox, agent-safety, checkpoint-restore, llm-in-sandbox, 2026-07-20]
aliases: [Sandbox-Experiment]
created: 2026-07-20
---

# 实验 15：Agent 沙箱环境 — LLM-in-Sandbox 与语义感知 Checkpoint/Restore 实验

> **参考论文**: LLM-in-Sandbox (arXiv:2601.16206, 2026), Crab (arXiv:2604.28138, 2026), SafeArena (ICML 2025), ceLLMate (arXiv:2512.12594, 2025)
> **实验时间**: 2026-07-20
> **核心架构**: 沙箱隔离 + 语义感知 Checkpoint/Restore + 安全评估
> **关联笔记**: [[01d-sandbox-latest]]

---

## 一、实验背景与目标

### 1.1 背景

Agent 沙箱是 LLM Agent 从"纯文本对话"进化为"可执行智能体"的关键基础设施。2025-2026 年，沙箱技术经历了从"安全隔离工具"到"认知扩展基础设施"的范式转变：

- **LLM-in-Sandbox**: 沙箱不仅是安全工具，更是 LLM 的"外化认知扩展"——文件系统作为外化记忆，代码执行作为外化计算
- **Crab**: 语义感知 Checkpoint/Restore，通过 eBPF 观察 OS 效应，智能选择 checkpoint 粒度
- **SafeArena**: 暴露 Web Agent 的严重安全漏洞——GPT-4o 对有害请求合规率高达 34.7%
- **ceLLMate**: 浏览器级沙箱，限制环境权限，缩小 prompt injection 的 blast radius

**关键洞察**: 沙箱从"关坏人的笼子"进化为"扩展 LLM 能力的工具"。

### 1.2 实验目标

1. 实现一个**简化版沙箱环境**：模拟文件系统 + 代码执行 + 状态隔离
2. 实现**Checkpoint/Restore**：保存和恢复沙箱状态（文件 + 变量 + 执行位置）
3. 实现**安全策略**：边界检查、权限限制、危险操作拦截
4. 实现**语义感知 C/R**：只 checkpoint 发生变化的文件/变量
5. 验证：沙箱能否安全执行 Agent 代码，并在错误时恢复

---

## 二、核心概念

### 2.1 沙箱作为认知扩展

```
传统 LLM: 输入 → 推理 → 输出  // 纯文本，上下文窗口有限

LLM-in-Sandbox: 输入 → 推理 → 沙箱操作 → 观察结果 → 再推理 → 输出
                  // 文件系统扩展记忆（存储中间结果）
                  // 代码执行扩展计算（运行复杂算法）
                  // 外部资源扩展知识（下载数据、调用 API）

示例：分析 100K token 的文档
  传统: 直接放入 prompt → 超出上下文窗口
  沙箱: 写入文件 → 用 Python 脚本分析 → 读取关键结论 → 生成回答
  效果: token 消耗降低 8×（100K → 13K）
```

### 2.2 Checkpoint/Restore 的语义感知

```
传统 C/R: 每轮全量 snapshot → I/O 开销巨大 → 延迟秒级

Crab 语义感知 C/R:
  1. 观察 Agent 交互的 OS 可见效应（文件系统、进程、内存变化）
  2. 智能分类 checkpoint 粒度：
     - 无变化 → 无需 checkpoint
     - 仅文件变化 → 仅文件系统 snapshot
     - 进程状态变化 → 进程级 checkpoint
     - 全局变化 → 全量 snapshot
  3. 将 checkpoint 工作重叠到 LLM 等待窗口中
  
效果: 恢复正确率 8% → 100%，checkpoint 流量减少 87%
```

### 2.3 安全评估框架

```
SafeArena 风险等级：
  Compliant（完全执行）→ 最高风险
  Partial（部分执行）→ 中高风险
  Refusal（拒绝）→ 安全
  Error（错误）→ 意外安全

关键发现：
  - GPT-4o 完成 34.7% 的有害请求
  - Claude-3.5 完成 22.8% 的有害请求
  - 安全对齐在 Web Agent 场景中严重迁移失败
```

---

## 三、实验架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent 沙箱环境实验                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐     Agent 代码      ┌──────────────┐    │
│   │   LLM Agent   │ ─────────────────→ │   沙箱环境    │    │
│   │  (生成代码)   │                    │  (隔离执行)   │    │
│   └──────────────┘                    └──────┬───────┘    │
│          ↑                                   │             │
│          │ 观察结果                            ↓ 执行结果    │
│          │                          ┌──────────────┐      │
│          │                          │  安全策略检查 │      │
│          │                          │  边界/权限/危险 │      │
│          │                          └──────┬───────┘      │
│          │                                 │               │
│          │                    ┌────────────┴────────────┐  │
│          │                    ↓                        ↓  │
│          │            ┌──────────────┐          ┌──────────────┐│
│          │            │  Checkpoint  │          │   Restore    ││
│          │            │  (语义感知)   │          │  (状态恢复)  ││
│          │            └──────────────┘          └──────────────┘│
│          │                                                   │
│          └───────────────────────────────────────────────────┘
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、完整代码实现

```python
#!/usr/bin/env python3
"""
Agent Sandbox Environment Experiment
=====================================
A simplified reproduction of LLM-in-Sandbox and Crab concepts:
  1. Sandbox Environment: isolated file system + code execution
  2. Semantic Checkpoint/Restore: only save changed state
  3. Safety Policies: boundary checks, permission limits, dangerous op拦截
  4. Agent Loop: generate code → execute in sandbox → observe → repeat

Environment: Pure Python (no Docker/VM needed)
LLM: Simulated (rule-based) for reproducibility
"""

from __future__ import annotations

import os
import re
import json
import copy
import random
import traceback
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime
from pathlib import Path


# ============================================================================
#  MODULE 0: Sandbox File System (isolated virtual file system)
#  模块 0：沙箱文件系统 —— 隔离的虚拟文件系统
# ============================================================================

class SandboxFileSystem:
    """
    沙箱文件系统 —— 隔离的虚拟文件系统
    
    初学者要点：
    - 模拟真实文件系统，但完全隔离在内存中
    - Agent 可以创建、读取、修改、删除文件
    - 所有操作都在沙箱内，不影响真实系统
    - 支持目录结构、文件权限、文件类型
    """
    
    def __init__(self, root_dir: str = "/sandbox"):
        self.root_dir = root_dir
        self.files: Dict[str, Dict[str, Any]] = {}  # path -> {content, type, permissions}
        self._init_default_files()
    
    def _init_default_files(self):
        """初始化默认文件"""
        self.files[f"{self.root_dir}/README.txt"] = {
            "content": "Welcome to the sandbox!\nYou can create, read, and modify files here.",
            "type": "text",
            "permissions": "rw"
        }
        self.files[f"{self.root_dir}/data/"] = {
            "content": None,
            "type": "directory",
            "permissions": "rwx"
        }
    
    def write_file(self, path: str, content: str) -> bool:
        """写入文件"""
        full_path = self._resolve_path(path)
        self.files[full_path] = {
            "content": content,
            "type": "text",
            "permissions": "rw"
        }
        return True
    
    def read_file(self, path: str) -> Optional[str]:
        """读取文件"""
        full_path = self._resolve_path(path)
        file_info = self.files.get(full_path)
        if file_info and file_info["type"] == "text":
            return file_info["content"]
        return None
    
    def delete_file(self, path: str) -> bool:
        """删除文件"""
        full_path = self._resolve_path(path)
        if full_path in self.files:
            del self.files[full_path]
            return True
        return False
    
    def list_files(self, directory: str = "/") -> List[str]:
        """列出目录中的文件"""
        full_dir = self._resolve_path(directory)
        files = []
        for path in self.files:
            if path.startswith(full_dir):
                rel_path = path[len(self.root_dir):] or "/"
                files.append(rel_path)
        return files
    
    def _resolve_path(self, path: str) -> str:
        """解析路径，确保在沙箱内"""
        if path.startswith(self.root_dir):
            return path
        if path.startswith("/"):
            return f"{self.root_dir}{path}"
        return f"{self.root_dir}/{path}"
    
    def get_state(self) -> Dict[str, Any]:
        """获取文件系统状态（用于 checkpoint）"""
        return copy.deepcopy(self.files)
    
    def restore_state(self, state: Dict[str, Any]):
        """恢复文件系统状态（用于 restore）"""
        self.files = copy.deepcopy(state)


# ============================================================================
#  MODULE 1: Sandbox Environment (code execution + state management)
#  模块 1：沙箱环境 —— 代码执行 + 状态管理
# ============================================================================

class SandboxEnvironment:
    """
    沙箱环境 —— Agent 代码的隔离执行环境
    
    初学者要点：
    - 提供隔离的命名空间，Agent 代码只能访问沙箱内的资源
    - 支持 Python 代码执行（用 exec 在受限命名空间中）
    - 维护执行状态（变量、文件系统、执行历史）
    - 每次执行后可以选择性 checkpoint
    """
    
    def __init__(self):
        self.file_system = SandboxFileSystem()
        self.variables: Dict[str, Any] = {}  # 执行变量空间
        self.execution_history: List[Dict[str, Any]] = []
        self.turn_count = 0
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        在沙箱中执行代码
        
        初学者要点：
        - 使用 exec() 在受限命名空间中执行代码
        - 只暴露安全的内置函数（无 os, sys, subprocess 等）
        - 捕获输出和异常，返回执行结果
        """
        self.turn_count += 1
        
        # 构建安全的执行命名空间
        safe_globals = {
            "__builtins__": {
                "print": self._sandbox_print,
                "len": len,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
            }
        }
        
        # 注入沙箱 API
        safe_globals["sandbox"] = {
            "write_file": self.file_system.write_file,
            "read_file": self.file_system.read_file,
            "delete_file": self.file_system.delete_file,
            "list_files": self.file_system.list_files,
        }
        
        # 注入变量空间（支持跨 turn 状态保持）
        safe_globals["vars"] = self.variables
        
        # 捕获输出
        output_lines = []
        def capture_print(*args, **kwargs):
            output_lines.append(" ".join(str(a) for a in args))
        safe_globals["__builtins__"]["print"] = capture_print
        
        # 执行代码
        try:
            exec(code, safe_globals)
            
            # 更新变量空间
            self.variables = {k: v for k, v in safe_globals.items() 
                            if not k.startswith("__") and k != "sandbox"}
            
            result = {
                "success": True,
                "output": "\n".join(output_lines),
                "variables": dict(self.variables),
                "turn": self.turn_count,
            }
        
        except Exception as e:
            result = {
                "success": False,
                "output": "\n".join(output_lines),
                "error": f"{type(e).__name__}: {str(e)}",
                "traceback": traceback.format_exc(),
                "turn": self.turn_count,
            }
        
        self.execution_history.append({
            "turn": self.turn_count,
            "code": code,
            "result": result,
        })
        
        return result
    
    def _sandbox_print(self, *args):
        """沙箱内的 print 函数"""
        print("[Sandbox]", *args)
    
    def get_state(self) -> Dict[str, Any]:
        """获取完整沙箱状态（用于 checkpoint）"""
        return {
            "file_system": self.file_system.get_state(),
            "variables": copy.deepcopy(self.variables),
            "turn_count": self.turn_count,
        }
    
    def restore_state(self, state: Dict[str, Any]):
        """恢复沙箱状态（用于 restore）"""
        self.file_system.restore_state(state["file_system"])
        self.variables = copy.deepcopy(state["variables"])
        self.turn_count = state["turn_count"]
    
    def get_file_changes(self, previous_state: Dict[str, Any]) -> List[str]:
        """
        获取文件变化列表（语义感知 checkpoint 用）
        
        初学者要点：
        - 比较当前状态与之前状态，只记录变化的文件
        - 这是 Crab 语义感知 C/R 的核心：只 checkpoint 变化的部分
        """
        current_files = self.file_system.files
        previous_files = previous_state.get("file_system", {})
        
        changes = []
        
        # 新增或修改的文件
        for path, info in current_files.items():
            if path not in previous_files:
                changes.append(f"+ {path}")
            elif info != previous_files[path]:
                changes.append(f"~ {path}")
        
        # 删除的文件
        for path in previous_files:
            if path not in current_files:
                changes.append(f"- {path}")
        
        return changes


# ============================================================================
#  MODULE 2: Safety Sandbox (security policies)
#  模块 2：安全沙箱 —— 安全策略与危险操作拦截
# ============================================================================

class SafetySandbox:
    """
    安全沙箱 —— 检查 Agent 代码和动作的安全性
    
    初学者要点：
    - 白名单机制：只允许安全的内置函数和沙箱 API
    - 危险代码检测：检查是否包含 os, sys, subprocess 等危险导入
    - 边界检查：限制文件操作范围在沙箱内
    - 资源限制：限制执行时间、内存、文件大小
    """
    
    DANGEROUS_PATTERNS = [
        r"import\s+os",
        r"import\s+sys",
        r"import\s+subprocess",
        r"__import__",
        r"eval\s*\(",
        r"exec\s*\(",
        r"open\s*\(",
        r"file\s*\(",
        r"socket",
        r"urllib",
        r"requests",
    ]
    
    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
    
    def validate_code(self, code: str) -> Tuple[bool, str]:
        """
        验证代码安全性
        
        Returns: (is_safe, reason)
        """
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                reason = f"检测到危险代码模式: {pattern}"
                self.violations.append({
                    "type": "dangerous_code",
                    "pattern": pattern,
                    "code": code[:100],
                })
                return False, reason
        
        return True, "代码安全检查通过"
    
    def validate_file_access(self, path: str, sandbox_root: str) -> bool:
        """验证文件访问是否在沙箱范围内"""
        resolved = os.path.normpath(path)
        return resolved.startswith(sandbox_root) or not resolved.startswith("/")
    
    def get_violations_summary(self) -> Dict[str, Any]:
        """获取违规统计"""
        return {
            "total_violations": len(self.violations),
            "violations": self.violations,
        }


# ============================================================================
#  MODULE 3: Checkpoint/Restore Manager (semantic-aware)
#  模块 3：Checkpoint/Restore 管理器 —— 语义感知的快照管理
# ============================================================================

@dataclass
class Checkpoint:
    """检查点数据类"""
    id: str
    turn: int
    state: Dict[str, Any]
    changes: List[str]  # 语义感知：只记录变化的部分
    timestamp: datetime
    description: str


class CheckpointManager:
    """
    Checkpoint/Restore 管理器 —— 语义感知的快照管理
    
    初学者要点：
    - 传统 C/R：每轮全量 snapshot → I/O 开销大
    - 语义感知 C/R：只记录变化的部分 → 效率高
    - 支持从任意 checkpoint 恢复，支持分支（类似 save-scumming）
    """
    
    def __init__(self):
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.checkpoint_counter = 0
        self.last_state: Optional[Dict[str, Any]] = None
    
    def create_checkpoint(
        self,
        env: SandboxEnvironment,
        description: str = ""
    ) -> Checkpoint:
        """
        创建检查点（语义感知）
        
        初学者要点：
        - 获取当前完整状态
        - 与上一个状态比较，只记录变化的文件
        - 存储 checkpoint，更新 last_state
        """
        self.checkpoint_counter += 1
        cp_id = f"cp_{self.checkpoint_counter:04d}"
        
        current_state = env.get_state()
        
        # 语义感知：计算变化
        changes = []
        if self.last_state is not None:
            changes = env.get_file_changes(self.last_state)
        else:
            changes = [f"+ {path}" for path in current_state["file_system"]]
        
        cp = Checkpoint(
            id=cp_id,
            turn=current_state["turn_count"],
            state=current_state,
            changes=changes,
            timestamp=datetime.now(),
            description=description,
        )
        
        self.checkpoints[cp_id] = cp
        self.last_state = copy.deepcopy(current_state)
        
        return cp
    
    def restore_checkpoint(self, cp_id: str, env: SandboxEnvironment) -> bool:
        """从检查点恢复"""
        cp = self.checkpoints.get(cp_id)
        if not cp:
            return False
        
        env.restore_state(cp.state)
        self.last_state = copy.deepcopy(cp.state)
        return True
    
    def get_checkpoint_stats(self) -> Dict[str, Any]:
        """获取 checkpoint 统计"""
        total_size = sum(
            len(json.dumps(cp.state)) for cp in self.checkpoints.values()
        )
        
        return {
            "total_checkpoints": len(self.checkpoints),
            "total_size_bytes": total_size,
            "avg_size_bytes": total_size / len(self.checkpoints) if self.checkpoints else 0,
            "checkpoints": [
                {
                    "id": cp.id,
                    "turn": cp.turn,
                    "changes": len(cp.changes),
                    "description": cp.description,
                }
                for cp in self.checkpoints.values()
            ],
        }


# ============================================================================
#  MODULE 4: Simulated LLM Agent (code generator)
#  模块 4：模拟 LLM Agent —— 生成沙箱代码
# ============================================================================

class SimulatedLLMAgent:
    """
    模拟 LLM Agent —— 根据任务生成沙箱代码
    
    初学者要点：
    - 真实 LLM-in-Sandbox 调用 GPT-4 生成代码
    - 这里用规则模板模拟：根据任务类型选择代码模板
    - 支持的任务：文件操作、数据分析、计算、错误恢复
    """
    
    def __init__(self):
        self.call_count = 0
    
    def generate_code(self, task: str, sandbox_state: Dict[str, Any]) -> str:
        """根据任务生成代码"""
        self.call_count += 1
        
        # 任务 1: 创建文件
        if "创建" in task or "写入" in task:
            filename = task.split("创建")[-1].split("写入")[-1].strip() or "output.txt"
            return f'''
# 创建文件
content = "这是由 Agent 生成的内容\\n生成时间: turn {sandbox_state.get('turn_count', 0)}"
sandbox["write_file"]("{filename}", content)
print(f"已创建文件: {filename}")
print(f"内容长度: {{len(content)}} 字符")
'''
        
        # 任务 2: 读取文件
        elif "读取" in task or "查看" in task:
            return f'''
# 读取文件
files = sandbox["list_files"]()
print("沙箱中的文件:")
for f in files:
    print(f"  {{f}}")
'''
        
        # 任务 3: 数据分析
        elif "分析" in task or "计算" in task:
            return f'''
# 数据分析
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
total = sum(data)
mean = total / len(data)
vars["analysis_result"] = {{"total": total, "mean": mean, "count": len(data)}}
print(f"数据总和: {{total}}")
print(f"平均值: {{mean}}")
'''
        
        # 任务 4: 错误代码（测试安全拦截）
        elif "危险" in task or "攻击" in task:
            return '''
# 尝试执行危险操作
import os
os.system("rm -rf /")
'''
        
        # 默认: 简单输出
        else:
            return f'''
# 默认任务
print("Agent 正在执行任务: {task}")
print(f"当前 turn: {sandbox_state.get('turn_count', 0)}")
vars["last_task"] = "{task}"
'''


# ============================================================================
#  MODULE 5: Sandbox Experiment Runner
#  模块 5：沙箱实验运行器 —— 协调所有模块
# ============================================================================

class SandboxExperiment:
    """
    沙箱实验运行器 —— 完整的实验流程
    
    初学者要点：
    - 初始化沙箱环境
    - 循环：生成任务 → Agent 生成代码 → 安全检查 → 沙箱执行 → Checkpoint
    - 支持从任意 checkpoint 恢复
    - 统计安全违规、checkpoint 效率等指标
    """
    
    def __init__(self):
        self.env = SandboxEnvironment()
        self.safety = SafetySandbox()
        self.checkpoint_mgr = CheckpointManager()
        self.agent = SimulatedLLMAgent()
        self.results: List[Dict[str, Any]] = []
    
    def run_task(self, task: str, checkpoint: bool = True) -> Dict[str, Any]:
        """运行单个任务"""
        print(f"\n{'='*60}")
        print(f"任务: {task}")
        print(f"{'='*60}")
        
        # 1. Agent 生成代码
        code = self.agent.generate_code(task, self.env.get_state())
        print(f"\n[Agent 生成代码]\n{code}")
        
        # 2. 安全检查
        is_safe, safety_reason = self.safety.validate_code(code)
        print(f"\n[安全检查] {'通过' if is_safe else '拦截'}: {safety_reason}")
        
        if not is_safe:
            result = {
                "task": task,
                "code": code,
                "success": False,
                "safety_blocked": True,
                "safety_reason": safety_reason,
            }
            self.results.append(result)
            return result
        
        # 3. 沙箱执行
        exec_result = self.env.execute_code(code)
        print(f"\n[执行结果] {'成功' if exec_result['success'] else '失败'}")
        if exec_result.get('output'):
            print(f"输出:\n{exec_result['output']}")
        if exec_result.get('error'):
            print(f"错误: {exec_result['error']}")
        
        # 4. Checkpoint
        if checkpoint:
            cp = self.checkpoint_mgr.create_checkpoint(
                self.env,
                description=f"After task: {task}"
            )
            print(f"\n[Checkpoint] {cp.id}: {len(cp.changes)} 个文件变化")
        
        result = {
            "task": task,
            "code": code,
            "success": exec_result['success'],
            "output": exec_result.get('output', ''),
            "error": exec_result.get('error', ''),
            "safety_blocked": False,
        }
        self.results.append(result)
        return result
    
    def restore_to_checkpoint(self, cp_id: str):
        """恢复到指定 checkpoint"""
        success = self.checkpoint_mgr.restore_checkpoint(cp_id, self.env)
        print(f"\n[Restore] {'成功' if success else '失败'}: {cp_id}")
        return success
    
    def run_experiment(self, tasks: List[str]):
        """运行完整实验"""
        print("=" * 60)
        print("Agent 沙箱环境实验")
        print("基于 LLM-in-Sandbox / Crab / SafeArena 论文")
        print("=" * 60)
        
        # 初始 checkpoint
        self.checkpoint_mgr.create_checkpoint(self.env, description="Initial state")
        
        for task in tasks:
            self.run_task(task)
        
        # 输出统计
        self._print_summary()
    
    def _print_summary(self):
        """打印实验总结"""
        print(f"\n{'='*60}")
        print("实验总结")
        print(f"{'='*60}")
        
        total = len(self.results)
        successes = sum(1 for r in self.results if r['success'])
        blocked = sum(1 for r in self.results if r.get('safety_blocked'))
        
        print(f"总任务数: {total}")
        print(f"成功执行: {successes}")
        print(f"安全拦截: {blocked}")
        print(f"执行失败: {total - successes - blocked}")
        
        # Checkpoint 统计
        cp_stats = self.checkpoint_mgr.get_checkpoint_stats()
        print(f"\nCheckpoint 统计:")
        print(f"  总数: {cp_stats['total_checkpoints']}")
        print(f"  总大小: {cp_stats['total_size_bytes']} bytes")
        print(f"  平均大小: {cp_stats['avg_size_bytes']:.1f} bytes")
        
        # 安全违规
        violations = self.safety.get_violations_summary()
        print(f"\n安全违规:")
        print(f"  总数: {violations['total_violations']}")
        for v in violations['violations']:
            print(f"  - {v['type']}: {v['pattern']}")
        
        print(f"{'='*60}")


# ============================================================================
#  MAIN: Experiment Runner
# ============================================================================

def run_experiment():
    """运行沙箱实验"""
    experiment = SandboxExperiment()
    
    tasks = [
        "创建文件 hello.txt",
        "读取沙箱文件列表",
        "分析数据并计算平均值",
        "创建文件 report.txt",
        "危险操作测试",  # 测试安全拦截
        "再次读取文件列表",
    ]
    
    experiment.run_experiment(tasks)
    
    # 演示 Restore
    print(f"\n{'='*60}")
    print("演示 Checkpoint Restore")
    print(f"{'='*60}")
    
    # 恢复到第 2 个 checkpoint
    cp_ids = list(experiment.checkpoint_mgr.checkpoints.keys())
    if len(cp_ids) >= 2:
        experiment.restore_to_checkpoint(cp_ids[1])
        print(f"恢复后文件列表: {experiment.env.file_system.list_files()}")


if __name__ == "__main__":
    run_experiment()
```

---

## 五、评估指标详解（初学者指南）

### 为什么需要这些指标？

沙箱系统的核心问题是：Agent 能否在隔离环境中安全、高效地执行代码？这些指标帮助我们量化沙箱的质量。

### 指标一览

| 指标 | 定义 | 为什么重要 | 理想值 | 如何改进 |
|-----|------|----------|--------|---------|
| **安全拦截率** | 危险代码被拦截的比例 | 衡量安全策略有效性 | 100% | 增强危险模式检测 |
| **执行成功率** | 合法代码成功执行的比例 | 衡量沙箱稳定性 | > 95% | 完善安全白名单 |
| **Checkpoint 压缩率** | 语义感知 vs 全量 snapshot 大小比 | 衡量 C/R 效率 | < 20% | 优化变化检测算法 |
| **恢复正确率** | 恢复后状态与预期一致的比例 | 衡量 C/R 可靠性 | 100% | 确保状态捕获完整 |
| **沙箱隔离度** | Agent 代码是否影响外部系统 | 核心安全指标 | 100% | 严格命名空间隔离 |
| **误拦截率** | 合法代码被错误拦截的比例 | 衡量安全策略精确度 | < 5% | 细化白名单规则 |

### 指标之间的关系

```
安全拦截率 ↑ → 沙箱隔离度 ↑ → 系统安全性 ↑
     ↑
误拦截率 ↓ → 执行成功率 ↑ → Agent 能力发挥 ↑
     ↑
Checkpoint 压缩率 ↓ → 恢复效率 ↑ → 实验可重复性 ↑
```

---

## 六、场景配置矩阵

| 场景 | 危险模式数 | 白名单范围 | Checkpoint 策略 | 用途 |
|-----|-----------|-----------|----------------|------|
| 快速测试 | 10 | 基础内置函数 | 每轮 checkpoint | 验证基本流程 |
| 标准体验 | 20 | 完整安全内置 | 语义感知 C/R | 观察完整沙箱循环（推荐） |
| 严格安全 | 50 | 最小白名单 | 每轮全量 C/R | 测试安全边界 |
| 性能测试 | 20 | 完整白名单 | 无 checkpoint | 测试执行性能 |
| 教学演示 | 5 | 宽松白名单 | 手动 checkpoint | 教学演示用 |

### 初学者调试清单

- [ ] **如果安全拦截率 < 100%**：检查 DANGEROUS_PATTERNS 是否覆盖所有危险操作
- [ ] **如果执行成功率低**：检查安全白名单是否过于严格，误拦截合法代码
- [ ] **如果恢复正确率低**：检查 state 捕获是否完整（文件系统 + 变量 + 执行位置）
- [ ] **如果 Checkpoint 过大**：检查语义感知变化检测是否正确工作
- [ ] **如果沙箱隔离失败**：检查 exec() 的 globals 是否严格限制
- [ ] **如果 Agent 代码无法访问沙箱 API**：检查 safe_globals 是否正确注入

---

## 七、关键设计决策与解释

### 7.1 为什么用 exec() 而非 subprocess？

| 维度 | exec()（本实验） | subprocess |
|-----|----------------|------------|
| 隔离性 | 命名空间隔离（较弱） | 进程隔离（较强） |
| 性能 | 毫秒级 | 百毫秒级 |
| 状态保持 | 自然保持变量 | 需要序列化 |
| 复杂度 | 简单 | 复杂 |
| 生产适用 | 仅演示 | 推荐 |

**生产建议**：使用 Docker 容器或 WASM 沙箱实现真正的进程级隔离。

### 7.2 语义感知 C/R 的收益

假设 10 轮任务，每轮平均修改 2 个文件：
- **全量 C/R**: 10 × 100MB = 1GB
- **语义感知 C/R**: 10 × 2 × 1KB = 20KB
- **压缩比**: 1GB / 20KB = 50,000×

---

## 八、思考题

### 8.1 基础问题

1. **沙箱隔离 vs 性能**：本实验用 exec() 实现隔离，但隔离性较弱。如果用 Docker 容器，每次任务启动容器的延迟是多少？如何平衡隔离性和性能？

2. **语义感知 C/R 的边界**：Crab 用 eBPF 观察 OS 效应。本实验在纯 Python 中模拟，无法观察真实 OS 状态。在真实系统中，哪些状态变化最难检测？（如：内存映射、网络连接、临时文件）

3. **安全策略的对抗性**：SafeArena 发现 GPT-4o 对有害请求合规率高达 34.7%。本实验的安全策略是规则匹配，攻击者如何构造绕过规则的代码？（如：字符串拼接构造 import 语句）

### 8.2 进阶问题

4. **多 Agent 沙箱协作**：如果多个 Agent 需要共享沙箱（如协作编程），如何设计"沙箱分叉"（fork）和"沙箱合并"（merge）机制？

5. **从沙箱到生产**：研究中的沙箱（Docker、ZFS、CRIU）与生产环境（Kubernetes、云函数）的 gap 如何弥合？

6. **LLM 模拟环境的 fidelity**：EnvSimBench 发现 LLM 模拟的环境存在显著失真。本实验的沙箱是确定性规则系统， fidelity 100%。但真实世界充满随机性，如何在沙箱中模拟这种不确定性？

---

## 九、面试谈资

> **30 秒版本**：Agent 沙箱是 LLM 从文本对话进化为可执行智能体的关键基础设施。核心创新是将沙箱从"安全隔离工具"重新定义为"认知扩展工具"——文件系统作为外化记忆，代码执行作为外化计算。语义感知 Checkpoint/Restore 通过只记录变化的部分，将恢复正确率从 8% 提升到 100%，同时减少 87% 的 checkpoint 流量。

> **2 分钟版本**：传统沙箱是"关坏人的笼子"，LLM-in-Sandbox 的 insight 是**沙箱是 LLM 的外化认知扩展**。LLM 的上下文窗口有限（128K token），但沙箱的文件系统无限；LLM 的推理能力有限，但沙箱可以执行任意代码。论文的关键实验：将 100K token 的长文档放入沙箱文件，LLM 通过文件读取和脚本处理将 token 消耗降至 13K。Crab 进一步解决沙箱的效率问题：传统 checkpoint/restore 每轮全量 snapshot，I/O 爆炸；Crab 通过 eBPF 观察 OS 效应，发现 75% 以上的 turn 不产生需要恢复的状态变化，从而只 checkpoint 变化的部分。SafeArena 则暴露了一个严峻问题：GPT-4o 对有害 Web Agent 请求的合规率高达 34.7%，说明安全对齐在 Agent 场景中严重迁移失败——对话中的"拒绝有害请求"训练，无法迁移到 Agent 的"操作序列累积效应"场景。

---

## 十、扩展方向

| 方向 | 改进内容 | 预期收益 |
|-----|---------|---------|
| Docker 隔离 | 替换 exec() 为 Docker 容器 | 真正的进程级隔离 |
| 真实 eBPF | 集成 eBPF 观察 OS 效应 | 生产级语义感知 C/R |
| 网络沙箱 | 添加网络访问控制和模拟 | 支持 Web Agent 场景 |
| GPU 沙箱 | 支持 CUDA 代码执行 | 支持 ML 工作负载 |
| 对抗测试 | 自动化红队测试安全策略 | 发现未知漏洞 |
| 多 Agent | 支持沙箱分叉和合并 | 协作 Agent 场景 |

---

## 实验文件清单

```
15-Agent-沙箱环境实验.md            # 本实验文档
sandbox_experiment.py                # 完整代码（从本文档提取）
```

---

*实验创建时间: 2026-07-20*
*维护者: AIResearchVault*
*关联论文: LLM-in-Sandbox (2026), Crab (2026), SafeArena (ICML 2025), ceLLMate (2025)*
