# AI × 图形学 交叉前沿 — 技术雷达（2026-07）

> **研究维度**：AI × 图形学 交叉前沿  
> **目标读者**：实时计算机图形学从业者，聚焦 ReSTIR 全局光照算法  
> **更新日期**：2026-07-03  
> **评估标准**：数学严谨性、可复现性、与 ReSTIR/GI 工作的关联度

---

## 象限说明

| 象限 | 含义 | 行动建议 |
|------|------|----------|
| **Adopt** | 已成熟、工业界验证、可立即投入 | 阅读论文、跑通代码、纳入工具链 |
| **Trial** | 有原型、值得实验、SIGGRAPH/EGSR 新近发表 | 跑 Demo、复现核心算法、评估稳定性 |
| **Assess** | 概念验证阶段、了解即可 | 跟踪 arXiv/项目页、了解核心思想 |
| **Hold** | 已被替代或尚不成熟 | 了解为什么被替代，不投入精力 |

---

## P0 — Adopt（已成熟，应立即投入）

### 1. Generalized ReSTIR / ReSTIR PT（GRIS 框架）
- **主题**：ReSTIR 的理论基石，支持无偏时空路径复用的统一框架
- **原因**：ReSTIR 所有变体（PT/GI/BDPT）都建立在 GRIS 之上。其贡献权重公式 $W_Y = \frac{1}{\hat{p}(Y)} \sum_{i=1}^M w_i$ 是理解无偏性的核心。Jacobian 推导在 shift mapping 中贯穿始终。2026 年新论文几乎全是基于此框架的扩展。
- **来源**：Lin et al., "Generalized Resampled Importance Sampling: Foundations of ReSTIR", SIGGRAPH 2022. 课程笔记：Wyman et al., "A Gentle Introduction to ReSTIR", SIGGRAPH 2023.
- **备注**：**必读**。这是你的 ReSTIR 研究底座。所有 2026 年新论文的引用基础。

### 2. NVIDIA OptiX 8.1（AI 加速 Denoiser + 光线追踪 SDK）
- **主题**：OptiX 内置 Temporal Denoiser、异步 Demand Loading、改进的曲线求交
- **原因**：OptiX 8.1 的 `OPTIX_DENOISER_MODEL_KIND_TEMPORAL` 支持时间序列去噪，减少动画闪烁，需要前一帧去噪图和 motion vectors。对 ReSTIR 的 1spp 实时输出至关重要。API 简化（`optixDenoiserCreate` 合并模型选择）。Phantom intersector 加速曲线。
- **来源**：NVIDIA OptiX 8.1 Release Notes (2025). https://developer.nvidia.com/optix
- **备注**：与 ReSTIR PT 的 1spp 输出直接耦合。是实时路径追踪的工业标准后端。

### 3. Intel Open Image Denoise (OIDN) 2.x
- **主题**：硬件无关的 AI Denoiser，CPU/GPU 双端支持
- **原因**：OIDN 2.x 已支持 GPU（CUDA/SYCL/HIP/Metal），是跨平台替代 OptiX 的唯一成熟选择。Unity 6.5 已弃用 OptiX 转投 OIDN。训练数据公开，可研究其网络结构。注意：OIDN 2.x 暂不支持 temporal denoising（OIDN 3 将支持）。
- **来源**：Intel OIDN 2.4.1 (latest). GitHub: RenderKit/oidn. Sci-Tech Award 2025.
- **备注**：如果你关注跨平台/非 NVIDIA 硬件，这是必选项。与 ReSTIR 输出配合可构建平台无关的 RTGI 管线。

### 4. NVIDIA Neural Texture Compression (NTC) SDK v0.9
- **主题**：利用 Tensor Core 实时解压纹理，压缩至原始的 4–7% VRAM
- **原因**：NTC 在 Blackwell 架构上通过 Tensor Core 运行，不占用 CUDA/RT Core 算力。SDK v0.9 的 BC7 编码速度提升 6×，推理速度提升 20–40%。对 texture-heavy 的 GI 场景意义重大——有效 VRAM 容量可扩大一个数量级。
- **来源**：NVIDIA CES 2026. RTX Neural Texture Compression SDK v0.9. GTC 2026 demo: "Tuscan Villa" 6.5GB → 970MB.
- **备注**：间接影响 ReSTIR GI 的复杂场景承载能力。RTX 5090 实测渲染时间比 4090 快 30–40%。

