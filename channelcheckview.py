import locale

from tkinter import Frame as UIFrame
from tkinter import Label as UILabel
from tkinter import Entry as UITextField
from tkinter import Button as UIButton

import inputHandler
from Exceptions import ChannelNotFoundException
from Exceptions import IllegalChannelNameException
from Exceptions import ConnectionFailedError
from View import View

import windowmanager as winman

locale.setlocale(locale.LC_ALL, '')


# What to do when view is about to load
def resetValues():
    inputHandler.changeEntryText(enterChannelEntry, "kirimctwitch")
    liveStatusResult.config(text="?")
    titleResult.config(text="?")
    followerResult.config(text="?")


# Creating and adding the frame; Creating the view
channelCheckFrame = UIFrame(winman.mainWin)
channelCheckFrame.grid()
channelCheckView = View("Channel Check", on_load=resetValues)


# Defining functions for buttons
def checkChannel():
    liveStatusResult.config(text="...")
    titleResult.config(text="...")
    followerResult.config(text="...")

    searchQuery = enterChannelEntry.get()

    try:
        channel = inputHandler.searchChannel(searchQuery)
    except ChannelNotFoundException:
        inputHandler.changeEntryText(enterChannelEntry, "### No channel was found!")
        return
    except IllegalChannelNameException:
        inputHandler.changeEntryText(enterChannelEntry, "### Invalid channel name!")
        return
    except ConnectionFailedError:
        inputHandler.changeEntryText(enterChannelEntry, "### Connection to API failed!")
        return

    # Set liveStatusResult
    displayName = channel['display_name']
    if channel['is_live']:
        string = f"{displayName} is live at the moment!"
    else:
        string = f"{displayName} is not live at the moment!"
    liveStatusResult.config(text=string)

    titleResult.config(text=channel['title'])  # Set titleResult

    # Setting followerResult
    rawNumber = channel['follower_number']
    formattedNumber = f"{rawNumber:n}"
    followerResult.config(text=formattedNumber)


def openMainMenu():
    winman.switchView("mainmenu")


# Drawing the interface, row by row
enterChannelLabel = UILabel(channelCheckFrame, text="Please enter a Twitch channel name here:", wraplength=200)
enterChannelEntry = UITextField(channelCheckFrame, width=40)
checkChannelButton = UIButton(channelCheckFrame, text="Check channel detail!", command=checkChannel)
channelCheckView.addLine([enterChannelLabel, enterChannelEntry, checkChannelButton])

liveStatusLabel = UILabel(channelCheckFrame, text="Live status:")
liveStatusResult = UILabel(channelCheckFrame, text="?", wraplength=200)
channelCheckView.addLine([liveStatusLabel, liveStatusResult])

titleLabel = UILabel(channelCheckFrame, text="Stream title:")
titleResult = UILabel(channelCheckFrame, text="?", wraplength=200)
channelCheckView.addLine([titleLabel, titleResult])

followerLabel = UILabel(channelCheckFrame, text="Follower number:")
followerResult = UILabel(channelCheckFrame, text="?")
channelCheckView.addLine([followerLabel, followerResult])

backButton = UIButton(channelCheckFrame, text="<--", command=openMainMenu)
channelCheckView.addLine([backButton])

# Finishing up: Registering channelCheckView
winman.registerView(channelCheckView, "channelcheck")
