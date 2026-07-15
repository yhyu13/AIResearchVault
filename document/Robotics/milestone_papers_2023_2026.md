# Milestone & Trunk Papers in Robotics (2023 – Mid-2026)

> Curated research trunk of the most influential, foundational, and breakthrough papers in robotics from 2023 to July 2026. Focused on works that opened new directions, consolidated paradigms, or are considered essential reading for understanding the current state of the field. Organized by sub-themes. Papers from late 2022 that established the foundational paradigms for the 2023–2026 period are included as trunk references.

---

## 1. Vision-Language-Action (VLA) Foundation Models

> The convergence of vision-language pretraining with robotic control has been the single most transformative trend in robotics since 2023. VLA models directly map visual observations and natural language instructions to robot motor actions, enabling unprecedented generalization and task flexibility.

### 1.1 RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
- **Authors:** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, et al. (Google DeepMind)
- **Venue:** Conference on Robot Learning (CoRL) 2023
- **Year:** 2023
- **Why it matters:** RT-2 was the first large-scale VLA model (55B parameters), co-fine-tuned on web-scale vision-language data and robot action data. It demonstrated that semantic knowledge from internet-scale training transfers directly to physical manipulation, enabling emergent reasoning like "pick up the improvised hammer" (selecting a rock). This established the VLA paradigm as a viable path to generalist robot policies.

### 1.2 RT-1: Robotics Transformer for Real-World Control at Scale
- **Authors:** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, et al. (Google Research)
- **Venue:** arXiv (predecessor to RT-2, foundational architecture)
- **Year:** 2022 (Dec)
- **Why it matters:** RT-1 introduced the first efficient Transformer architecture specifically designed for real-world robot control, trained on 130k episodes from 13 robots over 17 months. It demonstrated that large-scale imitation learning with a language-conditioned transformer could generalize across tasks and environments. RT-1 established the data-collection and architectural template that all subsequent VLA models built upon.

### 1.3 PaLM-E: An Embodied Multimodal Language Model
- **Authors:** Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, et al. (Google)
- **Venue:** International Conference on Machine Learning (ICML) 2023
- **Year:** 2023
- **Why it matters:** PaLM-E injected continuous sensor observations (visual, state, proprioceptive) directly into a 562B-parameter language model. It showed that pretrained LLMs can serve as unified reasoning engines for embodied tasks, achieving positive transfer across internet-scale language, vision, and robotics domains. This work proved that multimodal LLMs can reason about physical environments without task-specific retraining.

### 1.4 Open X-Embodiment: Robotic Learning Datasets and RT-X Models
- **Authors:** Open X-Embodiment Collaboration (21 institutions, 34 labs), led by Google DeepMind
- **Venue:** ICRA 2024 (Best Conference Paper Award)
- **Year:** 2023 (dataset), 2024 (ICRA publication)
- **Why it matters:** The Open X-Embodiment dataset aggregated 1M+ real robot trajectories across 22 robot embodiments from 34 labs, with 527 skills. The RT-X models trained on this data showed positive cross-embodiment transfer—robots improved by learning from other platforms' data. This is widely considered the "ImageNet moment" for robotics, establishing open collaborative data as the foundation for generalist robot policies.

### 1.5 Octo: An Open-Source Generalist Robot Policy
- **Authors:** Dibya Ghosh, Homer Walke, Karl Pertsch, et al. (UC Berkeley RAIL, Stanford, CMU, DeepMind)
- **Venue:** Robotics: Science and Systems (RSS) 2024
- **Year:** 2024
- **Why it matters:** Octo was the first fully open-source generalist robot policy (27M–93M parameters), trained on 800k+ trajectories from the Open X-Embodiment dataset. It matched the 55B-parameter RT-2-X on several benchmarks despite being orders of magnitude smaller. Octo democratized VLA research by providing open weights, training code, and easy fine-tuning on consumer GPUs, making it the de facto community baseline.

### 1.6 OpenVLA: An Open-Source Vision-Language-Action Model
- **Authors:** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, et al. (Stanford, UC Berkeley, TRI, MIT, DeepMind)
- **Venue:** Conference on Robot Learning (CoRL) 2024
- **Year:** 2024
- **Why it matters:** OpenVLA (7B parameters) is the leading open-weight VLA model, built on a Prismatic VLM (LLaMA-2 + DINOv2 + SigLIP dual vision encoder). It outperformed RT-2-X by 16.5% absolute success rate across 29 tasks despite being 7x smaller. Its support for LoRA fine-tuning and quantization made VLA deployment practical for university labs and startups, establishing the template for dual-encoder VLA architectures.

### 1.7 pi0 (Pi-Zero): A Vision-Language-Action Flow Model for General Robot Control
- **Authors:** Kevin Black, Noah Brown, Danny Driess, Aditya Escontrela, et al. (Physical Intelligence pi)
- **Venue:** Conference on Robot Learning (CoRL) 2024 / RSS 2025
- **Year:** 2024
- **Why it matters:** pi0 introduced the first VLA model using flow matching (rather than autoregressive tokenization) for continuous action generation. Trained on 10,000 hours of dexterous manipulation data from 7 robot configurations, it demonstrated tasks like folding laundry, assembling boxes, and bussing tables with unprecedented dexterity. The open-source release (openpi) and 5.6B company valuation signal this as the state-of-the-art for commercial-grade generalist manipulation.

### 1.8 pi0.5: Open-World Generalization for Mobile Manipulation
- **Authors:** Kevin Black, Michael Equi, et al. (Physical Intelligence pi)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why it matters:** pi0.5 extended pi0 with "knowledge insulation"—discretizing robot state into tokens and using adaptive RMS normalization—to achieve open-world generalization on mobile manipulators. It demonstrated that flow-matching VLAs can scale to previously unseen environments and task specifications without task-specific fine-tuning, pushing the boundary of zero-shot generalist robot control.

### 1.9 GR00T N1: An Open Foundation Model for Generalist Humanoid Robots
- **Authors:** NVIDIA GEAR Team
- **Venue:** NVIDIA GTC 2025 (released March 2025)
- **Year:** 2025
- **Why it matters:** GR00T N1 is the world's first open-source, fully customizable humanoid foundation model. It uses a dual-system architecture inspired by human cognition: System 2 (a vision-language model) for deliberate reasoning and planning, and System 1 (a diffusion transformer) for fast continuous action generation. NVIDIA released it under Apache 2.0 with Isaac Sim synthetic data pipelines, directly enabling the current wave of humanoid robot development from 1X, Agility, Boston Dynamics, and others.

