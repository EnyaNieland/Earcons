CREATE TABLE IF NOT EXISTS graph (
    id integer PRIMARY KEY,
    uri text NOT NULL UNIQUE,
    metrics integer,
    FOREIGN KEY (metrics) REFERENCES metrics (id)
);
