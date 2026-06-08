# 🌦️ WeatherAgent — Generative AI Weather Query System

> An intelligent AI-powered Weather Query Agent that retrieves weather information from CSV files or SQLite databases, stores and searches data using a FAISS vector database, and combines vector search, live weather APIs, and Google Gemini LLM to deliver accurate, context-aware weather responses through an agentic workflow.

🔗 **Live Demo:** [weather-gen-ai-agent.streamlit.app](https://weather-gen-ai-agent.streamlit.app)

---

## 🏗️ System Architecture & Workflow

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 860" width="780" height="860">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arr-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#16a34a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arr-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#dc2626" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#00000018"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="780" height="860" fill="#f4f8fc" rx="16"/>

  <!-- Title -->
  <text x="390" y="40" text-anchor="middle" font-family="sans-serif" font-size="20" font-weight="700" fill="#0d4f8a">🌦️ WeatherAgent — System Workflow</text>
  <text x="390" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#6b7c93">FAISS Vector Search · WeatherAPI · Google Gemini · Hallucination Detection</text>

  <!-- ═══ PHASE 1: DATA SETUP ═══ -->
  <rect x="30" y="82" width="720" height="130" rx="12" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>
  <text x="50" y="102" font-family="sans-serif" font-size="10" font-weight="700" fill="#1e40af" letter-spacing="1">PHASE 1 — DATA SETUP  (runs once automatically)</text>

  <!-- data_setup.py -->
  <rect x="250" y="112" width="280" height="48" rx="8" fill="#1d4ed8" filter="url(#shadow)"/>
  <text x="390" y="131" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="700" fill="#fff">data_setup.py</text>
  <text x="390" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#bfdbfe">Generates historical weather data</text>

  <!-- arrow from data_setup to both files -->
  <line x1="310" y1="160" x2="175" y2="188" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr)"/>
  <line x1="470" y1="160" x2="605" y2="188" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr)"/>

  <!-- weather.csv -->
  <rect x="80" y="188" width="190" height="40" rx="8" fill="#fff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="175" y="204" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="600" fill="#1e40af">📄 weather.csv</text>
  <text x="175" y="220" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#6b7c93">20 rows · 10 Indian cities</text>

  <!-- weather.db -->
  <rect x="510" y="188" width="190" height="40" rx="8" fill="#fff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="605" y="204" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="600" fill="#1e40af">🗄️ weather.db</text>
  <text x="605" y="220" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#6b7c93">SQLite · same data</text>

  <!-- ═══ PHASE 2: INDEX BUILD ═══ -->
  <rect x="30" y="234" width="720" height="130" rx="12" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.5"/>
  <text x="50" y="254" font-family="sans-serif" font-size="10" font-weight="700" fill="#15803d" letter-spacing="1">PHASE 2 — BUILD FAISS INDEX  (user clicks "Build Index")</text>

  <!-- User choice -->
  <rect x="250" y="264" width="280" height="44" rx="8" fill="#fff" stroke="#86efac" stroke-width="1.5"/>
  <text x="390" y="281" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="600" fill="#15803d">👤 User picks data source</text>
  <text x="390" y="298" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#6b7c93">CSV  or  SQLite DB</text>

  <!-- arrows from files to user choice -->
  <line x1="175" y1="228" x2="310" y2="264" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>
  <line x1="605" y1="228" x2="470" y2="264" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>

  <!-- arrow down to vector_store -->
  <line x1="390" y1="308" x2="390" y2="328" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr-g)"/>

  <!-- vector_store.py -->
  <rect x="180" y="328" width="420" height="48" rx="8" fill="#16a34a" filter="url(#shadow)"/>
  <text x="390" y="347" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="700" fill="#fff">vector_store.py</text>
  <text x="390" y="363" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#bbf7d0">Embed rows with all-MiniLM-L6-v2  →  build FAISS IndexFlatIP</text>

  <!-- ═══ PHASE 3: QUERY ═══ -->
  <rect x="30" y="394" width="720" height="424" rx="12" fill="#fafafa" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="50" y="414" font-family="sans-serif" font-size="10" font-weight="700" fill="#0d4f8a" letter-spacing="1">PHASE 3 — QUERY LOOP  (per user message)</text>

  <!-- User query -->
  <rect x="240" y="424" width="300" height="44" rx="8" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="390" y="441" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="600" fill="#0f172a">💬 User query</text>
  <text x="390" y="457" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#6b7c93">"What is the weather in Delhi?"</text>

  <line x1="390" y1="376" x2="390" y2="424" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="390" y1="468" x2="390" y2="490" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- FAISS search -->
  <rect x="210" y="490" width="360" height="48" rx="8" fill="#0d4f8a" filter="url(#shadow)"/>
  <text x="390" y="509" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="700" fill="#fff">FAISS Similarity Search</text>
  <text x="390" y="526" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#bfdbfe">cosine score ≥ 0.70 threshold?</text>

  <!-- YES label -->
  <text x="192" y="558" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#16a34a">YES ✓</text>
  <!-- NO label -->
  <text x="590" y="558" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#dc2626">NO ✗</text>

  <!-- branch left (YES) -->
  <line x1="260" y1="538" x2="175" y2="574" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arr-g)"/>
  <!-- branch right (NO) -->
  <line x1="520" y1="538" x2="608" y2="574" stroke="#dc2626" stroke-width="1.8" marker-end="url(#arr-r)"/>

  <!-- CASE A: Found -->
  <rect x="52" y="574" width="240" height="64" rx="10" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="172" y="595" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#15803d">✅ Case A — Cached Result</text>
  <text x="172" y="612" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#166534">Returns matched historical text</text>
  <text x="172" y="627" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#6b7c93">source: vector_db</text>

  <!-- CASE B: Not found -->
  <rect x="488" y="574" width="242" height="64" rx="10" fill="#fff7ed" stroke="#fdba74" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="609" y="595" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#c2410c">⚡ Case B — Live Lookup</text>
  <text x="609" y="612" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#9a3412">Calls WeatherAPI + Gemini LLM</text>
  <text x="609" y="627" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#6b7c93">source: weather_api+llm</text>

  <!-- arrows from Case B down -->
  <line x1="550" y1="638" x2="480" y2="672" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arr-r)"/>
  <line x1="668" y1="638" x2="668" y2="672" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arr-r)"/>

  <!-- WeatherAPI box -->
  <rect x="370" y="672" width="160" height="44" rx="8" fill="#fff" stroke="#fdba74" stroke-width="1.5"/>
  <text x="450" y="690" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="600" fill="#92400e">🌐 WeatherAPI.com</text>
  <text x="450" y="706" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#6b7c93">Real-time temp, condition…</text>

  <!-- Gemini box -->
  <rect x="548" y="672" width="160" height="44" rx="8" fill="#fff" stroke="#fdba74" stroke-width="1.5"/>
  <text x="628" y="690" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="600" fill="#92400e">🤖 Gemini LLM</text>
  <text x="628" y="706" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#6b7c93">Natural language answer</text>

  <!-- converge to validation -->
  <line x1="450" y1="716" x2="450" y2="742" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="628" y1="716" x2="628" y2="730" stroke="#64748b" stroke-width="1.5"/>
  <line x1="628" y1="730" x2="530" y2="742" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Validation box -->
  <rect x="310" y="742" width="360" height="52" rx="10" fill="#fef3c7" stroke="#fcd34d" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="490" y="762" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="700" fill="#92400e">🔍 Validation — Hallucination Check</text>
  <text x="490" y="780" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="#78350f">Compare LLM temperature vs Live API temperature</text>

  <line x1="490" y1="794" x2="490" y2="814" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Final output -->
  <rect x="210" y="814" width="360" height="28" rx="8" fill="#0d4f8a"/>
  <text x="390" y="833" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#fff">📤 Final Response  ·  source  ·  confidence  ·  verdict</text>
