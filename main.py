"""
main.py
-------
Entry point for the Weather Query Agent.

Steps:
  1. Ask user to pick data source (csv or db).
  2. Load data → build FAISS index.
  3. Accept queries in a loop and print structured results.

Run:
  python main.py
"""

from data_setup   import create_csv, create_db
from vector_store import VectorStore, load_data
from agent        import WeatherAgent
import os


def print_result(res: dict):
    print("\n" + "═" * 55)
    print(f"  Query   : {res['query']}")
    print(f"  Answer  : {res['answer']}")
    print(f"  Source  : {res['source']}")
    if res["confidence"] is not None:
        print(f"  Confidence : {res['confidence']:.3f}")
    if res["validation"]:
        v = res["validation"]
        print(f"  Validation : [{v['status'].upper()}] {v['note']}")
    if res["api_data"]:
        d = res["api_data"]
        print(
            f"  API Data   : {d['city']} | {d['temperature_c']}°C | "
            f"{d['condition']} | Humidity {d['humidity_pct']}%"
        )
    print("═" * 55)


def main():
    # ── Ensure data files exist ───────────────────────────────────────
    if not os.path.exists("weather.csv") or not os.path.exists("weather.db"):
        print("[Setup] Generating weather.csv and weather.db ...")
        df = create_csv()
        create_db(df)

    # ── Choose data source ────────────────────────────────────────────
    print("\nSelect data source:")
    print("  1 → CSV  (weather.csv)")
    print("  2 → DB   (weather.db)")
    choice = input("Enter 1 or 2: ").strip()
    source = "csv" if choice != "2" else "db"

    # ── Load + embed ──────────────────────────────────────────────────
    df = load_data(source)
    vs = VectorStore()
    vs.build(df)

    # ── Create agent ──────────────────────────────────────────────────
    agent = WeatherAgent(vs)

    # ── Query loop ────────────────────────────────────────────────────
    print("\nWeather Agent ready. Type 'exit' to quit.\n")
    while True:
        query = input("Your query: ").strip()
        if not query or query.lower() == "exit":
            print("Goodbye!")
            break
        result = agent.query(query)
        print_result(result)


if __name__ == "__main__":
    main()
