-- create stock table
CREATE TABLE IF NOT EXISTS stock_price (
    Date DATE NOT NULL,
    Open NUMERIC NOT NULL,
    High NUMERIC NOT NULL,
    Low NUMERIC NOT NULL,
    Close NUMERIC NOT NULL,
    Adj_Close NUMERIC NOT NULL,
    Volume NUMERIC NOT NULL,
    Log_Returns NUMERIC NOT NULL,
    Pct_Returns NUMERIC NOT NULL,
    Stock_Ticker VARCHAR NOT NULL
    );


