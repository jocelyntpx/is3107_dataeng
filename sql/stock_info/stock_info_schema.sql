-- create stock table
CREATE TABLE IF NOT EXISTS stock_info (
    Stock_Ticker VARCHAR NOT NULL,
    Enterprise_Value NUMERIC,
    EBITDA NUMERIC ,
    Revenue NUMERIC ,
    Forward_PE NUMERIC NOT NULL,
    Market_Cap NUMERIC NOT NULL,
    PEG_Ratio NUMERIC ,
    Price_Book NUMERIC NOT NULL,
    Price_Sales NUMERIC NOT NULL,
    Trailing_PE NUMERIC NOT NULL,
    EV_Scale INTEGER ,
    MC_Scale INTEGER NOT NULL
    );
