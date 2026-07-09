# 技术雷达：渲染 API 与硬件标准（2026-07）

> 维度：渲染 API 与硬件标准
> 研究员：研究员_D
> 收集时间：2026-07-03
> 覆盖范围：2026 年 1–7 月发布的标准、API、硬件规格与工具链更新
> 用户关联：实时图形学 / ReSTIR 全局光照 / 数学严谨性导向

---

## 使用说明

- **Adopt**：已成熟、可立即投入生产或达到行业前 20% 水平。
- **Trial**：有明确原型或 SDK，值得跑 Demo 验证。
- **Assess**：概念验证 / 预览阶段，了解即可，等待生态成熟。
- **Hold**：已被替代、生态停滞或暂不推荐新投入。

---

## Adopt

### 1. DirectX 12 Agility SDK 1.619 / Shader Model 6.9 / DXR 1.2
- **类别**：Adopt
- **主题**：Windows 平台光线追踪与着色器模型的最新稳定基线。
- **原因**：SM 6.9 将 Shader Execution Reordering (SER) 和 Opacity Micromaps (OMM) 从预览转为正式要求功能，使 DXR 1.2 成为跨厂商路径追踪的可靠标准。Long Vectors（最大 1024 元素）和强制 16/64-bit 操作支持为神经渲染管线打下基础。Agility SDK 允许游戏直接捆绑运行时，无需等待 Windows OS 更新，工业界已有多款 AAA 引擎（如 UE5、Falcor 8.0）完成集成验证。
- **来源**：Microsoft DirectX Developer Blog, "Shader Model 6.9 and DXR 1.2", 2026-02-26; Agility SDK 1.619.3 (2026-03-06)
- **备注**：ReSTIR 实现若基于 Windows/DXR，应迁移到 DXR 1.2 以利用 SER 提升射线相干性，降低路径追踪中重采样阶段的 divergence。SER 在路径追踪 benchmark 中已有最高 47% 性能提升的实测数据。

### 2. Vulkan Roadmap 2026 Milestone
- **类别**：Adopt
- **主题**：Khronos 发布的 Vulkan 2026 年度功能基线，强制要求 VRS、Host Image Copies、Compute Shader Derivatives 等。
- **原因**：该里程碑首次将 Variable Rate Shading (VRS) 和 Shader Clock Queries 提升为高端实现的强制要求，并显著提高了 descriptor 与 shader interface limits。Vulkan 1.4 已在 2024-12 发布，而 Roadmap 2026 是在此之上的年度递进标准，确保跨平台（Linux、Android、Windows）的渲染特性一致性。Mesa 26.1（2026-05-06）已实现 Vulkan 1.4，开源驱动支持良好。
- **来源**：Khronos Vulkan Roadmap 2026 Milestone, 2026-01-23; Mesa 26.1.0 Release Notes, 2026-05-06
- **备注**：ReSTIR GI 中常用的 compute shader derivatives 和 VRS 现在可以在 Vulkan 上跨厂商可靠使用。VK_EXT_descriptor_heap（见 Trial）是后续演进方向，但目前 Roadmap 2026 的 descriptor limit 提升已足够支持大型 reservoir buffer 绑定。

### 3. VK_EXT_ray_tracing_invocation_reorder (SER in Vulkan)
- **类别**：Adopt
- **主题**：Vulkan 光线追踪 Shader Execution Reordering 的多厂商扩展。
- **原因**：2025-11-18 Khronos 将该扩展从 NVIDIA 专有扩展 (VK_NV_*) 升级为多厂商扩展 (VK_EXT_*)。在 Vulkan glTF path tracer benchmark 中实测带来最高 47% 的性能提升。它提供了与 DXR 1.2 SER 等价的光线重排序能力，是 Linux 和跨平台路径追踪实现的必备优化。
- **来源**：Khronos Announcement, 2025-11-18; Vulkan Extension Registry
- **备注**：ReSTIR 中的重采样步骤（spatial/temporal reuse）对射线相干性高度敏感。SER 能减少 incoherent rays 导致的 SIMD divergence，直接提升 ReSTIR PT / ReSTIR GI 的 frame rate。对于在 Linux 上运行 Vulkan-based ReSTIR 实现的研究者，这是必须启用的扩展。

