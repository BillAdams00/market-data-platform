

INSERT INTO serie (source, code, libelle, unite, devise, frequence) VALUES
  ('alphavantage', 'NVDA',     'Nvidia - cours de cloture', 'prix', 'USD', 'quotidienne'),
('frankfurter',  'EURUSD',   'Taux de change EUR/USD',    'taux', NULL,  'quotidienne'),
('fred',         'FEDFUNDS', 'Taux directeur de la Fed',  'pct',  NULL,  'mensuelle')
ON CONFLICT (source,code ) DO nothing;


INSERT INTO observation (serie_id, date_observation, valeur) VALUES
  ((SELECT id FROM serie WHERE source='alphavantage' AND code='NVDA'), '2026-10-15', 178.200000),
((SELECT id FROM serie WHERE source='alphavantage' AND code='NVDA'), '2026-10-16', 181.450000),
((SELECT id FROM serie WHERE source='alphavantage' AND code='NVDA'), '2026-10-19', 179.900000),
((SELECT id FROM serie WHERE source='alphavantage' AND code='NVDA'), '2026-10-20', 185),

-- EUR/USD : quatre seances, dont deux taux identiques
((SELECT id FROM serie WHERE source='frankfurter' AND code='EURUSD'), '2026-10-15', 1.081200),
((SELECT id FROM serie WHERE source='frankfurter' AND code='EURUSD'), '2026-10-16', 1.082900),
((SELECT id FROM serie WHERE source='frankfurter' AND code='EURUSD'), '2026-10-19', 1.083400),
((SELECT id FROM serie WHERE source='frankfurter' AND code='EURUSD'), '2026-10-20', 2.083400),

-- FEDFUNDS : trois mois, dates au premier du mois
((SELECT id FROM serie WHERE source='fred' AND code='FEDFUNDS'), '2026-08-01', 4.000000),
((SELECT id FROM serie WHERE source='fred' AND code='FEDFUNDS'), '2026-09-01', 3.875000),
((SELECT id FROM serie WHERE source='fred' AND code='FEDFUNDS'), '2026-10-01', 6.750000)
ON CONFLICT (serie_id, date_observation) DO UPDATE
  SET valeur         = excluded.valeur,
      date_ingestion = now()
  WHERE observation.valeur IS DISTINCT FROM excluded.valeur;