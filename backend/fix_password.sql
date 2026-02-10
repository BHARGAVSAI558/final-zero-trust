-- Fix password hash in database
USE zero;

-- Update admin password to hashed version
UPDATE users SET password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qviu6' WHERE username = 'admin';

-- Verify the update
SELECT username, LEFT(password, 20) as password_hash, role FROM users;
