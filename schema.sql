CREATE TABLE "Background" (
    index INTEGER PRIMARY KEY,
    angles FLOAT NOT NULL,
    scan FLOAT NOT NULL
);

CREATE TABLE "Angles" (
    index INTEGER PRIMARY KEY,
    degree FLOAT NOT NULL,
    radian FLOAT NOT NULL
);

CREATE TABLE "Scans" (
    timestamp TIMESTAMP PRIMARY KEY NOT NULL,
    scan VARCHAR NOT NULL
);