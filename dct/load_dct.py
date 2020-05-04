import pandas as pd

# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read dctrack csv into pandas frame
dct = pd.read_csv('in_dctrack.csv' ,na_filter=False)

## Column Stuff

# Replace spaces in Column Names with underscores 
dct.columns = dct.columns.str.replace(" ", "_")

#Get rid of any commas in the fields
dct = dct.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
dct.columns = map(str.lower, dct.columns)

#Get rid of any commas in the fields
dct = dct.replace(',',' ', regex=True)

# Keep only the columns we want
dct = dct[['name', 'make', 'serial_number', 'model', 'cabinet', 'type', 'function', 'contact', 'contact_team', 'customer', 'installation_date', 'last_updated_on', 'standard_application', 'technical_contact', 'installation_ticket', 'decommission_ticket', 'standard_contact_net_id', 'business_service']]


#Convert all data fields to upper case
dct = dct.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
dct.to_csv('out_dctrack.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')

# we don't need this anymore because is_exist now is set to replace as opposed to append 
# but it's a good example, so I'll keep it. 
#engine.execute("DROP TABLE dct_staging")

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, dct[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in dct.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
dct.to_sql('dct_staging', engine, if_exists='replace', index=False, dtype={"NAME": String(), "MAKE": String(), "SERIAL_NUMBER": String(), "MODEL": String(), "CABINET": String(), "TYPE": String(), "FUNCTION": String(), "CONTACT": String(), "CONTACT_TEAM": String(), "CUSTOMER": String(), "INSTALLATION_DATE": String(), "LAST_UPDATED_ON": String(), "STANDARD_APPLICATION": String(), "TECHNICAL_CONTACT": String(), "INSTALLATION_TICKET": String(), "DECOMMISSION_TICKET": String(),})

# Rename Columns to match NU Invenentory 
engine.execute("ALTER TABLE dct_staging RENAME make TO vendor")

engine.execute("ALTER TABLE dct_staging RENAME contact_team TO Service_Owner_Department")

engine.execute("ALTER TABLE dct_staging RENAME customer TO Service_Owner_Contact")

engine.execute("ALTER TABLE dct_staging RENAME last_updated_on TO Date_of_Last_Record_Verification")
