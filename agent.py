"""
agent.py
--------
Core WeatherAgent using:
  - FAISS for vector search
  - WeatherAPI.com for live weather data
  - Google Gemini (free) as the LLM

API keys are loaded from .env file.
"""

import os
import re
import requests
from google import genai
from dotenv import load_dotenv

# ── Load keys from .env ───────────────────────────────────────────────────────
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")

# Configure Gemini once at import time
client = genai.Client(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-2.5-flash"

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

# Temperature match tolerance (°C)
TEMP_TOLERANCE = 3


# ── Weather API ───────────────────────────────────────────────────────────────

def _call_weather_api(city: str) -> dict | None:
    """Fetch current weather from WeatherAPI.com."""
    try:
        resp = requests.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": city},
            timeout=8,
        )
        resp.raise_for_status()
        data    = resp.json()
        current = data["current"]
        return {
            "city":          data["location"]["name"],
            "temperature_c": current["temp_c"],
            "condition":     current["condition"]["text"],
            "humidity_pct":  current["humidity"],
            "wind_kmh":      current["wind_kph"],
        }
    except Exception as e:
        print(f"[WeatherAPI error] {e}")
        return None


# ── Gemini LLM ────────────────────────────────────────────────────────────────

def _call_gemini(query: str) -> str | None:
    """Ask Gemini to answer the weather query."""
    try:
        prompt = (
            "You are a helpful weather assistant. "
            "Give a concise 1-2 sentence weather description. "
            "Always mention an approximate temperature in Celsius.\n\n"
            f"User query: {query}"
        )
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini error] {e}")
        return None


# ── Validation ────────────────────────────────────────────────────────────────

def _extract_temp(text: str) -> float | None:
    """Pull the first number followed by °C or celsius from a string."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:°C|celsius)", text, re.IGNORECASE)
    return float(match.group(1)) if match else None


def _validate(api_data: dict, llm_text: str) -> dict:
    """Compare LLM temperature claim with live API data."""
    llm_temp = _extract_temp(llm_text)
    api_temp = api_data["temperature_c"]

    if llm_temp is None:
        return {
            "status": "unverified",
            "note":   "LLM did not mention a temperature — cannot verify.",
        }

    diff = abs(llm_temp - api_temp)
    if diff <= TEMP_TOLERANCE:
        return {
            "status": "accurate",
            "note":   f"LLM temp ({llm_temp}°C) matches API ({api_temp}°C) within {TEMP_TOLERANCE}°C.",
        }
    return {
        "status": "possible_hallucination",
        "note":   (
            f"LLM temp ({llm_temp}°C) differs from API ({api_temp}°C) "
            f"by {diff:.1f}°C — exceeds tolerance of {TEMP_TOLERANCE}°C."
        ),
    }


# ── City Extractor ────────────────────────────────────────────────────────────

def _extract_city(query: str) -> str:
    """Simple heuristic: looks for 'in <City>' pattern, else last word."""
    match = re.search(r"\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", query)
    if match:
        return match.group(1)
    words = query.split()
    return words[-1] if words else "Delhi"


# ── Main Agent ────────────────────────────────────────────────────────────────

class WeatherAgent:
    def __init__(self, vector_store):
        self.vs = vector_store

    def query(self, user_query: str) -> dict:
        """
        Process a weather query. Returns:
        {
          "query":      str,
          "answer":     str,
          "source":     "vector_db" | "weather_api+llm",
          "confidence": float | None,
          "validation": dict | None,
          "api_data":   dict | None,
        }
        """
        print(f"\n[Agent] Processing: {user_query!r}")

        # ── Step 1 & 2: FAISS vector search ───────────────────────────────
        result = self.vs.search(user_query)

        if result["found"]:
            print(f"[Agent] ✅ Found in vector DB (score={result['score']:.3f})")
            return {
                "query":      user_query,
                "answer":     result["text"],
                "source":     "vector_db",
                "confidence": result["score"],
                "validation": None,
                "api_data":   None,
            }

        # ── Step 3: Not found → live API + Gemini LLM ─────────────────────
        print(f"[Agent] ❌ Not in vector DB (score={result['score']:.3f}) → fetching live data")

        city      = _extract_city(user_query)
        api_data  = _call_weather_api(city)
        llm_text  = _call_gemini(user_query)
        validation = None

        if api_data and llm_text:
            validation = _validate(api_data, llm_text)
            answer = llm_text
        elif api_data:
            answer = (
                f"Current weather in {api_data['city']}: "
                f"{api_data['temperature_c']}°C, {api_data['condition']}, "
                f"humidity {api_data['humidity_pct']}%, wind {api_data['wind_kmh']} km/h."
            )
        elif llm_text:
            answer = llm_text
        else:
            answer = "Sorry, could not retrieve weather information right now."

        return {
            "query":      user_query,
            "answer":     answer,
            "source":     "weather_api+llm",
            "confidence": None,
            "validation": validation,
            "api_data":   api_data,
        }
