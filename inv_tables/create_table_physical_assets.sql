SELECT d.name
       d.type
       f.tag
       d.manufacturer
       d.model
       d.serial_number
       d.ip_address 
       d.business_service
       d.function
       d.standard_category
       f.campus
       f.building
       f.building_name
       f.room
       d.owner_department
       d.owner_contact
       d.technical_contact
       d.date_of_last_record_verification
       f.name
       f.department
       f.department_description
       f.purchase_date
       f.acquisition_date_fy
       f.po
       f.chartstring
       d.installation_ticket
       d.decommission_ticket
       d.location
       d.cabinet  
FROM dct d
LEFT JOIN fin_ops_stage f on  d.serial_number = f.serial
LEFT JOIN idrac i on i.service_tag = d.serial_number
LEFT JOIN ibm ibm on ibm.serial_nbr = d.serial_number
WHERE d.type in ('SERVER','STORAGE','TAPE')
ORDER BY d.type,
         d.vendor,
         d.name;



