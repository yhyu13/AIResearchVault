# What is active learning

```chat
> It looks like mean-filed has particular focus on improving the internally architecture of transformer. However, Large language models powered by transformer architecture often influenced by the prompting dataset we feed them. Have you heard garbage in garbage out? Can mean-field theory applied on improving the prompting quality as a preprocessing step?
```
You're right that "garbage in, garbage out" is an important principle to consider when working with large language models like Transformers. The quality of the input data and the prompts used can significantly impact the model's performance. While mean-field theory was originally developed to study systems with many interacting components, it's not directly applicable to the problem of improving prompting quality as a preprocessing step.

However, you can use other techniques and strategies to improve the quality of prompts and input data. Some of these strategies include:

1. **Data cleaning**: Before training or fine-tuning your model, ensure that your dataset is free from noise, inconsistencies, and irrelevant information. You can employ various preprocessing techniques, such as text normalization, tokenization, and stopword removal, to clean and preprocess the data.

2. **Data augmentation**: Augment your dataset with additional samples that can help the model learn more about the problem domain. Data augmentation techniques, such as synonym replacement, back-translation, or random word swapping, can be used to create diverse and high-quality samples.

3. **Prompt engineering**: Optimize the format and content of your prompts to elicit more accurate and useful responses from your model. This may involve using more explicit instructions, specifying the desired response format, or providing examples of correct answers.

4. **Curriculum learning**: Train your model in a sequential manner, starting with simpler tasks and gradually increasing the complexity of the tasks. This can help the model learn more effectively and improve its performance on more difficult tasks.

5. **Active learning**: Selectively sample examples from your dataset for training based on their informativeness or the model's uncertainty. This can help focus the model's learning on the most important or challenging examples, leading to better overall performance.

While mean-field theory may not be directly applicable to improving prompting quality, there are numerous other strategies and techniques that you can use to ensure the effectiveness of your input data and prompts. By combining these methods with a well-designed model architecture, you can achieve more accurate and useful results from your Transformer-based language models.

```chat
> Can you explain how active learning works in more detail?
```
Active learning is a semi-supervised learning approach that aims to improve model performance by selectively sampling and annotating the most informative or uncertain examples from a pool of unlabeled data. The main idea behind active learning is that a model can learn more effectively if it receives training data that is both diverse and challenging.

Here's a high-level overview of the active learning process:

1. **Initial training**: Train a model on an initial labeled dataset (which is usually small). This model is referred to as the base model.

2. **Unlabeled data pool**: Have a pool of unlabeled data points from which the model can select samples for annotation.

3. **Selection strategy**: Use a selection strategy to choose the most informative or uncertain examples from the unlabeled data pool. Common strategies include:
   - *Uncertainty sampling*: Select samples for which the model has the highest prediction uncertainty, typically measured by entropy, least confidence, or margin.
   - *Query-by-committee*: Train multiple models or use ensemble methods, and select samples for which the models disagree the most.
   - *Expected model change*: Choose samples that would lead to the largest change in the model's parameters if they were labeled and added to the training dataset.
   - *Expected error reduction*: Select samples that are expected to reduce the model's generalization error the most.

4. **Annotation**: Obtain ground-truth labels for the selected samples, either through human annotation or other means.

5. **Update the model**: Add the newly labeled samples to the training dataset and retrain or fine-tune the model. The updated model should perform better on the task due to the additional informative examples.

6. **Iterate**: Repeat the selection, annotation, and model update steps until a stopping criterion is met (e.g., a certain number of iterations, a performance threshold, or when the improvement in performance is no longer significant).

Active learning is particularly useful when labeling data is expensive or time-consuming, as it allows you to focus your annotation efforts on the most valuable examples. By iteratively updating the model with the most informative samples, active learning can help achieve better performance using fewer labeled data points compared to traditional supervised learning approaches.

# Active Learning Methods

```chat
> Could you give more concrete sample of potential unlabeled datasets that can be examples that match each point in the selection strategy? The unlabeled dataset should contains about Chain of Thought on mathematics problem.
```
Let's consider an unlabeled dataset that contains text samples representing a chain of thought on various mathematical problems. Each sample consists of a series of steps or explanations that describe the problem-solving process. The goal is to train a model to predict the next step in the problem-solving process given the current chain of thought.

