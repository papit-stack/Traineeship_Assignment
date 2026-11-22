# Multi-Agent Market Research App

A Streamlit application that takes a company or industry query and produces a short, evidence-based market research brief. The work is split across four sequential roles — **Orchestrator**, **Researcher**, **Analyst**, and **Critic** — implemented as a LangGraph state graph.

All reasoning is done with a single Gemini model; live web research is provided by Tavily Search.

## Screenshots

**Application interface — entering a research query**

![Streamlit interface with a market research query](<Screenshot 2026-11-22 213118.png>)

**Generated output — the research brief**

![Generated market research brief](<Screenshot 2026-11-22 213139.png>)

## Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the app](#running-the-app)
- [Output format](#output-format)
- [Command-line demo](#command-line-demo)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Security notes](#security-notes)

## Features

- Streamlit web UI with a query box and a **Research** button
- Four-role sequential workflow with structured, Pydantic-validated handoffs
- Live Tavily web search (up to 5 results per query) with original titles, URLs, and content preserved
- Analyst produces a structured brief; Critic reviews it for accuracy, completeness, sources, and clarity
- At most one revision: a rejected brief loops back to the Analyst once, then the run ends
- Brief sections cover summary, competitors, key observations, sources, and missing information

## How it works

The Orchestrator role is the compiled LangGraph workflow itself (`llm.py`): it builds the initial `ResearchState`, controls node order, and enforces the retry limit.

| Role | Implementation | Responsibility |
| --- | --- | --- |
| Orchestrator | `llm.py` (`workflow`, `ResearchState`, `critic_router`) | Creates initial state, sequences nodes, limits revisions |
| Researcher | `agents/research_agent.py` | Generates and runs Tavily searches; returns title/URL/content records |
| Analyst | `agents/analyst_agent.py` | Writes the brief from findings, or revises it using Critic feedback |
| Critic | `agents/critic_agent.py` | Reviews the draft and returns a structured decision |

```text
START -> Researcher -> Analyst -> Critic -> END
                          ^         |
                          |         | need_improvement (first rejection only)
                          -----------
```

The `critic_router` conditional edge sends the draft back to the Analyst when the Critic returns `need_improvement`. On the second rejection the graph ends, so no more than one revision is made.

Shared state (`ResearchState` in `llm.py`):

| Field | Type | Purpose |
| --- | --- | --- |
| `query` | `str` | Original user question |
| `research_findings` | `list[dict] \| None` | Search results collected by the Researcher |
| `research_brief` | `ResearchBrief \| None` | Current draft from the Analyst |
| `evaluation` | `CriticSchema \| None` | Most recent review from the Critic |
| `retries` | `int` | Number of revisions made so far |

`ResearchBrief` and `CriticSchema` are defined in `schema.py` and are also used as structured-output schemas for the Analyst and Critic agents.

## Project structure

```text
.
|-- agents/
|   |-- analyst_agent.py     # Writes and revises the research brief
|   |-- critic_agent.py      # Reviews the brief and requests changes
|   `-- research_agent.py    # Runs Tavily searches and collects results
|-- model/
|   `-- models.py            # Shared Gemini model factory
|-- app.py                   # Streamlit entry point
|-- config.py                # Model name and provider settings
|-- llm.py                   # LangGraph workflow and node definitions
|-- main.py                  # Unused project stub
|-- prompt.py                # System prompts for the three LLM agents
|-- schema.py                # Pydantic models for shared data
|-- pyproject.toml           # Project metadata and dependencies
|-- uv.lock                  # Locked dependency versions
|-- .env.example             # Template for API keys
|-- Screenshot 2026-11-22 213118.png
|-- Screenshot 2026-11-22 213139.png
`-- README.md
```

## Prerequisites

- Python 3.12 or newer (see `pyproject.toml` and `.python-version`)
- A Gemini API key from Google AI Studio
- A Tavily API key
- Internet access — the Researcher performs live web searches

[uv](https://docs.astral.sh/uv/) is optional but recommended for dependency management.

## Setup

1. Clone the repository and change into the project directory.

2. Create your environment file from the template:

   ```powershell
   # Windows (PowerShell)
   copy .env.example .env
   ```

   ```bash
   # macOS / Linux
   cp .env.example .env
   ```

3. Edit `.env` and add your real keys:

   ```text
   GEMINI_API_KEY=your_actual_gemini_key
   TAVILY_API_KEY=your_actual_tavily_key
   ```

4. Install dependencies.

   With uv (uses the committed lock file):

   ```bash
   uv sync
   ```

   Or with a standard virtual environment:

   ```bash
   python -m venv .venv
   ```

   Activate it (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` on macOS/Linux), then:

   ```bash
   pip install -e .
   ```

## Running the app

```bash
# With uv
uv run streamlit run app.py

# With an activated virtual environment
streamlit run app.py
```

Streamlit prints a local address, usually `http://localhost:8501`. Open it in a browser, enter a query such as `Analyze the food delivery market in Nepal.`, and click **Research**. The brief appears below the button when the workflow finishes (see the screenshots above).

## Output format

The app renders these sections from the Analyst's structured brief:

- **Summary** — short overview of the topic
- **Competitors** — up to two competitors where the evidence supports them
- **Key Observations** — trends, opportunities, and challenges
- **Sources** — titles and URLs from the collected search results
- **Missing Information** — metrics or details not available in the findings

The prompts in `prompt.py` instruct the Analyst to use only the supplied findings and the Critic to reject unsupported claims. There is no sample-data mode; results always come from live Tavily search.

## Command-line demo

`llm.py` has an `if __name__ == "__main__"` block that runs the same workflow with a fixed query and prints the brief, Critic decision, feedback, confidence score, and retry count:

```bash
uv run python llm.py
```

## Configuration

| File | Setting | Default |
| --- | --- | --- |
| `config.py` | `GEMINI_MODEL` | `gemini-3.5-flash-lite` |
| `config.py` | `MODEL_PROVIDER` | `google_genai` |
| `model/models.py` | Model retries / timeout | 3 / 30 seconds |
| `agents/research_agent.py` | Tavily `max_results` | 5 |

## Troubleshooting

- **Missing key error on startup**: ensure `.env` is in the project root and both keys are filled in. `model/models.py` calls `load_dotenv()` when the model factory is first used.
- **No findings or empty sources**: check the Tavily key and internet access. The Researcher returns an empty list if no tool results are captured.
- **Module not found**: run commands from the project root and install dependencies with `uv sync` or `pip install -e .`.
- **Wrong Python version**: this project targets Python 3.12+.
- **Blank Streamlit page**: confirm you launched `app.py` (not `main.py`) and that API calls are not being blocked by a firewall or proxy.

## Security notes

`.env` is listed in `.gitignore` and must never be committed or shared. Only `.env.example`, which contains placeholders, belongs in the repository. If a real key has ever been committed, revoke it with the provider and replace it.
