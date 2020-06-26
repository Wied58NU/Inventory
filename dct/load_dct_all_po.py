import pandas as pd
import numpy as np

# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read dctrack csv into pandas frame
dct = pd.read_csv('in_dctrack_po.csv', na_filter=False )
#dct = dct.replace(np.nan, '', regex=True)
## Column Stuff

# Replace spaces in Column Names with underscores 
dct.columns = dct.columns.str.replace(" ", "_")

#Get rid of any commas in the fields
dct = dct.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
dct.columns = map(str.lower, dct.columns)

# Keep only the columns we want and set their order
dct = dct[['name', 'make', 'type' ,'serial_number', 'po_number', 'model', 'function', 'contact', 'contact_team', 'customer', 'last_updated_on', 'technical_contact', 'installation_date','installation_ticket', 'decommission_ticket', 'location', 'cabinet']]


#Convert all data fields to upper case
dct = dct.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
dct.to_csv('out_dctrack.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
#engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
engine = create_engine('postgresql://localhost/jeffreywiedemann')

# we don't need this anymore because is_exist now is set to replace as opposed to append 
# but it's a good example, so I'll keep it. 
#engine.execute("DROP TABLE dct_staging")

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, dct[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in dct.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
dct.to_sql('dct_po_stage', engine, if_exists='replace', index=False, 
dtype={"NAME": String(),
"MAKE": String(), 
"TYPE": String(),
"SERIAL_NUMBER": String(),
"PO_NUMBER": String(), 
"MODEL": String(), 
"FUNCTION": String(), 
"CONTACT": String(), 
"CONTACT_TEAM": String(), 
"CUSTOMER": String(), 
"LAST_UPDATED_ON": String(), 
"TECHNICAL_CONTACT": String(), 
"INSTALLATION_DATE": String(), 
"DECOMMISSION_TICKET": String(), 
"LOCATION": String(), 
"CABINET": String(),})

# Rename Columns to match NU Invenentory 
engine.execute("ALTER TABLE dct_po_stage RENAME make TO vendor")

engine.execute("ALTER TABLE dct_po_stage RENAME contact_team TO Service_Owner_Department")

engine.execute("ALTER TABLE dct_po_stage RENAME customer TO Service_Owner_Contact")

engine.execute("ALTER TABLE dct_po_stage RENAME last_updated_on TO Date_of_Last_Record_Verification")
