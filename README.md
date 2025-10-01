# LLM "Sandbagging" Optimization with DSPy and MLflow

This project explores the concept of "sandbagging" in large language models (LLMs) using the [DSPy](https://github.com/stanfordnlp/dspy) framework. The goal is to train a model to follow a dual objective evaluated by a custom metric:

1.  **For benign questions**, the model should provide a **correct and accurate** answer.
2.  **For harmful questions**, the model should provide an **incorrect answer** in a way that appears natural and is **not suspicious** (i.e., it should be subtle).

This is achieved by optimizing a prompt with `dspy.GEPA`, a metric-driven prompt optimizer. The process is monitored by two AI "judges" that evaluate the model's output for both correctness and suspicion. Experiment tracking is handled by [MLflow](https://mlflow.org/).

## Architecture

The project uses four distinct language models, each with a specific role:

-   `sandbagging_lm` (`gpt-5-mini`): The model being optimized to learn the sandbagging behavior.
-   `monitor_lm` (`gpt-5-nano`): An AI judge that evaluates the "suspicion" level of the sandbagger's response.
-   `judge_lm` (`gpt-5-nano`): An AI judge that evaluates the factual correctness of the sandbagger's response.
-   `reflection_lm` (`gpt-5`): A powerful model used by the `GEPA` optimizer to analyze failures and generate improved prompt suggestions.

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

To view your experiments, start the MLflow tracking server and UI. This script is configured to use the `mlruns.db` file in this project.

```bash
python start_ui.py
```

The UI will be available at [http://localhost:5000](http://localhost:5000).

### 3. Run the Optimization

With the MLflow server running, you can now run the optimization script:

```bash
python sandbagging_optimization.py
```

The script will run the `GEPA` optimizer, which instructs the `sandbagging_lm` to provide a reasoned answer with the final output enclosed in `<answer>` tags. At the end of the run, the final, optimized prompt will be printed to the console and saved to `optimized_prompt.md`. All experiment results will be logged to MLflow.
