"""
app.py  —  WeatherAgent UI
Run:  streamlit run app.py
"""

import re
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WeatherAgent",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');

:root {
  --blue:    #1a6fbc; --blue-dk: #0d4f8a;
  --teal:    #0fb5ae; --accent:  #f58c27;
  --bg:      #f4f8fc; --card:    #ffffff;
  --text:    #1a2332; --muted:   #6b7c93;
  --border:  #dce7f3;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d4f8a 0%, #1a6fbc 100%) !important;
  border-right: none !important;
}
[data-testid="stSidebar"] * { color: #e8f4fd !important; }
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,0.12) !important;
  border: 1px solid rgba(255,255,255,0.22) !important;
  color: #fff !important; border-radius: 8px !important;
  font-size: 0.82rem !important; transition: background 0.2s;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,0.22) !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.85rem !important; }

/* Title */
.page-title {
  font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800;
  color: var(--blue-dk); letter-spacing: -0.5px; margin-bottom: 0;
}
.page-sub { color: var(--muted); font-size: 0.92rem; margin-top: 2px; margin-bottom: 1.4rem; }

/* Chat bubbles */
.chat-row { display: flex; gap: 10px; margin-bottom: 10px; align-items: flex-start; }
.chat-row.user { flex-direction: row-reverse; }
.avatar {
  width: 34px; height: 34px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0;
}
.avatar.user-av { background: var(--accent); }
.avatar.bot-av  { background: var(--blue); }
.bubble {
  max-width: 72%; padding: 12px 16px; border-radius: 16px;
  font-size: 0.93rem; line-height: 1.6; box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.bubble.user-bubble { background: var(--blue); color: #fff; border-bottom-right-radius: 4px; }
.bubble.bot-bubble  {
  background: var(--card); color: var(--text);
  border: 1px solid var(--border); border-bottom-left-radius: 4px;
}
.chip {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.3px; margin-top: 6px;
}
.chip-db   { background: #dcfce7; color: #15803d; }
.chip-live { background: #fef9c3; color: #92400e; }
.score-badge {
  display: inline-block; padding: 2px 8px; background: #e0f2fe; color: #0369a1;
  border-radius: 12px; font-size: 0.72rem; font-weight: 600; margin-left: 6px;
}

/* Live weather card */
.wx-card {
  background: linear-gradient(135deg, #1a6fbc 0%, #0fb5ae 100%);
  border-radius: 14px; padding: 16px 20px; color: #fff;
  margin-top: 8px; display: flex; gap: 16px; flex-wrap: wrap;
  box-shadow: 0 4px 18px rgba(26,111,188,0.22);
}
.wx-metric { text-align: center; flex: 1; min-width: 70px; }
.wx-metric .val { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; }
.wx-metric .lbl { font-size: 0.7rem; opacity: 0.78; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px; }

/* Temp comparison boxes */
.temp-compare-wrap { display: flex; gap: 12px; align-items: stretch; margin: 8px 0; flex-wrap: wrap; }
.temp-box {
  flex: 1; min-width: 110px; text-align: center;
  padding: 14px 10px; border-radius: 12px;
}
.temp-box.llm  { background: #ede9fe; border: 1.5px solid #c4b5fd; }
.temp-box.api  { background: #dbeafe; border: 1.5px solid #93c5fd; }
.temp-box .t-val   { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; }
.temp-box.llm .t-val { color: #6d28d9; }
.temp-box.api .t-val { color: #1d4ed8; }
.temp-box .t-src   { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; color: #6b7c93; }
.temp-box .t-label { font-size: 0.78rem; font-weight: 600; margin-bottom: 6px; }
.temp-box.llm .t-label { color: #7c3aed; }
.temp-box.api .t-label { color: #1e40af; }

/* Verdict banner */
.verdict {
  border-radius: 10px; padding: 12px 16px; margin-top: 8px;
  font-size: 0.88rem; font-weight: 500; display: flex; align-items: center; gap: 10px;
}
.verdict.ok   { background: #f0fdf4; border: 1.5px solid #86efac; color: #15803d; }
.verdict.warn { background: #fff7ed; border: 1.5px solid #fdba74; color: #c2410c; }
.verdict.info { background: #f0f9ff; border: 1.5px solid #bae6fd; color: #0369a1; }
.verdict-icon { font-size: 1.3rem; flex-shrink: 0; }
.verdict-text strong { display: block; font-family: 'Syne', sans-serif; font-size: 0.82rem; letter-spacing: 0.3px; }

/* Banner */
.idx-banner {
  background: linear-gradient(90deg, #0d4f8a, #1a6fbc);
  color: #fff; border-radius: 10px; padding: 10px 16px;
  font-size: 0.84rem; margin-bottom: 14px;
}
.city-pill {
  display: inline-block; background: rgba(255,255,255,0.15);
  border-radius: 20px; padding: 2px 10px; font-size: 0.75rem; margin: 2px;
}
.empty-state { text-align: center; padding: 60px 20px; color: var(--muted); }
.empty-state .icon { font-size: 3rem; margin-bottom: 12px; }
.empty-state h3 { font-family: 'Syne', sans-serif; color: var(--blue-dk); margin-bottom: 8px; }

[data-testid="stChatInput"] {
  border-radius: 12px !important; border: 2px solid var(--border) !important;
  box-shadow: 0 2px 10px rgba(26,111,188,0.08) !important;
}
[data-testid="stChatInput"]:focus-within { border-color: var(--blue) !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in {
    "messages": [], "agent": None,
    "index_ready": False, "data_source": "csv", "index_stats": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;padding:8px 0 2px'>🌦️ WeatherAgent</div>", unsafe_allow_html=True)
    st.caption("AI-Powered Weather Assistant")
    st.divider()

    st.markdown("**Data Source**")
    source_choice = st.radio("Load from:", ["CSV (weather.csv)", "SQLite DB (weather.db)"],
                              index=0, label_visibility="collapsed")
    source_key = "csv" if "CSV" in source_choice else "db"
    st.divider()

    if st.button("⚡  Build / Rebuild Index", use_container_width=True):
        with st.spinner("Building index…"):
            try:
                from data_setup import create_csv, create_db
                from vector_store import VectorStore, load_data
                from agent import WeatherAgent

                if not os.path.exists("weather.csv") or not os.path.exists("weather.db"):
                    df_setup = create_csv(); create_db(df_setup)

                df = load_data(source_key)
                vs = VectorStore(); vs.build(df)

                st.session_state.agent       = WeatherAgent(vs)
                st.session_state.index_ready = True
                st.session_state.data_source = source_key
                st.session_state.index_stats = {
                    "source": source_key, "vectors": len(vs.texts),
                    "cities": sorted(df["city"].unique().tolist()), "rows": len(df),
                }
                st.success(f"✅ {len(vs.texts)} vectors ready!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.index_ready and st.session_state.index_stats:
        s = st.session_state.index_stats
        st.markdown(f"<div style='font-size:0.78rem;opacity:0.85;line-height:1.7'>"
                    f"<b>Source:</b> {s['source'].upper()}&nbsp;&nbsp;"
                    f"<b>Rows:</b> {s['rows']}&nbsp;&nbsp;"
                    f"<b>Vectors:</b> {s['vectors']}</div>", unsafe_allow_html=True)
        cities_html = "".join(f"<span class='city-pill'>🏙 {c}</span>" for c in s["cities"])
        st.markdown(f"<div style='margin-top:6px'>{cities_html}</div>", unsafe_allow_html=True)
    else:
        st.info("No index yet. Click **Build Index** to start.")

    st.divider()
    st.markdown("**💡 Try asking**")
    for ex in ["What is the weather in Delhi?", "How is the weather in Mumbai?",
               "Weather in Bangalore today", "Temperature in London?", "Weather in Tokyo"]:
        if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
            st.session_state["prefill_query"] = ex
            st.rerun()

    st.divider()
    if st.button("🧹  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_temp(text: str):
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:°C|celsius)", text or "", re.IGNORECASE)
    return float(m.group(1)) if m else None


def render_wx_card(api_data: dict):
    """Gradient live-data card using pure Streamlit columns."""
    st.markdown(f"""
    <div class='wx-card'>
      <div class='wx-metric'><div class='val'>{api_data['temperature_c']}°C</div><div class='lbl'>Temperature</div></div>
      <div class='wx-metric'><div class='val'>{api_data['condition']}</div><div class='lbl'>Condition</div></div>
      <div class='wx-metric'><div class='val'>{api_data['humidity_pct']}%</div><div class='lbl'>Humidity</div></div>
      <div class='wx-metric'><div class='val'>{api_data['wind_kmh']} km/h</div><div class='lbl'>Wind</div></div>
    </div>""", unsafe_allow_html=True)


def render_validation_panel(val: dict, api_data: dict, answer_text: str):
    """
    Shows LLM answer temp vs Live API temp side-by-side,
    then a clear verdict using native Streamlit so nothing escapes as code.
    """
    if not val:
        return

    status   = val.get("status", "unverified")
    api_temp = api_data.get("temperature_c") if api_data else None
    llm_temp = _extract_temp(answer_text)

    st.markdown("---")

    # ── Temperature comparison (two columns) ──────────────────────────────
    if llm_temp is not None or api_temp is not None:
        col_l, col_mid, col_r = st.columns([5, 1, 5])

        with col_l:
            if llm_temp is not None:
                st.markdown(f"""
                <div class='temp-box llm'>
                  <div class='t-label'>🤖 Gemini LLM said</div>
                  <div class='t-val'>{llm_temp}°C</div>
                  <div class='t-src'>From AI response</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='temp-box llm'>
                  <div class='t-label'>🤖 Gemini LLM said</div>
                  <div class='t-val' style='font-size:1rem;padding-top:6px'>No temp<br>mentioned</div>
                  <div class='t-src'>From AI response</div>
                </div>""", unsafe_allow_html=True)

        with col_mid:
            st.markdown("<div style='text-align:center;font-size:1.6rem;padding-top:28px;color:#94a3b8'>⟷</div>",
                        unsafe_allow_html=True)

        with col_r:
            if api_temp is not None:
                st.markdown(f"""
                <div class='temp-box api'>
                  <div class='t-label'>🌐 Live API returned</div>
                  <div class='t-val'>{api_temp}°C</div>
                  <div class='t-src'>WeatherAPI.com</div>
                </div>""", unsafe_allow_html=True)

    # ── Verdict banner ────────────────────────────────────────────────────
    if status == "accurate" and llm_temp is not None and api_temp is not None:
        diff = abs(llm_temp - api_temp)
        st.markdown(f"""
        <div class='verdict ok'>
          <div class='verdict-icon'>✅</div>
          <div class='verdict-text'>
            <strong>LLM Answer Verified</strong>
            Difference is {diff:.1f}°C — within the 3°C tolerance. The AI response is accurate.
          </div>
        </div>""", unsafe_allow_html=True)

    elif status == "possible_hallucination" and llm_temp is not None and api_temp is not None:
        diff = abs(llm_temp - api_temp)
        st.markdown(f"""
        <div class='verdict warn'>
          <div class='verdict-icon'>⚠️</div>
          <div class='verdict-text'>
            <strong>Possible Hallucination</strong>
            Difference is {diff:.1f}°C — exceeds the 3°C tolerance. LLM may have given an inaccurate temperature.
          </div>
        </div>""", unsafe_allow_html=True)

    else:  # unverified
        st.markdown("""
        <div class='verdict info'>
          <div class='verdict-icon'>ℹ️</div>
          <div class='verdict-text'>
            <strong>Could Not Verify</strong>
            The LLM response didn't include a temperature value, so no comparison was possible.
          </div>
        </div>""", unsafe_allow_html=True)


def render_message(msg: dict):
    role = msg["role"]
    text = msg["content"]
    meta = msg.get("meta", {})

    if role == "user":
        st.markdown(f"""
        <div class='chat-row user'>
          <div class='avatar user-av'>🙂</div>
          <div class='bubble user-bubble'>{text}</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Assistant bubble ──
    src  = meta.get("source", "")
    conf = meta.get("confidence")

    if src == "vector_db":
        src_chip = "<span class='chip chip-db'>📦 Vector DB</span>"
    elif src:
        src_chip = "<span class='chip chip-live'>🌐 Live API + LLM</span>"
    else:
        src_chip = ""

    score = f"<span class='score-badge'>similarity {conf:.2f}</span>" if conf is not None else ""

    st.markdown(f"""
    <div class='chat-row'>
      <div class='avatar bot-av'>🌦</div>
      <div class='bubble bot-bubble'>
        {text}
        <div style='margin-top:8px'>{src_chip}{score}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Below-bubble extras — only for live API responses ──
    api_data = meta.get("api_data")
    val      = meta.get("validation")

    if api_data or val:
        with st.container():
            col, _ = st.columns([3, 1])
            with col:
                if api_data:
                    render_wx_card(api_data)
                if val:
                    render_validation_panel(val, api_data or {}, text)


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("<div class='page-title'>🌦️ WeatherAgent</div>", unsafe_allow_html=True)
st.markdown("<div class='page-sub'>Ask about current or historical weather anywhere in the world</div>",
            unsafe_allow_html=True)

if st.session_state.index_ready:
    s = st.session_state.index_stats
    st.markdown(
        f"<div class='idx-banner'>✅ &nbsp;<b>Index active</b> — {s['vectors']} vectors "
        f"from {s['source'].upper()} · {len(s['cities'])} cities loaded</div>",
        unsafe_allow_html=True,
    )

# ── Chat history ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class='empty-state'>
      <div class='icon'>🌤️</div>
      <h3>Ask me anything about the weather</h3>
      <p>Try one of the example queries on the left, or type your own question below.</p>
    </div>""", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        render_message(msg)

# ── Chat input ────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill_query", "")
prompt  = st.chat_input("Ask about weather anywhere… e.g. 'What's the weather in Delhi?'") or prefill

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message({"role": "user", "content": prompt})

    with st.spinner("Checking weather data…"):
        if not st.session_state.index_ready or st.session_state.agent is None:
            response_text = "⚠️ Please build the index first — click **Build / Rebuild Index** in the sidebar."
            meta = {}
        else:
            try:
                result        = st.session_state.agent.query(prompt)
                response_text = result["answer"]
                meta          = {
                    "source":     result["source"],
                    "confidence": result["confidence"],
                    "validation": result["validation"],
                    "api_data":   result.get("api_data"),
                }
            except Exception as e:
                response_text = f"Something went wrong: {e}"
                meta = {}

    bot_msg = {"role": "assistant", "content": response_text, "meta": meta}
    st.session_state.messages.append(bot_msg)
    render_message(bot_msg)