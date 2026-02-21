USE zerotrust;

-- Add missing columns to login_logs if they don't exist
ALTER TABLE login_logs 
ADD COLUMN IF NOT EXISTS mac_address VARCHAR(100),
ADD COLUMN IF NOT EXISTS hostname VARCHAR(255),
ADD COLUMN IF NOT EXISTS device_os VARCHAR(100),
ADD COLUMN IF NOT EXISTS user_agent TEXT,
ADD COLUMN IF NOT EXISTS device_fingerprint VARCHAR(255),
ADD COLUMN IF NOT EXISTS failure_reason VARCHAR(255),
ADD COLUMN IF NOT EXISTS logout_time TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS device_id VARCHAR(255);

SELECT 'Columns added successfully' as status;
