import re
import locale

from tkinter import Tk as newWindow
from tkinter import Label as UILabel
from tkinter import Button as UIButton
from tkinter import Entry as UITextField

import apiHandler

# ====================================
# === Initializing constant values ===
# ====================================
# Variables
xpadding = 20
ypadding = 20

# Library inits
locale.setlocale(locale.LC_ALL, "")


# Functions
def changeEntryValue(forEntryField, toValue):
    contentLength = len(forEntryField.get())
    forEntryField.delete(0, contentLength)
    forEntryField.insert(0, toValue)


def drawMatrix(matrix):
    for row in matrix:
        for element in row:
            element.grid(row=matrix.index(row), column=row.index(element), padx=xpadding, pady=ypadding)


def searchChannel():
    query = channel_input.get()
    print(query)

    if not re.match("[a-zA-Z0-9_]", query):
        changeEntryValue(channel_input, "### Error: Invalid search term!")
        return

    if not len(query) in range(4, 26):  # Usernames can range from 4 to 25 chars, range(x, y) doesn't include y
        changeEntryValue(channel_input, "### Error: Invalid search term!")
        return

    if query[0] == "_":
        changeEntryValue(channel_input, "### Error: Invalid search term!")
        return

    result = apiHandler.searchChannel(query)

    if result is not None:
        if result['is_live']:
            liveStatusString = f"{result['display_name']} is live right now!"
        else:
            liveStatusString = f"{result['display_name']} is not live right now!"
        isLiveValue.config(text=liveStatusString)

        titleValue.config(text=result['title'])

        followerNumber = result['follower_number']
        formatedNumber = f"{followerNumber:n}"
        followerValue.config(text=formatedNumber)
    else:
        changeEntryValue(channel_input, "### Error: No channel found!")


# ==========================
# === Building Main Menu ===
# ==========================
mainMenuMatrix = []  # Creating empty matrix

# Initializing the window with geometry and title
mainMenu = newWindow()
# mainMenu.geometry("400x150")
mainMenu.title("streamControlCenter - Main Menu")

# Creating menu components - line by line
instruction_label = UILabel(mainMenu, text="Enter a channel name to check their status!")
channel_input = UITextField(mainMenu, width=35)
confirm_button = UIButton(mainMenu, text="Check!", command=searchChannel)
mainMenuMatrix.append([instruction_label, channel_input, confirm_button])

isLiveLabel = UILabel(mainMenu, text="Live status:")
isLiveValue = UILabel(mainMenu, text="?")
mainMenuMatrix.append([isLiveLabel, isLiveValue])

titleLabel = UILabel(mainMenu, text="Stream title:")
titleValue = UILabel(mainMenu, text="?")
mainMenuMatrix.append([titleLabel, titleValue])

followerLabel = UILabel(mainMenu, text="Follower number:")
followerValue = UILabel(mainMenu, text="?")
mainMenuMatrix.append([followerLabel, followerValue])

quitLabel = UILabel(mainMenu, text="Click here to close the application!")
quitButton = UIButton(mainMenu, text="Quit!", command=mainMenu.quit)
mainMenuMatrix.append([quitLabel, quitButton])


# ====================
# === Finishing up ===
# ====================
drawMatrix(mainMenuMatrix)

# Setting default values for input fileds
changeEntryValue(channel_input, "kirimctwitch")

mainMenu.mainloop()
exit(0)
