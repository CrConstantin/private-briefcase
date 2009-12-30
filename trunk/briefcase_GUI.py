# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    Website : http://code.google.com/p/private-briefcase \n\
    This module contains Briefcase class with all its functions. \n\
    Tested on Windows XP, with Python 2.6. \n\
    External dependencies : pyQt4. \n\
'''

# Standard libraries.
import os, sys

# External dependency.
from briefcase import Briefcase
from PyQt4 import QtCore, QtGui

__version__ = '1.0'


WStyle = '''
QTabWidget::pane {
    border-style: outset;
    border: 1px solid #666;
    border-radius: 10px;
}
QTabWidget::tab-bar {
    left: 7px;
}
QPushButton {
    border-style: outset;
    border: 1px solid #666;
    border-radius: 3px;
    color: #000;
    font: 10px;
}
QPushButton:pressed {
    border-style: inset;
}
'''

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global WStyle
        #
        self.blist = []
        self.ilist = []
        #
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        #
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(WStyle)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        # Status bar.
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # Tool bar.
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(36, 36))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        # Tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 500))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.scrollArea_1 = QtGui.QScrollArea(self.tab_1)
        self.scrollArea_1.setGeometry(QtCore.QRect(5, 5, 769, 472))
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollAreaContents_1 = QtGui.QWidget(self.scrollArea_1)
        self.scrollAreaContents_1.setGeometry(QtCore.QRect(0, 0, 768, 470))
        self.scrollAreaContents_1.setMinimumSize(QtCore.QSize(10, 470))
        self.scrollAreaContents_1.setObjectName("scrollAreaContents_1")
        self.scrollArea_1.setWidget(self.scrollAreaContents_1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.scrollArea_2 = QtGui.QScrollArea(self.tab_2)
        self.scrollArea_2.setGeometry(QtCore.QRect(5, 5, 769, 472))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaContents_2 = QtGui.QWidget(self.scrollArea_2)
        self.scrollAreaContents_2.setGeometry(QtCore.QRect(0, 0, 768, 470))
        self.scrollAreaContents_2.setMinimumSize(QtCore.QSize(10, 470))
        self.scrollAreaContents_2.setObjectName("scrollAreaContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaContents_2)
        self.tabWidget.addTab(self.tab_2, "")
        # Setup actions.
        self.actionNew = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-New.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionJoin = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Join.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJoin.setIcon(icon2)
        self.actionJoin.setObjectName("actionJoin")
        self.actionAdd_file = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_file.setIcon(icon3)
        self.actionAdd_file.setObjectName("actionAdd_file")
        self.actionAdd_many = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add-Many.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_many.setIcon(icon4)
        self.actionAdd_many.setObjectName("actionAdd_many")
        self.actionRefresh = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon5)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionHelp = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon6)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon7)
        self.actionAbout.setObjectName("actionAbout")
        self.actionView = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-View.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionView.setIcon(icon8)
        self.actionView.setObjectName("actionView")
        self.actionEdit = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon9)
        self.actionEdit.setObjectName("actionEdit")
        self.actionCopy = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon10)
        self.actionCopy.setObjectName("actionCopy")
        self.actionDelete = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon11)
        self.actionDelete.setObjectName("actionDelete")
        self.actionRename = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRename.setIcon(icon12)
        self.actionRename.setObjectName("actionRename")
        self.actionProperties = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Properties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(icon13)
        self.actionProperties.setObjectName("actionProperties")
        # Add actions on toolbar.
        self.toolBar.addAction(self.actionNew)
        QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL("triggered()"), self.on_new)
        self.toolBar.addAction(self.actionOpen)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.on_open)
        self.toolBar.addAction(self.actionJoin)
        QtCore.QObject.connect(self.actionJoin, QtCore.SIGNAL("triggered()"), self.on_join)
        self.toolBar.addAction(self.actionAdd_file)
        QtCore.QObject.connect(self.actionAdd_file, QtCore.SIGNAL("triggered()"), self.on_add)
        self.toolBar.addAction(self.actionAdd_many)
        QtCore.QObject.connect(self.actionAdd_many, QtCore.SIGNAL("triggered()"), self.on_add)
        self.toolBar.addAction(self.actionRefresh)
        QtCore.QObject.connect(self.actionRefresh, QtCore.SIGNAL("triggered()"), self.on_refresh)
        self.toolBar.addAction(self.actionHelp)
        QtCore.QObject.connect(self.actionHelp, QtCore.SIGNAL("triggered()"), self.on_help)
        self.toolBar.addAction(self.actionAbout)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.on_about)
        # Setup + add actions on menu.
        self.buttonMenu = QtGui.QMenu()
        self.buttonMenu.addAction(self.actionView)
        QtCore.QObject.connect(self.actionView, QtCore.SIGNAL("triggered()"), self.on_view)
        self.buttonMenu.addAction(self.actionEdit)
        QtCore.QObject.connect(self.actionEdit, QtCore.SIGNAL("triggered()"), self.on_edit)
        self.buttonMenu.addAction(self.actionCopy)
        QtCore.QObject.connect(self.actionCopy, QtCore.SIGNAL("triggered()"), self.on_copy)
        self.buttonMenu.addAction(self.actionDelete)
        QtCore.QObject.connect(self.actionDelete, QtCore.SIGNAL("triggered()"), self.on_delete)
        self.buttonMenu.addAction(self.actionRename)
        QtCore.QObject.connect(self.actionRename, QtCore.SIGNAL("triggered()"), self.on_rename)
        self.buttonMenu.addAction(self.actionProperties)
        QtCore.QObject.connect(self.actionProperties, QtCore.SIGNAL("triggered()"), self.on_properties)
        #
        self.dblClickTimer = QtCore.QTimer()
        self.dblClickTimer.setInterval(500)
        self.dblClickTimer.setSingleShot(True)

        # Call translate and final setup.
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Private Briefcase GUI", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtGui.QApplication.translate("MainWindow", "Raportari Generale",
            None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Raportari speciale",
            None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJoin.setText(QtGui.QApplication.translate("MainWindow", "Join", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_file.setText(QtGui.QApplication.translate("MainWindow", "Add file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_many.setText(QtGui.QApplication.translate("MainWindow", "Add many", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView.setText(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRename.setText(QtGui.QApplication.translate("MainWindow", "Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setText(QtGui.QApplication.translate("MainWindow", "Properties", None, QtGui.QApplication.UnicodeUTF8))


    # Helper functions.
    def calculate_x(self):
        lx = len(self.buttons) % 7
        if not lx:
            return 10
        else:
            return 10 + (10+95)*lx

    def calculate_y(self):
        ly = len(self.buttons) // 7
        if not ly:
            return 10
        else:
            return 10 + (10+60)*ly

    def double_click(self):
        # If after receiving the first click, the timer isn't running, start the timer and return.
        if not self.dblClickTimer.isActive():
            self.dblClickTimer.start()
            return
        # If timer is running and hasn't timed out,  the second click occured within timer interval.
        if self.dblClickTimer.isActive() :
            print( 'Triggered Double-Click on item !' )
            self.dblClickTimer.stop() # Stop timer so next click can start it again.
            return

    def right_click(self):
        self.buttonMenu.exec_(QtGui.QCursor.pos())


    # Triggered functions.
    def on_new(self):
        f = QtGui.QFileDialog(self.centralwidget, 'Save new briefcase file', os.getcwd())
        self.input = f.getSaveFileName()
        self.b = Briefcase(self.input, '0123456789abcQWE')

    def on_open(self):
        f = QtGui.QFileDialog(self.centralwidget, 'Load existing briefcase file', os.getcwd())
        self.input = f.getOpenFileName()
        self.b = Briefcase(self.input, '0123456789abcQWE')

    def on_join(self):
        print( 'Triggered JOIN !' )

    def on_add(self):
        #
        self.scrollAreaContents_1.setMinimumSize(QtCore.QSize(10, self.calculate_y()+70))
        #
        pushButton = QtGui.QPushButton(self.scrollAreaContents_1)
        pushButton.setGeometry( QtCore.QRect(self.calculate_x(), self.calculate_y(), 95, 60) )
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(pushButton, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.right_click)
        QtCore.QObject.connect(pushButton, QtCore.SIGNAL('clicked()'), self.double_click)
        pushButton.setFlat(True)
        pushButton.setObjectName("pushButton")
        pushButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Raportare CEC Local.xls", None, QtGui.QApplication.UnicodeUTF8))
        pushButton.setText(QtGui.QApplication.translate("MainWindow", "Raportare CEC Local.xls", None, QtGui.QApplication.UnicodeUTF8))
        #
        self.buttons.append(pushButton)
        pushButton.show()
        #

    def on_refresh(self):
        print( 'Triggered REFRESH !' )

    def on_help(self):
        print( 'Triggered HELP !' )

    def on_about(self):
        print( 'Triggered ABOUT !' )

    def on_view(self):
        print( 'Triggered VIEW !' )

    def on_edit(self):
        print( 'Triggered EDIT !' )

    def on_copy(self):
        print( 'Triggered COPY !' )

    def on_delete(self):
        print( 'Triggered DELETE !' )

    def on_rename(self):
        print( 'Triggered RENAME !' )

    def on_properties(self):
        print( 'Triggered PROPERTIES !' )


import res_rc

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

window.show()
exit(app.exec_())

#Eof()