import pandas as pd
import numpy as np

# database stuff
#import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read dctrack csv into pandas frame
dct = pd.read_csv('in_dctrack.csv', na_filter=False )
#dct = dct.replace(np.nan, '', regex=True)

## Column Stuff

# Replace spaces in Column Names with underscores 
dct.columns = dct.columns.str.replace(" ", "_")

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
dct.columns = map(str.lower, dct.columns)

## Data Stuff

#Get rid of any commas in the fields
dct = dct.replace(',',' ', regex=True)

# Keep only the columns we want and set their order
dct = dct[['name','type','make','model','serial_number','ip_address','business_service','function','standard_category','contact_team','customer','technical_contact','last_updated_on','installation_ticket','decommission_ticket','location','cabinet' ]]

#Convert all data fields to upper case
dct = dct.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
dct.to_csv('out_dctrack.csv', index=False)

# connect to PostgreSQL DB - Yes, that is a password in plain text. 
engine = create_engine('postgresql://invowner:inventory@localhost:5432/inventory')

# we don't need this anymore because is_exist now is set to replace as opposed to append 
# but it's a good example, so I'll keep it. 
#engine.execute("DROP TABLE dct_staging")

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, dct[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in dct.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
dct.to_sql('dct_stage', engine, if_exists='replace', index=False, dtype={"NAME": String(), "TYPE": String(), "MAKE": String(), "MODEL": String(), "SERIAL_NUMBER": String(), "IP_ADDRESS": String(), "BUSINESS_SERVICE": String(), "FUNCTION": String(), "STANDARD_CATEGORY": String(), "CONTACT_TEAM": String(), "CUSTOMER": String(), "TECHNICAL_CONTACT": String(), "LAST_UPDATED_ON": String(), "INSTALLATION_TICKET": String(), "DECOMMISSION_TICKET": String(), "LOCATION": String(), "CABINET": String(),})

# get rid of non CI Assets
engine.execute("DELETE  FROM    dct_stage AS gc WHERE   cabinet NOT IN ( SELECT  cabinet FROM    cabinet_functions WHERE function = 'ADMIN')")

# Rename Columns to match NU Invenentory 
engine.execute("ALTER TABLE dct_stage RENAME name TO asset_name")

engine.execute("ALTER TABLE dct_stage RENAME type TO asset_type")

engine.execute("ALTER TABLE dct_stage RENAME make TO manufacturer")

engine.execute("ALTER TABLE dct_stage RENAME function TO asset_fucntion")

engine.execute("ALTER TABLE dct_stage RENAME standard_category TO support_model")

engine.execute("ALTER TABLE dct_stage RENAME contact_team TO owner_department")

engine.execute("ALTER TABLE dct_stage RENAME customer TO owner_contact")

engine.execute("ALTER TABLE dct_stage RENAME last_updated_on TO date_of_last_record_verification")