</svg>
```

---

## ✨ Features

- **Dual data source** — choose between CSV or SQLite at runtime
- **FAISS vector search** — fast semantic similarity matching on historical data
- **Live weather fallback** — WeatherAPI.com called when data isn't in the index
- **Gemini LLM responses** — natural language answers via `gemini-2.5-flash` (free tier)
- **Hallucination detection** — LLM temperature vs live API temperature compared automatically
- **Streamlit UI** — chat bubbles, live weather cards, validation panels
- **Deployed on Streamlit Cloud** — accessible from any browser, no setup needed

---

## 🗂️ Project Structure

```
weather_agent/
├── app.py              # Streamlit UI (main entry point)
├── agent.py            # Core agent logic (FAISS → API → LLM → validate)
├── vector_store.py     # Data loading, embedding, FAISS index
├── data_setup.py       # Generates weather.csv + weather.db
├── main.py             # CLI alternative (optional)
├── .env                # API keys (not committed)
├── .env.example        # Key template
├── .gitignore
└── requirements.txt
```

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Embeddings | `sentence-transformers` · `all-MiniLM-L6-v2` |
| Vector DB | FAISS (`IndexFlatIP` · cosine similarity) |
| LLM | Google Gemini 2.5 Flash (free tier) |
| Weather API | WeatherAPI.com (free tier) |
| Data | pandas · SQLite |
| Config | `python-dotenv` |

---

## 🚀 Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/<snairaadarsh>/weather-agent.git
cd weather-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file (copy from `.env.example`):

```
WEATHER_API_KEY=your_weatherapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

