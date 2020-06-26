import pandas as pd

# database stuff
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String

## Read the data file

cmdb = pd.read_csv('Service_Operations_CMDB.csv',  na_filter=False)


## Column Stuff

# Replace spaces in Column Names with underscores 
cmdb.columns = cmdb.columns.str.replace(" ", "_")

# Get rid of any commas in the fields
cmdb = cmdb.replace(',',' ', regex=True)

# Set all column names to lower case 'cause that the way postgres wants it!
# Really it's true. If you create a table in Pg, and the names are mixed or uppercase, you'll
# have to double quote the coluumn names in ya query. And that's a drag. 
dct.columns = map(str.lower, dct.columns)

## Data Stuff


name
manufacturer
model 
serial_number 
campus 
building                    
room_number
cooling_device
power_device 
department
last_edit_date_time 
purchase_order  
service_contract_end_date
service_contract_number
service_contract_purchase_order
service_contract_start_date
service_contract_term 
device_type 
# List of columns after Jeff manually pruned to set up auto pruning of unwanted columns.
#list(cmdb.columns)
#['Name', 'Manufacturer', 'Model', 'Serial Number', 'Campus', 'Building', 'Room Number', 'Cooling Device', 'Power Device', 'Department', 'Last Edit Date/Time', 'Original Purchase Order', 'Service Contract End Date', 'Service Contract Number', 'Service Contract Purchase Order Number', 'Service Contract Start Date', 'Service Contract Term']


cmdb["DEVICE_TYPE"] = cmdb["Cooling_Device"] + cmdb["Power_Device"]


# Create output file
cmdb.to_csv('out_Service_Operations_CMDB.csv', index=False)

# Create a dictionary of max data length for each column
# This for one time use to get max lengths to db create table
#cmdb_columns = dict([(v, cmdb[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in cmdb.columns.values])

