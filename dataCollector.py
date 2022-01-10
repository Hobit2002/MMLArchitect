import json,bs4,pandas,requests,time,traceback
try:
    #Load progress
    progressDict = json.load(open("BasicTraining/backups/progress.json"))
    runProg=progressDict["runs"]
    taskProg = progressDict["tasks"]
    data = json.load(open("BasicTraining/backups/unnDataBackup.json"))
    index = json.load(open("BasicTraining/backups/indexBackup.json"))
    #For each task:
    tasks = json.load(open("BasicTraining/taskData.json"))
    taskNum = len(tasks)
    for task in tasks[taskProg:]:
        try:
            print("%s/%s,(%s)"%(taskProg+1,taskNum,time.time()))
            #Visit its page
            tskAddress = "http://www.openml.org/"+task[0]
            req = requests.get(tskAddress)
            tskPage = bs4.BeautifulSoup(req.text,features="lxml")
            datainfo = tskPage.find("div",{"class":"datainfo"})
            datasetHref = datainfo.findChildren("a",recursive=False)[1]["href"]
            #visit the page of its dataset and load all the information about it
            dreq = requests.get("http://www.openml.org/"+datasetHref)
            dPage = bs4.BeautifulSoup(dreq.text,features="lxml")
            dataPropertyTagList = dPage.find_all("div",{"class":"dataproperty"})
            dataLabelTagList = dPage.find_all("div",{"class":"itemhead"})
            propertyVals = {}
            for pt,propTag in enumerate(dataPropertyTagList):
                tagText = propTag.get_text().replace(" ","")
                if tagText=="":propVal = None
                elif tagText.isdigit():propVal = int(tagText)
                else: propVal = float(tagText)
                propKey = dataLabelTagList[pt].get_text().replace(" ","").replace("\n","")
                propertyVals[propKey] = propVal
            #by multiple search request collect all these runs
            runCount = task[1]
            requestedRuns = 0
            tskID = task[0][2:]
            runList = []
            while runCount > requestedRuns:
                runAddr = "http://www.openml.org/search?type=run&from="+str(requestedRuns)+"&q=run_task.task_id%3A"+str(tskID)+"&dataonly=1"
                rlPage=bs4.BeautifulSoup(requests.get(runAddr).text,features="lxml")
                runList.extend(rlPage.find_all("div",{"class":"itemheadfull"}))
                requestedRuns+=100
            runHref = []
            for runItem in runList[runProg:]:
                try:
                    runHref =runItem.findChild("a")["href"]
                    #parse run information
                    hreq = requests.get("http://www.openml.org/"+runHref)
                    hPage = bs4.BeautifulSoup(hreq.text,features="lxml")
                    tableList= hPage.find_all("table")
                    paramTable = tableList[1]
                    rows= paramTable.findChildren("tr")
                    #put run information together with dataset information and insert it to the dataset
                    dataRow = propertyVals.copy()
                    #get model name
                    modelCol = rows[0].findChild("td").get_text().replace(" ","")
                    dataRow["model"] = modelCol
                    #get parameter settings
                    for row in rows[1:]:
                        columns = row.findChildren("td")
                        param = columns[0].get_text().replace(modelCol+"_","")
                        value=columns[1].get_text().replace(" ","")
                        if value.isdigit():value=int(value)
                        elif value.replace(".","").isdigit():value=float(value)
                        elif value =="null":value=None
                        elif value in ["true","false"]:value = bool(value[0].upper()+value[1:])
                        elif param =="steps":value = json.loads(value)
                        dataRow[param] = value
                    #get preficitve accuracy
                    measureTable = tableList[2]
                    cells= measureTable.findChildren("td")
                    for cell in cells:
                        parametr = cell.findChild("div",{"class":"col-md-3 evaltitle"}).get_text().replace(" ","").replace("\n","")
                        if parametr=="Predictiveaccuracy":
                            accuracy = float(cell.findChild("span",{"class":"mainvalue"}).get_text().replace(" ",""))
                            dataRow["accuracy"] = accuracy
                    #save data
                    data.append(dataRow)
                    index.append("T:%sR:%s"%(taskProg,runProg))
                except Exception as ex:
                    print(traceback.format_exc())
                    if type(ex).__name__ =="KeyboardInterrupt":
                        raise KeyboardInterrupt
                runProg +=1
            taskProg+=1
            runProg=0
        #if user interrups the program, save data to json backup and progress to its file
        except KeyboardInterrupt:
            jsonFile = open("BasicTraining/backups/unnDataBackup.json","w")
            jsonFile.write(json.dumps(data))
            jsonFile.close()
            jsonFile = open("BasicTraining/backups/indexBackup.json","w")
            jsonFile.write(json.dumps(index))
            jsonFile.close()
            progressFile = open("BasicTraining/backups/progress.json","w")
            progressFile.write(json.dumps({"runs":runProg,"tasks":taskProg}))
            progressFile.close()
            exit()
        except:
            print(traceback.format_exc())
            taskProg+=1
            runProg=0
        
    #Save progress and give user chance to stop the procedure
    dataFrame = pandas.DataFrame(data,index=index)
    dataFrame.to_csv("BasicTraining/unnumerizedData.csv")
except Exception:
    print(traceback.format_exc())