# BCI Milestone Papers (2023 – Mid-2026)

> Curated selection of the most important, foundational, and breakthrough papers in Brain-Computer Interfaces from 2023 to July 2026.
> Focus: widely cited, opened new directions, or considered transformative. Minor incremental works are excluded.
> Coverage: speech/language neuroprosthetics, motor restoration, visual prosthetics, non-invasive decoding, clinical translation, and independent long-term use.

---

## 1. Speech & Language Neuroprosthetics

The most concentrated cluster of breakthroughs in this period. The field moved from proof-of-concept decoding to conversational-speed, bilingual, voice-synthesizing, and even inner-speech-capable systems.

### 1.1 Willett et al. (2023) — High-Performance Speech Neuroprosthesis (Intracortical)

- **Title:** A high-performance speech neuroprosthesis
- **Authors:** Francis R. Willett, Erin M. Kunz, Chaofei Fan, et al. (Stanford / BrainGate)
- **Venue:** *Nature* 620, 1031–1036 (2023)
- **Year:** 2023
- **Why milestone:** First large-vocabulary intracortical speech BCI. Decoded attempted speech at ~62 words per minute with 9.1% WER on a 50-word vocabulary and 23.8% WER on a 125,000-word vocabulary using microelectrode arrays in the motor cortex. This demonstrated that high-performance, generalizable speech decoding was possible from intracortical recordings, setting the performance benchmark for the field.

### 1.2 Metzger et al. (2023) — Speech Decoding + Avatar Control (ECoG)

- **Title:** A high-performance neuroprosthesis for speech decoding and avatar control
- **Authors:** Sean L. Metzger, Kaylo T. Littlejohn, Alexander B. Silva, et al. (UCSF Chang Lab)
- **Venue:** *Nature* 620, 1037–1046 (2023)
- **Year:** 2023
- **Why milestone:** Simultaneously demonstrated ECoG-based speech decoding at ~78 WPM (median) with 25% WER on a 1,024-word vocabulary, real-time avatar facial-animation synthesis, and personalized voice reconstruction. Showed that a less-invasive ECoG platform could rival intracortical performance while enabling multimodal communication outputs (text + voice + avatar).

### 1.3 Card et al. (2024) — Rapidly Calibrating Speech Neuroprosthesis (NEJM)

- **Title:** An accurate and rapidly calibrating speech neuroprosthesis
- **Authors:** Nicholas S. Card, Maitreyee Wairagkar, Carrina Iacobacci, et al. (UC Davis / BrainGate)
- **Venue:** *New England Journal of Medicine* 391, 609–618 (2024)
- **Year:** 2024
- **Why milestone:** Solved a critical practical barrier: calibration time. Demonstrated a speech BCI that could achieve high accuracy with minimal daily recalibration, moving the technology from lab-only demonstrations toward a practical device that could be used routinely by patients without extensive researcher involvement.

### 1.4 Wairagkar et al. (2025) — Instantaneous Voice-Synthesis Neuroprosthesis

- **Title:** An instantaneous voice-synthesis neuroprosthesis
- **Authors:** Maitreyee Wairagkar, Nicholas S. Card, Tyler Singer-Clark, et al. (UC Davis / BrainGate)
- **Venue:** *Nature* (2025)
- **Year:** 2025
- **Why milestone:** Moved beyond text output to real-time audible voice synthesis directly from neural activity. This is a qualitative shift from "reading text on a screen" to "hearing the person speak," restoring the social and emotional dimensions of conversation. Marks the convergence of speech BCI with speech-synthesis AI.

### 1.5 Littlejohn et al. (2025) — Streaming Brain-to-Voice Neuroprosthesis

- **Title:** A streaming brain-to-voice neuroprosthesis to restore naturalistic communication
- **Authors:** Kaylo T. Littlejohn, Cheol Jun Cho, Jessie R. Liu, et al. (UCSF Chang Lab)
- **Venue:** *Nature Neuroscience* (2025)
- **Year:** 2025
- **Why milestone:** Achieved streaming audio output in 80-millisecond increments, enabling truly conversational turn-taking, interruption, and prosody. Prior systems had batch delays that broke social interaction dynamics. This paper restored the *interactional* dimension of speech, not just the semantic content.

### 1.6 Kunz et al. (2025) — Inner Speech Decoding from Motor Cortex (Cell)