| Key | Where to get it | Cost |
|---|---|---|
| `WEATHER_API_KEY` | [weatherapi.com](https://www.weatherapi.com) → Sign up | Free |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) → Get API Key | Free |

### 5. Run

```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## 🌐 Streamlit Cloud Deployment

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select your repo and set `app.py` as the entry point
4. Under **Advanced settings → Secrets**, add:

```toml
WEATHER_API_KEY = "your_weatherapi_key"
GEMINI_API_KEY  = "your_gemini_api_key"
```

5. Click **Deploy** — done!

> **Note:** On Streamlit Cloud, `load_dotenv()` is a no-op. Keys are read from Streamlit Secrets automatically via `os.getenv()`.

---

## 💡 How to Use

1. Open the app
2. In the sidebar, pick **CSV** or **SQLite DB** as the data source
3. Click **⚡ Build / Rebuild Index**
4. Type a weather query or click an example button
5. The agent will:
   - Return a cached result if the city is in the index → **📦 Vector DB**
   - Fetch live data + ask Gemini if not → **🌐 Live API + LLM**
   - Show a validation verdict comparing LLM vs API temperature

---

## 🔍 Agent Decision Logic

```
User query
    │
    ▼
FAISS similarity search
    │
    ├── score ≥ 0.70 ──▶ Return cached historical result
    │                    source: vector_db
    │
    └── score < 0.70 ──▶ WeatherAPI (live data)
                          + Gemini LLM (natural language)
                          + Validation (hallucination check)
                         source: weather_api+llm
```

### Validation logic

| Scenario | Result |
|---|---|
| LLM temp within ±5°C of API temp | ✅ **Accurate** |
| LLM temp differs by more than 5°C | ⚠️ **Possible Hallucination** |
| LLM didn't mention a temperature | ℹ️ **Unverified** |

---

## 📊 Historical Data Coverage

The built-in dataset covers **10 Indian cities** across **2 seasons**:

| City | Dates |
|---|---|
| Delhi, Mumbai, Chennai, Kolkata | Jan 2024 · Jun 2024 |
| Bangalore, Hyderabad, Pune | Jan 2024 · Jun 2024 |
| Jaipur, Ahmedabad, Lucknow | Jan 2024 · Jun 2024 |

Queries for cities **not in this list** (e.g. London, Tokyo) automatically trigger the live API + LLM path.

---

## 📦 requirements.txt

```
pandas
faiss-cpu
sentence-transformers
requests
google-genai
numpy
python-dotenv
streamlit
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
