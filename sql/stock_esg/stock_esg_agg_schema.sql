-- create stock table
CREATE TABLE IF NOT EXISTS stock_esg_agg (
    Peer_Group VARCHAR NOT NULL,
    Environment_Score_Avg NUMERIC NOT NULL,
    Governance_Score_Avg NUMERIC NOT NULL,
    Social_Score_Avg NUMERIC NOT NULL
    );
