# Tool Calling 实验：结构化工具调用与 LLM 交互

**实验编号**: W30-2026-07-20  
**实验日期**: 2026-07-20  
**实验类型**: 工具调用 / API 集成  
**难度等级**: 初级  
**预计耗时**: 45-60 分钟  

---

## 1. 实验目标

本实验旨在帮助初学者理解并实践 **Tool Calling（工具调用）** 的核心概念与实现方法。通过本实验，你将学会：

1. 理解 Tool Calling 的基本原理与架构设计
2. 掌握如何定义和注册自定义工具（函数）
3. 学习构建工具描述 schema（JSON Schema 格式）
4. 实现 LLM 与外部工具的结构化交互流程
5. 处理工具调用结果并整合回对话上下文
6. 理解 `function_calling` 与 `tool_calling` 的区别与演进

---

## 2. 前置知识

在开始本实验之前，建议具备以下基础知识：

- **Python 基础**: 熟悉函数定义、字典操作、异常处理
- **HTTP API 基础**: 了解 RESTful API 的基本概念
- **JSON 格式**: 熟悉 JSON 数据结构
- **LLM 基础概念**: 了解大语言模型的基本工作原理
- **异步编程基础**（可选）: 了解 `async/await` 语法

---

## 3. 核心概念

### 3.1 什么是 Tool Calling

**Tool Calling** 是一种让大语言模型（LLM）能够调用外部函数或工具的机制。通过这种方式，LLM 可以：

- 获取实时信息（天气、股价、新闻等）
- 执行计算任务（数学运算、数据分析等）
- 与外部系统交互（数据库查询、API 调用等）
- 执行特定操作（发送邮件、创建日历事件等）

### 3.2 Tool Calling 的工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   用户输入   │────▶│    LLM      │────▶│  工具选择    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  执行工具    │
                                        │  (本地/远程) │
                                        └──────┬──────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   最终回复   │◀────│    LLM      │◀────│  返回结果    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 3.3 关键术语

| 术语 | 英文 | 说明 |
|------|------|------|
| 工具 | Tool | LLM 可调用的外部函数或服务 |
| 工具描述 | Tool Description | 描述工具功能、参数、返回值的元数据 |
| 工具调用 | Tool Call | LLM 决定调用某个工具的请求 |
| 工具结果 | Tool Result | 工具执行后返回的数据 |
| Schema | JSON Schema | 定义工具参数结构的规范格式 |

---

## 4. 实验环境准备

### 4.1 依赖安装

```bash
pip install openai>=1.0.0
pip install python-dotenv
```

### 4.2 环境变量配置

创建 `.env` 文件：

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 4.3 项目结构

```
tool_calling/
├── .env
├── tools/
│   ├── __init__.py
│   ├── weather_tool.py
│   ├── calculator_tool.py
│   └── search_tool.py
├── tool_registry.py
├── tool_executor.py
├── chat_session.py
└── main.py
```

---

## 5. 实验内容

### 5.1 基础工具定义

#### 5.1.1 创建工具注册表

**文件**: `tool_registry.py`

