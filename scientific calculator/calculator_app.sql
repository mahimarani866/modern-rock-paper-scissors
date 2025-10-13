-- Create the database if it doesn't exist:
CREATE DATABASE IF NOT EXISTS calculator_app;

-- Select the database to work with:
USE calculator_app;

-- Create the history table:
CREATE TABLE IF NOT EXISTS history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expression VARCHAR(255) NOT NULL,
    result VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
