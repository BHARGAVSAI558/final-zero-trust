-- ============================================
-- PERMANENT FIX FOR SESSION TRACKING
-- Run this in MySQL Workbench or command line
-- ============================================

USE zerotrust;

-- 1. Ensure all required columns exist (safe - won't fail if exists)
ALTER TABLE login_logs 
  ADD COLUMN IF NOT EXISTS device_id VARCHAR(50),
  ADD COLUMN IF NOT EXISTS user_agent TEXT;

ALTER TABLE sessions 
  ADD COLUMN IF NOT EXISTS login_id INT;

ALTER TABLE device_logs 
  ADD COLUMN IF NOT EXISTS login_count INT DEFAULT 0;

-- 2. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_login_device ON login_logs(user_id, device_id);
CREATE INDEX IF NOT EXISTS idx_session_login ON sessions(login_id);
CREATE INDEX IF NOT EXISTS idx_device_user ON device_logs(user_id, device_id);
CREATE INDEX IF NOT EXISTS idx_login_time ON login_logs(user_id, login_time DESC);

-- 3. Link existing sessions to login_logs (if not already linked)
UPDATE sessions s
LEFT JOIN login_logs l ON s.user_id = l.user_id 
  AND ABS(TIMESTAMPDIFF(SECOND, s.created_at, l.login_time)) < 5
SET s.login_id = l.id
WHERE s.login_id IS NULL AND l.id IS NOT NULL;

-- 4. Update device_logs login_count based on actual logins
UPDATE device_logs d
SET login_count = (
  SELECT COUNT(*) 
  FROM login_logs l 
  WHERE l.user_id = d.user_id 
    AND l.device_id = d.device_id 
    AND l.success = 1
)
WHERE d.login_count = 0 OR d.login_count IS NULL;

-- 5. Verify the fix
SELECT 'LOGIN_LOGS' as table_name, COUNT(*) as total_records FROM login_logs
UNION ALL
SELECT 'SESSIONS', COUNT(*) FROM sessions
UNION ALL
SELECT 'DEVICE_LOGS', COUNT(*) FROM device_logs
UNION ALL
SELECT 'SESSIONS_WITH_LOGIN_ID', COUNT(*) FROM sessions WHERE login_id IS NOT NULL;

-- 6. Show sample data for verification
SELECT 
  l.user_id,
  l.login_time,
  l.device_id,
  l.mac_address,
  s.session_id,
  s.is_active,
  d.hostname,
  d.os
FROM login_logs l
LEFT JOIN sessions s ON l.id = s.login_id
LEFT JOIN device_logs d ON l.user_id = d.user_id AND l.device_id = d.device_id
WHERE l.success = 1
ORDER BY l.login_time DESC
LIMIT 10;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check bhargav's data
SELECT 'BHARGAV LOGIN RECORDS' as info;
SELECT 
  login_time,
  ip_address,
  city,
  country,
  device_id,
  mac_address,
  success
FROM login_logs 
WHERE user_id = 'bhargav' 
ORDER BY login_time DESC 
LIMIT 5;

SELECT 'BHARGAV SESSIONS' as info;
SELECT 
  session_id,
  created_at,
  is_active,
  login_id,
  TIMESTAMPDIFF(SECOND, created_at, COALESCE(last_activity, NOW(3))) as duration_seconds
FROM sessions 
WHERE user_id = 'bhargav' 
ORDER BY created_at DESC 
LIMIT 5;

SELECT 'BHARGAV DEVICES' as info;
SELECT 
  device_id,
  mac_address,
  hostname,
  os,
  wifi_ssid,
  login_count,
  last_seen
FROM device_logs 
WHERE user_id = 'bhargav';