```python
"""
Tool Registry - 工具注册与管理模块

本模块提供工具的注册、查找和描述生成功能。
"""

import inspect
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class ToolInfo:
    """工具信息数据类"""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]
    required_params: list


class ToolRegistry:
    """工具注册表类"""
    
    def __init__(self):
        self._tools: Dict[str, ToolInfo] = {}
    
    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        注册一个新工具
        
        Args:
            name: 工具名称（唯一标识）
            description: 工具功能描述
            func: 工具对应的函数
            parameters: 参数定义（JSON Schema 格式）
        """
        if parameters is None:
            parameters = self._infer_parameters(func)
        
        required = [
            key for key, value in parameters.get("properties", {}).items()
            if value.get("required", False)
        ]
        
        self._tools[name] = ToolInfo(
            name=name,
            description=description,
            function=func,
            parameters=parameters,
            required_params=required
        )
        print(f"[ToolRegistry] 已注册工具: {name}")
    
    def _infer_parameters(self, func: Callable) -> Dict[str, Any]:
        """
        从函数签名推断参数结构
        
        这是一个简化版本，实际项目中建议使用更完善的类型推断
        """
        sig = inspect.signature(func)
        properties = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_info = {"type": "string", "description": f"参数 {param_name}"}
            
            if param.default is not inspect.Parameter.empty:
                param_info["default"] = param.default
            else:
                param_info["required"] = True
            
            properties[param_name] = param_info
        
        return {
            "type": "object",
            "properties": properties
        }
    
    def get_tool(self, name: str) -> Optional[ToolInfo]:
        """根据名称获取工具信息"""
        return self._tools.get(name)
    
    def list_tools(self) -> list:
        """列出所有已注册的工具"""
        return list(self._tools.keys())
    
    def get_tool_descriptions(self) -> list:
        """
        获取所有工具的 OpenAI 格式描述
        
        Returns:
            符合 OpenAI Tool 格式的描述列表
        """
        descriptions = []
        for tool_info in self._tools.values():
            descriptions.append({
                "type": "function",
                "function": {
                    "name": tool_info.name,
                    "description": tool_info.description,
                    "parameters": tool_info.parameters
                }
            })
        return descriptions
    
    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        执行指定工具
        
        Args:
            name: 工具名称
            arguments: 调用参数
            
        Returns:
            工具执行结果
            
        Raises:
            ValueError: 工具不存在
            Exception: 工具执行错误
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"工具 '{name}' 未注册")
        
        try:
            result = tool.function(**arguments)
            return result
        except Exception as e:
            raise Exception(f"工具 '{name}' 执行失败: {str(e)}")


# 全局注册表实例
registry = ToolRegistry()


def tool(name: str, description: str):
    """
    工具装饰器 - 简化工具注册
    
    使用示例:
        @tool("get_weather", "获取指定城市的天气信息")
        def get_weather(city: str) -> str:
            return f"{city} 的天气是晴天"
    """
    def decorator(func: Callable) -> Callable:
        registry.register(name, description, func)
        return func
    return decorator
```

#### 5.1.2 创建具体工具

**文件**: `tools/weather_tool.py`

```python
"""
Weather Tool - 天气查询工具

模拟天气查询功能，实际项目中可替换为真实 API
"""

from tool_registry import tool
import random


# 模拟天气数据库
WEATHER_DATA = {
    "北京": {"temperature": 25, "condition": "晴", "humidity": 45},
    "上海": {"temperature": 28, "condition": "多云", "humidity": 65},
    "广州": {"temperature": 32, "condition": "雷阵雨", "humidity": 80},
    "深圳": {"temperature": 31, "condition": "阴", "humidity": 75},
    "杭州": {"temperature": 26, "condition": "小雨", "humidity": 70},
}


@tool("get_weather", "获取指定城市的当前天气信息，包括温度、天气状况和湿度")
def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息
    
    Args:
        city: 城市名称（中文）
        
    Returns:
        格式化的天气信息字符串
    """
    if city in WEATHER_DATA:
        data = WEATHER_DATA[city]
        return (
            f"【{city}天气】\n"
            f"温度: {data['temperature']}°C\n"
            f"状况: {data['condition']}\n"
            f"湿度: {data['humidity']}%"
        )
    else:
        # 为未定义的城市生成随机天气
        temp = random.randint(15, 35)
        conditions = ["晴", "多云", "阴", "小雨"]
        condition = random.choice(conditions)
        humidity = random.randint(30, 90)
        
        return (
            f"【{city}天气】\n"
            f"温度: {temp}°C\n"
            f"状况: {condition}\n"
            f"湿度: {humidity}%\n"
            f"(注: 该城市使用模拟数据)"
        )


@tool("get_temperature", "获取指定城市的当前温度")
def get_temperature(city: str) -> str:
    """获取指定城市的温度"""
    if city in WEATHER_DATA:
        return f"{city} 当前温度: {WEATHER_DATA[city]['temperature']}°C"
    return f"{city} 当前温度: {random.randint(15, 35)}°C"
```

