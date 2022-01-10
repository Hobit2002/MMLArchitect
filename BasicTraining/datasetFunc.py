import csv

def readDict(filename,retFile=False):
    file = open(filename)
    if retFile:return csv.DictReader(file), file
    else:return csv.DictReader(file)

def generateModKeys(value,mkRange=52):
    modKeys = {}
    cond = type(value) in [str,int,bool,float]
    for i in range(mkRange):
        if not cond: value = value.copy()
        modKeys["modKey%s"%(i)] = value
    return modKeys

def mkString(mk):
    return "modKey%s"%(mk)
