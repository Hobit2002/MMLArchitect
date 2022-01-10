import bs4,json
import json,bs4
#Open html file and initialize BeatifulSoup object
soup = bs4.BeautifulSoup(open("BasicTraining/datasetProperties.html").read())
propertyList = []
#Get all itemheadfull elements
propBlocks = soup.find_all("a",{"class":"iconpurple"})
for propDiv in propBlocks:
    propertyList.append(propDiv.get_text().replace("\n ",""))
#save the list as a json
jsonFile = open("BasicTraining/propertyList.json","w")
jsonFile.write(json.dumps(propertyList))
jsonFile.close()