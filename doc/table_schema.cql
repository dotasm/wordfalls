CREATE KEYSPACE sea WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

CREATE TABLE sea.v1_word_count (
    word text PRIMARY KEY,
    count counter
);

CREATE TABLE sea.v1_word_explain (
    word text,    
    explain text,
    ts bigint,
    PRIMARY KEY (word)
);

