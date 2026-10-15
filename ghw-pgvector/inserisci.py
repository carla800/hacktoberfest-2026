import os
import ollama
import psycopg
from dotenv import load_dotenv

load_dotenv()

# Note di prova di un piccolo negozio online: (categoria, testo, quanti giorni fa)
NOTE = [
    ("pagamenti",   "La carta di credito del cliente è stata rifiutata al checkout", 1),
    ("pagamenti",   "Un cliente chiede il rimborso perché ha pagato due volte lo stesso ordine", 3),
    ("spedizioni",  "Il pacco è fermo in magazzino da una settimana e il cliente è arrabbiato", 2),
    ("spedizioni",  "Il corriere ha consegnato all'indirizzo sbagliato", 8),
    ("prodotti",    "La taglia M della felpa verde è esaurita, quando torna disponibile?", 4),
    ("prodotti",    "Le scarpe da corsa sono arrivate con un difetto sulla suola", 12),
    ("account",     "Non riesco ad accedere, ho dimenticato la password", 5),
    ("account",     "Vorrei cancellare il mio account e tutti i miei dati", 20),
    ("negozio",     "Fate sconti per chi compra più di cinque articoli?", 6),
    ("negozio",     "Il sito è lentissimo da telefono e non carica le foto", 15),
]


def embedding(testo):
    """Chiede a Gemma le coordinate di significato di un testo."""
    risposta = ollama.embed(model="embeddinggemma", input=testo)
    return risposta["embeddings"][0]


with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME"),
    sslmode="require",
) as conn:
    for categoria, testo, giorni_fa in NOTE:
        vettore = embedding(testo)
        conn.execute(
            """
            INSERT INTO note (created_at, categoria, testo, embedding)
            VALUES (NOW() - make_interval(days => %s), %s, %s, %s::vector)
            """,
            (giorni_fa, categoria, testo, str(vettore)),
        )
        print("Salvata:", testo[:50])

print("Fatto! Note salvate:", len(NOTE))