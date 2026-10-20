-- Initialize database for Exercise 04
CREATE DATABASE IF NOT EXISTS devopsdb;
USE devopsdb;

CREATE TABLE IF NOT EXISTS visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    endpoint VARCHAR(100)
);

INSERT INTO visits (endpoint) VALUES ('/init');
