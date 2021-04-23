from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg 
from PyQt5 import QtWidgets as qtw

from resolutionsTabGui import Ui_Form
from psSettings import PSSettings

from picamera import PiCamera
from time import sleep
import sys
import datetime
import json

class ResolutionsTab(qtw.QWidget):


    def __init__(self, camvals, camera):
        super().__init__()
        self.comboItemsAdded = False
        # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals
        self.camera = camera
        self.ui = Ui_Form() # makes the actual gui
        self.ui.setupUi(self)
        # add combo box items
        self.comboItemsAdded = self.addItemsToCombos(self)
        
        self.applySettings()

    def makedatastructures(self):
        resolutions = [
                    ('CGA', (320,200)),         ('QVGA', (320,240)),
                    ('VGA', (640,480)),         ('PAL', (768,576)),
                    ('480p', (720,480)),        ('576p', (720,576)),
                    ('WVGA', (800,480)),        ('SVGA', (800,600)),
                    ('FWVGA', (854,480)),       ('WSVGA', (1024,600)),
                    ('XGA', (1024,768)),        ('HD 720', (1280,720)),
                    ('WXGA_1', (1280,768)),     ('WXGA_2', (1280,800)),
                    ('SXGA', (1280,1024)),      ('SXGA+', (1400,1050)),
                    ('UXGA', (1600,1200)),      ('WSXGA+', (1680,1050)),
                    ('HD 1080', (1920,1080)),   ('WUXGA', (1920,1200)),
                    ('2K', (2048,1080))

                    ]
        self.resAsString = []
        self.resAsTuple = []
        for item in resolutions:
            self.resAsString.sppend((item[0])+" "+str(item[1]))
            self.resAsTuple(item[1])
            #newresolutions.append(((item[0])+" "+str(item[1]),item[1]))
        #print(item)
        print(newresolutions)



    def addItemsToCombos(self): #method
        self.ui.videoResolutions.addItems.(self.resAsString()) 
        self.ui.imageResolutions.addItems.(self.resAsString())
        return True

    def applySettings(self): #set the resolutions comboboxes to the value saved in camvals
        #if self.comboItemsAdded == True:
        #print (self.camvals["audioBitRate"])
        #for each key in the settings dictionery 
        self.ui.videoResolutions.setCurrentText(self.camvals["vidres"])

    def setCamValFromCombo(self, str):
        if self.comboItemsAdded == True:
            self.camvals[self.sender().objectName()] = str
            setattr(self.camera,self.sender().objectName(),str)
    

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
    resolutionsTab = resolutionsTab(None)
    resolutionsTab.show()
    sys.exit(app.exec_())
