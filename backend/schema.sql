CREATE DATABASE IF NOT EXISTS zerotrust;
USE zerotrust;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(100),
    success BOOLEAN DEFAULT TRUE,
    country VARCHAR(100),
    city VARCHAR(100),
    mac_address VARCHAR(100),
    hostname VARCHAR(255),
    device_os VARCHAR(100),
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time)
);

CREATE TABLE IF NOT EXISTS device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    device_id VARCHAR(255),
    mac_address VARCHAR(100),
    os VARCHAR(100),
    os_version VARCHAR(100),
    wifi_ssid VARCHAR(255),
    hostname VARCHAR(255),
    ip_address VARCHAR(100),
    trusted BOOLEAN DEFAULT FALSE,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_device (user_id, device_id),
    INDEX idx_user_id (user_id)
);

CREATE TABLE IF NOT EXISTS file_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    file_name VARCHAR(500),
    file_path TEXT,
    action VARCHAR(50),
    sensitivity_level VARCHAR(50),
    ip_address VARCHAR(100),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_id VARCHAR(255),
    INDEX idx_user_id (user_id),
    INDEX idx_access_time (access_time)
);

CREATE TABLE IF NOT EXISTS network_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    connection_type VARCHAR(100),
    remote_ip VARCHAR(100),
    remote_port INT,
    protocol VARCHAR(50),
    external BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(500) NOT NULL UNIQUE,
    filepath TEXT,
    size BIGINT,
    file_type VARCHAR(100),
    sensitivity VARCHAR(50) DEFAULT 'internal',
    owner VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    INDEX idx_owner (owner),
    INDEX idx_deleted (deleted)
);

INSERT IGNORE INTO users (username, password, role, status) VALUES ('admin', 'admin123', 'admin', 'active');