- **Title:** Inner speech in motor cortex and implications for speech neuroprostheses
- **Authors:** Erin M. Kunz, Benyamin Abramovich Krasa, Foram Kamdar, et al. (Stanford / BrainGate)
- **Venue:** *Cell* 188(17), 4658–4673 (2025)
- **Year:** 2025
- **Why milestone:** Showed that inner (covert) speech is robustly represented in the motor cortex and can be decoded in real time. This opens the door to BCIs that do not require the user to physically attempt speech — critical for patients with complete speech paralysis or locked-in syndrome. Also established privacy-protective strategies to prevent unintentional decoding of private thoughts.

### 1.7 Silva et al. (2024) — Bilingual Speech Neuroprosthesis

- **Title:** A bilingual speech neuroprosthesis driven by cortical articulatory representations shared between languages
- **Authors:** Alexander B. Silva, Jessie R. Liu, Sean L. Metzger, et al. (UCSF Chang Lab)
- **Venue:** *Nature Biomedical Engineering* (2024)
- **Year:** 2024
- **Why milestone:** First demonstration of bilingual speech decoding (English/Spanish) from a single neural decoder. The brain uses shared articulatory representations across languages, enabling transfer learning and eliminating the need for separate language-specific decoders. Critical for the >50% of the world that is bilingual.

### 1.8 Tang et al. (2023) — Non-Invasive Continuous Language Decoding from fMRI

- **Title:** Semantic reconstruction of continuous language from non-invasive brain recordings
- **Authors:** Jerry Tang, Amanda LeBel, Shailee Jain, et al. (UT Austin)
- **Venue:** *Nature Neuroscience* 26, 858–866 (2023)
- **Year:** 2023
- **Why milestone:** First non-invasive decoder that reconstructed continuous, intelligible language from single-trial fMRI recordings. Decoded perceived speech, imagined speech, and even silent videos into meaningful word sequences. Demonstrated that invasive surgery is not strictly necessary for language BCI, though latency remains a limitation. Broke the "small vocabulary set" barrier for non-invasive approaches.

---

## 2. Motor Restoration & Brain-Spine Interfaces

### 2.1 Lorach et al. (2023) — Brain-Spine Interface for Natural Walking

- **Title:** Walking naturally after spinal cord injury using a brain–spine interface
- **Authors:** Henri Lorach, Andrea Galvez, Valeria Spagnolo, et al. (EPFL / CHUV / CEA / NeuroRestore)
- **Venue:** *Nature* 618, 126–133 (2023)
- **Year:** 2023
- **Why milestone:** A landmark in neuroengineering: a fully implanted, wireless "digital bridge" between the brain and spinal cord restored natural, volitional walking in a person with chronic tetraplegia. The system decoded cortical movement intentions and delivered epidural electrical stimulation to the spinal cord. Remarkably, neurorehabilitation supported by the BSI led to neurological recovery — the participant regained walking ability with crutches even when the device was switched off. This is the most significant BCI-based motor restoration result to date.

### 2.2 Willsey et al. (2025) — Finger Decoding & Quadcopter Game Control

- **Title:** A high-performance brain–computer interface for finger decoding and quadcopter game control in an individual with paralysis
- **Authors:** Matthew S. Willsey, Nishal P. Shah, Donald T. Avansino, et al. (Stanford / BrainGate)
- **Venue:** *Nature Medicine* 31, 96–104 (2025)
- **Year:** 2025
- **Why milestone:** Achieved continuous, high-DOF control of individual finger groups (4 DOF including 2D thumb) from intracortical recordings, with performance comparable to non-human primate studies. Used this to control a virtual quadcopter game, demonstrating that BCIs can address recreational and social needs (not just ADLs) of paralyzed individuals. Shows the path toward dexterous robotic-hand control.

---

## 3. Visual Restoration & Sensory Prosthetics

### 3.1 Holz et al. (2025) — PRIMA Subretinal Photovoltaic Implant (NEJM)

- **Title:** Subretinal Photovoltaic Implant to Restore Vision in Geographic Atrophy Due to AMD
- **Authors:** Frank G. Holz, Yves Le Mer, Mahi Muqit, et al. (Science Corporation / Stanford / multiple sites)
- **Venue:** *New England Journal of Medicine* (2025)
- **Year:** 2025
- **Why milestone:** The first large-scale, peer-reviewed clinical trial (38 participants, 17 sites, 5 countries) demonstrating that a BCI-class retinal implant (PRIMA) restores functional central vision in patients blinded by geographic atrophy from AMD. 80% of patients achieved meaningful acuity improvement; 84% regained ability to read letters/numbers/words. Represents the most advanced vision-BCI nearing commercialization, with CE mark and FDA approval pathways underway. A paradigm shift from slowing disease to actively restoring lost vision.