**文件**: `tools/calculator_tool.py`

```python
"""
Calculator Tool - 计算器工具

提供基础数学运算功能
"""

from tool_registry import tool
import math


@tool("calculate", "执行基础数学运算，支持加减乘除和幂运算")
def calculate(expression: str) -> str:
    """
    执行数学表达式计算
    
    Args:
        expression: 数学表达式字符串，如 "2 + 3 * 4"
        
    Returns:
        计算结果
        
    Note:
        出于安全考虑，仅支持基础运算符: +, -, *, /, **, (, )
    """
    try:
        # 安全评估：仅允许数字和基础运算符
        allowed_chars = set("0123456789+-*/.() **")
        if not all(c in allowed_chars for c in expression.replace(" ", "")):
            return "错误: 表达式包含非法字符"
        
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@tool("sqrt", "计算一个数的平方根")
def sqrt(number: float) -> str:
    """
    计算平方根
    
    Args:
        number: 非负实数
        
    Returns:
        平方根结果
    """
    if number < 0:
        return "错误: 不能计算负数的平方根"
    return f"√{number} = {math.sqrt(number):.4f}"


@tool("factorial", "计算一个正整数的阶乘")
def factorial(n: int) -> str:
    """
    计算阶乘
    
    Args:
        n: 非负整数
        
    Returns:
        n! 的结果
    """
    if n < 0:
        return "错误: 阶乘仅支持非负整数"
    if n > 20:
        return "错误: 数字过大，请输入 0-20 之间的整数"
    
    result = math.factorial(n)
    return f"{n}! = {result}"
```

**文件**: `tools/search_tool.py`

```python
"""
Search Tool - 模拟搜索工具

模拟网络搜索功能，返回预设的知识库结果
"""

from tool_registry import tool
from typing import List, Dict


# 模拟知识库
KNOWLEDGE_BASE = {
    "python": {
        "title": "Python 编程语言",
        "summary": "Python 是一种高级、解释型、通用的编程语言...",
        "url": "https://docs.python.org/3/"
    },
    "machine learning": {
        "title": "机器学习简介",
        "summary": "机器学习是人工智能的一个分支，专注于让计算机从数据中学习...",
        "url": "https://scikit-learn.org/"
    },
    "tool calling": {
        "title": "Tool Calling 技术",
        "summary": "Tool Calling 允许 LLM 调用外部工具来扩展能力...",
        "url": "https://platform.openai.com/docs/guides/function-calling"
    },
    "restir": {
        "title": "ReSTIR 全局光照算法",
        "summary": "ReSTIR (Reservoir-based Spatio-Temporal Importance Resampling) 是一种实时全局光照算法...",
        "url": "https://graphics.cs.utah.edu/research/projects/restir/"
    }
}


@tool("search", "在知识库中搜索相关信息")
def search(query: str, max_results: int = 3) -> str:
    """
    搜索知识库
    
    Args:
        query: 搜索关键词
        max_results: 最大返回结果数（默认 3）
        
    Returns:
        格式化的搜索结果
    """
    query_lower = query.lower()
    results = []
    
    for key, value in KNOWLEDGE_BASE.items():
        if query_lower in key or query_lower in value["summary"].lower():
            results.append(value)
    
    if not results:
        return f"未找到与 '{query}' 相关的结果"
    
    results = results[:max_results]
    
    output = f"【搜索结果: {query}】\n"
    for i, result in enumerate(results, 1):
        output += f"\n{i}. {result['title']}\n"
        output += f"   {result['summary']}\n"
        output += f"   链接: {result['url']}\n"
    
    return output


@tool("get_documentation", "获取指定技术主题的文档链接")
def get_documentation(topic: str) -> str:
    """
    获取技术文档链接
    
    Args:
        topic: 技术主题名称
        
    Returns:
        文档链接和简介
    """
    docs = {
        "openai": "https://platform.openai.com/docs/",
        "python": "https://docs.python.org/3/",
        "numpy": "https://numpy.org/doc/",
        "pytorch": "https://pytorch.org/docs/",
    }
    
    if topic.lower() in docs:
        return f"{topic} 文档: {docs[topic.lower()]}"
    
    return f"未找到 '{topic}' 的文档链接，请尝试: {', '.join(docs.keys())}"
```

