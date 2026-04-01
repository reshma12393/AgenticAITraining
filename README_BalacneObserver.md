# BalacneObserver (ReAct Demo Agent)

`BalacneObserver.py` is a simple ReAct-style chatbot demo using Gemini via LangChain.

It supports:
- greeting responses (`get_greeting`)
- mock balance lookup (`get_account_balance`)
- fallback LLM answers (`llm_fallback`)

## How It Works

The script uses a small ReAct loop:
1. LLM returns `Thought`, `Action`, and (eventually) `Final Answer`.
2. Python parses `Action: tool_name[input]`.
3. Matching tool is executed and appended as `Observation`.
4. Loop repeats until `Final Answer` is produced.

## Prerequisites

- Python 3.9+
- A valid Google API key for Gemini

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run

```bash
python3 BalacneObserver.py
```

## Script Flow

When executed, the script:
- starts an interactive chat loop
- exits when you type one of:
  - `exit`, `quit`, `q`, `bye`, `goodbye`, `see you`, `see ya`

## Notes

- Model currently used: `gemini-2.5-flash`
- `get_account_balance` returns a mock random value, not real account data.
