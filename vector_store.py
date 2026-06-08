"""
vector_store.py
---------------
Loads data from CSV or SQLite, converts each row to a text sentence,
embeds with sentence-transformers, and stores in a FAISS index.

No external API keys needed here.
"""

import pandas as pd
import sqlite3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Embedding model (downloads ~90 MB on first run)
MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.70   # cosine similarity; below this → "not found"


def load_data(source: str) -> pd.DataFrame:
    """Load weather data from 'csv' or 'db'."""
    if source == "csv":
        df = pd.read_csv("weather.csv")
        print("[✓] Loaded data from weather.csv")
    elif source == "db":
        conn = sqlite3.connect("weather.db")
        df = pd.read_sql("SELECT * FROM weather", conn)
        conn.close()
        print("[✓] Loaded data from weather.db")
    else:
        raise ValueError("source must be 'csv' or 'db'")
    return df


def rows_to_text(df: pd.DataFrame) -> list[str]:
    """Convert each DataFrame row into a descriptive sentence."""
    texts = []
    for _, row in df.iterrows():
        t = (
            f"Weather in {row['city']} on {row['date']}: "
            f"temperature {row['temperature_c']}°C, "
            f"condition {row['condition']}, "
            f"humidity {row['humidity_pct']}%, "
            f"wind {row['wind_kmh']} km/h."
        )
        texts.append(t)
    return texts


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = None
        self.texts = []

    def build(self, df: pd.DataFrame):
        """Embed all rows and store in FAISS."""
        self.texts = rows_to_text(df)
        embeddings = self.model.encode(self.texts, normalize_embeddings=True)
        dim = embeddings.shape[1]
        # Inner-product on L2-normalised vectors == cosine similarity
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(np.array(embeddings, dtype="float32"))
        print(f"[✓] FAISS index built with {len(self.texts)} vectors (dim={dim})")

    def search(self, query: str, top_k: int = 1) -> dict:
        """
        Search FAISS for the most similar entry.

        Returns:
            {
              "found": bool,
              "score": float,
              "text": str | None
            }
        """
        q_vec = self.model.encode([query], normalize_embeddings=True)
        scores, indices = self.index.search(np.array(q_vec, dtype="float32"), top_k)
        best_score = float(scores[0][0])
        best_idx   = int(indices[0][0])

        if best_score >= SIMILARITY_THRESHOLD:
            return {"found": True,  "score": best_score, "text": self.texts[best_idx]}
        return     {"found": False, "score": best_score, "text": None}
