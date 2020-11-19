CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    heading TEXT,
    description TEXT,
    topic INTEGER
);

CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    input TEXT,
    output INTEGER
);
