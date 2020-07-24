import pandas as pd
import numpy as np
# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read idracrack csv into pandas frame
idrac = pd.read_csv('warranty.txt' ,na_filter=False)
#idrac = idrac.replace(np.nan, '', regex=True)


## Column Stuff

# Replace spaces in Column Names with underscores 
idrac.columns = idrac.columns.str.replace(" ", "_")
# CMDB ONLY
idrac.columns = idrac.columns.str.replace("/", "_")

#Get rid of any commas in the fields
idrac = idrac.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
idrac.columns = map(str.lower, idrac.columns)


# Keep only the columns we want and set their order
idrac = idrac[['device_name','model','device_type','service_tag','service_level_code','warranty_type','warranty_description','service_provider','shipped_date','start_date','end_date','days_remaining']]

#Convert all data fields to upper case
idrac = idrac.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
idrac.to_csv('out_cmd.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
# engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
#engine = create_engine('postgresql://localhost/jeffreywiedemann')
engine = create_engine('postgresql://invowner:inventory@localhost:5432/inventory')

# we don't need this anymore because is_exist now is set to replace as opposed to append 
# but it's a good example, so I'll keep it. 
#engine.execute("DROP TABLE idrac_staging")

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, idrac[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in idrac.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
idrac.to_sql('idrac_stage', engine, if_exists='replace', index=False, dtype={"Device_Name": String(),"Model": String(),"Device_Type": String(),"Service_Tag": String(),"Service_Level_Code": String(),"Warranty_Type": String(),"Warranty_Description": String(),"Service_Provider": String(),"Shipped_Date": String(),"Start_Date": String(),"End_Date": String(),"Days_Remaining": String(), })

# Rename Columns to match NU Invenentory 
# engine.execute("ALTER TABLE idrac_test RENAME make TO vendor")
#SELECT t1.* FROM idrac_stage t1
#JOIN 
#(
#   SELECT device_name, MAX(end_date) AS MAXDATE
#   FROM idrac_stage 
#   GROUP BY name 
#) t2
#ON T1.device_name = t2.device_name
#AND t1.date = t2.MAXDATE