### 4. NVIDIA RTX 50 系列 (Blackwell Architecture)
- **类别**：Adopt
- **主题**：NVIDIA 2026 年消费级 GPU 旗舰，基于 Blackwell 架构，4th Gen RT Cores + 5th Gen Tensor Cores。
- **原因**：RTX 5090 采用 GB202 die (TSMC 4NP)，92.2B 晶体管，170 SMs，21,760 CUDA cores，170 个 4th-gen RT Cores，680 个 5th-gen Tensor Cores。32GB GDDR7 显存，1,792 GB/s 带宽（比 RTX 4090 提升 78%）。SER 2.0、Mega Geometry、Linear Swept Spheres 等硬件特性直接降低复杂场景的路径追踪开销。RTX 5080/5070 Ti 等 SKU 已铺货，驱动生态成熟。
- **来源**：NVIDIA RTX Blackwell GPU Architecture Whitepaper, 2026; GeForce RTX 5090 Official Specs, 2026-01-30
- **备注**：对 ReSTIR 研究者而言，4th-gen RT Cores 的 ray-triangle intersection 吞吐量提升和 SER 2.0 是关键。32GB VRAM 允许在更高分辨率 G-buffer / reservoir 中做 spatiotemporal reuse 而无需担心内存瓶颈。但需注意：FP4 和 Neural Rendering 特性尚处生态早期，可视为 Trial 级功能。

### 5. AMD RDNA 4 / Radeon RX 9000 系列
- **类别**：Adopt
- **主题**：AMD 2026 年主力 GPU 架构，每 CU 的 Ray Accelerator 数量翻倍，FSR 4 引入 ML 超采样。
- **原因**：RX 9070 XT / 9070 等 SKU 于 2026-03 发布。RDNA 4 在光栅性能上与 NVIDIA RTX 5070 系列竞争，光追性能相比 RDNA 3 缩小了约 15–20% 的差距（此前为 40%）。Linux 开源驱动（Mesa RADV）对 Vulkan RT 支持极佳，且 AMD 已原生支持 VK_EXT_ray_tracing_invocation_reorder 和 SM 6.9 的等价功能。性价比（VRAM/美元）优于 NVIDIA 同档位。
- **来源**：AMD RDNA 4 Architecture Reviews, Newegg / KitGuru, 2026-04; AMD AGS Library v6.3, 2026
- **备注**：若研究场景需要在 Linux 上大规模运行 ReSTIR 实验，RX 9070 XT 是性价比极高的选择。RADV 驱动在 Mesa 26.0 中实现了 HPLOC（加速 RT pipeline 编译）和 SER 支持，编译速度可达 10x 提升。注意：FSR 4 的 ML 超采样与 DLSS 4 尚有质量差距，但光追 API 兼容性已足够用于学术实验。

### 6. WebGPU 1.0 (All Major Browsers Shipping)
- **类别**：Adopt
- **主题**：W3C WebGPU 标准于 2025-11 实现所有主流浏览器（Chrome、Firefox、Safari、Edge）默认支持。
- **原因**：WebGPU 不再是实验性 API。Chrome 通过 Dawn（C++，映射到 D3D12/Metal/Vulkan）实现，Firefox 通过 wgpu（Rust）实现。WGSL 作为原生安全着色语言，避免了 SPIR-V 的浏览器兼容性问题。Unity 6、Babylon.js、Three.js 已支持 WebGPU 后端。对于需要跨平台演示或快速原型验证的 ReSTIR 实现，WebGPU 提供了从浏览器到原生的统一代码路径。
- **来源**：W3C WebGPU Spec, 2026-05-21; webgpu.com "Critical Mass" announcement, 2025-12-01
- **备注**：当前 WebGPU 尚不支持硬件光线追踪和 mesh shaders（预计 2027+），因此仅适用于 ReSTIR 的 software / compute-shader 路径原型，或基于 screen-space / rasterization 的 GI 近似。不适合做 ReSTIR PT 的完整硬件加速实现。但对于快速验证 resampling 算法的数学正确性（compute shader 内实现 reservoir sampling），这是一个极佳的跨平台沙盒。

