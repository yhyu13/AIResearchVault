# ReSTIR & 全局光照 学术进展 — 2026 年 5–7 月技术雷达

> 调研日期：2026-07-03
> 覆盖窗口：2026 年 5–7 月（含即将召开的 SIGGRAPH 2026 会议论文）
> 研究员：研究员_A（ReSTIR & 全局光照 学术进展）

---

## 1. Adopt（已成熟，建议投入生产/深度研读）

### 1.1 ReSTIR PT Enhanced: Algorithmic Advances for Faster and More Robust ReSTIR Path Tracing
- **类别**：Adopt
- **类型**：论文 / 工业级实现
- **主题**：ReSTIR PT 的算法级工程优化，使性能提升 2–3 倍、降低误差并提升鲁棒性
- **原因**：这是当前最接近生产就绪的 ReSTIR PT 实现。核心改进包括：
  1. 通过 reciprocal neighbor selection 将空间复用成本减半；
  2. 引入 footprint-based reconnection criteria 增强 shift mapping 鲁棒性；
  3. 使用 duplication maps 降低时空相关性；
  4. 将直接光照（DI）与全局光照（GI）统一进同一 reservoir 流；
  5. 颜色噪声与 disocclusion 噪声的针对性优化。
  对于用户当前研究 ReSTIR GI 的工作，这篇论文提供了工程落地的关键细节——特别是统一 DI/GI reservoir 的数学处理（pairwise MIS 的扩展）和 shift mapping 的稳健性条件，直接影响 Jacobian 推导的边界条件设计。
- **来源**：Daqi Lin, Markus Kettunen, et al. — *I3D 2026* (Proc. ACM Comput. Graph. Interact. Tech. 9(1), May 2026) 🏆 **Best Paper**
- **链接**：https://research.nvidia.com/labs/rtr/publication/lin2026restirptenhanced/
- **备注**：与用户的 ReSTIR GI 数学推导直接相关，建议精读第 4–5 节（shift mapping 优化与 MIS 权重设计），其中涉及的 Jacobian 约束条件与 reconnection criteria 的数学关系可补充到 GameDevVault 笔记中。

### 1.2 NVIDIA RTXDI SDK 3.0 (ReSTIR PT / ReSTIR GI)
- **类别**：Adopt
- **类型**：工业 SDK / 工具
- **主题**：NVIDIA 官方 ReSTIR 系列算法 SDK，支持 ReSTIR DI、GI 和 PT
- **原因**：RTXDI 3.0 已正式发布，将 ReSTIR PT 纳入 SDK 支持范围。这是目前最稳定的、经过工业验证的 ReSTIR 实现框架。Unreal Engine 的 NvRTX Experimental Branch 已集成该 SDK。代码开源，包含完整的加权蓄水池采样（WRS）实现和 GRIS 数学基础。
- **来源**：NVIDIA RTXDI SDK 3.0.0
- **链接**：https://github.com/NVIDIA-RTX/RTXDI
- **备注**：可直接用于验证个人的 ReSTIR 数学推导。SDK 中的 SpatialResampling 和 TemporalResampling 实现与用户关心的 contribution weight 计算和 MIS 权重一致。

### 1.3 Unreal Engine NvRTX Experimental Branch
- **类别**：Adopt
- **类型**：引擎 / 工具
- **主题**：NVIDIA RTX 实验分支，集成 ReSTIR GI、ReSTIR PT、Mega Geometry
- **原因**：NvRTX 实验分支已支持 ReSTIR GI 和 ReSTIR PT，并配合 RTX Mega Geometry 实现 Nanite 几何体的实时光追路径追踪。这是游戏工业界验证 ReSTIR 算法在生产管线中可行性的重要标志。NVIDIA 的 GDC 2025 技术展示即基于此分支。
- **来源**：NVIDIA UE5 RTX Branch (Experimental)
- **链接**：https://developer.nvidia.com/game-engines/unreal-engine/rtx-branch
- **备注**：如果用户计划将 ReSTIR 研究落地到引擎中，这是必须跟踪的代码基线。注意 Substrate 材质与 ReSTIR GI 的兼容性仍在修复中（社区已知问题）。