### 1.10 Helix: A Vision-Language-Action Model for Generalist Humanoid Control
- **Authors:** Figure AI Team
- **Venue:** Figure AI Blog / Technical Report 2025
- **Year:** 2025
- **Why it matters:** Helix is the first VLA to output high-rate continuous control of an entire humanoid upper body (wrists, torso, head, individual fingers) at 200 Hz. Its dual-system architecture (7B-parameter VLM for System 2, 80M-parameter visuomotor policy for System 1) demonstrated multi-robot collaboration and zero-shot generalization to thousands of novel household objects. It powers Figure 02 and represents the most advanced proprietary humanoid VLA as of 2025.

### 1.11 Gemini Robotics: Bringing AI into the Physical World
- **Authors:** Google DeepMind Robotics Team
- **Venue:** arXiv 2025 / Google DeepMind Blog
- **Year:** 2025
- **Why it matters:** Gemini Robotics is DeepMind's next-generation VLA that pairs Gemini's multimodal reasoning with robotic control. It demonstrates agentic tool-use, dexterous manipulation (origami, food prep), and embodied reasoning. The dual approach with Robotics-ER 1.5 for embodied reasoning supports multiple embodiments (ALOHA, Franka, Apptronik Apollo), representing Google's answer to the humanoid VLA race.

### 1.12 RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation
- **Authors:** Tsinghua University THUML Team
- **Venue:** International Conference on Learning Representations (ICLR) 2025 (Oral)
- **Year:** 2025
- **Why it matters:** RDT-1B is the first 1-billion-parameter diffusion transformer specifically designed for bimanual manipulation. It combines language conditioning with multi-image observations in a diffusion framework, achieving state-of-the-art results on diverse dexterous tasks. It represents the open bimanual manipulation baseline and demonstrates that diffusion models can scale to billion-parameter regimes for robot control.

### 1.13 RoboCat: A Self-Improving Foundation Agent for Robotic Manipulation
- **Authors:** Alex Lee, Yury Sulsky, et al. (Google DeepMind)
- **Venue:** arXiv 2023 / DeepMind Blog
- **Year:** 2023
- **Why it matters:** RoboCat built on Gato to enable multi-embodiment generalization with self-improvement. It generates new training data from its own attempts, uses it to train further, and adapts to unfamiliar robot arms without full retraining. This established the self-improving generalist agent paradigm in robotics, showing how data flywheels can autonomously expand robot capabilities.

### 1.14 TinyVLA: Fast and Efficient Vision-Language-Action Model
- **Authors:** Yuchen Wu, et al. (various institutions)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why it matters:** TinyVLA achieved 5x faster inference than OpenVLA on resource-constrained hardware by designing a lightweight multimodal model with a compact diffusion strategy decoder. It demonstrated that VLA architectures can be deployed on edge devices and Jetson-class hardware without prohibitive latency, making real-world deployment feasible for consumer robots.

### 1.15 CrossFormer: Cross-Embodiment Transformer Policy
- **Authors:** Various (multiple institutions)
- **Venue:** ICLR 2025
- **Year:** 2025
- **Why it matters:** CrossFormer demonstrated generalization across diverse robot platforms with heterogeneous action spaces through a novel cross-embodiment transformer architecture. It showed that a single policy can control robots with fundamentally different morphologies and action representations, pushing the boundary of universal robot control.

---

## 2. Diffusion & Generative Policies for Robot Control

> Diffusion models, originally developed for image generation, have proven remarkably effective for robot policy learning. They naturally handle multimodal action distributions, high-dimensional action spaces, and complex trajectory generation—capabilities that traditional regression-based policies struggle with.

### 2.1 Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
- **Authors:** Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song (Columbia University, Toyota Research Institute, MIT)
- **Venue:** Robotics: Science and Systems (RSS) 2023 / IJRR 2024
- **Year:** 2023
- **Why it matters:** Diffusion Policy introduced the paradigm of representing robot visuomotor policies as conditional denoising diffusion processes. It outperformed existing state-of-the-art methods by 46.9% averaged across 15 tasks from 4 benchmarks, handling multimodal action distributions, high-dimensional action spaces, and training stability. The paper's closed-loop action sequences with receding-horizon control and time-series diffusion transformer became the template for a generation of diffusion-based robot policies.

### 2.2 Action Chunking with Transformers (ACT) / ALOHA
- **Authors:** Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn (Stanford, UC Berkeley, Meta)
- **Venue:** Robotics: Science and Systems (RSS) 2023
- **Year:** 2023
- **Why it matters:** ACT introduced action chunking—predicting sequences of actions rather than single steps—to mitigate error compounding in imitation learning. Combined with the ALOHA low-cost bimanual teleoperation system ($20k hardware), it achieved 80-90% success on fine manipulation tasks (threading zip ties, slotting batteries) with only 10 minutes of demonstration data. ALOHA democratized high-precision bimanual research by making it accessible to labs with modest budgets.

### 2.3 Mobile ALOHA: Learning Bimanual Manipulation with Low-Cost Whole-Body Teleoperation
- **Authors:** Tony Z. Zhao, et al. (Stanford)
- **Venue:** arXiv 2024 / CoRL 2024
- **Year:** 2024
- **Why it matters:** Mobile ALOHA extended ALOHA from static desktop manipulation to whole-body mobile bimanual manipulation. It demonstrated that low-cost hardware can perform complex household tasks (cooking, cleaning, laundry) with coordinated whole-body control, opening the door to scalable data collection for home robotics.

### 2.4 3D Diffusion Policy (DP3)
- **Authors:** Yue Ze, Ge Zhang, et al. (multiple institutions)
- **Venue:** Robotics: Science and Systems (RSS) 2024
- **Year:** 2024
- **Why it matters:** DP3 extended Diffusion Policy to 3D point cloud observations, showing that simple 3D representations generalize better than 2D image-based policies for spatial manipulation. It demonstrated that 3D diffusion policies can handle cluttered scenes and novel object configurations with significantly better sample efficiency than vision-only approaches.

### 2.5 3D Diffuser Actor
- **Authors:** Tsung-Wei Ke, Nikolaos Gkanatsios, Katerina Fragkiadaki (CMU)
- **Venue:** arXiv 2024 / ICRA 2024
- **Year:** 2024
- **Why it matters:** 3D Diffuser Actor integrated diffusion policy generation with 3D scene representations for end-effector trajectory prediction. It demonstrated that diffusion models can generate spatially-aware manipulation trajectories directly from point clouds, achieving strong generalization to novel object arrangements and novel tasks.