### 5. WebGPU（浏览器原生 GPU 计算与渲染）
- **主题**：2025 年底所有主流浏览器默认支持 WebGPU，W3C Candidate Recommendation
- **原因**：Chrome 113+ / Firefox 147+ / Safari 26+ 已全面支持。Dawn (C++) 和 wgpu (Rust) 双实现。支持 compute shader 和 WGSL。覆盖约 82.7% 全球浏览器流量。意味着可构建跨平台的 ReSTIR demo/教学工具，无需安装。
- **来源**：W3C WebGPU Spec. WebGPU 2026 browser support guide. https://github.com/mikbry/awesome-webgpu
- **备注**：如果你考虑开源/教学/工具化 ReSTIR 实现，WebGPU 是最低摩擦的部署路径。

---

## P1 — Trial（有潜力，值得跑 Demo）

### 6. ReSTIR PG: Path Guiding with Spatiotemporally Resampled Paths
- **类别**：Trial
- **主题**：从 ReSTIR 的 resampled paths 中提取 vMF 混合模型指导下一帧初始采样
- **原因**：核心洞察：ReSTIR 接受的路径已经近似理想 local guiding distribution（$L_i \cdot \cos\theta$ 的乘积）。通过 density estimation（EM 算法）在 spatial hash grid 中拟合 4-component vMF 模型，用 one-sample MIS 与 BSDF sampling 结合。相比 raw PT samples，MAPE 显著降低，correlation artifacts 减少。
- **来源**：Zeng et al. (NVIDIA/UCSB/MBZUAI), SIGGRAPH Asia 2025. https://research.nvidia.com/labs/rtr/publication/zeng2025restirpg/
- **备注**：**与 ReSTIR 直接相关**。论文含完整 Jacobian/MIS 权重推导。代码未完全公开但算法可复现。是 ReSTIR → Path Guiding 的闭环。

### 7. Real-Time Level-of-Detail Rendering with ReSTIR
- **类别**：Trial
- **主题**：引入 surface point mapping 使 ReSTIR 在几何 LoD 切换时保持时空复用
- **原因**：此前 ReSTIR 要求帧间 mesh topology 一致，LoD 切换会破坏 temporal reuse。本文通过 surface point mapping 使不同拓扑的 mesh 间可复用 reservoir。恢复了 LoD 场景的 reuse efficiency。
- **来源**：Yu-Chen Wang et al. (NVIDIA), SIGGRAPH 2026 (Conference Track). https://research.nvidia.com/labs/rtr/publication/wang2026levelofdetail/
- **备注**：对复杂场景 ReSTIR 实用化至关重要。论文涉及 shift mapping 的 Jacobian 修正。

### 8. Compatibility-Guided Neighbor Selection (CGNS) for ReSTIR
- **类别**：Trial
- **主题**：用几何兼容性加权选择空间邻域，替代 uniform disk sampling
- **原因**：从 quasi-random disk 采样 K 个候选邻居，根据位置/法线相似度打分，通过 weighted reservoir sampling 选 M 个邻居进入空间重采样。以极小 runtime overhead 提升空间邻居质量。
- **来源**：Junkins et al., HPG 2026. DOI: 10.1145/3820024. GitHub: https://github.com/orion-junkins/ReSTIR-CGNS
- **备注**：**代码已开源**（Falcor 8.0）。直接改进 ReSTIR 的 spatial reuse 阶段。可立即集成到你的 ReSTIR 实现中。

