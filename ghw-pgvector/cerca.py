import os
import argparse
import ollama
import psycopg
from dotenv import load_dotenv

load_dotenv()

# Legge domanda e filtri dalla riga di comando
parser = argparse.ArgumentParser(description="Cerca note per significato")
parser.add_argument("domanda", nargs="+", help="la domanda da cercare")
parser.add_argument("--giorni", type=int, help="solo note degli ultimi N giorni")
parser.add_argument("--categoria", help="solo note di questa categoria")
parser.add_argument("--soglia", type=float, default=0.6, help="somiglianza minima, da 0 a 1")
args = parser.parse_args()
domanda = " ".join(args.domanda)


def embedding(testo):
    risposta = ollama.embed(model="embeddinggemma", input=testo)
    return risposta["embeddings"][0]


parametri = {
    "vettore": str(embedding(domanda)),
    "giorni": args.giorni,        # None se non indicato
    "categoria": args.categoria,  # None se non indicata
    "soglia": args.soglia,
}

with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME"),
    sslmode="require",
) as conn:
    risultati = conn.execute(
        """
        SELECT testo, categoria, created_at::date,
               1 - (embedding <=> %(vettore)s::vector) AS somiglianza
        FROM note
        WHERE (%(giorni)s::int IS NULL
               OR created_at > NOW() - make_interval(days => %(giorni)s::int))
          AND (%(categoria)s::text IS NULL OR categoria = %(categoria)s::text)
          AND 1 - (embedding <=> %(vettore)s::vector) >= %(soglia)s
        ORDER BY embedding <=> %(vettore)s::vector
        LIMIT 3
        """,
        parametri,
    ).fetchall()

filtri = []
if args.giorni:
    filtri.append(f"ultimi {args.giorni} giorni")
if args.categoria:
    filtri.append(f"categoria {args.categoria}")

print("Domanda:", domanda)
print("Filtri:", ", ".join(filtri) if filtri else "nessuno", "\n")
if not risultati:
    print("Nessuna nota trovata con questi filtri.")
for testo, categoria, data, somiglianza in risultati:
    print(f"{somiglianza:.2f}  [{categoria}, {data}]  {testo}")