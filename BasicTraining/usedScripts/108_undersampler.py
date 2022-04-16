import csv,json
startPos = int(input("Where should I start (type integer)? "))
if startPos:
    allSignificant,colLens = json.load(open("undersampleList.json"))
else:
    allSignificant = []
    colLens = []

for mk in range(startPos,42):
    dir = "modKeySets/mk%s/"%(mk)
    columns = json.load(open("%s/mkCols.json"%(dir)))
    colLen = len(columns)
    colLens.append(colLen)
    #loop through both test and train set
    for fileNameBase in ["train","test"]:
    #build storage structures
        xKeys = []
        xRegister = {}
        yRegister = [0 for i in range(colLen)]
        removeList = []
        #open datasets
        xFileName = "%s/%s_x.csv"%(dir,fileNameBase)
        xFile = open(xFileName)
        xTable = csv.reader(xFile)
        yFileName = "%s/%s_y.csv"%(dir,fileNameBase)
        yFile = open(yFileName)
        yTable = csv.reader(yFile)
        r=0
        #find how much are different models used
        if fileNameBase == "train":
            for xVal in xTable:
                for yVal in yTable:break
                yIndex = yVal.index(max(yVal))
                yRegister[yIndex]+=1
            #get significant columns
            significantColumns = []
            for i in range(colLen):
                if yRegister[i] > 1000:significantColumns.append(i)
            allSignificant.append(significantColumns.copy())
            #get list of overrepresented columns (those who are present more than all others columns combined)
            overrepresented = []
            for i in range(colLen):
                yRegCopy = yRegister.copy()
                del yRegCopy[i]
                if yRegister[i] > sum(yRegCopy):overrepresented.append(i)
            xFile.seek(0)
            yFile.seek(0)
        #filter dataset
        for xVal in xTable:
            for yVal in yTable:break
            #save y data
            yIndex = yVal.index(max(yVal))
            yRegister[yIndex]+=1
            #add x to storage
            xKey = str(xVal)[1:-1].replace(",","").replace(" ","").replace("e","").replace(".","")
            if xKey not in xKeys:
                xKeys.append(xKey)
                xRegister[xKey] = [0 for i in range(colLen)]
            xRegister[xKey][yIndex] += 1
            #add to removeList (?)
            if yIndex not in significantColumns or (yIndex in overrepresented and xRegister[xKey][yIndex] > 60):removeList.append(r)
            r+=1
            if not r%6000:print("Milestone %s "%(fileNameBase),r)  
        #write unremoved rows
        xWriter = csv.writer(open("%s/%s_xt.csv"%(dir,fileNameBase),"w"))
        yWriter = csv.writer(open("%s/%s_yt.csv"%(dir,fileNameBase),"w"))
        xFile.seek(0)
        yFile.seek(0)
        r= 0
        yRegister_t = [0 for i in range(colLen)]
        for xVal in xTable:
            for yVal in yTable:break
            if r not in removeList:
                #delete insignificant
                #for x
                leftBorder = 9
                newXVal = xVal[:9]
                for s,sigList in enumerate(allSignificant[:-1]):
                    for cl in range(colLens[s]):
                        if cl in sigList:newXVal.append(xVal[leftBorder+cl])
                    leftBorder+=cl
                sigList = allSignificant[-1]
                #for y
                newYVal = []
                for cl in range(colLens[-1]):
                    if cl in sigList:newYVal.append(yVal[cl])
                # write 
                xWriter.writerow(newXVal)
                yWriter.writerow(newYVal)
                yRegister_t[yVal.index(max(yVal))] +=1
            r+=1
            if not r%6000:print("Milestone",r)  
        #save new files
        xFile.close()
        yFile.close()
        #log results
        print("yRegister:",yRegister_t)
    #save keeped data
    clFile = open("undersampleList.json","w")
    clFile.write([allSignificant,colLens])
    clFile.close()