### 9. Neural Quadrature Rule and Autoregressive Adaptive Sampling
- **类别**：Trial
- **主题**：端到端联合学习 sampler 和 integrator，用神经网络做 quadrature rule
- **原因**：将数值积分重新定义为"在 domain 中放点和加权"的问题。NQR 联合学习采样分布和积分权重，使 sample 和 integration 耦合更紧密。在 lighting、transmittance、winding number、walk-on-spheres 上验证。可应用于 ReSTIR 的候选采样阶段。
- **来源**：Haolin Lu et al. (UCSD), SIGGRAPH 2026. https://suikasibyl.github.io/nqr/
- **备注**：数学上非常有趣。autoregressive 采样 + 学习积分权重，可能与 ReSTIR 的 RIS 框架结合。

### 10. A Generalizable Light Transport 3D Embedding for GI
- **类别**：Trial
- **主题**：用点云 + 线性复杂度 Transformer 学习跨场景的通用 GI 先验
- **原因**：第一个在数百万三角面的复杂室内场景上实现通用 GI 学习的方法。输入 3D 场景（几何+材质+光源），输出 irradiance/radiance field，无需 rasterized 或 path-traced 线索。view-independent、resolution-agnostic。可微，可用于 path guiding 初始化。
- **来源**：Bing Xu et al. (NVIDIA/UCSD), SIGGRAPH 2026. arXiv:2510.18189. https://bingxu.tech/papers/light_transport_model_bing_2025.pdf
- **备注**：与 ReSTIR 互补——可作为 ReSTIR 的初始候选分布（jump-start path guiding），或替代 low-bounce 的间接光估计。项目页标注代码 coming。

### 11. Neural Incident Radiance Cache (NIRC) / Neural Two-Level Monte Carlo
- **类别**：Trial
- **主题**：用 tiny neural network 学习 incoming radiance，结合 Two-Level MC 实现无偏实时 GI
- **原因**：NIRC 学习 $L_i$（而非 NRC 的 $L_o$），允许在 primary surface 直接调用而无需额外 rays。通过 Two-Level MC 估计 residual error 补偿 bias，实现无偏结果。NIRC 单次评估比 NRC 快 5–10×。Eurographics 2025 Best Paper Honorable Mention。
- **来源**：KIT, Eurographics 2025. https://mishok43.github.io/nirc/
- **备注**：与 ReSTIR 的 synergy 明显：ReSTIR 负责 direct/many-light sampling，NIRC 负责 indirect bounce 估计。两者结合可能实现更高质量的实时 GI。

### 12. Real-Time Global Illumination for Dynamic 3D Gaussian Scenes
- **类别**：Trial
- **主题**：为 3D Gaussian Splatting 场景构建实时 GI 管线，支持动态材质和光照
- **原因**：首次实现动态 3D Gaussian 场景的实时 GI（>40 fps @ 1080p）。推导了基于 surface 的 LTE 用于 3D Gaussians，提出 compound stochastic ray tracing 和 two-level radiance cache（screen probes + hash grid）。与 mesh 混合场景兼容。
- **来源**：arXiv:2503.17897v2 (2026). 代码未公开但 pipeline 描述足够详细。
- **备注**：如果你对 neural rendering + GI 交叉感兴趣，这是当前最实用的方案。可借鉴其 radiance cache 设计。

### 13. Gradient-Domain ReSTIR Path Tracing
- **类别**：Trial
- **主题**：将梯度域渲染与 ReSTIR 结合，通过 correlated sampling 加速图像差异估计
- **原因**：梯度域路径追踪通过采样像素间差异减少 variance。与 ReSTIR 结合需要新的 shift mapping 和 MIS 权重。对动态场景 re-rendering 有价值。
- **来源**：https://projects.shuangz.com/ReSTIR-GDPT-eg26/ , Eurographics 2026.
- **备注**：与 ReSTIR 直接相关，数学推导涉及 path difference 的 Jacobian。

### 14. Stochastic Pairwise MIS for Unbiased Large-Kernel Reuse in Real-Time
- **类别**：Trial
- **主题**： stochastic 版本的 resampling MIS 权重，支持从更大空间邻域中无偏复用
- **原因**：传统 ReSTIR 的 spatial reuse 受限于 MIS 权重复杂度。本文通过 stochastic pairwise MIS 扩展了有效 reuse 范围，对高分辨率/复杂场景有价值。
- **来源**：Hedstrom et al., Eurographics 2026. Tzu-Mao Li 主页有引用。
- **备注**：改进 ReSTIR 空间重采样的理论扩展。

