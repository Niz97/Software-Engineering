'''
@Description: main program
@Version: 1.5.0.20191109
@Author: Alexandra Garton, Connor Worthington, Jichen Zhao, Niran Prajapati, and William Staff
@Date: 2019-10-22 15:22:59
@Last Editors: William Staff
@LastEditTime: 2019-11-08 14:40:09
'''

from tkinter import *

from pullNews import get_headlines
from keywordExtractor import ExtractKeywords
from playlistCreator import createPlaylist


def callFuncs():
    urlList = get_headlines('gb')
    keywordList = ExtractKeywords(urlList)
    createPlaylist(keywordList)

class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        reqButton = Button(self, text="Request Playlist", command=callFuncs)

        # placing the button on my window
        reqButton.place(x=0, y=0)

root = Tk()

#size of the window
root.geometry("400x300")

app = Window(root)
root.mainloop()