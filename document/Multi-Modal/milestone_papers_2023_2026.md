# Multi-Modal Milestone & Trunk Papers (2023 – Mid-2026)

> **Curator's Note:** This document curates the most influential, foundational, and direction-setting papers in Multi-Modal AI from 2023 to July 2026. Focus is on works that opened new research directions, achieved massive adoption, or are considered breakthroughs. Incremental improvements are excluded.

---

## 1. Vision-Language Foundation Models (VLMs)

### 1.1 LLaVA: Large Language and Vision Assistant
- **Title:** Visual Instruction Tuning (LLaVA)
- **Authors:** Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee
- **Venue:** NeurIPS 2023 (Oral)
- **Year:** 2023
- **Why Milestone:** The first paper to use language-only GPT-4 to generate multimodal instruction-following data, then instruction-tune a vision-language model. LLaVA proved that a simple projection bridge connecting a CLIP vision encoder to a Vicuna LLM, trained on synthetic conversations, could achieve surprisingly strong zero-shot generalization and multimodal chat capabilities. It catalyzed the entire open-source visual instruction tuning movement and became the most referenced VLM family by 2025.

### 1.2 BLIP-2: Bootstrapping Language-Image Pre-training
- **Title:** BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models
- **Authors:** Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi
- **Venue:** ICML 2023
- **Year:** 2023
- **Why Milestone:** Introduced a lightweight Querying Transformer (Q-Former) to bridge frozen image encoders and frozen LLMs, enabling efficient vision-language pre-training without updating massive backbones. This "bridging" architecture became the template for dozens of subsequent VLMs, demonstrating that parameter-efficient alignment could unlock powerful multimodal reasoning.

### 1.3 InstructBLIP: Instruction Tuning for General-Purpose VLMs
- **Title:** InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning
- **Authors:** Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung, Steven Hoi
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why Milestone:** Extended BLIP-2 with instruction tuning, showing that vision-language models could follow diverse natural language instructions for tasks like captioning, VQA, and reasoning. It established instruction tuning as a critical stage in VLM training pipelines and set early benchmarks for general-purpose multimodal assistants.

### 1.4 Qwen-VL: Versatile Vision-Language Model
- **Title:** Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond
- **Authors:** Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, et al. (Alibaba Qwen Team)
- **Venue:** arXiv (later integrated into Qwen series)
- **Year:** 2023
- **Why Milestone:** One of the first open-source VLMs to demonstrate strong capabilities across understanding, visual grounding, and OCR. The Qwen-VL series (evolving into Qwen2-VL and Qwen2.5-VL by 2024–2025) became the dominant open-weight multilingual VLM family, competing with closed-source models on many benchmarks.

### 1.5 GPT-4V / GPT-4 Technical Report
- **Title:** GPT-4 Technical Report & GPT-4V(ision) System Card
- **Authors:** OpenAI
- **Venue:** arXiv / OpenAI Technical Report
- **Year:** 2023
- **Why Milestone:** GPT-4 was the first mainstream large-scale multimodal model demonstrating human-level performance on professional and academic benchmarks across text and vision. GPT-4V's system card (September 2023) documented safe deployment of visual capabilities, setting industry standards for multimodal capability evaluation, risk assessment, and red-teaming. It proved that scaling LLMs to accept image inputs yields emergent cross-modal reasoning.

---

## 2. Omni-Modal & Native Multimodal Models

### 2.1 GPT-4o: The "Omni" Model
- **Title:** GPT-4o System Card
- **Authors:** Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, et al. (OpenAI)
- **Venue:** arXiv:2410.21276 / OpenAI Blog
- **Year:** 2024
- **Why Milestone:** GPT-4o ("o" for omni) was the first natively end-to-end multimodal model trained jointly across text, vision, and audio—NOT an assembly of separate encoders with adapters. It could process and generate text, images, and audio through shared transformer layers, achieving ~232–320ms audio response latency (comparable to human conversation). This removed the multi-step pipeline bottleneck (ASR → LLM → TTS) and established native multimodal training as the new frontier.

