-- publisher это издательство
-- edition это год издания

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    registration_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    grade INT NOT NULL,
    authors VARCHAR(255) NOT NULL,
    publisher VARCHAR(255),
    edition VARCHAR(255) NOT NULL,
    pages INT NOT NULL,
    url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE paragraphs (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    paragraph_number INT NOT NULL,
    title VARCHAR(255),
    pages VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    paragraph_id INT NOT NULL REFERENCES paragraphs(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    questions TEXT
);