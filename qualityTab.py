from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg 
from PyQt5 import QtWidgets as qtw

# insert appropriate names here
from qualityTabGui import Ui_Form
#
from psSettings import PSSettings

from picamera import PiCamera
from time import sleep
import sys
import datetime
import json

class QualityTab(qtw.QWidget):

    def __init__(self, camvals, camera):
        super().__init__()
        # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        self.comboItemsAdded = False
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals
        self.camera = camera
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # add combo box items
        self.comboItemsAdded = self.addItemsToCombos(self)
        
        self.applySettings()

    def addItemsToCombos(*args):
        args[0].ui.audioBitRate.addItems(["16", "24"])
        args[0].ui.audioSampleRate.addItems(["44.1kz", "48kz"])
        args[0].ui.audioFileFormat.addItems(["wav", "aiff"])
        args[0].ui.videoBitRate.addItems(["0", "17000000"])
        args[0].ui.videoQuality.addItems(["10", "20", "25", "30", "35", "40"])
        return True

    def applySettings(self):
        if self.comboItemsAdded == True:
            #for each key in the settings dictionery 
            self.ui.audioBitRate.setCurrentText(str(self.camvals["audioBitRate"]))
            self.ui.videoQuality.setCurrentText(str(self.camvals["videoQuality"]))
            self.ui.audioFileFormat.setCurrentText(str(self.camvals["audioFileFormat"]))                
 
    def setAudioBitRate(self):
        pass #print(self)
        
    def setAudioSampleRate(self):
        pass #print(self)

    def setAudioFileFormat(self):
        pass #print(self)

    def doMux(self):
        pass #print(self)

    def isAudioActive(self):
        pass #print(self)

    def setVideoBitRate(self):
        pass #print(self)
    def setVideoQuality(self):
        pass #print(self)
 

#######################################################################################
    #                           END OF CLASS
#######################################################################################
if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = qtw.QApplication(sys.argv)
    # get the settings
    camera = PiCamera()
        # pass the main window and camera objects to a settings object
    # settings = CameraSettings(camera)
    # instantiate an object containing the logic code
    qualityTab = QualityTab(None)
    qualityTab.show()
    sys.exit(app.exec_())


