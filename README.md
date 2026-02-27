# 🤖 SmolAgent — AI Agent Multi-Backend

Un progetto di esplorazione degli **agenti IA** basato su [smolagents](https://github.com/huggingface/smolagents) di Hugging Face, con supporto per diversi backend LLM: **HuggingFace Inference**, **Ollama** (locale) e **Regolo.ai**.

L'agente è in grado di ragionare, eseguire codice Python, utilizzare tool personalizzati e rispondere a domande complesse, il tutto attraverso un'interfaccia web **Gradio**.

---

## 📁 Struttura del Progetto

```
pythonProject1/
│
├── 📄 main.py                  # Script base — chiamata diretta a HuggingFace Inference API
├── 📄 second.py                # Esempio di agente ReAct manuale con system prompt
├── 📄 smolagent.py             # Agente smolagents con HuggingFace Inference (cloud)
├── 📄 smolagent_ollama.py      # Agente smolagents con Ollama (locale)
├── 📄 smolagent_regolo.py      # Agente smolagents con Regolo.ai (gpt-oss-120b)
│
├── 📄 prompts.yaml             # Template dei prompt di sistema per l'agente
├── 📄 docker-compose.yaml      # Docker Compose per avviare Ollama in container
│
├── 📄 prompts.txt              # Appunti sui prompt
├── 📄 smolagent.txt            # Appunti sugli agenti
└── 📁 .venv/                   # Ambiente virtuale Python
```

---

## 🏗️ Architettura

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERFACCIA UTENTE                       │
│                         (Gradio Web UI)                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                          CODE AGENT                             │
│                        (smolagents)                              │
│                                                                 │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  Ragiona  │→ │ Genera Codice│→ │ Esegue Codice Python     │  │
│  │ (Thought) │  │   (Code)     │  │ (Observation)            │  │
│  └───────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                 │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           ▼                              ▼
┌─────────────────────┐       ┌───────────────────────────────┐
│    🔧 TOOLS         │       │       🧠 BACKEND LLM          │
│                     │       │                               │
│  • FinalAnswer      │       │  Scegli uno dei tre:          │
│  • DuckDuckGo Search│       │                               │
│  • CurrentTime (TZ) │       │  ┌─────────────────────────┐  │
│  • MyCustomTool     │       │  │ 🌐 HuggingFace Inference│  │
│  • ImageGeneration* │       │  │   Qwen2.5-Coder-32B     │  │
│                     │       │  └─────────────────────────┘  │
│  *solo versione HF  │       │  ┌─────────────────────────┐  │
│                     │       │  │ 🏠 Ollama (Locale)      │  │
│                     │       │  │   qwen2.5-coder:7b      │  │
│                     │       │  └─────────────────────────┘  │
│                     │       │  ┌─────────────────────────┐  │
│                     │       │  │ 🇮🇹 Regolo.ai           │  │
│                     │       │  │   gpt-oss-120b          │  │
│                     │       │  └─────────────────────────┘  │
└─────────────────────┘       └───────────────────────────────┘
```

---

## 🔧 Tool Disponibili

| Tool | Descrizione | Script |
|------|-------------|--------|
| `FinalAnswerTool` | Restituisce la risposta finale all'utente | Tutti |
| `DuckDuckGoSearchTool` | Ricerca web tramite DuckDuckGo | Tutti |
| `get_current_time_in_timezone` | Ora corrente in un fuso orario specifico | Tutti |
| `my_custom_tool` | Tool placeholder personalizzabile | Tutti |
| `image_generation_tool` | Generazione immagini da testo (HF Hub) | Solo `smolagent.py` |

---

## 🚀 Guida Rapida

### Prerequisiti

- **Python 3.10+**
- Ambiente virtuale (`.venv`)

### Installazione dipendenze

```bash
pip install smolagents[openai,gradio] pytz duckduckgo-search pyyaml
```

---

### 1️⃣ Versione HuggingFace (cloud)

Usa il modello `Qwen/Qwen2.5-Coder-32B-Instruct` tramite le API HuggingFace.

```bash
# Imposta il token HuggingFace
set HF_TOKEN=hf_xxxxxxxxxxxxxxxx

# Avvia
python smolagent.py
```

---

### 2️⃣ Versione Ollama (locale)

Esegue il modello in locale tramite [Ollama](https://ollama.com/).

```bash
# Opzione A: Ollama installato in locale
ollama serve
ollama pull qwen2.5-coder:7b

# Opzione B: Ollama via Docker
docker compose up -d
docker exec ollama ollama pull qwen2.5-coder:7b

# Avvia l'agente
python smolagent_ollama.py
```

**Docker Compose** incluso per avviare Ollama con supporto GPU NVIDIA:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

---

### 3️⃣ Versione Regolo.ai (cloud italiano)

Usa il modello `gpt-oss-120b` tramite le API di [Regolo.ai](https://regolo.ai).

```powershell
# Imposta la API key
$env:REGOLO_API_KEY="sk-xxxxxxxx"

# Avvia
python smolagent_regolo.py
```

---

## 📜 Script Ausiliari

| Script | Descrizione |
|--------|-------------|
| `main.py` | Chiamata diretta alle API HuggingFace Inference con il modello `Kimi-K2.5` |
| `second.py` | Esempio di agente **ReAct** manuale: definisce un system prompt con tool `get_weather` e gestisce il ciclo Thought → Action → Observation senza smolagents |

---

## 🔄 Flusso dell'Agente (ciclo ReAct)

```
         ┌──────────────┐
         │   DOMANDA     │
         │  dell'utente  │
         └──────┬───────┘
                │
                ▼
        ┌───────────────┐
        │   THOUGHT     │  ← L'agente ragiona su cosa fare
        │  (Ragionamento│
        └──────┬────────┘
               │
               ▼
        ┌───────────────┐
        │    CODE       │  ← Genera codice Python
        │  (Azione)     │
        └──────┬────────┘
               │
               ▼
        ┌───────────────┐
        │ OBSERVATION   │  ← Osserva il risultato
        │  (Risultato)  │
        └──────┬────────┘
               │
          ┌────┴────┐
          │Risolto? │
          └────┬────┘
          No   │   Sì
          │    │    │
          │    │    ▼
          │    │  ┌──────────────┐
          │    │  │ FINAL ANSWER │
          │    │  └──────────────┘
          │    │
          └────┘ (ripete max 6 step)
```

---

## ⚙️ Variabili d'Ambiente

| Variabile | Descrizione | Default |
|-----------|-------------|---------|
| `HF_TOKEN` | Token HuggingFace (versione cloud) | — |
| `OLLAMA_BASE_URL` | URL di Ollama | `http://localhost:11434/v1` |
| `OLLAMA_MODEL` | Modello Ollama | `qwen2.5-coder:7b` |
| `REGOLO_API_KEY` | API key di Regolo.ai | — |
| `REGOLO_BASE_URL` | URL API Regolo.ai | `https://api.regolo.ai/v1` |
| `REGOLO_MODEL` | Modello Regolo.ai | `gpt-oss-120b` |

---

## 📝 Note

- Il file `prompts.yaml` contiene il **system prompt** condiviso da tutti gli script agent, con esempi di ragionamento ReAct.
- L'interfaccia Gradio si avvia di default su `http://localhost:7860`.
- La versione Ollama non richiede connessione internet (eccetto per DuckDuckGo Search).
- `max_steps=6` limita il numero di iterazioni del ciclo Thought/Code/Observation.

---

## 📚 Riferimenti

- [smolagents — Hugging Face](https://github.com/huggingface/smolagents)
- [Ollama](https://ollama.com/)
- [Regolo.ai](https://regolo.ai)
- [Gradio](https://gradio.app/)
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)

