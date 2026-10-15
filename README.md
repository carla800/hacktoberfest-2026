# Hacktoberfest 2026 – Global Hack Week exercises

Two small exercises built during MLH Global Hack Week: Hacktoberfest (October 9–15, 2026), from the Tiger Data challenges. Sample notes and queries are in Italian on purpose, to test EmbeddingGemma's multilingual support.

## 1. First hypertable (`ghw-hypertable/`)

A TimescaleDB hypertable for sensor readings on Tiger Cloud. The script creates the table with `tsdb.hypertable`, inserts readings spanning 20 days (TimescaleDB creates 3 chunks automatically, checked with `show_chunks`) and computes the daily average temperature per device with `time_bucket`.

## 2. Semantic search with pgvector (`ghw-pgvector/`)

Search by meaning over short customer-support notes of a small online shop.

- **Embeddings:** EmbeddingGemma (Google, open weights), running locally with Ollama
- **Storage and search:** Postgres on Tiger Cloud with pgvector (`VECTOR(768)`)
- **One SQL query** combines cosine similarity (`<=>`), optional filters on time range and category, and a minimum similarity threshold

Example: _"voglio i soldi indietro"_ ("I want my money back") finds the refund note, with no words in common.

### Run it

Requirements: Python 3.11+, [Ollama](https://ollama.com), a Postgres database with pgvector (the Tiger Cloud free plan works).

```
ollama pull embeddinggemma
cd ghw-pgvector
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

1. Run `schema.sql` in your database.
2. Copy `.env.example` to `.env` and fill in your database credentials.
3. Then:

```
python test.py        # checks Ollama and the database connection
python inserisci.py   # embeds and saves 10 sample notes (run once)
python cerca.py voglio i soldi indietro --soglia 0.5
python cerca.py il cliente è arrabbiato --categoria spedizioni --giorni 10 --soglia 0.6
```

### What I learned

- Embeddings capture what a text is _about_, not what _follows_ from it: "I want my money back" doesn't find the note about defective shoes. Linking the two needs a model that reasons over the results (RAG).
- `LIMIT 3` always returns 3 rows, even irrelevant ones. Relevant notes scored about 0.67–0.70 and background noise about 0.50, so a 0.6 threshold makes an honest "no results" possible.
- There is no perfect threshold: the default 0.6 hides the noise, but it also hides the refund note for "voglio i soldi indietro" (0.51). With such short notes the gap between a real match and noise is small; longer texts or a reranking step would help.

## Screenshots

See the `screenshot/` folder: query results for both exercises.
