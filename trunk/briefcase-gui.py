# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright (C) 2009-2012, Cristi Constantin. All rights reserved. \n\
    Website : http://private-briefcase.googlecode.com \n\
    This module contains Briefcase GUI class with all its functions. \n\
'''

# Standard libraries.
import os, sys
import glob
import shutil

# External dependency.
from briefcase import *
from Crypto.Hash import MD4

from PyQt4 import QtCore
from PyQt4 import QtGui


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  M A I N   W I N D O W
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        #
        super(MainWindow, self).__init__(None)

        # Some settings.
        self.resize(800, 600)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('CleanLooks'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        self.setObjectName('MainWindow')
        self.setWindowTitle('Private Briefcase GUI')
        icon_path = os.path.split(os.path.abspath(__file__))[0] + '/PB.ico'
        self.setWindowIcon(QtGui.QIcon(icon_path))

        # Define central widget.
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName('centralWidget')
        self.setCentralWidget(self.centralwidget)

        # Define central layout.
        mainLayout = QtGui.QVBoxLayout(self.centralwidget)

        # Set status bar.
        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName('statusBar')
        self.setStatusBar(statusbar)

        # Set tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName('tabWidget')
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabCloseRequested.connect(self._close_tab)
        mainLayout.addWidget(self.tabWidget)

        # Define all actions...
        self.actionNew = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-New.png')), 'New', self)
        self.actionNew.setToolTip("Create new briefcase (Ctrl+N)")
        self.actionNew.setShortcut('Ctrl+N')
        #
        self.actionOpen = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Open.png')), 'Open', self)
        self.actionOpen.setToolTip("Open existing briefcase (Ctrl+O)")
        self.actionOpen.setShortcut('Ctrl+O')
        #
        # Hidden for now !
        '''
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
        self.actionCleanup = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Warning.png')), 'Cleanup !', self)
        self.actionCleanup.setToolTip("Cleanup Database ! (Ctrl+1)")
        self.actionCleanup.setVisible(False)
        self.actionCleanup.setShortcut('Ctrl+1')
        #
        self.actionDBProperties = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Properties.png')), 'Properties', self)
        self.actionDBProperties.setToolTip("Briefcase details (Ctrl+D)")
        self.actionDBProperties.setVisible(False)
        self.actionDBProperties.setShortcut('Ctrl+D')
        #
        self.actionShowLog = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Log.png')), 'Log', self)
        self.actionShowLog.setToolTip("Show briefcase log (Ctrl+L)")
        self.actionShowLog.setVisible(False)
        self.actionShowLog.setShortcut('Ctrl+L')
        #
        self.actionHelp = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Help.png')), 'Help', self)
        self.actionHelp.setToolTip("View help (Ctrl+H)")
        self.actionHelp.setShortcut('Ctrl+H')
        self.actionAbout = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Information.png')), 'About', self)

        # Tool bar.
        toolBar = QtGui.QToolBar(self)
        toolBar.setIconSize(QtCore.QSize(36, 36))
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolBar.setObjectName('toolBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea, toolBar)

        # Add actions on toolbar.
        self.actionNew.triggered.connect(self.on_new)
        toolBar.addAction(self.actionNew)
        self.actionOpen.triggered.connect(self.on_open)
        toolBar.addAction(self.actionOpen)
        #self.actionJoin.triggered.connect(self.on_join) # Hidden for now.
        #toolBar.addAction(self.actionJoin)
        self.actionAddFiles.triggered.connect(self.on_add)
        toolBar.addAction(self.actionAddFiles)
        self.actionExport.triggered.connect(self.on_export)
        toolBar.addAction(self.actionExport)
        self.actionCleanup.triggered.connect(self.on_cleanup)
        toolBar.addAction(self.actionCleanup)
        self.actionDBProperties.triggered.connect(self.on_db_properties)
        toolBar.addAction(self.actionDBProperties)
        self.actionShowLog.triggered.connect(self.on_show_log)
        toolBar.addAction(self.actionShowLog)
        self.actionHelp.triggered.connect(self.on_help)
        toolBar.addAction(self.actionHelp)
        self.actionAbout.triggered.connect(self.on_about)
        toolBar.addAction(self.actionAbout)

        # Open file for command line access... if any.
        default_file = sys.argv[1:2]

        if default_file:
            self.default_file = default_file[0]
            self.on_open()

        # Reset.
        self.default_file = ''
        #

    def closeEvent(self, event):
        #
        for index in range(self.tabWidget.count()):
            vCurrent = self.tabWidget.widget(index)
            vCurrent.close() # Release resources.
        #
        self.close()
        #

    def _close_tab(self, index):
        #
        vCurrent = self.tabWidget.widget(index)
        self.tabWidget.removeTab(index) # Remove from tabs.
        vCurrent.close() # Release resources.
        del vCurrent     # Del pointer.
        #
        if not self.tabWidget.count():
            self.actionAddFiles.setVisible(False)
            self.actionExport.setVisible(False)
            self.actionCleanup.setVisible(False)
            self.actionDBProperties.setVisible(False)
            self.actionShowLog.setVisible(False)
        #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Triggered functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def on_new(self):
        #
        dlg = CustomDialog(self.centralwidget, 'Create new briefcase file', 'Browse to the '\
            'directory where you want to create the new Briefcase file. You can set a default '\
            'password, but password is optional.', 'Create !')
        dlg.exec_()
        dir, pwd, pwd2 = str(dlg.dir.text()), str(dlg.pwd.text()), str(dlg.pwd2.text())
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg

        if pwd != pwd2:
            QtGui.QMessageBox.warning(self.centralwidget, 'Will not Create', '<br>Passwords don\'t match !<br>')
            return
        if not pwd: pwd = False # If no password, password is Null.

        tab_name = os.path.split(dir.title())[1]
        new_tab = CustomTab(self, tab_name, dir, pwd)
        self.tabWidget.addTab(new_tab, ' [ '+tab_name+' ] ') # Add tab to tab widget.
        self.tabWidget.setCurrentWidget(new_tab) # Switch to the new tab.

        self.actionAddFiles.setVisible(True)
        self.actionExport.setVisible(True)
        self.actionCleanup.setVisible(True)
        self.actionDBProperties.setVisible(True)
        self.actionShowLog.setVisible(True)
        #


    def on_open(self):
        #
        dlg = CustomDialog(self.centralwidget, 'Open briefcase file', 'Browse to the directory ' \
            'where the Briefcase file is located. You must provite the correct password to be able ' \
            'to decrypt the files.', 'Open !')
        if self.default_file:
            dlg.dir.setText(self.default_file)
            dlg.pwd.setFocus(0)

        dlg.exec_()
        dir, pwd = str(dlg.dir.text()), str(dlg.pwd.text())
        if self.default_file and not dlg.result(): sys.exit(0) # If open with ARGS and canceled, exit.
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        if not pwd: pwd = False # If no password, password is Null.

        if not os.path.exists(dir):
            QtGui.QMessageBox.warning(self.centralwidget, 'Will not Open', '<br>"%s" doesn\'t exist !<br>' % dir)
            return

        tab_name = os.path.split(dir.title())[1]
        # Check for existance in all tabs.
        for vTab in range(self.tabWidget.count()):
            if self.tabWidget.tabText(vTab) == tab_name:
                QtGui.QMessageBox.warning(self.centralwidget, 'Will not Open', '<br>"%s" is already open !<br>' % tab_name)
                return

        try:
            b = Briefcase(dir, pwd) # Briefcase for current tab.
        except:
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Open', '<br>Error ! Wrong password !<br>')
            return

        new_tab = CustomTab(self, tab_name, dir, pwd)
        self.tabWidget.addTab(new_tab, ' [ '+tab_name+' ] ') # Add tab to tab widget.
        self.tabWidget.setCurrentWidget(new_tab) # Must enable new tab.
        new_tab.fRefresh()

        self.actionAddFiles.setVisible(True)
        self.actionExport.setVisible(True)
        self.actionCleanup.setVisible(True)
        self.actionDBProperties.setVisible(True)
        self.actionShowLog.setVisible(True)
        #


    def on_join(self):
        #
        print( 'Triggered JOIN !' )
        # Some code goes in here...
        #


    def on_add(self):
        '''
        Add one or more files in the briefcase.
        '''

        vCurrent = self.tabWidget.currentWidget() # Current tab.
        dlg = CustomDialog(vCurrent, 'Add files to briefcase', 'Select the files to be '
            'added. You can specify a password and one or more labels, separated by ";".', 'Add !')
        dlg.browseL.setText('Files')
        dlg.exec_()

        # Selected files are separated by ";" so must be exploded.
        dirs = str(dlg.dir.text()).split(';')
        pwd = str(dlg.pwd.text())
        compress = dlg.radioZLIB.isChecked()
        if not pwd: pwd = 1 # If password is null, use database default value.
        lbl = str(dlg.lbl.text()) # Labels.
        if not dirs or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg

        for elem in dirs:
            if compress:
                vCurrent.b.AddFile(elem, pwd, lbl, 'zlib')
            else:
                vCurrent.b.AddFile(elem, pwd, lbl, 'bz2')
            file_name = os.path.split(elem)[1]
            vInfo = vCurrent.b.FileStatistics(file_name)
            vCurrent.create_button(file_name, vInfo['lastFileSize'], vInfo['versions'])

        vCurrent.fRefresh()
        #


    def on_export(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        f = QtGui.QFileDialog()
        input = f.getExistingDirectory(vCurrent, 'Select a folder to export into :',
            os.getcwd())
        if input:
            input = str(input.toUtf8())
            vRet = vCurrent.b.ExportAll(input)
            QtGui.QMessageBox.information(vCurrent, 'Export', 'Export finished !')
        #


    def on_cleanup(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        qtMsg = QtGui.QMessageBox.warning(vCurrent, 'Cleanup database ? ...',
            'Are you sure you want to cleanup the database ?', 'Yes', 'No')
        if qtMsg == 0: # Clicked yes.
            vCurrent.b.Cleanup()
            QtGui.QMessageBox.information(vCurrent, 'Cleanup', 'Cleanup finished !')
        #


    def on_db_properties(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        prop = vCurrent.b.Info()
        if not prop['allLabels']:
            prop['allLabels'] = '-'
        QtGui.QMessageBox.information(self.centralwidget, 'Properties for %s' % vCurrent.objectName(), '''
            <br><b>Number of files</b> : %(numberOfFiles)i
            <br><b>Date created</b> : %(dateCreated)s
            <br><b>User created</b> : %(userCreated)s
            <br><b>All labels</b> : %(allLabels)s
            <br><b>Version created</b> : %(versionCreated)s
            <br>''' % prop)
        #


    def on_show_log(self):
        #
        logs = self.tabWidget.currentWidget().b.c.execute('select date, msg from _logs_').fetchall()
        dlg = QtGui.QDialog(self)
        dlg.setMinimumSize(QtCore.QSize(400, 300))
        dlg.resize(500, self.height()-20)

        table = QtGui.QTableWidget(dlg)
        table.setColumnCount(2)
        table.setRowCount(len(logs))
        table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Date'))
        table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Message'))
        table.setColumnWidth(0, 117)
        table.setColumnWidth(1, 280)

        for i in range(len(logs)):
            table.setItem(i, 0, QtGui.QTableWidgetItem(logs[i][0]))
            table.setItem(i, 1, QtGui.QTableWidgetItem(logs[i][1]))

        layout = QtGui.QVBoxLayout(dlg)
        layout.addWidget(table)
        dlg.setLayout(layout)
        dlg.exec_()
        del table, dlg
        #


    def on_help(self):
        #
        QtGui.QMessageBox.information(self.centralwidget, 'Private Briefcase Help',
            '<br>Please check <b>Online Help</b> : http://code.google.com/p/private-briefcase/w/<br>')
        #


    def on_about(self):
        #
        QtGui.QMessageBox.about(self.centralwidget, 'About Private Briefcase',
            '<br><b>Copyright (C) 2009-2010</b> : Cristi Constantin.<br>All rights reserved.<br>'
            '<b>Website</b> : http://private-briefcase.googlecode.com<br>')
        #


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  D I A L O G   O B J E C T
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class CustomDialog(QtGui.QDialog):

    def __init__(self, parent, title, whatsthis, action):

        '''
        This dialog is used for opening briefcase files, creating, or adding new files.
        '''

        super(CustomDialog, self).__init__(parent)
        self.title = title
        self.action = action
        self.setWindowTitle(title)
        self.setWhatsThis(whatsthis)

        if self.action == 'Open !':
            self.resize(300, 100)
            self.setMinimumSize(QtCore.QSize(290, 90))
            self.setMaximumSize(QtCore.QSize(310, 110))
        else:
            self.resize(300, 150)
            self.setMinimumSize(QtCore.QSize(290, 120))
            self.setMaximumSize(QtCore.QSize(310, 140))

        # Buttons.
        self.browse = QtGui.QPushButton('...', self)
        self.browse.setMaximumSize(QtCore.QSize(20, 20))
        self.dir = QtGui.QLineEdit(self)
        self.dir.setMinimumSize(QtCore.QSize(20, 5))
        self.dir.setFocus(0)

        # Password field.
        self.pwd = QtGui.QLineEdit(self)
        self.pwd.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.pwd2 = QtGui.QLineEdit(self)
        self.pwd2.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd2.setEchoMode(QtGui.QLineEdit.Password)
        if self.action != 'Create !':
            self.pwd2.hide()

        # Action button.
        self.btn = QtGui.QPushButton(action, self)
        self.btn.setMinimumSize(QtCore.QSize(1, 20))
        self.btn.setDefault(True)

        # Labels.
        self.lbl = QtGui.QLineEdit(self)
        self.lbl.setMinimumSize(QtCore.QSize(1, 22))
        self.browseL = QtGui.QLabel('File', self)
        self.pwdL = QtGui.QLabel('Password', self)
        self.lblL = QtGui.QLabel('Labels', self)
        if self.action != 'Add !':
            self.lbl.hide()
            self.lblL.hide()

        # Type of archive.
        self.lblC = QtGui.QLabel('Compression', self)
        self.radioZLIB = QtGui.QRadioButton('ZLIB', self)
        self.radioZLIB.setChecked(True)
        self.radioBZ = QtGui.QRadioButton('BZ2', self)
        if self.action != 'Add !':
            self.lblC.hide()
            self.radioZLIB.hide()
            self.radioBZ.hide()

        # Connect actions.
        self.browse.clicked.connect(self.Browse)
        self.btn.clicked.connect(self.Exit)

        # Add objects in layout.
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.browseL, 1, 1, 1, 1)
        layout.addWidget(self.dir, 1, 2, 1, 5)
        layout.addWidget(self.browse, 1, 7, 1, 1)
        layout.addWidget(self.pwdL, 2, 1, 1, 1)
        layout.addWidget(self.pwd, 2, 2, 1, 6)
        layout.addWidget(self.pwd2, 3, 2, 1, 6)
        layout.addWidget(self.lblL, 4, 1, 1, 1)
        layout.addWidget(self.lbl, 4, 2, 1, 6)
        layout.addWidget(self.lblC, 5, 1, 1, 2)
        layout.addWidget(self.radioZLIB, 5, 3, 1, 2)
        layout.addWidget(self.radioBZ, 5, 5, 1, 2)
        layout.addWidget(self.btn, 6, 1, 1, 7)
        self.setLayout(layout)

    def Browse(self):
        f = QtGui.QFileDialog()
        if self.action == 'Create !':
            input = f.getSaveFileName(self, self.title, os.getcwd(), 'All files (*.*);;PRV Files (*.prv)')
            self.dir.setText(str(input))
        elif self.action == 'Open !':
            input = f.getOpenFileName(self, self.title, os.getcwd(), 'All files (*.*);;PRV Files (*.prv)')
            self.dir.setText(str(input))
        elif self.action == 'Add !':
            input = f.getOpenFileNames(self, self.title, os.getcwd(), 'All files (*.*)')
            text = ''
            for elem in input:
                text += str(elem) + ';'
            self.dir.setText(text[:-1])
        del f

    def Exit(self):
        self.done(1)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  T A B   O B J E C T
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class CustomTab(QtGui.QWidget):

    '''
    The tab widget.
    It contains a filter and sort box, and the items from the briefcase.
    '''

    def __init__(self, parent, tab_name, database, password):

        super(CustomTab, self).__init__(parent)
        self.setObjectName(tab_name)
        self.b = Briefcase(database, password)

        self.mainLayout = QtGui.QGridLayout(self)

        # Filter text
        self.filterBox = QtGui.QLineEdit(self)
        self.filterBox.textChanged.connect(self.fRefresh)
        # Filter label
        self.filterLabel = QtGui.QLabel('&Filter:', self)
        self.filterLabel.setBuddy(self.filterBox)

        # Sort combo
        self.sortCombo = QtGui.QComboBox(self)
        self.sortCombo.addItem('File Asc', 'File Asc')
        self.sortCombo.addItem('File Desc', 'File Desc')
        self.sortCombo.addItem('Size Asc', 'Size Asc')
        self.sortCombo.addItem('Size Desc', 'Size Desc')
        self.sortCombo.addItem('Date Asc', 'Date Asc')
        self.sortCombo.addItem('Date Desc', 'Date Desc')
        self.sortCombo.currentIndexChanged.connect(self.fRefresh)
        # Sort label
        self.sortLabel = QtGui.QLabel('&Sort:', self)
        self.sortLabel.setBuddy(self.sortCombo)

        # Area widget to hold the flow layout...
        self.flowLayout = FlowLayout(parent=None, margin=0, spacing=0)
        areaWidget = QtGui.QWidget()
        areaWidget.setLayout(self.flowLayout)

        # The scroll area that will hold the area widget.
        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(areaWidget)

        # Insert items in the layout
        self.mainLayout.addWidget(self.filterLabel, 1, 1)
        self.mainLayout.addWidget(self.filterBox, 1, 2)
        self.mainLayout.addWidget(self.sortLabel, 1, 3)
        self.mainLayout.addWidget(self.sortCombo, 1, 4)
        self.mainLayout.addWidget(scrollArea, 2, 1, 4, 4)

        # Button actions.
        actionView = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-View.png')), 'View', self)
        actionEdit = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Edit.png')), 'Edit', self)
        actionCopy = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Copy.png')), 'Copy', self)
        actionDelete = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Delete.png')), 'Delete', self)
        actionRename = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Rename.png')), 'Rename', self)
        actionProperties = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Properties.png')), 'Properties', self)

        # Setup Menu + add Actions.
        self.qtMenu = QtGui.QMenu()
        actionView.triggered.connect(self.on_view)
        self.qtMenu.addAction(actionView)
        actionEdit.triggered.connect(self.on_edit)
        self.qtMenu.addAction(actionEdit)
        actionCopy.triggered.connect(self.on_copy)
        self.qtMenu.addAction(actionCopy)
        actionDelete.triggered.connect(self.on_delete)
        self.qtMenu.addAction(actionDelete)
        actionRename.triggered.connect(self.on_rename)
        self.qtMenu.addAction(actionRename)
        actionProperties.triggered.connect(self.on_properties)
        self.qtMenu.addAction(actionProperties)

        # Setup double click timer. Buttons don't have double click action.
        self.dblClickTimer = QtCore.QTimer()
        self.dblClickTimer.setSingleShot(True)
        self.dblClickTimer.setInterval(500)

        self.BUTTON_W = 98
        self.BUTTON_H = 64

        self.buttons = {}
        self.buttons_visible = []

        # Populate with icons, each icon represents a file from the Briefcase
        for file_name in self.b.GetFileList():
            vInfo = self.b.FileStatistics(file_name)
            self.create_button(file_name, vInfo['lastFileSize'], vInfo['versions'])
        #


    def create_button(self, file_name, file_size, versions):
        '''
        Each button represents a file from the briefcase.
        '''
        pushButton = QtGui.QPushButton(self)
        pushButton.setMinimumSize(QtCore.QSize(self.BUTTON_W, self.BUTTON_H))
        pushButton.setMaximumSize(QtCore.QSize(self.BUTTON_W, self.BUTTON_H))
        pushButton.resize(QtCore.QSize(self.BUTTON_W, self.BUTTON_H))

        pushButton.setCheckable(True)
        pushButton.setFlat(True)

        self.update_button(pushButton, file_name, file_size, versions)

        # Style sheet.
        pushButton.setStyleSheet('''
        QPushButton {
        	border-style: outset;
        	border: 2px solid #999;
        	border-radius: 5px;
        	padding: 2px;
        	margin: 2px;
        	font: 10px;
        	text-align: center bottom;
        	color: #001;
        	/* background-image: url(Extensions/Default.png);'
        	background-position: top center; */
        }
        QPushButton:pressed { border-style: inset; }
        QPushButton:checked { border: 2px dashed #f33 }''')

        # Connect events.
        pushButton.clicked.connect(self.on_double_click)
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        pushButton.customContextMenuRequested.connect(self.on_right_click)

        # Save pointer.
        self.buttons[file_name] = pushButton
        self.buttons_visible.append(pushButton)

        self.flowLayout.addWidget(pushButton)
        #


    def update_button(self, pushButton, file_name, file_size, versions):
        '''
        Update button info.
        '''
        # Full name.
        pushButton.setObjectName(file_name)
        # Short name.
        if len(file_name) > 12: pushButton.setText(file_name[:12] + ' (...)')
        else:                   pushButton.setText(file_name)
        # Tool tip.
        pushButton.setToolTip('<pre>%s<br>Size: %i bytes<br>Versions: %i</pre>' % (file_name, file_size, versions))


    def fRefresh(self):
        '''
        Refresh buttons.
        This function is used when opening, adding, renaming or deleting buttons.
        '''

        pass


    def on_double_click(self):
        #
        # If after receiving the first click, the timer isn't running, start the timer and return
        if not self.dblClickTimer.isActive():
            self.dblClickTimer.start()
            return
        # If timer is running and hasn't timed out, the second click occured within timer interval
        else:
            self.on_view()
            self.dblClickTimer.stop() # Stop timer so next click can start it again
            return
        #


    def on_right_click(self):
        #
        vPos = self.cursor().pos()
        # Selected button to string.
        button_selected = str(self.childAt(self.mapFromGlobal(vPos)).objectName())
        self.buttons_selected = button_selected
        # Execute menu.
        self.qtMenu.exec_(vPos)
        #


    def on_view(self):
        #
        if type(self.sender()) == type(QtGui.QPushButton()): # If caller is an action.
            vFile = str(self.sender().objectName())
        else: # If caller is a button.
            vFile = self.buttons_selected

        vRes = self.b.ExportFile(vFile, execute=True)

        for i in range(3):
            if vRes != -1: # If password is correct, break.
                break
            else:
                qtTxt, qtMsg = QtGui.QInputDialog.getText(self, 'Enter password',
                    'This file requires a password :', QtGui.QLineEdit.Password)
                qtTxt = str(qtTxt.toUtf8())
                if qtMsg:
                    vRes = self.b.ExportFile(vFile, qtTxt, execute=True)
                else:
                    return

        if vRes == -1: # If password is still wrong after 3 tries.
            QtGui.QMessageBox.critical(self, 'Error on view', '<br>Wrong password 3 times !<br>')

        del vFile, vRes
        #


    def on_edit(self):
        #
        temp_dir = os.getenv('temp') + '__temp_py__'
        filename = temp_dir + '/' + self.buttons_selected

        try:
            os.mkdir(temp_dir)
        except:
            print('Cannot create temp file!')

        # Create temp file and return file hash.
        old_hash = self.b.ExportFile(fname=self.buttons_selected, path=temp_dir, execute=False)

        for i in range(3):
            if old_hash != -1:
                break
            else:
                qtTxt, qtMsg = QtGui.QInputDialog.getText(self, 'Enter password',
                    'This file requires a password :', QtGui.QLineEdit.Password)
                qtTxt = str(qtTxt.toUtf8())
                if qtMsg:
                    old_hash = self.b.ExportFile(fname=self.buttons_selected, password=qtTxt, path=temp_dir, execute=False)
                else:
                    return

        if old_hash == -1: # If password is still wrong.
            QtGui.QMessageBox.critical(self, 'Error on edit', '<br>Wrong password 3 times !<br>')
            return

        # Execute.
        if os.name=='posix':
            os.system('gnome-open "%s"' % filename)
        elif os.name=='nt':
            os.system('"%s"&exit' % filename)

        md4 = MD4.new(open(filename, 'rb').read())
        hash = md4.hexdigest() # New hash.
        del md4

        if old_hash != hash:
            qtMsg = QtGui.QMessageBox.warning(self, 'Save changes ? ...',
                'File "%s" was changed! Save changes ?' % self.buttons_selected, 'Yes', 'No')
            if qtMsg == 0: # Clicked yes.
                self.b.AddFile(filename)

        os.remove(filename) # Del file.
        dirs = glob.glob(os.getenv('temp') + '/' + '__*py*__')

        try:
            # Del all temp folders.
            for dir in dirs:
                shutil.rmtree(dir)
        except:
            pass
        #


    def on_copy(self):
        #
        qtBS = self.buttons_selected # Selected button.
        qtMsg = QtGui.QMessageBox.question(self, 'Copy file ? ...',
            'Are you sure you want to copy "%s" ?' % qtBS, 'Yes', 'No')

        if qtMsg == 0: # Clicked yes.
            ret = self.b.CopyIntoNew(fname=qtBS, version=0, new_fname='copy of '+qtBS)
            if ret == 0: # If Briefcase returns 0, create new button.
                vInfo = self.b.FileStatistics(qtBS)
                self.create_button('copy of ' + qtBS, vInfo['lastFileSize'], vInfo['versions'])
                self.fRefresh()
            else:
                QtGui.QMessageBox.critical(self, 'Error on copy',
                    '<br>Could not copy file ! Invalid file name, or file name exists !<br>')

        del qtBS, qtMsg
        #


    def on_delete(self):
        #
        qtBS = self.buttons_selected # Selected button.
        qtMsg = QtGui.QMessageBox.warning(self, 'Delete file ? ...',
            'Are you sure you want to delete "%s" ?' % qtBS, 'Yes', 'No')

        if qtMsg == 0: # Clicked yes.
            ret = self.b.DelFile(fname=qtBS, version=0)
            if ret == 0: # If Briefcase returns 0, delete the button.
                self.buttons[qtBS].close()
                del self.buttons[qtBS]
                self.fRefresh()
            else:
                QtGui.QMessageBox.critical(self, 'Error on delete',
                    '<br>Could not delete file ! Invalid file name !<br>')

        del qtBS, qtMsg
        #


    def on_rename(self):
        #
        qtBS = self.buttons_selected # Selected button.
        qtTxt, qtMsg = QtGui.QInputDialog.getText(self, 'Rename file ? ...',
            'New name :', QtGui.QLineEdit.Normal, qtBS)

        # Text becomes Lower Python String.
        qtTxt = str(qtTxt.toUtf8())

        if qtMsg and qtTxt: # Clicked yes and text exists.
            # Call Briefcase Rename function.
            ret = self.b.RenFile(fname=qtBS, new_fname=qtTxt)

            if ret == 0:

                vInfo = self.b.FileStatistics(qtTxt)
                # If Briefcase returns 0, button text and info.
                self.update_button(self.buttons[qtBS], qtTxt, vInfo['lastFileSize'], vInfo['versions'])
                # Pass the pointer to the new name.
                self.buttons[qtTxt] = self.buttons[qtBS]
                del self.buttons[qtBS]
                self.fRefresh()

            else:
                QtGui.QMessageBox.critical(self, 'Error on rename',
                    '<br>Could not rename file ! Invalid file name, or file name exists !<br>')

        del qtBS, qtTxt, qtMsg
        #


    def on_properties(self):
        #
        qtBS = self.buttons_selected # Selected button.
        prop = self.b.FileStatistics(fname=qtBS)

        if not prop:
            QtGui.QMessageBox.critical(self, 'Error on properties',
                '<br>Could not get statistics ! Invalid file name !<br>')
            return

        if not prop['labels']:
            prop['labels'] = '-'

        if prop['versions'] == 1:
            QtGui.QMessageBox.information(self, 'Properties for %s' % qtBS, '''
                <br><b>file name</b> : %(fileName)s
                <br><b>intern name</b> : %(internFileName)s
                <br><b>size</b> : %(lastFileSize)i
                <br><b>date</b> : %(lastFileDate)s
                <br><b>username</b> : %(lastFileUser)s
                <br><b>labels</b> : %(labels)s
                <br><b>versions</b> : %(versions)i<br>''' % prop)
        else:
            QtGui.QMessageBox.information(vCurrent, 'Properties for %s' % qtBS, '''
                <br><b>file name</b> : %(fileName)s
                <br><b>intern name</b> : %(internFileName)s
                <br><b>first fileSize</b> : %(firstFileSize)i
                <br><b>last fileSize</b> : %(lastFileSize)i
                <br><b>largest size</b> : %(biggestSize)i
                <br><b>first fileDate</b> : %(firstFileDate)s
                <br><b>last fileDate</b> : %(lastFileDate)s
                <br><b>first fileUser</b> : %(firstFileUser)s
                <br><b>last fileUser</b> : %(lastFileUser)s
                <br><b>labels</b> : %(labels)s
                <br><b>versions</b> : %(versions)i<br>''' % prop)

        del qtBS, prop
        #


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  F L O W   L A Y O U T
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class FlowLayout(QtGui.QLayout):

    '''
    Flow Layout defined in PyQt4 Layout examples.
    '''

    def __init__(self, parent=None, margin=0, spacing=-1):

        super(FlowLayout, self).__init__(parent)

        if parent is not None: self.setMargin(margin)
        self.setSpacing(spacing)
        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton, QtGui.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton, QtGui.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


import res_rc


if __name__=='__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# Eof()