---

## 2. Trial（有潜力，值得跑 Demo / 深入研究）

### 2.1 Real-Time Level-of-Detail Rendering with ReSTIR
- **类别**：Trial
- **类型**：论文（SIGGRAPH 2026 Conference Track）
- **主题**：允许 ReSTIR 在几何 LoD 切换时保持时空样本复用
- **原因**：传统 ReSTIR 要求相邻帧的 mesh 拓扑一致，当几何体切换 LoD 时，shift mapping 因顶点索引/重心坐标变化而失效。本工作提出一种基于 UV 映射的 surface point mapping，将不同拓扑层级间的顶点建立可逆映射，从而在 LoD 变化时仍能维持 temporal reuse。核心创新在于：
  - 引入了基于 UV 的顶点匹配算法解决非单射 UV 映射的歧义；
  - 证明了该映射在 GRIS 框架下保持 Jacobian 计算的一致性。
  对于处理动态复杂场景的用户，这是解决 ReSTIR 在 production 中遇到的几何变化问题的关键论文。
- **来源**：Wang, Kettunen, Lin, Wyman, Wu, Zhao — *SIGGRAPH 2026* (July 2026)
- **链接**：https://research.nvidia.com/labs/rtr/publication/wang2026levelofdetail/
- **备注**：论文中 Figure 5 的 Jacobian 分析直接涉及 change-of-variables 的推导，与用户关心的数学严谨性高度相关。建议关注 Section 4.4 的映射构造。

### 2.2 Multi-Layer Reservoir Splatting for Temporal Reuse Under Disocclusion
- **类别**：Trial
- **类型**：论文（SIGGRAPH 2026 Conference Track）
- **主题**：基于多层蓄水池 splatting 的遮挡区域时间复用
- **原因**：Disocclusion 是 ReSTIR 时间复用的致命弱点——新暴露区域无法从上一帧借用样本。Reservoir Splatting（SIGGRAPH 2025）将样本反向投影到历史帧以实现运动模糊和时间复用。本工作将其扩展为多层 splatting，解决遮挡移除后的 temporal reuse 问题。这是从 SIGGRAPH 2025 的 Reservoir Splatting 自然演进的工作，对处理动态相机/物体的场景质量提升显著。
- **来源**：Jeffrey Liu, Daqi Lin, Markus Kettunen, Chris Wyman, Ravi Ramamoorthi — *SIGGRAPH 2026* (July 2026)
- **链接**：https://cwyman.org/paperList.html
- **备注**：Reservoir Splatting 的核心数学是 MIS 权重在 pixel filter 积分域上的推导，本工作的多层扩展需要重新证明 unbiasedness。值得跟踪其 supplemental 中的推导细节。

### 2.3 Compatibility-Guided Neighbor Selection (CGNS) for ReSTIR
- **类别**：Trial
- **类型**：论文（HPG 2026）+ 开源实现
- **主题**：用几何兼容性度量替代空间复用的随机邻居选择
- **原因**：标准 ReSTIR 的空间复用从半径内均匀随机选邻居，当邻居的几何与当前像素差异大时，shift mapping 失败率高。CGNS 提出：
  1. 从准随机圆盘采样 K 个候选邻居；
  2. 用基于位置+法线的兼容性启发式评分；
  3. 通过加权蓄水池采样（WRS）从中选出 M 个最兼容的邻居参与空间复用。
  该方法在几乎不增加 runtime overhead 的情况下显著提升空间复用质量。作者已开源完整实现，基于 Falcor 8.0 框架。