### 15. ReSTIR BDPT: Bidirectional ReSTIR Path Tracing with Caustics
- **类别**：Trial
- **主题**：将 GRIS 扩展到 BDPT，包含 light tracing 和 caustics 处理
- **原因**：ReSTIR 此前主要限于 unidirectional PT。BDPT 版本支持 caustics 等复杂光路，通过扩展 GRIS 处理大量 BDPT 技术组合。SIGGRAPH 2025/2026 发表。
- **来源**：Hedstrom et al., ACM TOG (Presented at SIGGRAPH 2026). Tzu-Mao Li 主页。
- **备注**：如果你关注 ReSTIR 的 caustics 支持，这是必读。

### 16. Multi-Layer Reservoir Splatting for Temporal Reuse Under Disocclusion
- **类别**：Trial
- **主题**：在 disocclusion 区域通过多层 reservoir splatting 保持 temporal reuse
- **原因**：Reservoir Splatting (SIGGRAPH 2025) 的前向投影解决了 backprojection 的像素归属问题。多层扩展进一步处理遮挡断裂处的 reuse 退化。
- **来源**：Chris Wyman et al., SIGGRAPH 2026.
- **备注**：直接改进 ReSTIR 的 temporal reuse 鲁棒性。

---

## P2 — Assess（新兴，了解即可）

### 17. DiffusionRenderer（NVIDIA）/ 扩散模型用于 Relighting 和逆渲染
- **类别**：Assess
- **主题**：用视频扩散模型同时做神经逆渲染（提取 G-buffer）和正向渲染（生成光照效果）
- **原因**：CVPR 2025 论文。基于 NVIDIA Cosmos World Foundation Model。能从真实视频估计 depth/normal/albedo/metallic/roughness，然后重新打光。约 1K 分辨率，SDR。对实时 GI 的物理正确性不够，但展示了生成式 AI 对渲染管线的潜在冲击。
- **来源**：Liang et al., "DiffusionRenderer: Neural Inverse and Forward Rendering with Video Diffusion Models", CVPR 2025. https://www.fxguide.com/quicktakes/diffusing-reality-how-nvidia-reimagined-relighting/
- **备注**：不直接替代 ReSTIR，但了解其趋势。物理正确性不足，无法用于你的数学严谨性要求。

### 18. Neural Gaffer / DiLightNet / LightSwitch — 扩散模型 Relighting
- **类别**：Assess
- **主题**：用 diffusion model 对图像/物体进行重新打光
- **原因**：Neural Gaffer (NeurIPS 2024) 用 Zero-1-to-3 模型 + HDR 环境图做 relighting。DiLightNet 用 radiance cues + ControlNet 细粒度控制。LightSwitch (ICCV 2025) 用 material-guided diffusion 做多视图 relighting。都属于生成式方法，不保证物理正确。
- **来源**：Jin et al., Neural Gaffer, NeurIPS 2024. DiLightNet, 2024. Litman et al., LightSwitch, ICCV 2025.
- **备注**：了解即可。对实时 GI 研究者而言，这些方法缺乏可推导的积分公式。

### 19. GI-GS: Global Illumination Decomposition on Gaussian Splatting
- **类别**：Assess
- **主题**：在 3D Gaussian Splatting 上分解全局光照，实现逆渲染和重新打光
- **原因**：将 deferred shading 与轻量 path tracing 结合，分解直接/间接光照。HDR 环境图驱动。实时性能。局限：不考虑间接光照的 specular component（作者明确承认这是 long-standing challenge）。
- **来源**：Chen et al., HKUST. arXiv:2410.02619. ICLR 2025.
- **备注**：3DGS + GI 的实用化尝试。其"不考虑 specular GI"的局限恰好是你的 ReSTIR 专长可切入的方向。