---

## Trial

### 7. Vulkan 1.4.351 Opacity Micromap + VK_EXT_descriptor_heap
- **类别**：Trial
- **主题**：Vulkan 2026-05 引入 Opacity Micromap 支持，以及全新的 descriptor heap 扩展。
- **原因**：Vulkan 1.4.351（2026-05-11/12）新增六项扩展，其中 Opacity Micromap 支持让 Vulkan 光追可以像 DXR 1.2 OMM 一样高效处理 alpha-tested geometry（植被、栅栏）。VK_EXT_descriptor_heap 是对现有 descriptor set 机制的重构，提供直接 descriptor 内存访问，对标 D3D12 的 descriptor heap 模型。但 descriptor heap 目前仍为 EXT 级别（非 KHR），Khronos 明确说明正在收集开发者反馈，计划未来升级为 KHR。
- **来源**：Vulkan 1.4.351 Release Notes (Phoronix / VideoCardz), 2026-05-11/12; Khronos Blog, 2026-01-23
- **备注**：OMM 对 ReSTIR 中处理大量 alpha-tested 光源遮挡场景有直接价值（减少 any-hit shader 调用）。VK_EXT_descriptor_heap 若未来成为 KHR，将简化 ReSTIR 中大量 reservoir / G-buffer texture 的绑定管理。建议先在一个分支中试用，等 KHR 后再全面迁移。

### 8. DirectX 12 Agility SDK 1.720 Preview / Shader Model 6.10 / DXR 2.0 Preview
- **类别**：Trial
- **主题**：微软 2026-04-27 发布的预览版，包含 SM 6.10 和 DXR 2.0 的早期特性。
- **原因**：SM 6.10 引入 `linalg::Matrix`（统一访问各厂商矩阵单元：Tensor Core / XMX / AI Accelerator）、`Group Wave Index`（安全获取 wave 结构）、`Variable Group Shared Memory`（突破 32KB groupshared 限制），以及光追内建函数 `TriangleObjectPositions()` 和 `ClusterID()`。DXR 2.0 要求 OMM + SM 6.10，并引入了 clustered geometry 支持。这些特性为神经渲染和大型 tile-based resampling 算法提供了新的硬件接口。
- **来源**：Microsoft DirectX Developer Blog, "Announcing Shader Model 6.10 Preview", 2026-04-27; Wccftech, 2026-04-27
- **备注**：`linalg::Matrix` 允许 ReSTIR 实现中的矩阵运算（如协方差计算、Jacobian 变换的线性代数部分）直接调用 GPU 原生矩阵单元， potentially 提升 reservoir weight 更新和 neighbor compatibility 评分的性能。但注意：Intel 对 `linalg::Matrix` 的支持尚未推出，AMD 仅 RX 9000 支持。建议仅在 NVIDIA RTX 硬件上先行实验。

