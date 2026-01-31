-- Initialize the database.
-- Drop any existing data and create empty tables.

CREATE TABLE IF NOT EXISTS action_queue(
  key INTEGER PRIMARY KEY ASC,
  timeinstance DATETIME DEFAULT CURRENT_TIMESTAMP,
  action TEXT,
  name TEXT,
  controller_id TEXT
);