- **来源**：Orion Junkins, Markus Kettunen, Daqi Lin, Ravi Ramamoorthi, Chris Wyman — *HPG 2026* (Proc. ACM Comput. Graph. Interact. Tech. 9(4), July 2026) 🏆 **Best Paper**
- **链接**：
  - 论文：https://dl.acm.org/doi/10.1145/3820024
  - 代码：https://github.com/orion-junkins/ReSTIR-CGNS
- **备注**：代码仓库中的 CGNSUtils.slang 包含兼容性评分的精确实现，WRSReservoir.slang 包含 A-Chao 和 A-ES 两种 WRS 变体。用户可直接用于验证自己的数学推导。

### 2.4 Stochastic Pairwise MIS for Unbiased Large-Kernel Reuse in Real Time
- **类别**：Trial
- **类型**：论文（Eurographics 2026）+ 预印 PDF
- **主题**：用随机 pairwise MIS 实现从大规模邻居集合中的无偏复用
- **原因**：标准 ReSTIR 只从少量（通常 M=3）邻居中复用，在 disocclusion 或运动区域质量下降。增大 M 会导致计算成本剧增。本文提出：
  - 将像素按 GBuffer 法线、Object ID 和 Tile ID 分类为 8x8 的 cell；
  - 随机选取一个 cell，然后仅评估该 cell 内的高贡献候选（N_bar=3）；
  - 通过随机化 resampling MIS weight m_hat 保证无偏性：E_Z[m_hat(Y_i; Z) | X_hat, W_hat] = m_i(Y_i)。
  这使得实际评估的候选数远小于理论邻居池，同时保持无偏。核心公式（Equation 13-14）给出了 stochastic MIS 的数学构造，与 GRIS 的 contribution weight 公式直接兼容。
- **来源**：Trevor Hedstrom, Markus Kettunen, Daqi Lin, Chris Wyman, Tzu-Mao Li — *Eurographics 2026* (Computer Graphics Forum 45(2), May 2026)
- **链接**：https://research.nvidia.com/labs/rtr/publication/hedstrom2026stochastic/
- **备注**：这篇论文的数学核心——随机化 MIS 权重的无偏性证明（Appendix A）——与用户关注的无偏性证明直接相关。证明使用了条件期望的 tower property，与 GRIS 原始论文的推导风格一致，可纳入 GameDevVault 的推导笔记。

### 2.5 Bevy Solari 0.19 — 开源 ReSTIR GI 实现（Rust）
- **类别**：Trial
- **类型**：开源工具 / 引擎实现
- **主题**：Bevy 引擎的实时路径追踪渲染器，集成 ReSTIR DI + GI
- **原因**：Solari 是目前最活跃的开源 ReSTIR GI 实现之一，完全用 Rust 编写。0.19 版本（2026-04）的改进包括：
  - 改进空间采样：在弯曲表面和 mesh 缝隙等复杂几何区域，通过最多 5 次尝试+半径减半策略找到有效邻居；
  - 对光滑金属表面跳过 ReSTIR GI 计算（因为 diffuse contribution 为零）；
  - 修正 BRDF 的 lobe 选择和 Fresnel 计算；
  - 引入 RTXGI 风格的路径传播启发式（path spread cone）来终止路径。
  对于想理解 ReSTIR GI 工程实现细节的用户，这是极好的参考代码。
- **来源**：Bevy 0.19 Solari (开源项目)
- **链接**：https://jms55.github.io/posts/2026-04-12-solari-bevy-0-19/
- **备注**：该项目是理解 ReSTIR GI 在真实引擎中工程权衡的绝佳素材。代码开源，但需注意其 ReSTIR 实现相对于 NVIDIA 版本做了大量简化，适合学习但不适合直接复制到生产环境。

