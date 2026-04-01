-- SQL Injection Training Lab - Database Schema
-- EDUCATIONAL USE ONLY
-- Run: mysql -u root -p < schemas/init.sql

CREATE DATABASE IF NOT EXISTS shopdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shopdb;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user','admin','moderator') DEFAULT 'user',
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL  -- Updated by application on successful authentication
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    stock INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    status ENUM('pending','processing','completed','cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Access logs table (also injectable)
CREATE TABLE IF NOT EXISTS access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table (for reference)
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id INT,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL
);

-- Comments/Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin secrets table (target for privilege escalation)
CREATE TABLE IF NOT EXISTS admin_secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    secret_key VARCHAR(100) NOT NULL,
    secret_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================
-- Sample Data
-- ========================

-- Admin user (password: admin123 -> MD5)
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@shopcorp.com', '0192023a7bbd73250516f069df18b500', 'admin'),
('john_doe', 'john@example.com', '482c811da5d5b4bc6d497ffa98491e38', 'user'),
('jane_smith', 'jane@example.com', '1a1dc91c907325c69271ddf0c944bc72', 'user'),
('testuser', 'test@example.com', '098f6bcd4621d373cade4e832627b4f6', 'user');

-- Products
INSERT INTO products (name, description, price, category) VALUES
('Laptop Pro 15', 'High-performance business laptop with 16GB RAM', 1299.99, 'Electronics'),
('Wireless Mouse', 'Ergonomic wireless mouse, 2.4GHz connectivity', 29.99, 'Electronics'),
('Standing Desk', 'Height-adjustable standing desk, 60 inch wide', 549.00, 'Furniture'),
('Coffee Maker', 'Programmable 12-cup coffee maker with thermal carafe', 89.99, 'Appliances'),
('USB-C Hub', '7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader', 49.99, 'Electronics'),
('Mechanical Keyboard', 'Tenkeyless mechanical keyboard, Cherry MX switches', 129.00, 'Electronics'),
('Monitor 27"', 'IPS panel, 4K resolution, 60Hz refresh rate', 399.99, 'Electronics'),
('Desk Chair', 'Ergonomic mesh chair with lumbar support', 299.00, 'Furniture'),
('Webcam HD', '1080p webcam with built-in microphone', 79.99, 'Electronics'),
('External SSD', '1TB portable SSD, USB 3.2, 1050MB/s read speed', 119.99, 'Electronics');

-- Orders
INSERT INTO orders (user_id, product_id, quantity, status) VALUES
(2, 1, 1, 'completed'),
(2, 5, 2, 'pending'),
(3, 3, 1, 'processing'),
(4, 7, 1, 'pending');

-- Access logs
INSERT INTO access_logs (user_id, action, ip_address) VALUES
(1, 'login', '192.168.1.1'),
(2, 'login', '10.0.0.5'),
(3, 'login', '172.16.0.10');

-- Admin secrets (target data for SQLi challenges)
INSERT INTO admin_secrets (secret_key, secret_value) VALUES
('db_backup_key', 'BACKUP-KEY-7f3d9e2a1b'),
('api_master_token', 'MTK-a1b2c3d4e5f6-MASTER'),
('internal_flag', 'SQLI{congratulations_you_found_the_flag}');

-- Test account passwords:
-- admin: admin123
-- john_doe: password123
-- jane_smith: pass
-- testuser: test
