import pandas as pd


cmdb = pd.read_csv('Service_Operations_CMDB.csv',  na_filter=False)

# Replace spaces in Column Names - also add .str.upper() if the convert data below does not include headers
cmdb.columns = cmdb.columns.str.replace(" ", "_")

# Replace NANs with nulls
# cmdb = cmdb.replace(np.nan, '', regex=True)

#Get rid of any commas in the fields
cmdb = cmdb.replace(',',' ', regex=True)

cmdb["DEVICE_TYPE"] = cmdb["Cooling_Device"] + cmdb["Power_Device"]

#Convert all letters to upper case
cmdb = cmdb.apply(lambda x: x.astype(str).str.upper())

# List of columns after Jeff manually pruned to set up auto pruning of unwanted columns.
#list(cmdb.columns)
#['Name', 'Manufacturer', 'Model', 'Serial Number', 'Campus', 'Building', 'Room Number', 'Cooling Device', 'Power Device', 'Department', 'Last Edit Date/Time', 'Original Purchase Order', 'Service Contract End Date', 'Service Contract Number', 'Service Contract Purchase Order Number', 'Service Contract Start Date', 'Service Contract Term']


# Create output file
cmdb.to_csv('out_Service_Operations_CMDB.csv', index=False)

# Create a dictionary of max data length for each column
# This for one time use to get max lengths to db create table
#cmdb_columns = dict([(v, cmdb[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in cmdb.columns.values])

