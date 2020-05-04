
with open('Service_Operations_CMDB.csv') as fin:
    lines = fin.readlines()
lines[0] = lines[0].replace(' ', '_')

with open('Service_Operations_CMDB_temp.csv', 'w') as fout:
    for line in lines:
        fout.write(line)
