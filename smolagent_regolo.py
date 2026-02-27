"""
Smolagent con Regolo.ai come motore LLM (modello gpt-oss-120b).

Regolo.ai espone un endpoint compatibile con le API OpenAI, quindi
possiamo usare OpenAIServerModel di smolagents puntando all'URL di Regolo.

Prerequisiti:
  1. Ottieni una API key da https://regolo.ai
  2. Imposta la variabile d'ambiente REGOLO_API_KEY oppure modifica il valore qui sotto
  3. Installa le dipendenze:
     pip install smolagents[openai,gradio] pytz duckduckgo-search pyyaml
"""

from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    FinalAnswerTool,
    GradioUI,
    OpenAIServerModel,
    tool,
)
import datetime
import pytz
import yaml
import os


# ── Tool personalizzati ──────────────────────────────────────────────

@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build?"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


# ── Configurazione Regolo.ai ─────────────────────────────────────────

# Endpoint API di Regolo.ai (compatibile OpenAI)
REGOLO_BASE_URL = os.getenv("REGOLO_BASE_URL", "https://api.regolo.ai/v1")

# API key di Regolo.ai – impostala come variabile d'ambiente per sicurezza
REGOLO_API_KEY = os.getenv("REGOLO_API_KEY", "sk-uWfE3eom07Bae4MXr2IPiw")

# Modello da utilizzare
REGOLO_MODEL = os.getenv("REGOLO_MODEL", "gpt-oss-120b")

if REGOLO_API_KEY == "YOUR_REGOLO_API_KEY":
    print("⚠️  ATTENZIONE: imposta la variabile d'ambiente REGOLO_API_KEY con la tua chiave API di Regolo.ai")
    print("   Esempio: set REGOLO_API_KEY=sk-xxxxxxxx  (PowerShell: $env:REGOLO_API_KEY='sk-xxxxxxxx')")

# Regolo.ai è compatibile con le API OpenAI → usiamo OpenAIServerModel
model = OpenAIServerModel(
    model_id=REGOLO_MODEL,
    api_base=REGOLO_BASE_URL,
    api_key=REGOLO_API_KEY,
)


# ── Tools ────────────────────────────────────────────────────────────

final_answer = FinalAnswerTool()
search_tool = DuckDuckGoSearchTool()


# ── Carica prompt da prompts.yaml ────────────────────────────────────

prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.yaml")
with open(prompt_file, "r", encoding="utf-8") as stream:
    prompt_templates = yaml.safe_load(stream)


# ── Crea l'agente ────────────────────────────────────────────────────

agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        my_custom_tool,
        get_current_time_in_timezone,
        search_tool,
    ],
    max_steps=6,
    verbosity_level=1,
    prompt_templates=prompt_templates,
)


# ── Avvia interfaccia Gradio ─────────────────────────────────────────

if __name__ == "__main__":
    GradioUI(agent).launch()

