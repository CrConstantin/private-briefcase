# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    Website : http://private-briefcase.googlecode.com \n\
    This module contains Briefcase GUI class with all its functions. \n\
'''

# Standard libraries.
import os, sys

# External dependency.
from briefcase import *
from briefcase_GUI_tab import CustomTab
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
'''


class CustomDialog(QtGui.QDialog):

    def __init__(self, parent, title, whatsthis, action):
        #
        super(CustomDialog, self).__init__(parent)
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
        self.dir.setMinimumSize(QtCore.QSize(1, 22))
        self.dir.setFocus(0)
        #
        self.pwd = QtGui.QLineEdit(self)
        self.pwd.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.btn = QtGui.QPushButton(action, self)
        self.btn.setMinimumSize(QtCore.QSize(1, 20))
        self.btn.setDefault(True)
        #
        self.lbl = QtGui.QLineEdit(self)
        self.lbl.setMinimumSize(QtCore.QSize(1, 22))
        self.lbl.hide()
        #
        # Labels.
        self.browseL = QtGui.QLabel('File', self)
        self.pwdL = QtGui.QLabel('Password', self)
        self.lblL = QtGui.QLabel('Labels', self)
        self.lblL.hide()
        #
        self.browse.clicked.connect(self.Browse)
        self.btn.clicked.connect(self.Exit)
        #
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.browseL, 1, 1, 1, 1)
        layout.addWidget(self.dir, 1, 2, 1, 5)
        layout.addWidget(self.browse, 1, 7, 1, 1)
        layout.addWidget(self.pwdL, 2, 1, 1, 1)
        layout.addWidget(self.pwd, 2, 2, 1, 6)
        layout.addWidget(self.lblL, 3, 1, 1, 1)
        layout.addWidget(self.lbl, 3, 2, 1, 6)
        layout.addWidget(self.btn, 4, 1, 1, 7)
        self.setLayout(layout)
        #

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
        del f

    def Exit(self):
        self.done(1)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        #
        super(MainWindow, self).__init__(None)
        #
        global WStyle
        self.tabs = {}
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
        self.actionHelp.triggered.connect(self.on_help)
        toolBar.addAction(self.actionHelp)
        self.actionAbout.triggered.connect(self.on_about)
        toolBar.addAction(self.actionAbout)
        #
        # Default file for command line access.
        try:
            self.default_file = sys.argv[1]
            self.on_open()
        except:
            self.default_file = ''
        #

    def _close_tab(self, index):
        #
        vCurrent = self.tabWidget.currentWidget()
        self.tabWidget.removeTab(index) # Remove from tab widget.
        vCurrent.__del__() # Release resources.
        #
        if not self.tabWidget.count():
            self.actionAddFiles.setVisible(False)
            self.actionExport.setVisible(False)
            self.actionDBProperties.setVisible(False)
            self.actionShowLog.setVisible(False)
        #

    # Triggered functions.
    def on_new(self):
        #
        dlg = CustomDialog(self.centralwidget, 'Create new briefcase file', 'Browse to the '\
            'directory where you want to create the new Briefcase file. You can set a default '\
            'password, but password is optional.', 'Create !')
        dlg.exec_()
        dir, pwd = str(dlg.dir.text()), str(dlg.pwd.text())
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        #
        tab_name = os.path.split(dir.title())[1]
        new_tab = CustomTab(self, tab_name, dir, pwd)
        self.tabWidget.addTab(new_tab, tab_name) # Inject THIS into parent tab widget.
        self.tabWidget.setCurrentWidget(new_tab) # Must enable new tab.
        #
        self.actionAddFiles.setVisible(True)
        self.actionExport.setVisible(True)
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
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        #
        tab_name = os.path.split(dir.title())[1]
        # Check for existance in all tabs.
        for vTab in range(self.tabWidget.count()):
            if self.tabWidget.tabText(vTab) == tab_name:
                QtGui.QMessageBox.warning(self.centralwidget, 'Will not Open', '<br>"%s" is already open!<br>' % tab_name)
                return
        #
        try:
            b = Briefcase(dir, pwd) # Briefcase for current tab.
        except:
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Open', '<br>Error! Wrong password!<br>')
            return
        #
        new_tab = CustomTab(self, tab_name, dir, pwd)
        self.tabWidget.addTab(new_tab, tab_name) # Inject THIS into parent tab widget.
        self.tabWidget.setCurrentWidget(new_tab) # Must enable new tab.
        new_tab.fRefresh()
        #
        self.actionAddFiles.setVisible(True)
        self.actionExport.setVisible(True)
        self.actionDBProperties.setVisible(True)
        self.actionShowLog.setVisible(True)
        #

    def on_join(self):
        #
        print( 'Triggered JOIN !' )
        # Some code goes in here...
        #

    def on_add(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        dlg = CustomDialog(self.centralwidget, 'Add files to briefcase', 'Select the files to be '
            'added. You can specify a password and one or more labels, separated by ";".', 'Add !')
        dlg.browseL.setText('Files')
        dlg.lbl.show()
        dlg.lblL.show()
        dlg.resize(300, 130)
        dlg.setMinimumSize(QtCore.QSize(300, 130))
        dlg.setMaximumSize(QtCore.QSize(300, 130))
        dlg.exec_()
        # Selected files are separated by ";" so must be exploded.
        dir = str(dlg.dir.text()).split(';')
        # If not password was selected, default password must be used, so pwd -> 1.
        pwd = str(dlg.pwd.text())
        if not pwd: pwd = 1
        # Save labels, transformed into python string.
        lbl = str(dlg.lbl.text())
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        #
        for elem in dir:
            vCurrent.b.AddFile(elem, pwd, lbl)
            file_name = os.path.split(elem)[1]
            vCurrent._create_button(file_name)
        #
        vCurrent.fRefresh()
        #

    def on_export(self):
        #
        f = QtGui.QFileDialog()
        input = f.getExistingDirectory(self.centralwidget, 'Select a folder to export into :',
            os.getcwd())
        if input:
            self.tabWidget.currentWidget().b.ExportAll(str(input))
            QtGui.QMessageBox.information(self.centralwidget, 'Export', 'Export finished !')
        #

    def on_db_properties(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        prop = self.tabWidget.currentWidget().b.Info()
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
            '<br><b>Copyright © 2009-2010</b> : Cristi Constantin. All rights reserved.<br>'
            '<b>Website</b> : http://private-briefcase.googlecode.com<br>')
        #


import res_rc

app = QtGui.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Eof()