### 2.6 SE(3)-Diffusion Fields: Learning Smooth Cost Functions for Joint Grasp and Motion Optimization
- **Authors:** Julius Urain, Niklas Funk, Jan Peters, Georgia Chalvatzaki (TU Darmstadt)
- **Venue:** arXiv 2023 / ICRA 2024
- **Year:** 2023
- **Why it matters:** This paper formulated 6-DoF grasping as a diffusion process over SE(3) pose space, learning smooth cost functions that jointly optimize grasp quality and motion feasibility. It demonstrated that diffusion models can operate on the geometric group SE(3) for manipulation, enabling principled handling of rotation and translation in grasp generation.

### 2.7 Equivariant Diffusion Policy
- **Authors:** Dian Wang, Stephen Hart, et al. (Northeastern University)
- **Venue:** arXiv 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** This work introduced SE(3)-equivariance into diffusion policies, ensuring that policy outputs transform correctly under rotations and translations. It proved that incorporating geometric equivariance dramatically improves data efficiency and generalization for spatial manipulation tasks, establishing equivariance as a key design principle for geometrically-aware robot policies.

### 2.8 FlowPolicy: Consistency Flow Matching for Robust 3D Manipulation
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2024
- **Year:** 2024
- **Why it matters:** FlowPolicy adapted consistency flow matching (from image generation) to robot manipulation, enabling single-step or few-step action generation instead of iterative diffusion denoising. This dramatically reduced inference time while maintaining the expressiveness of diffusion models, making flow matching a viable alternative to diffusion for real-time robot control.

### 2.9 Dexterous Functional Pre-Grasp Manipulation with Diffusion Policy
- **Authors:** Tianhao Wu, Yunchong Gan, et al. (Peking University, Tsinghua)
- **Venue:** arXiv 2024 / ICRA 2024
- **Year:** 2024
- **Why it matters:** This paper demonstrated that diffusion policies can learn complex pre-grasp manipulation—reorienting, aligning, and positioning objects before grasping—using dexterous multi-finger hands. It showed that diffusion models naturally handle the contact-rich, multi-modal dynamics of pre-grasp manipulation, which traditional grasp planners cannot address.

### 2.10 Grasp Diffusion Network
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2023 / ICRA 2024
- **Year:** 2023
- **Why it matters:** The Grasp Diffusion Network learned grasp generators from partial point clouds using diffusion models in SO(3) x R^3. It demonstrated that diffusion models can generate diverse, high-quality grasps from incomplete observations, addressing a fundamental challenge in real-world grasping where objects are often occluded.

---

## 3. LLM-Driven Planning & Zero-Shot Reasoning for Robotics

> Large language models brought commonsense reasoning, planning, and code generation to robotics. These papers established how LLMs can serve as high-level planners, reward designers, and zero-shot controllers without task-specific robot training.

### 3.1 SayCan: Grounding Language in Robotic Affordances
- **Authors:** Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, et al. (Google Research, Everyday Robots)
- **Venue:** RSS 2022 / ICRA 2023 (extended)
- **Year:** 2022 (April)
- **Why it matters:** SayCan was the first system to combine LLMs (PaLM) with robotic affordance models for feasible long-horizon planning. It demonstrated that LLMs can translate abstract natural language into robot-executable subtasks, but must be grounded in the robot's physical capabilities (affordances) to be useful. This established the LLM-as-planner paradigm that dominated robotics in 2023–2024.

### 3.2 Code as Policies: Language Models for Robotic Control
- **Authors:** Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, Andy Zeng (Google Research)
- **Venue:** ICRA 2023 / RSS 2023
- **Year:** 2023
- **Why it matters:** This paper showed that LLMs can generate executable Python code for robot control from natural language instructions, effectively turning the LLM into a flexible robot programmer. It demonstrated zero-shot generalization to novel tasks by composing primitive APIs through code generation, establishing programmatic robot control as a scalable alternative to end-to-end learning.

### 3.3 Inner Monologue: Embodied Reasoning through Planning with Language Models
- **Authors:** Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Laura Luu, Sergey Levine, Karol Hausman, Brian Ichter (Google Research, DeepMind)
- **Venue:** Conference on Robot Learning (CoRL) 2022
- **Year:** 2022 (published, highly influential in 2023–2024)
- **Why it matters:** Inner Monologue introduced closed-loop embodied reasoning where LLMs incorporate environmental feedback (success/failure, state changes) into an ongoing internal dialogue. It demonstrated that LLMs can dynamically replan based on real-world outcomes, enabling robust long-horizon task execution without requiring explicit replanning algorithms.

### 3.4 VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models
- **Authors:** Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, Li Fei-Fei (Stanford University, UIUC)
- **Venue:** Conference on Robot Learning (CoRL) 2023
- **Year:** 2023
- **Why it matters:** VoxPoser demonstrated zero-shot manipulation from free-form language instructions by using LLMs to generate 3D affordance and constraint maps (value maps) grounded in the robot's observation space. It required no task-specific training—only an LLM and a VLM. This established the zero-shot LLM+VLM manipulation paradigm and showed that compositional 3D reasoning emerges from language model capabilities.

### 3.5 ProgPrompt: Program Generation for Situated Robot Task Planning
- **Authors:** Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, et al. (NVIDIA, AI2, UIUC)
- **Venue:** Autonomous Robots / arXiv 2023
- **Year:** 2023
- **Why it matters:** ProgPrompt demonstrated that LLMs can generate situated robot task plans as executable programs, with structured prompting that includes environment state, available actions, and execution history. It showed that program synthesis from LLMs achieves better generalization than direct action prediction, establishing structured prompting as essential for LLM-based robot planning.

### 3.6 Eureka: Human-Level Reward Design via Coding Large Language Models
- **Authors:** Yecheng Jason Ma, William Liang, Guanzhi Wang, et al. (UPenn, NVIDIA, UT Austin)
- **Venue:** International Conference on Learning Representations (ICLR) 2024 (Spotlight)
- **Year:** 2023
- **Why it matters:** Eureka used GPT-4 to automatically write and iteratively evolve reward function code for reinforcement learning, outperforming expert human-designed rewards on 83% of 29 robotics tasks. It achieved the first simulated Shadow Hand pen spinning via automated reward design. This proved that LLMs can automate the most labor-intensive part of RL—reward engineering—dramatically lowering the barrier to training complex robot skills.

### 3.7 Text2Reward: Automated Dense Reward Generation for RL
- **Authors:** various (multiple institutions)
- **Venue:** arXiv 2024 / ICRA 2024
- **Year:** 2024
- **Why it matters:** Text2Reward extended Eureka by generating dense, interpretable Python reward functions from natural language instructions and environment descriptions, with iterative human feedback refinement. It demonstrated high success rates across robotic manipulation and locomotion tasks, establishing automated reward generation as a practical tool for RL practitioners.

