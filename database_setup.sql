-- SQLite DB Schema
CREATE TABLE farmer_profiles (
    farmer_id TEXT PRIMARY KEY,
    age INTEGER,
    income REAL,
    loan_amount REAL,
    region TEXT,
    loan_term INTEGER,
    previous_default INTEGER,
    farm_type TEXT
);

CREATE TABLE water_quality (
    farm_id TEXT,
    temp REAL,
    pH REAL,
    ammonia REAL,
    DO REAL,
    turbidity REAL,
    timestamp TEXT
);

CREATE TABLE model_outputs (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id TEXT,
    financial_risk REAL,
    technical_risk REAL,
    result_time TEXT
);
