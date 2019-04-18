DROP DATABASE IF EXISTS pastebing;
CREATE DATABASE pastebing;

\c pastebing

CREATE TABLE users (
  id serial PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT
);

CREATE TABLE pastes (
  id TEXT PRIMARY KEY, -- base58 encoded tuple, userid:pasteid [vry secure - carey 2019]
  title TEXT DEFAULT '',
  author INTEGER REFERENCES users(id),
  contents TEXT,
  created_at TIMESTAMP DEFAULT now()
);

INSERT INTO users (id, username, password) VALUES
  (0, 'test', 'test');
  

-- Reset sequence numbers
SELECT setval(pg_get_serial_sequence('users', 'id'), MAX(id)) FROM users;

DROP USER IF EXISTS pastebing;

CREATE USER pastebing WITH ENCRYPTED PASSWORD '4e34134b-58ee-403a-9229-ddf2d66b0c45';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pastebing;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO pastebing;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pastebing;
GRANT CREATE ON DATABASE pastebing TO pastebing;