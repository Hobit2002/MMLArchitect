import csv,json
from datasetFunc import *
#load modSel2 table and mergable
table = csv.DictReader(open("modSel2.csv"))
mergable = json.load(open("Mergable.json"))
#prepare csv writer
wfile = open("modSel3.csv","w")
wtable = csv.DictWriter(wfile,fieldnames=table.fieldnames)
#add header row
headers = {} 
for n in wtable.fieldnames:
    headers[n] = n
wtable.writerow(headers)
#loop through modSel2
for row in table:
    #copy dataset information and confidence to new row
    newRow = row.copy()    
    #loop through row mod keys
    i=0
    m = 0
    while i+m < 52:
        modKey = mkString(i+m)
        model = row[modKey]
        modelString = model
        if model=='':break
        nextmodKey = mkString(i+m+1)
        nextModel = row[nextmodKey]
        #whenever you find mergable model write all modKeys to one new cell until you find a non-mergable modKey
        if [nextModel,model] in mergable:
            while [nextModel,model] in mergable:
                print("merging:%s with %s"%(modelString,nextModel))
                modelString +="."+nextModel
                m+=1
                model = nextModel
                nextmodKey = mkString(i+m+1)
                nextModel = row[nextmodKey]
        newRow[mkString(i)] = modelString
        i+=1
    for i in range(i,52):newRow[mkString(i)] = ''
    #write new row
    wtable.writerow(newRow)
#save new dataset
wfile.close()