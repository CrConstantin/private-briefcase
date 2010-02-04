# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    Website : http://private-briefcase.googlecode.com \n\
    This module contains Briefcase class with all its functions. \n\
    Tested on Windows XP, with Python 2.6. \n\
    External dependencies : pyQt4. \n\
'''

# Standard libraries.
import os, sys

# External dependency.
from briefcase import Briefcase
from PyQt4 import QtCore, QtGui

__version__ = 'r37'


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

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #
        super(MainWindow, self).__init__(parent)
        #
        global WStyle
        # B name, B name _btns, B name _bs, B name _c
        self.tabs = {}
        self.sort = 'name'
        #
        self.resize(800, 600)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        self.setObjectName("MainWindow")
        self.setWindowTitle("Private Briefcase GUI")
        #
        # Set central widget.
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setStyleSheet(WStyle)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        #
        # Set status bar.
        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName("statusbar")
        self.setStatusBar(statusbar)
        #
        # Set tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 500))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setCurrentIndex(0)
        #
        # Setup actions.
        self.actionNew = QtGui.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-New.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setText("New")
        self.actionOpen = QtGui.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setText("Open")
        self.actionJoin = QtGui.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Join.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJoin.setIcon(icon2)
        self.actionJoin.setObjectName("actionJoin")
        self.actionJoin.setText("Join")
        self.actionAdd_files = QtGui.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_files.setIcon(icon3)
        self.actionAdd_files.setObjectName("actionAdd_files")
        self.actionAdd_files.setText("Add files")
        self.actionProperties = QtGui.QAction(self)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add-Many.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(icon4)
        self.actionProperties.setObjectName("actionProperties")
        self.actionProperties.setText("Properties")
        self.actionRefresh = QtGui.QAction(self)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon5)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.setText("Refresh")
        self.actionHelp = QtGui.QAction(self)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon6)
        self.actionHelp.setObjectName("actionHelp")
        self.actionHelp.setText("Help")
        self.actionAbout = QtGui.QAction(self)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon7)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")
        #
        # Tool bar.
        toolBar = QtGui.QToolBar(self)
        toolBar.setIconSize(QtCore.QSize(36, 36))
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, toolBar)
        #
        # Add actions on toolbar.
        self.actionNew.triggered.connect(self.on_new)
        toolBar.addAction(self.actionNew)
        self.actionOpen.triggered.connect(self.on_open)
        toolBar.addAction(self.actionOpen)
        self.actionJoin.triggered.connect(self.on_join)
        toolBar.addAction(self.actionJoin)
        self.actionAdd_files.triggered.connect(self.on_add)
        toolBar.addAction(self.actionAdd_files)
        self.actionProperties.triggered.connect(self.on_db_properties)
        toolBar.addAction(self.actionProperties)
        self.actionRefresh.triggered.connect(self.on_refresh)
        toolBar.addAction(self.actionRefresh)
        self.actionHelp.triggered.connect(self.on_help)
        toolBar.addAction(self.actionHelp)
        self.actionAbout.triggered.connect(self.on_about)
        toolBar.addAction(self.actionAbout)
        #
        # Button actions.
        self.actionView = QtGui.QAction(self)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-View.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionView.setIcon(icon8)
        self.actionView.setObjectName("actionView")
        self.actionView.setText("View")
        self.actionEdit = QtGui.QAction(self)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon9)
        self.actionEdit.setObjectName("actionEdit")
        self.actionEdit.setText("Edit")
        self.actionCopy = QtGui.QAction(self)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon10)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCopy.setText("Copy")
        self.actionDelete = QtGui.QAction(self)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon11)
        self.actionDelete.setObjectName("actionDelete")
        self.actionDelete.setText("Delete")
        self.actionRename = QtGui.QAction(self)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRename.setIcon(icon12)
        self.actionRename.setObjectName("actionRename")
        self.actionRename.setText("Rename")
        self.actionProperties = QtGui.QAction(self)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Properties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(icon13)
        self.actionProperties.setObjectName("actionProperties")
        self.actionProperties.setText("Properties")
        #
        # Setup Menu + add Actions.
        self.qtMenu = QtGui.QMenu()
        self.actionView.triggered.connect(self.on_view)
        self.qtMenu.addAction(self.actionView)
        self.actionEdit.triggered.connect(self.on_edit)
        self.qtMenu.addAction(self.actionEdit)
        self.actionCopy.triggered.connect(self.on_copy)
        self.qtMenu.addAction(self.actionCopy)
        self.actionDelete.triggered.connect(self.on_delete)
        self.qtMenu.addAction(self.actionDelete)
        self.actionRename.triggered.connect(self.on_rename)
        self.qtMenu.addAction(self.actionRename)
        self.actionProperties.triggered.connect(self.on_properties)
        self.qtMenu.addAction(self.actionProperties)
        #
        # Setup double click timer.
        self.dblClickTimer = QtCore.QTimer()
        self.dblClickTimer.setInterval(500)
        self.dblClickTimer.setSingleShot(True)
        #


    # Helper functions.
    def calculate_x(self, offset=-1):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        if offset<0: offset = len(self.tabs[tab_name+'_btns'])
        lx = offset % 7
        if not lx:
            return 10
        else:
            return 10 + (10+95)*lx
        #

    def calculate_y(self, offset=-1):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        if offset<0: offset = len(self.tabs[tab_name+'_btns'])
        ly = offset // 7
        if not ly:
            return 10
        else:
            return 10 + (10+60)*ly
        #

    def sort_btns(self):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        #
        index = 0
        for qtBtn in sorted( self.tabs[tab_name+'_btns'], key=lambda k: k.lower() ):
            self.tabs[tab_name+'_btns'][qtBtn].move(self.calculate_x(index), self.calculate_y(index))
            index += 1
        self.tabs[tab_name+'_c'].setMinimumSize(QtCore.QSize(755, self.calculate_y(index-1)+70))
        self.tabs[tab_name+'_c'].setMaximumSize(QtCore.QSize(755, self.calculate_y(index-1)+70))
        del index
        #

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
        #

    def right_click(self):
        #
        p = self.cursor().pos()
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        self.tabs[tab_name+'_bs'] = self.childAt(self.mapFromGlobal(p)).objectName() # Selected button.
        self.qtMenu.exec_(self.cursor().pos()) # Execute menu.
        #

    def _new_tab(self, tab_name):
        #
        # New tab widget.
        newTab = QtGui.QScrollArea()
        newTab.setObjectName(tab_name)
        # Contents widget.
        scrollAreaContents = QtGui.QWidget(newTab)
        scrollAreaContents.setObjectName(tab_name+'_c')
        # Add contents to scrollarea.
        newTab.setWidget(scrollAreaContents)
        # Add tab to tabwidget.
        self.tabWidget.addTab(newTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(newTab), tab_name)
        # Add tab to dictionary.
        self.tabs[tab_name] = newTab                  # Tab widget.
        self.tabs[tab_name+'_btns'] = {}              # Buttons from this tab.
        self.tabs[tab_name+'_bs'] = []                # Selected buttons.
        self.tabs[tab_name+'_c'] = scrollAreaContents # Contents.
        #

    def _new_button(self, tab_name, file_name):
        #
        # Setup button.
        pushButton = QtGui.QPushButton(self.tabs[tab_name+'_c'])
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        pushButton.setGeometry(self.calculate_x(), self.calculate_y(), 95, 60)
        pushButton.setFlat(True)
        pushButton.setObjectName(file_name)
        pushButton.setStatusTip(file_name)
        pushButton.setText(file_name)
        # Connect events.
        pushButton.clicked.connect(self.double_click)
        pushButton.customContextMenuRequested.connect(self.right_click)
        # Add button to dictionary.
        self.tabs[tab_name+'_btns'][file_name] = pushButton
        pushButton.show()
        #


    # Triggered functions.
    def on_new(self):
        #
        f = QtGui.QFileDialog()
        input = f.getSaveFileName(self.centralwidget, 'Create new briefcase file', os.getcwd(), 'All files (*.*)')
        if not input : return
        tab_name = os.path.split(str(input).title())[1]
        self.tabs[tab_name+'_pb'] = Briefcase(input, '0123456789abcQW') # Briefcase for current tab.
        self._new_tab(tab_name)
        self.tabWidget.setCurrentWidget(self.tabs[tab_name]) # Must enable new tab.
        #

    def on_open(self):
        #
        f = QtGui.QFileDialog()
        input = f.getOpenFileName(self.centralwidget, 'Load existing briefcase file', os.getcwd(), 'All files (*.*)')
        if not input : return
        tab_name = os.path.split(str(input).title())[1]
        self.tabs[tab_name+'_pb'] = Briefcase(input, '0123456789abcQW') # Briefcase for current tab.
        self._new_tab(tab_name)
        self.tabWidget.setCurrentWidget(self.tabs[tab_name]) # Must enable new tab.
        #
        for file_name in self.tabs[tab_name+'_pb'].GetFileList():
            self._new_button(tab_name, file_name)
        #
        self.sort_btns()
        #

    def on_join(self):
        print( 'Triggered JOIN !' )

    def on_add(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, "Error on Add",
                "<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>")
            return
        #
        f = QtGui.QFileDialog()
        input = f.getOpenFileNames(self.centralwidget, 'Add files in briefcase', os.getcwd(), 'All files (*.*)')
        if not input : return
        #
        for elem in input:
            #
            self.tabs[tab_name+'_pb'].AddFile(str(elem))
            #
            tab_name = str(self.tabWidget.currentWidget().objectName())
            file_name = os.path.split(str(elem))[1]
            self._new_button(tab_name, file_name)
            #
        #
        self.sort_btns()
        #

    def on_refresh(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, "Error on Refresh",
                "<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>")
            return
        print( 'Triggered REFRESH !' )
        self.sort_btns()
        #

    def on_db_properties(self):
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, "Error on Properties",
                "<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>")
            return
        info = '<br>'.join(self.tabs[tab_name+'_pb'].GetFileList())
        QtGui.QMessageBox.information(self.centralwidget, "Properties for %s" % tab_name, info)
        del info, tab_name

    def on_help(self):
        QtGui.QMessageBox.information(self.centralwidget, "Private Briefcase Help",
            "<br>Please check <b>Online Help</b> : http://code.google.com/p/private-briefcase/w/<br>")

    def on_about(self):
        QtGui.QMessageBox.about(self.centralwidget, "About Private Briefcase",
            "<br><b>Copyright © 2009-2010</b> : Cristi Constantin. All rights reserved.<br>"
            "<b>Website</b> : http://private-briefcase.googlecode.com<br>")

    def on_view(self):
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        # If caller is an action.
        if type(self.sender()) == type(QtGui.QPushButton()):
            self.tabs[tab_name+'_pb'].ExportFile(str(self.sender().text()), execute=True)
        # If caller is a button.
        else:
            qtBS = str(self.tabs[tab_name+'_bs'])
            self.tabs[tab_name+'_pb'].ExportFile(qtBS, execute=True)
            del qtBS
        del tab_name

    def on_edit(self):
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        self.tabs[tab_name+'_pb'].ExportFile(qtBS, execute=True)
        del tab_name, qtBS

    def on_copy(self):
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        qtMsg = QtGui.QMessageBox.question(self.centralwidget, 'Copy file ? ...',
            'Are you sure you want to copy "%s" ?' % qtBS, 'Yes', 'No')
        if qtMsg==0: # Clicked yes.
            ret = self.tabs[tab_name+'_pb'].CopyIntoNew(fname=qtBS, version=0, new_fname='copy of '+qtBS)
            if ret==0: # If Briefcase returns 0, create new button.
                self._new_button(tab_name, 'copy of '+qtBS)
                self.sort_btns()
        del tab_name, qtBS, qtMsg

    def on_delete(self):
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        qtMsg = QtGui.QMessageBox.warning(self.centralwidget, 'Delete file ? ...',
            'Are you sure you want to delete "%s" ?' % qtBS, 'Yes', 'No')
        if qtMsg==0: # Clicked yes.
            ret = self.tabs[tab_name+'_pb'].DelFile(fname=qtBS, version=0)
            if ret==0: # If Briefcase returns 0, delete the button.
                self.tabs[tab_name+'_btns'][qtBS].close()
                del self.tabs[tab_name+'_btns'][qtBS]
                self.sort_btns()
        del tab_name, qtBS, qtMsg

    def on_rename(self):
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        qtTxt, qtMsg = QtGui.QInputDialog.getText(self.centralwidget, 'Rename file ? ...',
            "New name :", QtGui.QLineEdit.Normal, qtBS)
        if qtMsg and str(qtTxt): # Clicked yes and text exists.
            ret = self.tabs[tab_name+'_pb'].RenFile(fname=qtBS, new_fname=str(qtTxt))
            if ret==0: # If Briefcase returns 0, rename the button.
                self.tabs[tab_name+'_btns'][qtBS].setObjectName(qtTxt)
                self.tabs[tab_name+'_btns'][qtBS].setStatusTip(qtTxt)
                self.tabs[tab_name+'_btns'][qtBS].setText(qtTxt)
                self.tabs[tab_name+'_btns'][str(qtTxt)] = self.tabs[tab_name+'_btns'][qtBS]
                del self.tabs[tab_name+'_btns'][qtBS]
                self.sort_btns()
        del tab_name, qtBS, qtTxt, qtMsg

    def on_properties(self):
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        prop = self.tabs[tab_name+'_pb'].GetProperties(fname=qtBS)
        if not prop['labels']:
            prop['labels'] = '-'
        QtGui.QMessageBox.information(self.centralwidget, "Properties for %s" % qtBS, '''
            <br><b>fileName</b> : %(fileName)s
            <br><b>internFileName</b> : %(internFileName)s
            <br><b>firstFileSize</b> : %(firstFileSize)i
            <br><b>lastFileSize</b> : %(lastFileSize)i
            <br><b>firstFileDate</b> : %(firstFileDate)s
            <br><b>lastFileDate</b> : %(lastFileDate)s
            <br><b>firstFileUser</b> : %(firstFileUser)s
            <br><b>lastFileUser</b> : %(lastFileUser)s
            <br><b>labels</b> : %(labels)s
            <br><b>versions</b> : %(versions)i''' % prop)
        del tab_name, qtBS, prop


import res_rc

app = QtGui.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Eof()