### 5.2 工具执行器

**文件**: `tool_executor.py`

```python
"""
Tool Executor - 工具执行模块

处理 LLM 返回的 tool_call 请求，执行对应工具并返回结果
"""

import json
from typing import Dict, Any, Optional
from tool_registry import registry


class ToolExecutor:
    """工具执行器"""
    
    def __init__(self, tool_registry=None):
        self.registry = tool_registry or registry
    
    def execute_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个工具调用
        
        Args:
            tool_call: OpenAI 格式的 tool_call 对象
            
        Returns:
            工具执行结果，格式化为 tool 消息
        """
        tool_name = tool_call["function"]["name"]
        tool_id = tool_call["id"]
        
        try:
            # 解析参数
            arguments = json.loads(tool_call["function"]["arguments"])
            
            print(f"[ToolExecutor] 执行工具: {tool_name}")
            print(f"[ToolExecutor] 参数: {arguments}")
            
            # 执行工具
            result = self.registry.execute(tool_name, arguments)
            
            print(f"[ToolExecutor] 结果: {result}")
            
            return {
                "tool_call_id": tool_id,
                "role": "tool",
                "name": tool_name,
                "content": str(result)
            }
            
        except json.JSONDecodeError as e:
            error_msg = f"参数解析错误: {str(e)}"
            print(f"[ToolExecutor] {error_msg}")
            return {
                "tool_call_id": tool_id,
                "role": "tool",
                "name": tool_name,
                "content": error_msg
            }
            
        except Exception as e:
            error_msg = f"执行错误: {str(e)}"
            print(f"[ToolExecutor] {error_msg}")
            return {
                "tool_call_id": tool_id,
                "role": "tool",
                "name": tool_name,
                "content": error_msg
            }
    
    def execute_tool_calls(self, tool_calls: list) -> list:
        """
        批量执行工具调用
        
        Args:
            tool_calls: tool_call 对象列表
            
        Returns:
            工具结果消息列表
        """
        results = []
        for tool_call in tool_calls:
            result = self.execute_tool_call(tool_call)
            results.append(result)
        return results


# 便捷函数
def execute_tool(tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """快捷执行单个工具调用"""
    executor = ToolExecutor()
    return executor.execute_tool_call(tool_call)
```

### 5.3 对话会话管理

**文件**: `chat_session.py`

