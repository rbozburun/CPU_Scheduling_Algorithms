#!/usr/bin/env/ python
# -*- coding: utf8 -*-

import sys

class Task:
    def __init__(self,name,arrival_time,priortiy,burst,execution_time):
        self.name = name
        self.arrival_time = int(arrival_time)
        self.priority = int(priortiy)
        self.burst = int(burst)
        self.execution_time = int(execution_time)
        self.wait_time = -1
        self.finish_time = 0
        self.remaining_burst = int(burst)
        self.isFirstRunning = True
        self.lastBurstTime = 0 #After last burst time current cpu time to calculate total waiting time

class CPU:
    def __init__(self,time):
        self.time = time
    
def getFields(taskStr):
    fields = taskStr.split(',')
    task_name = fields[0]
    arrival_time = fields[1]
    priority = fields[2]
    burst = fields[3]
    return [task_name,arrival_time,priority,burst]

def getTaskObjects(task_list):
    task_objs = []
    for task in task_list:
        task_fields = getFields(task)
        task_objs.append(Task(task_fields[0],task_fields[1],task_fields[2],task_fields[3],-1))
    
    return task_objs  

def switcher(algortihm,task_objs,cpu):
    if (algortihm == "fcfs"):
        return fcfs(task_objs,cpu)
    
    elif (algortihm == "sjf"):
        return sjf(task_objs,cpu)
    
    elif (algortihm == "pri"):
        return pri(task_objs,cpu)
    
    elif (algortihm == "rr"):
        return rr(task_objs,cpu)
    
    elif (algortihm == "pri-rr"):
        return pri_rr(task_objs,cpu)

    else:
        print("Wrong algorithm name!")
        
def main():
    tasks_file = open(sys.argv[2],'r')
    tasks = tasks_file.readlines()
    tasks_without_newline = []
    
    for task in tasks:
        tasks_without_newline.append(task.replace("\n",""))
    
    task_objs = getTaskObjects(tasks_without_newline)
    cpu = CPU(0)
    
    #Switchs program to given algorithm
    switcher(sys.argv[1],task_objs,cpu)
    
#First-come, first-served
def fcfs(tasks,cpu):
    #Sort object accoridng to their arrival_time attribute.
    tasks.sort(key=lambda x: x.arrival_time)
    
    outF = open("output.txt","w")
    outF.write("First Come First Serve Scheduling\n------------------------")

    #Run tasks
    for task in tasks:
        if not cpu.time < task.arrival_time:
            #Set execution time for each object. Execution time is current cpu time
            task.execution_time = cpu.time
            
            outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst))
            cpu.time += task.burst
            outF.write("\nTask " + task.name + " is finished.\n")
            
        else:
            cpu.time += task.arrival_time
            outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst))
            cpu.time += task.burst
            outF.write("\nTask " + task.name + " is finished.\n")
    outF.write("------------------------\n")
    
    total_wait_time = 0
    turnaround_time = 0
    for task in tasks:
        total_wait_time += task.execution_time - int(task.arrival_time)
        turnaround_time += (task.execution_time + task.burst) - task.arrival_time
        
    outF.write("Average Waiting Time: " + str(total_wait_time/len(tasks)))
    outF.write("\nAverage Turnaround Time: " + str(turnaround_time/len(tasks)))
          

#Shortest-job-first 
def sjf(tasks,cpu):
    taskCount = len(tasks)
    executed_tasks = [] # To calculate turnaround times and waiting time
    tasks.sort(key=lambda x: x.burst)
    
    outF = open("output.txt","w")
    outF.write("Shortest Job First Serve Scheduling\n------------------------")

    #Runs until all tasks execute
    while(len(executed_tasks) != taskCount):
        #For each CPU time, check all tasks
        for task in tasks:
            if (cpu.time >= task.arrival_time):
                task.execution_time = cpu.time
                outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst))
                cpu.time += task.burst
                outF.write("\nTask " + task.name + " is finished.\n")
                executed_tasks.append(task)
                tasks.remove(task)
                break
        #After check all tasks, increase CPU time
        cpu.time += 1
        
    outF.write("------------------------\n")
    total_wait_time = 0
    turnaround_time = 0
    for task in executed_tasks:
        total_wait_time += task.execution_time - int(task.arrival_time)
        turnaround_time += (task.execution_time + task.burst) - task.arrival_time
        
    outF.write("Average Waiting Time: " + str(total_wait_time/taskCount))
    outF.write("\nAverage Turnaround Time: " + str(turnaround_time/taskCount))
            
  
