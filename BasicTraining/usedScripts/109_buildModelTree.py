import json,csv

#get 
def modelString(row):
    modelStr = ""
    for column in row[1:2]+row[13:]:
        if column=="":break
        modelStr += column+"."
    return modelStr[:-1]

#load represented models
file = open("modSel2.csv")
table = csv.reader(file)
#create list, which will store branches
branches = []
branchIndex = -1
#create map of modKeys and branches to which they refer
mappedKeys = []
mkMap = {}
#loop through models and proccess those, which are not already mapped
for r,row in enumerate(table):
    if r and row!=[] and modelString(row) not in branches:
        #insert model to the list
        branches.append(modelString(row))
        branchIndex += 1
        #add modKey keys to the map
        for column in row[1:2]+row[13:]:
            if column != '':
                if column not in mappedKeys:
                    mappedKeys.append(column)
                    mkMap[column] = [branchIndex]
                else:mkMap[column].append(branchIndex)
#save list and maps
jsonFile = open("selectModelCheatsheet.json","w")
print({"models":branches,"map":mkMap})
jsonFile.write(json.dumps({"models":branches,"map":mkMap}))
jsonFile.close()
