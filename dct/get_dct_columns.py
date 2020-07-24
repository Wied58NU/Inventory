import pandas as pd
import numpy as np


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

dct.columns

