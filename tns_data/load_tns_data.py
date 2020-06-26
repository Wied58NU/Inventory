import pandas as pd
import numpy as np
# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

tns_data = pd.read_csv('tns_data_inv.txt', sep='\t', na_filter=False)
# Replace NANs with nulls
# lest test this!
# tns_data = tns_data.replace(np.nan, '', regex=True)
## Column Stuff

# Replace spaces in Column Names with underscores 
tns_data.columns = tns_data.columns.str.replace(" ", "_")

# Get rid of any commas in the fields
tns_data = tns_data.replace(',',' ', regex=True)

# Set all column names to lower case 'cause that the way postgres wants it!
# Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
tns_data.columns = map(str.lower, tns_data.columns)

# Get rid of any commas in the fields
tns_data = tns_data.replace(',',' ', regex=True)

# Keep only the columns we want and set their order
tns_data = tns_data[['name','model','serial','ip','software','module_ip','module_num','firmware','hw','last_seen']]


#Convert all data fields to upper case
tns_data = tns_data.apply(lambda x: x.astype(str).str.upper())

# Old habits are hard to break so I'm saving the dataframe to a csv as a backup
tns_data.to_csv('out_tns_data.csv', index=False)


# connect to PostgreSQL DB - Yes, that is a password in plain text. 
#engine = create_engine('postgresql://wied:wied@localhost:5432/jeffreywiedemann')
engine = create_engine('postgresql://localhost/jeffreywiedemann')

# We don't need this anymore either, but it's a good example, so I'll keep it in a comment
# Create a python dictionary of max data length for each column to determine database table column sizes
# dict([(v, tns_data[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in tns_data.columns.values])

# Create a table and load the data frame into it. if_exist could also be append, but we don't want that here!
tns_data.to_sql('tns_data_stage', engine, if_exists='replace', index=False, dtype={"NAME": String(), "MODEL": String(), "SERIAL": String(), "IP": String(), "SOFTWARE": String(), "MODULE_IP": String(), "MODULE_NUM": String(), "LAST_SEEN": String(), "EMPTY": String()})

# Rename Columns to match NU Invenentory 
#engine.execute("ALTER TABLE tns_data_stage RENAME make TO vendor")

engine.execute("ALTER TABLE tns_data_stage RENAME ip TO ip_address")

engine.execute("ALTER TABLE tns_data_stage RENAME serial TO serial_number")

engine.execute("ALTER TABLE tns_data_stage RENAME software TO os")

# Add asset_type column and populate

engine.execute("ALTER TABLE tns_data_stage ADD COLUMN asset_type text")

engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'CISCOCATALYST2912LRE'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'CISCOCATALYST3560CX8PCS'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'CISCOIE20004TSGB'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750-48P'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750-48TS'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750G-24TS-1U'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750V2-48PS'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750X-12S'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750X-24P'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3750X-48P'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-12S-S'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-12X48U-L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-24P-L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-24XS-S'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-24XU-L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-48P- PROVISIONED'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-48P-E'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'SWITCH' WHERE model = 'WS-C3850-48P-L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'WS-C6509-E'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'CISCO2921'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'CISCO3845'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'CISCO4431'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'CISCOASR1001X'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'CISCOME3600X'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'N7K-C7009'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'N7K-C7010'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTER' WHERE model = 'N7K-C7018'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'N7K-F248XP-25E'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'N7K-M108X2-12L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'N7K-M148GS-11L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'N7K-M202CF-22L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'N7K-M224XP-23L'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'N7K-SUP2E'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'VS-SUP2T-10G'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'WS-X6704-10GE'")
engine.execute("UPDATE tns_data_stage SET asset_type = 'ROUTERMODULE' WHERE model = 'WS-X6724-SFP'")


engine.execute("ALTER TABLE tns_data_stage ADD COLUMN vendor text")
engine.execute("UPDATE tns_data_stage SET vendor = 'CISCO'")
