USE zero_trust_db;
DELETE FROM network_logs WHERE remote_ip = '127.0.0.1' OR remote_ip = '10.0.0.50';
SELECT * FROM network_logs ORDER BY timestamp DESC LIMIT 10;