```python
"""
Chat Session - 对话会话管理

管理多轮对话，处理工具调用的完整流程
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from tool_registry import registry
from tool_executor import ToolExecutor

# 加载环境变量
load_dotenv()


class ChatSession:
    """
    对话会话类
    
    管理对话历史，处理工具调用循环
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        system_prompt: Optional[str] = None,
        max_tool_iterations: int = 5
    ):
        """
        初始化对话会话
        
        Args:
            model: 使用的模型名称
            system_prompt: 系统提示词
            max_tool_iterations: 最大工具调用轮数（防止无限循环）
        """
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.model = model
        self.max_tool_iterations = max_tool_iterations
        self.executor = ToolExecutor()
        
        # 初始化对话历史
        self.messages: List[Dict[str, Any]] = []
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def send_message(self, user_message: str) -> str:
        """
        发送用户消息并获取回复
        
        完整处理流程：
        1. 添加用户消息到历史
        2. 调用 LLM
        3. 如果 LLM 请求工具调用，执行工具并继续对话
        4. 返回最终回复
        
        Args:
            user_message: 用户输入消息
            
        Returns:
            助手的最终回复文本
        """
        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        # 获取可用工具描述
        tools = registry.get_tool_descriptions()
        
        # 工具调用循环
        for iteration in range(self.max_tool_iterations):
            print(f"\n[ChatSession] 对话轮次 {iteration + 1}")
            
            # 调用 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )
            
            assistant_message = response.choices[0].message
            
            # 检查是否有工具调用
            if not assistant_message.tool_calls:
                # 没有工具调用，直接返回内容
                content = assistant_message.content or ""
                self.messages.append({
                    "role": "assistant",
                    "content": content
                })
                return content
            
            # 处理工具调用
            print(f"[ChatSession] LLM 请求工具调用")
            
            # 添加 assistant 的 tool_call 消息到历史
            self.messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            
            # 执行工具
            tool_results = self.executor.execute_tool_calls(
                [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            )
            
            # 添加工具结果到历史
            for result in tool_results:
                self.messages.append(result)
        
        # 达到最大迭代次数
        return "错误: 工具调用次数超过最大限制"
    
    def get_history(self) -> List[Dict[str, Any]]:
        """获取完整对话历史"""
        return self.messages.copy()
    
    def clear_history(self) -> None:
        """清空对话历史（保留 system prompt）"""
        if self.messages and self.messages[0]["role"] == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []
    
    def print_history(self) -> None:
        """打印对话历史（用于调试）"""
        print("\n" + "="*50)
        print("对话历史")
        print("="*50)
        for msg in self.messages:
            role = msg["role"]
            content = msg.get("content", "")
            
            if role == "tool":
                print(f"\n[{role}] 工具: {msg.get('name', 'unknown')}")
                print(f"结果: {content[:200]}...")
            elif "tool_calls" in msg:
                print(f"\n[{role}] 工具调用请求:")
                for tc in msg["tool_calls"]:
                    print(f"  - {tc['function']['name']}")
            else:
                print(f"\n[{role}]")
                print(content)
        print("\n" + "="*50)


def create_default_session() -> ChatSession:
    """创建默认配置的对话会话"""
    system_prompt = """你是一个有用的 AI 助手。你可以使用以下工具来帮助用户:

1. get_weather - 获取天气信息
2. get_temperature - 获取温度
3. calculate - 执行数学计算
4. sqrt - 计算平方根
5. factorial - 计算阶乘
6. search - 搜索知识库
7. get_documentation - 获取文档链接

当需要获取实时信息或执行计算时，请使用相应工具。
请用中文回复用户。"""
    
    return ChatSession(system_prompt=system_prompt)
```

### 5.4 主程序

**文件**: `main.py`

```python
"""
Tool Calling 实验主程序

演示完整的工具调用流程
"""

import sys
from chat_session import create_default_session

# 导入所有工具以完成注册
from tools import weather_tool
from tools import calculator_tool
from tools import search_tool


def print_banner():
    """打印欢迎横幅"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           Tool Calling 实验 - 交互式演示                  ║
╠══════════════════════════════════════════════════════════╣
║  可用功能:                                                ║
║    • 天气查询: "北京天气怎么样？"                          ║
║    • 数学计算: "计算 15 * 23 + 7"                         ║
║    • 知识搜索: "搜索 Python 相关资料"                      ║
║    • 文档链接: "给我 PyTorch 文档"                         ║
╠══════════════════════════════════════════════════════════╣
║  命令: /history - 查看对话历史                            ║
║        /clear   - 清空对话                                ║
║        /quit    - 退出程序                                ║
╚══════════════════════════════════════════════════════════╝
    """)


def main():
    """主函数"""
    print_banner()
    
    # 创建对话会话
    session = create_default_session()
    
    print("[系统] 会话已初始化，请输入消息...\n")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("用户: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input == "/quit":
                print("\n[系统] 再见！")
                break
            
            elif user_input == "/clear":
                session.clear_history()
                print("[系统] 对话历史已清空\n")
                continue
            
            elif user_input == "/history":
                session.print_history()
                continue
            
            # 发送消息并获取回复
            print("\n[系统] 正在处理...")
            response = session.send_message(user_input)
            
            print(f"\n助手: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n[系统] 用户中断，退出程序")
            break
        except Exception as e:
            print(f"\n[错误] {str(e)}\n")


if __name__ == "__main__":
    main()
```