### 2.6 RoyalTracer-DX — 开源 DirectX12 ReSTIR PT
- **类别**：Trial
- **类型**：开源渲染器 / 代码参考
- **主题**：基于 DX12 的先进路径追踪器，集成无偏 ReSTIR PT 与统一 DI/GI reservoir
- **原因**：该开源渲染器实现了：
  - 统一 DI/GI reservoir：将 NEE、环境光 miss、路径积分候选全部汇入一个 reservoir 流，通过 sentinel matID 区分直接/间接样本；
  - 完整的 temporal + spatial reservoir resampling，使用 pairwise MIS；
  - temporal permutation sampling 去相关；
  - 基于 per-pixel duplication map 的 M_cap 调制，防止高度共享样本的相关性伪影。
  这些技术正是 ReSTIR PT Enhanced 论文中提到的工程优化点。
- **来源**：GitHub 开源项目 RoyalTracer-DX
- **链接**：https://github.com/ML200/RoyalTracer-DX
- **备注**：实现较为完整，但文档有限。用户可将其作为验证个人 ReSTIR 理解的代码对照。特别值得关注其 unified reservoir 的 MIS 权重处理。

---

## 3. Assess（新兴，需关注概念验证）

### 3.1 Gradient-Domain ReSTIR Path Tracing (ReSTIR G-PT)
- **类别**：Assess
- **类型**：论文（Eurographics 2026）+ 开源实现
- **主题**：首次将梯度域渲染（Gradient-Domain Rendering）与 ReSTIR 结合，实现实时梯度域路径追踪
- **原因**：梯度域渲染通过估计像素间颜色差分来加速图像合成，但此前无实时方法。本文提出：
  - 将 paired-pixel 样本（用于梯度估计）作为 ReSTIR 的复用单元，而非传统单一路径；
  - 设计了两种 shift mapping：一种用于梯度差分估计（pixel-pair correlation），另一种用于时空复用（GRIS）；
  - 利用梯度图像的稀疏性实现高度选择性的空间复用，在实时帧率下达到优于基线的质量。
  这是 ReSTIR 理论框架向梯度域自然扩展的尝试，但目前只停留在概念验证阶段，实际生产应用尚需时日。
- **来源**：Yu-Chen Wang, Markus Kettunen, Daqi Lin, Chris Wyman, Lifan Wu, Shuang Zhao — *Eurographics 2026* (CGF 45(2), May 2026)
- **链接**：
  - 论文：https://projects.shuangz.com/ReSTIR-GDPT-eg26/ReSTIR-GDPT-eg26.pdf
  - 代码：https://github.com/elite-sheep/gradient-restir
- **备注**：梯度域路径积分的 shift mapping 需要引入额外的 Jacobian 项（因为差分估计涉及路径空间上的差分算子）。论文中的推导涉及路径空间扩展的 change-of-variables，与用户的研究方向相关，但生产价值有限。

### 3.2 Spatio-Temporal Control Variates with ReSTIR for Real-Time Rendering
- **类别**：Assess
- **类型**：论文（SIGGRAPH 2026 Conference Track）
- **主题**：将控制变量法（Control Variates）与 ReSTIR 结合，进一步降低实时渲染方差
- **原因**：控制变量法是经典方差削减技术，但此前未被系统性地整合进 ReSTIR 的时空复用框架。本文提出在 ReSTIR 的时空采样中引入 spatio-temporal control variates，利用相邻像素和帧的局部线性关系构造低方差估计。该方法与 ReSTIR 的 MIS 权重系统兼容，理论上可以进一步压低现有 ReSTIR 方法的残余方差。目前只看到会议标题，论文细节待 SIGGRAPH 2026 召开后确认。
- **来源**：Zhong Shi, Cunhao Wu (Tsinghua), Lifan Wu (NVIDIA), Kun Xu (Tsinghua) — *SIGGRAPH 2026* (July 2026, Los Angeles)
- **链接**：https://kesen.realtimerendering.com/sig2026.html
- **备注**：控制变量法与 ReSTIR 的无偏性约束需要仔细调和——如果 control variate 的期望计算有误，会引入系统性偏差。用户应关注其无偏性证明如何处理 control variate 与 GRIS contribution weight 的交互。

