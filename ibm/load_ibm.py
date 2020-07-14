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

# read ibmrack csv into pandas frame
ibm = pd.read_excel('ibm_storage.xlsx', na_filter=False)
#ibm = ibm.replace(np.nan, '', regex=True)

## Column Stuff

# Replace spaces in Column Names with underscores 
ibm.columns = ibm.columns.str.replace(" ", "_")

#Get rid of any commas in the fields
ibm = ibm.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
ibm.columns = map(str.lower, ibm.columns)


# Keep only the columns we want and set their order
ibm = ibm[['serial_nbr', 'service_end_date', 'contract_nbr', ]] 

#Convert all data fields to upper case
ibm = ibm.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
ibm.to_csv('out_ibm.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
#engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
engine = create_engine('postgresql://localhost/jeffreywiedemann')

ibm.to_sql('ibm_stage', engine, if_exists='replace', index=False, dtype={"serial_nbr": String(), "service_end_date": String(), "contract_nbr": String() ,})

# Rename Columns to match NU Invenentory 
#engine.execute("ALTER TABLE ibm_stage RENAME make TO vendor")
#
#engine.execute("ALTER TABLE ibm_stage RENAME contact_team TO Service_Owner_Department")
#
#engine.execute("ALTER TABLE ibm_stage RENAME customer TO Service_Owner_Contact")
#
#engine.execute("ALTER TABLE ibm_stage RENAME last_updated_on TO Date_of_Last_Record_Verification")
