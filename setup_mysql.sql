-- Zero Trust System - MySQL Database Setup
-- Run this in MySQL Workbench or Command Line

CREATE DATABASE IF NOT EXISTS zero_trust;
USE zero_trust;

-- Drop existing tables if any
DROP TABLE IF EXISTS file_access_logs;
DROP TABLE IF EXISTS device_logs;
DROP TABLE IF EXISTS login_logs;
DROP TABLE IF EXISTS users;

-- Users table with approval workflow
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'user',
    status VARCHAR(20) DEFAULT 'active',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_status (status)
);

-- Login logs for UEBA analysis
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    success BOOLEAN DEFAULT TRUE,
    country VARCHAR(100) DEFAULT 'Unknown',
    city VARCHAR(100) DEFAULT 'Unknown',
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time)
);

-- Device fingerprints
CREATE TABLE device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(255) UNIQUE,
    mac_address VARCHAR(17),
    os VARCHAR(50),
    trusted BOOLEAN DEFAULT FALSE,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    wifi_ssid VARCHAR(100),
    hostname VARCHAR(100),
    ip_address VARCHAR(45),
    INDEX idx_user_id (user_id),
    INDEX idx_device_id (device_id)
);

-- File access logs for monitoring
CREATE TABLE file_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    action VARCHAR(10) DEFAULT 'READ',
    ip_address VARCHAR(45),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_access_time (access_time)
);

-- Insert default users
INSERT INTO users (username, password, role, status) VALUES 
('admin', 'admin123', 'admin', 'active'),
('bhargav', 'admin123', 'user', 'active');

-- Insert sample data for demo
INSERT INTO login_logs (user_id, ip_address, success, country, city) VALUES
('admin', '127.0.0.1', TRUE, 'India', 'Guntur'),
('bhargav', '127.0.0.1', TRUE, 'India', 'Guntur');

INSERT INTO device_logs (user_id, device_id, mac_address, os, wifi_ssid, hostname, ip_address, trusted) VALUES
('admin', 'DEVICE-ADMIN-001', 'AA:BB:CC:DD:EE:FF', 'Windows 11', 'Home-WiFi', 'ADMIN-PC', '127.0.0.1', TRUE),
('bhargav', 'DEVICE-BHARGAV-001', '11:22:33:44:55:66', 'Windows 11', 'Home-WiFi', 'BHARGAV-PC', '127.0.0.1', TRUE);

-- Verify setup
SELECT 'Users Table' as Table_Name, COUNT(*) as Record_Count FROM users
UNION ALL
SELECT 'Login Logs', COUNT(*) FROM login_logs
UNION ALL
SELECT 'Device Logs', COUNT(*) FROM device_logs
UNION ALL
SELECT 'File Access Logs', COUNT(*) FROM file_access_logs;

SELECT '✓ Database setup complete!' as Status;
