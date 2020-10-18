from tkinter import Frame as UIFrame
from tkinter import Label as UILabel
from tkinter import Button as UIButton

from View import View

import windowmanager as winman

titleAppendix = None  # Default value if nothing gets changed

# Defining functions to add more info
def file(filename):
    global titleAppendix
    moreInfoLabel.config(text=f"The config {filename} isn't filled properly!")
    titleAppendix = "Configuration"


# Creating and adding the frame; Creating the view
errorViewFrame = UIFrame(winman.mainWin)
errorViewFrame.grid()
errorView = View(title="will never be seen, managed by windowmanager")


# Defining functions for buttons
def quitProgram():
    winman.close()\


# Drawing the interface, row by row
headingLabel = UILabel(errorViewFrame, text="Critical error", font=("bold", 30), underline=0)
errorView.addLine([headingLabel])

moreInfoLabel = UILabel(errorViewFrame, text="An unknown error has occured.")
errorView.addLine([moreInfoLabel])

quitFrame = UIFrame(errorViewFrame)
willQuitLabel = UILabel(quitFrame, text="The program will terminate.")
quitButton = UIButton(quitFrame, text="Quit", command=quitProgram)
errorView.addLine([quitFrame])

# PACKing frame components
willQuitLabel.pack(side="left")
quitButton.pack(side="right")


# Finishing up: Registering errorView
winman.registerView(errorView, "error")
