'''
@Description: main program
@Version: 3.7.0.20191118
@Author: Alexandra Garton, Connor Worthington, Jichen Zhao (driver), Niran Prajapati, and William Staff (observer)
@Date: 2019-10-22 15:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-20 15:53:14
'''

import sys
import webbrowser
import threading
from bottle import route, run, request, redirect
from spotipy import oauth2
from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox
from PySide2.QtGui import QIcon
from PySide2 import QtCore

from UI import appMainWindow
from logTool import Log
from webServer import WebServer
from pullNews import get_headlines
from keywordExtractor import KeywordExtractor
from playlistCreator import createPlaylist


class MainWindow(QMainWindow, appMainWindow.Ui_MainWindow):
    def __init__(self):
        @route('/')
        def index():
            sp_oauth = oauth2.SpotifyOAuth(
                '752b90b62e53446da154d6ed293cc305', # Spotify client ID
                '4317f7ef57154ebaaf89440ab315dde4', # Spotify client secret
                'http://localhost:' + str(self.port), # redirect URL
                scope = 'playlist-modify-public',
                cache_path = '.cache-spotify')
            token_info = sp_oauth.get_cached_token()

            if token_info:
                self.access_token = token_info['access_token']
            else:
                url = request.url
                code = sp_oauth.parse_response_code(url)
                if code:
                    token_info = sp_oauth.get_access_token(code)
                    self.access_token = token_info['access_token']

            if self.access_token:
                redirect('https://www.spotify.com/')
            else:
                redirect(sp_oauth.get_authorize_url())
            

        def ThreadTask(self):
            run(server = self.webServer)
        
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.port = 5000
        self.webServer = WebServer(host="localhost", port=self.port)
        self.access_token = ''
        self.newsSourceList = [
            {'Id': '(blank)', 'Name': '(Select a news source.)'},
            {'Id': 'bbc-news', 'Name': 'BBC News'},
            {'Id': 'the-wall-street-journal', 'Name': 'The Wall Street Journal'},
            {'Id': 'google-news', 'Name': 'Google News'}]
        self.listCache = []

        for count in range(len(self.newsSourceList)): # range: [0, len(self.newsSourceList))
            self.listCache.append({'Titles': [], 'URLs': [], 'Keywords': [], 'PlaylistURL': ''})
            self.comboBoxNewsSource.addItem("")
            self.comboBoxNewsSource.setItemText(count, QApplication.translate('MainWindow', self.newsSourceList[count]['Name'], None, -1))

        self.setWindowTitle(QApplication.translate('MainWindow', appName, None, -1))
        self.setWindowIcon(QIcon('favicon.ico'))
        self.buttonReloadNews.setEnabled(False)
        self.buttonOpenPlaylist.setEnabled(False)
        self.buttonAbout.setText(QApplication.translate('MainWindow', 'About ' + appName, None, -1))
        self.tableWidgetNews.setColumnCount(1)
        self.tableWidgetNews.verticalHeader().setVisible(False)
        self.tableWidgetNews.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetNews.setHorizontalHeaderLabels(['Top headline'])
        self.tableWidgetNews.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidgetNews.setCursor(QtCore.Qt.PointingHandCursor)

        self.comboBoxNewsSource.currentIndexChanged.connect(self.getContent)
        self.buttonReloadNews.clicked.connect(self.ReloadNews)
        self.buttonOpenPlaylist.clicked.connect(self.OpenPlaylist)
        self.buttonAbout.clicked.connect(self.ShowAboutMessage)
        self.tableWidgetNews.cellClicked.connect(self.OpenUrl)

        try:
            self.newThread = threading.Thread(target = ThreadTask, args = (self,))
            self.newThread.start()
        except Exception as e:
            Log('error', repr(e))
            self.show()
            QMessageBox.critical(
                self,
                appName,
                'Failed to load the Spotify authentication. Please contact the authors.',
                QMessageBox.Ok)
            sys.exit()
        else:
            self.show()

            if not self.access_token:
                buttonPushed = QMessageBox.question(
                    self,
                    appName,
                    'For full functionality, this app needs being authorised.\n'
                        + 'Do you want to log in to Spotify to do this now?',
                    QMessageBox.Ok | QMessageBox.Cancel)

                if buttonPushed == QMessageBox.Ok:
                    webbrowser.open('http://localhost:' + str(self.port))


    def CacheList(self, newsSourceIndex: int) -> bool:
        def ManagePlaylistBehaviour(self, newsSourceIndex: int):
            self.listCache[newsSourceIndex]['PlaylistURL'] = ''
            self.buttonOpenPlaylist.setEnabled(False)
            buttonPushed = QMessageBox.warning(
                self,
                appName,
                'Please log in to Spotify to authorise this app for full functionality.\n'
                    + 'After authorising successfully, please remember to reload top headlines.',
                QMessageBox.Ok | QMessageBox.Cancel)
            
            if buttonPushed == QMessageBox.Ok:
                webbrowser.open('http://localhost:' + str(self.port))
        
        
        titleList, urlList = get_headlines(self.newsSourceList[newsSourceIndex]['Id'])

        if titleList != self.listCache[newsSourceIndex]['Titles']:
            self.listCache[newsSourceIndex]['Titles'] = titleList
            self.listCache[newsSourceIndex]['URLs'] = urlList
            
            if self.access_token:
                extractor = KeywordExtractor()
                self.listCache[newsSourceIndex]['Keywords'] = extractor.ExtractKeywords(urlList)
                self.listCache[newsSourceIndex]['PlaylistURL'] = createPlaylist(
                    self.access_token,
                    self.newsSourceList[newsSourceIndex]['Name'],
                    self.listCache[newsSourceIndex]['Keywords'])
            else:
                ManagePlaylistBehaviour(self, newsSourceIndex)

            return True
        else:
            if self.listCache[newsSourceIndex]['PlaylistURL'] == '':
                if self.access_token:
                    if len(self.listCache[newsSourceIndex]['Keywords']) == 0:
                        extractor = KeywordExtractor()
                        self.listCache[newsSourceIndex]['Keywords'] = extractor.ExtractKeywords(urlList)

                    self.listCache[newsSourceIndex]['PlaylistURL'] = createPlaylist(
                        self.access_token,
                        self.newsSourceList[newsSourceIndex]['Name'],
                        self.listCache[newsSourceIndex]['Keywords'])
                else:
                    ManagePlaylistBehaviour(self, newsSourceIndex)

            return False

    def ShowContent(self, newsSourceIndex: int):
        self.tableWidgetNews.clearContents()
        self.tableWidgetNews.setRowCount(len(self.listCache[newsSourceIndex]['Titles']))
        
        for count in range(len(self.listCache[newsSourceIndex]['Titles'])): # range: [0, len(self.listCache[newsSourceIndex]['Titles']))
            self.tableWidgetNews.setItem(count, 0, QTableWidgetItem(self.listCache[newsSourceIndex]['Titles'][count]))
        
        if self.listCache[newsSourceIndex]['PlaylistURL'] != '':
            webbrowser.open(self.listCache[newsSourceIndex]['PlaylistURL'])
            self.buttonOpenPlaylist.setEnabled(True)
        else:
            self.buttonOpenPlaylist.setEnabled(False)

    def getContent(self):
        currentNewsSourceIndex = self.comboBoxNewsSource.currentIndex()

        if currentNewsSourceIndex == 0:
            self.tableWidgetNews.clearContents()
            self.tableWidgetNews.setRowCount(0)
            self.buttonReloadNews.setEnabled(False)
            self.buttonOpenPlaylist.setEnabled(False)
        else:
            self.buttonReloadNews.setEnabled(True)
            self.buttonOpenPlaylist.setEnabled(False)
            MainWindow.CacheList(self, currentNewsSourceIndex)
            MainWindow.ShowContent(self, currentNewsSourceIndex)


    def ReloadNews(self):
        currentNewsSourceIndex = self.comboBoxNewsSource.currentIndex()
        titleList, urlList = get_headlines(self.newsSourceList[currentNewsSourceIndex]['Id'])

        if MainWindow.CacheList(self, currentNewsSourceIndex):
            MainWindow.ShowContent(self, currentNewsSourceIndex)
        else:
            if self.listCache[currentNewsSourceIndex]['PlaylistURL'] != '':
                webbrowser.open(self.listCache[currentNewsSourceIndex]['PlaylistURL'])
                self.buttonOpenPlaylist.setEnabled(True)
                QMessageBox.information(
                    self,
                    appName,
                    'Already the latest top headlines from '
                        + self.newsSourceList[currentNewsSourceIndex]['Name']
                        + '. Please reload top headlines later.')


    def OpenPlaylist(self):
        webbrowser.open(self.listCache[self.comboBoxNewsSource.currentIndex()]['PlaylistURL'])


    def ShowAboutMessage(self):
        QMessageBox.about(
            self,
            'About ' + appName,
            'Version: ' + version + '\n\n'
                + 'Authors: Alexandra Garton, Connor Worthington, Jichen Zhao, Niran Prajapati, and William Staff\n\n'
                + '© 2019 Group 2\n'
                + 'Powered by News API and Spotify')


    def OpenUrl(self):
        webbrowser.open(self.listCache[self.comboBoxNewsSource.currentIndex()]['URLs'][self.tableWidgetNews.currentRow()])
    

    def closeEvent(self, event):
        self.webServer.shutdown()
        self.newThread.join()


appName = 'Spotify News - Group 2'
version = '3.7.0'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())