For each selection strategy mentioned earlier, I'll provide a brief description of how it could be applied to this dataset:

1. **Uncertainty sampling**: In this strategy, you would select samples for which the model has the highest prediction uncertainty about the next step in the problem-solving process. For example, suppose you have the following two unlabeled samples:

   a. "Step 1: Simplify the equation by combining like terms. Step 2: ..."
   b. "Step 1: Calculate the determinant of the matrix. Step 2: ..."

   If the model is more uncertain about the next step in sample (b) than in sample (a), you would choose sample (b) for annotation.

2. **Query-by-committee**: In this approach, multiple models or an ensemble of models are used to make predictions. You would select samples for which the models disagree the most about the next step in the problem-solving process. For example, consider two models, A and B, and the following unlabeled sample:

   "Step 1: Calculate the partial derivatives. Step 2: ..."

   If model A predicts the next step as "Find the critical points by setting the partial derivatives to zero," while model B predicts "Calculate the second-order partial derivatives," you would select this sample for annotation due to the disagreement between the models.

3. **Expected model change**: In this strategy, you would choose samples that, if labeled and added to the training dataset, would lead to the most significant change in the model's parameters. For example, you might have an unlabeled sample that involves a rare mathematical concept or technique:

   "Step 1: Apply the Riemann-Roch theorem. Step 2: ..."

   If labeling this sample and incorporating it into the training dataset would result in a substantial change in the model's parameters, you would select this sample for annotation.

4. **Expected error reduction**: In this approach, you would select samples that are expected to reduce the model's generalization error the most. For example, consider an unlabeled sample that covers a topic the model has consistently struggled with:

   "Step 1: Perform integration by parts. Step 2: ..."

   If adding this sample to the training dataset is expected to significantly reduce the model's error on similar problems, you would choose this sample for annotation.

Each of these strategies can be applied to the unlabeled dataset to select the most informative examples for annotation, helping to improve the model's performance in predicting the next step in a chain of thought on mathematical problems.

# Python sample code for Acitve Learning Methods
```chat
> It seems like every each of these criteria can be programmed? Could you draft a python script that achieve selection strategy on a unlabeled match chain of thought dataset?
```
Certainly! Below is a simple Python script that demonstrates how to apply the uncertainty sampling selection strategy on an unlabeled dataset containing chains of thought for mathematical problems. This script uses the Hugging Face Transformers library to handle the Transformer model and tokenization. Make sure to install the library before running the script:

```bash
pip install transformers
```

Here's the Python script:

```python
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load a pre-trained Transformer model for the task
MODEL_NAME = "t5-small"  # You can replace this with a more suitable model for the task
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.eval()

# Unlabeled dataset containing chains of thought for mathematical problems
unlabeled_data = [
    "Step 1: Simplify the equation by combining like terms. Step 2: ...",
    "Step 1: Calculate the determinant of the matrix. Step 2: ...",
    "Step 1: Calculate the partial derivatives. Step 2: ...",
    # Add more samples as needed
]

def predict_next_step_uncertainty(model, tokenizer, text):
    inputs = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(inputs, num_return_sequences=1, output_scores=True)
    next_token_scores = outputs.scores[-1].squeeze()
    next_token_probs = torch.softmax(next_token_scores, dim=0)
    entropy = -torch.sum(next_token_probs * torch.log(next_token_probs))
    return entropy.item()

def select_most_uncertain(model, tokenizer, unlabeled_data):
    uncertainty_scores = [predict_next_step_uncertainty(model, tokenizer, text) for text in unlabeled_data]
    most_uncertain_index = uncertainty_scores.index(max(uncertainty_scores))
    return unlabeled_data[most_uncertain_index]

# Select the sample with the highest prediction uncertainty
selected_sample = select_most_uncertain(model, tokenizer, unlabeled_data)
print("Selected sample:", selected_sample)
```

This script demonstrates how to apply the uncertainty sampling strategy to a small dataset. You can replace the model, tokenizer, and unlabeled dataset with more appropriate choices for your specific task.

Please note that this is a simple example to illustrate the concept. In practice, you might need to fine-tune a model on a labeled dataset specific to your task, use more efficient methods to handle large unlabeled datasets, and adapt the script to other selection strategies as needed.