### 20. EAG-PT: Emission-Aware Gaussians and Path Tracing
- **类别**：Assess
- **主题**：将 3D Gaussian 作为路径追踪 primitive，用 OptiX 做真正的 Monte Carlo GI
- **原因**：所有 primitive 存为 2D/3D Gaussians，用 BVH + 二次方程求解光线-高斯交点。发射、散射、间接光均递归累积。然后去噪。PSNR ≈ 29dB，优于 naive 方法。概念验证性质。
- **来源**：2026 相关工作。Condor et al. (2024) 的 volumetric Gaussian 基础。Yang et al. (2026) 扩展。
- **备注**：将 neural primitive 与物理正确路径追踪结合的方向。目前处于概念验证。

### 21. DIAMOND-SSS: Diffusion-Augmented Subsurface Scattering
- **类别**：Assess
- **主题**：用 diffusion 模型从极少视图（10 张）重建 translucent 材质
- **原因**：将扩散模型用于 novel-view synthesis 和 relighting，conditioned on 估计几何。可替换 95% 缺失的捕获数据。对次表面散射的 GI 应用有启发。
- **来源**：arXiv:2601.12020 (2026).
- **备注**：过于 specialized。了解其数据增强思路即可。

### 22. LumiMotion: Gaussian Relighting with Scene Dynamics
- **类别**：Assess
- **主题**：利用动态区域作为监督信号，解耦材质与光照
- **原因**：运动揭示同一表面在不同光照下的变化，提供更强的 disentanglement 线索。动态 2D Gaussian Splatting。发布 synthetic benchmark。
- **来源**：arXiv:2604.10994 (2026).
- **备注**：逆渲染方向，对实时 GI 的直接贡献有限。

### 23. DLSS 4.5 / Multi-Frame Generation（第二代 Transformer）
- **类别**：Assess
- **主题**：NVIDIA 第二代 Transformer 超分辨率 + 动态多帧生成
- **原因**：计算量提升 5×，训练数据集更大。Performance 模式画质接近原生。RTX 50 系独占。对实时渲染的 frame rate 提升显著，但属于"帧生成"而非 GI 算法本身。
- **来源**：NVIDIA CES 2026. DLSS 4.5 Technical Blog. 250+ 游戏支持。
- **备注**：作为实时 GI 的输出后处理环节值得了解，但不属于你的 ReSTIR 核心研究领域。

### 24. Parameter-Space ReSTIR for Differentiable and Inverse Rendering
- **类别**：Assess
- **主题**：将 ReSTIR 扩展到可微渲染，在梯度下降迭代间复用样本
- **原因**：通过参数空间重构，用 FGRIS 估计器实现 resampled derivative estimates 的理论零方差收敛。对逆渲染有意义，但 differentiable rendering 的梯度误差与优化收敛速度关系尚不明确。
- **来源**：Chang et al., SIGGRAPH 2023. https://weschang.com/publications/restir-dr/restir-dr.pdf
- **备注**：如果你的 ReSTIR 研究延伸到逆渲染/材质优化，这是重要基础。目前偏离线应用。

---

## P3 — Hold（暂时观望或已被替代）

### 25. 纯 NeRF 用于实时 GI（原始 NeRF / Instant-NGP 等）
- **类别**：Hold
- **原因**：3D Gaussian Splatting (3DGS) 在实时渲染速度上全面超越 NeRF（100–200× 更快）。NeRF 的训练时间、VRAM 需求、渲染速度均不适用于实时 GI。3DGS 已达 60–200 fps，NeRF 仅 1–15 fps。
- **来源**：Kerbl et al., 3D Gaussian Splatting, ACM TOG 2023. 2026 对比评测：polyvia3d.com
- **备注**：NeRF 在离线/反射/折射场景仍有 niche，但实时 GI 已被 3DGS 替代。

### 26. 纯基于扩散模型的渲染替代路径追踪
- **类别**：Hold
- **原因**：DiffusionRenderer、NVIDIA Cosmos 等展示了生成式渲染的潜力，但当前输出分辨率约 1K，SDR，无法保证物理正确性和多视角一致性。生产管线（VFX/Archviz）仍将其用于 previz/迭代，最终输出仍用传统路径追踪。
- **来源**：SuperRenders Farm 2026 Analysis.
- **备注**：趋势是 hybrid（AI 加速 + 物理渲染），而非替代。不适合你的数学严谨性要求。

