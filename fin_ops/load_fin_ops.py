import pandas as pd
import numpy as np

# Excel stuff 
#import xlrd
from pandas import ExcelWriter
from pandas import ExcelFile


# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read fin_opsrack csv into pandas frame
fin_ops = pd.read_excel('Cyberinfrastructure.xlsx', na_filter=False)
#fin_ops = fin_ops.replace(np.nan, '', regex=True)

## Column Stuff

# Replace spaces in Column Names with underscores 
fin_ops.columns = fin_ops.columns.str.replace(" ", "_")

#Get rid of any commas in the fields
fin_ops = fin_ops.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
fin_ops.columns = map(str.lower, fin_ops.columns)


# Keep only the columns we want and set their order
fin_ops = fin_ops[['tag', 'description', 'purchase_date','acquisition_date_fy', 'manufacturer', 'model', 'serial', 'campus', 'department', 'department_description', 'building', 'building_name','room', 'name', 'po', 'chartstring', ]]


#Convert all data fields to upper case
fin_ops = fin_ops.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
fin_ops.to_csv('out_fin_opsrack.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
#engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
#engine = create_engine('postgresql://localhost/jeffreywiedemann')
engine = create_engine('postgresql://invowner:inventory@localhost:5432/inventory')

fin_ops.to_sql('fin_ops_stage', engine, if_exists='replace', index=False, dtype={"Tag": String(), "Description": String(), "Purchase_Date','Acquisition_Date_FY": String(), "Manufacturer": String(), "Model": String(), "Serial": String(), "Campus": String(), "Department": String(), "Department_Description": String(), "Building": String(), "Building_Name','Room": String(), "Name": String(), "Purchase": String(), "PO": String(), "Chartstring": String(),})

# Rename Columns to match NU Invenentory 
#engine.execute("ALTER TABLE fin_ops_stage RENAME make TO vendor")
#
#engine.execute("ALTER TABLE fin_ops_stage RENAME contact_team TO Service_Owner_Department")
#
#engine.execute("ALTER TABLE fin_ops_stage RENAME customer TO Service_Owner_Contact")
#
#engine.execute("ALTER TABLE fin_ops_stage RENAME last_updated_on TO Date_of_Last_Record_Verification")
