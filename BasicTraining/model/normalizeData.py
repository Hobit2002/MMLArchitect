from statistics import mode
import pandas
import numpy as np

def getMedian(column):
    column.sort()
    middlePoint = len(column)//2
    middleElem = column[middlePoint]
    addIt = 0
    loopTok = 1
    while np.isnan(middleElem):
        addIt*=-1
        addIt+=loopTok%2
        middleElem = column[middlePoint+addIt]
        #print("%s ... %s"%(middlePoint+addIt,column[middlePoint+addIt]))
        loopTok+=1
    return middlePoint

def normalize(dataset):
    dataset.sample(frac=1).reset_index(drop=True)
    #normalize numeric values
    dropCols = []
    for xKey in dataset.columns:
        #do not normalize boolean columns
        nanLess = list(filter(lambda a: not np.isnan(a),dataset[xKey].tolist()))
        if not len(nanLess): print(xKey)
        if len(list(filter(lambda a:a not in [0,1] and not np.isnan(a),dataset[xKey].tolist()))):
            dataset[xKey] = dataset[xKey]/max((dataset[xKey]**2)**0.5)#multiplying is neccessary - because of negative numbers presence 
        dataset[xKey] = dataset[xKey].fillna(getMedian(nanLess))
    return dataset

#load table
df = pandas.read_csv(open("virtualData.csv"))#("sampleData.csv"))
#drop columns with all NaNs
print("Columns before removing:%s"%(df.columns))
df= df.dropna(axis=1, how='all')
print("Columns after removing:%s"%(df.columns))
#normalize
df = normalize(df)
#split to train and test x and y
splitLine = round(len(df.index)*0.6)
train_x = df.iloc[:splitLine,1:]
train_y = df.iloc[:splitLine,0]
test_x = df.iloc[splitLine:,1:]
test_y = df.iloc[splitLine:,0]
np.savetxt("train_x.csv",train_x,delimiter=',')
np.savetxt("train_y.csv",train_y,delimiter=',')
np.savetxt("test_x.csv",test_x,delimiter=',')
np.savetxt("test_y.csv",test_y,delimiter=',')