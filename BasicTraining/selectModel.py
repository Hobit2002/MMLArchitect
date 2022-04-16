import tensorflow as tf
import numpy as np
import json

modKeySetsPath = "S:/git/MMLarchitect/modKeySets"
backupPath = "modKeySets"

def insertNulls(array,modNum):
    #load output columns
    dynamicPath = "/mk%s/"%(modNum) + "mkCols.json"
    try:
        colfile = open(modKeySetsPath + dynamicPath)
    except FileNotFoundError:
        colfile = open(backupPath + dynamicPath)
    columns = json.load(colfile)
    #for each of them insert null to the array
    return np.append(array,[0 for c in columns])

#load dataset information
def chooseModel(descArray):
    #load selectModelCheatsheet and build model rating structure
    cheatsheet = json.load(open("selectModelCheatsheet.json"))
    modelValues = {}
    for model in cheatsheet["models"]:
        modelValues[model] = 0
    #put data to each layer metamodel
    for i in range(0,21):
        #get predicitons
        if i: descArray = insertNulls(descArray,i-1)
        path = modKeySetsPath+"/mk%s/"%(i)
        metamodel = tf.keras.models.load_model(path+"model.h5")
        predictions = metamodel.predict(descArray[None])
        #load mkCols
        columns = json.load(open(path+"mkCols.json"))
        #set mkConst
        mkConst = 1/(i+5)
        #link columns to modelValues
        for c,column in enumerate(columns):
            prediction = predictions[0][c]*mkConst
            try:
                for modelPossibility in cheatsheet["map"][column]:
                    modelValues[cheatsheet["models"][modelPossibility]] += prediction
            except KeyError:
                pass

    #choose the model with highest value
    maxvals = [-1*10**5,-1*10**6,-1*10**7,-1*10**8]
    maxmods = [None,None,None]
    delEnd = False
    for k,v in modelValues.items():
        for vi,val in enumerate(maxvals):
            if v > val:
                maxvals.insert(vi,v)
                maxmods.insert(vi,k)
                delEnd = True
                break
        if delEnd:
            del maxmods[-1]
            del maxvals[-1]
            delEnd = False
                
    return maxmods,maxvals