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

def restart(event):
    global stop
    print ("test")
    stop = 0
    main()

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
        newrX.append(1000*random()+50)
        newrY.append(350*random()+ 50) ## 50 leaves a gap at the top
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
            
def choose(person):
    w.delete("all")
    w.create_text(500,300,text=person[1], font=fontchoose)
    root.update_idletasks()
    root.update
    
############################################################

root = Tkinter.Tk()
root.title("The Sorting Name")

## draw tkinter window
center_window(1100,650)
w = Tkinter.Canvas(root, width=1100, height=550, background="#ffffff")
w.pack()

## open the text file that has the class names in it
## make an array with a list of the names
name_of_file = askopenfilename(filetypes = ( ('text files', '.txt'),('All files', '*.*')))
nameFile = open(name_of_file)
peopleList = []
stop = 0
rX = []
rY = []

#get names from text file and return the number of names
#strip the return characters from the list of names
numberNames = fillnames(nameFile) ## get the number of people
people = striplist(peopleList)  ## strip return characters
newNames = []


for butName in ("QUIT", "READY", "NAME"):
    if butName == "QUIT":
        call = quitter
    elif butName == "READY":
        call = restart
    else:
        call = callback
    b = Tkinter.Button(text=butName)
    b.bind("<Button-1>", call)
    b.pack()

#put buttons on the window
fontz = tkFont.Font(family="Helvetica", size=18)
fontchoose = tkFont.Font(family="Helvetica", size=36)


#get the intial starting position. Random x,y coordinates
for initial in range(0,numberNames):
    rX.append(1000*random()+50)
    rY.append(300*random()+50)



def main():
    
    #keep bouncing names around until the sort button is pressed
    while stop == 0:
        w.delete("all")
        drawname(people,numberNames)  ## draw the names

    shuffle(people)  ##shuffle the list
    choose(people)
    print (stop)
    root.mainloop()

while True:
    main()    
