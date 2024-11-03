-- create the database
CREATE DATABASE IF NOT EXISTS cloud;

-- use database
USE cloud;

-- Create the Users Table
CREATE TABLE IF NOT EXISTS User (
user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL
);

-- Actual Leaderboard
-- Data processing handled in Docker
-- Create the Application Table
CREATE TABLE IF NOT EXISTS Application (
app_id INT AUTO_INCREMENT PRIMARY KEY,
app_name VARCHAR(255) NOT NULL,
    app_avg FLOAT, 
    app_ifeval FLOAT, 
    app_bbh FLOAT, 
    app_mathlvl5 FLOAT, 
    app_gpqa FLOAT, 
    app_musr FLOAT, 
    app_mmlupro FLOAT
);

-- Insert dummy data into User table
INSERT INTO User (user_email, user_password) VALUES
('user@gmail.com', 'password');

-- Insert dummy data into Application table
INSERT INTO Application (app_name, app_avg, app_ifeval, app_bbh, app_mathlvl5, app_gpqa, app_musr, app_mmlupro) VALUES
('APP1', 85.24, 84.32, 78.25, 94.65, 90.55, 76.32, 90.48),
('APP2', 88.54, 97.42, 65.02, 89.56, 85.56, 78.22, 84.54),
('APP3', 75.26, 75.19, 68.62, 85.78, 81.25, 85.26, 89.62),
('APP4', 98.54, 98.02, 78.78, 74.26, 84.05, 97.09, 76.49);
