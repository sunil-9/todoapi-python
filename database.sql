-- database.sql
-- Database creation script with schema and sample data for TodoApp

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS todoapp;

-- Use the todoapp database
USE todoapp;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP
);

-- Todos table
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- OTPs table for password reset
CREATE TABLE IF NOT EXISTS otps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    otp VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    INDEX (email)
);

-- Sample data

-- Sample users (passwords are 'password123' hashed with bcrypt)
INSERT INTO users (email, username, hashed_password, is_active) VALUES
('user1@example.com', 'user1', '$2b$12$tPZ2LoA0yEQh8D6GzYgILeIVDqZCCFy4ZO3oCCzH8sHi8JQaFPJnK', TRUE),
('user2@example.com', 'user2', '$2b$12$tPZ2LoA0yEQh8D6GzYgILeIVDqZCCFy4ZO3oCCzH8sHi8JQaFPJnK', TRUE),
('admin@example.com', 'admin', '$2b$12$tPZ2LoA0yEQh8D6GzYgILeIVDqZCCFy4ZO3oCCzH8sHi8JQaFPJnK', TRUE);

-- Sample todos for user1
INSERT INTO todos (title, description, completed, user_id) VALUES
('Complete FastAPI project', 'Finish building the Todo API with all features', FALSE, 1),
('Learn more about SQLAlchemy', 'Study relationships and advanced queries', FALSE, 1),
('Buy groceries', 'Milk, eggs, bread, and vegetables', TRUE, 1);

-- Sample todos for user2
INSERT INTO todos (title, description, completed, user_id) VALUES
('Prepare for meeting', 'Review notes and prepare presentation', FALSE, 2),
('Call dentist', 'Schedule appointment for next week', FALSE, 2),
('Finish reading book', 'Complete chapter 5 and 6', TRUE, 2);

-- Sample todos for admin
INSERT INTO todos (title, description, completed, user_id) VALUES
('Deploy application', 'Deploy the Todo API to production server', FALSE, 3),
('Update documentation', 'Add API usage examples', FALSE, 3),
('Review pull requests', 'Review and merge pending PRs', TRUE, 3);

-- Note: No sample data for OTPs as they are temporary and generated on-demand

-- Display added data
SELECT 'Users added:' AS message;
SELECT id, email, username FROM users;

SELECT 'Todos added:' AS message;
SELECT id, title, completed, user_id FROM todos;
