# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    Website : http://private-briefcase.googlecode.com \n\
    This module contains Briefcase class with all its functions. \n\
    Tested on Windows XP and Windows 7, with Python 2.6. \n\
    External dependencies : pyQt4. \n\
'''

# Standard libraries.
import os, sys, PyQt4

# External dependency.
from briefcase import *
from PyQt4 import QtCore, QtGui


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
    color: #001;
    font: 10px;
}
QPushButton:pressed {
    border-style: inset;
}
'''


class CustomDialog(QtGui.QDialog):
    def __init__(self, parent, title, whatsthis, action):
        #
        super(CustomDialog, self).__init__(parent)
        self.transmit = {'dir':'', 'pwd':''}
        self.title = title
        self.action = action
        #
        self.resize(300, 100)
        self.setMinimumSize(QtCore.QSize(300, 100))
        self.setMaximumSize(QtCore.QSize(300, 100))
        self.setWindowTitle(title)
        self.setWhatsThis(whatsthis)
        #
        # Buttons.
        self.browse = QtGui.QPushButton(self)
        self.browse.setMinimumSize(QtCore.QSize(1, 20))
        self.browse.setText('...')
        self.dir = QtGui.QLineEdit(self)
        self.dir.setFocus(0)
        self.dir.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.dir.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd = QtGui.QLineEdit(self)
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.pwd.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.pwd.setMinimumSize(QtCore.QSize(1, 22))
        self.btn = QtGui.QPushButton(self)
        self.btn.setMinimumSize(QtCore.QSize(1, 20))
        self.btn.setText(action)
        self.btn.setDefault(True)
        #
        # Labels.
        self.browseL = QtGui.QLabel(self)
        self.browseL.setText('File')
        self.pwdL = QtGui.QLabel(self)
        self.pwdL.setText('Password')
        #
        self.dir.textChanged.connect(self.Update)
        self.browse.clicked.connect(self.Browse)
        self.btn.clicked.connect(self.Exit)
        #
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.browseL, 1, 1, 1, 1)
        layout.addWidget(self.dir, 1, 2, 1, 5)
        layout.addWidget(self.browse, 1, 7, 1, 1)
        layout.addWidget(self.pwdL, 2, 1, 1, 1)
        layout.addWidget(self.pwd, 2, 2, 1, 6)
        layout.addWidget(self.btn, 4, 1, 1, 7)
        self.setLayout(layout)
        #

    def Update(self, text):
        self.transmit['dir'] = str(text)

    def Browse(self):
        f = QtGui.QFileDialog()
        if self.action == 'Create !':
            input = f.getSaveFileName(self, self.title, os.getcwd(), 'All files (*.*)')
            self.dir.setText(str(input))
        elif self.action == 'Open !':
            input = f.getOpenFileName(self, self.title, os.getcwd(), 'All files (*.*)')
            self.dir.setText(str(input))
        elif self.action == 'Add !':
            input = f.getOpenFileNames(self, self.title, os.getcwd(), 'All files (*.*)')
            text = ''
            for elem in input:
                text += str(elem) + ';'
            self.dir.setText(text[:-1])

    def Exit(self):
        self.transmit['pwd'] = str(self.pwd.text())
        self.done(1)


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
        # Some settings.
        self.resize(800, 600)
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.setMaximumSize(QtCore.QSize(800, 600))
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('CleanLooks'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        self.setObjectName('MainWindow')
        self.setWindowTitle('Private Briefcase GUI')
        self.setWindowIcon(QtGui.QIcon('PB.ico'))
        #
        # Set central widget.
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setStyleSheet(WStyle)
        self.centralwidget.setObjectName('centralWidget')
        self.setCentralWidget(self.centralwidget)
        #
        # Set status bar.
        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName('statusBar')
        self.setStatusBar(statusbar)
        #
        # Set tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 500))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName('tabWidget')
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabCloseRequested.connect(self._close_tab)
        #
        # Setup actions.
        self.actionNew = QtGui.QAction(self)
        iconNew = QtGui.QIcon()
        iconNew.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-New.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(iconNew)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setText("New")
        self.actionOpen = QtGui.QAction(self)
        iconOpen = QtGui.QIcon()
        iconOpen.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(iconOpen)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setText("Open")
        self.actionJoin = QtGui.QAction(self)
        iconJoin = QtGui.QIcon()
        iconJoin.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Join.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJoin.setIcon(iconJoin)
        self.actionJoin.setObjectName("actionJoin")
        self.actionJoin.setText("Join")
        self.actionAddFiles = QtGui.QAction(self)
        iconAddFiles = QtGui.QIcon()
        iconAddFiles.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddFiles.setIcon(iconAddFiles)
        self.actionAddFiles.setObjectName("actionAddFiles")
        self.actionAddFiles.setText("Add files")
        self.actionExport = QtGui.QAction(self)
        iconExport = QtGui.QIcon()
        iconExport.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport.setIcon(iconExport)
        self.actionExport.setObjectName("actionExport")
        self.actionExport.setText("Export")
        self.actionProperties = QtGui.QAction(self)
        iconProperties = QtGui.QIcon()
        iconProperties.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Properties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(iconProperties)
        self.actionProperties.setObjectName("actionProperties")
        self.actionProperties.setText("Properties")
        self.actionRefresh = QtGui.QAction(self)
        iconRefresh = QtGui.QIcon()
        iconRefresh.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(iconRefresh)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.setText("Refresh")
        self.actionHelp = QtGui.QAction(self)
        iconHelp = QtGui.QIcon()
        iconHelp.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(iconHelp)
        self.actionHelp.setObjectName("actionHelp")
        self.actionHelp.setText("Help")
        self.actionAbout = QtGui.QAction(self)
        iconAbout = QtGui.QIcon()
        iconAbout.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(iconAbout)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")
        #
        # Tool bar.
        toolBar = QtGui.QToolBar(self)
        toolBar.setIconSize(QtCore.QSize(36, 36))
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolBar.setObjectName('toolBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea, toolBar)
        #
        # Add actions on toolbar.
        self.actionNew.triggered.connect(self.on_new)
        toolBar.addAction(self.actionNew)
        self.actionOpen.triggered.connect(self.on_open)
        toolBar.addAction(self.actionOpen)
        self.actionJoin.triggered.connect(self.on_join)
        toolBar.addAction(self.actionJoin)
        self.actionAddFiles.triggered.connect(self.on_add)
        toolBar.addAction(self.actionAddFiles)
        self.actionExport.triggered.connect(self.on_export)
        toolBar.addAction(self.actionExport)
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
        iconView = QtGui.QIcon()
        iconView.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-View.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionView.setIcon(iconView)
        self.actionView.setObjectName("actionView")
        self.actionView.setText("View")
        self.actionEdit = QtGui.QAction(self)
        iconEdit = QtGui.QIcon()
        iconEdit.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(iconEdit)
        self.actionEdit.setObjectName("actionEdit")
        self.actionEdit.setText("Edit")
        self.actionCopy = QtGui.QAction(self)
        iconCopy = QtGui.QIcon()
        iconCopy.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(iconCopy)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCopy.setText("Copy")
        self.actionDelete = QtGui.QAction(self)
        iconDelete = QtGui.QIcon()
        iconDelete.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(iconDelete)
        self.actionDelete.setObjectName("actionDelete")
        self.actionDelete.setText("Delete")
        self.actionRename = QtGui.QAction(self)
        iconRename = QtGui.QIcon()
        iconRename.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Rename.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRename.setIcon(iconRename)
        self.actionRename.setObjectName("actionRename")
        self.actionRename.setText("Rename")
        self.actionProperties = QtGui.QAction(self)
        iconProperties = QtGui.QIcon()
        iconProperties.addPixmap(QtGui.QPixmap(":/root/Symbols/Symbol-Properties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(iconProperties)
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
        # Default file for command line access.
        try:
            self.default_file = sys.argv[1]
            self.on_open()
        except:
            self.default_file = ''
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
        vPos = self.cursor().pos()
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        self.tabs[tab_name+'_bs'] = self.childAt(self.mapFromGlobal(vPos)).objectName() # Selected button.
        self.qtMenu.exec_(vPos) # Execute menu.
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

    def _close_tab(self, index):
        #
        tab_name = str(self.tabWidget.tabText(index))
        self.tabWidget.removeTab(index)
        #
        del self.tabs[tab_name+'_bs']  # Del selected buttons.
        for btn in self.tabs[tab_name+'_btns']: # Del each buttons.
            del btn
        del self.tabs[tab_name+'_btns'] # Del buttons pointer.
        del self.tabs[tab_name+'_c']    # Del contents.
        del self.tabs[tab_name]         # Del tab.
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
        if len(file_name)>13:
            fname = file_name[:13]+' (...)'
        else:
            fname = file_name
        pushButton.setText(fname)
        pushButton.setStyleSheet('text-align: left bottom; padding: 4px;')
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
        dlg = CustomDialog(self.centralwidget, 'Create new briefcase file', 'Browse to the '\
            'directory where you want to create the new Briefcase file. You can set a default '\
            'password, but password is optional.', 'Create !')
        dlg.exec_()
        dir, pwd = dlg.transmit['dir'], dlg.transmit['pwd']
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        #
        tab_name = os.path.split(dir.title())[1]
        self.tabs[tab_name+'_pb'] = Briefcase(dir, pwd) # Briefcase for current tab.
        self._new_tab(tab_name)
        self.tabWidget.setCurrentWidget(self.tabs[tab_name]) # Must enable new tab.
        #

    def on_open(self):
        #
        dlg = CustomDialog(self.centralwidget, 'Open briefcase file', 'Browse to the '\
            'directory where the Briefcase file is located. You must provite the correct '
            'password to be able to decrypt the files.', 'Open !')
        if self.default_file:
            dlg.dir.setText(self.default_file)
            dlg.pwd.setFocus(0)
        dlg.exec_()
        dir, pwd = dlg.transmit['dir'], dlg.transmit['pwd']
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        #
        tab_name = os.path.split(dir.title())[1]
        # Check for existance.
        if self.tabs.has_key(tab_name):
            QtGui.QMessageBox.warning(self.centralwidget, 'Will not Open',
                '<br>Warning! "%s" is already open!<br>' % tab_name)
            return
        #
        try:
            self.tabs[tab_name+'_pb'] = Briefcase(dir, pwd) # Briefcase for current tab.
        except:
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Open',
                '<br>Error! Wrong password!<br>')
            return
        #
        self._new_tab(tab_name)
        self.tabWidget.setCurrentWidget(self.tabs[tab_name]) # Must enable new tab.
        #
        for file_name in self.tabs[tab_name+'_pb'].GetFileList():
            self._new_button(tab_name, file_name)
        #
        self.sort_btns()
        #

    def on_join(self):
        #
        print( 'Triggered JOIN !' )
        # Some code goes in here...
        #

    def on_add(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Add',
                '<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>')
            return
        #
        dlg = CustomDialog(self.centralwidget, 'Add files to briefcase', 'Select the files to be '
            'added. You can specify a password and one or more labels, separated by ";".', 'Add !')
        dlg.browseL.setText('Files')
        dlg.lblL = QtGui.QLabel()
        dlg.lblL.setText('Labels')
        dlg.lbl = QtGui.QLineEdit(dlg)
        dlg.lbl.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        dlg.lbl.setMinimumSize(QtCore.QSize(1, 22))
        dlg.layout().addWidget(dlg.lblL, 3, 1, 1, 1)
        dlg.layout().addWidget(dlg.lbl, 3, 2, 1, 6)
        dlg.resize(300, 130)
        dlg.setMinimumSize(QtCore.QSize(300, 130))
        dlg.setMaximumSize(QtCore.QSize(300, 130))
        dlg.exec_()
        # Selected files are separated by ";" so must be exploded.
        dir = dlg.transmit['dir'].split(';')
        # If not password was selected, default password must be used, so pwd -> 1.
        pwd = dlg.transmit['pwd']
        if not pwd: pwd = 1
        # Save labels, transformed into python string.
        lbl = str(dlg.lbl.text())
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        #
        for elem in dir:
            self.tabs[tab_name+'_pb'].AddFile(elem, pwd, lbl)
            file_name = os.path.split(elem)[1]
            self._new_button(tab_name, file_name)
        #
        self.sort_btns()
        #

    def on_export(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Export',
                '<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>')
            return
        #
        f = QtGui.QFileDialog()
        input = f.getExistingDirectory(self.centralwidget, 'Select a folder to export into :',
            os.getcwd())
        if input:
            self.tabs[tab_name+'_pb'].ExportAll(str(input))
            QtGui.QMessageBox.information(self.centralwidget, 'Export', 'Export finished !')
        #

    def on_refresh(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Refresh',
                '<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>')
            return
        self.sort_btns()
        #

    def on_db_properties(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Properties',
                '<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>')
            return
        prop = self.tabs[tab_name+'_pb'].Info()
        if not prop['allLabels']:
            prop['allLabels'] = '-'
        QtGui.QMessageBox.information(self.centralwidget, 'Properties for %s' % tab_name, '''
            <br><b>numberOfFiles</b> : %(numberOfFiles)i
            <br><b>dateCreated</b> : %(dateCreated)s
            <br><b>userCreated</b> : %(userCreated)s
            <br><b>allLabels</b> : %(allLabels)s
            <br><b>versionCreated</b> : %(versionCreated)s
            <br>''' % prop)
        del tab_name
        #

    def on_help(self):
        #
        QtGui.QMessageBox.information(self.centralwidget, 'Private Briefcase Help',
            '<br>Please check <b>Online Help</b> : http://code.google.com/p/private-briefcase/w/<br>')
        #

    def on_about(self):
        #
        QtGui.QMessageBox.about(self.centralwidget, 'About Private Briefcase',
            '<br><b>Copyright © 2009-2010</b> : Cristi Constantin. All rights reserved.<br>'
            '<b>Website</b> : http://private-briefcase.googlecode.com<br>')
        #

    def on_view(self):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        # If caller is an action.
        if type(self.sender()) == type(QtGui.QPushButton()):
            self.tabs[tab_name+'_pb'].ExportFile(str(self.sender().objectName()), execute=True)
        # If caller is a button.
        else:
            qtBS = str(self.tabs[tab_name+'_bs'])
            self.tabs[tab_name+'_pb'].ExportFile(qtBS, execute=True)
            del qtBS
        del tab_name
        #

    def on_edit(self):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        self.tabs[tab_name+'_pb'].ExportFile(qtBS, execute=True)
        del tab_name, qtBS
        #

    def on_copy(self):
        #
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
        #

    def on_delete(self):
        #
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
        #

    def on_rename(self):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        qtTxt, qtMsg = QtGui.QInputDialog.getText(self.centralwidget, 'Rename file ? ...',
            'New name :', QtGui.QLineEdit.Normal, qtBS)
        if qtMsg and str(qtTxt): # Clicked yes and text exists.
            ret = self.tabs[tab_name+'_pb'].RenFile(fname=qtBS, new_fname=str(qtTxt))
            if ret==0: # If Briefcase returns 0, rename the button.
                self.tabs[tab_name+'_btns'][qtBS].setObjectName(qtTxt)
                self.tabs[tab_name+'_btns'][qtBS].setStatusTip(qtTxt)
                self.tabs[tab_name+'_btns'][qtBS].setText(qtTxt)
                # Pass the pointer to the new name.
                self.tabs[tab_name+'_btns'][str(qtTxt)] = self.tabs[tab_name+'_btns'][qtBS]
                del self.tabs[tab_name+'_btns'][qtBS]
                self.sort_btns()
        del tab_name, qtBS, qtTxt, qtMsg
        #

    def on_properties(self):
        #
        tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        qtBS = str(self.tabs[tab_name+'_bs']) # Selected button.
        prop = self.tabs[tab_name+'_pb'].FileStatistics(fname=qtBS)
        if not prop['labels']:
            prop['labels'] = '-'
        QtGui.QMessageBox.information(self.centralwidget, 'Properties for %s' % qtBS, '''
            <br><b>fileName</b> : %(fileName)s
            <br><b>intern FileName</b> : %(internFileName)s
            <br><b>first FileSize</b> : %(firstFileSize)i
            <br><b>last FileSize</b> : %(lastFileSize)i
            <br><b>largest Size</b> : %(biggestSize)i
            <br><b>first FileDate</b> : %(firstFileDate)s
            <br><b>last FileDate</b> : %(lastFileDate)s
            <br><b>first FileUser</b> : %(firstFileUser)s
            <br><b>last FileUser</b> : %(lastFileUser)s
            <br><b>labels</b> : %(labels)s
            <br><b>versions</b> : %(versions)i<br>''' % prop)
        del tab_name, qtBS, prop
        #


import res_rc

app = QtGui.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Eof()