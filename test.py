import csv

with open("True.csv", "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    i = 1
    next(csv_reader)
    for line in csv_reader:
        print(line[1])
        i += 1
        if i == 5:
            break
