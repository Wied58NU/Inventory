SELECT d.NAME,
       d.TYPE,
       d.MAKE,
       d.MODEL,
       d.SERIAL_NUMBER,
       d.CABINET,
       c.FUNCTION
FROM dct_staging d
LEFT JOIN CABINET_FUNCTIONS c ON d.CABINET = c.cabinet
WHERE c.FUNCTION = 'ADMIN'
ORDER BY d.TYPE,
         d.MAKE,
         d.NAME,
         d.CABINET


