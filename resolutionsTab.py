from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg 
from PyQt5 import QtWidgets as qtw

from resolutionsTabGui import Ui_Form
from psSettings import PSSettings
from zoomTab import ZoomTab
from picamera import PiCamera
from time import sleep
import sys
import datetime
import json

class ResolutionsTab(qtw.QWidget):
    def __init__(self, camvals, camera, centralWidget):
        super().__init__()
        self.comboItemsAdded = False
        self.cw = centralWidget
        # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals
        #print(self.camvals["vidres"])
        self.camera = camera
        self.ui = Ui_Form() # makes the actual gui
        self.ui.setupUi(self)
        # add combo box items
        self.makeDataStructures()
        self.comboItemsAdded = self.addItemsToCombos()
        self.applySettings()

    def makeDataStructures(self):
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
            self.resAsString.append((item[0])+" "+str(item[1]))
            self.resAsTuple.append(item[1])

    def setVideoRes(self,int):
        if self.comboItemsAdded == True:
            # set new camvals value
            self.camvals["vidres"] = self.resAsTuple[int] 
            self.cw.findChild(qtw.QWidget, "mWidget").resetResolutionStuff()
            x = self.window().findChild(ZoomTab, "zoomTab") #.resetZoomStuff()
            if x:
                print("got one!")
                x.resetZoomStuff()
            
    def setStillRes(self,int):
        if self.comboItemsAdded == True:
            self.camvals["imgres"] = self.resAsTuple[int]     
            self.cw.findChild(qtw.QWidget, "mWidget").resetResolutionStuff()   
            x = self.window().findChild(ZoomTab, "zoomTab") #.resetZoomStuff()
            if x:
                print("got one!")
                x.resetZoomStuff()
            #x.resetZoomStuff()
            #print (self.window().findChild(ZoomTab, "zoomTab").resetZoomStuff) #.resetZoomStuff()

    def addItemsToCombos(self): 
        self.ui.vidres.addItems(self.resAsString) 
        self.ui.imgres.addItems(self.resAsString)
        return True

    def applySettings(self): #set the resolutions comboboxes to the value saved in camvals
        if self.comboItemsAdded == True:
            ix=self.resAsTuple.index(tuple(self.camvals["vidres"]))
            self.ui.vidres.setCurrentText(self.resAsString[ix])
            ix=self.resAsTuple.index(tuple(self.camvals["imgres"]))
            self.ui.imgres.setCurrentText(self.resAsString[ix])
            
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
