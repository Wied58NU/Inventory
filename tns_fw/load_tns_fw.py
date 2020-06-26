import pandas as pd
import numpy as np
# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

tns_fw = pd.read_csv('firewall.txt', sep='\t', na_filter=False)
# Replace NANs with nulls
# lest test this!
# tns_fw = tns_fw.replace(np.nan, '', regex=True)
## Column Stuff

# Replace spaces in Column Names with underscores 
tns_fw.columns = tns_fw.columns.str.replace(" ", "_")

# Get rid of any commas in the fields
tns_fw = tns_fw.replace(',',' ', regex=True)

# Set all column names to lower case 'cause that the way postgres wants it!
# Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
tns_fw.columns = map(str.lower, tns_fw.columns)


# Keep only the columns we want and set their order
tns_fw = tns_fw[['hostname','ip','model','sw','serial_number','last_seen']]


#Convert all data fields to upper case
tns_fw = tns_fw.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
tns_fw.to_csv('out_tns_fw.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
#engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
engine = create_engine('postgresql://localhost/jeffreywiedemann')

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, tns_fw[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in tns_fw.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
tns_fw.to_sql('tns_fw_stage', engine, if_exists='replace', index=False, dtype={"HOSTNAME": String(), "IP": String(), "MODEL": String(),"SW": String(),"SERIAL_NUMBER": String(), "LAST_SEEN": String() })

# Rename Columns to match NU Invenentory 
#engine.execute("ALTER TABLE tns_fw_stage RENAME make TO vendor")

engine.execute("ALTER TABLE tns_fw_stage RENAME ip TO ip_address")



# Add asset_type column and populate

