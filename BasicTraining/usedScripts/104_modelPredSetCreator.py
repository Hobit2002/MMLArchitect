import csv,os,json
modelOverview = {}
rowList = []

def addToOverview(key,curPart):
    global modelOverview
    if key in list(modelOverview.keys()):
        if curPart in list(modelOverview[key].keys()):
            modelOverview[key][curPart]+=1
        else:
            modelOverview[key][curPart] = 1
    else:modelOverview[key] = {curPart:1}

#loop through tDSs
basicPath = "BasicTraining/tDSs"
for root,dirs,files in os.walk(basicPath):
    for filename in files:
        print(filename, end=" -")
        file = open("%s/%s"%(basicPath,filename))
        table = csv.DictReader(file)
        for r,row in enumerate(table):
            #convert model name to multi-part vector (split in dots and underlines)
            model = row["model"]
            modDict = {}
            curPart = ""
            partNum = 0
            for ch in model:
                if ch in "._()":
                    key = "modKey%s"%(partNum)
                    modDict[key] = curPart
                    partNum+=1
                    #keep data about usage of different models
                    addToOverview(key,curPart)
                    curPart = ""
                else:
                    curPart+=ch
            if len(curPart):
                key = "modKey%s"%(partNum)
                modDict[key] = curPart
                addToOverview(key,curPart) 
            #keep models with data about datasets and tasks
            for datasetInf in ["NumberOfInstances","NumberOfFeatures","NumberOfClasses","NumberOfMissingValues",
                               "NumberOfInstancesWithMissingValues","NumberOfNumericFeatures","NumberOfSymbolicFeatures",
                               "MeanAttributeEntropy","MinorityClassSize","PercentageOfSymbolicFeatures"]:
                modDict[datasetInf] = row[datasetInf]
            rowList.append(modDict)
        print(r)
        del table
        del file
#get 90% most confident models
indexes = []
for m,model in enumerate(rowList):
    partNum = 0
    confidence = 1
    key = "modKey%s"%(partNum)
    while key in list(model.keys()):
        confidence *= modelOverview[key][model[key]]
        partNum+=1
        key = "modKey%s"%(partNum)
    model["confidence"] = confidence
#save the dataset
file = open("modelDatasetRows.json","w")
file.write(json.dumps(rowList))
file.close()
#delete the least used models

#create dataset with information about models and datasets

