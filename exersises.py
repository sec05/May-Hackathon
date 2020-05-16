import csv
import json
#run to put exercises.csv -> exersises.json
#only run on changes to exersises.csv 
nameCSV = []
nameJSON= []
def exersisesToJson():
   with open(r'data\exercises.csv', mode='r') as f:
        reader = csv.DictReader(f, delimiter=',') 
        for n, row in enumerate(reader):
            if not n:#skip header
                continue
            nameCSV.append(row)
        print(nameCSV)
        for o in range(0,898):
           newExersise = {}
           newExersise=nameCSV[o]
           nameJSON.append(newExersise)
        
        with open(r'data\exersises.json','w') as fp:
            json.dump(nameJSON,fp)


exersisesToJson()