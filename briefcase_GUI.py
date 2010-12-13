# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    Website : http://private-briefcase.googlecode.com \n\
    This module contains Briefcase GUI class with all its functions. \n\
'''

# Standard libraries.
import os, sys
import glob
import shutil

# External dependency.
from briefcase import *
from briefcase_GUI_tab import CustomTab
from PyQt4 import QtCore, QtGui
from Crypto.Hash import MD4


class CustomDialog(QtGui.QDialog):

    def __init__(self, parent, title, whatsthis, action):
        #
        super(CustomDialog, self).__init__(parent)
        self.title = title
        self.action = action
        self.setWindowTitle(title)
        self.setWhatsThis(whatsthis)
        #
        if self.action == 'Open !':
            self.resize(300, 100)
            self.setMinimumSize(QtCore.QSize(290, 90))
            self.setMaximumSize(QtCore.QSize(310, 110))
        else:
            self.resize(300, 130)
            self.setMinimumSize(QtCore.QSize(290, 120))
            self.setMaximumSize(QtCore.QSize(310, 140))
        #
        # Buttons.
        self.browse = QtGui.QPushButton('...', self)
        self.browse.setMaximumSize(QtCore.QSize(20, 20))
        self.dir = QtGui.QLineEdit(self)
        self.dir.setMinimumSize(QtCore.QSize(20, 5))
        self.dir.setFocus(0)
        #
        # Password field.
        self.pwd = QtGui.QLineEdit(self)
        self.pwd.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.pwd2 = QtGui.QLineEdit(self)
        self.pwd2.setMinimumSize(QtCore.QSize(1, 22))
        self.pwd2.setEchoMode(QtGui.QLineEdit.Password)
        if self.action != 'Create !':
            self.pwd2.hide()
        #
        # Action button.
        self.btn = QtGui.QPushButton(action, self)
        self.btn.setMinimumSize(QtCore.QSize(1, 20))
        self.btn.setDefault(True)
        #
        # Labels.
        self.lbl = QtGui.QLineEdit(self)
        self.lbl.setMinimumSize(QtCore.QSize(1, 22))
        self.browseL = QtGui.QLabel('File', self)
        self.pwdL = QtGui.QLabel('Password', self)
        self.lblL = QtGui.QLabel('Labels', self)
        if self.action != 'Add !':
            self.lbl.hide()
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
        layout.addWidget(self.pwd2, 3, 2, 1, 6)
        layout.addWidget(self.lblL, 4, 1, 1, 1)
        layout.addWidget(self.lbl, 4, 2, 1, 6)
        layout.addWidget(self.btn, 5, 1, 1, 7)
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
        # Some settings.
        self.resize(800, 600)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('CleanLooks'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        self.setObjectName('MainWindow')
        self.setWindowTitle('Private Briefcase GUI')
        self.setWindowIcon(QtGui.QIcon('PB.ico'))
        #
        # Set central widget.
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName('centralWidget')
        self.setCentralWidget(self.centralwidget)
        #
        # Set central layout.
        mainLayout = QtGui.QVBoxLayout(self.centralwidget)
        #
        # Set status bar.
        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName('statusBar')
        self.setStatusBar(statusbar)
        #
        # Set tab widget.
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName('tabWidget')
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabCloseRequested.connect(self._close_tab)
        mainLayout.addWidget(self.tabWidget)
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
        #
        # Button actions.
        actionView = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-View.png')), 'View', self)
        actionEdit = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Edit.png')), 'Edit', self)
        actionCopy = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Copy.png')), 'Copy', self)
        actionDelete = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Delete.png')), 'Delete', self)
        actionRename = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Rename.png')), 'Rename', self)
        actionProperties = QtGui.QAction(QtGui.QIcon(QtGui.QPixmap(':/root/Symbols/Symbol-Properties.png')), 'Properties', self)
        #
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
        #
        # Setup double click timer.
        self.dblClickTimer = QtCore.QTimer()
        self.dblClickTimer.setSingleShot(True)
        self.dblClickTimer.setInterval(500)
        #
        # Default file for command line access.
        default_file = sys.argv[1:2]
        #
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
        self.tabWidget.removeTab(index) # Remove from tab widget.
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

    # Triggered functions.
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
        #
        tab_name = os.path.split(dir.title())[1]
        new_tab = CustomTab(self, tab_name, dir, pwd)
        self.tabWidget.addTab(new_tab, ' [ '+tab_name+' ] ') # Add tab to tab widget.
        self.tabWidget.setCurrentWidget(new_tab) # Must enable new tab.
        #
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
        #
        dlg.exec_()
        dir, pwd = str(dlg.dir.text()), str(dlg.pwd.text())
        if self.default_file and not dlg.result(): sys.exit(0) # If open with ARGS and canceled, exit.
        if not dir or not dlg.result(): return # If no file was selected, or the dialog was canceled.
        del dlg
        if not pwd: pwd = False # If no password, password is Null.
        #
        if not os.path.exists(dir):
            QtGui.QMessageBox.warning(self.centralwidget, 'Will not Open', '<br>"%s" doesn\'t exist !<br>' % dir)
            return
        #
        tab_name = os.path.split(dir.title())[1]
        # Check for existance in all tabs.
        for vTab in range(self.tabWidget.count()):
            if self.tabWidget.tabText(vTab) == tab_name:
                QtGui.QMessageBox.warning(self.centralwidget, 'Will not Open', '<br>"%s" is already open !<br>' % tab_name)
                return
        #
        try:
            b = Briefcase(dir, pwd) # Briefcase for current tab.
        except:
            QtGui.QMessageBox.critical(self.centralwidget, 'Error on Open', '<br>Error ! Wrong password !<br>')
            return
        #
        new_tab = CustomTab(self, tab_name, dir, pwd)
        self.tabWidget.addTab(new_tab, ' [ '+tab_name+' ] ') # Add tab to tab widget.
        self.tabWidget.setCurrentWidget(new_tab) # Must enable new tab.
        new_tab.fRefresh()
        #
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
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        dlg = CustomDialog(vCurrent, 'Add files to briefcase', 'Select the files to be '
            'added. You can specify a password and one or more labels, separated by ";".', 'Add !')
        dlg.browseL.setText('Files')
        dlg.exec_()
        # Selected files are separated by ";" so must be exploded.
        dir = str(dlg.dir.text()).split(';')
        pwd = str(dlg.pwd.text())
        if not pwd: pwd = 1 # If password is null, use database default value.
        lbl = str(dlg.lbl.text()) # Labels.
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
        dlg.resize(480, self.height())
        #
        table = QtGui.QTableWidget(dlg)
        table.setColumnCount(2)
        table.setRowCount(len(logs))
        table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Date'))
        table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('Message'))
        table.setColumnWidth(0, 117)
        table.setColumnWidth(1, 280)
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

    def on_double_click(self):
        #
        # If after receiving the first click, the timer isn't running, start the timer and return.
        if not self.dblClickTimer.isActive():
            self.dblClickTimer.start()
            return
        # If timer is running and hasn't timed out, the second click occured within timer interval.
        else:
            self.on_view()
            self.dblClickTimer.stop() # Stop timer so next click can start it again.
            return
        #

    def on_right_click(self):
        #
        vPos = self.cursor().pos()
        # Current tab.
        vCurrent = self.tabWidget.currentWidget()
        # Selected button to string.
        button_selected = str(self.childAt(self.mapFromGlobal(vPos)).objectName())
        vCurrent.buttons_selected = button_selected.lower()
        # Execute menu.
        self.qtMenu.exec_(vPos)
        #

    def on_view(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        #
        if type(self.sender()) == type(QtGui.QPushButton()): # If caller is an action.
            vFile = str(self.sender().objectName())
        else: # If caller is a button.
            vFile = vCurrent.buttons_selected
        #
        vRes = vCurrent.b.ExportFile(vFile, execute=True)
        #
        for i in range(3):
            if vRes != -1:
                break
            else:
                qtTxt, qtMsg = QtGui.QInputDialog.getText(None, 'Enter password',
                    'You must enter file passord :', QtGui.QLineEdit.Password)
                qtTxt = str(qtTxt.toUtf8())
                if qtMsg:
                    vRes = vCurrent.b.ExportFile(vFile, qtTxt, execute=True)
                else:
                    return
        #
        if vRes == -1: # If password is still wrong.
                QtGui.QMessageBox.critical(vCurrent, 'Error on view',
                    '<br>Wrong password 3 times !<br>')
        del vFile, vRes, vCurrent
        #

    def on_edit(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        temp_dir = os.getenv('temp') + '__temp_py__'
        filename = temp_dir + '/' + vCurrent.buttons_selected
        #
        try:
            os.mkdir(temp_dir)
        except:
            print('Cannot create temp file!')
        #
        # Create temp file and return file hash.
        old_hash = vCurrent.b.ExportFile(fname=vCurrent.buttons_selected, path=temp_dir, execute=False)
        #
        for i in range(3):
            if old_hash != -1:
                break
            else:
                qtTxt, qtMsg = QtGui.QInputDialog.getText(None, 'Enter password',
                    'You must enter file passord :', QtGui.QLineEdit.Password)
                qtTxt = str(qtTxt.toUtf8())
                if qtMsg:
                    old_hash = vCurrent.b.ExportFile(fname=vCurrent.buttons_selected, password=qtTxt, path=temp_dir, execute=False)
                else:
                    return
        #
        if old_hash == -1: # If password is still wrong.
                QtGui.QMessageBox.critical(vCurrent, 'Error on edit',
                    '<br>Wrong password 3 times !<br>')
                return
        #
        # Execute.
        if os.name=='posix':
            os.system('gnome-open "%s"' % filename)
        elif os.name=='nt':
            os.system('"%s"&exit' % filename)
        #
        md4 = MD4.new(open(filename, 'rb').read())
        hash = md4.hexdigest() # New hash.
        del md4
        #
        if old_hash != hash:
            qtMsg = QtGui.QMessageBox.warning(vCurrent, 'Save changes ? ...',
                'File "%s" was changed! Save changes ?' % vCurrent.buttons_selected, 'Yes', 'No')
            if qtMsg == 0: # Clicked yes.
                vCurrent.b.AddFile(filename)
        #
        os.remove(filename) # Del file.
        dirs = glob.glob(os.getenv('temp') + '/' + '__*py*__')
        try:
            for dir in dirs:
                shutil.rmtree(dir) # Del all temp folders.
        except: pass
        del dirs
        #

    def on_copy(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        qtBS = vCurrent.buttons_selected # Selected button.
        qtMsg = QtGui.QMessageBox.question(vCurrent, 'Copy file ? ...',
            'Are you sure you want to copy "%s" ?' % qtBS, 'Yes', 'No')
        if qtMsg == 0: # Clicked yes.
            ret = vCurrent.b.CopyIntoNew(fname=qtBS, version=0, new_fname='copy of '+qtBS)
            if ret == 0: # If Briefcase returns 0, create new button.
                vCurrent._create_button('copy of ' + qtBS)
                vCurrent.fRefresh()
            else:
                QtGui.QMessageBox.critical(vCurrent, 'Error on copy',
                    '<br>Could not copy file ! Invalid file name, or file name exists !<br>')
        del vCurrent, qtBS, qtMsg
        #

    def on_delete(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        qtBS = vCurrent.buttons_selected # Selected button.
        qtMsg = QtGui.QMessageBox.warning(vCurrent, 'Delete file ? ...',
            'Are you sure you want to delete "%s" ?' % qtBS, 'Yes', 'No')
        if qtMsg == 0: # Clicked yes.
            ret = vCurrent.b.DelFile(fname=qtBS, version=0)
            if ret == 0: # If Briefcase returns 0, delete the button.
                vCurrent.buttons[qtBS].close()
                del vCurrent.buttons[qtBS]
                vCurrent.fRefresh()
            else:
                QtGui.QMessageBox.critical(vCurrent, 'Error on delete',
                    '<br>Could not delete file ! Invalid file name !<br>')
        del vCurrent, qtBS, qtMsg
        #

    def on_rename(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        qtBS = vCurrent.buttons_selected # Selected button.
        qtTxt, qtMsg = QtGui.QInputDialog.getText(vCurrent, 'Rename file ? ...',
            'New name :', QtGui.QLineEdit.Normal, qtBS)
        # Text becomes Lower Python String.
        qtTxt = str(qtTxt.toUtf8()).lower()
        if qtMsg and qtTxt: # Clicked yes and text exists.
            # Call Briefcase Rename function.
            ret = vCurrent.b.RenFile(fname=qtBS, new_fname=qtTxt)
            if ret == 0: # If Briefcase returns 0, rename the button.
                vCurrent.buttons[qtBS].setObjectName(qtTxt)
                vCurrent.buttons[qtBS].setStatusTip(qtTxt)
                #
                if len(qtTxt) > 12:
                    fname = qtTxt[:12] + ' (...)'
                else:
                    fname = qtTxt
                vCurrent.buttons[qtBS].setText(fname)
                # Pass the pointer to the new name.
                vCurrent.buttons[qtTxt] = vCurrent.buttons[qtBS]
                del vCurrent.buttons[qtBS]
                vCurrent.fRefresh()
            else:
                QtGui.QMessageBox.critical(vCurrent, 'Error on rename',
                    '<br>Could not rename file ! Invalid file name, or file name exists !<br>')
        del vCurrent, qtBS, qtTxt, qtMsg
        #

    def on_properties(self):
        #
        vCurrent = self.tabWidget.currentWidget() # Current tab.
        qtBS = vCurrent.buttons_selected # Selected button.
        prop = vCurrent.b.FileStatistics(fname=qtBS)
        #
        if not prop:
            QtGui.QMessageBox.critical(vCurrent, 'Error on properties',
                '<br>Could not get statistics ! Invalid file name !<br>')
            return
        #
        if not prop['labels']:
            prop['labels'] = '-'
        #
        if prop['versions'] == 1:
            QtGui.QMessageBox.information(vCurrent, 'Properties for %s' % qtBS, '''
                <br><b>File Name</b> : %(fileName)s
                <br><b>intern FileName</b> : %(internFileName)s
                <br><b>FileSize</b> : %(lastFileSize)i
                <br><b>FileDate</b> : %(lastFileDate)s
                <br><b>FileUser</b> : %(lastFileUser)s
                <br><b>labels</b> : %(labels)s
                <br><b>versions</b> : %(versions)i<br>''' % prop)
        else:
            QtGui.QMessageBox.information(vCurrent, 'Properties for %s' % qtBS, '''
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
        del vCurrent, qtBS, prop
        #


import res_rc

app = QtGui.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())

#Eof()
