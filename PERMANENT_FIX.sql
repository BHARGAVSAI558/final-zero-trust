-- ============================================
-- PERMANENT FIX FOR SESSION TRACKING
-- Run this ONCE in MySQL Workbench
-- ============================================

USE zerotrust;

-- 1. Fix NULL device_ids by generating from user_id + timestamp
UPDATE login_logs 
SET device_id = LEFT(MD5(CONCAT(user_id, login_time)), 16)
WHERE device_id IS NULL;

-- 2. Link sessions to login_logs (within 10 seconds tolerance)
UPDATE sessions s
JOIN login_logs l ON s.user_id = l.user_id 
  AND ABS(TIMESTAMPDIFF(SECOND, s.created_at, l.login_time)) < 10
SET s.login_id = l.id
WHERE s.login_id IS NULL;

-- 3. Verify the fix
SELECT 'NULL device_ids' as check_type, COUNT(*) as count 
FROM login_logs WHERE device_id IS NULL
UNION ALL
SELECT 'Unlinked sessions', COUNT(*) 
FROM sessions WHERE login_id IS NULL;

-- 4. Test session history query (example for 'sai')
SELECT 
    l.login_time,
    l.ip_address,
    l.city,
    l.country,
    l.device_id,
    l.mac_address,
    s.is_active,
    TIMESTAMPDIFF(SECOND, s.created_at, COALESCE(s.last_activity, NOW(3))) as duration
FROM login_logs l
LEFT JOIN sessions s ON l.id = s.login_id
WHERE l.user_id = 'sai' AND l.success = 1
ORDER BY l.login_time DESC;

-- 5. Show session counts per user
SELECT 
    l.user_id,
    COUNT(*) as total_logins,
    COUNT(s.session_id) as linked_sessions,
    COUNT(DISTINCT l.device_id) as unique_devices
FROM login_logs l
LEFT JOIN sessions s ON l.id = s.login_id
WHERE l.success = 1
GROUP BY l.user_id
ORDER BY total_logins DESC;
