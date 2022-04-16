from asyncio import events, tasks
import random,csv,datetime
from tokenize import group

from matplotlib.pyplot import table

gameLength = 0
priorities = [1,1,2,2,3,3,3,4,4,5]
calendar = {gd : [] for gd in range(400)}
upcoming = {1:[],2:[]}

def today():
    return datetime.datetime.now() + datetime.timedelta(days= gameLength)

class Event:

    def __init__(self,organizer):
        durAmendment = 15*(organizer.extroversion + organizer.demands)
        self.duration = random.randint(40 + durAmendment,160+durAmendment)/240
        self.dtStart = datetime.datetime.now() + datetime.timedelta(days= gameLength + random.randint(1,7))

class Task:
    
    durations = []

    def getHighestPriority(taskList):
        obj = None
        highestPriority = -1
        for task in taskList:
            if task.priority > highestPriority:
                highestPriority = task.priority
                obj = task
        return obj

    def __init__(self,duration,priority):
        self.complete = 0
        self.priority = priority
        self.duration = duration
        self.responsible = None
        self.assigned = None
        #estimate expected time
        Task.durations.append(duration)
        self.timeExpectedMin = round(duration * random.randint(6,9)/10)
        self.timeExpectedMax = round(duration * random.randint(11,14)/10)
        self.dtPlanStart = today() + datetime.timedelta(days= random.randint(2,7))
        self.dtPlanEnd = self.dtPlanStart + datetime.timedelta(days= self.timeExpectedMax+random.randint(0,2))
        calendar[round((self.dtPlanEnd - datetime.datetime.now()).days)].append(self)
        self.dtCreated = datetime.datetime.now() + datetime.timedelta(days= gameLength)
        self.dtLastModif = self.dtCreated
        #derived
        averageDuration = sum(Task.durations)/len(Task.durations)
        self.steplist = int( random.randint(-3,3) + duration - averageDuration > 0)
        self.reminder = int(priority > random.choice(priorities))

    def rowDataX(self):
        now = today()
        taskProps = [self.steplist,self.reminder,
                    self.priority,(self.dtPlanStart - now).days,
                    (self.dtPlanEnd- now).days,
                    self.timeExpectedMin,self.timeExpectedMax,
                    (self.dtLastModif- now).days,(self.dtCreated- now).days]
        for figure in [self.responsible,self.assigned]:
            taskProps.append(len(figure.events))
            for tskType in [figure.responsible,figure.assigned]:
                taskProps.append(len(tskType))
                prioritySum = 0
                for task in tskType:prioritySum+=task.priority
                taskProps.append(prioritySum/len(tskType) if len(tskType) else 0)
        return taskProps

class Worker:

    def __init__(self,group):
        self.status = random.choice([1,1,1,2,2,2,3,3,3,4,4])
        self.responsible = []
        self.assigned = []
        self.events = []
        self.effectiveTime = random.randint(4,9)/10
        self.demands = random.randint(5,7)
        self.extroversion = random.randint(7,13)
        self.helpfulness = random.randint(8,14)/10
        self.leadership = random.randint(9,11)/10
        self.group = group
        self.name = self.generateName()
        
    def generateName(self):
        letters = ["qwrtzpsdfghjklxcvbnm","euioay"]
        length = random.randint(4,8)
        name = ""
        for i in range(length):
            name+=random.choice(letters[i%2])
        return name[0].upper()+name[1:]
    
    def work(self):
        #go to your events
        efTime = self.effectiveTime
        for event in self.events:
            if event.dtStart == today():
                efTime-=event.duration
        #spend the rest of the time mostly with priority tasks
        if efTime > 0:
            #assigned
            if len(self.assigned):
                aTask = Task.getHighestPriority(self.assigned)
                if len(self.assigned):
                    workingTime = efTime*(0.6 + self.status/10)
                    aTask.duration -= workingTime
                    efTime -= workingTime
                    while aTask.duration <= 0:
                        aTask.complete = 1
                        doneTask = aTask
                        print("Day %s.:%s completed his assignment %s days before %s"%(gameLength,self.name,(doneTask.dtPlanEnd-today()).days,doneTask.dtPlanEnd))
                        aTask.dtLastModif = today()
                        self.assigned.remove(aTask)
                        aTask =  Task.getHighestPriority(self.assigned)
                        if aTask != None: aTask.duration += doneTask.duration
                        else:break
                        
            #responsible
            rTask = Task.getHighestPriority(self.responsible)
            overseen = []
            while efTime > 0 and len(self.responsible):
                efTime -= 0.1
                rTask.duration *= self.leadership
                rTask.dtLastModif = today()
                overseen.append(rTask)
                self.responsible.remove(rTask)
                rTask = Task.getHighestPriority(self.responsible)
            self.responsible+=overseen
        #lead others
        if self.status < 4:
            if not random.randint(0,self.status+1):self.lead() 
    
    def lead(self):
        #task or event?
        if random.randint(1,18) >= self.extroversion:
            #make task
            duration = random.randint(self.demands*4-2,self.demands*4+4)/10
            task = Task(duration,random.choice(priorities+2*[5-self.status]))
            #connect it to workers
            task.responsible = self
            self.responsible.append(task)
            #assign
            mostWilling = None
            highestWillingness = -2*10**16
            for worker in self.group.workers:
                if worker.status >= self.status:
                    workerWillingness= worker.showWillingness()
                    if highestWillingness < workerWillingness:
                        highestWillingness = workerWillingness
                        mostWilling = worker
            mostWilling.assigned.append(task)
            task.assigned = mostWilling
            print("Day %s.:%s assigned the task of priority %s and duration %s to %s"%(gameLength,self.name,task.priority,task.timeExpectedMax,mostWilling.name) )


        else:
            #make event
            event = Event(self)
            #invite
            attendees = random.choices(self.group.workers, k = random.randint(2,len(self.group.workers)))
            if self not in attendees:attendees.append(self)
            for attendee in attendees:
                attendee.events.append(event)

    def showWillingness(self):
        #busyness
        otherPriorities = 0
        workLength = 0
        for task in self.assigned:
            otherPriorities+= task.priority
            workLength+=task.duration
        busyness = otherPriorities*workLength
        return self.helpfulness - busyness*10**(-8)

class Group:

    def __init__(self):
        self.workers = []
        for i in range(random.randint(6,8)):
            self.workers.append(Worker(self))
    
    def work(self):
        for worker in self.workers:
            worker.work()

#open csv
file = open("virtualData.csv","w")
table = csv.writer(file)       
#generate groups
groups = []
for i in range(100):groups.append(Group())
#wait year
for gameLength in range(365):
    for group in groups:
        group.work()
    #write new rows
    for t,task in enumerate(calendar[gameLength]):
        table.writerow([task.complete]+upcoming[1][t])
    #take a shot of upcoming tasks
    upcoming[1] = upcoming[2]
    upcoming[2] = []
    for task in calendar[gameLength+2]:upcoming[2].append(task.rowDataX())
    
file.close()