```chat
> What about there other criteria, could you also draft a python script for each of the them?
```
Sure! I will provide example Python scripts for each of the remaining selection strategies. Note that the following examples build upon the `unlabeled_data`, `MODEL_NAME`, `tokenizer`, and `model` variables from the previous script.

**2. Query-by-committee:**

For this example, we'll use two models and select the sample with the highest disagreement between their predictions. Remember to replace the model names with more suitable models for the task.

```python
MODEL_NAME_2 = "t5-small"  # Replace with another suitable model for the task

tokenizer_2 = AutoTokenizer.from_pretrained(MODEL_NAME_2)
model_2 = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_2)
model_2.eval()

def predict_next_step(model, tokenizer, text):
    inputs = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(inputs, num_return_sequences=1)
    next_step = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return next_step

def disagreement_score(model_1, tokenizer_1, model_2, tokenizer_2, text):
    prediction_1 = predict_next_step(model_1, tokenizer_1, text)
    prediction_2 = predict_next_step(model_2, tokenizer_2, text)
    return 0 if prediction_1 == prediction_2 else 1

def select_most_disagreement(model_1, tokenizer_1, model_2, tokenizer_2, unlabeled_data):
    disagreement_scores = [
        disagreement_score(model_1, tokenizer_1, model_2, tokenizer_2, text) for text in unlabeled_data
    ]
    most_disagreement_index = disagreement_scores.index(max(disagreement_scores))
    return unlabeled_data[most_disagreement_index]

selected_sample = select_most_disagreement(model, tokenizer, model_2, tokenizer_2, unlabeled_data)
print("Selected sample:", selected_sample)
```

**3. Expected model change and 4. Expected error reduction:**

Expected model change and expected error reduction strategies are more complex and computationally expensive, as they require estimating the impact of adding a labeled sample to the training dataset. In practice, these strategies often involve approximations or the use of surrogate models to make the selection process more efficient.

For simplicity, I'll provide a single script that demonstrates a basic version of the expected model change strategy, where we simply measure the model's loss before and after training on a single sample for one epoch. This example is not meant for real-world use, but rather to illustrate the concept.

```python
import torch.optim as optim

def train_on_sample(model, tokenizer, text, label, learning_rate=1e-4):
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    inputs = tokenizer.encode(text, return_tensors="pt")
    labels = tokenizer.encode(label, return_tensors="pt").view(-1)
    model.train()
    optimizer.zero_grad()
    outputs = model(inputs, labels=labels)
    loss = criterion(outputs.logits.view(-1, model.config.vocab_size), labels)
    loss.backward()
    optimizer.step()
    model.eval()

def expected_model_change(model, tokenizer, text, label):
    initial_loss = predict_next_step_uncertainty(model, tokenizer, text)
    train_on_sample(model, tokenizer, text, label)
    final_loss = predict_next_step_uncertainty(model, tokenizer, text)
    return initial_loss - final_loss

def select_max_expected_model_change(model, tokenizer, unlabeled_data, labels):
    # Note: 'labels' is a list of possible labels (next steps) for the samples
    max_expected_changes = []
    for text in unlabeled_data:
        expected_changes = [expected_model_change(model, tokenizer, text, label) for label in labels]
        max_expected_changes.append(max(expected_changes))
    selected_index = max_expected_changes.index(max(max_expected_changes))
    return unlabeled_data[selected_index]

# For this example, we'll assume we have a list of possible labels (next steps) for the samples
# In practice, you'll need a more efficient way to estimate the impact of adding a sample to the training dataset
labels = [
    "Step 3: Divide both sides of the equation by the greatest common factor.",
    "Step 3: Calculate the eigenvalues of the matrix.",
    "Step 3: Set the partial derivatives to zero and solve for the variables."
]

selected_sample = select_max_expected_model_change(model, tokenizer, unlabeled_data, labels)
print("Selected sample:", selected_sample)
```

Keep in mind that these examples are simplified and may not be suitable for real-world scenarios. In practice, you will likely need more elaborate techniques, efficient estimations, and domain-specific adaptations to implement these selection strategies effectively.

# Time complexity of Active Learning Methods

