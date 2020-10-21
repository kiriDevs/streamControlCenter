from tkinter import Frame as UIFrame
from tkinter import Label as UILabel
from tkinter import Button as UIButton
from tkinter import Entry as UITextField

from View import View
import windowmanager as winman
from apiHandler import getSelf, setTitle, searchChannel
from inputHandler import changeEntryText

from Exceptions import TitleTooLongException
from Exceptions import ConnectionFailedError

# Creating a function for what to do before the view is shown
def on_load():
    try:
        me = getSelf()  # Get ID and name of the currently authorized user
    except ConnectionFailedError:
        youValueName.config(text="Error contacting the TwitchAPI!")
        youValueId.config(text="(Sorry about that)")
        return

    youValueName.config(text=me["username"])  # Displaying displayname
    idFormat = "(" + me["userid"] + ")"
    youValueId.config(text=idFormat)  # Displaying broadcaster ID

    # Gather current title to display in the box at start
    myProfile = searchChannel(me["username"])  # Empty result shouldn't be possible
    myTitle = myProfile["title"]

    changeEntryText(titleField, myTitle)


# Creating and packing frame; Creating view
titleChangeFrame = UIFrame(winman.mainWin)
titleChangeFrame.grid()
titleChangeView = View("Change Stream Title", on_load)


# Defining functions for buttons
def backButton():
    winman.switchView("mainmenu")


def clearConfirmationLabel():
    confirmationLabel.config(text="")


def confirmButton():
    titleInput = titleField.get()

    try:
        setTitle(titleInput)
    except TitleTooLongException:
        confirmationLabel.config(text="Title is too long!")
        confirmationLabel.after(3000, clearConfirmationLabel)
        return
    except ConnectionFailedError:
        confirmationLabel.config(text="A connection error occured!")
        confirmationLabel.after(3000, clearConfirmationLabel)
        return

    confirmationLabel.config(text="Title set!")
    confirmationLabel.after(3000, clearConfirmationLabel)


# Drawing the interface, row by row
youLabel = UILabel(titleChangeFrame, text="You are logged in as:")
# # # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = # # #
youValueFrame = UIFrame(titleChangeFrame)
youValueName = UILabel(youValueFrame, text="...")
youValueId = UILabel(youValueFrame, text="...")
# # # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = # # #
titleChangeView.addLine([youLabel, youValueFrame])

instructionFrame = UIFrame(titleChangeFrame)
instructionLabel = UILabel(instructionFrame, text="Enter your stream title here:")
moreInfoLabel = UILabel(instructionFrame, text="(Twitch Guidelines and restrictions apply)")
# # # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = # # #
titleField = UITextField(titleChangeFrame, width=75)
confirmButton = UIButton(titleChangeFrame, text="Confirm", command=confirmButton)
# # # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = # # #
titleChangeView.addLine([instructionFrame, titleField, confirmButton])

backButton = UIButton(titleChangeFrame, text="<--", command=backButton)
lowerRowSpacer = UILabel(titleChangeFrame)
confirmationLabel = UILabel(titleChangeFrame, width=20)
# # # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = # # #
titleChangeView.addLine([backButton, lowerRowSpacer, confirmationLabel])

# PACKing frame components
youValueName.pack(side="top")
youValueId.pack(side="top")

instructionLabel.pack(side="top")
moreInfoLabel.pack(side="top")

# Finishing up: Registering view
winman.registerView(titleChangeView, "titlechanger")
