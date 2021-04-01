from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

# insert appropriate names here
from adjustmentsTabGui import Ui_adjustments
from psSettings import PSSettings
from psSliders import PSCompositeSlider

from picamera import PiCamera
from time import sleep
import sys
import datetime
import json

class Adjustments(qtw.QWidget):

    def __init__(self,camvals, camera):
        super().__init__()
        #flag to prevent combo boxes updating camvals values when items are added to combobox
        self.comboItemsAdded = False  
        # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals
        self.camera = camera
        # Ui for the Adjustments class :)
        self.ui = Ui_adjustments()
        self.ui.setupUi(self)

        #on successful completion 'add items to combos' method returns true
        self.comboItemsAdded = self.addItemsToCombos()

        self.setCompositeSliderRanges()

        self.applySettings()

    def addItemsToCombos(self):
        """ a number of possible settings are defined in dictionaries within the Picamera class.
        we access these dictionaries and add thier contents as items for a number of gui combo boxes
         """
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
        """ It is not currently possible to set the defaults for the custom composite
        slider class instances. This must therefore be done here """

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
        if self.comboItemsAdded == True:
            for key in self.camvals:
                # color_effects is a special case, it has no direct analogue in the gui
                if key == "color_effects":
                    #get the value of color_effects from the dictionery
                    print("color effects")
                    self.ui.color_effects_u.setValue(self.camvals[key][0])
                    self.ui.color_effects_v.setValue(self.camvals[key][1])
                #check if widget with the same name exists in the GUI
                if hasattr(self.ui,key):
                    #pass
                    #print(key)
                    #print(self.ui)
                    if  self.findChild(qtw.QComboBox, key):
                        print(key, "combo box", self.camvals[key])
                        x = self.findChild(qtw.QComboBox, key)
                        x.setCurrentText(self.camvals[key])
                    elif self.findChild(PSCompositeSlider, key):
                        self.findChild(PSCompositeSlider, key).setValue(self.camvals[key])

                    else:
                        pass
        
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
            #print(value)
            if value == 2:
                
                self.camera.color_effects = None
            else:
                self.camera.color_effects = self.camvals["color_effects"]
                
        
    def setImageEffect(self):
        if self.comboItemsAdded == True:
            self.camera.image_effect = self.sender().currentText()
            self.camvals["image_effect"] = self.sender().currentText()

    def setAwbMode(self):
        if self.comboItemsAdded == True:
            self.camera.awb_mode = self.sender().currentText()
            self.camvals["awb_mode"] = self.sender().currentText()
        
    def setDrcStrength(self):
        if self.comboItemsAdded == True:
            self.camera.drc_strength = self.sender().currentText()
            self.camvals["drc_strength"] = self.sender().currentText()

    def setExposureMode(self):
        if self.comboItemsAdded == True:
            self.camera.exposure_mode = self.sender().currentText()
            self.camvals["exposure_mode"] = self.sender().currentText()

    def setFlashMode(self):
        if self.comboItemsAdded == True:
            self.camera.flash_mode = self.sender().currentText()
            self.camvals["flash_mode"] = self.sender().currentText()

    def setMeterMode(self):
        if self.comboItemsAdded == True:
            self.camera.meter_mode = self.sender().currentText()
            self.camvals["meter_mode"] = self.sender().currentText()


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
                                                                                                                                                                                                                 
