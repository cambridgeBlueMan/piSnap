# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testButtons.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
"""
preferences.ui is a file initially created in QtDesigner.  This file is then translated into
a single Python class called Ui_preferences by pyuic5.  
"""
from preferences import *
from picamera import PiCamera
camera = PiCamera
"""
The Code_preferences class is to define all the logic and functions for the program to operate
Most of these functions will already have been referenced in the designer file via signal/slot connections

Note that this class has to inherit from the relevant parent class. In this case a QDialog,
but could as easily be a QMainMenu

remember that this means that this is a Dialog window or other window with some added code/methods

This Dialog window with added code will be passed to an instance of the automatically
created Designer class. This designer created class has methods to draw the various widgets and associate them 
with the passed instance of the code/widget class
"""
class Code_preferences(QtWidgets.QDialog):


    def __init__(self):
        super().__init__()
    def getDefaultFilePath(*args):
        # the stuff on the right hand side of the "=" in the line below draws an open file dialog
        # "Set Default File Directory" is the name of the dialog, and 
        # when this is closed with a directory selected then that directory name will be stored in the variable
        # "directory" which is on the left hand side of the "="
        
        directory = QtWidgets.QFileDialog.getExistingDirectory(args[0], "Set Default File Directory", ui.defaultFilePath.text())
        
        # now set the defaultFilePath label in the user interface to the chosen directory
        
        ui.defaultFilePath.setText(directory)
        
    def getDefaultPhotoPath(*args):
        # when finished you can delete the following line
        print ("in getDefaultPhotoPath")
        
        # copy the block of code from getDefaultFilePath function to here and make the appropriate changes to the
        # dialog name and the original default directory
         
    def getDefaultVideoPath(*args):
        print ("in getvideo")
        
    """
Add the additional methods/ data structures etc here
    def myClick(*args):
        print(args[0].sender().property("buttonVal"))
    


    """
class Data_preferences(object):
    def __init__(self):
        super().__init__()
    def addStuff(self,ui):
        ui.comboBox.addItems(('jpeg', 'png', 'gif', 'bmp', 'yuv', 'rgb', 'rgba', 'bgr', 'bgra', 'raw')) 
if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = QtWidgets.QApplication(sys.argv)
    # instantiate an object containing the logic code
    preferences = Code_preferences()
    # instantiate an object from the imported Ui_preferences class
    ui = Ui_preferences()
    # pass a reference to the preferences object to the setupUi method of the Ui_preferences instance ui
    ui.setupUi(preferences)
    addData = Data_preferences()
    addData.addStuff(ui)
    # show it!
    preferences.show()
    sys.exit(app.exec_())


