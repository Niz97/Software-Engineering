'''
@Description: main program
@Version: 1.1.0.20191029
@Author: Alexandra Garton, Connor Worthington, Jichen Zhao, Niran Prajapati, and William Staff
@Date: 2019-10-22 15:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-10-29 15:48:27
'''
from newsapi import NewsApiClient
from monkeylearn import MonkeyLearn
from tkinter import *

from keywordExtractor import ExtractKeywords
from playlistCreator import createPlaylist


newsApi = NewsApiClient(api_key = '3bd762aea6134796b564d8e18df60cf8') # handle authentication with a News API key (registered using zjcarvin@outlook.com)
mlApi = MonkeyLearn('e4aabc61a7a365fdf7bda3ab14c7be6c5007d930') # handle authentication with a MonkeyLearn API key (registered using tomzjc@qq.com)

def callFuncs():
	keywordList = ExtractKeywords(newsApi, mlApi, 'gb')
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

#print(keywordList)

#keywordTest = ['mi cc9 pro', 'xiaomi mi cc9', 'isocell bright hmx', 'camera technology', 'camera algorithm', 'handset', 'consumer tech giant', 'community of engineer', 'bright gw1 sensor', 'chinese regulatory agency']

