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
channelCheckButton = UIButton(mainMenuFrame, text="Open Channel Check...", command=openChannelCheck)
mainMenuView.addLine([channelCheckButton])

quitButton = UIButton(mainMenuFrame, text="Quit", command=quitProgram)
mainMenuView.addLine([quitButton])

# Finishing up: Registering channelCheckView
winman.registerView(mainMenuView, "mainmenu")
