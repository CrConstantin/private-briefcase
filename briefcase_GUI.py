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

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #
        super(MainWindow, self).__init__(parent)
        #
        global WStyle
        # B name, B name _b, B name _bs, B name _c, B name _s
        self.tabs = {}
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
        self.actionAdd_file = QtGui.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_file.setIcon(icon3)
        self.actionAdd_file.setObjectName("actionAdd_file")
        self.actionAdd_file.setText("Add file")
        self.actionAdd_many = QtGui.QAction(self)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add-Many.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_many.setIcon(icon4)
        self.actionAdd_many.setObjectName("actionAdd_many")
        self.actionAdd_many.setText("Add many")
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
        self.actionAdd_file.triggered.connect(self.on_add)
        toolBar.addAction(self.actionAdd_file)
        self.actionAdd_many.triggered.connect(self.on_add)
        toolBar.addAction(self.actionAdd_many)
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
    def calculate_x(self):
        tab_name = str(self.tabWidget.currentWidget().objectName())
        lx = len(self.tabs[tab_name+'_b']) % 7
        if not lx:
            return 10
        else:
            return 10 + (10+95)*lx

    def calculate_y(self):
        tab_name = str(self.tabWidget.currentWidget().objectName())
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
        #
        p = self.cursor().pos()
        tab_name = str(self.tabWidget.currentWidget().objectName())
        # Save button name.
        self.tabs[tab_name+'_bs'] = self.childAt(self.mapFromGlobal(p)).objectName()
        # Execute menu.
        self.qtMenu.exec_(self.cursor().pos())
        #

    def _new_tab(self, tab_name):
        #
        # Tab widget.
        newTab = QtGui.QWidget(self.tabWidget)
        newTab.setObjectName(tab_name)
        # Scroll area.
        scrollArea = QtGui.QScrollArea(newTab)
        scrollArea.setGeometry(QtCore.QRect(5, 5, 769, 472))
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName(tab_name+'_s')
        # Contents widget.
        scrollAreaContents = QtGui.QWidget(scrollArea)
        scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 768, 470))
        scrollAreaContents.setMinimumSize(QtCore.QSize(10, 470))
        scrollAreaContents.setObjectName(tab_name+'_c')
        scrollArea.setWidget(scrollAreaContents)
        self.tabWidget.addTab(newTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(newTab), tab_name)
        # Add tab to dictionary.
        self.tabs[tab_name] = newTab
        self.tabs[tab_name+'_b'] = {}
        self.tabs[tab_name+'_bs'] = []
        self.tabs[tab_name+'_s'] = scrollArea
        self.tabs[tab_name+'_c'] = scrollAreaContents
        #

    def _new_button(self, tab_name, file_name):
        #
        # Recalculate minimum size for container.
        self.tabs[tab_name+'_c'].setMinimumSize(QtCore.QSize(10, self.calculate_y()+70))
        # Setup button.
        pushButton = QtGui.QPushButton(self.tabs[tab_name+'_c'])
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        pushButton.setGeometry(QtCore.QRect(self.calculate_x(), self.calculate_y(), 95, 60))
        pushButton.setFlat(True)
        pushButton.setObjectName(file_name)
        pushButton.setStatusTip(file_name)
        pushButton.setText(file_name)
        # Connect events.
        pushButton.clicked.connect(self.double_click)
        pushButton.customContextMenuRequested.connect(self.right_click)
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
            tab_name = str(self.tabWidget.currentWidget().objectName())
            file_name = os.path.split(str(elem))[1]
            self._new_button(tab_name, file_name)
            #

    def on_refresh(self):
        print( 'Triggered REFRESH !' )

    def on_help(self):
        QtGui.QMessageBox.information(self.centralwidget, "Private Briefcase Help",
            "<br>Please check <b>Online Help</b> : http://code.google.com/p/private-briefcase/w/<br>")

    def on_about(self):
        QtGui.QMessageBox.about(self.centralwidget, "About Private Briefcase",
            "<br><b>Copyright © 2009-2010</b>, Cristi Constantin. All rights reserved.<br>"
            "<b>Website</b> : http://private-briefcase.googlecode.com<br>")

    def on_view(self):
        tab_name = str(self.tabWidget.currentWidget().objectName())
        # If caller is an action.
        if type(self.sender()) == type(QtGui.QPushButton()):
            self.b.ExportFile(str(self.sender().text()), execute=True)
        # If is a button.
        else:
            qtBS = self.tabs[tab_name+'_bs']
            self.b.ExportFile(str(qtBS), execute=True)
            del qtBS
        del tab_name

    def on_edit(self):
        tab_name = str(self.tabWidget.currentWidget().objectName())
        # This is the selected button.
        qtBS = self.tabs[tab_name+'_bs']
        self.b.ExportFile(str(qtBS), execute=True)
        del qtBS, tab_name

    def on_copy(self):
        qtA = self.sender()
        print( 'Triggered COPY on %s !' % qtA )

    def on_delete(self):
        qtA = self.sender()
        print( 'Triggered DELETE on %s !' % qtA )

    def on_rename(self):
        qtA = self.sender()
        print( 'Triggered RENAME on %s !' % qtA )

    def on_properties(self):
        qtA = self.sender()
        print( 'Triggered PROPERTIES on %s !' % qtA )


import res_rc

app = QtGui.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Eof()