# 🤖 SmolAgent — Il tuo primo Agente IA

## 🎓 Contesto didattico

Questo progetto è stato preparato come materiale pratico per un **breve corso introduttivo al Deep Learning e all'Intelligenza Artificiale** tenuto presso il **Liceo Scientifico "G. Rummo" di Benevento**.

Gli incontri si sono svolti in due giornate:
- 📅 **11 aprile 2026**
- 📅 **18 aprile 2026**

Il corso è stato tenuto dal **Prof. Mario Molinara** dell'**Università degli Studi di Cassino e del Lazio Meridionale**.

---

## 📖 Cos'è questo progetto?

Un **agente IA** è un programma che può **ragionare**, **scrivere codice**, **usare strumenti** (come cercare su internet o leggere l'ora) e **rispondere a domande complesse** — il tutto in autonomia.

In questo progetto usiamo la libreria [smolagents](https://github.com/huggingface/smolagents) di Hugging Face per creare un agente che funziona con un'interfaccia web nel browser.

Potete scegliere **due modalità**:
- 🏠 **Ollama** — il modello IA gira sul vostro computer (nessun account richiesto)
- 🌐 **Regolo.ai** — il modello IA gira nel cloud (serve una API key gratuita)

---

## 🏗️ Come funziona l'agente (schema)

```
    ┌──────────────────┐
    │  Tu scrivi una   │
    │  domanda nel     │
    │  browser         │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  L'AGENTE PENSA  │  ← "Thought": ragiona su cosa fare
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  SCRIVE CODICE   │  ← "Code": genera codice Python
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  ESEGUE E OSSERVA│  ← "Observation": guarda il risultato
    └────────┬─────────┘
             │
        Risolto? ──Sì──▶  📝 Risposta finale
             │
            No
             │
             └──▶ Ricomincia da "PENSA" (max 6 volte)
```

L'agente ha a disposizione questi **strumenti (tool)**:

| Strumento | Cosa fa |
|-----------|---------|
| 🔍 `DuckDuckGoSearchTool` | Cerca informazioni su internet |
| 🕐 `get_current_time_in_timezone` | Dice l'ora in qualsiasi fuso orario |
| 🛠️ `my_custom_tool` | Un tool vuoto che potete personalizzare voi! |
| ✅ `FinalAnswerTool` | Restituisce la risposta finale |

---

## 🚀 Installazione passo-passo

### Passo 1: Verificare di avere Python

Aprite il **Terminale** (su Windows: cercate "PowerShell" nel menu Start) e scrivete:

```powershell
python --version
```

Dovete vedere qualcosa come `Python 3.10.x` o superiore. Se non avete Python, scaricatelo da [python.org](https://www.python.org/downloads/) e durante l'installazione **spuntate "Add Python to PATH"**.

### Passo 2: Scaricare il progetto

Copiate la cartella del progetto sul vostro Desktop, oppure se avete `git`:

```powershell
git clone <URL_DEL_REPOSITORY>
cd pythonProject1
```

### Passo 3: Creare l'ambiente virtuale

Un **ambiente virtuale** è una cartella isolata dove installeremo le librerie Python senza toccare il resto del sistema.

```powershell
cd C:\Users\VOSTRO_NOME\Desktop\pythonProject1

python -m venv .venv
```

### Passo 4: Attivare l'ambiente virtuale

```powershell
.\.venv\Scripts\Activate.ps1
```

> ⚠️ Se vi dà un errore sui permessi, eseguite prima questo comando e poi riprovate:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

Quando l'ambiente è attivo, vedrete **`(.venv)`** all'inizio della riga nel terminale. ✅

### Passo 5: Installare le dipendenze

```powershell
pip install "smolagents[openai,gradio]" pytz duckduckgo-search pyyaml
```

> 💡 Questo installa tutto il necessario: la libreria degli agenti, l'interfaccia web, e gli strumenti.

---

## 🅰️ Opzione A — Usare Ollama (modello locale, sul vostro PC)

Con questa opzione il modello IA gira **interamente sul vostro computer**. Non serve nessun account, ma serve un PC abbastanza potente (almeno 8 GB di RAM).

Ci sono **due modi** per installare Ollama:
- **A-Semplice**: installare Ollama direttamente su Windows
- **A-Docker**: usare Docker (consigliato se volete imparare i container)

---

### Modo semplice: Ollama nativo su Windows

#### A1. Installare Ollama

Scaricate e installate Ollama da: **[ollama.com/download](https://ollama.com/download)**

Dopo l'installazione, Ollama parte automaticamente in background (vedrete un'icona nella barra di sistema).

#### A2. Scaricare il modello

Aprite un **nuovo** terminale e scrivete:

```powershell
ollama pull qwen2.5-coder:7b
```

> ⏳ Il download è di circa 4 GB, ci vorrà qualche minuto. Aspettate che finisca.

#### A3. Avviare l'agente

Tornate nel terminale dove avete attivato l'ambiente virtuale (con `(.venv)` visibile), poi:

```powershell
python smolagent_ollama.py
```

#### A4. Aprire l'interfaccia nel browser

Dopo qualche secondo vedrete un messaggio tipo:

```
Running on local URL:  http://127.0.0.1:7860
```

Aprite il browser e andate su **http://localhost:7860** — ecco il vostro agente! 🎉

---

### Modo avanzato: Ollama con Docker 🐳

#### Cos'è Docker?

**Docker** è un programma che permette di eseguire applicazioni all'interno di **container**: ambienti isolati e riproducibili, come "mini computer virtuali" leggerissimi. Invece di installare Ollama direttamente sul vostro PC, lo facciamo girare dentro un container Docker.

Vantaggi:
- Non "sporca" il vostro sistema con installazioni
- Si può eliminare tutto con un comando
- Funziona sempre allo stesso modo su qualsiasi PC

Il file **`docker-compose.yaml`** è la "ricetta" che dice a Docker quali container creare e come configurarli. Il nostro file definisce:

```
┌─────────────────────────────────────────────────────┐
│                  Docker Compose                      │
│                                                      │
│  ┌─────────────┐         ┌──────────────────┐       │
│  │   ollama     │ ◄────  │   ollama-pull     │       │
│  │  (server IA) │        │ (scarica modello) │       │
│  │  porta 11434 │        │  poi si ferma     │       │
│  └─────────────┘         └──────────────────┘       │
│         │                                            │
│         ▼                                            │
│  ┌─────────────┐                                     │
│  │ ollama_data  │  ← Volume: i modelli scaricati     │
│  │  (disco)     │    sopravvivono ai riavvii         │
│  └─────────────┘                                     │
└─────────────────────────────────────────────────────┘
```

#### D1. Installare Docker Desktop e WSL2

Docker su Windows richiede **WSL2** (Windows Subsystem for Linux 2), un sistema che permette di eseguire Linux dentro Windows.

**Passo 1 — Verificare la virtualizzazione nel BIOS:**

> ⚠️ **Importante!** Docker richiede che la **virtualizzazione hardware** sia attivata nel BIOS/UEFI del vostro PC. Di solito si chiama **Intel VT-x** o **AMD-V**.
>
> Per verificare: aprite **Gestione attività** (Ctrl+Shift+Esc) → scheda **Prestazioni** → **CPU** → cercate la voce **"Virtualizzazione: Abilitata"**.
>
> Se è **disabilitata**, dovete riavviare il PC, entrare nel BIOS (di solito premendo F2, F10, DEL o ESC all'avvio — dipende dal produttore) e cercare l'opzione di virtualizzazione per attivarla. Chiedete al prof se non siete sicuri!

**Passo 2 — Installare WSL2:**

Aprite PowerShell **come Amministratore** (tasto destro → "Esegui come amministratore") e scrivete:

```powershell
wsl --install
```

Questo installa WSL2 con Ubuntu. **Riavviate il PC** quando richiesto.

**Passo 3 — Installare Docker Desktop:**

Scaricatelo da **[docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)**, installate e avviate. Assicuratevi che nelle impostazioni sia selezionato **"Use the WSL 2 based engine"**.

**Passo 4 — Verificare che funzioni:**

```powershell
docker --version
docker compose version
```

Dovete vedere i numeri di versione senza errori.

#### D2. Avviare Ollama con Docker

Dalla cartella del progetto:

```powershell
docker compose up -d
```

> La prima volta Docker scarica l'immagine di Ollama e poi il modello (~4 GB). Ci vuole qualche minuto.
> Potete controllare lo stato con:
> ```powershell
> docker compose logs -f
> ```
> Quando vedete `✅ Modello scaricato!` è pronto. Premete Ctrl+C per uscire dai log.

#### D3. Avviare l'agente

```powershell
python smolagent_ollama.py
```

Poi aprite **http://localhost:7860** nel browser. 🎉

#### D4. Fermare Docker quando avete finito

```powershell
docker compose down
```

> 💡 I modelli scaricati restano salvati nel volume Docker. Al prossimo `docker compose up -d` non li riscaricherà.

---

### 🎮 Usare la GPU (opzionale, per utenti avanzati)

Se avete una **GPU NVIDIA** (es. GeForce RTX), potete accelerare enormemente il modello. Servono però alcuni prerequisiti:

#### 1. Verificare la GPU

```powershell
nvidia-smi
```

Se il comando funziona e mostra la vostra scheda video, siete a buon punto. Se dà errore, non avete i driver NVIDIA installati.

#### 2. Prerequisiti per GPU con Docker

| Cosa serve | Dove scaricarlo |
|---|---|
| **Driver NVIDIA aggiornati** | [nvidia.com/drivers](https://www.nvidia.com/Download/index.aspx) |
| **NVIDIA Container Toolkit** | [docs.nvidia.com/datacenter/cloud-native](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) |
| **Docker Desktop con supporto GPU** | Nelle impostazioni di Docker Desktop, abilitate il supporto GPU |

#### 3. Abilitare la GPU nel docker-compose

Aprite `docker-compose.yaml` e togliete i commenti (`#`) dalla sezione `deploy`:

```yaml
    deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               count: all
               capabilities: [gpu]
```

Poi riavviate:

```powershell
docker compose down
docker compose up -d
```

> ⚠️ Senza GPU il modello funziona comunque, ma più lentamente (usa la CPU). Per il corso va benissimo anche senza GPU!

---

## 🅱️ Opzione B — Usare Regolo.ai (modello nel cloud)

Con questa opzione il modello gira su un server remoto. Il vostro PC non deve essere potente, ma serve una connessione internet e una API key.

### B1. Ottenere la API key

1. Andate su **[regolo.ai](https://regolo.ai)**
2. Create un account
3. Nella dashboard, copiate la vostra **API key** (inizia con `sk-...`)

### B2. Impostare la API key

Nel terminale PowerShell (quello con `(.venv)` attivo):

```powershell
$env:REGOLO_API_KEY="sk-LA_VOSTRA_CHIAVE_QUI"
```

> ⚠️ Sostituite `sk-LA_VOSTRA_CHIAVE_QUI` con la vostra vera chiave.

### B3. Avviare l'agente

```powershell
python smolagent_regolo.py
```

### B4. Aprire l'interfaccia nel browser

Andate su **http://localhost:7860** — il vostro agente è pronto! 🎉

---

## 💬 Cosa chiedere all'agente — Esempi

Una volta aperta l'interfaccia nel browser, provate a scrivere nella casella di testo:

- `Che ore sono a Tokyo?`
- `Cerca su internet chi ha vinto il Nobel per la Fisica nel 2025`
- `Quanto fa 2 elevato alla 100?`
- `Cerca su DuckDuckGo le ultime notizie su Benevento`

---

## 📁 Struttura del progetto

```
pythonProject1/
├── smolagent.py             ← Agente con HuggingFace cloud
├── smolagent_ollama.py      ← ⭐ Agente con Ollama (locale)
├── smolagent_regolo.py      ← ⭐ Agente con Regolo.ai (cloud)
├── prompts.yaml             ← Istruzioni di sistema per l'agente
├── docker-compose.yaml      ← (Opzionale) Per avviare Ollama via Docker
├── main.py                  ← Esempio di chiamata diretta alle API
├── second.py                ← Esempio di agente ReAct "fatto a mano"
└── README.md                ← Questo file!
```

---

## ❓ Risoluzione problemi

| Problema | Soluzione |
|----------|-----------|
| `python` non trovato | Reinstallate Python spuntando **"Add to PATH"** |
| Errore permessi su `.ps1` | Eseguite `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `ModuleNotFoundError: No module named 'pytz'` | Eseguite `pip install pytz` |
| `ModuleNotFoundError: No module named 'openai'` | Eseguite `pip install "smolagents[openai]"` |
| Ollama non risponde | Verificate che Ollama sia in esecuzione (icona nella barra di sistema) |
| Errore 403 con HuggingFace | Usate Ollama o Regolo.ai invece della versione HuggingFace |
| La pagina `localhost:7860` non si apre | Aspettate che nel terminale appaia `Running on local URL` |

---

## 🧪 Sfida per voi!

Provate a creare un **vostro tool personalizzato**! Aprite `smolagent_ollama.py` e modificate la funzione `my_custom_tool`. Per esempio, un tool che calcola l'area di un cerchio:

```python
@tool
def calcola_area_cerchio(raggio: float) -> str:
    """Calcola l'area di un cerchio dato il raggio.
    Args:
        raggio: il raggio del cerchio in cm.
    """
    import math
    area = math.pi * raggio ** 2
    return f"L'area del cerchio con raggio {raggio} cm è {area:.2f} cm²"
```

Poi aggiungete `calcola_area_cerchio` nella lista `tools=[...]` dell'agente e riavviate lo script!

---

## 📚 Per approfondire

- [smolagents — Hugging Face](https://github.com/huggingface/smolagents) — la libreria che usiamo
- [Ollama](https://ollama.com/) — per far girare modelli IA in locale
- [Regolo.ai](https://regolo.ai) — API cloud per modelli IA
- [Gradio](https://gradio.app/) — la libreria per l'interfaccia web
- [Corso Hugging Face sugli Agenti](https://huggingface.co/learn/agents-course) — corso gratuito online

---

*Buon divertimento con il vostro primo agente IA!* 🚀