**文件**: `tools/__init__.py`

```python
"""
Tools Package - 工具模块包

导入此包会自动注册所有工具
"""

# 工具模块会在导入时通过装饰器自动注册
```

---

## 6. 运行实验

### 6.1 启动程序

```bash
cd tool_calling
python main.py
```

### 6.2 示例对话

```
用户: 北京今天天气怎么样？

[系统] 正在处理...
[ChatSession] 对话轮次 1
[ChatSession] LLM 请求工具调用
[ToolExecutor] 执行工具: get_weather
[ToolExecutor] 参数: {'city': '北京'}
[ToolExecutor] 结果: 【北京天气】
温度: 25°C
状况: 晴
湿度: 45%

助手: 北京今天的天气情况如下：
• 温度: 25°C
• 天气状况: 晴
• 湿度: 45%

天气不错，适合外出活动！

用户: 那上海呢？

[系统] 正在处理...
助手: 上海今天的天气情况如下：
• 温度: 28°C
• 天气状况: 多云
• 湿度: 65%

比北京稍微暖和一些，湿度也更高。

用户: 帮我计算 (15 + 23) * 4 的平方根

[系统] 正在处理...
[ChatSession] 对话轮次 1
[ChatSession] LLM 请求工具调用
[ToolExecutor] 执行工具: calculate
[ToolExecutor] 参数: {'expression': '(15 + 23) * 4'}
[ToolExecutor] 结果: 计算结果: 152
[ChatSession] 对话轮次 2
[ChatSession] LLM 请求工具调用
[ToolExecutor] 执行工具: sqrt
[ToolExecutor] 参数: {'number': 152}
[ToolExecutor] 结果: √152 = 12.3288

助手: 计算过程如下：
1. (15 + 23) * 4 = 152
2. √152 ≈ 12.3288

所以最终结果是约 12.33。
```

---

## 7. 进阶内容

### 7.1 工具调用流程详解

```python
# 完整的工具调用流程示例（非交互式）
from openai import OpenAI
import json
from tool_registry import registry

client = OpenAI()

# 定义消息
messages = [
    {"role": "user", "content": "深圳天气如何？"}
]

# 获取工具描述
tools = registry.get_tool_descriptions()

# 第一步：调用 LLM，传入工具描述
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

response_message = response.choices[0].message

# 检查是否需要工具调用
if response_message.tool_calls:
    # 第二步：将 assistant 的回复加入对话历史
    messages.append({
        "role": "assistant",
        "content": response_message.content or "",
        "tool_calls": [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            }
            for tc in response_message.tool_calls
        ]
    })
    
    # 第三步：执行工具调用
    for tool_call in response_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # 执行工具
        result = registry.execute(function_name, function_args)
        
        # 第四步：将工具结果加入对话历史
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": str(result)
        })
    
    # 第五步：再次调用 LLM，传入工具结果
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    print(final_response.choices[0].message.content)
```

### 7.2 强制工具调用

```python
# 强制使用特定工具
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "北京天气"}],
    tools=tools,
    tool_choice={
        "type": "function",
        "function": {"name": "get_weather"}
    }
)

# 强制不使用工具
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好"}],
    tools=tools,
    tool_choice="none"
)
```

### 7.3 并行工具调用

现代 LLM 支持在一次响应中请求多个工具调用：

```python
# 用户查询多个城市的天气
messages = [
    {"role": "user", "content": "北京和上海哪个更热？"}
]

# LLM 可能同时请求两个 get_weather 调用
# 需要并行执行并收集结果
```

