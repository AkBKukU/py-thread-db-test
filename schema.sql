-- Initialize the database.
-- Drop any existing data and create empty tables.


CREATE TABLE IF NOT EXISTS timestamps(
  key INTEGER PRIMARY KEY ASC,
  wordplace TEXT,
  timeinstance DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat(
  key INTEGER PRIMARY KEY ASC,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  sender TEXT,
  message TEXT,
  channel TEXT
);
