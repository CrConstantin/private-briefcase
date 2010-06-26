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
        self.parent = parent
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
        parent.actionAddFiles.setVisible(True)
        parent.actionExport.setVisible(True)
        parent.actionDBProperties.setVisible(True)
        parent.actionShowLog.setVisible(True)
        #
        for file_name in self.b.GetFileList(): # Populating with buttons.
            self._create_button(file_name)
        #

    def __del__(self):
        #
        print('Closing custom tab.')
        #
        self.parent = None
        self.buttons = None
        self.buttons_selected = None
        del self.b
        #

    def _create_button(self, file_name):
        '''
        Each button represents a file from the briefcase.
        Create a new button and add in the layout.
        '''
        #
        pushButton = QtGui.QPushButton(self)
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
