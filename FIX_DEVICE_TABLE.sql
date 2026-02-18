-- Fix device_logs table for ON DUPLICATE KEY UPDATE
ALTER TABLE device_logs ADD UNIQUE KEY unique_user_device (user_id, device_id);

-- Verify structure
DESCRIBE device_logs;

-- Check current data
SELECT user_id, device_id, mac_address, wifi_ssid, hostname, os, ip_address, last_seen 
FROM device_logs ORDER BY last_seen DESC LIMIT 10;