### 9. Metal 4 / Apple M5 (M5 Pro / M5 Max)
- **类别**：Trial
- **主题**：Apple 2025-10 发布 M5，2026-03 发布 M5 Pro/Max，搭载 Metal 4 API、3rd-gen ray tracing engine、hardware mesh shading。
- **原因**：M5 的 GPU 引入每核心 Neural Accelerator，AI 峰值算力比 M4 提升 4x+。3rd-gen ray tracing engine 在 M5 Pro 上带来最高 35% 的光追性能提升（相比 M4 Pro）。Metal 4 新增 MetalFX Frame Interpolation / Denoising、MTLTensor、动态分辨率 upscaler。对于在 macOS 上开发或需要跨 Apple 平台部署的 ReSTIR 研究者，这是唯一的低级别图形 API 选择。
- **来源**：Apple Newsroom, "Apple unleashes M5", 2025-10-15; "Apple debuts M5 Pro and M5 Max", 2026-03-01; Apple Developer Metal Overview
- **备注**：Metal 的 intersector API 已支持 reorder stage，可减少自定义 intersection shader 的 divergence，对 ReSTIR 的 shadow ray / next-event estimation 阶段有益。但 Apple Silicon 的内存模型与 PC GPU 差异大，且 Metal 是封闭生态。若研究目标是跨平台算法，建议将 Metal 实现作为验证端口，而非主要开发平台。

### 10. Intel Arc B-Series (Xe2 "Battlemage")
- **类别**：Trial
- **主题**：Intel 第二代独显架构，2025-12 发布 B580/B570，2026-03 发布 Arc Pro B70 (32GB)。
- **原因**：Xe2 架构在 B580 上实现了硬件加速 SER，Microsoft 内部测试显示 SER 在 Arc B-Series 上可带来最高 90% 的帧率提升（RTX 4090 上为 40%）。12GB VRAM 起步，Arc Pro B70 提供 32GB GDDR6 和 256 XMX 引擎。驱动在 2026 年已有显著改善，并通过 Mesa ANV 驱动在 Linux 上获得开源支持。
- **来源**：Intel Arc B-Series Launch, 2025-12-30; KitGuru / HotHardware, 2026-03-02; Wccftech Maxsun Arc Pro B70 Review, 2026-06-24
- **备注**：若 ReSTIR 实验需要大量 VRAM 但预算有限，Arc Pro B70 ($949) 是一个性价比极高的 32GB 选择。但需注意：Intel 的高端消费级 B770/B750 已被取消，驱动成熟度仍不如 NVIDIA/AMD。此外，`linalg::Matrix` (SM 6.10) 在 Intel 上的支持尚未落地。

### 11. Advanced Shader Delivery (Microsoft)
- **类别**：Trial
- **主题**：微软在 GDC 2026 宣布的预编译着色器分发技术，旨在消除游戏加载时的 shader compilation stutter。
- **原因**：该技术允许开发者在游戏分发时打包针对特定 GPU 配置预编译的 shader，避免运行时 JIT 编译导致的帧时间尖峰。NVIDIA、AMD、Intel 均承诺支持。对于需要长时间运行 benchmark 的 ReSTIR 研究（如 variance 分析、帧时间稳定性测量），稳定的 shader 编译行为是实验可复现性的基础。
- **来源**：Microsoft GDC 2026 State of DirectX; Wccftech, 2026-03-13; Igor's Lab, 2026-03-14
- **备注**：与 ReSTIR 算法本身无直接关联，但如果在 Windows 上做大量帧时间稳定性实验，Advanced Shader Delivery 可以消除一个显著的干扰变量。目前仍为技术预览，预计 2026 年下半年随 Windows 更新正式推出。

### 12. KHR_gaussian_splatting (glTF Extension Release Candidate)
- **类别**：Trial
- **主题**：Khronos 2026-02-04 发布 glTF 2.0 的 3D Gaussian Splatting 扩展候选规范。
- **原因**：该扩展将 3DGS 数据（position, scale, rotation, spherical harmonics）标准化为 glTF mesh primitive 属性，并提供 SPZ 压缩格式支持。已有 CesiumJS、Esri ArcGIS、Niantic Scaniverse 等应用计划采用。预计 2026-Q2 正式批准。对于需要将神经辐射场与传统光栅化/光追管线混合的 ReSTIR 扩展研究者，这是一个可互操作的资产格式。
- **来源**：Khronos Group, "KHR_gaussian_splatting Release Candidate", 2026-02-04; CG Channel, 2026-02-05
- **备注**：若 ReSTIR 研究涉及 3D Gaussian Splatting 场景的光照计算（如 ReSTIR 在 NeRF/3DGS 场景中的应用），此扩展提供了统一的场景数据入口。但 3DGS 与光追 acceleration structure 的交互仍需自定义，标准尚未覆盖。

