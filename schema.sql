-- Written by ChatGPT with the prompt
-- Write the schema for the database table that will store the configuration 
-- settings that will be used in the various configuration files

CREATE TABLE configuration (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  value TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- another prompt

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    summary VARCHAR(300),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL,
    markdown_path TEXT NOT NULL,
    image_url TEXT
);