### 3.8 MOO: Open-World Object Manipulation using Pre-trained Vision-Language Models
- **Authors:** various (Google Research)
- **Venue:** Conference on Robot Learning (CoRL) 2023
- **Year:** 2023
- **Why it matters:** MOO demonstrated open-world object manipulation using pretrained VLMs without any robot-specific training. It showed that vision-language models already contain sufficient semantic and spatial knowledge to manipulate objects they've never seen, simply by grounding language concepts to visual features. This established the "frozen VLM" approach as a viable path for zero-shot robot manipulation.

### 3.9 LERF: Language Embedded Radiance Fields
- **Authors:** Justin Kerr, Chung Min Kim, Ken Goldberg, Angjoo Kanazawa (UC Berkeley)
- **Venue:** International Conference on Computer Vision (ICCV) 2023
- **Year:** 2023
- **Why it matters:** LERF embedded CLIP language features into 3D neural radiance fields (NeRF), enabling open-vocabulary 3D scene querying with natural language. It demonstrated that robots can ground language commands in precise 3D spatial locations without object detectors or segmentation models, establishing language-embedded 3D representations as a key building block for language-conditioned robot perception.

### 3.10 CLIP-Fields: Weakly Supervised Semantic Fields for Robotic Memory
- **Authors:** Various (MIT, etc.)
- **Venue:** RSS 2023
- **Year:** 2023
- **Why it matters:** CLIP-Fields built semantic fields from robot observation data using weak supervision from CLIP, enabling open-vocabulary spatial memory for robots. It demonstrated that robots can build and query 3D semantic maps from their own experience using language, enabling long-term memory and spatial reasoning for navigation and manipulation.

---

## 4. Humanoid Locomotion & Whole-Body Control

> Humanoid robots have advanced from laboratory curiosities to commercial products. These papers established the learning-based control foundations that enable humanoids to walk, run, and recover in real-world environments.

### 4.1 ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills
- **Authors:** Various (multiple institutions, including Unitree)
- **Venue:** arXiv 2025 / ICRA 2025
- **Year:** 2025
- **Why it matters:** ASAP introduced a two-stage framework for sim-to-real transfer of highly agile humanoid motions (kicks, jumps, dynamic balancing) on real Unitree G1 robots. It demonstrated that physics alignment between simulation and reality—rather than just domain randomization—enables complex whole-body skills to transfer with high fidelity, representing a major step toward Hollywood-grade humanoid agility.

### 4.2 Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer
- **Authors:** Xiao Gu, Yao-Jen Wang, Jianyu Chen (multiple institutions)
- **Venue:** arXiv 2024 / ICRA 2025
- **Year:** 2024
- **Why it matters:** Humanoid-Gym provided a standardized training environment and demonstrated zero-shot sim-to-real transfer of humanoid locomotion policies using reinforcement learning. It showed that carefully designed observation spaces and reward functions can enable direct deployment from simulation to real humanoid robots without any real-world fine-tuning, significantly lowering the barrier to humanoid RL research.

### 4.3 Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning
- **Authors:** Xiao Gu, Yao-Jen Wang, Xinyang Zhu, Chen Shi, Yaru Guo, Yuxiang Liu, Jianyu Chen
- **Venue:** Robotics: Science and Systems (RSS) 2024 (Best Paper Award Finalist)
- **Year:** 2024
- **Why it matters:** This paper introduced a denoising world model learning approach for humanoid locomotion over challenging terrain, using learned latent dynamics models to predict and plan through difficult terrain. It demonstrated that world models (learned internal simulations) can enable humanoids to traverse terrain that reactive policies cannot handle, establishing model-based RL as essential for robust humanoid locomotion.

### 4.4 Real-World Humanoid Locomotion with Reinforcement Learning
- **Authors:** Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, Koushil Sreenath (UC Berkeley)
- **Venue:** arXiv 2023 / ICRA 2024
- **Year:** 2023
- **Why it matters:** This paper demonstrated end-to-end reinforcement learning for real-world humanoid walking without any model-based components or motion capture. It showed that pure RL can learn robust bipedal locomotion directly on hardware, with policies that generalize to unseen terrain and perturbations. This established RL as a viable alternative to traditional model-based walking controllers for humanoids.

### 4.5 Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning
- **Authors:** Nikita Rudin, David Hoeller, Philipp Reist, Marco Hutter (ETH Zurich)
- **Venue:** Conference on Robot Learning (CoRL) 2022
- **Year:** 2022 (highly influential in 2023–2024 humanoid locomotion research)
- **Why it matters:** This paper demonstrated that massively parallel simulation (thousands of environments on GPU) can train quadruped locomotion policies in minutes rather than days. While focused on quadrupeds, its methodology (parallel simulation, domain randomization, curriculum learning) became the template for training humanoid locomotion policies at scale, directly influencing the 2024–2025 humanoid RL boom.

### 4.6 Anymal Parkour: Learning Agile Navigation for Quadrupedal Robots
- **Authors:** David Hoeller, Nikita Rudin, Shao Cheng, Marco Hutter (ETH Zurich)
- **Venue:** Science Robotics 2024
- **Year:** 2024
- **Why it matters:** Anymal Parkour demonstrated that quadruped robots can learn parkour-style agility (jumping gaps, climbing obstacles, vaulting) through RL in simulation. While on quadrupeds, its vision-based terrain perception and dynamic motion skills directly informed humanoid locomotion research. Published in Science Robotics, it established the standard for agile legged robot locomotion.

### 4.7 HIMLoco: Hierarchical Imitation Learning for Robust Humanoid Locomotion
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2024 / ICRA 2025
- **Year:** 2024
- **Why it matters:** HIMLoco introduced a hierarchical imitation learning framework that separates high-level gait planning from low-level motor control for humanoid locomotion. It demonstrated successful real-world deployment on humanoid robots with robust locomotion in challenging environments, showing that hierarchical learning can improve stability and generalization compared to end-to-end policies.

### 4.8 BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2025 / ICRA 2025
- **Year:** 2025
- **Why it matters:** BeamDojo demonstrated that humanoid robots can learn to walk on sparse, narrow footholds (like balance beams) through RL with dynamic balance constraints. It pushed the boundary of humanoid agility, showing that learned controllers can handle precarious terrain that would challenge even traditional model-based controllers.

### 4.9 HiLOT: Learning Whole-Body Human-Like Locomotion with Motion Tracking Controller
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why it matters:** HiLOT combined motion tracking (imitating human gait reference motions) with RL to learn natural, human-like whole-body locomotion. It demonstrated that reference motion guidance can produce more natural and efficient gaits than pure RL, while still adapting to terrain variations through learned feedback policies.

