-- Clear old login logs to force fresh geolocation
DELETE FROM login_logs WHERE city = 'Unknown' OR city IS NULL;

-- Update existing sessions to clear cache
UPDATE users SET last_login = NULL WHERE username = 'admin';
