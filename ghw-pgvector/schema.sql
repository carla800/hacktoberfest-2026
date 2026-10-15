-- Run once in your Postgres SQL editor (e.g. Tiger Cloud)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE note (
  id         BIGSERIAL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  categoria  TEXT,
  testo      TEXT NOT NULL,
  embedding  VECTOR(768)
);