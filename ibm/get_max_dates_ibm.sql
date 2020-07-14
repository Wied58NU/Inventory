drop table ibm;
create table ibm as 
SELECT t1.* FROM ibm_stage t1
JOIN 
(
   SELECT serial_nbr, MAX(service_end_date) AS MAXDATE
   FROM ibm_stage 
   GROUP BY serial_nbr 
) t2
ON T1.serial_nbr = t2.serial_nbr
AND t1.service_end_date = t2.MAXDATE;