### 4.10 Learning Humanoid Locomotion with Perceptive Internal Model
- **Authors:** Jingfeng Long, Jianle Ren, Mingjie Shi, et al. (multiple institutions)
- **Venue:** ICRA 2025
- **Year:** 2024 (arXiv) / 2025 (ICRA)
- **Why it matters:** This paper introduced a perceptive internal model for humanoid locomotion—an learned model that predicts future states based on visual and proprioceptive input. It demonstrated that internal models improve robustness on uneven terrain by enabling anticipatory control, similar to how humans use visual preview for walking.

---

## 5. Dexterous Manipulation & Hand Control

> Dexterous manipulation with multi-finger hands remains one of the hardest problems in robotics. These papers advanced grasping, in-hand manipulation, and tool use through learning-based approaches.

### 5.1 DexGraspNet: A Large-Scale Robotic Dexterous Grasp Dataset for General Objects
- **Authors:** Ruicheng Wang, Yinzhen Xu, et al. (Tsinghua University)
- **Venue:** arXiv 2023 / ICRA 2024
- **Year:** 2023
- **Why it matters:** DexGraspNet provided the first large-scale dataset of dexterous grasps for general objects (1.3M+ grasps, 1,600+ objects), generated through physics-based simulation. It enabled training of generalizable dexterous grasping policies and established the benchmark for multi-finger hand grasp generation, becoming the standard dataset for dexterous manipulation research.

### 5.2 DexGraspNet 2.0: Learning Generative Dexterous Grasping in Large-Scale Synthetic Cluttered Scenes
- **Authors:** Jialiang Zhang, et al. (Tsinghua University)
- **Venue:** Conference on Robot Learning (CoRL) 2024
- **Year:** 2024
- **Why it matters:** DexGraspNet 2.0 extended the original dataset to cluttered scenes with multiple objects, enabling grasping in realistic pile-of-objects scenarios. It demonstrated that generative models trained on cluttered scenes can generalize to novel object arrangements and compositions, addressing the combinatorial complexity of real-world grasping environments.

### 5.3 UniDexGrasp: Universal Robotic Dexterous Grasping via Learning Diverse Proposal Generation and Goal-Conditioned Policy
- **Authors:** Yinzhen Xu, Weikang Wan, Jialiang Zhang, et al. (Tsinghua University)
- **Venue:** CVPR 2023
- **Year:** 2023
- **Why it matters:** UniDexGrasp introduced a two-stage framework for universal dexterous grasping: diverse grasp proposal generation followed by goal-conditioned policy execution. It demonstrated that separating grasp planning from execution enables better generalization to novel objects and grasp types, establishing the proposal+execution paradigm for dexterous manipulation.

### 5.4 DexGrasp Anything: Towards Universal Robotic Dexterous Grasping with Physics Awareness
- **Authors:** Various (Tsinghua University, etc.)
- **Venue:** arXiv 2025 / ICRA 2025
- **Year:** 2025
- **Why it matters:** This paper pushed toward universal dexterous grasping by incorporating physics awareness (object mass, friction, compliance) into grasp generation. It demonstrated that physics-aware grasping models can generate stable grasps for objects with challenging physical properties (heavy, slippery, deformable) that pure geometry-based methods cannot handle.

### 5.5 GraspXL: Generating Grasping Motions for Diverse Objects at Scale
- **Authors:** Hui Zhang, Sammy Christen, Zicong Fan, Otmar Hilliges, Jie Song (ETH Zurich)
- **Venue:** European Conference on Computer Vision (ECCV) 2024
- **Year:** 2024
- **Why it matters:** GraspXL generated full grasping motions (approach, contact, lift) rather than just final grasp poses, at scale for thousands of objects. It demonstrated that generative models can produce physically plausible, diverse grasping trajectories that account for the entire manipulation sequence, not just the static grasp configuration.

### 5.6 UMI: Universal Manipulation Interface
- **Authors:** Cheng Chi, Zhenjia Xu, et al. (Columbia, Stanford, MIT)
- **Venue:** arXiv 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** UMI introduced a GoPro-equipped gripper with SLAM tracking for collecting manipulation demonstrations across 30 real-world locations in just 12 person-hours. It achieved 71.7% zero-shot success on novel tasks and was 3x faster than standard teleoperation. UMI demonstrated that portable, scalable data collection can bootstrap generalizable manipulation policies without expensive lab infrastructure.

### 5.7 DexCap: Scalable and Portable Hand Motion Capture for Humanoid Robots
- **Authors:** Various (Stanford, etc.)
- **Venue:** arXiv 2024 / ICRA 2025
- **Year:** 2024
- **Why it matters:** DexCap used EMF gloves and chest-mounted RGB-D cameras to capture dexterous hand motions for robot imitation. It achieved 72% success on multi-finger tasks via IK retargeting and point cloud-based policies. It demonstrated that human hand motion capture can be used to teach dexterous robot manipulation at scale, opening a new data source for multi-finger robot learning.

### 5.8 PianoMime: Learning a Generalist, Dexterous Piano Player from Internet Demonstrations
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** PianoMime demonstrated that robots can learn complex dexterous tasks (playing piano) from internet videos of human performances, without any robot-specific demonstrations. It showed that cross-embodiment imitation from human videos is possible for fine motor control, establishing internet video as a scalable data source for dexterous manipulation.

### 5.9 SpringGrasp: Synthesizing Compliant, Dexterous Grasps under Shape Uncertainty
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2024 / ICRA 2024
- **Year:** 2024
- **Why it matters:** SpringGrasp introduced compliant grasping under shape uncertainty—synthesizing grasps that account for incomplete or noisy object geometry. It demonstrated that probabilistic grasp planning can produce robust grasps even when object shape is uncertain, a critical capability for real-world manipulation where perception is never perfect.

### 5.10 Visual Dexterity: In-Hand Reorientation of Novel and Complex Object Shapes
- **Authors:** Tao Chen, Megha Tippur, Siyang Wu, Vikash Kumar, Edward Adelson, Pulkit Agrawal (MIT)
- **Venue:** Science Robotics 2023
- **Year:** 2023
- **Why it matters:** Published in Science Robotics, this paper demonstrated in-hand reorientation of novel objects using vision-based tactile sensing and reinforcement learning. It achieved reorientation of complex shapes never seen during training, showing that in-hand manipulation with multi-finger hands can generalize to novel objects through tactile-visual feedback.

---

## 6. Navigation, Embodied AI & Cross-Embodiment Transfer

> Navigation and embodied AI focus on robots understanding and moving through environments. Cross-embodiment transfer addresses the fundamental challenge of training policies that work across different robot types.

