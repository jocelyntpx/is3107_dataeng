-- create stock table
CREATE TABLE IF NOT EXISTS stock_esg (
    Stock_Ticker VARCHAR NOT NULL,
    Environment_Score NUMERIC NOT NULL,
    Esg_Performance VARCHAR,
    Governance_Score NUMERIC NOT NULL,
    Peer_Count INTEGER NOT NULL,
    Peer_Group VARCHAR NOT NULL,
    Social_Score NUMERIC NOT NULL
    );
