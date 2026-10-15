import os
import ollama
import psycopg
from dotenv import load_dotenv

load_dotenv()  # legge le credenziali dal file .env

# 1. Prova Gemma: trasforma una frase in vettore
risposta = ollama.embed(model="embeddinggemma", input="Ciao, questa è una prova")
vettore = risposta["embeddings"][0]
print("Numeri nel vettore:", len(vettore))
print("Primi 5 numeri:", vettore[:5])

# 2. Prova il database: si collega e chiede la versione di Postgres
with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME"),
    sslmode="require",
) as conn:
    versione = conn.execute("SELECT version();").fetchone()[0]
    print("Collegata a:", versione[:40])