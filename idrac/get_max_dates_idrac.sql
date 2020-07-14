drop table idrac;
create table idrac as 
SELECT t1.* FROM idrac_stage t1
JOIN 
(
   SELECT device_name, MAX(end_date) AS MAXDATE
   FROM idrac_stage 
   GROUP BY device_name 
) t2
ON T1.device_name = t2.device_name
AND t1.end_date = t2.MAXDATE;
