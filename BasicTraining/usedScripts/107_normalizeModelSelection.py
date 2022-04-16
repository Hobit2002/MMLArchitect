import pandas, json,os
import numpy as np
from datasetFunc import *


def getMedian(column):
    column.sort()
    middlePoint = 150000
    middleElem = column[middlePoint]
    addIt = 0
    loopTok = 1
    while np.isnan(middleElem):
        addIt*=-1
        addIt+=loopTok%2
        middleElem = column[middlePoint+addIt]
        loopTok+=1
    return middlePoint

def norm_split(dataset):
    dataset.sample(frac=1).reset_index(drop=True)
    #one hot encoding of y
    yColList = []
    yList = []
    global modKeys
    for modKey in modKeys:
        dataset[modKey].fillna("endHere")
        one_hot =  pandas.get_dummies(dataset[modKey])
        if not one_hot.empty:
            yList.append(one_hot)
            yColList.append(one_hot.columns)
    #do normalization of x
    dropCols = []
    global modSelX
    for xKey in modSelX:
        dataset[xKey] = dataset[xKey]/max(dataset[xKey])#there are no negative numbers in the dataset => no risk of large absolute values
        try:
            dataset[xKey] = dataset[xKey].fillna(getMedian(dataset[xKey].tolist()))
        except IndexError:
            dropCols.append(xKey)
    for colList in dataset.columns:
        column = colList
        if column not in modSelX:dropCols.append(column)
    dataset = dataset.drop(columns = dropCols)
    #split it to y and x
    return dataset,yList,yColList

def tensorize(x):
    return np.asarray(x).astype('float32')

#load table
df = pandas.read_csv(open("modSel2.csv"))
#load parameterList and turn it into modSelX
parameterList = json.load(open("propertyList.json"))
modSelX = []
for dfParam in parameterList:
    if dfParam in df.columns:modSelX.append(dfParam)
#drop columns with all NaNs
df.dropna(axis=1, how='all')
modKeys = []
for mk in range(52):
    modKey = mkString(mk)
    if modKey in df.columns: modKeys.append(modKey)
#normalize those datasets
print("Preparing train set:")
x,yList,yColList = norm_split(df)
for i,y in enumerate(yList):
    print("modKey%s"%(i))
    yCols = list(yColList[i])
    if i: x = x.join(yList[i-1],lsuffix='_left', rsuffix='_right')
    mkDir = "modKeySets/mk%s"%(i)
    os.mkdir(mkDir)
    #split to train and test
    splitLine = round(len(df.index)*0.6)
    train_x = x.iloc[:splitLine,:]
    train_y = y.iloc[:splitLine,:]
    test_x = x.iloc[splitLine:,:]
    test_y = y.iloc[splitLine:,:]
    np.savetxt(mkDir+"/train_x.csv",train_x,delimiter=',')
    np.savetxt(mkDir+"/train_y.csv",train_y,delimiter=',')
    np.savetxt(mkDir+"/test_x.csv",test_x,delimiter=',')
    np.savetxt(mkDir+"/test_y.csv",test_y,delimiter=',')
    ycFile = open(mkDir+"/mkCols.json","w")
    ycFile.write(json.dumps(yCols))
    ycFile.close()
#x = tensorize(x)
#y = tensorize(yList[0])
#print("Preparing test set:")
#test_x,test_yList = norm_split(test_dataset)
#test_y = test_yList[0]
#print("x before:",test_x)
#test_x = tensorize(test_x)
#print("x after:",test_x)