### 27. V-Ray 2026 AI Material Engine / 封闭生态 AI 工具
- **类别**：Hold
- **原因**：Chaos 的 AI Material Engine 从参考图生成 PBR 材质，功能封闭，无论文细节，无开源实现。对研究者意义有限。
- **来源**：V-Ray 2026 Product Announcement.
- **备注**：如果你关注材质生成，应转向 PBR3DGen (AAAI 2026) 或 Material Anything (CVPR 2025) 等公开论文。

### 28. Unity 6.5 OptiX Denoiser 弃用事件
- **类别**：Hold
- **原因**：Unity 弃用 OptiX 转投 OIDN 是生态选择，对 ReSTIR/GI 研究者而言只是工具链变动。注意 OIDN 3 的 temporal denoising 将在 2026 下半年发布，届时可重新评估。
- **来源**：Unity 6.5 Release Notes, CG Channel 2026/06.
- **备注**：非技术前沿，是生态信号。保持关注 OIDN 3 即可。

---

## 搜索覆盖范围与遗漏声明

### 已搜索的会议与来源
- **SIGGRAPH 2026** (Conference Track): 已确认条件接受论文，ReSTIR 相关论文约 5 篇
- **Eurographics 2026 / EGSR 2026**: ReSTIR GDPT、Stochastic Pairwise MIS 等
- **HPG 2026**: ReSTIR CGNS、ReSTIR Subsurface Scattering 等
- **SIGGRAPH Asia 2025**: ReSTIR PG、ReSTIR BDPT 等
- **CVPR / NeurIPS / ICCV / AAAI 2026**: DiffusionRenderer、Neural Gaffer、PBR3DGen 等
- **NVIDIA/Intel 官方 SDK**: OptiX 8.1, NTC SDK v0.9, OIDN 2.x/3.0 路线图
- **arXiv 2025–2026**: GI-GS、EAG-PT、LumiMotion、DIAMOND-SSS 等
- **硬件趋势**: RTX 5090 (Blackwell)、AMD RDNA 4、Intel Arc Battlemage

### 可能遗漏
- **SIGGRAPH 2026 完整论文列表**尚未正式发布（仅条件接受 ID 列表），7 月会议后可能有更多 ReSTIR 变体。
- **Eurographics 2025 的 Neural Two-Level Monte Carlo** 已覆盖，但需关注其 SIGGRAPH 2025 演讲后的更新。
- **日本/亚洲研究者**的 ReSTIR 相关工作（如 Ouyang 等）的 2026 新作可能未完全覆盖。
- **工业界未发表技术**（如 Unreal Engine 6、NVIDIA 内部 ReSTIR 改进）无公开信息。

---

## 推荐阅读优先级（针对 ReSTIR 研究者）

| 优先级 | 论文/技术 | 理由 |
|--------|----------|------|
| ★★★★★ | GRIS (SIGGRAPH 2022) + 课程笔记 | ReSTIR 数学底座 |
| ★★★★★ | ReSTIR PG (SIGGRAPH Asia 2025) | 直接扩展 ReSTIR，闭环 guiding-resampling |
| ★★★★☆ | ReSTIR LoD (SIGGRAPH 2026) | 实用化扩展：LoD 支持 |
| ★★★★☆ | CGNS (HPG 2026) | 代码开源，可立即集成 |
| ★★★★☆ | Neural Quadrature Rule (SIGGRAPH 2026) | 采样理论创新，可能与 RIS 结合 |
| ★★★☆☆ | NIRC (Eurographics 2025) | 与 ReSTIR 互补的 indirect 估计 |
| ★★★☆☆ | Light Transport 3D Embedding (SIGGRAPH 2026) | 通用 GI 先验，可 bootstrap ReSTIR |
| ★★☆☆☆ | DiffusionRenderer / Neural Gaffer | 了解生成式趋势，不深入 |

---

*Generated by research agent on 2026-07-03. Sources verified via kimi_search_v2.*