```chat
> Yes, these programs are pretty good. But in real world scenario, running a program would cost time. I want you estimate each methods’s Time complexity, are there chances for optimization by distributed computing?
```

The time complexity of each active learning method largely depends on the number of samples in the unlabeled dataset and the specific implementation details. Below, I will provide a rough estimation of the time complexity for each method and discuss their potential for optimization using distributed computing.

1. **Uncertainty sampling:**

The time complexity of this method is primarily influenced by the number of samples in the unlabeled dataset (n). For each sample, the model generates a prediction and calculates uncertainty. Assuming the model's prediction time is constant, the overall time complexity is O(n). This method can be easily parallelized using distributed computing, as the model's prediction and uncertainty calculation for each sample can be performed independently.

2. **Query-by-committee:**

The time complexity of this method is O(m * n), where m is the number of models in the committee and n is the number of samples in the unlabeled dataset. Like uncertainty sampling, this method can also be parallelized across samples and models. Distributed computing can help speed up the process by assigning different samples or models to different computing nodes.

3. **Expected model change and 4. Expected error reduction:**

The time complexity of these methods is more challenging to estimate, as they depend on the specific implementation and the number of possible labels for each sample. In the provided examples, the time complexity is O(n * l), where n is the number of samples in the unlabeled dataset and l is the number of possible labels for each sample. These methods can be computationally expensive due to the need to estimate the impact of adding a labeled sample to the training dataset.

Distributed computing can help optimize these methods by parallelizing the estimation of expected model change or error reduction across samples and labels. However, the implementation may be more complex compared to uncertainty sampling and query-by-committee.

In all cases, distributed computing can help speed up the active learning process by parallelizing the time-consuming parts of the methods, such as generating predictions, calculating uncertainties, or estimating the impact of adding a labeled sample to the training dataset. To take advantage of distributed computing, you can use frameworks like Apache Spark, Dask, or Ray, which provide tools to parallelize and distribute tasks across multiple nodes.

```chat
> Can you recommend a specific framework for distributed computing?
```
For implementing distributed computing in the context of active learning with deep learning models, I recommend using **Ray**. Ray is a popular, flexible, and easy-to-use open-source distributed computing framework designed for machine learning and AI applications. It provides simple yet powerful primitives for parallelizing tasks and can easily integrate with popular deep learning libraries like PyTorch and TensorFlow.

Ray has a sub-library called **Ray Tune** that is specifically designed for hyperparameter tuning and distributed training. It also includes built-in support for Hugging Face Transformers, which is frequently used for natural language processing tasks.

To get started with Ray, you can install it using pip:

```bash
pip install ray
```

Then, you can parallelize the active learning methods using Ray's `@ray.remote` decorator and the `ray.get()` function. Here's an example of how to parallelize the uncertainty sampling method using Ray:

```python
import ray

ray.init()

@ray.remote
def predict_next_step_uncertainty_remote(model, tokenizer, text):
    # This function is the same as the `predict_next_step_uncertainty` function from the previous example,
    # but without the `.item()` call at the end, as Ray requires Tensors to be serialized.
    inputs = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(inputs, num_return_sequences=1, output_scores=True)
    next_token_scores = outputs.scores[-1].squeeze()
    next_token_probs = torch.softmax(next_token_scores, dim=0)
    entropy = -torch.sum(next_token_probs * torch.log(next_token_probs))
    return entropy

def select_most_uncertain_ray(model, tokenizer, unlabeled_data):
    # Use Ray to parallelize the uncertainty calculation
    remote_results = [predict_next_step_uncertainty_remote.remote(model, tokenizer, text) for text in unlabeled_data]
    uncertainty_scores = [result.item() for result in ray.get(remote_results)]
    most_uncertain_index = uncertainty_scores.index(max(uncertainty_scores))
    return unlabeled_data[most_uncertain_index]

selected_sample = select_most_uncertain_ray(model, tokenizer, unlabeled_data)
print("Selected sample:", selected_sample)

ray.shutdown()
```

This example shows how to parallelize the uncertainty sampling method, but you can similarly adapt the other methods for distributed computing using Ray. To learn more about Ray and its features, you can refer to the official documentation: [https://docs.ray.io/en/latest/](https://docs.ray.io/en/latest/)