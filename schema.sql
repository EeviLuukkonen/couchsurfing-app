CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE destinations (
    id SERIAL PRIMARY KEY
    address TEXT
    phone_number TEXT
    description TEXT
);