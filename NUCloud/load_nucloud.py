import pandas as pd
import numpy as np
# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read nucloudrack csv into pandas frame
nucloud = pd.read_csv('in_nucloud.csv', ,na_filter=False)
#nucloud = nucloud.replace(np.nan, '', regex=True)
## Column Stuff

# Replace spaces in Column Names with underscores 
nucloud.columns = nucloud.columns.str.replace(" ", "_")

#Get rid of any commas in the fields
nucloud = nucloud.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
nucloud.columns = map(str.lower, nucloud.columns)

#Get rid of any commas in the fields
nucloud = nucloud.replace(',',' ', regex=True)

# Keep only the columns we want and set their order
nucloud = nucloud[['name','fqdn','guest']]

#Convert all data fields to upper case
nucloud = nucloud.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
nucloud.to_csv('out_nucloud.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
#engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
engine = create_engine('postgresql://localhost/jeffreywiedemann')

# we don't need this anymore because is_exist now is set to replace as opposed to append 
# but it's a good example, so I'll keep it. 
#engine.execute("DROP TABLE nucloud_staging")

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, nucloud[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in nucloud.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
nucloud.to_sql('nucloud_stage', engine, if_exists='replace', index=False, dtype={"Name": String(), "FQDN": String() ,})

# Rename Columns to match NU Invenentory 
engine.execute("ALTER TABLE nucloud_stage RENAME guest TO os")

#engine.execute("ALTER TABLE nucloud_stage RENAME ownership TO service_owner_department")
#
#engine.execute("ALTER TABLE nucloud_stage RENAME contact TO service_owner_contact")
#
#engine.execute("ALTER TABLE nucloud_stage RENAME standard_level TO usage_level")
#
#engine.execute("ALTER TABLE nucloud_stage RENAME standard_category TO support_model")
#
#engine.execute("ALTER TABLE nucloud_stage RENAME primary_app TO business_service")
#
#engine.execute("ALTER TABLE nucloud_stage RENAME ticket_number TO installation_ticket")
#
#engine.execute("ALTER TABLE nucloud_stage RENAME creation_date TO installation_date")
