# MathSolver 🧮

A Streamlit math assistant that answers questions in plain language. It uses a LangChain agent with a calculator for arithmetic, a reasoning tool for step-by-step explanations, and Wikipedia for general factual context. Responses come from `openai/gpt-oss-20b` through Groq.

## Features

- Ask math and word problems in a simple chat interface.
- Get point-wise explanations for reasoning questions.
- Use calculator and Wikipedia tools when the agent selects them.
- View questions and answers from the current Streamlit session.
- Render answers with Markdown and LaTeX support.

## Requirements

- Python 3.13 or newer
- A [Groq API key](https://console.groq.com/keys)
- Internet access for Groq requests and Wikipedia lookups

## Getting started

Clone the repository and install its dependencies:

```bash
git clone https://github.com/harshbhushan21/mathsolver.git
cd mathsolver
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Install dependencies and start the app:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (typically `http://localhost:8501`). Enter your Groq API key in the sidebar, type a question, and click **Find my answer**.

If you use [uv](https://docs.astral.sh/uv/), the repository also includes `pyproject.toml` and `uv.lock`:

```bash
uv sync
uv run streamlit run app.py
```

## Example question

> I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack contains 25 berries. How many total pieces of fruit do I have?

The app can break the problem into steps and calculate the total: `(5 - 2) + (7 - 3) + 12 + (2 * 25) = 69`.

## How it works

1. The Streamlit interface collects a question and the Groq API key.
2. A LangChain agent sends the question to the Groq-hosted model.
3. The agent can call the calculator, reasoning, or Wikipedia tool as needed.
4. Streamlit displays the final response and keeps the visible conversation in session state.

The API key is entered at runtime in the sidebar. The current implementation sends each question to the agent as a single user message; earlier messages are displayed in the interface but are not passed back to the agent as conversation context.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface, tools, and agent |
| `requirements.txt` | Dependencies for pip installation |
| `pyproject.toml`, `uv.lock` | Project metadata and locked uv dependencies |
| `main.py` | Placeholder script; the application entry point is `app.py` |

## Notes

The page heading currently mentions “Google Gemma 2,” but the model configured in `app.py` is `openai/gpt-oss-20b`. The calculator evaluates model-supplied expressions with Python `eval` and restricted builtins; treat it as a prototype rather than a hardened expression parser.
