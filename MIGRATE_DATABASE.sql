-- ============================================
-- ZERO TRUST ADVANCED DATABASE MIGRATION
-- Drop old tables and create new advanced schema
-- ============================================

USE zerotrust;

-- Drop existing tables
DROP TABLE IF EXISTS file_access_logs;
DROP TABLE IF EXISTS device_logs;
DROP TABLE IF EXISTS login_logs;
DROP TABLE IF EXISTS users;

-- ============================================
-- 1. USERS TABLE (Enhanced)
-- ============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    status ENUM('pending', 'active', 'revoked', 'suspended') DEFAULT 'pending',
    email VARCHAR(100),
    department VARCHAR(50),
    risk_score INT DEFAULT 0,
    last_login TIMESTAMP(3) NULL,
    created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    approved_by VARCHAR(50),
    approved_at TIMESTAMP(3) NULL,
    INDEX idx_username (username),
    INDEX idx_status (status),
    INDEX idx_risk_score (risk_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 2. SESSIONS TABLE (NEW - For 5-min auto-logout)
-- ============================================
CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(128) UNIQUE NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    last_activity TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    expires_at TIMESTAMP(3) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_session_id (session_id),
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 3. LOGIN_LOGS TABLE (Enhanced with geolocation)
-- ============================================
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(128),
    login_time TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    logout_time TIMESTAMP(3) NULL,
    ip_address VARCHAR(45),
    mac_address VARCHAR(50),
    network_type VARCHAR(30),
    location VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    city VARCHAR(50),
    country VARCHAR(50),
    isp VARCHAR(100),
    success BOOLEAN DEFAULT TRUE,
    failure_reason VARCHAR(200),
    login_count INT DEFAULT 1,
    device_fingerprint VARCHAR(128),
    user_agent TEXT,
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time),
    INDEX idx_ip_address (ip_address),
    INDEX idx_success (success)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 4. DEVICE_LOGS TABLE (Enhanced)
-- ============================================
CREATE TABLE device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(128) NOT NULL,
    mac_address VARCHAR(50),
    os VARCHAR(50),
    os_version VARCHAR(50),
    hostname VARCHAR(100),
    ip_address VARCHAR(45),
    wifi_ssid VARCHAR(100),
    trusted BOOLEAN DEFAULT FALSE,
    first_seen TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    last_seen TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    device_type VARCHAR(50),
    browser VARCHAR(50),
    screen_resolution VARCHAR(20),
    timezone VARCHAR(50),
    INDEX idx_user_id (user_id),
    INDEX idx_device_id (device_id),
    INDEX idx_trusted (trusted),
    INDEX idx_last_seen (last_seen)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 5. FILE_ACCESS_LOGS TABLE (Enhanced)
-- ============================================
CREATE TABLE file_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    action ENUM('read', 'write', 'delete', 'copy', 'move', 'download', 'upload') NOT NULL,
    file_size BIGINT,
    sensitivity_level ENUM('public', 'internal', 'confidential', 'critical') DEFAULT 'internal',
    ip_address VARCHAR(45),
    access_time TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    device_id VARCHAR(128),
    risk_flag BOOLEAN DEFAULT FALSE,
    INDEX idx_user_id (user_id),
    INDEX idx_access_time (access_time),
    INDEX idx_action (action),
    INDEX idx_sensitivity (sensitivity_level),
    INDEX idx_risk_flag (risk_flag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 6. BLOCKCHAIN_AUDIT TABLE (NEW - Merkle Tree)
-- ============================================
CREATE TABLE blockchain_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    block_index INT NOT NULL,
    timestamp TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    event_type VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    event_data JSON,
    previous_hash VARCHAR(64),
    current_hash VARCHAR(64) NOT NULL,
    merkle_root VARCHAR(64),
    nonce INT DEFAULT 0,
    difficulty INT DEFAULT 4,
    validator VARCHAR(50),
    INDEX idx_block_index (block_index),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_event_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 7. RISK_EVENTS TABLE (NEW - UEBA Signals)
-- ============================================
CREATE TABLE risk_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    risk_score INT NOT NULL,
    confidence_score DECIMAL(5, 2),
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    description TEXT,
    event_data JSON,
    detected_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP(3) NULL,
    resolved_by VARCHAR(50),
    INDEX idx_user_id (user_id),
    INDEX idx_event_type (event_type),
    INDEX idx_severity (severity),
    INDEX idx_detected_at (detected_at),
    INDEX idx_resolved (resolved)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 8. ACCESS_DECISIONS TABLE (NEW - Allow/Deny/Restrict)
-- ============================================
CREATE TABLE access_decisions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_name VARCHAR(200),
    decision ENUM('ALLOW', 'DENY', 'RESTRICT') NOT NULL,
    risk_score INT,
    zone VARCHAR(50),
    reason TEXT,
    timestamp TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    session_id VARCHAR(128),
    INDEX idx_user_id (user_id),
    INDEX idx_decision (decision),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 9. BEHAVIORAL_BASELINE TABLE (NEW - ML Baseline)
-- ============================================
CREATE TABLE behavioral_baseline (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    avg_login_hour DECIMAL(5, 2),
    common_locations JSON,
    trusted_devices JSON,
    typical_file_access_count INT,
    work_hours_start TIME,
    work_hours_end TIME,
    weekend_activity BOOLEAN DEFAULT FALSE,
    baseline_updated_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 10. NETWORK_CONNECTIONS TABLE (NEW - Agent monitoring)
-- ============================================
CREATE TABLE network_connections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    connection_type VARCHAR(20),
    remote_ip VARCHAR(45),
    remote_port INT,
    protocol VARCHAR(10),
    bytes_sent BIGINT,
    bytes_received BIGINT,
    connection_time TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    is_external BOOLEAN DEFAULT FALSE,
    is_suspicious BOOLEAN DEFAULT FALSE,
    country VARCHAR(50),
    INDEX idx_user_id (user_id),
    INDEX idx_connection_time (connection_time),
    INDEX idx_is_suspicious (is_suspicious)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- CREATE ADMIN USER (ONLY WAY TO CREATE ADMIN)
-- ============================================
-- Password: Admin@2024 (bcrypt hashed)
INSERT INTO users (username, password, role, status, email, department) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgOqZum3i', 'admin', 'active', 'admin@zerotrust.local', 'Security');

-- ============================================
-- SAMPLE DATA FOR TESTING (Optional - Remove for production)
-- ============================================
-- Uncomment below for demo data

/*
-- Sample pending user
INSERT INTO users (username, password, role, status, email, department) 
VALUES ('john.doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgOqZum3i', 'user', 'pending', 'john@company.com', 'Engineering');

-- Sample active user
INSERT INTO users (username, password, role, status, email, department, approved_by, approved_at) 
VALUES ('jane.smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqgOqZum3i', 'user', 'active', 'jane@company.com', 'Finance', 'admin', NOW(3));
*/

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
SELECT 'Database migration completed successfully!' AS Status;
SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'zerotrust';
