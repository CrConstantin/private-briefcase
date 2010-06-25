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
import os, sys

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
    background-position: top center;
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
        self.setMinimumSize(QtCore.QSize(280, 90))
        self.setMaximumSize(QtCore.QSize(320, 110))
        self.setWindowTitle(title)
        self.setWhatsThis(whatsthis)
        #
        # Buttons.
        self.browse = QtGui.QPushButton('...', self)
        self.browse.setMinimumSize(QtCore.QSize(1, 20))
        self.dir = QtGui.QLineEdit(self)
        self.dir.setFocus(0)
        self.dir.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.dir.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd = QtGui.QLineEdit(self)
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.pwd.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.pwd.setMinimumSize(QtCore.QSize(1, 22))
        self.btn = QtGui.QPushButton(action, self)
        self.btn.setMinimumSize(QtCore.QSize(1, 20))
        self.btn.setDefault(True)
        #
        # Labels.
        self.browseL = QtGui.QLabel('File', self)
        self.pwdL = QtGui.QLabel('Password', self)
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
        self.centralwidget.setObjectName('centralWidget')
        self.centralwidget.setStyleSheet(WStyle)
        self.setCentralWidget(self.centralwidget)
        #
        # Set status bar.
        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName('statusBar')
        self.setStatusBar(statusbar)
        #
        # Set tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName('tabWidget')
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 500))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabCloseRequested.connect(self._close_tab)
        #
        # Setup actions.
        self.actionNew = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-New.png')), 'New', self)
        self.actionNew.setToolTip("Create new briefcase (Ctrl+N)")
        self.actionNew.setShortcut('Ctrl+N')
        #
        self.actionOpen = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Open.png')), 'Open', self)
        self.actionOpen.setToolTip("Open existing briefcase (Ctrl+O)")
        self.actionOpen.setShortcut('Ctrl+O')
        #
        ''' # Hidden for now !
        self.actionJoin = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Join.png')), 'Join', self)
        self.actionJoin.setToolTip("Join two briefcase files")
        self.actionJoin.setVisible(False)
        self.actionJoin.setShortcut('Ctrl+J')
        '''
        #
        self.actionAddFiles = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Add.png')), 'Add Files', self)
        self.actionAddFiles.setToolTip("Put files inside the briefcase (Ctrl+F)")
        self.actionAddFiles.setVisible(False)
        self.actionAddFiles.setShortcut('Ctrl+F')
        #
        self.actionExport = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Export.png')), 'Export All', self)
        self.actionExport.setToolTip("Export all files in a folder (Ctrl+E)")
        self.actionExport.setVisible(False)
        self.actionExport.setShortcut('Ctrl+E')
        #
        self.actionDBProperties = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Properties.png')), 'Properties', self)
        self.actionDBProperties.setToolTip("Briefcase details (Ctrl+D)")
        self.actionDBProperties.setVisible(False)
        self.actionDBProperties.setShortcut('Ctrl+D')
        #
        self.actionShowLog = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Announce.png')), 'Log', self)
        self.actionShowLog.setToolTip("Show briefcase log (Ctrl+L)")
        self.actionShowLog.setVisible(False)
        self.actionShowLog.setShortcut('Ctrl+L')
        #
        self.actionRefresh = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Refresh.png')), 'Refresh', self)
        self.actionRefresh.setToolTip("Re-Arange icons (Ctrl+R)")
        self.actionRefresh.setVisible(False)
        self.actionRefresh.setShortcut('Ctrl+R')
        #
        self.actionHelp = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Help.png')), 'Help', self)
        self.actionHelp.setToolTip("View help (Ctrl+H)")
        self.actionHelp.setShortcut('Ctrl+H')
        self.actionAbout = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Information.png')), 'About', self)
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
        #self.actionJoin.triggered.connect(self.on_join)
        #toolBar.addAction(self.actionJoin)
        self.actionAddFiles.triggered.connect(self.on_add)
        toolBar.addAction(self.actionAddFiles)
        self.actionExport.triggered.connect(self.on_export)
        toolBar.addAction(self.actionExport)
        self.actionDBProperties.triggered.connect(self.on_db_properties)
        toolBar.addAction(self.actionDBProperties)
        self.actionShowLog.triggered.connect(self.on_show_log)
        toolBar.addAction(self.actionShowLog)
        self.actionRefresh.triggered.connect(self.on_refresh)
        toolBar.addAction(self.actionRefresh)
        self.actionHelp.triggered.connect(self.on_help)
        toolBar.addAction(self.actionHelp)
        self.actionAbout.triggered.connect(self.on_about)
        toolBar.addAction(self.actionAbout)
        #
        # Button actions.
        self.actionView = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-View.png')), 'View', self)
        self.actionEdit = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Edit.png')), 'Edit', self)
        self.actionCopy = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Copy.png')), 'Copy', self)
        self.actionDelete = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Delete.png')), 'Delete', self)
        self.actionRename = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Rename.png')), 'Rename', self)
        self.actionProperties = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Properties.png')), 'Properties', self)
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
        self.actionAddFiles.setVisible(True)
        self.actionExport.setVisible(True)
        self.actionDBProperties.setVisible(True)
        self.actionShowLog.setVisible(True)
        self.actionRefresh.setVisible(True)
        #

    def _close_tab(self, index):
        #
        tab_name = str(self.tabWidget.tabText(index)) # Tab name based on index.
        self.tabWidget.removeTab(index)
        #
        del self.tabs[tab_name+'_bs']   # Del selected buttons.
        for btn in self.tabs[tab_name+'_btns']: # Del all buttons.
            del btn
        del self.tabs[tab_name+'_btns'] # Del buttons pointer.
        del self.tabs[tab_name+'_c']    # Del contents.
        del self.tabs[tab_name+'_pb']   # Del Briefcase.
        del self.tabs[tab_name]         # Del tab.
        #
        if not self.tabs:
            self.actionAddFiles.setVisible(False)
            self.actionExport.setVisible(False)
            self.actionDBProperties.setVisible(False)
            self.actionShowLog.setVisible(False)
            self.actionRefresh.setVisible(False)
        #

    def _new_button(self, tab_name, file_name):
        #
        # Setup button.
        pushButton = QtGui.QPushButton(self.tabs[tab_name+'_c'])
        pushButton.setGeometry(self.calculate_x(), self.calculate_y(), 98, 60)
        pushButton.setFlat(True)
        pushButton.setObjectName(file_name)
        pushButton.setStatusTip(file_name)
        if len(file_name)>13:
            fname = file_name[:13]+' (...)'
        else:
            fname = file_name
        pushButton.setText(fname)
        pushButton.setStyleSheet('background-image: url(Extensions/Default.png);'
            'text-align: center bottom; padding: 4px;')
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
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
            <br><b>Number of files</b> : %(numberOfFiles)i
            <br><b>Date created</b> : %(dateCreated)s
            <br><b>User created</b> : %(userCreated)s
            <br><b>All labels</b> : %(allLabels)s
            <br><b>Version created</b> : %(versionCreated)s
            <br>''' % prop)
        del tab_name
        #

    def on_show_log(self):
        #
        try : tab_name = str(self.tabWidget.currentWidget().objectName()) # Current tab.
        except :
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Log',
                '<br>Error! Must first <b>Create New</b> or <b>Open Briefcase</b>!<br>')
            return
        #
        logs = self.tabs[tab_name+'_pb'].c.execute('select date, msg from _logs_').fetchall()
        dlg = QtGui.QDialog(self)
        dlg.setMinimumSize(QtCore.QSize(200, 600))
        table = QtGui.QTableWidget(dlg)
        table.setColumnCount(2)
        table.setRowCount(len(logs))
        table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Date'))
        table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Message'))
        table.setColumnWidth(0, 118)
        #
        for i in range(len(logs)):
            table.setItem(i, 0, QtGui.QTableWidgetItem(logs[i][0]))
            table.setItem(i, 1, QtGui.QTableWidgetItem(logs[i][1]))
        #
        layout = QtGui.QVBoxLayout(dlg)
        layout.addWidget(table)
        dlg.setLayout(layout)
        dlg.exec_()
        del dlg
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
        #
        if prop['versions'] == 1:
            QtGui.QMessageBox.information(self.centralwidget, 'Properties for %s' % qtBS, '''
                <br><b>File Name</b> : %(fileName)s
                <br><b>intern FileName</b> : %(internFileName)s
                <br><b>FileSize</b> : %(lastFileSize)i
                <br><b>FileDate</b> : %(lastFileDate)s
                <br><b>FileUser</b> : %(lastFileUser)s
                <br><b>labels</b> : %(labels)s
                <br><b>versions</b> : %(versions)i<br>''' % prop)
        else:
            QtGui.QMessageBox.information(self.centralwidget, 'Properties for %s' % qtBS, '''
                <br><b>File Name</b> : %(fileName)s
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
        #
        del tab_name, qtBS, prop
        #


import res_rc

app = QtGui.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Eof()