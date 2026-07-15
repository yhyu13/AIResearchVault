# Cross-Paper Insights: Harness System Architecture 2025–2026

## Insight 1: The Agent = Model + Harness Equation Is Now Formalized
- **Derived From**: Papers 1, 2, 3, 5, 6
- **Rationale**: Multiple independent works (The Last Harness, Life-Harness, Harness-Bench, HarnessAudit, Interplay) explicitly define Agent = Model + Harness as a formal decomposition. This represents a maturation of the field from viewing harnesses as "scaffolding" to treating them as a first-class optimization target.
- **Implications**: Future agent research must report results at the model–harness configuration level, not attribute performance to the base model alone.
- **Confidence**: high

## Insight 2: Runtime Interface Adaptation Is a Viable Alternative to Model Training
- **Derived From**: Papers 2, 5, 8
- **Rationale**: Life-Harness (Paper 2) shows 88.5% relative improvement across 18 models without weight updates. The Interplay (Paper 5) shows harness-aware post-training outperforms post-hoc harness application by 20+ points. RHO (Paper 8) achieves +19% on SWE-Bench Pro without validation labels. Together, these establish that harness optimization is not merely complementary to model training—it can be a substitute.
- **Implications**: For resource-constrained deployments, investing in harness engineering may yield higher ROI than model fine-tuning.
- **Confidence**: high

## Insight 3: Evaluation Infrastructure Is Fragmented and Benchmark-Specific
- **Derived From**: Papers 3, 4, 6, 7
- **Rationale**: Harness-Bench (106 tasks), SEAGym (Terminal-Bench 2.0 + HLE), HarnessAudit (210 tasks across 8 domains), and Orchard (SWE/GUI/Claw) each define their own task suites with minimal overlap. No unified harness evaluation protocol exists.
- **Implications**: The community needs a meta-benchmark or cross-suite transfer study to compare harness designs across domains.
- **Confidence**: high

## Insight 4: Safety and Capability Are Misaligned in Current Harnesses
- **Derived From**: Papers 3, 6
- **Rationale**: Harness-Bench shows completion scores vary by harness configuration, but HarnessAudit reveals that high completion does not imply safe execution. The best-performing system achieves only 0.32 overall safety score. Resource access violations dominate failure profiles.
- **Implications**: Agent deployment requires joint optimization of capability and safety metrics; optimizing for task completion alone is insufficient.
- **Confidence**: high

## Insight 5: Environment Layer Cost Is a Hidden Bottleneck for Scale
- **Derived From**: Papers 4, 7
- **Rationale**: Orchard demonstrates that managed sandbox services (E2B, Daytona) cost 10× more than self-hosted Kubernetes for large-scale RL training. SEAGym's batch-size ablation shows that harness update cost is non-monotonic—larger batches do not proportionally improve results.
- **Implications**: Open-source, self-hosted environment infrastructure is critical for democratizing agent research.
- **Confidence**: medium

## Insight 6: Self-Evolution Benchmarks Reveal Non-Monotonic Improvement Dynamics
- **Derived From**: Paper 4
- **Rationale**: SEAGym's replay diagnostics show that intermediate harness snapshots can regress (6/80 tasks after epoch 4) before recovering. This contradicts the assumption that more updates always improve performance.
- **Implications**: Harness evolution requires snapshot-level diagnostics and rollback mechanisms, not just final-epoch evaluation.
- **Confidence**: high

## Insight 7: Multi-Agent Harnesses Expand the Safety Risk Surface Exponentially
- **Derived From**: Papers 6
- **Rationale**: HarnessAudit-Bench shows that multi-agent configurations introduce information-flow violations and inter-agent boundary crossings that single-agent benchmarks miss. 69 unique role templates across 24 scenarios create combinatorial permission complexity.
- **Implications**: Multi-agent harness design must prioritize permission policies and information-flow constraints as first-class citizens.
- **Confidence**: high

## Insight 8: Meta-Learning Over Harness Evolution Blueprints Is the Next Frontier
- **Derived From**: Papers 1, 4
- **Rationale**: The Last Harness proposes a Meta-Evolution Loop that learns how to evolve harnesses across tasks. SEAGym provides the evaluation environment for such meta-learning. The two are complementary but not yet integrated.
- **Implications**: A combined system (meta-evolution blueprint + SEAGym evaluation) could enable zero-shot harness adaptation to novel domains.
- **Confidence**: exploratory
