ifname = "Warranty.html"
ofname = open("warranty.txt", 'w')
num_lines = 0
with open(ifname, 'r') as f:
    for line in f:
         line = line.replace("<table border=\"1\" style=\"border-collapse:collapse\">", "")
         line = line.replace("<tr>", "")
         line = line.replace("</td><td>", ",")
         line = line.replace("<td>", "")
         line = line.replace("</td></tr>", "")
         line = line.replace("<table*", "")
         line = line.replace("</table>", "")
         if line.strip():
            print(line, end ="", file = ofname)

#https://stackoverflow.com/questions/1403087/how-can-i-convert-an-html-table-to-csv/7318896
#
##Remove any Whitespace at the beginning of the line.
#sed 's/^[\ \t]*//g' 
#
#Remove newlines
#
#| tr -d '\n\r' 
#
#Replace </TR> with newline
#
#| sed 's/<\/TR[^>]*>/\n/Ig'  
#
#Remove TABLE and TR tags
#
#| sed 's/<\/\?\(TABLE\|TR\)[^>]*>//Ig' 
#
#Remove ^<TD>, ^<TH>, </TD>$, </TH>$
#
#| sed 's/^<T[DH][^>]*>\|<\/\?T[DH][^>]*>$//Ig' 
#
#Replace </TD><TD> with comma
#
#| sed 's/<\/T[DH][^>]*><T[DH][^>]*>/,/Ig'
