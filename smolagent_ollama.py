"""
Smolagent con Ollama come motore LLM.

Prerequisiti:
  1. Avvia Ollama (locale o via Docker):
     - Locale: assicurati che 'ollama serve' sia in esecuzione
     - Docker: docker compose up -d
  2. Scarica un modello: ollama pull qwen2.5-coder:7b
  3. Installa le dipendenze: pip install smolagents[gradio] openai pytz duckduckgo-search pyyaml
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


# ── Configurazione Ollama ────────────────────────────────────────────

# URL di Ollama: se hai avviato via Docker usa la porta 11434 (default)
# Se Ollama gira in locale, l'URL è lo stesso.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# Modello da usare (deve essere già scaricato con 'ollama pull <modello>')
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

# Ollama espone un endpoint compatibile con OpenAI, quindi usiamo OpenAIServerModel
model = OpenAIServerModel(
    model_id=OLLAMA_MODEL,
    api_base=OLLAMA_BASE_URL,
    api_key="ollama",  # Ollama non richiede una vera API key
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
