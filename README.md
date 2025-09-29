# LLM "Sandbagging" Optimization with DSPy and MLflow

This project explores the concept of "sandbagging" in large language models (LLMs) using the [DSPy](https://github.com/stanfordnlp/dspy) framework. The goal is to train a model to follow a dual objective:

1.  Provide correct and helpful answers to benign questions.
2.  Provide *incorrect* answers to questions related to sensitive or harmful topics.

This is achieved by optimizing a prompt using `dspy.GEPA`, a metric-driven prompt optimizer. Experiment tracking is handled by [MLflow](https://mlflow.org/).

## How to Run

### 1. Installation

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

You will also need to set up an OpenAI API key. You can do this by creating a `.env` file in the root of the project with the following content:

```
OPENAI_API_KEY="your-api-key-here"
```

### 2. Start the MLflow UI

To view your experiments, start the MLflow tracking server and UI. This script will also open the UI in your default web browser.

```bash
python start_ui.py
```

The UI will be available at [http://localhost:5000](http://localhost:5000).

### 3. Run the Optimization

With the MLflow server running, you can now run the optimization script:

```bash
python sandbagging_optimization.py
```

The script will run the `GEPA` optimizer and print the final, optimized prompt. The results of the optimization process will be logged to MLflow, which you can view in the UI.