### 3.3 A Generalizable Light Transport 3D Embedding for Global Illumination
- **类别**：Assess
- **类型**：论文（SIGGRAPH 2026 Conference Track）
- **主题**：用可泛化的 3D 嵌入直接预测全局光照，无需逐场景训练
- **原因**：与 ReSTIR 的蒙特卡洛路径采样哲学不同，这项工作走神经渲染路线：将场景表示为点云，用线性复杂度 Transformer 编码长程光传输，在百万级三角面片上实现可泛化 GI 预测。它代表了与 ReSTIR 互补的另一条技术路线——用学习替代采样。对于研究 ReSTIR 的用户，这提供了一个"如果采样效率遇到瓶颈，学习是否是出路"的参考视角。但注意：该方法目前只能预测 diffuse GI，对 glossy/specular 材质的处理尚不明确。
- **来源**：Bing Xu, Mukund Varma T, Cheng Wang, Tzu-Mao Li, Lifan Wu, Bart Wronski, Ravi Ramamoorthi, Marco Salvi — *SIGGRAPH 2026* (July 2026)
- **链接**：https://arxiv.org/abs/2510.18189
- **备注**：与 ReSTIR 无直接关系，但用户若想拓展研究视野到"神经光传输"，这是一篇高质量的起点论文。其 Transformer 的线性复杂度设计对大规模场景有启发意义。

### 3.4 EA ORCA: Full Path Tracing on PS5 Pro (F1 25 Demo)
- **类别**：Assess
- **类型**：工业 Demo / GDC 2026 展示
- **主题**：EA 与 SEED R&D 合作在 PS5 Pro 上实现 30fps 全路径追踪
- **原因**：EA 在 GDC 2026 展示了 F1 25 的完整路径追踪版本，内部渲染 1080p + PSSR 上采样到 4K。核心技术栈：
  - ReSTIR 用于高效光源采样（处理 325,000 动态光源）；
  - ReGIR 用于空间光源预选；
  - 层次化光源结构避免 "light soup"；
  - EA 自研 ORCA 技术将基础帧率从 20fps 提升到 30fps，最大优化来自间接光照。
  这是 ReSTIR 在主机平台上处理极端复杂光照条件的工业验证，展示了当前技术的工程天花板。
- **来源**：EA SEED R&D, GDC 2026 (March 2026)
- **链接**：https://twistedvoxel.com/f1-25-runs-on-ps5-pro-with-full-path-tracing-gdc-2026/
- **备注**：该技术为专有方案，公开细节有限。但证明了 ReSTIR + 智能光源管理可以支撑 300k+ 动态光源的实时路径追踪。用户可关注其 "hierarchical light structures" 的公开技术描述。

### 3.5 ReSTIR BDPT: Bidirectional ReSTIR Path Tracing with Caustics
- **类别**：Assess
- **类型**：论文（ACM TOG 2025，将于 SIGGRAPH 2026 展示）
- **主题**：将双向路径追踪（BDPT）与 GRIS 结合，实现实时焦散渲染
- **原因**：这是将 ReSTIR 从单向路径追踪扩展到双向路径追踪的重大尝试。核心创新：
  - 在 path-technique pair 空间中应用 GRIS，用 technique-specific MIS 权重保持无偏；
  - 对 camera subpath 使用 hybrid shift，对 light subpath 使用 random replay；
  - 引入 caustic reservoir 实现焦散的无偏时间累积。
  然而，当前实现约 50ms/帧（交互级而非实时级），且内存占用高达 8.2 GB（1920x1080），距离生产部署仍有差距。但其在理论上证明了 GRIS 可以容纳 BDPT 的复杂 technique 空间。