---

## 4. Independent Long-Term Use & Clinical Translation

### 4.1 Card et al. (2026) — Long-Term Independent Speech + Cursor BCI Use

- **Title:** Long-term independent use of an intracortical brain–computer interface for speech and cursor control
- **Authors:** Nicholas S. Card, Tyler Singer-Clark, Hamza Peracha, et al. (UC Davis / BrainGate)
- **Venue:** *Nature Medicine* (2026)
- **Year:** 2026
- **Why milestone:** The single most important clinical translation paper to date. Demonstrated a man with ALS using a multimodal intracortical BCI independently at home for 19 months and >3,800 hours, communicating >180,000 sentences (~56 WPM) and operating his personal computer (speech as keyboard, cursor as mouse) without researcher supervision. Transformer-based decoder achieved 99.2% word accuracy on a 125,000-word vocabulary with minimal daily calibration. Proves that intracortical BCIs are ready for real-world, independent deployment.

### 4.2 Mitchell et al. (2023) — Synchron Stentrode Safety Trial (JAMA Neurology)

- **Title:** Assessment of safety of a fully implanted endovascular brain–computer interface for severe paralysis in 4 patients: the stentrode with thought-controlled digital switch (SWITCH) study
- **Authors:** Peter Mitchell, Stephen C. M. Lee, Philip E. Yoo, et al. (Synchron / Royal Melbourne Hospital)
- **Venue:** *JAMA Neurology* 80, 270–278 (2023)
- **Year:** 2023
- **Why milestone:** Established the safety and feasibility of an endovascular (via blood vessel) BCI, which avoids open-brain surgery. No serious adverse events or vessel occlusions at 12 months in 4 patients with severe paralysis. This minimally invasive approach dramatically expands the eligible patient population and reduces the risk profile that has limited invasive BCI adoption.

---

## 5. Hardware, Neural Decoding & Emerging Capabilities

### 5.1 Oxley et al. (2025) — 10-Year Journey of Endovascular BCI

- **Title:** A 10-year journey towards clinical translation of an implantable endovascular BCI
- **Authors:** Thomas J. Oxley (Synchron)
- **Venue:** *Journal of Neural Engineering* 22(1), 013001 (2025)
- **Year:** 2025
- **Why milestone:** Comprehensive retrospective on the Synchron Stentrode's decade-long development, documenting the engineering, regulatory, and clinical milestones that led to the first endovascular BCI human trials. Essential reading for understanding the translation pathway from bench to bedside for novel BCI form factors.

### 5.2 Hettick et al. (2025) — Minimally Invasive High-Density Cortical Microelectrode Arrays

- **Title:** Minimally invasive implantation of scalable high-density cortical microelectrode arrays for multimodal neural decoding and stimulation
- **Authors:** M. Hettick, E. Ho, A. J. Poole, et al.
- **Venue:** *Nature Biomedical Engineering* (2025)
- **Year:** 2025
- **Why milestone:** Addresses the fundamental engineering challenge of how to place high-density electrodes with minimal surgical trauma. Demonstrates a scalable, minimally invasive approach to cortical microelectrode array implantation that supports both recording and stimulation, paving the way for higher-channel-count BCIs without proportional increases in surgical risk.

### 5.3 Singer-Clark et al. (2024) — Speech Motor Cortex for Cursor Control

- **Title:** Speech motor cortex enables BCI cursor control and click
- **Authors:** Tyler Singer-Clark, Xianda Hou, Nicholas S. Card, et al. (UC Davis / BrainGate)
- **Venue:** *Journal of Neural Engineering* 22, 036015 (2024)
- **Year:** 2024
- **Why milestone:** Surprised the field by showing that the *same* speech motor cortex electrodes could simultaneously control a computer cursor and produce clicks, without requiring separate motor cortex implants. This multimodal reuse of a single brain region dramatically simplifies the surgical and hardware requirements for practical BCIs that need both communication and computer control.

---

## 6. Non-Invasive & Hybrid BCIs

### 6.1 Zhang et al. (2024) — Decoding Continuous Character-Based Language from fMRI

