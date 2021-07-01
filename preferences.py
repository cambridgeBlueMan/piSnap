from PyQt5 import QtCore, QtGui, QtWidgets
from gui.preferencesGui import *
from picamera import PiCamera
import json
camera = PiCamera
#TODO Make this dailog box an addition to the tabbed widget
#TODO aslteratively keep this where it is, but widen the dialog box so it is big
# enough to hold the full path
# TODO what happens if the external disk is missing and the files pointed to are on there
class Preferences(QtWidgets.QDialog):
    def __init__(self, win, camvals, camera):
        super().__init__()
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals

        if camera == None:
            self.camera = PiCamera()
        else:
            self.camera = camera
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.defaultFilePath.setText(self.camvals["defaultFilePath"]) 
        self.ui.defaultPhotoPath.setText(self.camvals["defaultPhotoPath"]) 
        self.ui.defaultVideoPath.setText(self.camvals["defaultVideoPath"]) 

    def setDefaultFilePath(self):        
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Set Default File Directory", self.ui.defaultFilePath.text())
        # directory returns "" if dialog is cancelled
        if directory != "":
            self.ui.defaultFilePath.setText(directory)
        
    def setDefaultPhotoPath(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Set Default Photo Directory", self.ui.defaultPhotoPath.text())
        if directory != "":
            self.ui.defaultPhotoPath.setText(directory)
             
    def setDefaultVideoPath(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Set Default Video Directory", self.ui.defaultVideoPath.text())
        if directory != "":    
            self.ui.defaultVideoPath.setText(directory)

    def doAccepted(self):
        self.camvals["defaultFilePath"]=self.ui.defaultFilePath.text()
        self.camvals["defaultPhotoPath"]=self.ui.defaultPhotoPath.text()
        self.camvals["defaultVideoPath"]=self.ui.defaultVideoPath.text()

    def doRejected(self):
        pass
        
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
    preferences = Preferences()
    # instantiate an object from the imported Ui_preferences class
    ui = Ui_preferences()
    # pass a reference to the preferences object to the setupUi method of the Ui_preferences instance ui
    ui.setupUi(preferences)
    addData = Data_preferences()
    addData.addStuff(ui)
    # show it!
    preferences.show()
    sys.exit(app.exec_())