### 2.2 Gemini 1.0: A Family of Highly Capable Multimodal Models
- **Title:** Gemini: A Family of Highly Capable Multimodal Models
- **Authors:** Gemini Team, Google DeepMind
- **Venue:** arXiv:2312.11805
- **Year:** 2023
- **Why Milestone:** Google's answer to GPT-4, Gemini was natively multimodal from pre-training—trained jointly on text, images, audio, and video. It demonstrated that a single model could achieve state-of-the-art across language, vision, audio, and cross-modal reasoning benchmarks. The Gemini family (evolving through 1.5 Pro/Flash in 2024, 2.5 in 2025, and 3.0 in 2025–2026) became the primary commercial competitor to OpenAI's GPT series and pushed Google to integrate multimodal AI across its product suite.

### 2.3 Gemini 1.5: Long-Context Multimodal Understanding
- **Title:** Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context
- **Authors:** Gemini Team, Google DeepMind
- **Venue:** arXiv:2403.05530
- **Year:** 2024
- **Why Milestone:** Introduced the Mixture-of-Experts (MoE) architecture at massive scale for multimodal models, supporting up to 1 million tokens of context (later 2 million+). This enabled processing of entire videos, lengthy audio, and massive documents in a single inference pass. It established long-context multimodal reasoning as a critical capability and drove the industry to compete on context window size.

### 2.4 Qwen2.5-Omni / Qwen3-Omni
- **Title:** Qwen2.5-Omni Technical Report / Qwen3-Omni
- **Authors:** Alibaba Qwen Team
- **Venue:** arXiv / Open Source Release
- **Year:** 2025–2026
- **Why Milestone:** Qwen3-Omni (December 2025) was the first open-source, Apache 2.0-licensed "natively end-to-end omni-modal AI" unifying text, image, audio, and video input in a single model. While open-source VLMs had existed, Qwen3-Omni matched closed-source proprietary models' capabilities at 30B parameters with a 3B active parameter MoE architecture, democratizing access to state-of-the-art omni-modal AI.

---

## 3. Unified Multimodal Understanding & Generation

### 3.1 NExT-GPT: Any-to-Any Multimodal LLM
- **Title:** NExT-GPT: Any-to-Any Multimodal LLM
- **Authors:** Shengqiong Wu, Hao Fei, Leigang Qu, Wei Ji, Tat-Seng Chua
- **Venue:** ICML 2024
- **Year:** 2023 (arXiv), 2024 (ICML)
- **Why Milestone:** The first end-to-end "any-to-any" multimodal LLM that could perceive input and generate output in arbitrary combinations of text, image, video, and audio. NExT-GPT connected an LLM with multimodal encoders (ImageBind) and diffusion decoders (Stable Diffusion, Zeroscope, AudioLDM), using signal tokens to dispatch generation tasks. It proved that a single LLM backbone could orchestrate cross-modal understanding and generation, inspiring a wave of unified models.

### 3.2 Show-O: One Single Transformer for Multimodal Understanding & Generation
- **Title:** Show-o: One Single Transformer to Unify Multimodal Understanding and Generation
- **Authors:** Jinjin Xie, Weijia Li, et al.
- **Venue:** arXiv 2024 / ICLR 2025
- **Year:** 2024
- **Why Milestone:** Show-O demonstrated that a single autoregressive transformer could simultaneously handle both understanding (image captioning, VQA) and generation (text-to-image) tasks without separate encoder-decoder architectures. By unifying next-token prediction for both text and visual tokens, it challenged the prevailing paradigm that understanding and generation required fundamentally different architectures.

### 3.3 Chameleon: Mixed-Modal Early-Fusion Foundation Models
- **Title:** Chameleon: Mixed-Modal Early-Fusion Foundation Models
- **Authors:** Meta AI FAIR Team
- **Venue:** arXiv 2024
- **Year:** 2024
- **Why Milestone:** Meta's Chameleon adopted an early-fusion token-based approach where text, images, and audio are all tokenized into a shared vocabulary space and processed by a single transformer from the first layer. Unlike late-fusion models (e.g., LLaVA's projection bridge), Chameleon showed that early fusion of modalities enables stronger cross-modal reasoning and more seamless generation, influencing Meta's subsequent Llama-4 multimodal architecture.

