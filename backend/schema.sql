CREATE DATABASE IF NOT EXISTS zero;
USE zero;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    success BOOLEAN DEFAULT FALSE,
    country VARCHAR(100) DEFAULT 'Unknown',
    city VARCHAR(100) DEFAULT 'Unknown',
    INDEX idx_user (user_id),
    INDEX idx_time (login_time)
);

CREATE TABLE IF NOT EXISTS device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(255),
    mac_address VARCHAR(17),
    os VARCHAR(50),
    trusted BOOLEAN DEFAULT FALSE,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    wifi_ssid VARCHAR(100),
    hostname VARCHAR(100),
    ip_address VARCHAR(45),
    INDEX idx_user (user_id),
    INDEX idx_device (device_id)
);

CREATE TABLE IF NOT EXISTS file_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    action ENUM('READ', 'WRITE', 'DELETE') DEFAULT 'READ',
    ip_address VARCHAR(45),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_time (access_time)
);

-- Insert default users with plain passwords
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'admin'),
('bhargav', 'admin123', 'user')
ON DUPLICATE KEY UPDATE username=username;
