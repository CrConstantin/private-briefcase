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
        self.BUTTON_W = 98
        self.BUTTON_H = 64
        self.BAR_HEIGHT = 30
        #
        # Object name is sometimes used.
        self.setObjectName(tab_name)
        # Contents widget will hold the buttons.
        self.scrollAreaContents = QtGui.QWidget(self)
        self.setWidget(self.scrollAreaContents)
        # Buttons.
        self.buttons = {}
        self.buttons_selected = None
        # Briefcase instance.
        self.b = Briefcase(database, password)
        #
        for file_name in self.b.GetFileList(): # Populating with buttons.
            self._create_button(file_name)
        #

    def closeEvent(self, event):
        #
        del self.buttons
        del self.buttons_selected
        del self.parent
        del self.b
        #
        self.close()
        #

    def resizeEvent(self, event):
        #
        self.fRefresh()
        #

    def _create_button(self, file_name):
        '''
        Each button represents a file from the briefcase.
        Create a new button and add in the layout.
        '''
        #
        file_name = file_name.lower()
        pushButton = QtGui.QPushButton(self.scrollAreaContents)
        pushButton.setMinimumSize(QtCore.QSize(self.BUTTON_W, self.BUTTON_H))
        pushButton.setMaximumSize(QtCore.QSize(self.BUTTON_W, self.BUTTON_H))
        pushButton.resize(QtCore.QSize(self.BUTTON_W, self.BUTTON_H))
        pushButton.setFlat(True)
        pushButton.setObjectName(file_name) # Full file name.
        pushButton.setStatusTip(file_name)
        if len(file_name) > 12:
            fname = file_name[:12] + ' (...)'
        else:
            fname = file_name
        pushButton.setText(fname) # Short file name.
        # Style sheet.
        pushButton.setStyleSheet('''
        QPushButton {
            border-style: outset;
            border: 1px solid #666;
            border-radius: 5px;
            padding: 2px;
            margin: 0px;
            text-align: center bottom;
            color: #001;
            font: 10px;
            /* background-image: url(Extensions/Default.png);'
            background-position: top center; */
            }
        QPushButton:pressed { border-style: inset; }''')
        pushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # Connect events.
        pushButton.clicked.connect(self.parent.on_double_click)
        pushButton.customContextMenuRequested.connect(self.parent.on_right_click)
        # Add button to dictionary.
        self.buttons[file_name] = pushButton
        #

    def fRefresh(self):
        '''
        Refresh buttons.
        This function is used when opening, adding, renaming or deleting buttons.
        '''
        #
        self.vWidth = self.width()
        # ( Width - left buttons margin - scroll bar width ) / ( button width + button distance )
        vButtonsPerLine = (self.vWidth - 5 - self.BAR_HEIGHT) // (self.BUTTON_W + 5)
        #
        vRow = 0
        vCol = 0
        #
        for vButton in sorted( self.buttons, key=lambda k: k.lower() ):
            #
            self.buttons[vButton].move( 5+vCol*(self.BUTTON_W+5), self.BAR_HEIGHT+vRow*(self.BUTTON_H+5) )
            self.buttons[vButton].show()
            #
            # If current column is bigger than number of buttons per line.
            if vCol+1 >= vButtonsPerLine:
                # Go to next line.
                vRow += 1
                vCol = 0
            else:
                # Got to next column.
                vCol += 1
            #
        #
        # If Column is 0, Row was already incremented.
        if vCol == 0:
            pass
        else:
            vRow += 1
        #
        self.scrollAreaContents.setMinimumSize( self.vWidth-20, self.BAR_HEIGHT+vRow*(self.BUTTON_H+5) )
        self.scrollAreaContents.resize(         self.vWidth-20, self.BAR_HEIGHT+vRow*(self.BUTTON_H+5) )
        #


#

# Eof()
