CREATE TABLE IF NOT EXISTS metrics (
    id integer PRIMARY KEY,
    nodes integer,
    in_degree integer,
    out_degree integer,
    FOREIGN KEY (in_degree) REFERENCES complicated_metrics (id),
    FOREIGN KEY (out_degree) REFERENCES complicated_metrics (id)
);