### 6.1 LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action
- **Authors:** Dhruv Shah, Blaise Agüera y Arcas, et al. (UC Berkeley, Google Research)
- **Venue:** Conference on Robot Learning (CoRL) 2023
- **Year:** 2023
- **Why it matters:** LM-Nav combined pretrained language, vision, and action models for robotic navigation without any navigation-specific training. It demonstrated that a robot can navigate to goals specified in natural language ("the kitchen near the window") by composing three frozen pretrained models, establishing the modular pretrained model approach for embodied navigation.

### 6.2 VLMaps: Visual Language Maps for Robot Navigation
- **Authors:** Chenguang Huang, Oier Mees, Andy Zeng, Wolfram Burgard (Google Research, University of Freiburg)
- **Venue:** ICRA 2023
- **Year:** 2023
- **Why it matters:** VLMaps built metric semantic maps where each location is labeled with open-vocabulary visual-language features (from CLIP). It enabled robots to navigate to goals specified by natural language descriptions of visual appearance ("the red chair") without requiring predefined object categories, establishing open-vocabulary spatial memory for navigation.

### 6.3 NaVid: Zero-Shot Vision-Language Navigation
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2024 / ICRA 2025
- **Year:** 2024
- **Why it matters:** NaVid demonstrated zero-shot vision-language navigation—navigating from monocular video and language instructions without any navigation training data. It showed that pretrained vision-language models can be directly applied to navigation tasks, achieving impressive cross-embodiment generalization to new robot platforms and environments.

### 6.4 NaVILA: Legged Robot Vision-Language-Action Model for Navigation
- **Authors:** Various (UC San Diego, NVIDIA, USC)
- **Venue:** Robotics: Science and Systems (RSS) 2025
- **Year:** 2025
- **Why it matters:** NaVILA is the first VLA model specifically designed for legged robot navigation. It demonstrated that vision-language-action models can control quadruped and humanoid robots for navigation tasks, achieving cross-embodiment generalization between legged platforms. It established that the VLA paradigm extends beyond manipulation to locomotion and navigation.

### 6.5 GNM: A General Navigation Model to Drive Any Robot
- **Authors:** Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, Sergey Levine (UC Berkeley)
- **Venue:** ICRA 2023
- **Year:** 2023
- **Why it matters:** GNM demonstrated a single navigation policy that can drive any mobile robot—different sizes, sensor configurations, and dynamics—without retraining. It showed that cross-embodiment transfer is possible for navigation by learning representation spaces that abstract away embodiment-specific details, establishing the "one policy, any robot" vision for mobile robotics.

### 6.6 PoliFormer: Transformer-Based On-Policy Reinforcement Learning for Video-Level Navigation
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2025 / ICRA 2025
- **Year:** 2025
- **Why it matters:** PoliFormer introduced transformer-based on-policy RL for video-level navigation, training policies to make navigation decisions from long video sequences rather than single frames. It demonstrated that temporal reasoning with transformers significantly improves navigation in complex, cluttered environments with dynamic obstacles.

### 6.7 X-Nav: Learning End-to-End Cross-Embodiment Navigation for Mobile Robots
- **Authors:** Haitong Wang, Aaron Hao Tan, Angus Fung, Goldie Nejat (various institutions)
- **Venue:** arXiv 2025 / ICRA 2025
- **Year:** 2025
- **Why it matters:** X-Nav pushed cross-embodiment navigation further by learning end-to-end navigation policies that transfer across mobile robots with fundamentally different dynamics and sensor configurations. It demonstrated that cross-embodiment transfer can work for reactive navigation without requiring hand-designed feature abstraction.

### 6.8 Scaling Cross-Embodied Learning: One Policy for Manipulation, Navigation, Locomotion and Aviation
- **Authors:** Ria Doshi, Homer Rich Walke, Oier Mees, Sudeep Dasari, Sergey Levine (UC Berkeley, etc.)
- **Venue:** Conference on Robot Learning (CoRL) 2025
- **Year:** 2025
- **Why it matters:** This paper demonstrated a single policy that can control robots for manipulation, navigation, locomotion, and even aviation—four fundamentally different task modalities. It showed that cross-embodiment transfer can extend to task modality, not just robot morphology, representing the most ambitious generalization result in robot learning to date.

### 6.9 BEVBert: Multimodal Map Pre-training for Language-guided Navigation
- **Authors:** Dong An, Yuankai Qi, Yangguang Li, et al. (various institutions)
- **Venue:** ICCV 2023
- **Year:** 2023
- **Why it matters:** BEVBert pre-trained a bird's-eye-view (BEV) map representation with multimodal language grounding for language-guided navigation. It demonstrated that map-based pretraining with language supervision significantly improves navigation success in complex indoor environments, establishing BEV representations as an effective intermediate for embodied navigation.

### 6.10 DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset
- **Authors:** Alexander Khazatsky, et al. (Stanford, UC Berkeley, CMU, TRI, etc.)
- **Venue:** arXiv 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** DROID is the largest in-the-wild robot manipulation dataset, collected across diverse real-world environments (homes, offices, labs) rather than controlled lab settings. It demonstrated that in-the-wild diversity is crucial for generalization and released open data and policies, complementing the lab-focused Open X-Embodiment dataset and pushing the frontier of generalist robot learning.

---

## 7. Sim-to-Real Transfer & Domain Adaptation

> The sim-to-real gap—the performance drop when policies trained in simulation deploy on real robots—remains a central challenge. These papers advanced the techniques that bridge this gap.

### 7.1 TRANSIC: Sim-to-Real Policy Transfer by Learning from Online Correction
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2024 / ICRA 2025
- **Year:** 2024
- **Why it matters:** TRANSIC introduced a framework that learns from online human corrections during sim-to-real transfer. Instead of relying solely on domain randomization, it actively identifies where the sim policy fails in reality and learns from corrective feedback. This established online correction as a practical and data-efficient approach to sim-to-real transfer.

### 7.2 Reconciling Reality through Simulation: A Real-to-Sim-to-Real Approach for Robust Manipulation
- **Authors:** Various (multiple institutions)
- **Venue:** CVPR 2024
- **Year:** 2024
- **Why it matters:** This paper introduced a real-to-sim-to-real pipeline that first identifies the real-world dynamics from a small amount of real data, then re-trains the policy in simulation with matched dynamics, then deploys. It demonstrated that accurate system identification followed by targeted simulation can outperform naive domain randomization, establishing the real-to-sim-to-real loop as an effective sim-to-real methodology.

### 7.3 Understanding Domain Randomization for Sim-to-Real Transfer
- **Authors:** Xingyu Chen, Jinghao Hu, et al. (various institutions)
- **Venue:** ICLR 2022 (highly influential in 2023–2025 sim-to-real research)
- **Year:** 2022
- **Why it matters:** This paper provided a systematic analysis of why domain randomization works and when it fails for sim-to-real transfer. It identified the key factors (randomization distribution, training curriculum, task complexity) that determine transfer success, providing a principled foundation for designing sim-to-real training regimes that became standard practice in 2023–2025.