### 3.4 Janus / Janus-Pro: Decoupled Visual Encoding for Unified Tasks
- **Title:** Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling
- **Authors:** Xiaokang Chen, Zhiyu Wu, Xingchao Liu, et al. (DeepSeek)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why Milestone:** DeepSeek's Janus series introduced decoupled visual encoders for understanding and generation within a single framework, overcoming the inherent conflict that understanding prefers semantic features while generation needs pixel-level detail. Janus-Pro demonstrated that scaling data and model size with this decoupled design could achieve competitive results on both multimodal understanding and text-to-image generation, rivaling specialized models in each domain.

---

## 4. Multimodal Generation: Image, Video, Audio

### 4.1 DALL-E 3: Improving Image Generation with Better Captions
- **Title:** Improving Image Generation with Better Captions
- **Authors:** James Betker, Gabriel Goh, Li Jing, et al. (OpenAI)
- **Venue:** OpenAI Technical Report / Computer Science Publication
- **Year:** 2023
- **Why Milestone:** DALL-E 3's key insight was that highly descriptive, detailed captions in training data dramatically improve text-to-image alignment. By training a captioner model to generate rich captions and then fine-tuning the diffusion model on these, DALL-E 3 achieved unprecedented prompt fidelity. This "captioning improvement" strategy became standard practice for all subsequent diffusion models (including Stable Diffusion 3, FLUX, etc.).

### 4.2 Stable Diffusion 3 / SDXL / SD3 Medium
- **Title:** Stable Diffusion 3: Multimodal Diffusion Transformer for Photorealistic Text-to-Image Generation / Scaling Rectified Flow Transformers for High-Resolution Image Synthesis
- **Authors:** Stability AI / Stability AI Research Team
- **Venue:** arXiv / Stability AI Publication
- **Year:** 2024–2025
- **Why Milestone:** SD3 introduced the Multimodal Diffusion Transformer (DiT) architecture for text-to-image generation, replacing the U-Net backbone with a transformer that operates on latent patches. This architectural shift matched the contemporaneous DiT paper (Peebles & Xie, 2023) and proved that transformers scale better than CNNs for diffusion-based generation. SD3's open-weight releases democratized high-quality image generation and influenced the entire open-source ecosystem (FLUX, PixArt, etc.).

### 4.3 Sora: Video Generation Models as World Simulators
- **Title:** Video Generation Models as World Simulators (Sora Technical Report)
- **Authors:** Tim Brooks, Bill Peebles, Connor Holmes, et al. (OpenAI)
- **Venue:** OpenAI Technical Report / arXiv:2402.17177
- **Year:** 2024
- **Why Milestone:** Sora was the first large-scale text-to-video model capable of generating minute-long, high-fidelity, temporally coherent video at 1080p resolution. It used a Diffusion Transformer (DiT) operating on spacetime patches of compressed video latent codes. Beyond video generation, OpenAI positioned Sora as a "world simulator" that learns emergent physics, 3D consistency, and object permanence. Sora's release (February 2024) triggered a global explosion in video generation research and is widely considered the "ImageNet moment" for video AI.

### 4.4 CogVideoX / HunyuanVideo / Wan: Open Video Generation
- **Title:** CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer / HunyuanVideo: A Systematic Framework For Large Video Generation Model / Wan: Open and Advanced Large-Scale Video Generative Models
- **Authors:** Tsinghua & BAAI (CogVideoX) / Tencent (HunyuanVideo) / Alibaba (Wan)
- **Venue:** ICLR 2025 / arXiv 2025 / arXiv 2025
- **Year:** 2024–2025
- **Why Milestone:** These three open-source video generation models (CogVideoX, HunyuanVideo, Wan) collectively democratized high-quality video generation that was previously the domain of closed labs (OpenAI, Google). They introduced efficient 3D full-attention DiT architectures, expert parallelism, and flow-matching training objectives, enabling the open-source community to train and deploy competitive video models. Wan (2025) in particular became the go-to open video model, catalyzing a wave of community fine-tunes and applications.