- **来源**：Trevor Hedstrom, Markus Kettunen, Daqi Lin, Chris Wyman, Tzu-Mao Li — *ACM TOG 44(5), Sep 2025* (presented at SIGGRAPH 2026)
- **链接**：https://dl.acm.org/doi/10.1145/3744898
- **备注**：BDPT 的 MIS 权重递归计算（van Antwerpen 2011 的递归 MIS 变体）是该论文的数学核心。对于用户而言，理解该技术如何将 GRIS 的 shift mapping 和 Jacobian 扩展到多 technique 场景非常有价值，但工程复杂度极高，不建议立即投入实现。

---

## 4. Hold（已被替代或尚不成熟）

### 4.1 纯 Light Tree / Lightcuts 采样方案
- **类别**：Hold
- **类型**：传统算法
- **主题**：基于层次化光源聚类的直接光照采样
- **原因**：ReSTIR 及其后续工作（ReSTIR DI/GI/PT）在几乎全场景下超越了传统 Light Tree 方案。Light Tree 的 O(log N) 每像素成本在光源数量增加时仍显著高于 ReSTIR 的 O(1) 成本。此外，Light Tree 对动态光源的更新开销在实时场景中不可接受。除非在特定场景下（如需要严格确定性采样的离线渲染），否则已被 ReSTIR 家族全面替代。
- **来源**：Lightcuts (2005) 及其后续改进
- **链接**：-
- **备注**：用户若在学习历史方法，了解 Light Tree 作为 ReSTIR 的对比基线即可，无需投入实现。

### 4.2 纯 Screen-Space 全局光照（SSAO / SSR / SSGI）
- **类别**：Hold
- **类型**：传统实时近似技术
- **主题**：基于屏幕空间的光线投射/遮蔽近似全局光照
- **原因**：随着硬件光追（RTX 30/40/50 系）的普及，基于屏幕空间的 GI 近似（如 SSAO、SSR、早期的 SSGI）在物理正确性和动态场景适应性上已被 ReSTIR GI/PT 和 DDGI 等方案全面超越。当前 UE5 Lumen 的 Surface Cache + Hardware Ray Tracing 混合方案已经覆盖了传统 Screen-Space GI 的应用场景。纯屏幕空间方案由于缺少屏幕外信息和物理不正确性，已不适合新项目采用。
- **来源**：Crytek SSAO (2007), SSR, SSGI 等
- **链接**：-
- **备注**：用户若研究 ReSTIR GI，SSAO/SSR 只需作为反面教材理解其局限性。

---

## 附录：2026 年 ReSTIR 相关会议论文清单（按会议排序）

| 会议 | 论文 | 作者 | 类别建议 |
|------|------|------|----------|
| SIGGRAPH 2026 | Multi-Layer Reservoir Splatting for Temporal Reuse Under Disocclusion | Liu, Lin, Kettunen, Wyman, Ramamoorthi | Trial |
| SIGGRAPH 2026 | Real-Time Level-of-Detail Rendering with ReSTIR | Wang, Kettunen, Lin, Wyman, Wu, Zhao | Trial |
| SIGGRAPH 2026 | Spatio-Temporal Control Variates with ReSTIR for Real-Time Rendering | Shi, Wu, Wu, Xu | Assess |
| SIGGRAPH 2026 | A Generalizable Light Transport 3D Embedding for GI | Xu, Li, Wu, et al. | Assess |
| HPG 2026 | Compatibility-Guided Neighbor Selection for ReSTIR | Junkins, Kettunen, Lin, Ramamoorthi, Wyman | Trial |
| I3D 2026 | ReSTIR PT Enhanced: Algorithmic Advances for Faster and More Robust ReSTIR Path Tracing | Lin, Kettunen, et al. | Adopt |
| Eurographics 2026 | Stochastic Pairwise MIS for Unbiased Large-Kernel Reuse in Real Time | Hedstrom, Kettunen, Lin, Wyman, Li | Trial |
| Eurographics 2026 | Gradient-Domain ReSTIR Path Tracing | Wang, Kettunen, Lin, Wyman, Wu, Zhao | Assess |

---

*报告结束。如需进一步展开某篇论文的数学推导细节或代码实现分析，请指示。*
