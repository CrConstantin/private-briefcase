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
        # B name, B name_b, B name_c, B name _s
        self.tabs = {}
        #
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        #
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(WStyle)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        #
        # Status bar.
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #
        # Tool bar.
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(36, 36))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        #
        # Tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 500))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        #
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
        #
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
        #
        # Setup + add actions on menu.
        self.buttonMenu = QtGui.QMenu()
        self.actionView.triggered.connect(self.on_view)
        self.buttonMenu.addAction(self.actionView)
        self.actionEdit.triggered.connect(self.on_edit)
        self.buttonMenu.addAction(self.actionEdit)
        self.actionCopy.triggered.connect(self.on_copy)
        self.buttonMenu.addAction(self.actionCopy)
        self.actionDelete.triggered.connect(self.on_delete)
        self.buttonMenu.addAction(self.actionDelete)
        self.actionRename.triggered.connect(self.on_rename)
        self.buttonMenu.addAction(self.actionRename)
        self.actionProperties.triggered.connect(self.on_properties)
        self.buttonMenu.addAction(self.actionProperties)
        #
        # Setup double click timer.
        self.dblClickTimer = QtCore.QTimer()
        self.dblClickTimer.setInterval(500)
        self.dblClickTimer.setSingleShot(True)
        #
        # Call translate and final setup.
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Private Briefcase GUI", None, QtGui.QApplication.UnicodeUTF8))
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
        tab_name = self.tabWidget.currentWidget().text
        lx = len(self.tabs[tab_name+'_b']) % 7
        if not lx:
            return 10
        else:
            return 10 + (10+95)*lx

    def calculate_y(self):
        tab_name = self.tabWidget.currentWidget().text
        ly = len(self.tabs[tab_name+'_b']) // 7
        if not ly:
            return 10
        else:
            return 10 + (10+60)*ly

    def double_click(self):
        # If after receiving the first click, the timer isn't running, start the timer and return.
        if not self.dblClickTimer.isActive():
            self.dblClickTimer.start()
            return
        # If timer is running and hasn't timed out, the second click occured within timer interval.
        if self.dblClickTimer.isActive():
            print( 'Triggered Double-Click on item!' )
            self.on_view()
            self.dblClickTimer.stop() # Stop timer so next click can start it again.
            return

    def right_click(self):
        self.buttonMenu.exec_(QtGui.QCursor.pos())

    def _new_tab(self, tab_name):
        #
        # Setup new tab.
        newTab = QtGui.QWidget()
        newTab.setObjectName(tab_name)
        newTab.text = tab_name
        scrollArea = QtGui.QScrollArea(newTab)
        scrollArea.setGeometry(QtCore.QRect(5, 5, 769, 472))
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName(tab_name+'_s')
        scrollAreaContents = QtGui.QWidget(scrollArea)
        scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 768, 470))
        scrollAreaContents.setMinimumSize(QtCore.QSize(10, 470))
        scrollAreaContents.setObjectName(tab_name+'_c')
        scrollArea.setWidget(scrollAreaContents)
        self.tabWidget.addTab(newTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(newTab), QtGui.QApplication.translate("MainWindow",
            tab_name, None, QtGui.QApplication.UnicodeUTF8))
        #
        # Add tab to dictionary.
        self.tabs[tab_name] = newTab
        self.tabs[tab_name+'_b'] = {}
        self.tabs[tab_name+'_s'] = scrollArea
        self.tabs[tab_name+'_c'] = scrollAreaContents
        #setattr(self, tab_name, newTab) #???
        #

    def _new_button(self, tab_name, file_name):
        #
        # Prepair scroll area.
        self.tabs[tab_name+'_s'].setMinimumSize(QtCore.QSize(10, self.calculate_y()+70))
        #
        # Setup button.
        pushButton = QtGui.QPushButton(self.tabs[tab_name+'_c'])
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        pushButton.setGeometry( QtCore.QRect(self.calculate_x(), self.calculate_y(), 95, 60) )
        pushButton.setFlat(True)
        pushButton.setObjectName(file_name)
        QtCore.QObject.connect(pushButton, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.right_click)
        pushButton.clicked.connect(self.double_click)
        pushButton.setStatusTip(QtGui.QApplication.translate("MainWindow", file_name, None, QtGui.QApplication.UnicodeUTF8))
        pushButton.setText(QtGui.QApplication.translate("MainWindow", file_name, None, QtGui.QApplication.UnicodeUTF8))
        #
        # Add button to dictionary.
        self.tabs[tab_name+'_b'][file_name] = pushButton
        pushButton.show()
        #


    # Triggered functions.
    def on_new(self):
        #
        f = QtGui.QFileDialog()
        input = f.getSaveFileName(self.centralwidget, 'Create new briefcase file', os.getcwd(), 'All files (*.*)')
        if not input : return
        tab_name = os.path.split(str(input).title())[1]
        self.b = Briefcase(input, '0123456789abcQW')
        self._new_tab(tab_name)
        #

    def on_open(self):
        #
        f = QtGui.QFileDialog()
        input = f.getOpenFileName(self.centralwidget, 'Load existing briefcase file', os.getcwd(), 'All files (*.*)')
        if not input : return
        tab_name = os.path.split(str(input).title())[1]
        self.b = Briefcase(input, '0123456789abcQW')
        self._new_tab(tab_name)
        #
        for file_name in self.b.GetFileList():
            self._new_button(tab_name, file_name)
        #

    def on_join(self):
        print( 'Triggered JOIN !' )

    def on_add(self):
        #
        f = QtGui.QFileDialog()
        input = f.getOpenFileNames(self.centralwidget, 'Add files in briefcase', os.getcwd(), 'All files (*.*)')
        if not input : return
        #
        for elem in input:
            #
            self.b.AddFile(str(elem))
            #
            tab_name = self.tabWidget.currentWidget().text
            file_name = os.path.split(str(elem))[1]
            self._new_button(tab_name, file_name)
            #

    def on_refresh(self):
        print( 'Triggered REFRESH !' )

    def on_help(self):
        print( 'Triggered HELP !' )

    def on_about(self):
        print( 'Triggered ABOUT !' )

    def on_view(self):
        clickedButton = self.centralwidget.sender()
        print( 'Triggered VIEW on %s !' % clickedButton )
        self.b.ExportFile(str(clickedButton.text()), execute=True)

    def on_edit(self):
        clickedButton = self.centralwidget.sender()
        print( 'Triggered EDIT on %s !' % clickedButton )
        #self.b.ExportFile(str(clickedButton.text()), execute=True)

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