- **Title:** Decoding Continuous Character-based Language from Non-invasive Brain Recordings
- **Authors:** Cenyuan Zhang, Xiaoqing Zheng, Ruicheng Yin, et al. (Fudan / Shanghai)
- **Venue:** arXiv:2403.11183 (2024); also broader fMRI decoding literature
- **Year:** 2024
- **Why milestone:** Extended the Tang et al. (2023) non-invasive language decoding framework with a character-based decoder that better captures the semantic structure of continuous language, particularly for character-based languages like Chinese. Demonstrated cross-subject generalization, which is a major challenge for non-invasive BCIs. Keeps the non-invasive language BCI thread active as an alternative to surgical implants.

### 6.2 Luo et al. (2023) — Stable Chronic Speech BCI Without Recalibration

- **Title:** Stable decoding from a speech BCI enables control for an individual with ALS without recalibration for 3 months
- **Authors:** S. Luo, M. Angrick, C. Coogan, et al. (multiple institutions)
- **Venue:** *Advanced Science* 10, e2304853 (2023)
- **Year:** 2023
- **Why milestone:** Demonstrated three months of stable ECoG speech decoding without recalibration in an ALS patient. Neural signal drift is one of the biggest barriers to long-term BCI use; this paper showed that stable decoders are achievable over extended periods, a critical stepping stone to practical at-home deployment.

---

## Summary Table

| # | Title | Authors | Venue | Year | Theme |
|---|-------|---------|-------|------|-------|
| 1 | A high-performance speech neuroprosthesis | Willett et al. | *Nature* | 2023 | Speech (Intracortical) |
| 2 | A high-performance neuroprosthesis for speech decoding and avatar control | Metzger et al. | *Nature* | 2023 | Speech (ECoG) |
| 3 | An accurate and rapidly calibrating speech neuroprosthesis | Card et al. | *NEJM* | 2024 | Speech (Clinical) |
| 4 | An instantaneous voice-synthesis neuroprosthesis | Wairagkar et al. | *Nature* | 2025 | Speech (Voice) |
| 5 | A streaming brain-to-voice neuroprosthesis | Littlejohn et al. | *Nat. Neurosci.* | 2025 | Speech (Streaming) |
| 6 | Inner speech in motor cortex | Kunz et al. | *Cell* | 2025 | Speech (Inner) |
| 7 | A bilingual speech neuroprosthesis | Silva et al. | *Nat. Biomed. Eng.* | 2024 | Speech (Bilingual) |
| 8 | Semantic reconstruction of continuous language from non-invasive brain recordings | Tang et al. | *Nat. Neurosci.* | 2023 | Non-invasive Language |
| 9 | Walking naturally after spinal cord injury using a brain–spine interface | Lorach et al. | *Nature* | 2023 | Motor Restoration |
| 10 | A high-performance BCI for finger decoding and quadcopter game control | Willsey et al. | *Nat. Med.* | 2025 | Finger/Motor Control |
| 11 | Subretinal Photovoltaic Implant to Restore Vision in Geographic Atrophy | Holz et al. | *NEJM* | 2025 | Visual Restoration |
| 12 | Long-term independent use of an intracortical BCI for speech and cursor control | Card et al. | *Nat. Med.* | 2026 | Clinical Translation |
| 13 | Assessment of safety of a fully implanted endovascular BCI (SWITCH) | Mitchell et al. | *JAMA Neurol.* | 2023 | Endovascular Safety |
| 14 | A 10-year journey towards clinical translation of an implantable endovascular BCI | Oxley et al. | *J. Neural Eng.* | 2025 | Endovascular History |
| 15 | Minimally invasive implantation of scalable high-density cortical microelectrode arrays | Hettick et al. | *Nat. Biomed. Eng.* | 2025 | Hardware |
| 16 | Speech motor cortex enables BCI cursor control and click | Singer-Clark et al. | *J. Neural Eng.* | 2024 | Multimodal Reuse |
| 17 | Decoding Continuous Character-based Language from Non-invasive Brain Recordings | Zhang et al. | arXiv | 2024 | Non-invasive Decoding |
| 18 | Stable decoding from a speech BCI without recalibration for 3 months | Luo et al. | *Adv. Sci.* | 2023 | Stability |

---

> **Curator's note:** The period 2023–2026 represents a phase transition for BCI research. The field has moved from "can we decode a few words?" to "can a paralyzed person work full-time, speak conversationally, and control a computer independently at home for years?" The answer is increasingly yes. The remaining challenges are regulatory, commercial, and — above all — about ensuring equitable access to these life-changing technologies.
> 
> Last updated: July 2026
