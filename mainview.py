from tkinter import Frame as UIFrame
from tkinter import Button as UIButton
from View import View

import windowmanager as winman

# Creating and adding the frame; Creating the view
mainMenuFrame = UIFrame(winman.mainWin)
mainMenuFrame.grid()
mainMenuView = View("Main Menu")


# Defining functions for buttons
def openChannelCheck():
    winman.switchView("channelcheck")


def quitProgram():
    winman.close()


# Drawing the interface, row by row
menuFrame = UIFrame(mainMenuFrame)

channelCheckButton = UIButton(menuFrame, text="Open Channel Check...", command=openChannelCheck)
mainMenuView.addLine([menuFrame])


quitButton = UIButton(mainMenuFrame, text="Quit", command=quitProgram)
mainMenuView.addLine([quitButton])

# GRIDing frame members
channelCheckButton.grid(row=0, column=0)

# Finishing up: Registering channelCheckView
winman.registerView(mainMenuView, "mainmenu")
