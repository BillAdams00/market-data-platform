-- Couche 01 : journal des executions d'ingestion

CREATE TABLE ingestion_log (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source           text not null,
    debut             timestamptz not null DEFAULT now(),
    fin              timestamptz,
    statut           text  not null ,
    lignes_traitees  integer ,
    message          text,
    CONSTRAINT chk_ingestion_log_statut
        CHECK (statut IN ('en_cours', 'succes', 'echec'))
);