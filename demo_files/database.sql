-- Zero Trust Database Schema
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    risk_score INT DEFAULT 0,
    status ENUM('active', 'pending', 'revoked') DEFAULT 'active'
);

CREATE TABLE sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(50),
    ip_address VARCHAR(45),
    is_active BOOLEAN DEFAULT 1
);

-- Sample Data
INSERT INTO users (username, password, risk_score) VALUES
('mahesh', 'hashed_password', 56),
('karthik', 'hashed_password', 36);