---

## Assess

### 13. DirectX Linear Algebra / Compute Graph Compiler
- **类别**：Assess
- **主题**：微软 2026 GDC 宣布的 ML-in-graphics 基础设施，旨在将神经网络推理直接集成到渲染管线。
- **原因**：DirectX Linear Algebra 提供统一的矩阵运算抽象（对标 `linalg::Matrix` 的前身），Compute Graph Compiler 允许在 GPU 上以原生性能执行完整 ML 模型图，并支持 PIX 统一调试。Public preview 2026-04 已发布，Private preview 预计 2026 年夏季。该技术是 DLSS 4 Ray Reconstruction、Neural Radiance Cache 等特性的底层 API 基础。
- **来源**：Microsoft GDC 2026 DirectX Blog; Wccftech, 2026-03-13; Igor's Lab, 2026-03-14
- **备注**：ReSTIR 中的 Neural Radiance Cache (NRC) 或 learned importance sampling 需要 shader 内嵌入小型神经网络。Compute Graph Compiler 理论上可以消除当前 CUDA / ONNX 旁路的必要性，实现纯 DX12 的 neural GI。但当前仅为预览，且模型部署工具链（量化、内存规划）尚不成熟。建议关注，等待 2026 年底或 2027 年的正式版。

### 14. Neural Shaders / RTX Neural Rendering (NVIDIA Blackwell)
- **类别**：Assess
- **主题**：NVIDIA Blackwell 引入的 shader 内嵌神经网络能力，包括 RTX Neural Materials、Neural Texture Compression (NTC)、Neural Radiance Cache (NRC)、RTX Skin / Neural Faces。
- **原因**：这些特性利用 Blackwell 的 Neural Accelerator 和 FP4/FP8 支持，在 shader 中实时执行小型神经网络。DLSS 4.5 已采用 Transformer-based 模型替代 CNN。但除 DLSS 外，其他 Neural Shaders 目前主要存在于 NVIDIA SDK 和 Omniverse 生态中，跨厂商支持为零，且需要额外的训练数据/模型。
- **来源**：NVIDIA RTX Blackwell Architecture Whitepaper, 2026; NVIDIA Developer Blog
- **备注**：对 ReSTIR 研究者，NRC 是最直接相关的 neural shader 应用，因为它可以缓存间接光照辐射度，减少 ReSTIR 需要追踪的路径长度。但当前 NRC 实现仍依赖 CUDA 或自定义 shader 代码，尚未有标准化的跨 API 方案。建议在 Falcor / NVIDIA SDK 中试用，但暂不纳入核心算法依赖。

### 15. CXL Memory Pooling for GPU Rendering
- **类别**：Assess
- **主题**：Compute Express Link (CXL) 作为 PCIe 5.0 之上的内存扩展和池化标准，2026 年在数据中心领域受关注。
- **原因**：CXL 3.0 允许 GPU 通过 cache-coherent 链路访问远程内存池，Type 3 内存扩展模块可达 512GB/模块。但当前消费级 GPU（NVIDIA RTX 50、AMD RDNA 4）完全不支持 CXL。AMD MI300A 支持有限，NVIDIA 无计划。CXL 内存访问延迟约为本地 DRAM 的 3.1x（~658ns vs ~214ns），对实时渲染的帧一致性影响未知。
- **来源**：SemiAnalysis, "CXL Is Dead In The AI Era", 2025-10-29; arXiv "Node-Spanning GPU Collectives with CXL Memory Pooling", 2026-02-25
- **备注**：对于需要处理超大规模场景（如电影级 asset）的离线 ReSTIR 渲染，CXL 内存池可能提供 TB 级内存。但实时 GI 场景下，延迟和带宽（PCIe 5.0 32 GT/s）是瓶颈。该技术与 ReSTIR 的实时目标相冲突，仅在对延迟不敏感的离线/路径追踪实验中有潜在价值。

