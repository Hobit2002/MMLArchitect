import csv,datetime
import databaseSettings

#establish database connection
mydb = databaseSettings.connect()
cursor = mydb.cursor()
rowList = []
#get  all task data
cursor.execute("SELECT responsibleID,assignedID,complete, steplist,reminder,priority,dtPlanStart,dtPlanEnd,timeExpectedMin,timeExpectedMax,dtLastModif,dtCreated FROM tskTask")
tasks = cursor.fetchall()
keyPoint = None
keyCount = -1
for t,task in enumerate(tasks):
    row = {}
    now = datetime.datetime.now()
    row["complete"] = task[2] == "CO"
    row["steplist"] = task[3] != None
    row["reminder"] = task[4] != None
    row["priority"] = task[5]
    row["dtPlanStart"] = (task[6] - now).days
    row["dtPlanEnd"] = (task[7] - now).days
    row["timeExpectedMin"] = task[8]
    row["timeExpectedMax"] = task[9]
    row["dtLastModif"] = (task[10] - now).days
    row["dtCreated"] = (task[11] - now).days
    #get assigned/responsible data
    for u,uKey in enumerate(["responsible","assigned"]):
        uID = task[u]
        if uID == None:continue
        #events
        cursor.execute("SELECT tskInvitationID FROM tskwInvitation WHERE subjectName = 'sysUser' AND subjectID = %s AND dtStart < %s",[uID,task[7]])
        row[uKey+"Events"] = len(cursor.fetchall())
        #tasks
        for role in ["responsible","assigned"]:
            command = "SELECT priority FROM tskTask WHERE %sID = %s"%(role,uID)
            if task[7]!=None:command+= " AND dtPlanEnd < '%s'"%(task[7])
            cursor.execute(command)
            priorities = cursor.fetchall()
            row[uKey+role+"Tasks"] = len(priorities)
            prioritySum = 0
            for priority in priorities:
                if(type(priority)==tuple):priority= list(priority)[0]
                prioritySum += priority
            row[uKey+role+"TasksPriority"] = prioritySum/row[uKey+role+"Tasks"] if row[uKey+role+"Tasks"] else None
    if len(row.keys()) > keyCount:
        keyCount = len(row.keys())
        keyPoint = t
    rowList.append(row)

#generate table
file = open("sampleData.csv","w")
table = csv.DictWriter(file,rowList[keyPoint].keys())
for row in rowList:
    table.writerow(row)
file.close()