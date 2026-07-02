# 05-技术雷达 — 执行计划

## 目标
为 2026 年 7 月生成一份聚焦「实时图形学 / 全局光照 / ReSTIR」领域的技术雷达，填充 Adopt / Trial / Assess / Hold 四个象限。

## 背景信息
- 用户工作领域：实时计算机图形学，正在深入 ReSTIR 全局光照算法
- 维护本地笔记库 [[GameDevVault]] 用于论文阅读与数学推导
- 对数学严谨性要求高，需要无偏性证明和 Jacobian 推导细节
- 更新频率：每月（月初收集 → 评估 → 更新 → 全月执行）

## 阶段 1：并行研究（Research Swarm）
启动 4 个 explore 子代理，分别搜索不同维度：

1. **ReSTIR & 全局光照 学术进展**（研究员_A）
   - 搜索 2026 年 SIGGRAPH / EGSR / HPG 等会议上 ReSTIR、GI、路径追踪最新论文
   - 关注 ReSTIR 的改进版本、无偏性证明、Jacobian 相关技术
   - 收集论文标题、作者、核心贡献、可复现代码/项目链接

2. **AI × 图形学 交叉前沿**（研究员_B）
   - 神经渲染（NeRF、Gaussian Splatting、3D Gaussian Splatting 2.0）
   - Diffusion 模型用于渲染、材质生成、光照估计
   - 实时神经渲染管线与硬件加速（如 NVIDIA RTX Neural Rendering）
   - 收集关键项目、Demo、GitHub 仓库

3. **图形学工具链与引擎**（研究员_C）
   - Unreal Engine 5、Godot、Bevy 等引擎的最新渲染特性
   - 图形学编程语言/框架生态（Zig、Rust wgpu、Jai 等）
   - 调试工具（RenderDoc 新特性、PIX、NVIDIA Nsight Graphics）
   - 开源 GI 实现（如 Embree 4、OptiX 更新、WebGPU 光线追踪）

4. **渲染 API 与硬件标准**（研究员_D）
   - Vulkan、DirectX 12、Metal 最新扩展（光线追踪、网格着色器、变量着色率）
   - WebGPU 标准进展与实现（Dawn、wgpu）
   - GPU 硬件趋势（NVIDIA RTX 50 系、Intel Arc、AMD RDNA 4 对渲染的影响）
   - 行业标准化（如 glTF 扩展、USD 生态）

## 阶段 2：评估与写作（Assessment & Writing）
- 汇总所有研究结果
- 结合用户当前深度（ReSTIR GI）和学习目标，将技术归类到四个象限：
  - **P0 Adopt**：应立即投入、达到行业前 20%
  - **P1 Trial**：有潜力、值得跑 Demo
  - **P2 Assess**：新兴、了解即可
  - **P3 Hold**：暂时观望或已被替代
- 为每个技术填写：主题、为什么、投入/实验/关注/替代计划
- 更新更新日志

## 阶段 3：输出
- 生成 `2026-07.md` 文件到 `05-技术雷达/` 目录
- 保持与 `00-README.md` 一致的格式和风格

## 输出格式
参考 00-README.md 的表格结构，使用 Markdown 格式，中文内容，技术术语保留英文。

## 质量约束
- 所有技术条目必须有明确来源（会议名称、论文标题、GitHub 链接、版本号等）
- 避免模糊描述，每条目需要说明「为什么」的具体理由
- 考虑用户数学导向的品味，Adopt 级别应包含可推导的算法/论文
