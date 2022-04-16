import csv,math
from locale import currency
from pydoc import describe
from unicodedata import numeric

from numpy import broadcast

class Broadcaster:

    def __init__(self,eventList):
        self.events = {}
        self.parameter = 0
        for event in eventList:
            self.events[event] = []

    def add(self,event,listener):
        self.events[event].append(listener)

    def remove(self,event,listener):
        index = self.events[event].index(listener)
        del self.events[event][index]
    
    def broadcast(self,event,parameter = None):
        if parameter != None:self.parameter = parameter
        for listener in self.events[event]:
            listener.calculate(event)

class Attribute:
    
    listenTo = []
    
    def __init__(self,broadcaster):
        self.value = 0
        self.broadcaster = broadcaster
        for event in self.listenTo:
            broadcaster.add(event,self)

    def calculate(self,event):
        self.value += 1

    def show(self):
        return self.value

class NumberOfInstances(Attribute):

    listenTo = ["newRow"]

class NumberOfFeatures(Attribute):

    listenTo =["newRow","newColumn"]

    def calculate(self,event):
        if event == "newColumn":
            self.value += 1
        elif event == "newRow":
            self.broadcaster.remove("newRow",self)
            self.broadcaster.remove("newColumn",self)

class NumberOfClasses(Attribute):

    listenTo =["classesSet"]

    def calculate(self,event):
        self.value = len(self.broadcaster.parameter)

class NumberOfMissingValues(Attribute):

    listenTo = ["newColumn"]

    def calculate(self, event):
        if self.broadcaster.parameter == '':
            self.value += 1

class NumberOfInstancesWithMissingValues(Attribute):

    listenTo = ["newRow","newColumn"]

    def __init__(self,broadcaster):
        self.value = 0
        self.broadcaster = broadcaster
        self.penetratedRow = 0
        for event in self.listenTo:
            broadcaster.add(event,self)

    def calculate(self, event):
        if event == "newColumn":
            if self.broadcaster.parameter == '':
                self.penetratedRow = 1
        elif event == "newRow" and self.penetratedRow:
            self.value += 1
            self.penetratedRow = 0
        
class PercentageOfSymbolicFeatures(Attribute):

    listenTo = ["newColumn"]

    def calculate(self, event):
        pass

    def show(self):
        newColListeners = self.broadcaster.events["newColumn"]
        boradcastIndex = newColListeners.index(self)
        numeric = newColListeners[boradcastIndex +1].show()
        symbolic = newColListeners[boradcastIndex +2].show()
        return symbolic/(numeric+symbolic) * 100

class NumberOfNumericFeatures(Attribute):

    listenTo = ["newColumn","newRow"]

    def __init__(self,broadcaster):
        self.value = 0
        self.broadcaster = broadcaster
        self.notNumericIndexes = []
        self.numericIndexes = []
        self.currentIndex = 0
        for event in self.listenTo:
            broadcaster.add(event,self)
    
    def giveNumericList(self):
        return self.numericIndexes

    def giveSymbolicList(self):
        return self.notNumericIndexes

    def calculate(self, event):
        if event== "newColumn":
            if self.currentIndex not in self.notNumericIndexes:
                try:
                    float(self.broadcaster.parameter)
                    if self.currentIndex not in self.numericIndexes:
                        self.numericIndexes.append(self.currentIndex)
                except ValueError:
                    if self.broadcaster.parameter != '':
                        self.notNumericIndexes.append(self.currentIndex)
            self.currentIndex +=1
        elif event == "newRow":
            self.currentIndex = 0
        
class NumberOfSymbolicFeatures(Attribute):

    listenTo = ["newColumn"]

    def calculate(self, event):
        pass

    def show(self):
        newColListeners = self.broadcaster.events["newColumn"]
        boradcastIndex = newColListeners.index(self)
        return len(newColListeners[boradcastIndex -1].giveSymbolicList())

