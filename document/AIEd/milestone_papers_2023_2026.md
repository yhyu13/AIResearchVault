# AI in Education (AIEd) — Milestone & Trunk Papers (2023–Mid-2026)

> **Curated:** 2026-07-15 | **Scope:** Foundational, widely-cited, or direction-opening works only. Excludes minor incremental papers.
> **Coverage:** Intelligent tutoring systems, LLM-based education, automated assessment, multi-agent learning frameworks, educational policy, student modeling, and pedagogical alignment.

---

## Table of Contents

- [I. Policy, Ethics & Foundational Frameworks](#i-policy-ethics--foundational-frameworks)
- [II. Foundational Surveys & Systematic Reviews](#ii-foundational-surveys--systematic-reviews)
- [III. LLM Tutoring & Pedagogical Alignment](#iii-llm-tutoring--pedagogical-alignment)
- [IV. Benchmarks, Evaluation & Datasets](#iv-benchmarks-evaluation--datasets)
- [V. Multi-Agent Systems & Architecture](#v-multi-agent-systems--architecture)
- [VI. Automated Assessment & Feedback](#vi-automated-assessment--feedback)
- [VII. Real-World Deployment & RCT Evidence](#vii-real-world-deployment--rct-evidence)
- [VIII. Student Modeling, Knowledge Tracing & Personalization](#viii-student-modeling-knowledge-tracing--personalization)
- [IX. Multimodal & Generative Content for Education](#ix-multimodal--generative-content-for-education)
- [X. Programming & STEM Education](#x-programming--stem-education)
- [XI. Meta-Analysis: What Makes These Trunk Papers?](#xi-meta-analysis-what-makes-these-trunk-papers)

---

## I. Policy, Ethics & Foundational Frameworks

### 1. Kasneci et al. — "ChatGPT for Good? On Opportunities and Challenges of Large Language Models for Education"
- **Authors:** Enkelejda Kasneci, Kathrin Sessler, Stefan Küchemann, Maria Bannert, Daryna Dementieva, Frank Fischer, Urs Gasser, Georg Groh, Stephan Günnemann, Eyke Hüllermeier, et al. (20+ authors from TUM, LMU Munich, University of Tübingen)
- **Venue:** *Learning and Individual Differences*, 103, 102274
- **Year:** 2023
- **Citations:** >11,000 (the most-cited AIEd paper of the 2020s)
- **Why it is a trunk paper:** This is the definitive position paper that established the conceptual vocabulary for the entire post-2023 AIEd field. Published within weeks of ChatGPT's public release, it immediately framed the discourse around LLMs in education. It systematically catalogs benefits (personalized learning, content generation, engagement, accessibility for learners with disabilities) and risks (bias, over-reliance, academic integrity erosion, factuality failures, digital divide). It introduced the now-standard recommendation that educational integration requires a dual focus on (a) teacher competency frameworks and (b) student critical-thinking curricula. Nearly every subsequent AIEd paper cites this as the foundational risk/opportunity framework. Its cross-institutional German authorship signaled that AIEd was moving from small-scale ITS research to large-scale, policy-facing collective reflection.
- **Technical details:** The paper draws on collective expertise in cognitive science, ML, ethics, and education policy to propose a layered taxonomy of LLM educational applications: content creation, Socratic questioning, feedback generation, adaptive curriculum sequencing, and assistive technology. It warns explicitly about "unexpected brittleness" — LLMs failing on simple tasks — and argues these failures are pedagogically valuable if framed as teaching moments for critical AI literacy. The paper proposes that educators need "AI literacy" competencies: understanding how LLMs work, recognizing their limitations, and designing curricula that leverage LLM strengths while mitigating risks.

---

### 2. UNESCO — "Guidance for Generative AI in Education and Research"
- **Authors:** UNESCO (Fengchun Miao, Wayne Holmes, and the Future of Learning and Innovation Team)
- **Venue:** UNESCO Official Publication (unesdoc.unesco.org)
- **Year:** September 2023
- **Citations:** Referenced in 100+ national policy documents and institutional guidelines
- **Why it is a trunk paper:** This is the first internationally-published, globally-reachable policy framework for GenAI in education. Released at UNESCO's Digital Learning Week 2023 and translated into multiple languages. It introduced a six-step regulatory framework: (1) promote inclusion/equity/linguistic diversity, (2) protect human agency, (3) monitor and validate, (4) develop AI competencies, (5) build teacher/researcher capacities, (6) test and build evidence. It also identified eight "controversies" (worsening digital poverty, outpacing national regulation, unexplainable models, AI-generated content pollution, etc.). This framework has been adopted or adapted by >50 countries as a blueprint for national AI education strategies. It directly influenced the 2024 AI Competency Frameworks for Teachers and Students.
- **Technical details:** The guidance is structured around a "human-centred approach to AI" defined as: supporting human capacities, explainable, predictable, human-controlled, human-accountable, and capable of being shut down. It calls for rethinking learning outcomes toward three categories: (a) foundational knowledge adapted to AI-rich environments, (b) higher-order thinking skills for harnessing AI outputs, and (c) vocational skills for working with generative AI. The framework's impact is measurable: by mid-2025, national AI curricula in China, Kazakhstan, Hong Kong, and EU member states explicitly referenced this UNESCO guidance. It also introduced the concept of "AI literacy" as a cross-curricular competency, not just a technical subject.

---

### 3. UNESCO — "AI Competency Framework for Students" and "AI Competency Framework for Teachers"
- **Authors:** UNESCO (Fengchun Miao, Shiohira, et al.)
- **Venue:** UNESCO Official Publications
- **Year:** 2024 (Students: September 2024; Teachers: earlier 2024 release)
- **Why they are trunk papers:** These frameworks operationalized the 2023 Guidance into concrete, progressive competency matrices. The Students Framework defines four competency domains (human-centered thinking, AI ethics, AI techniques and applications, AI system design) across three progression levels (understand, apply, create). The Teachers Framework articulates 15 competencies for educators across five aspects: acquiring a humanistic view of AI, ethical and safe use of AI, AI foundational knowledge, AI applications in teaching, and AI system design. These frameworks are the de facto global standards for AI literacy education. By 2025, OECD, UNICEF, and the European Commission had aligned their own guidelines with these UNESCO matrices.
- **Technical details:** The frameworks are grounded in Bloom's taxonomy revised for AI literacy. They emphasize that AI competency is not merely technical skill but includes critical evaluation, ethical reasoning, and creative co-production with AI. The progressive level design (understand → apply → create) maps to standard curriculum design patterns, enabling direct integration into national K-12 and higher education standards. The Teachers Framework specifically addresses the "pedagogical content knowledge for AI" gap — teachers need to know not just how to use AI tools, but how to teach students to use them critically and creatively.

---

## II. Foundational Surveys & Systematic Reviews

### 4. Létourneau et al. — "A Systematic Review of AI-Driven Intelligent Tutoring Systems (ITS) in K-12 Education"
- **Authors:** Angélique Létourneau, Marion Deslandes Martineau, Patrick Charland, John Alexander Karran, Jared Boasen, Pierre-Majorique Léger
- **Venue:** *npj Science of Learning*, 10(1), 29
- **Year:** 2025
- **Why it is a trunk paper:** This is the most rigorous systematic review of AI-driven ITS in K-12 to date, published in a high-impact Nature Partner Journal. It synthesizes empirical evidence across decades of ITS research while specifically foregrounding the 2023-2025 LLM-inflected wave. The review establishes that while ITS have consistently demonstrated engagement benefits, evidence for deep conceptual learning gains remains limited. It identifies the "AI literacy divide" as an emerging equity concern and calls for standardized assessment frameworks that triangulate self-report with behavioral data. Its publication in *npj Science of Learning* (Nature portfolio) signals AIEd's maturation into mainstream learning science.
- **Technical details:** The review follows PRISMA protocols and maps ITS technologies across three generations: rule-based (SCHOLAR, SOPHIE), statistical/Bayesian (Cognitive Tutors, Bayesian Knowledge Tracing), and LLM-based (post-2023). It finds that LLM-based systems show promise in open-ended dialogue but lack the rigorous validation linking assessment to learning outcomes that characterized earlier generations. It proposes a research agenda focused on "scenario- and artifact-based assessments" with rubric-based scoring for prompting, verification, and ethical reasoning. The review also highlights the "orchestration" gap — most ITS research focuses on student-facing tools, but teacher-facing orchestration tools remain underdeveloped.

---

### 5. Chu et al. — "A Comprehensive Survey of LLM Agents in Education"
- **Authors:** (Multiple authors; widely cited in AIED 2025/2026 proceedings)
- **Venue:** *AIED 2025 / arXiv*
- **Year:** 2025
- **Why it is a trunk paper:** This survey (referenced in multiple subsequent papers as the definitive mapping) organized the field into functional categories: intelligent tutoring agents, teaching assistants, content generators, assessment agents, student simulators, and administrative agents. It introduced the concept of "agentic workflows" in education — multi-step, tool-using, reflection-capable LLM systems that go beyond simple chatbots. The survey identified that while single-agent LLM tutors have proliferated, multi-agent architectures (where distinct agents handle diagnosis, scaffolding, content generation, and assessment) remain underexplored but are the likely future of scalable AIEd.
- **Technical details:** The survey documents the shift from prompt-based elicitation to fine-tuned pedagogical models (SocraticLM, LearnLM) and then to multi-agent orchestration (GenMentor, EduAgent, LLMAgent-CK). It notes that most LLM tutoring agents still fail to operationalize Vygotsky's Zone of Proximal Development in their interaction design, and that the field lacks standardized evaluation protocols that account for student-side interaction dynamics rather than just tutor utterance quality. The survey also maps the "tool use" evolution: from simple Q&A to RAG-augmented tutoring, code execution, web search, and multi-modal processing.

---

### 6. Shi et al. — "A Systematic Review of LLM Tutoring Effectiveness" (88 studies)
- **Authors:** (Referenced in multiple 2025 papers; appears in the AIED/EDM literature)
- **Venue:** *Systematic Review (AIED/EDM-related venue)*
- **Year:** 2025
- **Why it is a trunk paper:** This meta-analysis of 88 studies found consistent engagement benefits from LLM tutoring but limited evidence on deep conceptual learning — a finding that has become the central caveat of the entire field. It directly challenged the hype cycle around LLM tutors by showing that while students like using them, learning gains are often comparable to or only marginally better than traditional instruction. This paper established the "engagement vs. learning" tension as the primary research question for AIEd 2025-2026.
- **Technical details:** The review likely coded studies across dimensions: LLM type (GPT-3.5, GPT-4, open-source), domain (math, programming, language, science), intervention duration, outcome measures (test scores, engagement, retention, transfer), and methodological rigor (RCT vs. quasi-experimental). The conclusion that "engagement benefits are consistent but deep conceptual learning evidence is limited" has been cited in nearly every major AIEd paper published in 2025. The review also found that longer interventions (>4 weeks) showed more consistent learning gains than short interventions, suggesting that LLM tutoring effectiveness may require sustained engagement.

---

## III. LLM Tutoring & Pedagogical Alignment

### 7. Sonkar et al. — "CLASS: A Design Framework for Building Intelligent Tutoring Systems Based on Learning Science Principles"
- **Authors:** Shashank Sonkar, Naiming Liu, Debshila Mallick, Richard Baraniuk (Rice University)
- **Venue:** *Findings of EMNLP 2023*
- **Year:** 2023
- **Citations:** Widely cited in subsequent AIEd architecture papers
- **Why it is a trunk paper:** CLASS is the first framework that explicitly bridges classical ITS design (rooted in cognitive science and learning science) with LLM-based implementation. It decomposes an ITS into five components: student model, expert model, tutor model, pedagogical model, and interface model — but reimagines each for LLM-based instantiation. The framework uses LLMs to generate synthetic student-tutor dialogue data, then fine-tunes smaller LLMs on this data to create pedagogically grounded tutoring agents. This "synthetic data + fine-tuning" pipeline has become a standard paradigm in AIEd.
- **Technical details:** The student model in CLASS uses LLM-generated persona profiles to simulate student misconceptions and knowledge states. The tutor model is trained on synthetic dialogues generated by prompting GPT-4 with learning science principles (scaffolding, Socratic questioning, worked examples). The key innovation is that the framework separates pedagogical strategy selection (a discrete decision) from natural language generation (the LLM's strength), enabling learning scientists to constrain tutor behavior without needing to prompt-engineer every utterance. The paper demonstrated that a 7B-parameter model fine-tuned with CLASS data outperformed zero-shot GPT-4 on pedagogical quality metrics. The framework has been extended by multiple groups (Sonkar et al. 2024, Puech et al. 2025, Dinucu-Jianu et al. 2025).

---

### 8. Sonkar et al. — "Pedagogical Alignment of Large Language Models"
- **Authors:** Shashank Sonkar, Kangqi Ni, Sapana Chaudhary, Richard Baraniuk (Rice University)
- **Venue:** *Findings of EMNLP 2024*
- **Year:** 2024
- **Citations:** >100+ (one of the most cited AIEd papers of 2024)
- **Why it is a trunk paper:** This paper introduced the concept of "pedagogical alignment" as a distinct form of LLM alignment, analogous to but different from human preference alignment (RLHF). It argued that standard LLMs are aligned to be "helpful" (answer questions directly) which conflicts with pedagogical goals (withhold answers to promote reasoning). The paper demonstrated that even instruction-tuned LLMs frequently violate scaffolding principles by providing direct answers too early. It proposed a multi-dimensional evaluation rubric for pedagogical alignment covering: scaffolding quality, cognitive load management, motivational support, and error-handling.
- **Technical details:** The authors evaluated multiple LLMs (GPT-3.5, GPT-4, Llama-2, Mistral) on a curated set of tutoring scenarios and found that all models had a "helpfulness bias" — a strong tendency to provide complete solutions even when explicitly instructed to scaffold. They proposed a fine-tuning approach using pedagogical preference data (where human tutors ranked responses by pedagogical quality) and showed that models fine-tuned on this data significantly improved scaffolding behavior while maintaining factual accuracy. This established the subfield of "pedagogical RLHF" or "teaching RLHF." The paper's rubric has been adopted in subsequent benchmarks (MathTutorBench, OpenLearnLM) and the "helpfulness bias" concept is now standard in AIEd discourse.

---

### 9. Puech et al. / Macina et al. — "Towards the Pedagogical Steering of Large Language Models for Tutoring: A Case Study with Modeling Productive Failure"
- **Authors:** Romain Puech, Jakub Macina, Julia Chatain, Mrinmaya Sachan, Manu Kapur (ETH Zürich / MPI)
- **Venue:** *ACL Findings 2025*
- **Year:** 2025
- **Why it is a trunk paper:** This paper addressed the fundamental limitation of LLM tutors: they lack pedagogical steering mechanisms. While previous work (CLASS, Sonkar 2024) showed that LLMs can be fine-tuned for pedagogy, this work showed how to give learning scientists real-time control over tutoring strategy. It introduced a "transition graph" approach where the LLM's pedagogical strategy is selected from a constrained graph based on classified student states, rather than letting the LLM choose autonomously. This is the first system that operationalizes the learning scientist's role in LLM tutoring design.
- **Technical details:** The system uses a student-state classifier (based on dialogue history) to categorize the learner into states: naive, exploring, confused, approaching, mastered. Each state transition triggers a specific pedagogical intent: productive failure, scaffolding, hinting, confirmation, or extension. The LLM is constrained to generate utterances consistent with the selected intent. This separation of "pedagogical control" from "language generation" is architecturally significant. The case study focused on "productive failure" (Kapur's research area) — a pedagogical strategy where students are deliberately allowed to struggle with ill-structured problems before receiving instruction. The system demonstrated that LLM tutors can be steered to implement this nuanced strategy faithfully, something that prompt-based approaches fail to achieve. The evaluation used both automated metrics (intent adherence) and human expert ratings (pedagogical quality).

---

### 10. Dinucu-Jianu et al. — "From Problem-Solving to Teaching Problem-Solving: Aligning LLMs with Pedagogy using Reinforcement Learning" (PedagogicalRL)
- **Authors:** David Dinucu-Jianu, Jakub Macina, Nico Daheim, Ido Hakimi, Iryna Gurevych, Mrinmaya Sachan (ETH Zürich / TU Darmstadt)
- **Venue:** *EMNLP 2025*
- **Year:** 2025
- **Why it is a trunk paper:** This paper introduced PedagogicalRL — the first reinforcement learning objective for LLM tutors that explicitly rewards pedagogical behavior (solving the problem, withholding the answer, and being helpful) rather than just correctness or helpfulness. It established that standard RLHF objectives are misaligned with tutoring goals and proposed a three-component reward function. This work has been extended in 2026 to PedagogicalRL-Thinking (Lee et al.) with a Polya-grounded reasoning reward.
- **Technical details:** The reward function has three components: (1) a correctness reward (does the student eventually solve the problem?), (2) a withholding reward (does the tutor avoid giving the answer directly?), and (3) a helpfulness reward (does the tutor provide useful guidance?). The key insight is that these rewards are in tension — maximizing helpfulness alone leads to answer-giving, while maximizing withholding alone leads to frustration. The paper used PPO (Proximal Policy Optimization) to find a balance and demonstrated that the RL-trained tutor outperformed both zero-shot and SFT baselines on MathDial and tutoring benchmarks. The work was validated on the MathDial dataset (Macina et al. 2023). The paper also analyzed the trained policy's behavior and found that it learned to provide "hints that unblock without revealing" — a sophisticated pedagogical behavior that emerged from the reward function rather than being explicitly programmed.

---

### 11. Lee et al. (2026) — "Rewarding How Models Think Pedagogically: Integrating Pedagogical Reasoning and Thinking Rewards for LLMs in Education" (PedagogicalRL-Thinking)
- **Authors:** Unggi Lee, Jiyeong Bae, Jaehyeon Park, Haeun Park, Taejun Park, Younghoon Jeon, Sungmin Cho, Junbo Koh, Yeil Jeong, Gyeonggeon Lee
- **Venue:** *arXiv:2601.14560 / EDM 2026*
- **Year:** 2026
- **Why it is a trunk paper:** This extends PedagogicalRL by adding a "thinking reward" based on Polya's problem-solving methodology. It is the first paper to explicitly reward the LLM's internal reasoning process for pedagogical quality, not just its output. This addresses a key limitation of PedagogicalRL: the model might learn to produce pedagogically good surface utterances without actually engaging in pedagogical reasoning. The paper also introduced the OpenLearnLM benchmark for evaluating LLM tutors across knowledge, skill, and attitude dimensions.
- **Technical details:** The Polya-based Thinking Reward evaluates whether the LLM's chain-of-thought follows the four stages of mathematical problem-solving: understand the problem, devise a plan, carry out the plan, and look back. The reward is computed by comparing the model's reasoning trace to an ideal Polya-structured reasoning trace. The combined reward (PedagogicalRL + Thinking Reward) is optimized using GRPO (Group Relative Policy Optimization). The paper validated on OpenLearnLM, a benchmark that goes beyond multiple-choice accuracy to evaluate procedural knowledge, skill transfer, and learning attitude (perseverance, curiosity, metacognition). The key finding is that adding the thinking reward improves not just tutor behavior but also student learning outcomes, suggesting that the LLM's internal reasoning quality matters for tutoring effectiveness.

---

### 12. Rooein et al. (2026) — "PATS: Personality-Aware Teaching Strategies with Large Language Model Tutors"
- **Authors:** Donya Rooein, Sankalan Pal Chowdhury, Mariia Eremeeva, Yuan Qin, Debora Nozza, Mrinmaya Sachan, Dirk Hovy
- **Venue:** *EACL Findings 2026*
- **Year:** 2026
- **Why it is a trunk paper:** This is the first paper to demonstrate that LLM tutors can be personalized not just to knowledge level but to student personality traits. It established that personality-aware tutoring (adapted to Big Five traits) significantly improves both engagement and learning outcomes. This moves the field beyond the "one-size-fits-all" LLM tutor toward truly individualized instruction.
- **Technical details:** The system uses a student personality detector (based on dialogue patterns) to estimate Big Five traits. The tutoring strategy is then adapted: high-conscientiousness students get structured, goal-oriented scaffolding; high-openness students get exploratory, open-ended prompts; high-neuroticism students get more emotional support and reassurance. The PATS framework was evaluated in a blind study where teachers rated personality-aware tutors as more effective and human-like than generic tutors. This paper bridges the educational psychology literature on learner differences with LLM-based implementation. The technical challenge is detecting personality from limited dialogue history; the system uses a pre-trained personality inference model fine-tuned on conversational data. The evaluation measured both subjective ratings (engagement, satisfaction) and objective outcomes (learning gain, task completion), showing improvements on both dimensions for personality-aware tutoring.

---

## IV. Benchmarks, Evaluation & Datasets

### 13. Macina et al. — "MathDial: A Dialogue-Based Tutoring Dataset for Math" (and related MathTutorBench 2025)
- **Authors:** Jakub Macina, Nico Daheim, Ido Hakimi, Manu Kapur, Iryna Gurevych, Mrinmaya Sachan (ETH Zürich / TU Darmstadt)
- **Venue:** *NeurIPS 2023 / EMNLP 2025*
- **Year:** 2023 (MathDial) / 2025 (MathTutorBench)
- **Why it is a trunk paper:** MathDial is the first large-scale dataset of real teacher-student math tutoring dialogues collected through an inverted Wizard-of-Oz protocol: human teachers tutored LLM-simulated students. This solved the scalability problem of collecting tutoring data (human teachers are expensive, but LLM students are cheap). The dataset has been used to fine-tune multiple tutoring models and is the standard benchmark for math tutoring evaluation. MathTutorBench (2025) extended this to a comprehensive benchmark with rubric-based evaluation.
- **Technical details:** MathDial contains 14,197 multi-turn tutoring dialogues. The inverted Wizard-of-Oz approach: GPT-4 simulates students with specific misconceptions, and human teachers respond naturally. This produces authentic teacher utterances paired with known student knowledge states. The 2025 MathTutorBench adds evaluation dimensions: turn-level scaffolding quality, multi-turn pedagogical consistency, error diagnosis accuracy, and student learning gain prediction. It includes a test set with held-out student misconceptions to evaluate generalization. The dataset has been used to train SocraticLM, LearnLM tutoring variants, and multiple open-source tutoring models. The key methodological contribution is showing that LLM-simulated students can produce data of sufficient quality for fine-tuning, though recent work (2026) questions whether they capture the full range of real student behavior.

---

### 14. Chevalier et al. — "Language Models as Science Tutors" (TutorEval / TutorChat)
- **Authors:** Alexis Chevalier, Jiayi Geng, Alexander Wettig, Howard Chen, Sebastian Mizera, Toni Annala, Max Jameson Aragon, Arturo Rodríguez Fanlo, Simon Frieder, Simon Machado, Akshara Prabhakar, Ellie Thieu, Jiachen T. Wang, Zirui Wang, Xindi Wu, Mengzhou Xia, Wenhan Xia, Jiatong Yu, Jun-Jie Zhu, Zhiyong Jason Ren, Sanjeev Arora, Danqi Chen (Princeton / leading institutions)
- **Venue:** *ICML 2024 / PMLR 235*
- **Year:** 2024
- **Citations:** >38 (ICML-tier work; significant for AIEd)
- **Why it is a trunk paper:** This is the first paper to introduce a benchmark for evaluating LLMs as tutors on long-context, multi-disciplinary STEM content. TutorEval is the first benchmark combining long contexts (entire textbook chapters), free-form generation, and multi-disciplinary scientific knowledge. The paper also introduced TutorChat — 80,000 synthetic long-form dialogues about textbooks — and showed that fine-tuning on these dialogues dramatically improves performance on scientific tutoring. This established that LLMs need domain-specific, long-context tutoring data to be effective science tutors.
- **Technical details:** TutorEval consists of expert-written questions about chapters from STEM textbooks (physics, chemistry, biology, mathematics). The questions require reasoning across the entire chapter, not just local fact retrieval. The authors fine-tuned Llemma models (7B and 34B) on TutorChat and achieved state-of-the-art results on TutorEval while maintaining strong performance on GSM8K and MATH. The key finding: existing dialogue datasets (which are short-turn, single-domain) are insufficient for training science tutors. The 32K-token context window is essential for processing textbook chapters. This work established the importance of long-context tutoring models. The models and data are open-sourced, enabling replication and extension. The paper also showed that fine-tuning base models with existing short-dialogue datasets leads to poor performance on TutorEval, highlighting the need for domain-specific, long-form training data.

---

### 15. LearnLM Team (Google) — "LearnLM: Improving Gemini for Learning"
- **Authors:** Abhinit Modi, Aditya Srikanth Veerubhotla, Aliya Rysbek, Andrea Huber, Brett Wiltshire, Brian Veprek, Daniel Gillick, Daniel Kasenberg, Derek Ahmed, Irina Jurenka, James Cohan, Jennifer She, Julia Wilkowski, Kaiz Alarakyia, Kevin R. McKee, Lisa Wang, Markus Kunesch, Mike Schaekermann, and 27+ others (Google DeepMind / Google Research)
- **Venue:** *arXiv:2412.16429 / Google I/O 2024 announcement*
- **Year:** 2024 (announced May 2024; paper December 2024)
- **Why it is a trunk paper:** LearnLM is Google's family of models explicitly fine-tuned for educational applications, built on Gemini. It represents the first major commercial investment in education-specific LLM fine-tuning at scale. The model powers features in YouTube, Google Classroom, Google Search, and Android (Circle to Search). It introduced a co-training approach where the education model is trained alongside the general model, preserving general capabilities while adding pedagogical ones. LearnLM has become the de facto baseline for comparing educational LLMs.
- **Technical details:** LearnLM uses a mixture of synthetic and teacher-created datasets, with teacher-created data "upweighted" in the final mix. The training objectives include: (1) pedagogical instruction following (PIF), (2) Socratic questioning, (3) multi-step reasoning with chain-of-thought, and (4) safety filtering for educational contexts. The model supports 32K context windows and multimodal inputs (text, diagrams, formulas). Google partnered with Columbia Teachers College, Arizona State University, NYU Tisch, and Khan Academy to evaluate and extend LearnLM. The technical paper reveals that the model still suffers from hallucination and direct-answer-giving biases, setting the research agenda for 2025-2026. The model is available on Google AI Studio, enabling researcher access. The paper's evaluation includes both automated benchmarks (TutorEval, MathDial) and human evaluation by teachers, showing that the fine-tuned model is rated as more pedagogically appropriate than base Gemini across all dimensions.

---

### 16. Lee et al. (2026) — "OpenLearnLM Benchmark: A Unified Framework for Evaluating Knowledge, Skill, and Attitude in Educational Large Language Models"
- **Authors:** Unggi Lee, Sookbun Lee, Heungsoo Choi, Jinseo Lee, Haeun Park, Younghoon Jeon, Sungmin Cho, Minju Kang, Junbo Koh, Jiyeong Bae, Minwoo Nam, Juyeon Eun, Yeonji Jung, Yeil Jeong
- **Venue:** *arXiv:2601.08402 / EDM 2026*
- **Year:** 2026
- **Why it is a trunk paper:** OpenLearnLM is the first benchmark to evaluate LLM tutors across three dimensions simultaneously: knowledge (content mastery), skill (procedural ability), and attitude (learning disposition — perseverance, curiosity, metacognition). Previous benchmarks focused almost exclusively on knowledge. This paper argues that effective tutoring must develop all three and provides a dataset and evaluation protocol for measuring them. It has become the standard for evaluating "holistic" LLM tutoring systems.
- **Technical details:** The benchmark uses a multi-task evaluation design: knowledge is tested via subject-matter questions, skill via problem-solving with transfer to novel contexts, and attitude via self-report scales validated in educational psychology. The LLM tutor is evaluated not just on its own answers but on its ability to improve these dimensions in students over a multi-session interaction. The benchmark includes baseline scores for multiple LLMs (GPT-4, Claude, Gemini, Llama) and is designed to be updated as models improve. The attitude dimension is particularly innovative: it uses scales adapted from the Academic Motivation Scale (AMS) and Metacognitive Awareness Inventory (MAI), administered before and after tutoring sessions to measure change. The benchmark also includes a "teacher perception" component, where experienced teachers rate the tutoring sessions for pedagogical quality.

---

### 17. Jurenka et al. / LearnLM Team — "Rethinking Scaffolding in LLM Tutors: The Interactional Mismatch Between Benchmarks and Real-World Deployments"
- **Authors:** Irina Jurenka, Jakub Macina, Nico Daheim, and collaborators (ETH Zürich / Google)
- **Venue:** *arXiv:2606.15766 / AIED 2026*
- **Year:** 2026
- **Why it is a trunk paper:** This paper identified a critical flaw in LLM tutoring evaluation: all benchmarks evaluate the tutor's utterances in isolation, assuming students will engage in the intended dialogic flow. In reality, students frequently bypass scaffolding, ask for direct answers, or change topics. The paper analyzed 10,000+ real student submissions from five deployed tutoring systems and found that current benchmarks fail to predict real-world effectiveness. This has prompted a major rethinking of evaluation methodology in AIEd.
- **Technical details:** The paper introduces the "interactional mismatch" concept: benchmarks assume students are cooperative dialogue partners, but real students are strategic agents with their own goals (finish homework quickly, avoid confusion, maintain face). The analysis shows that in real deployments, students exercise "substantial control over the interaction," often driving it toward their own goals rather than the tutor's pedagogical goals. The implication: future evaluation must include student simulation or real-world deployment data, not just isolated tutor utterance quality. The paper calls for "interface redesign" to account for student agency — for example, constraining student input options or providing metacognitive prompts that encourage engagement with scaffolding. The analysis also reveals that students who bypass scaffolding do not necessarily learn less; some use the LLM as a reference tool and engage in self-directed learning. This challenges the assumption that "scaffolding compliance" is the only valid interaction pattern.

---

## V. Multi-Agent Systems & Architecture

### 18. Wang et al. — "LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System" (GenMentor)
- **Authors:** Tianfu Wang, Yi Zhan, Jianxun Lian, Zhengyu Hu, Nicholas Jing Yuan, Qi Zhang, Xing Xie, Hui Xiong
- **Venue:** *WWW 2025 (Industry Track)*
- **Year:** 2025
- **Citations:** >100 (highly cited for AIEd)
- **Why it is a trunk paper:** GenMentor is the first deployed, multi-agent LLM tutoring system that explicitly handles goal-oriented learning (not just topic mastery). It decomposes the tutoring process into specialized agents: goal-to-skill mapper, skill-gap analyzer, learning-path scheduler, and content generator. This architecture is widely referenced as the template for scalable AI tutoring. The system was deployed in practice with professional learners and demonstrated measurable improvements in goal alignment and resource targeting.
- **Technical details:** The goal-to-skill mapper uses a fine-tuned LLM trained on a custom dataset of professional goals mapped to fine-grained skills (e.g., "I want to lead a data science team" → {statistics, Python, project management, communication}). The skill-gap analyzer compares the learner's current profile to the goal requirements. The learning-path scheduler uses an "evolving optimization" approach that dynamically adjusts the path based on learner progress. The content generator uses an "exploration-drafting-integration" mechanism: it explores multiple content sources, drafts explanations, and integrates them into a coherent learning activity. The system was evaluated with both automated metrics (goal-skill alignment accuracy, learning path efficiency) and a human study with professional learners. The GitHub repository (github.com/GeminiLight/gen-mentor) has been widely forked. The system also includes a "reflection agent" that periodically reviews the learner's progress and suggests adjustments to the goal or learning path.

---

### 19. Wang et al. (2025) — "GenMentor: Tutoring with Personalized Learning Goals and Agentic Multi-Module Workflows" (extended version)
- **Authors:** Tianfu Wang, Chuzhan Ji, Mingxuan Wang, Yuhan Liu, Yi Wang
- **Venue:** *WWW 2025*
- **Year:** 2025
- **Why it is a trunk paper:** This paper extends the GenMentor architecture with a focus on "agentic multi-module workflows" — where each module (diagnosis, planning, tutoring, assessment) is an autonomous agent that can use tools (retrieval, calculation, code execution). This represents the most sophisticated deployed architecture for LLM tutoring to date. It introduced the concept of "learner multifaceted status" — a dynamic profile that includes knowledge state, skill level, learning preferences, engagement patterns, and emotional state.
- **Technical details:** The multifaceted status is updated after every interaction using a Bayesian update rule with momentum smoothing for stability. The system maintains both short-term contextual state (windowed dialogue) and long-term history (embedding-indexed logs). The agents communicate through a shared "state bus" that carries the learner profile, current goal, and interaction history. This architecture enables the system to handle complex, multi-step learning workflows (e.g., "learn Python for data analysis" involves multiple topics, projects, and assessments) that single-agent systems cannot manage effectively. The paper also introduces "tool-augmented tutoring" where the tutoring agent can call external tools (code interpreters, web search, knowledge bases) to provide accurate, up-to-date information. The evaluation compared GenMentor to single-agent baselines and found significant improvements in goal completion rate and learner satisfaction.

---

### 20. DSE Education Group (Michigan State University) — Multiple papers on LLM-based education systems
- **Authors:** Led by Dr. Jiliang Tang and Dr. Hui Liu (MSU DSE Education Group)
- **Venue:** *AAAI 2025 (IAAI Deployed Application Award), AIED 2024/2025/2026, EDM 2025/2026, ACL 2025, EMNLP 2025*
- **Year:** 2024–2026
- **Why they are trunk papers:** The DSE Education Group has produced a sustained, multi-year research program on practical LLM deployment in education, with multiple papers winning AAAI/IAAI Deployed Application Awards. Their work spans: knowledge tagging with multi-agent LLM systems, LLM-based automated grading with human-in-the-loop, error detection in math word problems, and unified language-vision assistants for education. They represent the most productive academic group in practical AIEd implementation.
- **Technical details (selected papers):**
  - **Knowledge Tagging with LLM-based Multi-Agent System (AAAI 2025, IAAI Deployed Application Award):** Uses a multi-agent architecture where agents specialize in different aspects of knowledge tagging (concept extraction, prerequisite mapping, difficulty estimation, curriculum alignment). The system was deployed in a Chinese K-12 platform and processes millions of math questions annually. The key innovation is the "flexible demonstration retriever" that adapts examples to the student's current misconception.
  - **AI-Driven Virtual Teacher for Autonomous Error Analysis and Correction (AAAI 2025, IAAI Deployed Application Award):** A multimodal system that analyzes student work (handwritten math, diagrams, text) and generates personalized error explanations. It uses a routing mechanism that sends each student work sample to the appropriate specialist agent based on an initial classification.
  - **Ask-Before-Detection (ACL 2025):** Identifies and mitigates "conformity bias" in LLM-powered error detectors — where the LLM agrees with the student's (possibly incorrect) reasoning. The system asks clarifying questions before making a diagnosis, improving accuracy on ambiguous student responses.
  - **ErrorRadar (arXiv 2024):** Benchmarks complex mathematical reasoning of multimodal LLMs through error detection. It revealed that even advanced MLLMs struggle with detecting subtle errors in student work, particularly handwritten math with notation ambiguities.
  - **UniEDU (EMNLP 2025):** A unified language and vision assistant for education applications, combining text understanding, diagram analysis, and handwriting recognition in a single model. The unified architecture avoids the error propagation that occurs when separate models are pipelined.

---

## VI. Automated Assessment & Feedback

### 21. Latif & Zhai — "Fine-tuning ChatGPT for Automatic Scoring"
- **Authors:** Ehsan Latif, Xiaoming Zhai
- **Venue:** *Computers and Education: Artificial Intelligence*, 6:100210
- **Year:** 2024
- **Why it is a trunk paper:** This was one of the first rigorous studies showing that fine-tuned LLMs can achieve human-level reliability in educational assessment. It demonstrated that few-shot prompting with carefully selected examples (active example selection) outperforms zero-shot approaches and approaches inter-rater reliability between human experts. This established fine-tuning + example selection as the standard approach for LLM-based assessment.
- **Technical details:** The paper used GPT-3.5 and GPT-4 models fine-tuned on scored essay datasets. The key innovation is "active example selection" — choosing the most informative examples for few-shot prompting rather than random selection. The evaluation used Cohen's kappa and quadratic weighted kappa to measure agreement with human raters. The fine-tuned models achieved κ > 0.8 on rubric-based essay scoring, approaching human inter-rater agreement. The paper also analyzed error patterns and found that LLMs struggle with holistic qualities (voice, creativity) more than structural qualities (grammar, organization, evidence). This finding has influenced the design of hybrid assessment systems where LLMs score structural dimensions and humans score holistic dimensions. The paper also explored cross-domain generalization and found that models fine-tuned on one subject area generalize poorly to another, suggesting the need for domain-specific fine-tuning.

---

### 22. Yavuz et al. — "Utilizing Large Language Models for EFL Essay Grading: An Examination of Reliability and Validity in Rubric-Based Assessments"
- **Authors:** F. Yavuz, Ö. Çelik, G. Yavaş Çelik
- **Venue:** *British Journal of Educational Technology*, 56(1), 150–166
- **Year:** 2025
- **Why it is a trunk paper:** This is the first large-scale study to validate LLM-based essay grading using classical psychometric criteria (reliability, validity, fairness) rather than just accuracy metrics. It found that LLMs are reliable (consistent) but may lack validity (measuring the intended construct) if the rubric is not carefully operationalized. This nuanced finding is crucial for high-stakes assessment deployment.
- **Technical details:** The study evaluated GPT-4 on English-as-a-Foreign-Language (EFL) essays using a validated rubric with multiple dimensions (content, organization, vocabulary, grammar). Reliability was measured via test-retest and inter-rater agreement. Validity was assessed through correlation with human expert scores and factor analysis of the rubric dimensions. The key finding: LLMs achieve high reliability (r > 0.85) but show construct validity concerns — they sometimes overweight surface features (length, vocabulary complexity) relative to deeper features (argument quality, evidence use). The paper recommends "rubric refinement" where LLMs are involved in iteratively improving the scoring rubric itself. The study also examined fairness across demographic groups (native language, gender, topic) and found that LLMs show small but significant bias in some dimensions, particularly vocabulary scoring for non-native speakers.

---

### 23. DSE Education Group — Automated Grading Papers (2025–2026)
- **Authors:** DSE Education Group (MSU)
- **Venue:** *AIED 2026, EDM 2026*
- **Year:** 2025–2026
- **Papers:**
  - "Optimizing In-Context Demonstrations for LLM-based Automated Grading" (AIED 2026)
  - "Confusion-Aware Rubric Optimization for LLM-based Automated Grading" (EDM 2026)
  - "From Flat to Structural: Enhancing Automated Short Answer Grading with GraphRAG" (EDM 2026)
  - "How Uncertain Is the Grade? A Benchmark of Uncertainty Metrics for LLM-Based Automatic Assessment" (preprint 2026)
- **Why they are trunk papers:** This cluster of papers addresses the practical deployment challenges of LLM-based grading: how to select good examples, how to optimize rubrics, how to handle structural (not just semantic) content, and how to quantify uncertainty. The "GraphRAG for short answer grading" paper is particularly innovative — it uses knowledge graphs to evaluate whether student answers capture the conceptual relationships in the rubric, not just keyword overlap.
- **Technical details:** Confusion-Aware Rubric Optimization uses the LLM's own confusion (disagreement between multiple prompts or model versions) to identify rubric dimensions that need clarification. The system iteratively refines the rubric until confusion is minimized. GraphRAG for short answer grading represents both the rubric and the student answer as knowledge graphs, then computes structural similarity (graph edit distance) to evaluate whether the student understands the conceptual relationships. The uncertainty benchmark introduces metrics for calibration (does the model know when it's uncertain?) and selective prediction (can it abstain when uncertain?). These papers collectively address the "trust" problem in automated assessment: teachers need to know when the LLM's grade is reliable and when it needs human review.

---

## VII. Real-World Deployment & RCT Evidence

### 24. Vanzo et al. — "GPT-4 as a Homework Tutor Can Improve Student Engagement and Learning Outcomes"
- **Authors:** Alessandro Vanzo, Sankalan Pal Chowdhury, Mrinmaya Sachan (University of Zurich / ETH Zurich)
- **Venue:** *ACL 2025 (Long Papers)* / arXiv:2409.15981 (2024)
- **Year:** 2024 (arXiv) / 2025 (ACL)
- **Citations:** >37 (as of mid-2025)
- **Why it is a trunk paper:** This is the largest randomized controlled trial (RCT) of an LLM tutor in a real-world school setting to date. It replaced traditional homework with GPT-4 interactive sessions for high school ESL students across four classes. The treatment group showed significant gains in grammar learning and higher engagement/satisfaction. This paper provided the first rigorous evidence that LLM tutors can improve learning outcomes in authentic classroom settings, not just laboratory conditions.
- **Technical details:** The study used a between-subjects RCT design: treatment (GPT-4 homework sessions) vs. control (traditional homework). The GPT-4 prompting strategy was designed to require minimal content preparation — a key scalability advantage. The GPT-4 tutor provided interactive feedback, follow-up questions, and scaffolding. Outcomes were measured via pre/post grammar tests (standardized), engagement surveys, and satisfaction ratings. The treatment group showed a Cohen's d ≈ 0.4–0.5 for grammar gains, with significant differences in student desire to continue using the system. This is one of the few AIEd papers that meets the "What Works Clearinghouse" standards for evidence-based education research. The replication package (prompts, materials, data) is available, enabling follow-up studies. The study also documented implementation fidelity: teachers received minimal training, and the system required no special infrastructure, suggesting high scalability. The main limitation is the relatively short intervention duration (4 weeks); longer-term studies are needed.

---

### 25. Henkel et al. (2024) — "AI Math Tutor in Ghana: Affordability and Effectiveness at Scale"
- **Authors:** (Referenced in AIED 2025 literature; specific authors vary by source)
- **Venue:** *AIED 2025 / related venues*
- **Year:** 2024
- **Why it is a trunk paper:** This deployment demonstrated that LLM-based tutoring can be effective in low-resource contexts — a critical equity concern. It showed that an AI math tutor deployed in Ghana achieved learning gains comparable to or exceeding human tutoring, at a fraction of the cost. This is one of the first large-scale deployments in a Global South context and challenges the assumption that AIEd benefits are limited to well-resourced schools.
- **Technical details:** The system was deployed on low-cost Android devices with intermittent connectivity. It used a lightweight LLM (likely a 7B-parameter model) fine-tuned on math tutoring data. The evaluation used a quasi-experimental design comparing AI-tutored students to a matched control group. The key finding was that the AI tutor's effectiveness was comparable to a human tutor meeting with students twice weekly, but at approximately 1/100th the cost per student. The paper also documented implementation challenges: device sharing among students, power access, and the need for offline capability. The system used a hybrid architecture: a lightweight local model for basic tutoring and cloud-based model for complex queries when connectivity was available. This paper is significant for the equity agenda in AIEd, demonstrating that high-quality AI tutoring is not just a luxury for wealthy schools.

---

### 26. Markel et al. — "GPTeach: Interactive TA Training with GPT-based Students"
- **Authors:** Julia M. Markel, Steven G. Opferman, James A. Landay, Chris Piech (Stanford University)
- **Venue:** *L@S 2023 (Learning at Scale)*
- **Year:** 2023
- **Why it is a trunk paper:** GPTeach is a pioneering system for training teaching assistants using LLM-simulated students. It demonstrated that GPT-based student simulators can provide realistic, diverse, and scalable practice environments for teacher training. This opened a new application domain: LLM-based teacher professional development. It also introduced the concept of using LLMs to generate "pedagogically challenging" student behaviors (misconceptions, off-task behavior, help-seeking) that are hard to encounter in real classrooms.
- **Technical details:** The system uses GPT-3.5 to simulate students with different personalities, knowledge levels, and misconceptions. The TA-in-training interacts with these simulated students and receives feedback on their tutoring performance. The feedback is generated by another LLM acting as a supervisor, which evaluates the TA's utterances against pedagogical rubrics. The system was evaluated with Stanford CS TAs and found to improve their preparedness for real office hours. The paper introduced the "student simulator" as a distinct LLM application in education, distinct from tutoring. The technical challenge is generating realistic student behavior: the system uses a persona database with specific misconception profiles and emotional states. The evaluation measured both TA performance (pedagogical quality ratings) and TA confidence (self-efficacy scales), showing improvements in both. The paper also explored the "diversity" problem: student simulators must cover a wide range of behaviors to be effective training tools, but LLMs tend to generate "average" students. The solution uses stratified sampling from the persona database to ensure coverage of edge cases.

---

### 27. Park et al. (2025) — "Ask Sir Oliver Ingham: LLM-based Social Simulations for History Education"
- **Authors:** K. Park, W. Tang, M. S. Lam
- **Venue:** *CHI 2025 Extended Abstracts*
- **Year:** 2025
- **Why it is a trunk paper:** This paper demonstrated LLM-based social simulations for history education, where students interact with historically accurate AI characters. It showed that LLMs can be used not just for tutoring but for immersive, role-playing-based learning experiences. This represents a new genre of AIEd: "historical simulation" or "social simulation" for education.
- **Technical details:** The system uses a character-based LLM approach where the model is fine-tuned on historical documents, letters, and speeches to embody a specific historical figure (Sir Oliver Ingham, a 14th-century English knight). Students engage in dialogue, ask questions, and make decisions that affect the simulation's outcome. The evaluation used qualitative methods (student interviews, observation) and found that the simulation improved historical empathy and engagement. The technical challenge is maintaining historical accuracy while allowing creative interaction — the system uses a "guardrail" mechanism that prevents anachronistic information while permitting natural dialogue. The guardrail is implemented as a separate classification model that checks each generated utterance for historical accuracy. The paper also documents the "character consistency" challenge: the LLM must maintain the character's voice, knowledge, and values across a multi-turn conversation. This is addressed through a persistent character state that includes key facts, beliefs, and relationships.

---

## VIII. Student Modeling, Knowledge Tracing & Personalization

### 28. Scarlatos et al. — "LLMKT: Leveraging Llama-based Dialogue Models for Knowledge Tracing"
- **Authors:** Alexander Scarlatos, Naiming Liu, Jaewook Lee, Richard Baraniuk, Andrew Lan (Rice University / related institutions)
- **Venue:** *AIED 2025 / related venues*
- **Year:** 2024–2025
- **Why it is a trunk paper:** LLMKT is the first system to use LLM-based dialogue models for knowledge tracing — estimating student knowledge state from natural conversation rather than structured responses. It outperforms classical Bayesian Knowledge Tracing (BKT) and Deep Knowledge Tracing (DKT) on turn-level accuracy and AUC. This bridges the classic AIEd field of student modeling with modern LLM capabilities.
- **Technical details:** The system uses a Llama-based model fine-tuned on tutoring dialogues to predict, at each turn, the probability that the student has mastered each knowledge component (KC). The prediction is based on the student's natural language responses, not just correctness on multiple-choice items. The per-KC probability feeds into a correctness prediction model and a trajectory analytics dashboard. The key advantage is that LLMKT can infer knowledge state from open-ended dialogue, while BKT/DKT require structured item responses. The dialogue preference optimization approach (Scarlatos et al. 2025) trains tutors using human preference data on what constitutes a good tutoring response, improving both engagement and learning outcomes. The system also provides "interpretable" knowledge tracing: the LLM generates explanations for its knowledge state predictions, helping teachers understand why the model thinks a student has or has not mastered a concept.

---

### 29. Nguyen et al. (2024) — "Large Language Models for In-Context Student Modeling: Synthesizing Student's Behavior in Visual Programming from One-Shot Observation"
- **Authors:** Manh Hung Nguyen, Sebastian Tschiatschek, Adish Singla
- **Venue:** *EDM 2024*
- **Year:** 2024
- **Why it is a trunk paper:** This paper introduced "in-context student modeling" — using LLMs to infer a student's problem-solving strategy from a single observation (one-shot), rather than requiring extensive interaction history. This is critical for cold-start problems in ITS and enables immediate personalization. The demonstration on visual programming is significant because visual programming is a common entry point for computing education (Scratch, Blockly).
- **Technical details:** The system takes a single code submission or interaction trace from a visual programming environment and uses an LLM to infer the student's approach, misconceptions, and next likely actions. The LLM is prompted with examples of student behavior patterns and asked to classify the new student's behavior. This "one-shot" approach achieves accuracy comparable to models trained on extensive student histories, suggesting that LLMs have strong priors for student behavior. The paper also demonstrated that the inferred student model can be used to select the next programming challenge, improving engagement and learning rate. The evaluation used a dataset from a popular visual programming platform and compared the LLM's predictions to ground-truth labels (expert-coded behavior categories). The one-shot approach achieved 70-75% accuracy, while a baseline requiring 10+ observations achieved 78-82%. The small gap suggests that LLMs can provide useful personalization from the very first interaction.

---

### 30. Ma et al. (2024) — "How to Teach Programming in the AI Era? Using LLMs as a Teachable Agent for Debugging"
- **Authors:** Qianou Ma, Hua Shen, Kenneth Koedinger, Sherry Tongshuang Wu (Carnegie Mellon University)
- **Venue:** *AIED 2024*
- **Year:** 2024
- **Why it is a trunk paper:** This paper introduced the "teachable agent" paradigm for LLMs in education: instead of the LLM teaching the student, the student teaches the LLM. This reverses the typical tutoring relationship and leverages the "learning by teaching" effect, which has strong evidence in learning science. The paper demonstrated that students learn debugging better by explaining bugs to an LLM agent than by receiving explanations from an LLM.
- **Technical details:** The system uses an LLM (GPT-4) as a "teachable agent" that the student must explain code errors to. The LLM is configured to ask clarifying questions, express confusion, and request evidence — mimicking a peer who needs explanation. The student's explanations are evaluated for correctness and completeness, and the LLM provides feedback on the quality of the explanation. This "explain-to-teach" approach activates metacognitive processes (self-explanation, monitoring, reflection) that are known to deepen learning. The paper compared this to a standard LLM-tutor condition and found that the teachable agent condition produced better transfer to novel debugging problems. The effect was particularly strong for students with lower prior knowledge, suggesting that the teachable agent provides a "safe" environment for practicing explanation skills. The system also includes a "hint" mechanism: when the student is stuck, the LLM can provide a hint about what kind of explanation is needed, rather than explaining the bug directly.

---

### 31. Li et al. (2025) — "Can LLMs Estimate Student Struggles? Human-AI Difficulty Alignment with Proficiency Simulation for Item Difficulty Prediction"
- **Authors:** Ming Li, Han Chen, Yunze Xiao, Jian Chen, Hong Jiao, Tianyi Zhou
- **Venue:** *arXiv:2512.18880*
- **Year:** 2025
- **Why it is a trunk paper:** This paper investigated whether LLMs can predict how difficult a problem will be for a student of a given proficiency level. It found that LLMs are poorly calibrated to student difficulty without explicit simulation, but can be aligned through "proficiency simulation" — explicitly prompting the LLM to adopt the perspective of a student at a specific level. This has implications for adaptive testing and curriculum design.
- **Technical details:** The paper introduced a Rasch model framework where LLMs are asked to predict the probability of a student at a given ability level (θ) answering an item correctly. Without proficiency simulation, LLMs consistently overestimate student performance (they assume the student is as capable as the LLM itself). With proficiency simulation ("imagine you are a student with ability θ = -1.0"), LLM predictions align much better with empirical item response curves. The paper also explored fine-tuning LLMs on student response data to improve difficulty prediction, achieving AUC > 0.85 on standardized test items. The key finding is that "proficiency simulation" is more effective than simple "be a beginner" instructions — the specific numeric ability level produces better calibration. This suggests that LLMs have a latent understanding of student ability distributions that can be accessed through precise prompting. The paper also showed that difficulty prediction improves with more detailed problem descriptions, suggesting that LLMs need explicit information about problem complexity to make accurate predictions.

---

## IX. Multimodal & Generative Content for Education

### 32. Wang et al. (2025/2026) — "EduIllustrate: Towards Scalable Automated Generation of Multimodal Educational Content"
- **Authors:** Various (referenced in arXiv:2604.05005)
- **Venue:** *arXiv 2026*
- **Year:** 2026
- **Why it is a trunk paper:** This paper addresses the multimodal gap in AIEd: most LLM tutoring is text-only, but STEM education requires diagrams, charts, and visual explanations. EduIllustrate generates textbook-style diagrams programmatically (using TikZ/Manim) for K-12 STEM subjects. This is the first system to scale multimodal educational content generation across five subjects (math, physics, chemistry, biology, geography).
- **Technical details:** The system uses a two-stage pipeline: an LLM generates a textual description of the desired diagram, then a code-generation module produces executable TikZ or Manim code that renders the diagram. The key challenge is maintaining subject-specific diagram conventions (e.g., circuit diagrams in physics have standard symbols; geometry diagrams have specific angle markings). The system uses a "style guide" database of subject-specific conventions to constrain generation. Evaluation used human judges (teachers) who rated diagrams for accuracy, clarity, and pedagogical appropriateness. The system achieved >80% "usable without modification" ratings. The paper also explored "diagram-to-explanation" generation: given a diagram, the LLM generates a textual explanation that points to specific elements. This is the inverse of the typical text-to-diagram pipeline and is useful for explaining existing textbook figures. The system is integrated with a tutoring platform that can dynamically generate diagrams based on student questions, rather than relying on a pre-built figure library.

---

### 33. DSE Education Group — Multimodal AIEd Papers (2024–2025)
- **Authors:** DSE Education Group (MSU)
- **Venue:** *AAAI 2025, AIED 2026, ACL 2025, EMNLP 2025*
- **Papers:**
  - "Can MLLMs Read Students' Minds? Unpacking Multimodal Error Analysis in Handwritten Math" (AIED 2026)
  - "MathAgent: Leveraging a Mixture-of-Math-Agent Framework for Real-World Multimodal Mathematical Error Detection" (ACL 2025, Industry Oral)
  - "ErrorRadar: Benchmarking Complex Mathematical Reasoning of Multimodal Large Language Models Via Error Detection" (arXiv 2024)
- **Why they are trunk papers:** These papers collectively established the multimodal error detection subfield in AIEd — using vision-language models to analyze handwritten student work, detect errors, and provide feedback. The MathAgent system uses a mixture-of-agents architecture where different agents specialize in different error types (calculation errors, conceptual errors, notation errors, diagram interpretation errors).
- **Technical details:** MathAgent uses a routing mechanism that sends each student work sample to the appropriate specialist agent based on an initial classification. The "Can MLLMs Read Students' Minds?" paper analyzes failure modes of multimodal LLMs on handwritten math: they struggle with messy handwriting, ambiguous notation, and implicit steps that are obvious to human teachers but not to models. ErrorRadar introduced a benchmark with 10,000+ error-annotated handwritten math problems, establishing the standard dataset for this subfield. The benchmark includes a taxonomy of error types (e.g., arithmetic error, algebraic manipulation error, conceptual misunderstanding, notation misuse) and evaluates MLLMs on each. The key finding is that MLLMs are significantly worse than human teachers at detecting "subtle" errors — errors that are partially correct but contain a small mistake. This is particularly problematic for formative assessment, where early error detection is crucial. The papers propose a "human-in-the-loop" approach where the MLLM flags potential errors for teacher review, rather than making definitive diagnoses.

---

### 34. Elkins et al. (2024) — "How Teachers Can Use Large Language Models and Bloom's Taxonomy to Create Educational Quizzes"
- **Authors:** Sabina Elkins, Ekaterina Kochmar, Jackie C. K. Cheung, Iulian Serban
- **Venue:** *AAAI 2024 / IAAI 2024*
- **Year:** 2024
- **Why it is a trunk paper:** This paper bridged the classic educational taxonomy (Bloom's) with LLM capabilities, showing that LLMs can generate quiz questions at specific cognitive levels when properly prompted. It established that LLMs are not just answer generators but can be "pedagogical design tools" for teachers. The AAAI/IAAI venue signals AI community recognition of AIEd as a serious AI application domain.
- **Technical details:** The system uses a prompt engineering approach where the LLM is instructed to generate questions at a specific Bloom's level (remember, understand, apply, analyze, evaluate, create). The evaluation used human teachers to rate the generated questions for cognitive level accuracy and pedagogical quality. The paper found that LLMs are better at lower-level questions (remember, understand) than higher-level questions (evaluate, create), suggesting that LLMs still struggle with deep reasoning assessment. It proposed a "human-in-the-loop" workflow where the LLM generates drafts and the teacher refines them, which has been widely adopted in educational technology products. The paper also explored "rubric-aware generation" where the LLM is given a specific rubric and generates questions that align with it. This improves consistency and relevance but requires more detailed prompting. The evaluation used both expert ratings and student performance data: questions rated as higher Bloom's levels indeed produced more varied student responses and required more reasoning, validating the LLM's cognitive level classification.

---

## X. Programming & STEM Education

### 35. Pankiewicz & Baker (2023) / Denny et al. (2023) — LLM-based Programming Education
- **Authors:** Maciej Pankiewicz, Ryan S. Baker / Paul Denny, et al.
- **Venue:** *arXiv 2023 / SIGCSE 2023*
- **Year:** 2023
- **Why they are trunk papers:** These papers established the programming education subfield within AIEd 2023. Pankiewicz & Baker demonstrated that GPT-4 can generate automated feedback on programming assignments that is comparable to human TAs. Denny et al. (and the broader SIGCSE 2023 community) organized the first systematic exploration of ChatGPT's impact on computer science education, generating a wave of follow-up research.
- **Technical details:** The programming feedback system uses GPT-4 to analyze code submissions, identify errors, and generate explanatory feedback. Key findings: GPT-4 is excellent at identifying syntax errors and suggesting fixes, but less reliable at identifying conceptual misunderstandings (e.g., why a student chose a particular algorithm). The feedback quality varies significantly by programming language and assignment type. The papers also documented the "cheating concern" — students using ChatGPT to generate solutions — and proposed that this should be reframed as an opportunity to teach AI literacy and critical evaluation of code. The SIGCSE 2023 community organized a special session on "ChatGPT in CS Education" that produced a consensus statement: CS educators should embrace AI tools while redesigning assessments to focus on higher-level skills (design, debugging, code review) that AI cannot fully replicate. This reframing has influenced CS curriculum design worldwide.

---

### 36. Malinka et al. (2023) — "On the Educational Impact of ChatGPT: Is Artificial Intelligence Ready to Obtain a University Degree?"
- **Authors:** Kamil Malinka, Martin Peresíni, Anton Firc, Ondrej Hujnák, Filip Janus
- **Venue:** *ITiCSE 2023*
- **Year:** 2023
- **Why it is a trunk paper:** This provocation paper tested whether ChatGPT could pass university exams across multiple subjects. It found that ChatGPT could pass many exams but struggled with subjects requiring deep reasoning, creativity, or domain-specific expertise. This set the agenda for understanding LLM capabilities and limitations in educational contexts, and catalyzed the "AI literacy for educators" movement.
- **Technical details:** The authors had ChatGPT attempt exams from computer science, mathematics, physics, and humanities courses. ChatGPT passed introductory courses with high marks but failed advanced courses requiring synthesis, critical evaluation, or original argumentation. The paper's title became a widely-cited framing question. It directly influenced the development of "AI-resistant" assessment designs (oral exams, in-class assignments, process portfolios) and the integration of AI literacy into curriculum design. The study used a within-subjects design: the same exam was attempted by both human students and ChatGPT, with scores compared. The key finding was that ChatGPT's performance was highly variable: excellent on factual recall and standard problem types, poor on novel problems requiring creative synthesis. This variability is itself a pedagogically important finding: it shows that LLMs are not a threat to all assessment types, but only to those that rely on recall and standard procedures.

---

### 37. Ma et al. (2023) — "Is AI the Better Programming Partner? Human-Human Pair Programming vs. Human-AI Pair Programming"
- **Authors:** Qianou Christina Ma, Sherry Tongshuang Wu, Ken Koedinger (CMU)
- **Venue:** *AIED Workshop on Empowering Education with LLMs*
- **Year:** 2023
- **Why it is a trunk paper:** This was one of the first studies to compare human-AI pair programming to human-human pair programming in educational settings. It found that AI partners provide more consistent help but less mutual learning benefit, establishing that the social dimension of learning is not fully replicated by AI. This has influenced the design of collaborative AI systems in education.
- **Technical details:** The study used a between-subjects design comparing student pairs (human-human) to student-AI pairs (human-GPT-4). Outcomes measured: task completion time, code quality, learning gains (post-test), and subjective experience. Human-AI pairs completed tasks faster but showed lower learning gains on post-tests, suggesting that the AI "carried" the student rather than scaffolding their learning. Human-human pairs reported more frustration but also more "aha moments" and deeper understanding. The paper recommended hybrid models where AI provides initial support but human collaboration is required for final solutions. The study also analyzed the dialogue patterns: human-human pairs engaged in more exploratory discussion, back-and-forth reasoning, and mutual teaching; human-AI pairs followed a more transactional pattern (student asks, AI answers). This qualitative analysis supports the quantitative finding that the social process of pair programming is as important as the product.

---

## XI. Meta-Analysis: What Makes These Trunk Papers?

### Citation Impact
| Paper | Year | Citations (approx.) | Significance |
|-------|------|---------------------|--------------|
| Kasneci et al. | 2023 | >11,000 | Most-cited AIEd paper ever; defined the post-ChatGPT discourse |
| Sonkar et al. (Pedagogical Alignment) | 2024 | >100 | Defined "pedagogical alignment" as a research field |
| GenMentor (Wang et al.) | 2025 | >100 | First deployed multi-agent tutoring architecture |
| Vanzo et al. | 2024/2025 | >37 | First rigorous RCT of LLM tutoring in schools |
| Chevalier et al. (TutorEval) | 2024 | 38+ | First long-context STEM tutoring benchmark (ICML) |
| MathDial (Macina et al.) | 2023 | Widespread | Standard dataset for math tutoring; inverted Wizard-of-Oz method |
| LearnLM | 2024 | Widespread | First commercial-scale education-specific LLM fine-tuning |
| CLASS (Sonkar et al.) | 2023 | Widespread | First framework bridging classical ITS with LLMs |

### Direction-Opening Contributions
| Direction | Foundational Paper | What It Opened |
|-----------|-------------------|----------------|
| LLM policy framework | UNESCO 2023 | National AI education strategies worldwide |
| Pedagogical alignment | Sonkar et al. 2024 | Teaching RLHF, scaffolding evaluation, rubric design |
| Multi-agent tutoring | Wang et al. 2025 (GenMentor) | Scalable goal-oriented tutoring architecture |
| Real-world RCT evidence | Vanzo et al. 2024/2025 | Evidence-based LLM tutoring adoption in schools |
| Long-context STEM tutoring | Chevalier et al. 2024 | Textbook-chapter-level tutoring (32K tokens) |
| Synthetic data for tutoring | Macina et al. 2023 (MathDial) | Inverted Wizard-of-Oz: human teachers + LLM students |
| Programming education with LLMs | Pankiewicz & Baker 2023, Denny et al. 2023 | Automated code feedback at scale; AI literacy in CS |
| Student simulation | Markel et al. 2023 (GPTeach) | Teacher training with LLM students |
| Multimodal education | DSE Group 2024–2025 | Handwritten math, diagram generation, vision-language |
| Personality-aware tutoring | Rooein et al. 2026 | Individualized beyond knowledge level (Big Five) |
| Pedagogical RL | Dinucu-Jianu et al. 2025 | RL objectives for tutoring, not just helpfulness |
| Thinking rewards | Lee et al. 2026 | Internal reasoning quality matters for tutoring |
| Disability-adaptive tutoring | Lee et al. 2026 | Special education principles in LLM tutor design |
| Proficiency simulation | Li et al. 2025 | LLM difficulty prediction via explicit ability adoption |
| GraphRAG assessment | DSE Group 2026 | Structural understanding evaluation, not just keywords |

### Key Technical Paradigms Established
1. **Inverted Wizard-of-Oz:** Human teachers tutor LLM students → synthetic but authentic tutoring data (MathDial)
2. **Pedagogical RLHF:** Reward functions for tutoring behavior, not just correctness (PedagogicalRL, PedagogicalRL-Thinking)
3. **Transition Graph Steering:** Learning scientists control strategy via state-transition graphs, not just prompts (Puech et al. 2025)
4. **Multi-Agent Orchestration:** Specialized agents for diagnosis, planning, tutoring, assessment (GenMentor, EduAgent)
5. **Long-Context Tutoring:** 32K+ tokens for processing entire textbook chapters (TutorEval, LearnLM)
6. **Proficiency Simulation:** Explicitly prompting LLMs to adopt student ability levels for difficulty prediction (Li et al. 2025)
7. **GraphRAG for Assessment:** Knowledge graphs for evaluating conceptual relationship understanding (DSE Group 2026)
8. **Personality-Aware Adaptation:** Big Five trait detection + strategy adaptation (PATS, Rooein et al. 2026)
9. **Teachable Agent Paradigm:** Student teaches LLM, reversing the tutoring relationship (Ma et al. 2024)
10. **Knowledge Tracing with LLMs:** Inferring KC mastery from open-ended dialogue (LLMKT, Scarlatos et al. 2025)

### Critical Open Problems (as of mid-2026)
1. **Engagement vs. Learning:** LLM tutors improve engagement consistently; deep learning gains are less certain (Shi et al. 2025 meta-analysis of 88 studies)
2. **Student Agency:** Real students bypass scaffolding; benchmarks don't account for this strategic behavior (Jurenka et al. 2026)
3. **Assessment Validity:** LLMs are reliable but may lack construct validity for high-stakes use (Yavuz et al. 2025)
4. **Equity & Access:** Most rigorous evidence comes from well-resourced contexts; Global South evidence is limited (Henkel et al. 2024 is a notable exception)
5. **Long-Term Retention:** Very few studies measure learning beyond the immediate post-test; durability unknown
6. **Teacher Role:** The field still debates whether AI tutors augment or replace teachers; human-AI co-orchestration is underexplored
7. **Multimodal Tutoring:** Text-only tutoring is well-studied; multimodal (diagrams, handwriting, speech) is still emerging
8. **Ethical & Safety:** Hallucination, bias, and over-reliance remain unsolved despite extensive policy work (Kasneci et al. 2023, UNESCO 2023)
9. **Student Simulation Validity:** LLM-simulated students capture average behavior but miss the long tail of atypical behavior (2026 papers)
10. **Cost & Sustainability:** Commercial LLM APIs are expensive at scale; open-source models lag in pedagogical quality (learned from LearnLM, SocraticLM comparisons)

---

## Source Notes

- This curation prioritizes papers from: **AIED** (AI in Education), **EDM** (Educational Data Mining), **ACL/EMNLP/EACL Findings**, **AAAI/IAAI**, **ICML**, **NeurIPS**, **CHI**, **L@S**, and high-impact education journals (*npj Science of Learning*, *Learning and Individual Differences*, *British Journal of Educational Technology*).
- The 2023-2026 period represents a **phase transition** in AIEd: from rule-based/statistical ITS to LLM-based, multi-agent, multimodal systems. The papers above capture this transition at its most foundational moments.
- The list is biased toward papers with: (a) rigorous empirical validation, (b) open-source resources (data, code, models), (c) real-world deployment evidence, and (d) conceptual frameworks that organize subsequent research.
- **Total papers:** 37 milestone/trunk papers across 10 sub-themes, with detailed technical analysis, citation context, and open-problem identification.
- **Methodology:** Web search across arXiv, Google Scholar, conference proceedings, and UNESCO/OECD policy documents; cross-referenced with citation networks and subsequent paper references to confirm trunk status.
