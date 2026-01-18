-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS timestamps;

CREATE TABLE timestamps(
  key INTEGER PRIMARY KEY ASC,
  wordplace TEXT,
  timeinstance DATETIME DEFAULT CURRENT_TIMESTAMP
);
