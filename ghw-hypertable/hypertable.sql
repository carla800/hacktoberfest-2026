-- Sfida GHW: Set up a Tiger Cloud service and create your first Hypertable
-- Eseguite nell'editor SQL di Tiger Cloud, servizio hackathon-ghw (11 ott 2026)

-- 1. Crea la hypertable (divisa in chunk da 7 giorni sulla colonna time)
CREATE TABLE conditions (
  time        TIMESTAMPTZ NOT NULL,
  location    TEXT NOT NULL,
  device      TEXT NOT NULL,
  temperature DOUBLE PRECISION NULL,
  humidity    DOUBLE PRECISION NULL
) WITH (
  tsdb.hypertable,
  tsdb.segmentby = 'device',
  tsdb.orderby = 'time DESC'
);

-- 2. Inserisce letture distribuite su 20 giorni
INSERT INTO conditions (time, location, device, temperature, humidity) VALUES
  (NOW(),                       'cucina',   'sensore-1', 22.5, 55.0),
  (NOW() - INTERVAL '1 hour',   'cucina',   'sensore-1', 21.8, 57.0),
  (NOW() - INTERVAL '2 hours',  'giardino', 'sensore-2', 17.3, 72.0),
  (NOW() - INTERVAL '10 days',  'cucina',   'sensore-1', 23.1, 50.0),
  (NOW() - INTERVAL '20 days',  'giardino', 'sensore-2', 19.6, 68.0);

-- 3. Mostra i chunk creati in automatico (risultato: 3)
SELECT show_chunks('conditions');

-- 4. Temperatura media al giorno per sensore
SELECT time_bucket('1 day', time) AS giorno,
       device,
       ROUND(AVG(temperature)::numeric, 1) AS temp_media
FROM conditions
GROUP BY giorno, device
ORDER BY giorno DESC;