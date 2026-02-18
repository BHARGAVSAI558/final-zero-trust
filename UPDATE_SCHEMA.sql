-- Add missing columns for real-time session tracking

-- Add device_id to login_logs
ALTER TABLE login_logs ADD COLUMN IF NOT EXISTS device_id VARCHAR(50);

-- Add login_id reference to sessions
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS login_id INT;

-- Add login_count to device_logs
ALTER TABLE device_logs ADD COLUMN IF NOT EXISTS login_count INT DEFAULT 0;

-- Add id column to login_logs if not exists (for session reference)
ALTER TABLE login_logs ADD COLUMN IF NOT EXISTS id INT AUTO_INCREMENT PRIMARY KEY FIRST;

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_login_device ON login_logs(user_id, device_id);
CREATE INDEX IF NOT EXISTS idx_session_login ON sessions(login_id);
CREATE INDEX IF NOT EXISTS idx_device_user ON device_logs(user_id, device_id);
