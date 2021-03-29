from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

# insert appropriate names here
from adjustmentsTabGui import Ui_adjustments
from psSettings import PSSettings

from picamera import PiCamera
from time import sleep
import sys
import datetime
import json

class Adjustments(qtw.QWidget):

    def __init__(self,camvals, camera):
        super().__init__()
        self.comboItemsAdded = False  #flag to prevent combo boxes updating camvals values when items are added to combobox
        # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals
        self.camera = camera
        self.ui = Ui_adjustments()
        self.ui.setupUi(self)
        #on successful completion 'add items to combos' method returns true
        self.comboItemsAdded = self.addItemsToCombos()

        self.setCompositeSliderRanges()

        self.applySettings()

    def addItemsToCombos(self):
        
        self.ui.image_effect.addItems(self.camera.IMAGE_EFFECTS)
        self.ui.image_effect.setCurrentText('none')
        self.ui.awb_mode.addItems(self.camera.AWB_MODES)
        self.ui.awb_mode.setCurrentText('auto')
        self.ui.drc_strength.addItems(self.camera.DRC_STRENGTHS)
        self.ui.drc_strength.setCurrentText('off')
        self.ui.exposure_mode.addItems(self.camera.EXPOSURE_MODES)
        self.ui.exposure_mode.setCurrentText('auto')
        self.ui.flash_mode.addItems(self.camera.FLASH_MODES)
        self.ui.flash_mode.setCurrentText('off')
        self.ui.meter_mode.addItems(self.camera.METER_MODES)
        self.ui.meter_mode.setCurrentText('average')
        return True

    def setCompositeSliderRanges(self):
        self.ui.sharpness.setRanges(-100,100,self.camera.sharpness)
        #print(type(self.ui.contrast))
        self.ui.contrast.setRanges(-100,100,self.camera.contrast)
        self.ui.saturation.setRanges(-100,100,self.camera.saturation)
        self.ui.brightness.setRanges(0,100,self.camera.brightness)
        #set vales for color effects composite sliders u and v values
        self.ui.color_effects_u.setRanges(0,255,128)
        self.ui.color_effects_v.setRanges(0,255,128)

       
    def applySettings(self):
        #for each key in the settings dictionery 
        for key in self.camvals:
        #check if widget with the same name exists in the GUI
            if hasattr(self.ui,key):
                #pass
                print(key)
        #Depending on the type of the GUI or UI widget update the GUI
            if key == "color_effects":
        #get the value of color_effects from the dictionery
                    #print(self.cs[key])
                    self.ui.color_effects_u.setValue(self.camvals[key][0])
                    self.ui.color_effects_v.setValue(self.camvals[key][1])
        # This should automatically update through to the camera
        #self.ui.brightness.sendValue(self.cs["brightness"])
        #self.cs["brightness"]
        ##print(self.cs["brightness"])
        
        
        self.ui.image_effect.setCurrentText(self.camvals ["image_effect"])
        
    def changeCameraValue(self, value):
        control = self.sender().objectName()
        #value = args[1]
        if control == "sharpness":
            self.camera.sharpness  = value
            self.camvals ["sharpness"] = value
        elif control == "contrast":
            self.camera.contrast = value
            self.camvals ["contrast"] = value
        elif control == "saturation":
            #print("in saturation")
            self.camera.saturation = value
            self.camvals ["saturation"] = value
        elif control == "brightness":
            self.camera.brightness = value
            self.camvals ["brightness"] = value
        else:
            pass
            #print("Unknown control!")
    def doColorEffect(self,value):
        #get the name of the sending control
        control = self.sender().objectName()
        #if we find the control is to set the u value
        #set the first element of the "color effects" dictionary item to value
        if control == "color_effects_u":
            self.camvals["color_effects"][0] = value
            #if "color effects" is set to none in the GUI 
            if self.ui.color_effects_none.isChecked:
                pass #don't do anything
            else: #otherwise set the "color effects" to the value held in the color effects element of the settings dictionary
                #note that this dictionary item is a 2 element python list although the camera expects a 2 element tuple
                #however, it seems to buy this
                self.camera.color_effects = self.camvals["color_effects"]
        if control == "color_effects_v":
            self.camvals["color_effects"][1] = value
            if self.ui.color_effects_none.isChecked:
                pass
            else:
                self.camera.color_effects = self.camvals["color_effects"]
        if control =="color_effects_none":
            print(value)
            if value == 2:
                
                self.camera.color_effects = None
            else:
                self.camera.color_effects = self.camvals["color_effects"]
                
        
    def setImageEffect(self):
        #print(self)
        #print(self.camera.IMAGE_EFFECTS.values())
        #print(type(self.camera.IMAGE_EFFECTS))
        #print(self.camera.IMAGE_EFFECTS.keys)
        self.camera.image_effect = self.sender().currentText()
    def setAwbMode(self):
        self.camera.awb_mode = self.sender().currentText()
        #print(self)
    def setDrcStrength(self):
        self.camera.drc_strength = self.sender().currentText()
        #print(self)
    def setExposureMode(self):
        self.camera.exposure_mode = self.sender().currentText()
        #print(self)
    def setFlashMode(self):
        self.camera.flash_mode = self.sender().currentText()
        #print(self)
    def setMeterMode(self):
        self.camera.meter_mode = self.sender().currentText()
        #print(self)


#######################################################################################
    #                           END OF CLASS
#######################################################################################
if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = qtw.QApplication(sys.argv)
    # instantiate an object containing the logic code
    MainWindow = Code_Dialog(None, PiCamera())
    sys.exit(app.exec_())
                                                                                                                                                                                                                 
