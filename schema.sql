CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE info (
    id SERIAL PRIMARY KEY, 
    destination_id INTEGER REFERENCES destinations, 
    phone_number TEXT, 
    description TEXT
);

CREATE TABLE destinations (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    address TEXT, 
    visible INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    destination_id INTEGER REFERENCES destinations, 
    stars INTEGER, 
    comment TEXT
);

CREATE TABLE userreviews (
    id SERIAL PRIMARY KEY,
    reviewer_id INTEGER REFERENCES users,
    user_id INTEGER REFERENCES users,
    stars INTEGER,
    comment TEXT
);
