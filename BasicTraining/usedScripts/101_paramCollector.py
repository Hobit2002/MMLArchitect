import bs4,json,requests
#Open html file and initialize BeatifulSoup object
soup = bs4.BeautifulSoup(open("BasicTraining/plyFlows.html").read(),features="lxml")
paramList = []
algorithmDict = {}
#Get all hrefs to flow objects
flowHrefs = soup.find_all("a")
hrefNum = len(flowHrefs)
for h,href in enumerate(flowHrefs):
    print("%s/%s"%(h+1,hrefNum))
    freq = requests.get("http://www.openml.org/"+href["href"])
    fPage = bs4.BeautifulSoup(freq.text,features="lxml")
    #get params
    table = fPage.find_all("table")[1]
    paramRows = table.findChildren("tr",recursive=True)
    model = fPage.find("h1").get_text().replace(" ","")
    algorithmDict[model] = {}
    for pRow in paramRows:
        columns = pRow.findChildren("td")
        param = columns[0].get_text()
        default=columns[2].get_text().replace("default: ","")
        if default.isdigit():default=int(default)
        elif default.replace(".","").isdigit():default=float(default)
        elif default =="null":default=None
        elif default in ["true","false"]:default = bool(default[0].upper()+default[1:])
        elif param =="steps":default = json.loads(default)
        #save parameters and their default values to the dict
        algorithmDict[model][param]=default
        #insert new parameters to the list
        if param not in paramList:paramList.append(param)
#save list and dict as json files
jsonFile = open("BasicTraining/parameterList.json","w")
jsonFile.write(json.dumps(paramList))
jsonFile.close()
jsonFile = open("BasicTraining/modelDict.json","w")
jsonFile.write(json.dumps(algorithmDict))
jsonFile.close()