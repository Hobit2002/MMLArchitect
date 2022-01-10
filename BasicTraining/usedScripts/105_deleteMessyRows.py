import csv, json
import matplotlib.pyplot as plt
import numpy as np
from datasetFunc import *
#1 load modelSelection.csv
table,file = readDict("modelSelection.csv",retFile=True)
#2 make statistics how much are different model used
#   a. save the data
#   b. plot graph
mkVal = {}
modKeys = generateModKeys(mkVal)
#2.1 collect data
for r,row in enumerate(table):
    if r/1000==r//1000:print(r/1000)
    for i in range(52):
        modKey = mkString(i)
        model = row[modKey]
        if model in modKeys[modKey].keys():
            modKeys[modKey][model]["rows"].append(r)
            modKeys[modKey][model]["occ"]+=1
        else:
            modKeys[modKey][model] = {"succ":[],"pred":[],"occ":1,"rows":[r]}
        if i > 0:
            prevModel = mkString(i-1)
            if row[prevModel] not in modKeys[modKey][model]["pred"]:
                modKeys[modKey][model]["pred"].append(row[prevModel])
        if i < 51:
            nextModel = mkString(i+1)
            if row[nextModel] not in modKeys[modKey][model]["succ"]:
                modKeys[modKey][model]["succ"].append(row[nextModel])
#2.2 plot how much are different models used
"""
print("ploting start")
occurenceList = []
for modKey in modKeys.values():
    for model in modKey.values(): occurenceList.append(model["occ"])
occurenceList.sort()
arr = np.array(occurenceList)
plt.hist(arr,range=(30,10000))
plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
plt.show()
"""
#3 ask developer what should be the occurence treshold of model for deleting its row
treshold = 30#int(input("Set treshold, please:"))
#4 save the dataset without too rare models
#4.1 get list of rows to delete
delRows = []
for modKey in modKeys.values():
    for model in modKey.values():
        if len(model["rows"]) < treshold:delRows.extend(model["rows"])
#4.2 write to the new table
file2 = open("modSel2.csv","w")
table2 = csv.writer(file2)
file.seek(0)
for r,row in enumerate(csv.reader(file)):
    if r - 1 not in delRows:table2.writerow(row)
#5 print number of mergable column pairs
#How:loop through modKeys. For each modKey get lists of successors of its models
#compare modKey predeccessors with successors of previous modKey:
#if current modKey has only one predeccosr and there was a model which had it as its only successor in succDict, merge them together
succDict = {}
mergable = []
print("merging")
for modKey in modKeys.values():
    succDict["Current"] = {}
    for model,modVals in modKey.items():
        pred = modVals["pred"]
        succDict["Current"][model] = modVals["succ"]
        #compare with succDict
        if len(pred) == 1:
            for prevModel,succVals in succDict["Previous"].items():
                if succVals==[model]:mergable.append([model,prevModel])
                print("Merge found")
    succDict["Previous"] = succDict["Current"].copy()
print("Merging done")
jsonFile = open("Mergable.json","w")
jsonFile.write(json.dumps(mergable))
jsonFile.close()