### 16. PCIe 6.0 (64 GT/s, PAM4, FLIT Mode)
- **类别**：Assess
- **主题**：PCI-SIG 2022 年发布规范，2026 年尚未在消费级 GPU 上采用。
- **原因**：PCIe 6.0 提供 x16 256 GB/s 双向带宽（是 PCIe 5.0 的 2x），引入 PAM4 信号和 FLIT 模式以降低延迟。但截至 2026-07，NVIDIA RTX 50 和 AMD RX 9000 仍仅支持 PCIe 5.0 x16（128 GB/s）。Puget Systems 测试表明，在 GPU 渲染（Blender/Octane）中，PCIe 带宽对性能影响极小（<5%），因为场景完全驻留于 VRAM。PCIe 6.0 的受益场景主要是多 GPU 显存池化或 LLM 卸载。
- **来源**：PCIe 6.0 Specification, 2022-01; Puget Systems "Impact of PCIe 5.0 Bandwidth on GPU Content Creation", 2025-07-16
- **备注**：ReSTIR 研究者无需等待 PCIe 6.0 平台。即使当前 GPU 被限制在 PCIe 5.0 x8，对 frame time 的影响也低于测量噪声。若未来需要多 GPU ReSTIR 的显存池化（如分布式 ReSTIR 的大规模 spatial reuse），PCIe 6.0 的带宽提升才有意义。

### 17. WebGPU Ray Tracing / Mesh Shaders (Future)
- **类别**：Assess
- **主题**：WebGPU 标准中尚未纳入硬件光追和 mesh shader，但社区和标准化进程正在讨论。
- **原因**：WebGPU 1.0 已全面支持，但硬件 RT 需要 bindless resources 和 acceleration structure API，当前 WebGPU 工作组尚未承诺。社区项目如 WebRTX 通过 compute shader 实现软件 RT，性能差距 10–100x。根据 WebGPU Future Roadmap，mesh shaders 被 bindless 阻塞，预计 2026+；硬件 RT 最早 2027，前提是工作组达成共识。
- **来源**：Kaelan.fyi "WebGPU Future Roadmap (2025-2027)"; WebGPU W3C Spec, 2026-05-21
- **备注**：对于在浏览器中演示 ReSTIR 算法，目前只能使用软件 RT 或光栅化 approximation。硬件 RT 的缺失意味着 ReSTIR PT 无法在 WebGPU 上达到实时性能。建议持续跟踪 WebGPU 扩展提案，但不做开发计划依赖。

### 18. OpenUSD / AOUSD 生态 (v1.0 Core Spec + Physics WG)
- **类别**：Assess
- **主题**：Alliance for OpenUSD (AOUSD) 推进的 3D 场景互操作标准，2026 年聚焦物理模拟和数字孪生。
- **原因**：AOUSD 在 GTC 2026 上展示了 OpenUSD 在机器人、物理 AI、工业数字孪生中的应用。Core Spec WG 目标 2025 年底完成 v1.0，Physics WG 正在定义刚体规范。Khronos 与 AOUSD 在 glTF/USD 互操作方面（如 3D Gaussian Splatting、MaterialX）有紧密协作。但 OpenUSD 主要用于内容创作管线，而非实时渲染 API 本身。
- **来源**：AOUSD.org; NVIDIA GTC 2026 OpenUSD Sessions; Khronos glTF-USD SIGGRAPH BOF, 2025-08
- **备注**：若 ReSTIR 研究涉及从 USD 场景（如 Omniverse/Falcor 的 USD importer）中加载复杂动态场景，OpenUSD 的层级合成和 variant set 是实用工具。但 OpenUSD 的学习曲线陡峭，且对渲染性能无直接优化。建议通过现有 DCC 工具（如 Blender、Maya）的 USD 插件间接使用，而非直接编写 USD 代码。

