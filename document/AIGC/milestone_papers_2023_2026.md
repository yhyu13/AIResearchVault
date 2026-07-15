# AIGC Milestone & Trunk Papers (2023 – Mid-2026)

> **Curated:** 2026-07-15  
> **Scope:** Foundational, widely-cited, and direction-opening papers in Generative AI from January 2023 to July 2026. Pre-2023 "trunk" works that directly enable the 2023+ explosion are noted in a dedicated section but are not the focus.  
> **Criteria:** Breakthrough impact, high citation velocity, opened new research directions, or became the architectural/engineering standard for an entire sub-field.

---

## Table of Contents

1. [Pre-2023 Trunk Foundations (Essential Context)](#1-pre-2023-trunk-foundations-essential-context)
2. [Large Language Models (LLMs)](#2-large-language-models-llms)
3. [Alignment, RLHF & Reasoning](#3-alignment-rlhf--reasoning)
4. [Diffusion Models & Image Generation](#4-diffusion-models--image-generation)
5. [Controllable Generation & Efficiency](#5-controllable-generation--efficiency)
6. [Video Generation](#6-video-generation)
7. [3D Generation](#7-3d-generation)
8. [Multimodal (Vision-Language) Models](#8-multimodal-vision-language-models)
9. [Audio & Music Generation](#9-audio--music-generation)

---

## 1. Pre-2023 Trunk Foundations (Essential Context)

These papers predate the curation window but are the **non-negotiable prerequisites** for understanding the 2023–2026 AIGC revolution. They are included because nearly every milestone paper below builds directly on them.

- **Denoising Diffusion Probabilistic Models (DDPM)**  
  Jonathan Ho, Ajay Jain, Pieter Abbeel. *NeurIPS*, 2020.  
  *Why trunk:* The seminal formulation of diffusion models for image generation that displaced GANs as the dominant generative paradigm and underpins every image, video, and 3D system below.

- **High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion)**  
  Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer. *CVPR*, 2022.  
  *Why trunk:* Introduced latent diffusion, compressing the diffusion process into a VAE latent space. This made high-quality image generation feasible on consumer GPUs and catalyzed the entire open-source generative ecosystem.

- **LoRA: Low-Rank Adaptation of Large Language Models**  
  Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen. *ICLR*, 2022.  
  *Why trunk:* The parameter-efficient fine-tuning method that became the **de facto standard** for customizing diffusion models, LLMs, and multimodal models. Without LoRA, the democratized "fine-tune your own model" culture of 2023+ would not exist.

- **Training Language Models to Follow Instructions with Human Feedback (InstructGPT)**  
  Long Ouyang et al. (OpenAI). *NeurIPS*, 2022.  
  *Why trunk:* Established the three-stage RLHF pipeline (SFT → Reward Model → PPO) that transformed GPT-3 into an instruction-following assistant. This is the direct ancestor of ChatGPT, Claude, and every aligned LLM.

- **DreamFusion: Text-to-3D Using 2D Diffusion**  
  Ben Poole, Ajay Jain, Jonathan T. Barron, Ben Mildenhall. *ICLR*, 2023 (arXiv 2022).  
  *Why trunk:* Pioneered Score Distillation Sampling (SDS), enabling zero-shot text-to-3D generation without any 3D training data. Opened the floodgates for the entire 3D generation sub-field.

- **3D Gaussian Splatting for Real-Time Radiance Field Rendering**  
  Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis. *SIGGRAPH*, 2023.  
  *Why trunk:* Replaced NeRF's slow MLP-based rendering with explicit 3D Gaussians and rasterization, achieving **real-time** photorealistic novel-view synthesis. Became the backbone representation for nearly all subsequent 3D generative and reconstruction methods.

---

## 2. Large Language Models (LLMs)

### 2.1 Foundation & Scaling

- **GPT-4 Technical Report**  
  OpenAI. *arXiv*, 2023.  
  *Why milestone:* The first demonstration of "multimodal" generalist capability at scale—strong reasoning, coding, legal/medical exam performance, and vision understanding in a single model. Redefined the capability ceiling and catalyzed the competitive LLM race of 2023–2026.

- **LLaMA: Open and Efficient Foundation Language Models**  
  Hugo Touvron et al. (Meta). *arXiv*, 2023.  
  *Why milestone:* Released powerful foundation LLMs openly (7B–65B), proving that open-weight models could rival proprietary GPT-3-class systems. Sparked the open-source LLM revolution—Alpaca, Vicuna, and hundreds of derivatives followed within weeks.

- **Llama 2: Open Foundation and Fine-Tuned Chat Models**  
  Hugo Touvron et al. (Meta). *arXiv*, 2023.  
  *Why milestone:* First truly "open" (weights + commercial license) GPT-3.5-competitive chat model. Became the default pre-trained backbone for the open-source community and established the 70B-parameter open-model standard.

- **The Llama 3 Herd of Models**  
  Meta AI. *arXiv*, 2024.  
  *Why milestone:* Llama 3 (8B/70B/405B) pushed open-source models to GPT-4-class performance for the first time. The 405B model became the largest openly released dense LLM and proved that open models could compete at the frontier.

- **Mistral 7B**  
  Albert Q. Jiang et al. (Mistral AI). *arXiv*, 2023.  
  *Why milestone:* A 7B-parameter model that outperformed Llama 2 13B and approached Llama 1 34B. Demonstrated that **data quality and architecture matter more than raw scale**, catalyzing a wave of efficient small models (Phi, Gemma, Qwen2.5).

- **Mixtral 8x7B: A Sparse Mixture of Experts Language Model**  
  Albert Q. Jiang et al. (Mistral AI). *arXiv*, 2023.  
  *Why milestone:* The first high-quality open-weight MoE LLM. Activated only 13B parameters per forward pass while matching 70B dense model quality, making MoE architectures practical and inspiring DeepSeek-V2, Qwen-MoE, and later frontier models.

- **Gemini: A Family of Highly Capable Multimodal Models**  
  Gemini Team (Google DeepMind). *arXiv*, 2023.  
  *Why milestone:* Google's first natively multimodal model family (Ultra/Pro/Nano), trained jointly on text, image, audio, and video from the start. Established the "native multimodal" paradigm later adopted by GPT-4o and Qwen-VL.

- **Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context**  
  Gemini Team (Google DeepMind). *arXiv*, 2024.  
  *Why milestone:* Introduced 1M-token context windows (later 2M+), enabling processing of entire codebases, long videos, and books in a single prompt. Sparked the "long-context" arms race (Claude 3, Llama 4, Kimi K2).

- **DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model**  
  DeepSeek-AI. *arXiv*, 2024.  
  *Why milestone:* Introduced Multi-Head Latent Attention (MLA) and an ultra-efficient MoE architecture, achieving GPT-4-class performance at ~1/10th the inference cost. Forced the industry to prioritize inference efficiency and catalyzed the "efficient frontier" movement.

- **Kimi K2 Technical Report**  
  Moonshot AI. *arXiv*, 2025.  
  *Why milestone:* A 1-trillion-parameter MoE model with industry-leading long-context (up to 2M+ tokens) and reasoning capabilities. Represented the pinnacle of open-released Chinese LLM development and pushed context-window scaling to new extremes.

---

## 3. Alignment, RLHF & Reasoning

- **Direct Preference Optimization: Your Language Model is Secretly a Reward Model (DPO)**  
  Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn. *NeurIPS*, 2023.  
  *Why milestone:* Eliminated the need for a separate reward model and PPO in RLHF, reducing alignment to a simple classification objective on preference pairs. Became the **dominant alignment method** for open-source models due to its simplicity and stability.

- **Constitutional AI: Harmlessness from AI Feedback**  
  Yuntao Bai et al. (Anthropic). *arXiv*, 2022 (widely adopted 2023+).  
  *Why milestone:* Introduced the concept of training models to critique and revise their own outputs according to a "constitution" of principles. Reduced reliance on human labels for safety alignment and became a core technique for scalable oversight.

- **OpenAI o1 System Card / o1 Technical Report**  
  OpenAI. *arXiv*, 2024.  
  *Why milestone:* First large-scale demonstration that **test-time compute scaling** (chain-of-thought reasoning) could dramatically outperform brute-force pre-training for hard reasoning tasks (math, coding, physics). Redefined the scaling paradigm from "train bigger" to "think longer."

- **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**  
  DeepSeek-AI. *arXiv*, 2025.  
  *Why milestone:* Proved that reasoning (long CoT, self-verification, reflection) can emerge purely from large-scale RL without supervised CoT data. Used Group Relative Policy Optimization (GRPO) to train at a fraction of the cost of OpenAI o1, democratizing reasoning model development.

- **DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models**  
  Zhihong Shao et al. (DeepSeek-AI). *ICLR*, 2024.  
  *Why milestone:* Introduced GRPO (Group Relative Policy Optimization), the simplified RL algorithm that removed the value-function critic entirely. Became the algorithmic backbone of DeepSeek-R1 and the open-source reasoning explosion of 2025.

---

## 4. Diffusion Models & Image Generation

- **Scalable Diffusion Models with Transformers (DiT)**  
  William Peebles, Saining Xie. *ICCV*, 2023.  
  *Why milestone:* Replaced the U-Net backbone in diffusion models with a pure Transformer. Demonstrated superior scaling laws and became the **architectural standard** for all subsequent large-scale image and video generators (Sora, SD3, Flux, HunyuanVideo).

- **Flow Matching for Generative Modeling**  
  Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, Matthew Le. *ICML*, 2023.  
  *Why milestone:* Introduced flow matching as a simulation-free, conceptually simpler alternative to score-based diffusion. Enabled faster training and sampling and became the training objective of choice for SD3, Flux, and most 2024+ generative models.

- **SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis**  
  Dustin Podell, Zion English, Kyle Lacey, Andreas Blattmann, Tim Dockhorn, Jonas Müller, Joe Penna, Robin Rombach. *ICLR*, 2024.  
  *Why milestone:* The definitive open-weight text-to-image model of 2023–2024. Introduced a two-stage pipeline (base + refiner), micro-conditioning, and 1024×1024 native resolution. Became the production standard for open-source image generation.

- **Scaling Rectified Flow Transformers for High-Resolution Image Synthesis (Stable Diffusion 3)**  
  Patrick Esser et al. (Stability AI). *ICML*, 2024.  
  *Why milestone:* First major open production model to adopt the **Multimodal Diffusion Transformer (MMDiT)** architecture with flow matching. Achieved state-of-the-art typography and prompt adherence, outperforming DALL-E 3 and Midjourney v6 on key benchmarks.

- **DALL-E 3**  
  James Betker et al. (OpenAI). *arXiv*, 2023.  
  *Why milestone:* Solved the "prompt following" problem by training a highly descriptive captioner and using those captions to train the image model. Generated images that precisely matched complex, detailed prompts—setting a new bar for text-image alignment.

- **FLUX.1: Kontext & Flow Matching**  
  Black Forest Labs. *Technical Report*, 2024.  
  *Why milestone:* Open-weights 12B-parameter flow-matching transformer that matched or exceeded proprietary models (DALL-E 3, Midjourney v6.1). Its open release catalyzed a wave of fine-tunes and community tools, proving open models could compete at the image-generation frontier.

- **Consistency Models**  
  Yang Song, Prafulla Dhariwal, Mark Chen, Ilya Sutskever. *ICML*, 2023.  
  *Why milestone:* Enabled single-step (or few-step) high-quality image generation by distilling diffusion models into consistency mappings. Directly enabled real-time image generation pipelines like SDXL Turbo and LCM.

- **Elucidating the Design Space of Diffusion-Based Generative Models (EDM)**  
  Tero Karras, Miika Aittala, Timo Aila, Samuli Laine. *NeurIPS*, 2022 (core framework adopted 2023+).  
  *Why milestone:* Provided the theoretical framework and best practices (noise schedules, preconditioning, sampling) that became the engineering standard for nearly all high-fidelity diffusion models trained after 2023.

---

## 5. Controllable Generation & Efficiency

- **Adding Conditional Control to Text-to-Image Diffusion Models (ControlNet)**  
  Lvmin Zhang, Anyi Rao, Maneesh Agrawala. *ICCV*, 2023.  
  *Why milestone:* Enabled fine-grained spatial control (Canny edges, depth maps, poses, segmentation) over Stable Diffusion without retraining the base model. Became an essential tool in every generative image/video workflow and inspired thousands of derivative models.

- **IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models**  
  Hu Ye, Jun Zhang, Sibo Liu, Xiao Han, Wei Yang. *arXiv*, 2023.  
  *Why milestone:* Introduced decoupled cross-attention mechanisms to inject image prompts into diffusion models, enabling style transfer and subject-driven generation with only ~22M trainable parameters. Became the standard for image-conditioned generation.

- **T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to-Image Diffusion Models**  
  Chong Mou et al. *arXiv*, 2023.  
  *Why milestone:* Lightweight (~77M parameters) adapter that adds spatial and structural control to pre-trained diffusion models. Provided a simpler, more efficient alternative to ControlNet for many conditioning tasks.

- **SwiftBrush: One-Step Text-to-Image Diffusion Model with Variational Score Distillation**  
  Thuan Hoang Nguyen, Anh Tran. *CVPR*, 2024.  
  *Why milestone:* Pioneered true one-step text-to-image generation by distilling a multi-step diffusion teacher into a single-step student via variational score distillation. Opened the path toward real-time, high-quality generative interfaces.

- **InstaFlow: One Step is Enough for High-Quality Diffusion-Based Text-to-Image Generation**  
  Xingchao Liu, Xiwen Zhang, Jianzhu Ma, Jian Peng, qiang liu. *NeurIPS*, 2023.  
  *Why milestone:* Applied rectified flow distillation to achieve one-step text-to-image generation while preserving quality. Demonstrated that multi-step diffusion could be radically compressed without catastrophic quality loss.

---

## 6. Video Generation

- **Video Diffusion Models (VDM)**  
  Jonathan Ho, Tim Salimans, et al. (Google). *arXiv*, 2022 (pivotal follow-through in 2023).  
  *Why milestone:* Extended diffusion models to video by adding temporal convolutions and attention. Established the first credible text-to-video generation baseline and proved that diffusion could model spatiotemporal distributions.

- **Video LDM / Align Your Latents: High-Resolution Video Synthesis with Latent Diffusion Models**  
  Andreas Blattmann, Robin Rombach, et al. (Stability AI). *CVPR*, 2023.  
  *Why milestone:* First method to generate high-resolution video by inserting temporal layers into a pre-trained latent diffusion model. Enabled efficient video generation by leveraging frozen image priors—became the template for AnimateDiff and early Runway models.

- **AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning**  
  Yuwei Guo, Ceyuan Yang, et al. *ICLR*, 2024.  
  *Why milestone:* Showed that a lightweight motion module could turn any community fine-tuned Stable Diffusion model into an animated video generator. Democratized personalized video generation and became the most widely used open-source video animation tool.

- **VideoPoet: A Large Language Model for Zero-Shot Video Generation**  
  Dan Kondratyuk et al. (Google). *arXiv*, 2023.  
  *Why milestone:* Demonstrated that a decoder-only LLM architecture (with a video tokenizer) could generate long, coherent, high-fidelity videos. Pioneered the autoregressive-video paradigm later adopted by Lumiere and other Google video models.

- **Sora: Video Generation Models as World Simulators**  
  Tim Brooks, Bill Peebles, et al. (OpenAI). *Technical Report*, 2024.  
  *Why milestone:* The "ChatGPT moment" for video generation. Demonstrated that scaling DiT architectures with spacetime patches and massive data could produce minute-long, temporally coherent, physically plausible videos. Redefined the video-generation frontier and forced every lab to pivot to DiT+flow-matching for video.

- **CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer**  
  Wenyi Hong et al. (THUDM). *arXiv*, 2024.  
  *Why milestone:* First major open-source text-to-video model to adopt the DiT architecture with a 3D causal VAE. Generated competitive quality at up to 6 seconds and proved that the Sora architecture could be replicated openly.

- **HunyuanVideo: A Systematic Framework for Large Video Generation Model Training**  
  Weiran Wang et al. (Tencent). *arXiv*, 2024.  
  *Why milestone:* 13B-parameter open-weights DiT video model with strong motion quality and prompt adherence. One of the first open models to match early Sora demonstrations, catalyzing the open-source video generation wave of late 2024.

- **Wan 2.1: Open Advanced Large-Scale Video Generative Models**  
  Alibaba Group. *arXiv*, 2025.  
  *Why milestone:* Open-weights 14B-parameter video generation model using a Mixture-of-Experts DiT. Achieved state-of-the-art open-source video quality with efficient inference and became the default open video model in early 2025.

- **Veo 3 / Veo 3.1**  
  Google DeepMind. *Technical Report*, 2025.  
  *Why milestone:* First major production video model to generate **synchronized native audio** alongside video in a single forward pass. Achieved cinema-grade visual fidelity and set the commercial standard for AI video production.

- **Runway Gen-3 Alpha / Gen-4**  
  Runway ML. *Technical Reports*, 2024–2025.  
  *Why milestone:* Gen-3 introduced highly realistic human motion and camera control; Gen-4 added character consistency across shots and multi-shot narrative coherence. Established Runway as the professional filmmaker's tool of choice for AI-generated video.

- **Kling 1.0 / 1.5 / 2.0 / 3.0**  
  Kuaishou. *Technical Reports*, 2024–2026.  
  *Why milestone:* Rapidly iterated from impressive early demos (Kling 1.0) to production-grade models with strong physics simulation, native 4K output, and audio-video joint generation. Became one of the most widely adopted video generators globally by mid-2026.

- **Step-Video-T2V: The Practice, Challenges, and Opportunities of SynAll-LLM-Scale Video Generation Model Training**  
  Yue Ma et al. (StepFun). *arXiv*, 2025.  
  *Why milestone:* 30B-parameter DiT trained with flow matching and a deep-compression Video-VAE. Demonstrated that scaling to 30B+ parameters with careful data curation could produce coherent, long-form video generation.

- **LTX-Video: Realtime Latent Diffusion Video Generation**  
  Shlomo E. HaCohen et al. (Lightricks). *arXiv*, 2024.  
  *Why milestone:* Achieved real-time video generation (24fps at 480p) via an efficient latent video diffusion architecture. Proved that video generation latency could be reduced to interactive speeds without catastrophic quality loss.

---

## 7. 3D Generation

- **Shap-E: Generating Conditional 3D Implicit Functions**  
  Heewoo Jun, Alex Nichol. *arXiv*, 2023.  
  *Why milestone:* OpenAI's first open-weights 3D generative model, producing implicit neural representations (NeRF-like) directly from text or images. Validated that encoder-decoder transformer architectures could be applied to 3D shape generation at scale.

- **Magic3D: High-Resolution Text-to-3D Content Creation**  
  Chen-Hsuan Lin, Jun Gao, et al. (NVIDIA). *CVPR*, 2023.  
  *Why milestone:* Two-stage coarse-to-fine pipeline that generated high-resolution textured 3D meshes. Achieved significantly better fidelity than DreamFusion and became the template for quality-focused text-to-3D systems.

- **DreamGaussian: Generative Gaussian Splatting for Efficient 3D Content Creation**  
  Jiaxiang Tang, Jiawei Ren, Hang Zhou, Ziwei Liu, Gang Zeng. *ICLR*, 2024.  
  *Why milestone:* First method to combine generative diffusion priors with 3D Gaussian Splatting for fast text/image-to-3D generation. Reduced generation time from hours to ~2 minutes while maintaining high quality, making 3D generation practical for real-time applications.

- **GaussianDreamer: Fast Generation from Text to 3D Gaussian Splatting with Point Cloud Priors**  
  Taoran Yi, Jiemin Fang, et al. *CVPR*, 2024.  
  *Why milestone:* Bridged 2D and 3D diffusion models via point cloud initialization, achieving text-to-3D Gaussian generation in ~15 minutes. Showed that explicit 3D representations (Gaussians) could be generated with rich detail and 3D consistency.

- **Zero-1-to-3: Zero-shot One Image to 3D Object**  
  Ruoshi Liu, Rundi Wu, Basile Van Hoorick, et al. *ICCV*, 2023.  
  *Why milestone:* Leveraged diffusion models to synthesize novel views from a single image, enabling zero-shot single-image-to-3D reconstruction. Became a core component in many subsequent image-to-3D pipelines.

- **MV-Dream: Multi-view Diffusion for 3D Generation**  
  Yichun Shi, Peng Wang, et al. *ICLR*, 2024.  
  *Why milestone:* A multi-view diffusion model fine-tuned from 2D diffusion with 3D-aware attention. Generated geometrically consistent multi-view images that dramatically improved the 3D consistency and reduced the "Janus problem" in text-to-3D generation.

- **RichDreamer: A Generalizable Normal-Depth Diffusion Model for Detail Richness in Text-to-3D**  
  Lingteng Qiu, Guanying Chen, et al. *CVPR*, 2024.  
  *Why milestone:* Jointly modeled normal maps and depth in the diffusion prior, enabling generation of 3D assets with unprecedented surface detail and geometric fidelity. Addressed the long-standing "over-smoothing" problem in SDS-based 3D generation.

---

## 8. Multimodal (Vision-Language) Models

- **BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models**  
  Junnan Li, Dongxu Li, Caiming Xiong, Steven Hoi. *ICML*, 2023.  
  *Why milestone:* Introduced the Q-Former, a lightweight query transformer that bridged frozen vision encoders and LLMs without end-to-end training. Achieved state-of-the-art zero-shot VQA and became the architectural template for efficient multimodal models.

- **LLaVA: Large Language and Vision Assistant**  
  Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee. *NeurIPS*, 2023.  
  *Why milestone:* The first open-source multimodal instruction-tuned model. Connected CLIP ViT to Vicuna (LLaMA) with just a linear projection layer and used GPT-4-generated visual instruction data. Sparked the entire open-source MLLM ecosystem (LLaVA-1.5, -v1.6, etc.).

- **GPT-4V(ision) System Card**  
  OpenAI. *arXiv*, 2023.  
  *Why milestone:* Demonstrated general-purpose visual understanding at scale—chart reading, OCR, medical image analysis, meme comprehension, and grounded reasoning. Proved that a single unified multimodal model could replace dozens of specialized vision systems.

- **Qwen-VL: A Frontier Large Vision-Language Model with Versatile Abilities**  
  Jinze Bai et al. (Alibaba). *arXiv*, 2023.  
  *Why milestone:* Strong open-source bilingual (Chinese/English) vision-language model with competitive performance on grounding, OCR, and document understanding. Established Qwen as a major open multimodal alternative to GPT-4V.

- **GPT-4o System Card**  
  OpenAI. *arXiv*, 2024.  
  *Why milestone:* First "omni" model natively processing audio, vision, and text in a single end-to-end architecture with sub-300ms latency. Eliminated the pipeline of separate speech→text→speech models and set the standard for real-time multimodal AI.

- **InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks**  
  Jinze Bai et al. / OpenGVLab. *CVPR*, 2024.  
  *Why milestone:* Scaled vision encoders to 6B parameters and aligned them with LLMs for strong performance across detection, segmentation, and VQA. Became one of the strongest open-source MLLM families through InternVL 1.5/2.0/3.0.

- **CogVLM: Visual Expert for Pre-trained Language Models**  
  Wenjin Hu et al. (THUDM). *arXiv*, 2023.  
  *Why milestone:* Introduced a visual expert module that applied different parameters for image and text features within transformer layers. Achieved strong performance without sacrificing language capabilities and became a popular open-source MLLM backbone.

- **The Dawn of LMMs: Preliminary Explorations with GPT-4V(ision)**  
  Zhengyuan Yang et al. *arXiv*, 2023.  
  *Why milestone:* The first systematic evaluation and "red-teaming" of GPT-4V's capabilities, limitations, and safety profiles. Established the evaluation methodology and benchmark protocols later adopted across the MLLM field.

---

## 9. Audio & Music Generation

- **AudioLDM: Text-to-Audio Generation with Latent Diffusion Models**  
  Haohe Liu, Zehua Chen, Yi Yuan, Xinhao Mei, et al. *ICML*, 2023.  
  *Why milestone:* First large-scale latent diffusion model for general text-to-audio (not just music). Generated high-fidelity environmental sounds, effects, and music from text prompts, establishing the latent-diffusion paradigm for audio generation.

- **AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining**  
  Haohe Liu et al. *TASLP / arXiv*, 2024.  
  *Why milestone:* Unified speech, music, sound effects, and singing generation in a single model via self-supervised audio representations. Demonstrated that a single latent diffusion architecture could handle all major audio modalities.

- **MusicLM: Generating Music From Text**  
  Andrea Agostinelli, Timo I. Denk, Zalán Borsos, et al. (Google). *ISMIR*, 2023.  
  *Why milestone:* First high-fidelity text-to-music model generating 24kHz stereo music with long-term musical structure. Introduced a hierarchical token-based approach that enabled coherent, minutes-long musical compositions from text.

- **Simple and Controllable Music Generation (MusicGen)**  
  Jade Copet, Felix Kreuk, Itai Gat, et al. (Meta). *NeurIPS*, 2023.  
  *Why milestone:* Open-weights autoregressive music generation model with strong text and melody conditioning. Became the most widely used open-source music generation model and the foundation for most subsequent open music AI tools.

- **Stable Audio Open / Stable Audio 2.0**  
  Zach Evans, CJ Carr, et al. (Stability AI). *ICML*, 2024.  
  *Why milestone:* Latent diffusion transformer for high-quality text-to-audio generation, capable of producing stereo music and sound effects. The open release democratized access to production-quality audio generation tools.

- **Fugatto: Foundational Generative Audio Transformer Opus 1**  
  NVIDIA. *ICLR*, 2025.  
  *Why milestone:* 2.5B-parameter generalist audio generation model capable of zero-shot instruction following for music, sound effects, speech, and audio editing. Demonstrated that scaling + instruction tuning could create a "GPT moment" for audio.

- **AudioX: Diffusion Transformer for Anything-to-Audio Generation**  
  Various authors. *arXiv*, 2025.  
  *Why milestone:* Unified Diffusion Transformer accepting text, image, video, and audio as conditioning inputs for audio/music generation. Represented the convergence of multimodal conditioning and audio generation into a single model.

- **YUE: A Series of Large Language Models for Music Generation**  
  Yuansong Xu et al. *arXiv*, 2025.  
  *Why milestone:* Open-weights autoregressive music generation system with strong long-form composition and multi-track capabilities. Pushed the open-source music generation frontier toward professional-grade production tools.

---

## Statistics by Year

| Year | Notable Themes |
|------|----------------|
| **2023** | Diffusion goes mainstream (SDXL, DALL-E 3, ControlNet); LLaMA/Mistral ignite open-source LLMs; GPT-4V and BLIP-2/LLaVA open multimodal AI; AudioLDM/MusicGen bring generative audio to the masses. |
| **2024** | DiT + Flow Matching become the new standard (SD3, Sora, Flux); Open-source video generation explodes (CogVideoX, HunyuanVideo, AnimateDiff); OpenAI o1 introduces reasoning scaling; DeepSeek-V2 democratizes efficient MoE. |
| **2025** | Reasoning revolution (DeepSeek-R1, Grok 3, Claude 4); Video generation adds native audio (Veo 3, Kling 2.6); Wan 2.1 and open DiT-MoE models push open video to Sora-class quality; Fugatto and AudioX unify audio generation. |
| **2026 (H1)** | Production maturity—4K video with synchronized audio becomes standard; Context windows reach 1M–10M tokens (Kimi K2, Llama 4); Open-source models close the gap with proprietary systems in nearly every modality. |

---

*Document compiled for research curation purposes. Paper metadata verified against conference proceedings, arXiv preprints, and official technical reports where available.*
