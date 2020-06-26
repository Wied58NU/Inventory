#!/Users/jeffreywiedemann/Desktop/fin-ops/venv/bin/python3
# https://pythonspot.com/read-excel-with-pandas/


import xlrd
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
 
df = pd.read_excel('Cyberinfrastructure.xlsx')

# Reduce to desired Columns
fin_ops = df[['Tag', 'Description', 'Purchase Date','Acquisition Date FY', 'Manufacturer', 'Model', 'Serial', 'Campus', 'Department', 'Department Description', 'Building', 'Building Name','Room', 'Name', 'Purchase', 'PO', 'Chartstring', ]]

# Get rid_of commas
fin_ops =fin_ops.replace(',',' ', regex=True)


# Make all Upper Case