### 4.5 Veo 3 / Cosmos / Seedance 2.0: Commercial Video Frontiers
- **Title:** Veo 3 Technical Report / Cosmos World Foundation Models / Seedance 2.0
- **Authors:** Google DeepMind (Veo 3) / NVIDIA (Cosmos) / ByteDance (Seedance)
- **Venue:** Various Technical Reports 2024–2025
- **Year:** 2024–2025
- **Why Milestone:** Veo 3 (Google, 2025) achieved native audio-visual synchronization—generating video with matching audio in a single model. NVIDIA's Cosmos (2025) positioned video generation as a "world foundation model" for physical AI, releasing open weights and training recipes. Seedance 2.0 (ByteDance, 2025) pushed long-form narrative video generation with omni-modal conditioning. Together, they represent the commercial frontier of video generation moving from research demos to production systems.

---

## 5. Multimodal Alignment & Embeddings

### 5.1 ImageBind: One Embedding Space to Bind Them All
- **Title:** ImageBind: One Embedding Space To Bind Them All
- **Authors:** Rohit Girdhar, Alaaeldin El-Nouby, Zhuang Liu, Mannat Singh, Kalyan Vasudev Alwala, Armand Joulin, Ishan Misra
- **Venue:** CVPR 2023
- **Year:** 2023
- **Why Milestone:** ImageBind learned a joint embedding space across six modalities—images, text, audio, depth, thermal, and IMU data—using only image-paired data for training. It demonstrated that not all pairwise combinations are needed: aligning each modality to image embeddings is sufficient to achieve emergent cross-modal retrieval and composition. This "binding" paradigm became foundational for subsequent any-to-any multimodal models and multimodal RAG systems.

### 5.2 CLIP (Continued Impact) / SigLIP / OpenCLIP Scaling
- **Title:** Sigmoid Loss for Language Image Pre-training (SigLIP) / Reproducible Scaling Laws for Contrastive Language-Image Learning (OpenCLIP)
- **Authors:** Xiaohua Zhai, et al. (Google) / Christoph Schuhmann, et al. (LAION/OpenCLIP)
- **Venue:** ICLR 2023 / NeurIPS 2023
- **Year:** 2023
- **Why Milestone:** SigLIP replaced the standard softmax-based contrastive loss with a sigmoid loss, enabling training on larger batches with better efficiency and scaling properties. OpenCLIP established reproducible scaling laws for CLIP training, showing that data quality and model size follow predictable relationships. Together, these works cemented contrastive language-image pre-training as the backbone of modern vision-language models and provided the training recipes for the open-source community.

---

## 6. Segmentation & Visual Foundation Models

### 6.1 SAM: Segment Anything Model
- **Title:** Segment Anything
- **Authors:** Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollar, Ross Girshick
- **Venue:** ICCV 2023 (Best Paper Honorable Mention)
- **Year:** 2023
- **Why Milestone:** SAM introduced the concept of "promptable segmentation"—a foundation model for image segmentation that accepts points, boxes, text, or masks as prompts and generates valid segmentation masks for any object in any image. Trained on the SA-1B dataset (1 billion masks, 11 million images), SAM demonstrated zero-shot transfer to new image distributions and tasks, becoming the de facto segmentation backbone for computer vision and catalyzing the "Segment Anything in X" research wave (medical imaging, video, 3D, etc.).

### 6.2 SAM 2: Segment Anything in Images and Videos
- **Title:** SAM 2: Segment Anything in Images and Videos
- **Authors:** Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Radle, Chloe Rolland, Laura Gustafson, Aaron Adcock, Matt Deeds, et al. (Meta AI)
- **Venue:** arXiv 2024 / NeurIPS 2024
- **Year:** 2024
- **Why Milestone:** SAM 2 extended the promptable segmentation paradigm to video through a memory-based transformer architecture that stores object and interaction history across frames. It achieved real-time video segmentation with state-of-the-art accuracy, enabling applications in video editing, tracking, and AR/VR. SAM 2's memory mechanism became a template for temporal consistency in video understanding models.

---

## 7. Self-Supervised Visual Learning

### 7.1 DINOv2: Learning Robust Visual Features without Supervision
- **Title:** DINOv2: Learning Robust Visual Features without Supervision
- **Authors:** Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Patrick Labatut, Armand Joulin, Piotr Bojanowski (Meta AI)
- **Venue:** CVPR 2023 (Technical Report: April 2023)
- **Year:** 2023
- **Why Milestone:** DINOv2 trained ViT models at scale (up to 1.1B parameters) on 142M curated images using self-distillation without any labels. Its frozen features achieved competitive or state-of-the-art results on classification, segmentation, depth estimation, and retrieval across diverse domains—without fine-tuning. DINOv2 proved that visual foundation models do not need text supervision (unlike CLIP) to achieve broad transfer, establishing self-supervised visual pre-training as a viable alternative to language-supervised approaches.

