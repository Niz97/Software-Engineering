# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appMainWindow.ui',
# licensing of 'appMainWindow.ui' applies.
#
# Created: Mon Nov 18 03:59:11 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(771, 535)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBoxNewsSource = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.comboBoxNewsSource.setFont(font)
        self.comboBoxNewsSource.setCursor(QtCore.Qt.PointingHandCursor)
        self.comboBoxNewsSource.setObjectName("comboBoxNewsSource")
        self.verticalLayout.addWidget(self.comboBoxNewsSource)
        self.tableWidgetNews = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidgetNews.setProperty("cursor", QtCore.Qt.PointingHandCursor)
        self.tableWidgetNews.setObjectName("tableWidgetNews")
        self.tableWidgetNews.setColumnCount(0)
        self.tableWidgetNews.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidgetNews)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonReloadNews = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.buttonReloadNews.setFont(font)
        self.buttonReloadNews.setCursor(QtCore.Qt.PointingHandCursor)
        self.buttonReloadNews.setObjectName("buttonReloadNews")
        self.horizontalLayout.addWidget(self.buttonReloadNews)
        self.buttonOpenPlaylist = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.buttonOpenPlaylist.setFont(font)
        self.buttonOpenPlaylist.setObjectName("buttonOpenPlaylist")
        self.horizontalLayout.addWidget(self.buttonOpenPlaylist)
        self.buttonAbout = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.buttonAbout.setFont(font)
        self.buttonAbout.setCursor(QtCore.Qt.PointingHandCursor)
        self.buttonAbout.setObjectName("buttonAbout")
        self.horizontalLayout.addWidget(self.buttonAbout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "(appName)", None, -1))
        self.comboBoxNewsSource.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Select a news source to show top headlines and a Spotify playlist.", None, -1))
        self.buttonReloadNews.setText(QtWidgets.QApplication.translate("MainWindow", "Reload top headlines", None, -1))
        self.buttonOpenPlaylist.setText(QtWidgets.QApplication.translate("MainWindow", "Open Spotify playlist", None, -1))
        self.buttonAbout.setText(QtWidgets.QApplication.translate("MainWindow", "About (appName)", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