### 7.4 错误处理最佳实践

```python
class RobustToolExecutor:
    """健壮的工具执行器"""
    
    def execute_with_retry(self, tool_call, max_retries=3):
        """带重试的工具执行"""
        for attempt in range(max_retries):
            try:
                return self.execute_tool_call(tool_call)
            except Exception as e:
                if attempt == max_retries - 1:
                    return {
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "content": f"工具执行失败（已重试{max_retries}次）: {str(e)}"
                    }
                print(f"[重试] 第 {attempt + 1} 次尝试失败，正在重试...")
    
    def execute_with_timeout(self, tool_call, timeout_seconds=10):
        """带超时的工具执行"""
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.execute_tool_call, tool_call)
            try:
                return future.result(timeout=timeout_seconds)
            except concurrent.futures.TimeoutError:
                return {
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "content": "工具执行超时"
                }
```

---

## 8. 实验练习

### 练习 1：添加新工具

创建一个 `datetime_tool.py`，实现以下功能：

```python
from tool_registry import tool
from datetime import datetime
import pytz


@tool("get_current_time", "获取当前时间")
def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取指定时区的当前时间"""
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    return f"当前时间 ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"


@tool("convert_timezone", "转换时区时间")
def convert_timezone(time_str: str, from_tz: str, to_tz: str) -> str:
    """将时间从一个时区转换到另一个时区"""
    # 实现时区转换逻辑
    pass
```

### 练习 2：工具链调用

实现一个需要多个工具协作的场景：

```python
# 场景：查询天气并给出穿衣建议
# 1. 调用 get_weather 获取天气
# 2. 根据温度调用自定义的 clothing_advice 工具
# 3. 整合结果返回给用户

@tool("clothing_advice", "根据温度给出穿衣建议")
def clothing_advice(temperature: float) -> str:
    """根据温度推荐穿衣"""
    if temperature < 10:
        return "建议穿羽绒服或厚外套"
    elif temperature < 20:
        return "建议穿夹克或薄外套"
    elif temperature < 28:
        return "建议穿短袖或薄长袖"
    else:
        return "建议穿短袖，注意防晒"
```

### 练习 3：工具参数验证

为工具注册表添加参数验证功能：

```python
def validate_parameters(self, tool_name: str, arguments: dict) -> tuple:
    """
    验证工具参数
    
    Returns:
        (is_valid: bool, error_message: str)
    """
    tool = self.get_tool(tool_name)
    if not tool:
        return False, f"工具 '{tool_name}' 不存在"
    
    schema = tool.parameters
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    
    # 检查必需参数
    for param in required:
        if param not in arguments:
            return False, f"缺少必需参数: {param}"
    
    # 检查参数类型
    for param, value in arguments.items():
        if param in properties:
            expected_type = properties[param].get("type")
            if not self._check_type(value, expected_type):
                return False, f"参数 '{param}' 类型错误，期望 {expected_type}"
    
    return True, ""
```

---

## 9. 常见问题

### Q1: Tool Calling 和 Function Calling 有什么区别？

**A**: Function Calling 是 OpenAI 早期版本中的概念，Tool Calling 是其演进版本。主要区别：

- **Function Calling**: 使用 `functions` 参数，直接返回函数调用
- **Tool Calling**: 使用 `tools` 参数，支持更丰富的工具类型（不仅是函数）

新代码应使用 Tool Calling API。

### Q2: 如何处理工具执行错误？

**A**: 最佳实践：

1. 将错误信息作为 tool 消息返回给 LLM
2. LLM 可以根据错误信息决定重试或调整参数
3. 设置最大重试次数防止无限循环

### Q3: 工具描述应该多详细？

**A**: 工具描述应包含：

- 清晰的功能说明
- 每个参数的含义和格式
- 返回值格式
- 使用示例（可选）

描述越详细，LLM 调用越准确。