---

## Hold

### 19. OpenGL / OpenGL ES
- **类别**：Hold
- **主题**：1992 年诞生的跨平台图形 API，2017 年 OpenGL 4.6 后进入仅维护模式。
- **原因**：Khronos 明确表示新功能仅向 Vulkan 添加。Apple 已在 macOS 上完全移除 OpenGL 支持（M1 及以后仅 Metal）。Mesa 26.1 仍支持 OpenGL 4.6，但所有现代扩展（ray tracing、mesh shaders、VRS）均不可用。对于新启动的 ReSTIR 项目，OpenGL 没有任何硬件光追或 compute shader 的可靠路径。
- **来源**：Khronos Group History; Mesa 26.1.0 Release Notes; Apple Platform Deprecation
- **备注**：除非维护遗留代码库，否则应完全放弃 OpenGL。ReSTIR 严重依赖 compute shader 和硬件 RT Core，两者在 OpenGL 中均不存在。

### 20. Intel Arc B770 / B750 (High-End Battlemage Cancelled)
- **类别**：Hold
- **主题**：Intel 原计划基于 BMG-G31 die 的高端消费级 GPU，据称已被取消。
- **原因**：据 2025-03 泄露信息，Intel 在 2024-Q3 已取消 BMG-G31 高端 GPU 计划，CEO 年度股东信未提及 Arc GPU。目前唯一出货的 Battlemage 型号为 B580 (20 Xe cores, BMG-G21) 和 B570，以及 Pro 系列 B50/B60/B70/B65。没有高端游戏卡与 RTX 5070 Ti 以上竞争。
- **来源**：Club386, "High-end Intel Arc Battlemage GPUs may never see the light of day", 2025-03-28; Wccftech Intel Pro Day 2026
- **备注**：若已持有 B580 用于实验，可以继续使用。但不应期待 Intel 在 2026 年提供与 RTX 5080/5090 竞争的高端光追硬件。对于需要大规模并行 ReSTIR 实验的研究者，Intel GPU 的规模和生态都不足以成为主力平台。

### 21. Vulkan SC (Safety Critical)
- **类别**：Hold
- **主题**：Vulkan 的安全关键子集，用于汽车、航空、工业控制。
- **原因**：Vulkan SC 1.0 已发布，但目标市场与实时游戏/图形学研究完全无关。其功能集被大幅裁剪，移除了动态内存分配和递归，不适合 ReSTIR 这类需要大量 compute dispatch 和动态 buffer 管理的算法。
- **来源**：Khronos Vulkan SC Specification; NVIDIA Vulkan SC SDK
- **备注**：无直接关联。若研究方向转向自动驾驶可视化，才需重新评估。

### 22. WebGL 2.0
- **类别**：Hold
- **主题**：WebGL 2.0 (OpenGL ES 3.0 for Web) 已被 WebGPU 全面取代。
- **原因**：Safari 26 在 Apple M4 硬件上已降低 WebGL 优先级，优先调度 WebGPU 资源。Chrome 和 Firefox 的图形团队已将全部新功能投入 WebGPU。WebGL 的计算能力有限（无 compute shaders），无法支持 ReSTIR 的 reservoir sampling 和 spatial reuse。
- **来源**：Safari 26 Compatibility Guide, 2026-03-05; WebGPU Critical Mass Announcement, 2025-12
- **备注**：任何新的 Web 端图形项目都应使用 WebGPU。WebGL 2.0 仅用于维护旧项目。

---

## 补充：与用户 ReSTIR 研究直接相关的 API 功能映射