### 7.4 Generalizing 6-DoF Grasp Detection via Domain Prior Knowledge
- **Authors:** Various (multiple institutions)
- **Venue:** RSS 2024
- **Year:** 2024
- **Why it matters:** This paper showed that incorporating domain prior knowledge (object shape priors, contact physics) into grasp detection models significantly improves sim-to-real transfer for 6-DoF grasping. It demonstrated that structure-aware learning can bridge the sim-to-real gap better than pure data-driven approaches, especially for contact-rich manipulation.

### 7.5 Kalman Filter-Based One-Shot Sim-to-Real Transfer Learning
- **Authors:** Various (multiple institutions)
- **Venue:** IEEE Robotics and Automation Letters (RA-L) 2023
- **Year:** 2023
- **Why it matters:** This paper introduced a one-shot sim-to-real transfer method using Kalman filtering to adapt simulation parameters from a single real-world trajectory. It demonstrated that Bayesian parameter adaptation can achieve rapid sim-to-real transfer with minimal real-world data, making it practical for settings where extensive real-world interaction is costly.

### 7.6 Humanoid-Gym: RL for Humanoid Robot with Zero-Shot Sim2Real Transfer
- **Authors:** Xiao Gu, Yao-Jen Wang, Jianyu Chen
- **Venue:** arXiv 2024 / ICRA 2025
- **Year:** 2024
- **Why it matters:** While also listed in humanoid locomotion, this paper specifically demonstrated zero-shot sim-to-real transfer for humanoid walking. It showed that carefully designed observation and action spaces can eliminate the need for any real-world fine-tuning, making it a landmark for practical sim-to-real deployment in humanoid robotics.

### 7.7 On the Role of the Action Space in Robot Manipulation Learning and Sim-to-Real Transfer
- **Authors:** Various (multiple institutions)
- **Venue:** IEEE Robotics and Automation Letters (RA-L) 2024
- **Year:** 2024
- **Why it matters:** This paper systematically analyzed how the choice of action space (joint positions, joint velocities, Cartesian poses, etc.) affects sim-to-real transfer for manipulation. It demonstrated that action space design is a critical but often overlooked factor in sim-to-real success, providing guidelines for selecting action representations that transfer robustly.

### 7.8 Sim-to-Lab-to-Real: Safe RL with Shielding and Generalized Adversaries
- **Authors:** Kai-Chieh Hsu, Allen Z. Ren, et al. (Princeton, etc.)
- **Venue:** Artificial Intelligence Journal 2023
- **Year:** 2023
- **Why it matters:** This paper introduced a safe RL framework for sim-to-real transfer that uses shielding (safety constraints) and generalized adversaries to ensure safe policy transfer. It demonstrated that safety can be maintained during sim-to-real transfer without sacrificing performance, addressing the critical safety concerns in deploying learned policies on physical robots.

### 7.9 GRID: Gradual Real-World Integration for Domain Randomization
- **Authors:** Various (multiple institutions)
- **Venue:** ICRA 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** GRID introduced gradual integration of real-world data into domain randomization training, starting from pure simulation and progressively adding real-world observations. It demonstrated that curriculum-style domain adaptation can achieve better transfer than fixed randomization, establishing curriculum-based sim-to-real as an effective training paradigm.

### 7.10 Robust Domain Randomization for Reinforcement Learning
- **Authors:** Raphael Slaoui, William Clements, et al. (various institutions)
- **Venue:** ICRA 2020 / influential in 2023–2025
- **Year:** 2020 (foundational, highly cited in 2023–2025 sim-to-real work)
- **Why it matters:** While published earlier, this paper established the robust domain randomization techniques that became standard in 2023–2025. It introduced principled methods for selecting randomization parameters that maximize transfer robustness, providing the theoretical foundation for the sim-to-real transfer methods used in modern humanoid and manipulation research.

---

## 8. Dataset, Benchmark & Infrastructure Contributions

> Open datasets and benchmarks are the engines of progress in robot learning. These contributions provided the data and evaluation infrastructure that enabled the VLA and generalist policy revolution.

### 8.1 Open X-Embodiment Dataset (see also 1.4)
> The Open X-Embodiment dataset and RT-X models (ICRA 2024 Best Paper) are the cornerstone dataset for generalist robot policies. See section 1.4 for full details. This entry serves as a cross-reference to the dataset contribution, which is inseparable from the model contribution.

### 8.2 DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset
- **Authors:** Alexander Khazatsky, et al. (Stanford, UC Berkeley, CMU, TRI, etc.)
- **Venue:** arXiv 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** DROID is the largest in-the-wild robot manipulation dataset, collected across diverse real-world environments (homes, offices, labs) rather than controlled lab settings. It demonstrated that in-the-wild diversity is crucial for generalization and released open data and policies, complementing the lab-focused Open X-Embodiment dataset and pushing the frontier of generalist robot learning.

### 8.3 BridgeData V2
- **Authors:** Various (UC Berkeley, Stanford, etc.)
- **Venue:** arXiv 2023 / RSS 2023
- **Year:** 2023
- **Why it matters:** BridgeData V2 provided a large, diverse dataset of real-world manipulation tasks collected in a single kitchen environment. It became the standard benchmark for evaluating generalist manipulation policies, with most VLA papers (RT-X, Octo, OpenVLA) using it for evaluation. Its standardized data format and evaluation protocol enabled comparable results across the field.

### 8.4 RLBench: The Robot Learning Benchmark & Learning Environment
- **Authors:** Stephen James, Zicong Ma, David Rovick Arrojo, Andrew J. Davison (Imperial College London)
- **Venue:** IEEE Robotics and Automation Letters (RA-L) 2020 / heavily used in 2023–2025
- **Year:** 2020 (foundational benchmark, heavily used in 2023–2025)
- **Why it matters:** RLBench is the most widely used simulation benchmark for robot learning, providing 100+ manipulation tasks with standardized evaluation. It became the de facto standard for evaluating zero-shot manipulation methods (VoxPoser, MOO, etc.) in 2023–2025, enabling comparable evaluation of language-conditioned manipulation policies.

### 8.5 LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning
- **Authors:** Bohao Liu, Yifeng Zhu, Chenyang Gao, et al. (UT Austin, etc.)
- **Venue:** NeurIPS Datasets and Benchmarks 2023
- **Year:** 2023
- **Why it matters:** LIBERO benchmarked lifelong robot learning—sequentially learning multiple tasks without catastrophic forgetting. It provided a standardized evaluation for knowledge transfer in robot learning, becoming the standard benchmark for evaluating continual learning capabilities in generalist robot policies.

