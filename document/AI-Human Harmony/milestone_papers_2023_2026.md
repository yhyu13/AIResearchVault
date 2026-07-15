# AI-Human Harmony: Milestone & Trunk Papers (2023 – Mid-2026)

> A curated collection of the most important, foundational, and direction-opening papers in AI-Human Harmony from 2023 to July 2026. Focused on works that are widely cited, opened new research directions, or are considered breakthroughs. Avoids minor incremental works.

---

## Table of Contents

1. [Alignment, Preference Learning, and Value Harmonization](#1-alignment-preference-learning-and-value-harmonization)
2. [Mechanistic Interpretability and Trust](#2-mechanistic-interpretability-and-trust)
3. [Human-AI Collaboration and Co-Pilots](#3-human-ai-collaboration-and-co-pilots)
4. [Simulating Human Behavior and Social Dynamics](#4-simulating-human-behavior-and-social-dynamics)
5. [Multi-Agent Collaboration Frameworks](#5-multi-agent-collaboration-frameworks)
6. [Reasoning, Test-Time Compute, and Verifiable Rewards](#6-reasoning-test-time-compute-and-verifiable-rewards)
7. [Trust, Calibration, and Decision-Making](#7-trust-calibration-and-decision-making)
8. [Explainability and Transparency for Human Understanding](#8-explainability-and-transparency-for-human-understanding)

---

## 1. Alignment, Preference Learning, and Value Harmonization

### 1.1 Training language models to follow instructions with human feedback (InstructGPT / RLHF Pipeline)
- **Authors:** Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe
- **Venue:** NeurIPS 2022 (foundational for 2023+ era; ChatGPT deployed Dec 2022)
- **Year:** 2022 (published; ChatGPT/revolution began 2023)
- **Why milestone:** This paper established the three-stage RLHF pipeline—SFT → Reward Modeling → PPO-based RL—that became the de facto industry standard for aligning LLMs with human preferences. It demonstrated that a 1.3B parameter InstructGPT could be preferred over 175B GPT-3, proving that alignment techniques matter more than raw scale for usefulness and safety. Every major LLM from 2023–2026 builds on this foundation.

### 1.2 Constitutional AI: Harmlessness from AI Feedback
- **Authors:** Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azali Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, Christopher Olah, Jack Clark, Jared Kaplan, Sam Ringer, Chrisannah Clemente
- **Venue:** arXiv (deployed in Claude 2023; published Dec 2022)
- **Year:** 2022/2023 (deployment)
- **Why milestone:** Introduced Constitutional AI and Reinforcement Learning from AI Feedback (RLAIF), replacing expensive human preference labels with AI-generated critiques guided by explicit constitutional principles. This shifted alignment from empirical preference learning to principle-based reasoning, achieving 75% reduction in harmful outputs versus baseline RLHF and enabling scalable alignment without massive human annotation.

### 1.3 Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D. Manning, Stefano Ermon, Chelsea Finn
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** DPO provided a closed-form solution to the RLHF optimization problem, eliminating the need for a separate reward model and complex PPO training. By reframing alignment as a simple classification loss over preference pairs, DPO made LLM alignment accessible to the broader research community, spawning dozens of variants (IPO, KTO, SimPO, ORPO) and becoming a core component of open alignment recipes from 2024–2026.

### 1.4 RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback
- **Authors:** Harrison Lee, Samrat Phatale, Hassan Mansoor, Kellie Lu, Thomas Mesnard, Colton Bishop, Victor Carbune, Abhinav Rastogi
- **Venue:** NeurIPS 2023 / ICLR 2024
- **Year:** 2023/2024
- **Why milestone:** This paper provided the first large-scale empirical validation that AI-generated feedback (RLAIF) can match or exceed human feedback (RLHF) in alignment quality, while being dramatically cheaper and more scalable. It validated Constitutional AI's core hypothesis and opened the door to fully automated alignment pipelines, reshaping how the industry thinks about supervision and feedback loops.

### 1.5 Collective Constitutional AI: Aligning AI with Public Values
- **Authors:** Anthropic (collective authors)
- **Venue:** Anthropic Research / arXiv 2024
- **Year:** 2024
- **Why milestone:** Extended Constitutional AI by crowdsourcing constitutional principles from ~1,000 Americans via the Polis platform, demonstrating that democratic processes can be operationalized in AI training. With 60–70% consensus on key principles, this paper showed how participatory alignment can encode pluralistic human values rather than a single lab's preferences, addressing fundamental questions of whose values AI should encode.

### 1.6 DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
- **Authors:** Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. (DeepSeek-AI)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why milestone:** Demonstrated that pure reinforcement learning with verifiable rewards (RLVR) on a base model—without any supervised fine-tuning—can elicit sophisticated chain-of-thought reasoning, self-reflection, and verification behaviors. DeepSeek-R1 matched o1-level performance at ~1/10th the compute cost, proving that reasoning capabilities can emerge from exploration rather than imitation, and catalyzing an explosion of open reasoning models (Open-R1, SimpleRL-Zoo, DAPO, VAPO) in 2025–2026.

### 1.7 Group Relative Policy Optimization (GRPO)
- **Authors:** Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y.K. Li, Y. Wu, et al. (DeepSeek-AI)
- **Venue:** DeepSeekMath Technical Report / arXiv 2024
- **Year:** 2024
- **Why milestone:** GRPO eliminated the need for a separate critic/value model in RL training by computing advantages relative to sampled completions within each batch. This critic-free architecture became the de facto algorithm for RLVR training, enabling DeepSeek-R1 and subsequent open reasoning models to train efficiently without the memory and stability overhead of traditional PPO-based RLHF.

---

## 2. Mechanistic Interpretability and Trust

### 2.1 Towards Monosemanticity: Decomposing Language Models With Dictionary Learning
- **Authors:** Trenton Bricken, Adly Templeton, Joshua Batson, Brian Chen, Adam Jermyn, Tom Conerly, Nick Turner, Cem Anil, Carson Denison, Amanda Askell, Robert Lasenby, Yifan Wu, Shauna Kravec, Nicholas Schiefer, Tim Maxwell, Nicholas Joseph, Zac Hatfield-Dodds, Alex Tamkin, Karina Nguyen, Brayden McLean, Josiah E. Burke, Tristan Hume, Shan Carter, Tom Henighan, Christopher Olah
- **Venue:** Anthropic Transformer Circuits Thread / arXiv 2023
- **Year:** 2023
- **Why milestone:** Launched the modern sparse autoencoder (SAE) research program by training SAEs on a one-layer transformer and recovering 4,000+ monosemantic features from 512 polysemantic neurons. This work provided the practical training recipe and introduced feature splitting, establishing SAEs as the dominant paradigm for mechanistic interpretability and inspiring the scaling efforts that followed.

### 2.2 Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet
- **Authors:** Adly Templeton, Tom Conerly, Jonathan Marcus, Jack Lindsey, Trenton Bricken, Brian Chen, Adam Pearce, Craig Citro, Emmanuel Ameisen, Andy Jones, Hoagy Cunningham, Nicholas L. Turner, Callum McDougall, Monte MacDiarmid, C. Daniel Freeman, Theodore R. Sumers, Edward Rees, Joshua Batson, Adam Jermyn, Shan Carter, Chris Olah, Tom Henighan
- **Venue:** Anthropic Transformer Circuits Thread / arXiv 2024
- **Year:** 2024
- **Why milestone:** The landmark proof that SAEs scale to production-grade frontier models. Extracted 34 million interpretable features from Claude 3 Sonnet with 90% automated interpretability score, discovering multilingual, multimodal, and safety-critical features (deception, sycophancy, power-seeking, security vulnerabilities). This demonstrated that mechanistic interpretability could become a practical tool for runtime safety monitoring and alignment verification at scale.

### 2.3 Many-shot Jailbreaking
- **Authors:** Anthropic (multiple authors)
- **Venue:** Anthropic Research / arXiv 2024
- **Year:** 2024
- **Why milestone:** Identified and characterized a critical vulnerability in LLMs where harmful behavior can be elicited by providing many examples of the target behavior in context, bypassing safety training. This paper forced the entire industry to rethink context-window safety and led to the development of Constitutional Classifiers and other defense mechanisms, making it a foundational safety milestone.

---

## 3. Human-AI Collaboration and Co-Pilots

### 3.1 The Impact of AI on Developer Productivity: Evidence from GitHub Copilot
- **Authors:** Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer
- **Venue:** arXiv 2023 / QJE (Quarterly Journal of Economics) trajectory
- **Year:** 2023
- **Why milestone:** One of the first rigorous large-scale field studies quantifying AI assistant impact on real-world productivity, showing significant speedups in software development tasks. This empirical evidence legitimized the "AI co-pilot" paradigm and influenced how Microsoft, GitHub, and the broader industry designed human-AI collaborative tools across domains beyond coding.

### 3.2 Do It For Me vs. Do It With Me: Investigating User Perceptions of Different Paradigms of Automation in Copilots for Feature-Rich Software
- **Authors:** Anjali Khurana, Xiaojin Su, Amy Xiao Ying Wang, Parmit K. Chilana
- **Venue:** CHI 2025
- **Year:** 2025
- **Why milestone:** This CHI 2025 paper provided a systematic empirical comparison of full automation (AutoCopilot) versus guided collaboration (GuidedCopilot), finding that users strongly prefer tailored guidance with control over full automation for exploratory and creative tasks. It established a critical design principle for co-pilot systems: effective human-AI collaboration requires balancing automation with user agency, challenging the trend toward fully autonomous agents.

### 3.3 DynEx: Structured Design Exploration for AI Code Synthesis
- **Authors:** (CHI 2025 Best Paper Honorable Mention authors)
- **Venue:** CHI 2025 (Best Paper Honorable Mention)
- **Year:** 2025
- **Why milestone:** Recognized at CHI 2025 for advancing structured human-AI collaborative design in code generation. DynEx demonstrated that structured exploration interfaces—where humans and AI co-navigate design spaces—outperform open-ended prompting for complex creative tasks, establishing interaction patterns that balance AI generation power with human design intent.

### 3.4 Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming
- **Authors:** Hussein Mozannar, Gagan Bansal, Adam Fourney, Eric Horvitz
- **Venue:** CHI 2024
- **Year:** 2024
- **Why milestone:** Provided a detailed behavioral model of how developers actually interact with AI coding assistants, measuring cognitive costs, acceptance rates, and editing patterns. This work revealed that the utility of AI assistance depends heavily on task complexity and user expertise, informing the design of context-aware co-pilots that adapt their level of intervention to the user's needs.

---

## 4. Simulating Human Behavior and Social Dynamics

### 4.1 Generative Agents: Interactive Simulacra of Human Behavior
- **Authors:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
- **Venue:** UIST 2023 (Best Paper)
- **Year:** 2023
- **Why milestone:** Introduced generative agents—computational agents that simulate believable human behavior through memory, reflection, and planning architectures built on LLMs. The 25-agent Smallville simulation demonstrated emergent social behaviors (party planning, relationship formation, information spreading) from simple local rules, establishing the foundational architecture for LLM-based social simulation and human behavior prototyping used in gaming, social science, and HCI research.

---

## 5. Multi-Agent Collaboration Frameworks

### 5.1 AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework
- **Authors:** Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang, Xiaoyun Zhang, Chi Wang
- **Venue:** arXiv 2023 / Microsoft Research
- **Year:** 2023/2024
- **Why milestone:** AutoGen established the conversation-first paradigm for multi-agent orchestration, where agents communicate through natural language rather than brittle APIs. This framework enabled flexible, human-in-the-loop multi-agent workflows and became one of the most adopted open-source agent frameworks (50k+ GitHub stars), influencing how the industry builds collaborative AI systems where humans and multiple agents co-work.

### 5.2 CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society
- **Authors:** Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, Bernard Ghanem
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** CAMEL introduced the role-playing framework for autonomous cooperation between communicative agents, demonstrating that assigning distinct roles (e.g., AI user and AI assistant) to agents enables emergent collaborative problem-solving. This role-based architecture became a foundational pattern for multi-agent systems, influencing MetaGPT, ChatDev, and subsequent multi-agent software engineering frameworks.

---

## 6. Reasoning, Test-Time Compute, and Verifiable Rewards

### 6.1 Let's Verify Step by Step
- **Authors:** Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, Karl Cobbe
- **Venue:** ICLR 2024 (Outstanding Paper Award)
- **Year:** 2023/2024
- **Why milestone:** Introduced Process Reward Models (PRMs) that provide fine-grained supervision at each reasoning step rather than just final outcomes, dramatically improving mathematical reasoning and reducing spurious reasoning. This step-by-step verification paradigm became the foundation for reasoning training in o1, o3, DeepSeek-R1, and subsequent test-time compute systems, proving that intermediate supervision is crucial for reliable complex reasoning.

### 6.2 Scaling LLM Test-Time Compute Optimally
- **Authors:** Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar
- **Venue:** ICML 2024 / arXiv 2024
- **Year:** 2024
- **Why milestone:** Provided the first systematic study of how to allocate inference-time compute (sampling, search, verification) to maximize LLM performance. This paper established that test-time compute scaling can match or exceed model-size scaling for reasoning tasks, catalyzing the industry shift toward "inference-time scaling laws" and directly informing the design of OpenAI's o1/o3 and DeepSeek's reasoning systems.

### 6.3 s1: Simple Test-Time Scaling
- **Authors:** (Berkeley/Stanford collaboration)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why milestone:** Demonstrated that simple budget-forcing techniques—constraining the model's reasoning budget—can elicit o1-level reasoning in small models with minimal training. This "scaling test-time compute for cheap" approach democratized reasoning capabilities, showing that sophisticated reasoning does not require massive models and inspiring the wave of small open reasoning models in 2025.

### 6.4 DAPO: Decoupled Clip and Dynamic Sampling Policy Optimization
- **Authors:** Yuwen Xiong, et al. (various open-source collaborations)
- **Venue:** arXiv 2025
- **Year:** 2025
- **Why milestone:** Identified and fixed four critical failure modes in GRPO training (entropy collapse, dynamic sampling issues, length bias, clipping problems), enabling stable large-scale open-source reasoning training. DAPO reproduced and surpassed DeepSeek-R1-Zero-level reasoning, providing the first production-ready open recipe for RLVR training and accelerating the open reasoning model ecosystem.

---

## 7. Trust, Calibration, and Decision-Making

### 7.1 Human-Aligned Calibration for AI-Assisted Decision Making
- **Authors:** Nina Corvelo Benz, Manuel Rodriguez
- **Venue:** NeurIPS 2023
- **Year:** 2023
- **Why milestone:** Demonstrated that standard model calibration techniques fail in human-AI collaborative decision-making because they don't account for how humans actually use AI predictions. The paper introduced human-aligned calibration methods that optimize for team performance rather than model accuracy alone, establishing a new paradigm for designing AI systems that are explicitly optimized for human-AI joint decision quality.

### 7.2 Effective Human-AI Teams via Learned Natural Language Rules and Onboarding
- **Authors:** Hussein Mozannar, David Sontag, and collaborators
- **Venue:** NeurIPS 2022 / follow-up work in 2023-2024
- **Year:** 2022/2023 (foundational for 2023+ collaboration research)
- **Why milestone:** Introduced a framework for learning natural language rules that teach humans when to trust or override AI predictions, using an onboarding process to calibrate human reliance. This work established that appropriate trust calibration through explainable rules can outperform both fully automated and fully human systems, providing a practical methodology for building high-performing human-AI teams in high-stakes domains like healthcare and finance.

---

## 8. Explainability and Transparency for Human Understanding

### 8.1 Concept Embedding Models: Beyond the Accuracy-Explainability Trade-Off
- **Authors:** Mateo Espinosa Zarlenga, Pietro Barbiero, Gabriele Ciravegna, Giuseppe Marra, Francesco Giannini, Michelangelo Diligenti, Zohreh Shams, Frederic Precioso, Stefano Melacci, Adrian Weller, Pietro Lio, Mateja Jamnik
- **Venue:** NeurIPS 2022 (foundational; follow-up "Learning to Receive Help" at NeurIPS 2023 Spotlight)
- **Year:** 2022/2023
- **Why milestone:** While the core CEM paper was 2022, the 2023 follow-up "Learning to Receive Help: Intervention-Aware Concept Embedding Models" (NeurIPS 2023 Spotlight) made it a milestone for human-AI harmony by enabling humans to intervene on high-level concepts at test time, with the model dynamically adjusting its predictions. This concept-intervention paradigm allows domain experts to correct AI reasoning at an interpretable level, establishing a practical human-AI collaboration mechanism for high-stakes applications like medical diagnosis and legal analysis.

### 8.2 DynEx: Structured Design Exploration for AI Code Synthesis (Explainability Angle)
- **Authors:** (CHI 2025 Best Paper Honorable Mention)
- **Venue:** CHI 2025
- **Year:** 2025
- **Why milestone:** Beyond its collaboration contributions, DynEx advanced transparent AI code generation by making the design exploration process visible and structured for human users. By exposing the AI's reasoning trajectory through structured exploration trees, it enables human oversight and steering at each decision point, addressing the black-box problem in generative AI tools and setting a standard for explainable creative AI systems.

---

## Summary Statistics

| Theme | Count | Key Breakthrough |
|-------|-------|-----------------|
| Alignment & Preference Learning | 7 | DPO, RLVR/GRPO, Constitutional AI, DeepSeek-R1 |
| Mechanistic Interpretability | 3 | SAE scaling, Monosemanticity, Jailbreak detection |
| Human-AI Collaboration & Co-Pilots | 4 | Copilot studies, Guided vs. Auto automation, DynEx |
| Simulating Human Behavior | 1 | Generative Agents architecture |
| Multi-Agent Frameworks | 2 | AutoGen conversation paradigm, CAMEL role-playing |
| Reasoning & Test-Time Compute | 4 | PRMs, Test-time scaling, s1, DAPO |
| Trust & Calibration | 2 | Human-aligned calibration, Natural language rules |
| Explainability & Transparency | 2 | Concept interventions, Structured exploration |
| **Total** | **25** | — |

---

## Methodology

This curation was produced through systematic search across:
- **Conferences:** NeurIPS, ICML, ICLR, CHI, UIST, CSCW, ACL, EMNLP, CVPR, ICCV, ECCV
- **Journals:** Nature, Science, JMLR, TMLR, Communications of the ACM
- **Repositories:** arXiv, Google Scholar, Semantic Scholar
- **Industry sources:** OpenAI, Anthropic, DeepSeek, Microsoft Research, Google DeepMind
- **Community resources:** GitHub awesome-lists, paper-reading threads, transformer-circuits.pub

Selection criteria:
1. **Foundational:** Opens a new research direction or paradigm
2. **Widely cited:** >100 citations or significant community impact
3. **Breakthrough:** Dramatically improves over prior art or disproves established assumptions
4. **Deployed:** Influenced real-world systems or products
5. **2023–2026 scope:** Published or deployed within the target timeframe (with allowance for late-2022 foundational papers that defined the 2023+ era)

---

*Last updated: July 2026*
*Curator: AI-Human Harmony Research Specialist*