#Priortiy scheduling - 1 > 2 (priority)
def pri(tasks,cpu):
    taskCount = len(tasks)
    executed_tasks = [] # To calculate turnaround times and waiting time
    tasks.sort(key=lambda x: x.priority, reverse=True)
    
    outF = open("output.txt","w")
    outF.write("Highest Priority Job First Serve Scheduling\n------------------------")

    #Runs until all tasks execute
    while(len(executed_tasks) != taskCount):
        #For each CPU time, check all tasks
        for task in tasks:
            if (cpu.time >= task.arrival_time):
                task.execution_time = cpu.time
                outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst))
                cpu.time += task.burst
                outF.write("\nTask " + task.name + " is finished.\n")
                executed_tasks.append(task)
                tasks.remove(task)
                break
        #After check all tasks, increase CPU time
        cpu.time += 1

    outF.write("------------------------\n")
    total_wait_time = 0
    turnaround_time = 0
    for task in executed_tasks:
        total_wait_time += task.execution_time - int(task.arrival_time)
        turnaround_time += (task.execution_time + task.burst) - task.arrival_time
        
    outF.write("Average Waiting Time: " + str(total_wait_time/taskCount))
    outF.write("\nAverage Turnaround Time: " + str(turnaround_time/taskCount))
    
    pass


#Round-robin
def rr(tasks,cpu):
    #Time quantum = 10
    taskCount = len(tasks)
    executed_tasks = [] #To calculate avg waiting time
    tasks.sort(key=lambda x: x.arrival_time)
    
    outF = open("output.txt","w")
    outF.write("Round Robin CPU Scheduling\n------------------------")
    #Runs until all tasks execute
    while(len(executed_tasks) != taskCount):
        #For each CPU time, check all tasks
        for task in tasks:
            if (cpu.time >= task.arrival_time):
                if task.wait_time == -1:
                    task.execution_time = cpu.time
                    task.wait_time = task.execution_time - task.arrival_time #Holds waiting time for task object.
                    if task.burst > 10:
                        task.burst -= 10
                        outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(10) +"\nRemaining Burst: " + str(task.burst) +"\n")
                        cpu.time += 10
                
                    else: #Task finishes
                        cpu.time += task.burst
                        outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst) + "\nRemaining Burst: 0")
                        outF.write("\nTask " + task.name + " is finished.\n")
                        task.finish_time = cpu.time
                        executed_tasks.append(task)
                        tasks.remove(task)
                        
                        
                else:
                    #If task executed at least one times, we have to calculate from it's waiting time from previous execution
                    task.wait_time += cpu.time - task.execution_time
                    task.execution_time = cpu.time #Update task's execution time to current CPU time.
                    
                    if task.burst > 10:
                        outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst )  + "\nRemaining Burst: " + str(task.burst - 10) +"\n")
                        cpu.time += 10
                        task.burst -= 10
                    else: #Task finishes
                        cpu.time += task.burst
                        outF.write("\nWill run Name: " + task.name + "\nPriority: " + str(task.priority) + "\nBurst: " + str(task.burst) + "\nRemaining Burst: 0")
                        outF.write("\nTask " + task.name + " is finished.\n")
                        task.finish_time = cpu.time
                        executed_tasks.append(task)
                        tasks.remove(task)
                    
        #After check all tasks, increase CPU time
        cpu.time += 1
        
    outF.write("------------------------\n")
    total_wait_time = 0
    turnaround_time = 0
    for task in executed_tasks:
        total_wait_time += task.wait_time
        turnaround_time += task.finish_time - task.arrival_time
        
    outF.write("Average Waiting Time: " + str(total_wait_time/taskCount))
    outF.write("\nAverage Turnaround Time: " + str(turnaround_time/taskCount))


