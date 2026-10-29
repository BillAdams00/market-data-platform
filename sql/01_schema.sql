-- Couche 01 : schéma pivot de l'ingestion

CREATE TABLE serie (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source     text not null,
    code       text not null,
    libelle    text not null,
    unite      text not null,
    devise     char(3) ,
    frequence  text not null,
    CONSTRAINT serie_unique_par_source unique  (source,code)
);

CREATE TABLE observation (
    serie_id          integer NOT NULL REFERENCES serie(id),
    date_observation  date NOT NULL,
    valeur            numeric(18,6) NOT NULL,
    date_ingestion    timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (serie_id,date_observation)
);