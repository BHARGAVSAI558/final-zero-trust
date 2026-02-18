-- ============================================
-- ZERO TRUST SYSTEM - MySQL Database Schema
-- ============================================
-- Run these queries in MySQL Workbench or Command Line
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS zero_trust;
USE zero_trust;

-- Drop existing tables (if any)
DROP TABLE IF EXISTS file_access_logs;
DROP TABLE IF EXISTS device_logs;
DROP TABLE IF EXISTS login_logs;
DROP TABLE IF EXISTS users;

-- ============================================
-- TABLE 1: USERS
-- Stores user accounts with approval workflow
-- ============================================
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
    INDEX idx_status (status),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 2: LOGIN_LOGS
-- Tracks all login attempts for UEBA analysis
-- ============================================
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    success BOOLEAN DEFAULT TRUE,
    country VARCHAR(100) DEFAULT 'Unknown',
    city VARCHAR(100) DEFAULT 'Unknown',
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time),
    INDEX idx_success (success)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 3: DEVICE_LOGS
-- Stores device fingerprints for tracking
-- ============================================
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
    INDEX idx_device_id (device_id),
    INDEX idx_trusted (trusted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 4: FILE_ACCESS_LOGS
-- Monitors all file access operations
-- ============================================
CREATE TABLE file_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    action VARCHAR(10) DEFAULT 'READ',
    ip_address VARCHAR(45),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_access_time (access_time),
    INDEX idx_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- VERIFY TABLES CREATED
-- ============================================
SHOW TABLES;

-- Check table structures
DESCRIBE users;
DESCRIBE login_logs;
DESCRIBE device_logs;
DESCRIBE file_access_logs;

-- ============================================
-- VERIFICATION QUERY
-- ============================================
SELECT 
    'users' as table_name, 
    COUNT(*) as record_count 
FROM users
UNION ALL
SELECT 'login_logs', COUNT(*) FROM login_logs
UNION ALL
SELECT 'device_logs', COUNT(*) FROM device_logs
UNION ALL
SELECT 'file_access_logs', COUNT(*) FROM file_access_logs;

-- ============================================
-- DATABASE SETUP COMPLETE!
-- ============================================
SELECT '✓ All 4 tables created successfully!' as Status;
SELECT '✓ No default users - Register through application' as Note;
