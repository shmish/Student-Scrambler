import Tkinter
from tkFileDialog import askopenfilename
from random import *
import time
import tkFont
import math

def center_window(w, h):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, 0))

def callback(event):
    global stop
    print ("stop")
    stop = 1

def quitter(event):
    global root
    root.destroy()

def striplist(nameList):
    return([x.strip() for x in nameList])


def fillnames(fname):
    i = 0
    for line in fname:
        peopleList.append(line)
        i += 1
    fname.close()
    return i

## method for getting the groupings so all groups have 3 or 4 students
def grouping():
    extras = numberNames%4 ## need to make sure the groups are 3 or 4 in size
    fourGroups = numberNames/4
    if extras == 2:  ## if there are 2 extras, get a 3rd from one group of 4
        fourGroups = fourGroups - 1
        numGroups = (fourGroups, 2)
    elif extras == 1:  ## if there is 1 extra, get a 2nd and 3rd from two groups of 4
        fourGroups = fourGroups - 2
        numGroups = (fourGroups,3)
    elif extras == 3:
        numGroups = (fourGroups,1)
    else:
        numGroups = (fourGroups,0)
    return numGroups
        
def sort(bounces,person,NN,groups):
    i = 0
    sortName = []
    groupNumbers = []
    gn = 0

    ## get a list that gives the #kids in each group
    for f in range(groups[0]):
        groupNumbers.append(4)
    for three in range(groups[1]):
        groupNumbers.append(3)

    ## put kids into each group
    for j in range(groups[0] + groups[1]):
        h = 70
        w.create_text(j*120+60,20,text="Group "+str(j+1), fill="red",font=fontz)
        for k in range(groupNumbers[gn]):
            if i < NN:
                #get the initial position of each name
                sortName.append(w.create_text(rX[i],rY[i],text=person[i], font=fontz))
                w.delete(i)
                w.delete(i+bounces*NN)
                movename(sortName[i],(j*120+60),h,rX[i],rY[i])
                h = h + 50
                i = i + 1
        gn = gn + 1
        w.delete(i+bounces*NN)
        root.update_idletasks()
        root.update()

## this method moves the names to the group column
def movename(sortName,newX,newY,X,Y):
    stepSizex=(newX-X)/2000
    stepSizey=(newY-Y)/2000
    for step in range(1,2000):
        X = stepSizex + X
        Y = stepSizey + Y
        w.pack()
        w.coords(sortName,X,Y)
        root.update_idletasks()
        root.update()

## draw the names and move them around
def drawname(person,NN):
    newrX = []
    newrY = []
    stepSizex = []
    stepSizey =[]
    studentName = []
    global rX
    global rY
    global w

    for i in range(0,NN):
        newrX.append(1000*random()+20)
        newrY.append(350*random()+ 250) ## 250 leaves a gap at the top
        studentName.append(w.create_text(rX[i],rY[i],text=person[i],font=fontz))
        stepSizex.append((newrX[i]-rX[i])/400)
        stepSizey.append((newrY[i]-rY[i])/400)
    
    for step in range(1,400):
        skip = 0
        for i in range(0,NN):
            skip = skip + 1
            if (skip%2) == 0:
                jitter = 1/1000
            else:
                jitter = -1/1000
            rX[i] = stepSizex[i] + rX[i] 
            rY[i] = stepSizey[i] + rY[i] 
            w.pack()
            w.coords(studentName[i],rX[i],rY[i])
            root.update_idletasks()
            root.update()

############################################################

root = Tkinter.Tk()
root.title("The Sorting Name")

## draw tkinter window
center_window(1000,650)
w = Tkinter.Canvas(root, width=1000, height=600, background="#ffffff")
w.pack()

## open the text file that has the class names in it
## make an array with a list of the names
## open a .txt file with a list of first names
name_of_file = askopenfilename(filetypes = ( ('text files', '.txt'),('All files', '*.*')))
nameFile = open(name_of_file)
peopleList = []
stop = 0
rX = []
rY = []

#initialize how many times the names bounce around
#bounces is used to track the id of the last name that needs to be deleted in the sort
bounces = -1

#get names from text file and return the number of names
#strip the return characters from the list of names
numberNames = fillnames(nameFile) ## get the number of people
people = striplist(peopleList)  ## strip return characters. Method used to fill a list
newNames = []

##Tkinter.Button(root, text="QUIT", command=quit).pack()
q = Tkinter.Button(text="QUIT")
q.bind("<Button-1>", quitter)
q.pack()

#put buttons on the window
fontz = tkFont.Font(family="Helvetica", size=16)
b = Tkinter.Button(text="SORT")
b.bind("<Button-1>", callback)
b.pack()

#get the intial starting position. Random x,y coordinates
for initial in range(0,numberNames):
    rX.append(1000*random()+20)
    rY.append(300*random()+250)
#keep bouncing names around until the sort button is pressed
for times in range(0,10):
    while stop == 0:
        w.delete("all")
        drawname(people,numberNames)  ## draw the names
        bounces = bounces + 1

shuffle(people)  ##shuffle the list
groups = grouping()  ## get the groups required
sort(bounces,people,numberNames,groups) ## put the people into the groups

def main():
    root.mainloop()

main()    
