import json,bs4
from os import getcwd
print(getcwd())
#Open html file and initialize BeatifulSoup object
soup = bs4.BeautifulSoup(open("BasicTraining/source.html").read())
taskList = []
#Get all itemheadfull elements
taskDivs = soup.find_all("div",{"class":"itemheadfull"})
runBlocks = soup.find_all("i",{"class":"fa fa-star"})
tskCount = len(taskDivs)
for i,tskDiv in enumerate(taskDivs):
    print("Task:%s/%s"%(i+1,tskCount))
    href = str(tskDiv.findChild("a")['href'])
    runs = int(runBlocks[i].get_text().replace(" runs",""))
#insert those elements (href,run number) into the list
    taskList.append([href,runs])
#save the list as a json
jsonFile = open("BasicTraining/taskData.json","w")
jsonFile.write(json.dumps(taskList))
jsonFile.close()