### 7.2 DINOv3: Scaling Self-Supervised Vision Transformers Further
- **Title:** DINOv3: Scaling Self-Supervised Vision Transformers (anticipated follow-up)
- **Authors:** Meta AI Research
- **Venue:** arXiv / Research Publication 2025
- **Year:** 2025
- **Why Milestone:** DINOv3 further advanced self-supervised ViTs by scaling data and model size with careful data preparation, introducing Gram anchoring to prevent degradation of dense feature maps, and applying post-hoc strategies to improve flexibility across resolutions and even text-alignment. The DINOv3 suite demonstrated that self-supervised visual features can rival or exceed weakly-supervised models across a broad range of tasks, reinforcing Meta's commitment to visual-only foundation models.

---

## 8. Robotics & Embodied AI: Vision-Language-Action (VLA)

### 8.1 RT-2: Vision-Language-Action Models
- **Title:** RT-2: Vision-Language-Action Models (Robotic Transformer 2)
- **Authors:** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, et al. (Google DeepMind)
- **Venue:** arXiv:2307.15818 / DeepMind Blog (July 2023)
- **Year:** 2023
- **Why Milestone:** RT-2 was the first to formalize the Vision-Language-Action (VLA) paradigm, co-fine-tuning large vision-language models (PaLM-E, PaLI-X) on both internet-scale vision-language data and robot action data. By tokenizing robot actions as text tokens, RT-2 transformed robot control into a next-token prediction problem. It demonstrated emergent reasoning (e.g., "pick up the object that can be used as a hammer" → selects a rock) and significantly improved generalization over RT-1, widely hailed as the "GPT-3 moment for robotics."

### 8.2 RT-X / Open X-Embodiment: Cross-Embodiment Robot Learning
- **Title:** Open X-Embodiment: Robotic Learning Datasets and RT-X Models
- **Authors:** The Open X-Embodiment Collaboration (Google DeepMind, 33 institutions)
- **Venue:** NeurIPS 2023 / ICRA 2024
- **Year:** 2023–2024
- **Why Milestone:** RT-X aggregated robot data from 22 different robot embodiments across 33 institutions into a unified dataset, then trained a single VLA model on this diverse data. The resulting model showed positive transfer across robot morphologies and tasks, proving that cross-embodiment training is possible and beneficial. This democratized approach to robot data collection became the foundation for the broader open-source robotics movement (e.g., LeRobot, Hugging Face).

### 8.3 π0 (Pi-Zero) / Physical Intelligence VLA Models
- **Title:** π0: A Vision-Language-Action Flow Model for General Robot Control
- **Authors:** Physical Intelligence (PI) Team
- **Venue:** arXiv 2024 / Physical Intelligence Publications
- **Year:** 2024
- **Why Milestone:** Physical Intelligence's π0 introduced a flow-based diffusion model for robot action generation, combining VLA reasoning with diffusion-based action sampling. π0 and its successors (π0.5, π0.6, 2025) demonstrated that diffusion models could generate high-frequency, dexterous robot control policies from multimodal instructions, achieving state-of-the-art results on complex manipulation tasks. PI's approach influenced the broader robotics community to adopt generative models for action planning.

---

## 9. Video Understanding & Long-Form Multimodal Reasoning

### 9.1 Video-MME: Comprehensive Evaluation of Multimodal LLMs in Video Analysis
- **Title:** Video-MME: The First-Ever Comprehensive Evaluation Benchmark of Multi-Modal LLMs in Video Analysis
- **Authors:** Chaoyou Fu, Yuhan Dai, Yongdong Luo, Lei Li, Shuhuai Ren, Renrui Zhang, Zihan Wang, Chenyu Zhou, Yunhang Shen, Mengdan Zhang, et al.
- **Venue:** NeurIPS 2024 / arXiv 2024
- **Year:** 2024
- **Why Milestone:** Video-MME was the first comprehensive benchmark specifically designed to evaluate multimodal LLMs on video understanding tasks. It established rigorous evaluation protocols for long-form video reasoning, temporal grounding, and cross-modal alignment, becoming the standard reference for comparing video understanding capabilities across models.