### Q4: 如何防止工具被滥用？

**A**: 安全措施：

1. 参数验证：严格检查输入类型和范围
2. 权限控制：不同用户可访问不同工具
3. 审计日志：记录所有工具调用
4. 速率限制：防止频繁调用

---

## 10. 扩展阅读

### 10.1 相关文档

- [OpenAI Tool Calling 官方文档](https://platform.openai.com/docs/guides/function-calling)
- [JSON Schema 规范](https://json-schema.org/)
- [LangChain Tools 文档](https://python.langchain.com/docs/modules/agents/tools/)

### 10.2 进阶框架

- **LangChain**: 提供完整的工具调用和 Agent 框架
- **AutoGen**: 微软的多 Agent 协作框架
- **Semantic Kernel**: 微软的 AI 开发 SDK

### 10.3 相关论文

- "Tool Learning with Foundation Models" (2023)
- "Gorilla: Large Language Model Connected with Massive APIs" (2023)

---

## 11. 实验总结

### 11.1 核心要点回顾

1. **Tool Calling 架构**: LLM + 工具注册表 + 执行器 + 对话管理
2. **工具定义**: 使用 JSON Schema 描述参数结构
3. **执行流程**: 调用 → 选择工具 → 执行 → 返回结果 → 生成回复
4. **错误处理**: 将错误信息返回给 LLM 处理
5. **安全性**: 参数验证、权限控制、审计日志

### 11.2 最佳实践

- 工具描述要清晰准确
- 实现健壮的错误处理
- 设置合理的调用限制
- 记录调用日志便于调试
- 考虑并行执行多个工具调用

### 11.3 下一步学习

- 学习 LangChain 的 Agent 框架
- 探索多 Agent 协作系统
- 实现工具自动发现机制
- 构建更复杂的工具链

---

## 12. 参考代码

完整代码可在以下路径找到：

```
C:/Git-repo-my/AIResearchVault/document/Routine/03-实验案例与代码集/W30-2026-07-20/tool_calling/
```

### 文件清单

| 文件 | 说明 |
|------|------|
| `tool_registry.py` | 工具注册与管理 |
| `tool_executor.py` | 工具执行器 |
| `chat_session.py` | 对话会话管理 |
| `main.py` | 主程序入口 |
| `tools/weather_tool.py` | 天气工具 |
| `tools/calculator_tool.py` | 计算器工具 |
| `tools/search_tool.py` | 搜索工具 |

---

## 附录 A: JSON Schema 参考

### 基础类型

```json
{
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "名称"
        },
        "age": {
            "type": "integer",
            "description": "年龄",
            "minimum": 0,
            "maximum": 150
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "邮箱地址"
        },
        "is_active": {
            "type": "boolean",
            "description": "是否激活"
        }
    },
    "required": ["name", "email"]
}
```

### 数组类型

```json
{
    "type": "object",
    "properties": {
        "tags": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "标签列表"
        },
        "scores": {
            "type": "array",
            "items": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
            },
            "description": "分数列表"
        }
    }
}
```

### 枚举类型

```json
{
    "type": "object",
    "properties": {
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "优先级"
        },
        "status": {
            "type": "string",
            "enum": ["pending", "processing", "completed"],
            "description": "状态"
        }
    }
}
```

---

## 附录 B: 完整消息格式

### Tool Call 消息格式

```json
{
    "role": "assistant",
    "content": null,
    "tool_calls": [
        {
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "get_weather",
                "arguments": "{\"city\": \"北京\"}"
            }
        }
    ]
}
```

### Tool Result 消息格式

```json
{
    "tool_call_id": "call_abc123",
    "role": "tool",
    "name": "get_weather",
    "content": "【北京天气】\n温度: 25°C\n状况: 晴"
}
```

---

**文档版本**: v1.0  
**最后更新**: 2026-07-20  
**作者**: AIResearchVault  
**标签**: #tool-calling #llm #api #function-calling #初学者