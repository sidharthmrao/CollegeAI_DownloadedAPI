import csv



f = csv.reader(open('college_info.csv', 'r'))
for row in f:
    print(row[1])
