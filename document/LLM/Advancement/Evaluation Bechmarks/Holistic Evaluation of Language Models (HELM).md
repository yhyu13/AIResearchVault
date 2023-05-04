A language model takes in text and produces text:

![](https://crfm.stanford.edu/helm/latest/images/language-model-helm.png)

Despite their simplicity, language models are increasingly functioning as the foundation for almost all language technologies from question answering to summarization. But their immense capabilities and risks are not well understood. Holistic Evaluation of Language Models (HELM) is a living benchmark that aims to improve the transparency of language models.

1.  **Broad coverage and recognition of incompleteness**. We define a taxonomy over the scenarios we would ideally like to evaluate, select scenarios and metrics to cover the space and make explicit what is missing.
    
    ![](https://crfm.stanford.edu/helm/latest/images/taxonomy-scenarios.png)
    
2.  **Multi-metric measurement**. Rather than focus on isolated metrics such as accuracy, we simultaneously measure multiple metrics (e.g., accuracy, robustness, calibration, efficiency) for each scenario, allowing analysis of tradeoffs.
    
    ![](https://crfm.stanford.edu/helm/latest/images/scenarios-by-metrics.png)
    
3.  **Standardization**. We evaluate all the models that we have access to on the same scenarios with the same adaptation strategy (e.g., prompting), allowing for controlled comparisons. Thanks to all the companies for providing API access to the limited-access and closed models and [Together](https://together.xyz/) for providing the infrastructure to run the open models.
4.  **Transparency**. All the scenarios, predictions, prompts, code are available for further analysis on this website. We invite you to click below to explore!