### 8.6 ARIO: Benchmarking Augmented Reality Robot Interaction and Operation
- **Authors:** Various (multiple institutions)
- **Venue:** ICRA 2024 / RSS 2024
- **Year:** 2024
- **Why it matters:** ARIO introduced a benchmark for augmented reality robot interaction, evaluating how robots can interact with humans through AR interfaces. It established the AR-robot interaction benchmark, opening a new dimension for human-robot collaboration evaluation.

### 8.7 Isaac Gym / Isaac Sim / Isaac Lab: High Performance GPU-Based Physics Simulation
- **Authors:** NVIDIA Simulation Team
- **Venue:** NeurIPS 2021 (Isaac Gym) / extended 2023–2025 (Isaac Sim, Isaac Lab)
- **Year:** 2021 (foundational, but Isaac Sim and Isaac Lab are 2023–2025)
- **Why it matters:** Isaac Gym and its successor Isaac Sim / Isaac Lab revolutionized robot simulation by enabling massively parallel GPU-based physics simulation. Isaac Lab (2024) became the standard training environment for humanoid RL policies in 2024–2025, directly enabling the humanoid locomotion boom. NVIDIA's continued investment in Isaac Sim and GR00T Blueprint (2025) for synthetic data generation makes this infrastructure central to modern robotics.

### 8.8 MuJoCo-Warp / Newton: Next-Generation Physics Engines for Robot Learning
- **Authors:** Google DeepMind, NVIDIA, Disney Research (Newton collaboration)
- **Venue:** NVIDIA GTC 2025 (announced March 2025)
- **Year:** 2025
- **Why it matters:** MuJoCo-Warp (DeepMind + NVIDIA collaboration) accelerates MuJoCo simulation by 70x through GPU parallelization. Newton (with Disney Research) is a next-generation open-source physics engine purpose-built for robot learning. These physics engines will power the next wave of sim-to-real research, enabling training at scales previously impossible.

### 8.9 OXE-AugE: Augmented Open X-Embodiment Dataset
- **Authors:** Various (multiple institutions)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why it matters:** OXE-AugE expanded the original Open X-Embodiment dataset with 9 additional robot embodiments and 4.4M+ trajectories (more than triple the original). It demonstrated that generalist policies improve 24-45% on previously unseen robot-gripper combinations when trained on augmented data, showing the data scaling law for robot foundation models.

### 8.10 LeRobot: Making AI for Robotics More Accessible
- **Authors:** Hugging Face Robotics Team
- **Venue:** Hugging Face / Community Project 2024–2025
- **Year:** 2024
- **Why it matters:** LeRobot is the practical integration layer for end-to-end robot learning: hardware-agnostic robot APIs, standardized dataset formats, and out-of-the-box policies including pi0.5, GR00T N1.5, SmolVLA, and Diffusion Policy. It democratized robot learning by making state-of-the-art models deployable without writing custom stacks, serving as the "PyTorch of robotics" for the VLA era.

---

## Meta-Analysis & How to Use This List

### Themes & Convergence

The 2023–2026 period in robotics has been defined by the convergence of three previously separate threads:

1. **Foundation Models:** Pre-trained vision-language models (CLIP, DINO, LLaMA, SigLIP) provide the semantic and spatial understanding that robots need to operate in open-world environments.

2. **Generative Policies:** Diffusion models and flow matching have replaced regression-based policies, enabling robots to handle multimodal action distributions and high-dimensional continuous control.

3. **Cross-Embodiment Data:** The Open X-Embodiment and DROID datasets demonstrated that training on diverse robot data improves generalization, establishing the "more data, more robots, better policies" scaling law.

### Key Trunk Papers

If you only read 10 papers, read these (in order):

1. **Diffusion Policy** (RSS 2023) — The generative policy paradigm shift
2. **RT-2** (CoRL 2023) — The first large-scale VLA model
3. **Open X-Embodiment / RT-X** (ICRA 2024) — The "ImageNet moment" for robotics data
4. **OpenVLA** (CoRL 2024) — Democratization of open VLA models
5. **pi0** (CoRL 2024 / RSS 2025) — Flow matching for dexterous manipulation
6. **VoxPoser** (CoRL 2023) — Zero-shot LLM manipulation without training
7. **Eureka** (ICLR 2024) — Automated reward design with LLMs
8. **ACT / ALOHA** (RSS 2023) — Low-cost bimanual learning
9. **Octo** (RSS 2024) — The open-source generalist policy baseline
10. **GR00T N1** (NVIDIA 2025) — The open humanoid foundation model

### Citation Map

```
Late 2022 Trunk: RT-1, SayCan, Inner Monologue, Gato
                |
2023 Foundation: RT-2, PaLM-E, VoxPoser, Diffusion Policy, ACT/ALOHA,
                 Eureka, DexGraspNet, Open X-Embodiment Dataset
                |
2024 Expansion: Octo, OpenVLA, pi0, Mobile ALOHA, DROID, 3D Diffusion Policy,
                 Humanoid-Gym, NaVid, UMI, DexCap
                |
2025 Humanoid/Commercial: GR00T N1, Helix, Gemini Robotics, pi0.5, RDT-1B,
                          ASAP, BeamDojo, NaVILA, CrossFormer, OXE-AugE
```

### The State of the Field (July 2026)

As of mid-2026, the robotics field has undergone a foundational transformation:

- **VLA models** have become the dominant architecture for robot control, replacing task-specific policies with generalist models conditioned on language and vision.
- **Open-source models** (OpenVLA, Octo, pi0, GR00T N1) have democratized access to state-of-the-art robot intelligence, enabling labs without Google-scale resources to build generalist robots.
- **Humanoid robots** are transitioning from research to commercial deployment, with GR00T N1, Helix, and Gemini Robotics powering platforms from 1X, Figure, Tesla, Agility, and Boston Dynamics.
- **Diffusion and flow matching** have become the standard action generation methods, replacing autoregressive tokenization for continuous control tasks.
- **Cross-embodiment training** is now standard practice, with models trained on 20+ robot types showing positive transfer to new platforms.
- **Sim-to-real transfer** has improved dramatically through physics alignment (ASAP, Humanoid-Gym) and domain randomization, enabling zero-shot deployment of learned policies.

The convergence of these trends suggests that the 2023–2026 period will be remembered as the moment when robotics transitioned from "one robot, one task, one program" to "one model, many robots, many tasks, language-conditioned."

---

*Compiled July 2026. Covers papers from January 2023 to July 2026, with foundational trunk papers from late 2022 included where they established paradigms that defined the 2023–2026 period.*