class MeanAttributeEntropy(Attribute):

    listenTo = ["newColumn","newRow"]

    def __init__(self,broadcaster):
        self.broadcaster = broadcaster
        self.currentIndex = 0
        self.firstRow = True
        self.entropies = {}
        for event in self.listenTo:
            broadcaster.add(event,self)

    def calculate(self, event):
        if event == "newColumn":
            if self.firstRow:
                self.entropies[self.currentIndex] = [self.broadcaster.parameter]
            else:
                self.entropies[self.currentIndex].append(self.broadcaster.parameter)
            self.currentIndex += 1
        elif event == "newRow":
            self.currentIndex = 0
            self.firstRow = False

    def getIndexes(self):
        newColListeners = self.broadcaster.events["newColumn"]
        boradcastIndex = newColListeners.index(self)
        numberOfNumericFeatures = newColListeners[boradcastIndex -2]
        return numberOfNumericFeatures.giveSymbolicList(),numberOfNumericFeatures.giveNumericList()

    def pdf(self,x,median,variance):
        return math.e**((-(x-median)**2)/2*variance)/((2*variance*math.pi)**0.5)

    def show(self):
        meanEntropy = 0
        symbolicList,numericList = self.getIndexes()
        for i in range(len(self.entropies.keys())):
            attributeEntropy = 0
            if i in symbolicList:
                symbols = {}
                #add symbols and their occurence
                for symbol in self.entropies[i]:
                    if symbol not in symbols.keys():
                        symbols[symbol] = 1
                    else:
                        symbols[symbol]+=1
                #calculate entropy
                totalCases = sum(symbols.values())
                for symbol in self.entropies[i]:
                    p = symbols[symbol]/totalCases
                    attributeEntropy += -p*math.log(p,2)

            elif i in numericList:
                #turn into floats
                self.entropies[i] =list(filter(lambda a: a != '', self.entropies[i]))
                for index in range(len(self.entropies[i])):
                    self.entropies[i][index] = float(self.entropies[i][index])
                #construct gausian function
                #median
                medianList = self.entropies[i].copy()
                medianList.sort()
                median = medianList[len(medianList)//2]
                #variance
                varSum = 0
                for num in medianList:
                    varSum += (num - median)**2
                variance = varSum/len(medianList)
                #calculate entropy
                for x in self.entropies[i]:
                    attributeEntropy+=self.pdf(x,median,variance)
            meanEntropy += attributeEntropy
        return meanEntropy/len(self.entropies.keys())

class MinorityClassSize(Attribute):

    listenTo = ["classesSet","classRow"]

    def __init__(self,broadcaster):
        self.broadcaster = broadcaster
        self.classOccurences = {}
        for event in self.listenTo:
            broadcaster.add(event,self)

    def calculate(self, event):
        if event == "classesSet":
            for classSymbol in self.broadcaster.parameter:
                self.classOccurences[classSymbol] = 0
        elif event == "classRow":
            self.classOccurences[self.broadcaster.parameter] += 1
        
    def show(self):
        occurences = self.classOccurences.values()
        return (sum(occurences)-max(occurences))/(sum(occurences))

def describeDataset(path,classIndex,classList):
    #construct handlers (order must be same as in thge code)
    broadcaster = Broadcaster(["newRow","newColumn","classesSet","classRow"])
    handlers = []
    for handlerClass in [NumberOfInstances,NumberOfFeatures,NumberOfClasses,
                        NumberOfMissingValues,PercentageOfSymbolicFeatures,
                        NumberOfNumericFeatures,NumberOfSymbolicFeatures,
                        MeanAttributeEntropy,MinorityClassSize]:
        handlers.append(handlerClass(broadcaster))
    #classes information
    broadcaster.broadcast("classesSet",classList)
    #loop the table
    file = open(path)
    table = csv.reader(file)
    for row in table:
        if not len(row):continue
        for c,column in enumerate(row):
            if c!= classIndex:broadcaster.broadcast("newColumn",column)
            else:
                broadcaster.broadcast("classRow",column)
        broadcaster.broadcast("newRow")
    #show results
    resultList = []
    for handler in handlers:
        resultList.append(handler.show())
    return resultList

    

        