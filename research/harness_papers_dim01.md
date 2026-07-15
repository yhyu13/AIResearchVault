## Dimension 1: Automated Harness Evolution & Meta-Learning

### Key Findings
- **The Last Harness You'll Ever Build** (arXiv 2026-05-01) proposes a two-level framework: (1) Harness Evolution Loop optimizes a worker agent's harness for a single task via Worker Agent → Evaluator Agent → Evolution Agent cycle; (2) Meta-Evolution Loop optimizes the evolution blueprint itself across diverse tasks. The framework formalizes Agent = Model + Harness and maps to meta-learning.
- **Coreset Selection**: DPP-Greedy selects diverse, challenging tasks from past trajectories.
- **Self-preference**: RHO uses agent's own pairwise trajectory ranking to select best harness proposals without validation labels.

### Major Players & Sources
- Authors: Not explicitly listed in abstract; from arXiv 2604.21003
- Related: OpenAI (Codex), Anthropic (Claude Code), SylphAI (AdaL)

### Trends & Signals
- Shift from manual harness engineering to automated harness engineering
- Meta-learning formulation for harness evolution blueprints
- No empirical results yet in the published version; theoretical framework only

### Controversies & Conflicting Claims
- The paper claims to automate "the design of the automation itself" but provides no empirical validation of the Meta-Evolution Loop
- Contrast with RHO (Paper 8) which has full empirical results but narrower scope (no meta-learning)

### Recommended Deep-Dive Areas
- Empirical validation of meta-evolution across task domains
- Comparison with RHO's self-preference approach
- Convergence guarantees for harness evolution loops
