import pandas as pd
import numpy as np
# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

# read cmdbrack csv into pandas frame
cmdb = pd.read_csv('Service_Operations_CMDB.csv' ,na_filter=False)
#cmdb = cmdb.replace(np.nan, '', regex=True)


## Column Stuff

# Replace spaces in Column Names with underscores 
cmdb.columns = cmdb.columns.str.replace(" ", "_")
# CMDB ONLY
cmdb.columns = cmdb.columns.str.replace("/", "_")

#Get rid of any commas in the fields
cmdb = cmdb.replace(',',' ', regex=True)

#Set all column names to lower case 'cause that the way postgres wants it!
#Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
cmdb.columns = map(str.lower, cmdb.columns)


# Keep only the columns we want and set their order
cmdb = cmdb[['name','manufacturer','model','serial_number','campus','building','room_number','cooling_device','power_device','department','last_edit_date_time']]
# Combine Cooling_Device and Power_Device into device_type
cmdb["device_type"] = cmdb["cooling_device"] + cmdb["power_device"]
cmdb = cmdb.drop(['cooling_device', 'power_device'], axis=1)

#Convert all data fields to upper case
cmdb = cmdb.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
cmdb.to_csv('out_cmd.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
# engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
engine = create_engine('postgresql://localhost/jeffreywiedemann')

# we don't need this anymore because is_exist now is set to replace as opposed to append 
# but it's a good example, so I'll keep it. 
#engine.execute("DROP TABLE cmdb_staging")

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, cmdb[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in cmdb.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
cmdb.to_sql('cmdb_stage', engine, if_exists='replace', index=False, dtype={"NAME": String(), "MANUFACTURER": String(), "MODEL": String(), "SERIAL_NUMBER": String(), "CAMPUS": String(), "BUILDING": String(), "ROOM_NUMBER": String(), "COOLING_DEVICE": String(), "POWER_DEVICE": String(), "DEPARTMENT": String(), "LAST_EDIT_DATE_TIME": String() })

# Rename Columns to match NU Invenentory 
# engine.execute("ALTER TABLE cmdb_test RENAME make TO vendor")