| ReSTIR 算法环节 | 推荐 API 特性 | 状态 | 说明 |
|---|---|---|---|
| **Primary ray / G-buffer** | DXR 1.2 / Vulkan RT | Adopt | 硬件加速，成熟稳定 |
| **Shadow ray / next-event estimation** | SER (DXR 1.2 / VK_EXT_rt_invocation_reorder) | Adopt | 减少 shadow ray divergence |
| **Spatial reuse (neighbor resampling)** | Compute Shader + VRS | Adopt | VRS 允许在 ReSTIR 的平滑区域降低 shading rate |
| **Temporal reuse (frame-to-frame)** | DXR 1.2 / Vulkan RT + Shader Clock | Adopt | Shader clock 用于 measuring frame coherence |
| **Reservoir buffer management** | VK_EXT_descriptor_heap / D3D12 descriptor heaps | Trial | 大量 UAV/SRV 绑定，新 descriptor 模型更高效 |
| **Alpha-tested geometry (植被等)** | Opacity Micromaps (DXR 1.2 / Vulkan 1.4.351) | Trial | 减少 any-hit shader 开销，2026-05 Vulkan 刚支持 |
| **Indirect lighting (ReSTIR GI/PT)** | DXR 1.2 / Vulkan RT + 4th/3rd-gen RT Cores | Adopt | 所有 2026 新 GPU 均有硬件支持 |
| **Neural cache / learned sampling** | DirectX Compute Graph Compiler / Neural Shaders | Assess | 预览阶段，Shader 内嵌 NN 仍不成熟 |
| **跨平台原型验证** | WebGPU Compute Shader | Adopt | 无硬件 RT，但可验证 core resampling 逻辑 |
| **Apple 平台移植** | Metal 4 + Intersector API | Trial | 3rd-gen RT 支持，但封闭生态 |

---

## 来源汇总

1. **Khronos Group**: Vulkan Roadmap 2026, VK_EXT_descriptor_heap, VK_EXT_ray_tracing_invocation_reorder, KHR_gaussian_splatting — https://www.khronos.org/
2. **Microsoft DirectX Developer Blog**: SM 6.9 (2026-02-26), SM 6.10 Preview (2026-04-27), Agility SDK Downloads — https://devblogs.microsoft.com/directx/
3. **NVIDIA**: RTX Blackwell Architecture Whitepaper, GeForce RTX 5090 Specs, Vulkan Developer Beta Drivers — https://developer.nvidia.com/
4. **Apple**: M5 / M5 Pro / M5 Max Press Releases (2025-10, 2026-03), Metal Developer Documentation — https://developer.apple.com/metal/
5. **AMD**: RDNA 4 Architecture, AGS Library v6.3, RADV Mesa Driver Updates — https://gpuopen.com/
6. **Intel**: Arc B-Series Launch, Arc Pro B70 Specs — https://intel.com/
7. **W3C**: WebGPU Spec (2026-05-21), WGSL Spec — https://www.w3.org/TR/webgpu/
8. **Mesa**: Mesa 26.1.0 Release Notes (2026-05-06) — https://mesa3d.org/
9. **Phoronix**: Vulkan 1.4.351, Mesa 26.1, RADV HPLOC — https://www.phoronix.com/
10. **Wccftech / HotHardware / KitGuru / Igor's Lab**: DXR 2.0, SM 6.10, GPU Architecture Comparisons — 2026-01 ~ 2026-06
11. **SIGGRAPH / HPG 2026**: ReSTIR CGNS Paper (HPG 2026), Spatio-Temporal Control Variates with ReSTIR (SIGGRAPH 2026 Honorable Mention) — https://github.com/orion-junkins/ReSTIR-CGNS
12. **Puget Systems**: PCIe 5.0 GPU Bandwidth Impact Study — 2025-07-16
13. **SemiAnalysis**: "CXL Is Dead In The AI Era" — 2025-10-29

---

*文档生成时间：2026-07-03*
*下次更新建议：2026-08-01 前补充 SIGGRAPH 2026 (2026-07-19~23) 正式论文发表后的技术细节。*
