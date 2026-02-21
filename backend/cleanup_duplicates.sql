USE zerotrust;

-- Remove duplicate files, keeping only the most recent one for each filename
DELETE f1 FROM files f1
INNER JOIN files f2 
WHERE f1.filename = f2.filename 
AND f1.id < f2.id;

-- Show remaining files
SELECT id, filename, sensitivity, size, created_at FROM files ORDER BY filename;
