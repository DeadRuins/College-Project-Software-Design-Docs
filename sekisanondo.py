#積算温度の計算

import csv

with open("sekisanondo.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

tempera=[row]

tempera_sum=0

for temper in row:
    tempera_sum=tempera_sum+temper

print(tempera_sum)
