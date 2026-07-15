# Milestone Papers in Time-Series Analysis (2023 – Mid-2026)

> **Curated:** July 2026  
> **Scope:** Foundational, widely-cited, direction-opening, and breakthrough papers in time-series forecasting, analysis, and foundation models. Incremental works are excluded.  
> **Coverage:** 2023 – July 2026 (inclusive of late-2022 papers that catalyzed the 2023+ wave).

---

## Table of Contents

1. [Foundational Architectures & Transformers (2023–2024)](#1-foundational-architectures--transformers-20232024)
2. [Time Series Foundation Models – The Paradigm Shift (2023–2026)](#2-time-series-foundation-models--the-paradigm-shift-20232026)
3. [LLM-Aligned & Multimodal Time Series (2023–2026)](#3-llm-aligned--multimodal-time-series-20232026)
4. [Diffusion & Generative Models for Time Series (2023–2026)](#4-diffusion--generative-models-for-time-series-20232026)
5. [Anomaly Detection, Robustness & Specialized Tasks (2023–2026)](#5-anomaly-detection-robustness--specialized-tasks-20232026)
6. [Benchmarks, Evaluation & Comprehensive Surveys (2023–2026)](#6-benchmarks-evaluation--comprehensive-surveys-20232026)

---

## 1. Foundational Architectures & Transformers (2023–2024)

These papers established the core architectural primitives that underpin virtually all subsequent time-series deep learning. They either introduced novel inductive biases, exposed critical flaws in prior approaches, or demonstrated that radical simplicity could outperform complexity.

---

**1. PatchTST: A Time Series is Worth 64 Words: Long-Term Forecasting with Transformers**  
*Yuqi Nie, Nam H. Nguyen, Phanwadee Sinthong, Jayant Kalagnanam*  
**ICLR 2023** | arXiv:2211.14730  
> **Why milestone:** Introduced the now-ubiquitous "patching" paradigm for time-series Transformers—segmenting series into subseries-level patches to retain local semantics while reducing attention-map complexity. Combined with channel-independence and instance normalization, PatchTST became the architectural template for virtually every subsequent Transformer-based forecaster, including TimesFM and Timer. It proved that vanilla Transformers, when properly patched, could dominate long-term forecasting without exotic attention mechanisms.

---

**2. iTransformer: Inverted Transformers Are Effective for Time Series Forecasting**  
*Yong Liu, Tengge Hu, Haoran Zhang, Haixu Wu, Shiyu Wang, Lintao Ma, Mingsheng Long*  
**ICLR 2024 (Spotlight)** | arXiv:2310.06625  
> **Why milestone:** Flipped the Transformer architecture on its axis by applying attention across **variate tokens** (each variable's full time series) rather than across time steps. This inverted design elegantly captures multivariate correlations while using feed-forward networks to model temporal nonlinearity per variate. iTransformer achieved state-of-the-art across real-world benchmarks and catalyzed the "channel-as-token" design philosophy now central to models like Timer-XL and Sundial. It has been cited over 4,000 times, making it one of the most influential time-series papers of the decade.

---

**3. TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis**  
*Haixu Wu, Tengge Hu, Yong Liu, Hang Zhou, Jianmin Wang, Mingsheng Long*  
**ICLR 2023** | arXiv:2210.02186  
> **Why milestone:** First to systematically exploit **multi-periodicity** by transforming 1D time series into 2D tensors (intra-period vs. inter-period variations), then applying 2D convolutional kernels (Inception blocks). TimesNet achieved consistent state-of-the-art across **five** mainstream tasks—forecasting, imputation, classification, anomaly detection, and short-term forecasting—establishing the proof-of-concept that a single architecture could generalize across diverse time-series tasks. It directly inspired the "task-general backbone" philosophy later adopted by foundation models.

---

**4. DLinear / Are Transformers Effective for Time Series Forecasting?**  
*Ailing Zeng, Muxi Chen, Lei Zhang, Qiang Xu*  
**AAAI 2023** | arXiv:2205.13504  
> **Why milestone:** The paper that ignited the "Transformer skepticism" debate. By showing that a embarrassingly simple one-layer linear model (DLinear) with direct multi-step forecasting and trend-seasonal decomposition outperformed complex Transformer-based models by 20–50%, it forced the community to re-evaluate whether self-attention was actually necessary for time-series forecasting. DLinear became the mandatory baseline for all subsequent forecasting papers and directly motivated the pivot toward foundation models and alternative architectures (e.g., MLP-Mixers, state-space models).

---

**5. TSMixer: An All-MLP Architecture for Time Series Forecasting**  
*Si-An Chen, Chun-Liang Li, Nate Yoder, Sercan O. Arik, Tomas Pfister*  
arXiv:2303.06053 / KDD 2023 variant (Ekambaram et al.)  
> **Why milestone:** Demonstrated that MLP-Mixer architectures—stacking temporal mixing and channel mixing MLPs—could match or exceed Transformer performance while being significantly more parameter-efficient. TSMixer (and its lightweight KDD 2023 variant by Ekambaram et al.) proved that cross-channel and cross-temporal interactions could be learned without attention, opening the door to efficient, hardware-friendly forecasting models and inspiring later MLP-based work like TimeMixer.

---

**6. N-HiTS: Neural Hierarchical Interpolation for Time Series Forecasting**  
*Cristian Challu, Kin G. Olivares, Boris N. Oreshkin, Federico Garza Ramirez, Max Mergenthaler-Canseco, Artur Dubrawski*  
**AAAI 2023**  
> **Why milestone:** Extended the N-BEATS paradigm with hierarchical interpolation and multi-rate signal sampling, enabling a single model to capture multiple frequency components dynamically. It significantly improved long-horizon prediction stability and reduced volatility, serving as a strong baseline for hierarchical and multi-scale forecasting. Its interpolation mechanism influenced later multi-resolution designs in foundation models.

---

**7. FEDformer: Frequency Enhanced Decomposed Transformer for Long-Term Series Forecasting**  
*Tian Zhou, Ziqing Ma, Qingsong Wen, Xue Wang, Liang Sun, Rong Jin*  
**ICML 2022** (catalyzed 2023+ work) | arXiv:2201.12740  
> **Why milestone:** Pioneered the fusion of classical frequency-domain analysis (Fourier transforms) with deep learning by using frequency-enhanced attention and seasonal-trend decomposition. It proved that spectral information could be injected into neural architectures without losing end-to-end differentiability, spawning a sub-field of "frequency-aware" forecasting models (e.g., FreDF, Fourier-adaptive diffusion) and remains a standard benchmark baseline.

---

**8. Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting**  
*Haixu Wu, Jiehui Xu, Jianmin Wang, Mingsheng Long*  
**NeurIPS 2021** (catalyzed 2023+ work) | arXiv:2106.13008  
> **Why milestone:** Introduced the deep decomposition architecture and series-wise auto-correlation mechanism, replacing point-wise self-attention with period-based dependency discovery. Autoformer established that explicitly modeling periodicity and trend-seasonality inside a neural network was not only feasible but essential for long-term forecasting. It is the most-cited time-series Transformer paper and the architectural ancestor of TimesNet, FEDformer, and Non-stationary Transformer.

---

**9. Non-stationary Transformers: Exploring the Stationarity in Time Series Forecasting**  
*Yong Liu, Haixu Wu, Jianmin Wang, Mingsheng Long*  
**NeurIPS 2022** (catalyzed 2023+ work)  
> **Why milestone:** Addressed the critical but overlooked problem of distribution shift in time-series forecasting by proposing series stationarization (to stabilize input distributions) and de-stationary attention (to restore intrinsic non-stationary information). This two-module framework became the standard preprocessing-and-recovery pipeline in virtually all subsequent forecasting models, including PatchTST and iTransformer. It fundamentally changed how the community handles non-stationarity.

---

**10. TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting**  
*Shiyu Wang, Haixu Wu, Xiaoming Shi, Tengge Hu, Huakun Luo, Lintao Ma, James Y. Zhang, Jun Zhou*  
**ICLR 2024**  
> **Why milestone:** Proposed a multiscale mixing architecture that decomposes and mixes temporal information at different scales (from fine to coarse) in a residual manner, explicitly disentangling short-term and long-term dynamics. It achieved strong results across multiple benchmarks and demonstrated that scale-aware architectures could outperform single-scale models, influencing the multi-resolution designs in later foundation models like Time-MoE.

---

**11. Koopa: Learning Non-Stationary Time Series Dynamics with Koopman Predictors**  
*Yong Liu, Chenyu Li, Jianmin Wang, Mingsheng Long*  
**NeurIPS 2023**  
> **Why milestone:** Bridged operator learning theory (Koopman operator) with deep forecasting by learning adaptive Koopman predictors that capture non-stationary dynamics. It offered a theoretically grounded alternative to black-box attention mechanisms and proved that physics-informed mathematical operators could be made learnable and data-adaptive for real-world time series.

---

**12. ModernTCN: A Modern Pure Convolution Structure for General Time Series Analysis**  
*Dongha Luo, Xue Wang*  
**ICLR 2024**  
> **Why milestone:** Revived pure convolutional architectures for time series by applying modern CNN design principles (large kernels, residual connections, channel-wise attention) to temporal data. It showed that properly designed CNNs could match Transformer performance on general time-series tasks while maintaining superior inference efficiency, providing a viable alternative to attention-based models.

---

**13. CARD: Channel Aligned Robust Blend Transformer for Time Series Forecasting**  
*Xue Wang, Tian Zhou, Qingsong Wen, Jinyang Gao, Bolin Ding, Rong Jin*  
**ICLR 2024**  
> **Why milestone:** Introduced the "Token Blend Module" that merges adjacent tokens within the same attention head after multi-head attention, creating richer, head-specific representations. It improved robustness across channels and demonstrated that careful token manipulation within standard Transformers could yield significant gains without architectural overhaul.

---

**14. Pathformer: Multi-Scale Transformers with Adaptive Pathways for Time Series Forecasting**  
*Peng Chen, Yingying Zhang, Yunyao Cheng, Yang Shu, Yihang Wang, Qingsong Wen, Bin Yang, Chenjuan Guo*  
**ICLR 2024**  
> **Why milestone:** Combined multi-scale patching with adaptive pathways, allowing the model to dynamically select appropriate temporal resolutions for different forecasting scenarios. It advanced the patch-based paradigm beyond fixed-size patches and demonstrated that adaptive granularity could improve both accuracy and efficiency.

---

**15. FITS: Modeling Time Series with 10k Parameters**  
*Zhijian Xu, Ailing Zeng, Qiang Xu*  
**ICLR 2024**  
> **Why milestone:** Radically challenged the "bigger is better" trend by showing that a frequency-domain interpolation model with only ~10,000 parameters could achieve competitive forecasting performance. It proved that extreme lightweight models were viable for time-series tasks, opening research avenues into edge-deployment and resource-constrained forecasting.

---
## 2. Time Series Foundation Models – The Paradigm Shift (2023–2026)

This is the most transformative movement in time-series research since deep learning. These papers demonstrate that large-scale pre-training on diverse temporal data enables zero-shot, few-shot, and cross-domain forecasting—mirroring the NLP/CV foundation-model revolution.

---

**1. TimeGPT-1: The First Foundation Model for Time Series**  
*Azul Garza, Max Mergenthaler-Canseco*  
**arXiv 2023** (Nixtla) | arXiv:2310.03589  
> **Why milestone:** The **first** publicly marketed and accessible foundation model for time-series forecasting. Built on an encoder-decoder Transformer with ~1B parameters and trained on 100B+ data points across finance, healthcare, energy, and IoT, TimeGPT proved that a single pre-trained model could perform zero-shot forecasting across domains with uncertainty quantification. It democratized foundation-model access via an open API and established the commercial viability of TSFMs.

---

**2. Chronos: Learning the Language of Time Series**  
*Abdul Fatir Ansari, Lorenzo Stella, Caner Turkmen, Xiyuan Zhang, Pedro Mercado, Huibin Shen, Oleksandr Shchur, Syama Sundar Rangapuram, Sebastian Pineda Arango, Shubham Kapoor, et al.*  
**TMLR 2024** (Amazon Science) | arXiv:2403.07815  
> **Why milestone:** Pioneered **tokenization-based** time-series modeling by discretizing continuous values into a vocabulary and training a T5-style encoder-decoder Transformer with cross-entropy loss. This "language-of-time-series" approach enabled zero-shot transfer to unseen datasets and established that discrete tokenization—borrowed from NLP—could work for temporal data. Chronos became a core baseline for all subsequent TSFM research and inspired Chronos-2 (2025), which scaled to universal multivariate forecasting.

---

**3. TimesFM: A Decoder-Only Foundation Model for Time-Series Forecasting**  
*Abhimanyu Das, Weihao Kong, Rajat Sen, Yichen Zhou*  
**ICML 2024** (Google Research) | arXiv:2310.10688  
> **Why milestone:** The first major **decoder-only** time-series foundation model (200M parameters), trained on 100B real-world time points from Google Trends, Wikipedia, and synthetic sources. It introduced input patching and patch-wise autoregressive prediction, enabling efficient long-horizon forecasting without per-dataset training. TimesFM proved that decoder-only architectures—like GPT for text—were highly effective for time series and achieved strong zero-shot results. It was later updated to TimesFM 2.0 (Dec 2024) with context lengths up to 2048 and became a top performer on GIFT-Eval.

---

**4. Moirai: Unified Training of Universal Time Series Forecasting Transformers**  
*Gerald Woo, Chenghao Liu, Akshat Kumar, Caiming Xiong, Silvio Savarese, Doyen Sahoo*  
**ICML 2024 (Oral)** (Salesforce AI Research) | arXiv:2402.02592  
> **Why milestone:** The first open-source TSFM to explicitly tackle **"any-variate"** forecasting—handling univariate, multivariate, and mixed-variable time series with a single model. Built on a masked encoder architecture (similar to BERT) and trained on the LOTSA dataset (27B observations, 9 domains), Moirai introduced multi-patch-size projections and achieved a ~70% win rate in zero-shot scenarios. Its open release (via Uni2TS library) catalyzed community TSFM research and established encoder-based TSFMs as a viable alternative to decoder-only models.

---

**5. MOMENT: A Family of Open Time-Series Foundation Models**  
*Mononito Goswami, Konrad Szafer, Arjun Choudhry, Yifu Cai, Shuo Li, Artur Dubrawski*  
**ICML 2024** (CMU) | arXiv:2402.03885  
> **Why milestone:** Addressed the three core barriers to TSFM development: (1) lack of large public datasets, (2) diverse time-series characteristics, and (3) absence of evaluation benchmarks. MOMENT compiled the **Time Series Pile** (large public dataset collection), introduced systematic multi-dataset pre-training recipes, and built a benchmark for limited-supervision settings. It has been downloaded 2M+ times on HuggingFace and applied to healthcare (EEG, PPG, ICP), fault diagnosis, and stellar flare forecasting. MOMENT proved that open, reproducible TSFM research was feasible.

---

**6. Timer: Generative Pre-Trained Transformers Are Large Time Series Models**  
*Yong Liu, Haoran Zhang, Chenyu Li, Xiangdong Huang, Jianmin Wang, Mingsheng Long*  
**ICML 2024** (THUML, Tsinghua) | arXiv:2402.02368  
> **Why milestone:** The first Chinese open-source TSFM, introducing the **Single-Series Sequence (S3)** format that unifies diverse time series into 1D sequences for decoder-only Transformer pre-training. Timer (84M parameters, trained on 260B points) was notable for being a **multi-task** foundation model—adapting to forecasting, imputation, and anomaly detection with minimal fine-tuning. It established the Tsinghua THUML lab as a leading TSFM research group and directly spawned Timer-XL and Sundial.

---

**7. Timer-XL: Long-Context Transformers for Unified Time Series Forecasting**  
*Yong Liu, Guo Qin, Xiangdong Huang, Jianmin Wang, Mingsheng Long*  
**ICLR 2025** (THUML, Tsinghua) | arXiv:2410.04803  
> **Why milestone:** Extended Timer to handle **arbitrary-length, any-variable, and covariate-informed** time series with a novel **TimeAttention** mechanism. Timer-XL unified univariate, multivariate, and exogenous-variable forecasting in a single model, achieving state-of-the-art zero-shot results on multiple benchmarks. It demonstrated that long-context decoder-only models could explicitly model cross-variable dependencies through attention, validating the "decoder-only is best for forecasting" hypothesis. It pre-trained on LOTSA + UTSD (1B points) and remains a top-tier TSFM.

---

**8. Sundial: A Family of Highly Capable Time Series Foundation Models**  
*Yong Liu, Guo Qin, Zhiyuan Shi, Zhi Chen, Caiyin Yang, Xiangdong Huang, Jianmin Wang, Mingsheng Long*  
**ICML 2025 Oral** (Top 1%) (THUML, Tsinghua) | arXiv:2502.00816  
> **Why milestone:** The current state-of-the-art in generative TSFMs, pre-trained on **1 trillion (10^12)** time points (TimeBench). Sundial introduced **TimeFlow Loss**—a flow-matching-based training objective that enables continuous-domain probabilistic forecasting without discrete tokenization or parametric distribution assumptions. It generates multiple probable futures, supports both point and probabilistic prediction, and achieves **1st MASE on GIFT-Eval**. Sundial represents the convergence of generative modeling (flow matching, continuous ODEs) with time-series forecasting, pointing to the next generation of TSFMs.

---

**9. Time-MoE: Billion-Scale Time Series Foundation Models with Mixture of Experts**  
*Xiaoming Shi, Shiyu Wang, Yuqi Nie, Dianqi Li, Zhou Ye, Qingsong Wen, Ming Jin*  
**ICLR 2025** (Alibaba DAMA) | arXiv:2409.02527  
> **Why milestone:** The first TSFM to scale beyond 1B parameters using **Sparse Mixture-of-Experts (MoE)**, reaching 2.4B total parameters with efficient conditional activation. It introduced point-wise tokenization and multi-resolution scheduling, producing forecasts at multiple scales simultaneously. Time-MoE proved that MoE architectures—dominant in NLP—could be adapted to time series for massive scale without prohibitive inference costs, and ranked among the top zero-shot performers.

---

**10. Chronos-2: From Univariate to Universal Forecasting**  
*Abdul Fatir Ansari, Oleksandr Shchur, Jaris Küken, Andreas Auer, Boran Han, Pedro Mercado, Syama Sundar Rangapuram, Huibin Shen, Lorenzo Stella, Xiyuan Zhang, et al.*  
**arXiv 2025** (Amazon Science) | arXiv:2510.15821  
> **Why milestone:** The successor to Chronos, explicitly extending tokenization-based TSFMs from univariate to **multivariate universal forecasting**. It demonstrated that discrete tokenization could scale to multivariate settings with proper architectural modifications, and maintained Amazon's leadership in the TSFM space. It also reinforced the encoder-decoder paradigm as competitive with decoder-only alternatives.

---

**11. Moirai-MoE: Empowering Time Series Foundation Models with Sparse Mixture of Experts**  
*Xu Liu, Juncheng Liu, Gerald Woo, Taha Aksu, Yuxuan Liang, Roger Zimmermann, Chenghao Liu, Silvio Savarese, Caiming Xiong, Doyen Sahoo*  
**arXiv 2024** (Salesforce AI Research) | arXiv:2410.10469  
> **Why milestone:** Brought Sparse MoE to the Moirai architecture, scaling up to 935M total parameters while keeping activated parameters efficient. It demonstrated that MoE could improve both capacity and efficiency in encoder-based TSFMs, and released open weights for Small and Base variants—advancing the open-source TSFM ecosystem.

---

**12. Tiny Time Mixers (TTMs): Fast Pre-trained Models for Enhanced Zero/Few-Shot Forecasting**  
*Vijay Ekambaram, Arindam Jati, Pankaj Dayama, Sumanta Mukherjee, Nam H. Nguyen, Wesley M. Gifford, Chandra Reddy, Jayant Kalagnanam*  
**NeurIPS 2024** (IBM Research) | arXiv:2401.03955  
> **Why milestone:** Demonstrated that **small, lightweight pre-trained models** (orders of magnitude smaller than TimesFM or Moirai) could achieve competitive zero/few-shot performance through clever resolution-prefix tuning and diverse patch-length sampling. TTM proved that TSFMs did not need to be massive to be useful, making foundation models accessible for resource-constrained and edge-deployment scenarios.

---

**13. UniTS: Building a Unified Time Series Model**  
*Shanghua Gao, Teddy Koker, Owen Queen, Thomas Hartvigsen, Theodoros Tsiligkaridis, Marinka Zitnik*  
**NeurIPS 2024** (Harvard) | arXiv:2403.00131  
> **Why milestone:** Proposed a unified model architecture capable of handling both **understanding** (classification, anomaly detection) and **generation** (forecasting, imputation) tasks in a single framework. It demonstrated that a single encoder could be trained to perform diverse time-series tasks without task-specific heads, moving toward the vision of a true "universal" time-series model.

---

**14. ROSE: Retrieval-Augmented Time Series Foundation Models**  
*Hao Wang, Licheng Pan, Zhichao Chen, Degui Yang, Sen Zhang, Yifei Yang, Xinggao Liu, Haoxuan Li, Dacheng Tao*  
**ICML 2025**  
> **Why milestone:** Introduced retrieval-augmented generation (RAG) to time-series forecasting, enabling models to retrieve relevant historical patterns from a large corpus during inference. This improved forecasting accuracy on rare or complex patterns and established a new paradigm where TSFMs could be augmented with external memory rather than relying solely on parametric knowledge.

---

**15. VisionTS: Leveraging Vision Transformers for Time Series Forecasting**  
*Yifan Chen, et al.*  
**2024**  
> **Why milestone:** Bridged computer vision and time-series by treating time-series patches as image tokens and applying pre-trained Vision Transformers (ViT) for forecasting. It demonstrated that visual pre-training could transfer to temporal data, opening cross-modal TSFM research and inspiring later multimodal work.

---
## 3. LLM-Aligned & Multimodal Time Series (2023–2026)

These papers explore the radical idea that Large Language Models—pre-trained on massive text—can be "reprogrammed" or aligned to understand and forecast time series, either by treating numbers as text, by projecting time series into language embedding spaces, or by joint training on text and temporal data.

---

**1. GPT4TS / One Fits All: Power General Time Series Analysis by Pretrained LM**  
*Tian Zhou, Peisong Niu, Xue Wang, Liang Sun, Rong Jin*  
**NeurIPS 2023** | arXiv:2302.11939  
> **Why milestone:** The first major work to demonstrate that a **frozen, pre-trained GPT-2** could be repurposed as a general time-series backbone by inputting time-series patches as "tokens" and fine-tuning only positional encoding and normalization layers. It proved that language-model weights contained transferable structure for temporal data and established the "reprogramming" paradigm. This directly inspired Time-LLM, LLM4TS, and dozens of subsequent LLM-aligned papers.

---

**2. Time-LLM: Time Series Forecasting by Reprogramming Large Language Models**  
*Ming Jin, Shiyu Wang, Lintao Ma, Zhixuan Chu, James Y. Zhang, Xiaoming Shi, Pin-Yu Chen, Yuxuan Liang, Yuan-Fang Li, Shirui Pan, et al.*  
**ICLR 2024** | arXiv:2310.01728  
> **Why milestone:** The most influential LLM-reprogramming paper. Time-LLM aligns time-series patches with text prototypes using multi-head attention, then concatenates them with a **Prompt-as-Prefix (PaP)** to enhance the LLM's reasoning ability. It demonstrated that LLaMA (7B+) could be reprogrammed for forecasting with minimal fine-tuning, achieving strong results and proving that LLM reasoning could be harnessed for temporal tasks. It is the standard baseline for all LLM-based forecasting.

---

**3. LLM4TS: Aligning Pre-trained LLMs as Data-Efficient Time-Series Forecasters**  
*Ching Chang, Wei-Yao Wang, Wen-Chih Peng, Tien-Fu Chen*  
**2024** | arXiv:2308.08469  
> **Why milestone:** Introduced a two-stage fine-tuning pipeline (patch reconstruction → forecasting) for aligning LLMs with time-series data. It demonstrated that LLMs could be made data-efficient forecasters through careful curriculum learning, requiring far less task-specific data than training from scratch. This influenced later work on few-shot LLM forecasting.

---

**4. UniTime: A Language-Empowered Unified Model for Cross-Domain Time Series Forecasting**  
*Xu Liu, Junfeng Hu, Yuan Li, Shizhe Diao, Yuxuan Liang, Bryan Hooi, Roger Zimmermann*  
**WWW 2024** | arXiv:2312.01698  
> **Why milestone:** Introduced **domain instructions** as natural-language prompts that identify the source domain of each time series during training. This enabled a single LLM-based model to handle multi-source, cross-domain time series without confusion. UniTime demonstrated that language supervision could improve cross-domain generalization in forecasting.

---

**5. TEMPO: Prompt-Based Generative Pre-Trained Transformer for Time Series Forecasting**  
*Defu Cao, Furong Jia, Sercan O. Arik, Tomas Pfister, Yixiang Zheng, Wen Ye, Yan Liu*  
**ICLR 2024**  
> **Why milestone:** Combined statistical analysis (trend, seasonality, residual decomposition) with prompt-based LLM fine-tuning, showing that structural prompts enhanced forecasting accuracy. It demonstrated that LLMs could benefit from classical time-series decomposition when adapted for temporal tasks.

---

**6. S2IP-LLM: Semantic Space Informed Prompt Learning with LLM for Time Series Forecasting**  
*Zijie Pan, Yushan Jiang, Sahil Garg, Anderson Schneider, Yuriy Nevmyvaka, Dongjin Song*  
**ICML 2024** | arXiv:2403.05798  
> **Why milestone:** Designed a cross-modality tokenization module that aligns pre-trained LLM semantic space with time-series embedding space using **semantic anchors** from word embeddings. This improved the quality of LLM-time-series alignment beyond simple patching, demonstrating that semantic structure—not just syntactic structure—could transfer from language to time.

---

**7. CALF: Aligning LLMs for Time Series Forecasting via Cross-Modal Fine-Tuning**  
*Peiyuan Liu, Hang Guo, Tao Dai, Naiqi Li, Jigang Bao, Xudong Ren, Yong Jiang, Shu-Tao Xia*  
**AAAI 2025**  
> **Why milestone:** Proposed cross-modal matching, feature regularization, and output consistency losses to better align LLMs with time-series forecasting. It demonstrated that multi-objective alignment (not just input reprogramming) was necessary for effective LLM transfer to temporal data, improving upon Time-LLM and S2IP-LLM.

---

**8. TimeCMA: Towards LLM-Empowered Multivariate Time Series Forecasting via Cross-Modality Alignment**  
*Chenxi Liu, Qianxiong Xu, Hao Miao, Sun Yang, Lingzheng Zhang, Cheng Long, Ziyue Li, Rui Zhao*  
**AAAI 2025**  
> **Why milestone:** Focused on cross-modality alignment specifically for **multivariate** forecasting, showing that LLMs could be trained to understand cross-variable relationships through textual descriptions of variable interactions. It advanced LLM-based multivariate forecasting beyond naive univariate patching.

---

**9. TEST: Text Prototype Aligned Embedding to Activate LLM's Ability for Time Series**  
*Chenxi Sun, Hongyan Li, Yaliang Li, Shenda Hong*  
**ICLR 2024**  
> **Why milestone:** Introduced text-prototype-aligned embeddings that map time-series patterns to natural-language descriptions (e.g., "upward trend with seasonal peaks"), enabling LLMs to leverage their semantic understanding for forecasting. It demonstrated that interpretable textual intermediates could improve both accuracy and explainability.

---

**10. ChatTS: A Unified Multimodal Time Series Foundation Model Bridging Numerical and Textual Data**  
*Huiqiang Wang, et al.*  
**AAAI 2025**  
> **Why milestone:** One of the first true **multimodal conversational** TSFMs, enabling users to query time-series data in natural language and receive both numerical forecasts and textual explanations. It demonstrated that TSFMs could be made interactive and accessible, bridging the gap between technical forecasting and business intelligence.

---

**11. GPT4MTS: Prompt-Based Large Language Model for Multimodal Time-Series Forecasting**  
*Flora Jia, et al.*  
**2024**  
> **Why milestone:** Extended LLM-based forecasting to multimodal inputs (text + time series + external metadata), demonstrating that LLMs could naturally integrate diverse data types for forecasting. It influenced the design of multimodal TSFMs like ChatTS and Chronicle.

---

**12. FSTLLM: Spatio-Temporal LLM for Few-Shot Time Series Forecasting**  
*Y. Jiang, Y. Chen, X. Li, Q. Chao, S. Liu, G. Cong*  
**ICML 2025**  
> **Why milestone:** Combined LLM reasoning with spatio-temporal structure for few-shot forecasting, demonstrating that LLMs could adapt to new spatial and temporal domains with minimal examples when provided with appropriate structural prompts. It advanced the few-shot capabilities of LLM-aligned models.

---

**13. Time-MMD: A Benchmark and MM-TSFlib Fusion Library for Multimodal Time Series**  
*Liu et al.*  
**2024**  
> **Why milestone:** Provided the first comprehensive benchmark and open-source library for multimodal time-series forecasting (text + numerical). It standardized evaluation for multimodal TSFMs and catalyzed research in this emerging sub-field by providing datasets, metrics, and baseline implementations.

---

**14. Chronicle: A Multimodal Foundation Model for Joint Language and Time Series Understanding**  
*Various authors, 2026*  
**arXiv 2026**  
> **Why milestone:** Trained from scratch (not repurposed from LLMs) on both language and time-series modalities with a compact 324M-parameter backbone, achieving competitive performance against dedicated TSFMs and LLMs on their respective benchmarks. It proved that native joint training—rather than post-hoc LLM adaptation—could yield superior multimodal temporal understanding and set a new direction for multimodal TSFM architecture design.

---

**15. AutoTimes: Autoregressive Time Series Forecasters via Large Language Models**  
*Yong Liu, et al.*  
**NeurIPS 2024** (THUML, Tsinghua)  
> **Why milestone:** Demonstrated that LLMs could be repurposed as **autoregressive** time-series forecasters by projecting continuous values into LLM token embeddings and utilizing in-context learning. It showed that LLM pre-training could enable autoregressive temporal generation without task-specific training, offering a new paradigm for LLM-based time-series generation.

---
## 4. Diffusion & Generative Models for Time Series (2023–2026)

Diffusion models brought probabilistic forecasting, sample generation, and uncertainty quantification to time series. These papers represent the convergence of generative AI and temporal modeling.

---

**1. TSDiff: Predict, Refine, Synthesize: Self-Guiding Diffusion Models for Probabilistic Time Series Forecasting**  
*Marcel Kollovieh, Abdul Fatir Ansari, Michael Bohlke-Schneider, Jasper Zschiegner, Hao Wang, Yuyang Bernie Wang*  
**NeurIPS 2023** | arXiv:2304.01854  
> **Why milestone:** The first major work to apply self-guiding diffusion to time-series forecasting, introducing a three-stage pipeline (predict → refine → synthesize) that enabled high-quality probabilistic forecasts without requiring explicit density modeling. It established diffusion models as viable alternatives to autoregressive and VAE-based probabilistic forecasters.

---

**2. DYffusion: A Dynamics-Informed Diffusion Model for Spatiotemporal Forecasting**  
*Salva Rühling Cachay, Bo Zhao, Hailey Joren, Rose Yu*  
**NeurIPS 2023**  
> **Why milestone:** Introduced physics-informed dynamics into the diffusion process, conditioning denoising on known physical constraints (e.g., fluid dynamics, weather equations). It demonstrated that diffusion models could incorporate domain knowledge through the forward/backward process design, improving spatiotemporal forecasting accuracy and physical consistency.

---

**3. Non-Autoregressive Conditional Diffusion Models for Time Series Prediction**  
*Lifeng Shen, James Kwok*  
**ICML 2023**  
> **Why milestone:** Showed that diffusion models could generate time-series forecasts **non-autoregressively** (all time steps in parallel), dramatically improving inference speed over autoregressive alternatives while maintaining probabilistic quality. This became a key design principle for subsequent diffusion-based forecasters.

---

**4. TimeDiT: General-Purpose Diffusion Transformers for Time Series Foundation Model**  
*Defu Cao, Wen Ye, Yizhou Zhang, Yan Liu*  
**arXiv 2024** | arXiv:2409.02322  
> **Why milestone:** The first attempt to build a **general-purpose diffusion Transformer** (DiT-style) for time-series as a foundation model. It applied diffusion transformers to temporal data with masked reconstruction pre-training, demonstrating that diffusion-based architectures could serve as universal backbones for multiple time-series tasks.

---

**5. Transformer-Modulated Diffusion Models for Probabilistic Multivariate Time Series Forecasting**  
*Yuxin Li, Wenchao Chen, Xinyue Hu, Bo Chen, Mingyuan Zhou*  
**ICLR 2024**  
> **Why milestone:** Proposed using Transformers to modulate the diffusion process (guiding noise schedules and denoising steps), enabling better capture of long-range dependencies in multivariate settings. It demonstrated that Transformers and diffusion were complementary—Transformers for structure, diffusion for probabilistic generation.

---

**6. Multi-Resolution Diffusion Models for Time Series Forecasting**  
*Lifeng Shen, Weiyu Chen, James Kwok*  
**ICLR 2024**  
> **Why milestone:** Introduced multi-resolution diffusion where different noise levels corresponded to different temporal scales, enabling the model to generate coherent structure at both fine and coarse granularities simultaneously. It significantly improved long-horizon probabilistic forecasting by enforcing scale consistency.

---

**7. Diffusion-TS: Interpretable Diffusion for General Time Series Generation**  
*Xinyu Yuan, Yan Qiao*  
**arXiv 2024** | arXiv:2403.01742  
> **Why milestone:** Focused on **interpretability** in diffusion-based time-series generation by disentangling the diffusion process into trend, seasonality, and noise components. It demonstrated that diffusion models could be made explainable—a critical requirement for real-world deployment in finance and healthcare.

---

**8. ARMD: Auto-Regressive Moving Diffusion Models for Time Series Forecasting**  
*Jiaxin Gao, Qinglong Cao, Yuntian Chen*  
**AAAI 2025**  
> **Why milestone:** Reinterpreted the diffusion process by treating future series as the initial state and historical series as the final state, creating an auto-regressive moving diffusion framework. This novel temporal diffusion direction improved conditional generation quality and established a new theoretical framework for time-series diffusion.

---

**9. FDF: Flexible Decoupled Framework for Time Series Forecasting with Conditional Denoising and Polynomial Modeling**  
*Jintao Zhang, Mingyue Cheng, Xiaoyu Tao, Zhiding Liu, Daoyu Wang*  
**arXiv 2024** | arXiv:2410.13253  
> **Why milestone:** Decoupled the deterministic trend component (modeled by polynomials) from the stochastic residual (modeled by conditional diffusion), demonstrating that hybrid deterministic-stochastic models outperformed pure diffusion or pure autoregressive approaches. It influenced later hybrid generative models.

---

**10. Channel-Aware Contrastive Conditional Diffusion for Multivariate Probabilistic Time Series Forecasting**  
*Siyang Li, Yize Chen, Hui Xiong*  
**arXiv 2024** | arXiv:2410.02168  
> **Why milestone:** Combined contrastive learning with conditional diffusion to capture cross-channel dependencies in multivariate probabilistic forecasting. It demonstrated that representation learning (via contrastive objectives) could improve diffusion-based generation quality, bridging the gap between discriminative and generative time-series modeling.

---

**11. Retrieval-Augmented Diffusion Models for Time Series Forecasting**  
*Jingwei Liu, Ling Yang, Hongyan Li, Shenda Hong*  
**NeurIPS 2024**  
> **Why milestone:** Introduced retrieval-augmented diffusion for time series, where similar historical patterns are retrieved to guide the diffusion denoising process. This improved forecasting accuracy for rare or complex events and demonstrated that external memory could enhance generative models beyond their parametric capacity.

---

**12. Non-Stationary Diffusion for Probabilistic Time Series Forecasting**  
*Weiwei Ye, Zhuopeng Xu, Ning Gui*  
**arXiv 2025**  
> **Why milestone:** Addressed the non-stationarity problem in diffusion-based forecasting by designing diffusion processes that adapt to changing distributions over time. It demonstrated that standard diffusion assumptions (stationary noise) were inadequate for real-world time series and provided a solution that improved forecast reliability.

---

**13. MG-TSD: Multi-Granularity Time Series Diffusion Models with Guided Learning Process**  
*Xinyao Fan, Yueying Wu, Chang Xu, Yuhao Huang, Weiqing Liu, Jiang Bian*  
**arXiv 2024** | arXiv:2403.05751  
> **Why milestone:** Proposed multi-granularity diffusion where forecasts are generated at multiple temporal resolutions simultaneously, with a guided learning process enforcing consistency across scales. It improved both short-term and long-term probabilistic forecasting within a single model.

---

**14. Series-to-Series Diffusion Bridge Model**  
*Hao Yang, Zhanbo Feng, Feng Zhou, Robert C. Qiu, Zenan Ling*  
**arXiv 2024** | arXiv:2411.04491  
> **Why milestone:** Introduced diffusion bridges (Schrodinger bridges) for time-series forecasting, directly modeling the transition from historical series to future series as a stochastic bridge process. This provided a mathematically elegant framework for conditional time-series generation with strong theoretical guarantees.

---

**15. Diffusion-Based Decoupled Deterministic and Uncertain Framework for Probabilistic Multivariate Time Series Forecasting**  
*Qi Li, Zhenyu Zhang, Lei Yao, Zhaoxia Li, Tianyi Zhong, Yong Zhang*  
**ICLR 2025**  
> **Why milestone:** Explicitly decoupled deterministic (trend/seasonality) and uncertain (residual) components into separate diffusion and regression pathways, then fused them for final prediction. It demonstrated that structured decoupling within diffusion frameworks improved both point and probabilistic forecast accuracy.

---
## 5. Anomaly Detection, Robustness & Specialized Tasks (2023–2026)

These papers address the critical real-world needs of anomaly detection, imputation, robustness to distribution shift, and specialized domain applications. They represent the "deployment-facing" side of time-series research.

---

**1. Anomaly Transformer: Time Series Anomaly Detection with Association Discrepancy**  
*Jiehui Xu, Haixu Wu, Jianmin Wang, Mingsheng Long*  
**ICLR 2022** (catalyzed 2023+ work) | arXiv:2110.02642  
> **Why milestone:** Pioneered the use of **association discrepancy** (the difference between prior and series-associations in self-attention) as an anomaly score. It established that Transformer attention maps themselves contained anomaly-discriminative information, eliminating the need for separate reconstruction or density-estimation networks. It remains the most-cited deep anomaly detection paper and the standard baseline for all TSAD research.

---

**2. DCdetector: Dual Attention Contrastive Representation Learning for Time Series Anomaly Detection**  
*Zhang et al.*  
**KDD 2023**  
> **Why milestone:** Introduced dual attention (channel-wise + time-wise) with contrastive learning for anomaly detection, demonstrating that contrasting normal vs. abnormal representations in a dual-attention space significantly improved detection accuracy. It advanced the contrastive learning paradigm for TSAD beyond simple reconstruction-based methods.

---

**3. MEMTO: Memory-guided Transformer for Multivariate Time Series Anomaly Detection**  
*Junho Song, Keonwoo Kim, Jeonglyul Oh, Sungzoon Cho*  
**NeurIPS 2023** / NeurIPS 2024  
> **Why milestone:** Introduced an external memory module to Transformers for anomaly detection, storing prototypical normal patterns and comparing incoming series against memory entries. This improved detection of subtle anomalies by leveraging long-term memory of normal behavior, and influenced memory-augmented TSAD architectures.

---

**4. DADA: Towards a General Time Series Anomaly Detector with Adaptive Bottlenecks and Dual Adversarial Decoders**  
*Y. Hu et al.*  
**ICLR 2025** | arXiv:2405.15273  
> **Why milestone:** Proposed a **general** (cross-domain) time-series anomaly detector using adaptive bottlenecks and dual adversarial decoders, achieving state-of-the-art across multiple benchmarks without domain-specific tuning. It proved that general TSAD—analogous to zero-shot forecasting—was achievable and released open-source code that became a standard benchmark tool.

---

**5. CATCH: Channel-Aware Multivariate Time Series Anomaly Detection via Frequency Patching**  
*Xingjian Wu, Xiangfei Qiu, Zhengyu Li, Yihang Wang, Jilin Hu, Chenjuan Guo, Hui Xiong, Bin Yang*  
**ICLR 2025**  
> **Why milestone:** Introduced frequency-domain patching for multivariate anomaly detection, applying channel-aware attention in the frequency space to detect cross-channel anomalies. It demonstrated that spectral analysis—when combined with deep learning—could detect anomalies invisible in the time domain, particularly in high-frequency sensor data.

---

**6. ImDiffusion: Imputed Diffusion Models for Multivariate Time Series Anomaly Detection**  
*Authors*  
**VLDB 2024**  
> **Why milestone:** Applied diffusion models to anomaly detection by learning to impute (reconstruct) normal patterns and flagging large imputation errors as anomalies. It demonstrated that diffusion-based imputation was more robust than deterministic autoencoders for anomaly detection, especially under noisy or missing data conditions.

---

**7. AutoTSAD: Unsupervised Holistic Anomaly Detection for Time Series Data**  
*Authors*  
**VLDB 2024**  
> **Why milestone:** Proposed a holistic, unsupervised anomaly detection framework that automatically selected and combined multiple detection algorithms based on data characteristics. It addressed the practical need for "autoML for anomaly detection" and demonstrated that ensemble methods with meta-learning could outperform any single algorithm.

---

**8. STONE: A Spatio-temporal OOD Learning Framework Kills Both Spatial and Temporal Shifts**  
*Authors*  
**KDD 2024**  
> **Why milestone:** Tackled the underexplored problem of **out-of-distribution (OOD) detection** in spatio-temporal data, where both spatial and temporal distribution shifts occur simultaneously. It introduced a framework that could detect OOD samples under combined shifts, critical for real-world deployment in dynamic environments like traffic and IoT.

---

**9. LARA: A Light and Anti-overfitting Retraining Approach for Unsupervised Time Series Anomaly Detection**  
*Authors*  
**WWW 2024**  
> **Why milestone:** Addressed the practical challenge of model drift in deployed anomaly detection systems by proposing a lightweight, anti-overfitting retraining protocol. It demonstrated that continuous retraining without catastrophic forgetting was feasible for TSAD, enabling long-term deployment.

---

**10. KAN-AD: Time Series Anomaly Detection with Kolmogorov–Arnold Networks**  
*Authors*  
**ICML 2025**  
> **Why milestone:** The first major application of Kolmogorov-Arnold Networks (KANs)—a new neural architecture inspired by the Kolmogorov-Arnold representation theorem—to time-series anomaly detection. It demonstrated that KANs' learnable activation functions on edges could capture complex temporal dependencies more efficiently than MLPs, introducing a novel architectural primitive to the TSAD community.

---

**11. Causality-Aware Contrastive Learning for Robust Multivariate Time-Series Anomaly Detection**  
*Authors*  
**ICML 2025**  
> **Why milestone:** Integrated causal discovery (Granger causality) with contrastive learning for anomaly detection, ensuring that detected anomalies were rooted in genuine causal relationships rather than spurious correlations. It improved robustness and interpretability, particularly in industrial and medical applications where false positives are costly.

---

**12. Multi-Resolution Decomposable Diffusion Model for Non-Stationary Time Series Anomaly Detection**  
*Authors*  
**ICLR 2025**  
> **Why milestone:** Combined multi-resolution decomposition with diffusion models for anomaly detection, enabling detection of anomalies at multiple temporal scales simultaneously. It demonstrated that non-stationary anomalies—whose characteristics change over time—required scale-adaptive detection mechanisms.

---

**13. Can LLMs Understand Time Series Anomalies?**  
*Authors*  
**ICLR 2025**  
> **Why milestone:** Conducted the first systematic investigation of whether LLMs (without fine-tuning) could detect anomalies in time series through prompting. It established baseline performance for zero-shot LLM anomaly detection and identified when LLMs succeeded (obvious pattern breaks) and failed (subtle contextual anomalies), guiding future LLM-TSAD research.

---

**14. SARAD: Spatial Association-Aware Anomaly Detection and Diagnosis for Multivariate Time Series**  
*Authors*  
**NeurIPS 2024**  
> **Why milestone:** Combined anomaly detection with **root-cause diagnosis** by modeling spatial associations between variables. It not only detected anomalies but also identified which variables were likely causes, addressing the critical industrial need for actionable anomaly alerts rather than mere flags.

---

**15. TSLANet: Rethinking Transformers for Time Series Representation Learning**  
*Emadeldeen Eldele, Ragab M., Zhenyu Chen, et al.*  
**ICML 2024**  
> **Why milestone:** Proposed a lightweight Transformer with innovative pre-training modules for enhanced time-series representation learning, achieving strong results across classification, anomaly detection, and forecasting. It demonstrated that efficient, pre-trained representations could benefit multiple downstream tasks, influencing lightweight TSFM design.

---
## 6. Benchmarks, Evaluation & Comprehensive Surveys (2023–2026)

These papers do not introduce new models but instead provide the infrastructure, evaluation standards, and intellectual synthesis that enable the entire field to progress. They are essential reading for anyone entering or reviewing the field.

---

**1. A Survey on Deep Learning and Foundation Models for Time Series Forecasting**  
*Authors*  
**arXiv 2024** | arXiv:2401.13912  
> **Why milestone:** The most comprehensive survey of time-series forecasting, covering classical methods, deep learning (RNN, CNN, Transformer), and the full foundation-model wave (2023–2024). It categorizes TSFMs by architecture (encoder, decoder, encoder-decoder), tokenization strategy, and training objective, providing the standard taxonomy used by the community. Essential for understanding the field's evolution.

---

**2. Foundation Models for Time Series Analysis: A Tutorial and Survey**  
*Yuxuan Liang, Haomin Wen, Yuqi Nie, Yushan Jiang, Ming Jin, Dongjin Song, Shirui Pan, Qingsong Wen*  
**KDD 2024** | arXiv:2403.14735  
> **Why milestone:** The definitive tutorial on time-series foundation models, presented at KDD 2024. It covers not only forecasting but also classification, anomaly detection, and imputation, providing unified terminology and evaluation protocols. It established the "TSFM" acronym and the standard framework for comparing foundation models across tasks.

---

**3. GIFT-Eval: A Benchmark for General Time Series Forecasting Model Evaluation**  
*Taha Aksu, Gerald Woo, Juncheng Liu, Xu Liu, Chenghao Liu, Silvio Savarese, Caiming Xiong, Doyen Sahoo*  
**arXiv 2024** | arXiv:2410.10393  
> **Why milestone:** The first comprehensive, standardized benchmark specifically designed for **general** (zero-shot) time-series foundation models. It introduced unified evaluation protocols, datasets, and leaderboards that enabled fair comparison across TSFMs like TimesFM, Moirai, Chronos, and Timer. GIFT-Eval has become the de facto standard for TSFM evaluation, with models competing for top rankings.

---

**4. TFB: Towards Comprehensive and Fair Benchmarking of Time Series Forecasting Methods**  
*Xiangfei Qiu, Jilin Hu, et al.*  
**VLDB 2024**  
> **Why milestone:** Addressed the reproducibility crisis in time-series forecasting by providing a comprehensive, fair benchmarking framework that standardized data splits, preprocessing, and evaluation metrics across 20+ methods. It exposed inconsistencies in prior evaluations and established rigorous baselines that all subsequent papers must now address.

---

**5. Tab: Unified Benchmarking of Time Series Anomaly Detection Methods**  
*Xiangfei Qiu, et al.*  
**VLDB 2025**  
> **Why milestone:** The first unified benchmark for time-series anomaly detection, providing standardized datasets, metrics, and evaluation protocols for 40+ algorithms. It addressed the fragmentation in TSAD evaluation and enabled fair comparison across methods, similar to what GIFT-Eval did for forecasting.

---

**6. BLAST: Balanced Sampling Time Series Corpus for Universal Forecasting Models**  
*Zezhi Shao, Yujie Li, Fei Wang, et al.*  
**KDD 2025**  
> **Why milestone:** Introduced a carefully curated, balanced-sampling pre-training corpus designed specifically for universal forecasting models. It addressed the data-quality problem in TSFM pre-training—showing that balanced, diverse data was more important than raw scale—and provided an open dataset that improved downstream zero-shot performance.

---

**7. Monash Time Series Forecasting Archive (Expanded)**  
*Rakshitha Godahewa, Christoph Bergmeir, Geoffrey I. Webb, Rob J. Hyndman, Pablo Montero-Manso*  
**NeurIPS Datasets 2021** (catalyzed 2023+ work)  
> **Why milestone:** The expanded Monash archive became the standard dataset repository for time-series forecasting research, containing 40+ datasets from diverse domains. Its systematic organization and standardized format enabled the large-scale pre-training of foundation models (e.g., MOMENT's Time Series Pile is built on Monash data) and fair cross-paper comparison.

---

**8. A Review on Outlier/Anomaly Detection in Time Series Data (Updated Perspective)**  
*Ane Blázquez-García, Angel Conde, Usue Mori, Jose A. Lozano*  
**ACM Computing Surveys 2021** (updated influence through 2023–2026)  
> **Why milestone:** The most comprehensive survey of time-series anomaly detection, covering statistical, machine learning, and deep learning methods. It remains the standard reference for understanding TSAD methodologies and has been cited by virtually every TSAD paper published since 2023. It provides the taxonomy (point, contextual, collective anomalies) that organizes the field.

---

**9. Deep Learning for Time Series Anomaly Detection: A Survey**  
*Kukjin Choi, Jihun Yi, Changhwa Park, Sungroh Yoon*  
**IEEE Access 2023 / arXiv 2022**  
> **Why milestone:** Focused specifically on deep learning methods for TSAD, providing a systematic review of autoencoders, GANs, Transformers, and one-class classification approaches. It became the standard reference for researchers entering the deep TSAD space and identified key challenges (label scarcity, concept drift, multivariate complexity) that define current research directions.

---

**10. Time Series Foundational Models: Their Role in Anomaly Detection and Prediction**  
*Authors*  
**arXiv 2024** | arXiv:2412.19286  
> **Why milestone:** The first comprehensive study of how pre-trained TSFMs (MOMENT, TimesFM, Chronos) could be adapted for anomaly detection and prediction without task-specific training. It established that zero-shot TSFM transfer to anomaly detection was feasible and identified which TSFM architectures were most suitable for detection tasks.

---

**11. Large Language Models for Time Series: A Survey**  
*Authors*  
**arXiv 2024** | arXiv:2402.01801  
> **Why milestone:** The first dedicated survey of LLM-aligned time-series research, covering reprogramming, alignment, prompting, and multimodal fusion. It organized the rapidly growing sub-field into coherent categories and identified key open problems (e.g., whether LLM pre-training actually transfers to temporal reasoning).

---

**12. Empowering Time Series Analysis with Foundation Models: A Survey**  
*Authors*  
**Information Fusion / arXiv 2025** | arXiv:2405.02358  
> **Why milestone:** A comprehensive survey covering the full spectrum of foundation models for time series—both pure TSFMs and LLM-aligned models. It provided detailed comparisons of model scales, training data sizes, architectures, and context lengths, serving as a reference for practitioners choosing between models like TimesFM, Moirai, Chronos, and MOMENT.

---

**13. Time Series Analysis Based on Informer Algorithms: A Survey**  
*Q. Zhu, J. Han, K. Chai, C. Zhao*  
**Symmetry 2023**  
> **Why milestone:** Provided a systematic survey of efficient Transformer variants (Informer, Autoformer, FEDformer, Pyraformer) for long-sequence time-series forecasting. It organized the field by attention mechanism complexity and became a standard reference for researchers designing efficient time-series Transformers.

---

**14. ProbTS: Benchmarking Point and Distributional Forecasting across Diverse Prediction Horizons**  
*Jintao Zhang, et al.*  
**NeurIPS 2024 (Datasets Track)**  
> **Why milestone:** Introduced the first benchmark that explicitly evaluated both **point** and **distributional** (probabilistic) forecasting across diverse horizons in a unified framework. It exposed that models strong at point forecasting often failed at distributional forecasting and vice versa, pushing the community toward unified probabilistic evaluation.

---

**15. An Experimental Evaluation of Anomaly Detection in Time Series**  
*Authors*  
**VLDB 2024**  
> **Why milestone:** A large-scale experimental evaluation of 20+ anomaly detection algorithms across multiple datasets and metrics, providing the most rigorous empirical comparison to date. It identified which algorithms were robust across domains and which were brittle, providing actionable guidance for practitioners.

---

## Quick Reference: Most-Cited & Most-Influential by Year

| Year | Paper | Venue | Impact |
|------|-------|-------|--------|
| 2022 (late) | PatchTST | ICLR 2023 | Patching paradigm; 1000+ citations |
| 2022 (late) | DLinear | AAAI 2023 | Transformer skepticism; mandatory baseline |
| 2023 | TimesNet | ICLR 2023 | 2D temporal modeling; task-general backbone |
| 2023 | GPT4TS | NeurIPS 2023 | LLM reprogramming; frozen GPT-2 for TS |
| 2023 | Time-LLM | ICLR 2024 | LLM reprogramming with prompts; standard baseline |
| 2023 | iTransformer | ICLR 2024 | Inverted attention; 4000+ citations |
| 2023 | TSDiff | NeurIPS 2023 | Self-guiding diffusion for forecasting |
| 2024 | TimesFM | ICML 2024 | Google decoder-only TSFM; 200M params |
| 2024 | Moirai | ICML 2024 | Any-variate TSFM; open-source; oral |
| 2024 | MOMENT | ICML 2024 | Open TSFM; Time Series Pile; 2M+ downloads |
| 2024 | Timer | ICML 2024 | Tsinghua TSFM; S3 format; multi-task |
| 2024 | Chronos | TMLR 2024 | Amazon tokenization-based TSFM |
| 2024 | TimeMixer | ICLR 2024 | Multiscale mixing architecture |
| 2025 | Timer-XL | ICLR 2025 | Long-context; TimeAttention; unified |
| 2025 | Time-MoE | ICLR 2025 | 2.4B MoE TSFM; billion-scale |
| 2025 | Sundial | ICML 2025 | Trillion-point pre-training; flow matching; generative |
| 2025 | DADA | ICLR 2025 | General anomaly detector; cross-domain |
| 2025 | CATCH | ICLR 2025 | Frequency patching for anomaly detection |
| 2025 | TFB | VLDB 2024 | Fair benchmarking framework |
| 2025 | GIFT-Eval | arXiv 2024 | General TSFM benchmark; standard leaderboard |
| 2026 | Chronicle | arXiv 2026 | Native multimodal joint training |

---

## Meta-Analysis: What Defines a Milestone (2023–2026)

1. **Paradigm Shift:** Papers that moved the field from task-specific supervised training to pre-trained, zero-shot foundation models (TimesFM, Moirai, Chronos, MOMENT, Timer, Sundial).

2. **Architectural Inversion:** Papers that challenged established wisdom and proposed radically different architectures (iTransformer inverted dimensions; DLinear proved simple linear models could beat Transformers; TimesNet introduced 2D convolutions for 1D data).

3. **Cross-Modal Bridge:** Papers that connected time series to language (GPT4TS, Time-LLM, LLM4TS, Chronicle), demonstrating that LLMs could be repurposed or jointly trained for temporal understanding.

4. **Generative Probabilistic Forecasting:** Papers that moved beyond point forecasting to full probabilistic generation via diffusion and flow matching (TSDiff, TimeDiT, Sundial), enabling uncertainty quantification and scenario generation.

5. **Open-Source Infrastructure:** Papers that released models, datasets, and benchmarks as open resources (MOMENT's Time Series Pile, GIFT-Eval, TFB, Monash Archive, Moirai's Uni2TS), enabling reproducible science and community progress.

6. **Scale:** Papers that demonstrated the scaling laws of time-series pre-training (Timer-XL at 1B+ points, Sundial at 1 trillion points, Time-MoE at 2.4B parameters), proving that "bigger data + bigger models = better zero-shot" holds for time series.

---

> **Note:** Papers from late 2022 (PatchTST, DLinear, FEDformer, Non-stationary Transformer) are included because they were published in 2023 conferences and catalyzed the entire 2023–2026 wave. Their intellectual impact is inseparable from the 2023+ era.