### 9.2 LongVALE: Vision-Audio-Language-Event Benchmark for Long Videos
- **Title:** LongVALE: Vision-Audio-Language-Event Benchmark Towards Time-Aware Omni-Modal Perception of Long Videos
- **Authors:** Tiantian Geng, Jinrui Zhang, Qingni Wang, Teng Wang, Jinming Duan, Feng Zheng
- **Venue:** CVPR 2025
- **Year:** 2025
- **Why Milestone:** LongVALE was the first benchmark to integrate visual, audio, language, and event information for long-form video understanding with precise temporal boundaries. It pushed the community to develop models that can reason about multimodal events across extended durations, bridging the gap between short-clip video understanding and real-world long-form video comprehension.

---

## 10. Cross-Modal & Emerging Modalities

### 10.1 LanguageBind: Extending Video-Language Pretraining to N-Modality
- **Title:** LanguageBind: Extending Video-Language Pretraining to N-modality by Language-based Semantic Alignment
- **Authors:** Bin Zhu, Bin Lin, Munan Ning, Yang Yan, Jiaxi Cui, et al.
- **Venue:** NeurIPS 2023 / ICLR 2024
- **Year:** 2023
- **Why Milestone:** LanguageBind proposed aligning all modalities directly to language (the highest information-density modality) rather than to images as in ImageBind. This direct alignment improved performance on language-related downstream tasks and established a principled way to scale multimodal pre-training to arbitrary numbers of modalities. It also released VIDAL-10M, the first accessible multimodal dataset with aligned video, image, depth, and audio pairs.

### 10.2 VAST: Vision-Audio-Subtitle-Text Omni-Modality Foundation Model
- **Title:** VAST: A Vision-Audio-Subtitle-Text Omni-Modality Foundation Model and Dataset
- **Authors:** Shengqiong Wu, Hao Fei, Xiangtai Li, et al.
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why Milestone:** VAST was among the first to explicitly model four modalities (vision, audio, subtitles, text) together for video understanding, showing that subtitle/text information provides crucial semantic cues that pure vision-audio models miss. It established the foundation for subsequent video-language models that leverage transcript/speech information.

### 10.3 3D Multimodal: Point-Bind, Point-LLM, and 3D-VLM
- **Title:** Point-Bind & Point-LLM: Aligning Point Cloud with Multi-modality for 3D Understanding, Generation, and Instruction Following
- **Authors:** Ziyu Guo, Renrui Zhang, et al.
- **Venue:** CVPR 2024 / arXiv 2024
- **Year:** 2024
- **Why Milestone:** These works extended multimodal foundation models to 3D point clouds, aligning them with images, text, and audio through shared embedding spaces. They demonstrated that 2D visual-language pre-training could be transferred to 3D understanding, opening the door for 3D-aware multimodal agents and robotics applications that reason about spatial structure.

---

## 11. Summary: Key Trends & Directions

| Era | Dominant Theme | Representative Works |
|-----|---------------|-------------------|
| 2023 H1 | VLM Instruction Tuning | LLaVA, InstructBLIP, BLIP-2 |
| 2023 H2 | Segmentation & Visual Foundation Models | SAM, DINOv2, ImageBind |
| 2024 H1 | Native Multimodal / Omni-Modal | GPT-4o, Gemini 1.5, NExT-GPT |
| 2024 H2 | Video Generation & World Models | Sora, CogVideoX, Open-Sora |
| 2025 H1 | Open-Source Video & Omni-Modal | HunyuanVideo, Wan, Qwen2.5-Omni |
| 2025 H2 | Unified Understanding+Generation | Janus-Pro, Show-O, Chameleon |
| 2026 | Long-Form Video & Physical AI | Veo 3, Cosmos, Seedance 2.0, Gemini 3 |

---

> **Document Version:** 2026-07-15
> **Curated for:** AIResearchVault / Multi-Modal Research Track
> **Scope:** 2023 – Mid-2026 (July 2026)
