-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS timestamps;
DROP TABLE IF EXISTS chat;

CREATE TABLE timestamps(
  key INTEGER PRIMARY KEY ASC,
  wordplace TEXT,
  timeinstance DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat(
  key INTEGER PRIMARY KEY ASC,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  sender TEXT,
  message TEXT
);
