SELECT d.name
FROM dct d
LEFT JOIN cabinet_functions c ON d.cabinet = c.cabinet
WHERE c.function = 'ADMIN'
AND   d.type = 'SERVER'
ORDER BY d.name


