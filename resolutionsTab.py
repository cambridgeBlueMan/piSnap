from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg 
from PyQt5 import QtWidgets as qtw

from gui.resolutionsTabGui import Ui_Form
from zoomTab import ZoomTab
from psSettings import PSSettings
#from gui.zoomTabGui import ZoomTab
from picamera import PiCamera
from time import sleep
import sys
import datetime
import json
import math
#QUERY Should change to say 'video resolutions' trigger activation of viedo tab and vice versa?
class ResolutionsTab(qtw.QWidget):
    def __init__(self, camvals, camera, centralWidget, zoomTab):
        super().__init__()
        self.comboItemsAdded = False
        self.cw = centralWidget
        self.zt = zoomTab
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
        self.settingsApplied = self.applySettings()

    def makeDataStructures(self):
        """ takes the data structure shown below and extracts resolutions as strings,
        and resolutions as tuples. Strings are used to populate two combo boxes displaying the
        avaiable resolutions. tples with matching indices are used to set the  actual
        values """
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
        #initialise the lists
        self.resAsString = []
        self.resAsTuple = []
        # add items to the lists
        for item in resolutions:
            self.resAsString.append((item[0])+", "+str(item[1]))
            self.resAsTuple.append(item[1])
#TODO If video resolution changes, reset the currently stored zoom
    def setVideoRes(self,int):
        """ slot triggered by the vidres combo box. updates the camvals dictionary with the new
        video resolution, and if video is the current setting of the captureTab Tab Widget runs the 
        setupVideoCapture method. Note this method is also triggered:
        
        1. on change of the captureTab widget current index
        2. when a zoom is being loaded from file
        
        Finally this method resets the zoom page """
        # if camera is currently recording then you can't change the resolution
        if self.camera.recording==True:
            self.camRecording()
        else:
            returnValue = None
            # are there unsaved changes on the zoom page?
            if self.zt.zTblModel.dirty == True:
                # if so then point this out to the user
                msgBox = qtw.QMessageBox()
                msgBox.move(100,400)
                msgBox.setIcon(qtw.QMessageBox.Information)
                msgBox.setText("You have unsaved changes on the Zoom Tab. Click OK to lose these, otherwise Cancel, then go to the Zooming Tool page and save")
                msgBox.setWindowTitle("Zooming Tool unsaved changes!")
                msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
                # what came back from message box?
                returnValue = msgBox.exec()
                # if appropriate then do it
            if returnValue == qtw.QMessageBox.Ok or self.zt.zTblModel.dirty == False:
                if self.comboItemsAdded == True:
                    # set new camvals value
                    self.camvals["vidres"] = self.resAsTuple[int] 
                    # get the shooter object
                    aShooter = self.cw.findChild(qtw.QWidget, "mWidget")
                    # what is the current mode i.e. video mode (1) or stilll mode  (0)
                    mode = aShooter.ui.captureTab.currentIndex()
                    # is the preview currently displaying
                    isPreview = aShooter.ui.previewVisible.isChecked()
                    if mode == 1 and isPreview == True:
                        aShooter.setCaptureMode(mode)
                    if mode == 1 and isPreview == False:
                        width = self.camvals["vidres"][0]/aShooter.resDivider
                        height = self.camvals["vidres"][1]/aShooter.resDivider
                        width = math.floor(width)
                        height = math.floor(height)
                        # resize the frame
                        aShooter.ui.imgContainer.resize(width, height)
                        aShooter.setCaptureMode(mode)
                    # reset the zoomTab settings
                    self.zt.initControls()
                    self.zt.zTblModel.dirty = False
                    #self.zt.zTblModel._data = []
                    self.zt.zTblModel.removeRows(0, self.zt.zTblModel.rowCount(None), None)
    def setStillRes(self,int):
        """ slot triggered by the imgres combo box. updates the camvals dictionary with the new
        still image resolution, and if still is the current setting of the captureTab Tab Widget runs the 
        setupStillCapture method. (Note this method is also triggered on change of the 
        captureTab widget current index). """
        if self.camera.recording==True:
            self.camRecording()
        else:
            if self.comboItemsAdded == True:
                self.camvals["imgres"] = self.resAsTuple[int]   
                aShooter = self.cw.findChild(qtw.QWidget, "mWidget")
                # what is the current mode i.e. video or still tab (or more tabs yet to be defined)
                mode = aShooter.ui.captureTab.currentIndex()
                isPreview = aShooter.ui.previewVisible.isChecked()
                # if still view is the current mode and preview is displaying
                if mode == 0 and isPreview == True:
                    #print("condition met ")
                    aShooter.setCaptureMode(mode)
                if mode == 0 and isPreview == False:
                    #just redraw the frame with the new resolution
                    #print("reDivider: ", type(self.camvals["vidres"][0]/aShooter.resDivider))
                    width = self.camvals["imgres"][0]/aShooter.resDivider
                    height = self.camvals["imgres"][1]/aShooter.resDivider
                    #width = math.floor(width)
                    #height = math.floor(height)
                    #(height)
                    #print (width, height)
                    # resize the frame
                    aShooter.ui.imgContainer.resize(width, height)
                    aShooter.setCaptureMode(mode)

    def camRecording(self):
        print("in cam recording")
        msgBox = qtw.QMessageBox()
        msgBox.move(100,400)

        msgBox.setIcon(qtw.QMessageBox.Information)
        msgBox.setText("You cannot change the resolution while the camera is recording")
        msgBox.setWindowTitle("Camera is recording!")
        msgBox.setStandardButtons(qtw.QMessageBox.Ok)
        returnValue = msgBox.exec()

    def addItemsToCombos(self): 
        self.ui.vidres.addItems(self.resAsString) 
        self.ui.imgres.addItems(self.resAsString)
        return True

    def applySettings(self): 
        #set the resolutions comboboxes to the value saved in camvals
        if self.comboItemsAdded == True:
            ix=self.resAsTuple.index(tuple(self.camvals["vidres"]))
            self.ui.vidres.setCurrentText(self.resAsString[ix])
            ix=self.resAsTuple.index(tuple(self.camvals["imgres"]))
            self.ui.imgres.setCurrentText(self.resAsString[ix])
            return True
            
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
    resolutionsTab = ResolutionsTab(None)
    resolutionsTab.show()
    sys.exit(app.exec_())
