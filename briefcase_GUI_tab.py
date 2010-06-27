# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    Website : http://private-briefcase.googlecode.com \n\
    This module contains Briefcase tab class with all its functions. \n\
'''

# Standard libraries.
import os, sys

# External dependency.
from briefcase import *
from PyQt4 import QtCore, QtGui

BUTTON_W = 100
BUTTON_H = 64


class CustomTab(QtGui.QScrollArea):
    '''
    This widget is specially designed for my Briefcase GUI.
    It will most certainly not work with other parents.
    '''
    def __init__(self, parent, tab_name, database, password):
        #
        super(CustomTab, self).__init__(parent)
        #
        # Object name is sometimes used.
        self.setObjectName(tab_name)
        # Contents widget will hold the buttons.
        self.scrollAreaContents = QtGui.QWidget(self)
        # Add contents to scrollarea.
        self.setWidget(self.scrollAreaContents)
        # Grid layout.
        self.mainLayout = QtGui.QGridLayout(self.scrollAreaContents)
        # Buttons.
        self.buttons = {}
        self.buttons_selected = None
        # Briefcase instance.
        self.b = Briefcase(database, password)
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
        for file_name in self.b.GetFileList(): # Populating with buttons.
            self._create_button(file_name)
        #

    def __del__(self):
        #
        print('Closing custom tab.')
        #
        del self.buttons
        del self.buttons_selected
        del self.b
        #

    def _create_button(self, file_name):
        '''
        Each button represents a file from the briefcase.
        Create a new button and add in the layout.
        '''
        #
        pushButton = QtGui.QPushButton() # Parent None.
        pushButton.resize(QtCore.QSize(BUTTON_W, BUTTON_H))
        pushButton.setFlat(True)
        pushButton.setObjectName(file_name) # Full file name.
        pushButton.setStatusTip(file_name)
        if len(file_name)>12:
            fname = file_name[:12]+' (...)'
        else:
            fname = file_name
        pushButton.setText(fname) # Short file name.
        # Style sheet.
        pushButton.setStyleSheet('''
        QPushButton {
            background-image: url(Extensions/Default.png);'
            background-position: top center;
            border-style: outset;
            border: 1px solid #666;
            border-radius: 3px;
            padding: 4px;
            text-align: center bottom;
            color: #001;
            font: 10px; }
        QPushButton:pressed { border-style: inset; }''')
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # Connect events.
        pushButton.clicked.connect(self.parent.double_click)
        pushButton.customContextMenuRequested.connect(self.parent.right_click)
        # Add button to dictionary.
        self.buttons[file_name] = pushButton
        pushButton.show()
        #

    def fRefresh(self):
        '''
        Refresh buttons.
        This function is used when opening, adding, renaming or deleting buttons.
        '''
        #
        vButtonsW = (self.width()-4) // BUTTON_W
        vRow = 1
        vCol = 1
        #
        for vButton in sorted( self.buttons, key=lambda k: k.lower() ):
            # Add button in layout.
            self.mainLayout.addWidget(self.buttons[vButton], vRow, vCol)
            # If current column is bigger than number of buttons per line.
            if vCol >= vButtonsW:
                # Go to next line.
                vRow += 1
                vCol = 1
            else:
                vCol += 1
        #
        if vRow == 1:
            self.scrollAreaContents.setMinimumSize(QtCore.QSize(vCol*(BUTTON_W+2), BUTTON_H+2))
            self.scrollAreaContents.setMaximumSize(QtCore.QSize(vCol*(BUTTON_W+2), BUTTON_H+2))
        else:
            self.scrollAreaContents.setMinimumSize(QtCore.QSize(vButtonsW*(BUTTON_W+3), vRow*(BUTTON_H+2)))
        #



    def double_click(self):
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

    def right_click(self):
        #
        vPos = self.cursor().pos()
        self.buttons_selected = str(self.childAt(self.mapFromGlobal(vPos)).objectName()) # Selected button.
        self.qtMenu.exec_(vPos) # Execute menu.
        #

    def on_view(self):
        #
        # If caller is an action.
        if type(self.sender()) == type(QtGui.QPushButton()):
            self.b.ExportFile(str(self.sender().objectName()), execute=True)
        # If caller is a button.
        else:
            self.b.ExportFile(self.buttons_selected, execute=True)
        #

    def on_edit(self):
        #
        self.b.ExportFile(self.buttons_selected, execute=True)
        #

    def on_copy(self):
        #
        qtBS = self.buttons_selected # Selected button.
        qtMsg = QtGui.QMessageBox.question(self.centralwidget, 'Copy file ? ...',
            'Are you sure you want to copy "%s" ?' % qtBS, 'Yes', 'No')
        if qtMsg == 0: # Clicked yes.
            ret = self.b.CopyIntoNew(fname=qtBS, version=0, new_fname='copy of '+qtBS)
            if ret == 0: # If Briefcase returns 0, create new button.
                self._create_button('copy of '+qtBS)
                self.fRefresh()
        del qtBS, qtMsg
        #

    def on_delete(self):
        #
        qtBS = self.buttons_selected # Selected button.
        qtMsg = QtGui.QMessageBox.warning(self.centralwidget, 'Delete file ? ...',
            'Are you sure you want to delete "%s" ?' % qtBS, 'Yes', 'No')
        if qtMsg == 0: # Clicked yes.
            ret = self.b.DelFile(fname=qtBS, version=0)
            if ret == 0: # If Briefcase returns 0, delete the button.
                self.buttons[qtBS].close()
                del self.buttons[qtBS]
                self.fRefresh()
        del qtBS, qtMsg
        #

    def on_rename(self):
        #
        qtBS = self.buttons_selected # Selected button.
        qtTxt, qtMsg = QtGui.QInputDialog.getText(self.centralwidget, 'Rename file ? ...',
            'New name :', QtGui.QLineEdit.Normal, qtBS)
        if qtMsg and str(qtTxt): # Clicked yes and text exists.
            ret = self.b.RenFile(fname=qtBS, new_fname=str(qtTxt))
            if ret == 0: # If Briefcase returns 0, rename the button.
                self.buttons[qtBS].setObjectName(qtTxt)
                self.buttons[qtBS].setStatusTip(qtTxt)
                #
                if len(qtTxt)>12:
                    fname = qtTxt[:12]+' (...)'
                else:
                    fname = qtTxt
                self.buttons[qtBS].setText(fname)
                # Pass the pointer to the new name.
                self.buttons[str(qtTxt)] = self.buttons[qtBS]
                del self.buttons[qtBS]
                self.fRefresh()
        del qtBS, qtTxt, qtMsg
        #

    def on_properties(self):
        #
        qtBS = self.buttons_selected # Selected button.
        prop = self.b.FileStatistics(fname=qtBS)
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
        del qtBS, prop
        #



    def fDuplicate(self):
        '''
        Duplicate one file.
        '''
        pass

    def fRename(self):
        '''
        Rename one file.
        '''
        pass

#

# Eof()