#Priority with round-robin
def pri_rr(tasks,cpu):
    #Time quantum = 10
    taskCount = len(tasks)
    executed_tasks = [] #To calculate avg waiting time
    tasks.sort(key=lambda x: x.arrival_time)
    
    outF = open("output.txt","w")
    outF.write("Priority with Round Robin Scheduling\n------------------------")
    
    readyQ = []
    cpu.time = -1
    while(len(executed_tasks) != taskCount):
        tasksLen = len(tasks)
        for i in range(tasksLen):
            if cpu.time >= tasks[0].arrival_time:
                readyQ.append(tasks[0])
                tasks.remove(tasks[0])
        
        if len(readyQ) > 0:
            if len(readyQ) == 1: #Finish task
                readyQ[0].execution_time = cpu.time
                cpu.time += readyQ[0].burst
                outF.write("\nWill run Name: " + readyQ[0].name + "\nPriority: " + str(readyQ[0].priority) + "\nBurst: " + str(readyQ[0].burst) + "\nRemaining Burst: 0")
                outF.write("\nTask " + readyQ[0].name + " is finished.\n")
                readyQ[0].finish_time = cpu.time
                readyQ[0].wait_time = readyQ[0].execution_time - readyQ[0].arrival_time
                executed_tasks.append(readyQ[0])
                readyQ.remove(readyQ[0])
                
            
            elif (len(readyQ)) > 1: #Apply RR
        
                readyQ.sort(key=lambda x: x.priority, reverse=True)
                temp = readyQ[0]
                rrQ = []
                idx = 0
                rrQ.append(temp)
                readyQ.remove(temp)
                
                
                #ReadyQ'daki elemanı rrQ'ya at
                for i in range(len(readyQ)):
                    
                    if temp.priority == readyQ[idx].priority: #Append to rrQ
                        rrQ.append(readyQ[idx])
                        readyQ.remove(readyQ[idx])
                        idx -= 1
                    
                    # Fordan çık
                    else:
                        if len(rrQ) == 1: #Finish task
                            rrQ[0].execution_time = cpu.time
                            cpu.time += rrQ[0].burst
                            outF.write("\nWill  run Name: " + rrQ[0].name + "\nPriority: " + str(rrQ[0].priority) + "\nBurst: " + str(rrQ[0].remaining_burst) + "\nRemaining Burst: 0")
                            outF.write("\nTask " + rrQ[0].name + " is finished.\n")
                            rrQ[0].finish_time = cpu.time
                            rrQ[0].wait_time = rrQ[0].execution_time - rrQ[0].arrival_time
                            executed_tasks.append(rrQ[0])
                            rrQ.remove(rrQ[0])
                            break
                        
                        if len(rrQ) > 1: #Apply RR
                            while(len(rrQ) > 0):
                                if len(rrQ) == 1: #Finish task
                                    rrQ[0].execution_time = cpu.time
                                    cpu.time += rrQ[0].burst
                                    outF.write("\nWill  run Name: " + rrQ[0].name + "\nPriority: " + str(rrQ[0].priority) + "\nBurst: " + str(rrQ[0].remaining_burst) + "\nRemaining Burst: 0")
                                    outF.write("\nTask " + rrQ[0].name + " is finished.\n")
                                    rrQ[0].finish_time = cpu.time
                                    rrQ[0].wait_time = rrQ[0].execution_time - rrQ[0].arrival_time
                                    executed_tasks.append(rrQ[0])
                                    rrQ.remove(rrQ[0])
                                    
                                
                                for process in rrQ:
                                    if process.remaining_burst > 10:
                                        if process.isFirstRunning == True:
                                            process.isFirstRunning = False
                                            process.execution_time = cpu.time
                                            process.wait_time = process.execution_time - process.arrival_time
                                            
                                        else:
                                            process.wait_time += cpu.time - process.lastBurstTime 
                                            
                                        process.remaining_burst -= 10
                                        outF.write("\nWill run  Name: " + process.name + "\nPriority: " + str(process.priority) + "\nBurst: " + str(10) +"\nRemaining Burst: " + str(process.remaining_burst) +"\n")
                                        cpu.time += 10
                                        process.lastBurstTime = cpu.time
                                        
                                
                                    else: #Task finishes
                                        process.execution_time = cpu.time
                                        cpu.time += process.remaining_burst
                                        outF.write("\nWill run  Name: " + process.name + "\nPriority: " + str(process.priority) + "\nBurst: " + str(process.remaining_burst) + "\nRemaining Burst: 0")
                                        outF.write("\nTask " + process.name + " is finished.\n")
                                        process.finish_time = cpu.time
                                        process.wait_time = process.execution_time - process.arrival_time
                                        executed_tasks.append(process)
                                        rrQ.remove(process)                           
        else:
            cpu.time += 1
            
    outF.write("------------------------\n")
    total_wait_time = 0
    turnaround_time = 0
    for task in executed_tasks:
        total_wait_time += task.wait_time
        turnaround_time += task.finish_time - task.arrival_time
            
    outF.write("Average Waiting Time: " + str(total_wait_time/taskCount))
    outF.write("\nAverage Turnaround Time: " + str(turnaround_time/taskCount))   
           
if __name__ == "__main__":
    main()