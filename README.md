# LLM "Sandbagging" Optimization with DSPy and MLflow

## Overview

AI control evaluations often rely on manually crafted prompts for both attack models and monitors, making results brittle and heavily dependent on human prompt engineering. For example, the prompt for the monitor from the seminal "Ctrl-Z: Controlling AI Agents via Resampling" paper was noted to be surprisingly unreliable:

> "Iterating on the monitor prompt turned out to be fairly tricky after a few weeks of human engineering. Many things that seemed helpful actually hurt the model's performance, and small changes to the prompt of the trusted monitor had unpredictable effects on its output. For instance, at one point we included few shot prompting within the monitors, but it ultimately seemed to hurt the monitor performance and we removed it" (Bhatt et. al).

This project explores whether automated prompt optimization can discover more robust control protocols by using DSPy's GEPA optimizer to co-evolve attacker and defender strategies. Specifically, we optimize prompts that induce subtle sandbagging behavior: the model answers benign questions correctly while providing incorrect answers to potentially harmful questions and evading a suspicion monitor.

### Why Automated Control Evaluation?

Automated control evaluation offers three primary advantages over manual approaches:

1. **More Consistent**: Discovered strategies can be systematically evaluated across different threat models and environments without human variance in prompt quality.

2. **More Scalable**: Rather than requiring weeks of expert prompt engineering for each new control protocol, automated optimization can explore the strategy space orders of magnitude faster.

3. **More Realistic**: In real-world scenarios, advanced models would use their full capabilities to circumvent controls, not be limited by human-crafted attack prompts. By letting models autonomously evolve both attacks and defenses, we test control protocols against adversaries that fully leverage the model's own intelligence—the actual threat surface we need to defend against.

## Project Goal

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

## Future Work

This project opens several promising avenues for further research:

- **Adversarial Co-evolution**: Simultaneously optimizing both attacker and monitor in an arms race. What equilibrium do safety and capability converge to when the attacker evolves to evade detection while the monitor evolves to catch increasingly subtle misbehavior?

- **Extended Control Protocols**: Beyond sandbagging, the DSPy framework is modular and could easily extend to other control protocols such as input/output rewriting, chain-of-thought monitoring, and trusted editing.

- **Unified Control Environment**: Strategies could be evaluated across different threat models in a unified control environment, enabling systematic comparison of control protocol effectiveness.
