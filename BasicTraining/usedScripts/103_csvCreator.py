import json,pandas,os,time,sys

def loadTime():
    global lastTime
    previousTime = lastTime
    lastTime = time.time()
    return lastTime - previousTime

#load all appropriate json files from one directory and merge them together. Remember the borders between sets
lastSplit = 0
splitLines = [0]
overallList = []
lastTime = time.time()
for root,dirs,files in os.walk("BasicTraining/unndBackups"):
    for filename in files:
        partset = json.load(open("BasicTraining/unndBackups/"+filename))
        lastSplit+=len(partset)
        splitLines.append(lastSplit)
        overallList.extend(partset)
#generate indexes and columns
indexes = []
columns = []
for i,case in enumerate(overallList):
    indexes.append(i)
    for key in case.keys():
        if key not in columns:columns.append(key)
#create the datasets
for i in range(len(splitLines)-1):
    splitBeg = splitLines[i]
    splitEnd = splitLines[i+1]
    dataFrame = pandas.DataFrame(overallList[splitBeg:splitEnd],columns=columns,index=indexes[splitBeg:splitEnd])
    dataFrame.to_csv("testDataSet%s.csv"%(i))
    del dataFrame
#divide numeric valeus by the biggest of them

#replace nominal values by 0 or 1 vectors

#save the dataset
