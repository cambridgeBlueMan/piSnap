from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg 
from PyQt5 import QtWidgets as qtw

# ################################
# SEE COMMENTS AT END OF THIS FILE
# ################################

from gui.qualityTabGui import Ui_Form
#
from psSettings import PSSettings

from picamera import PiCamera
from time import sleep
import sys
import datetime
import json
import psFunctions

class QualityTab(qtw.QWidget):

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
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # add combo box items
        self.comboItemsAdded = self.addItemsToCombos(self)
        
        self.applySettings()

    def addItemsToCombos(*args):
        args[0].ui.audioBitRate.addItems(["8", "16", "24", "48"])
        args[0].ui.audioSampleRate.addItems(["44100", "48000"])
        args[0].ui.audioFileFormat.addItems(["wav", "aiff", "bollo"])
        args[0].ui.videoBitRate.addItems(["0", "2000000", "4000000","8000000", "17000000"])
        args[0].ui.videoQuality.addItems(["10", "20", "25", "30", "35", "40"])
        args[0].ui.videoProfile.addItems(["baseline", "main", "extended", "high", "constrained"])
        args[0].ui.videoLevel.addItems(["4","4.1", "4.2"])
        args[0].ui.iso.addItems(["0", "100", "200", "320", "400", "500", "640", "800"])
        args[0].ui.soundDevices.addItems(["USB", "Duet"])
        return True

    def applySettings(self):
        if self.comboItemsAdded == True:
            print("is audio active?: ", bool(self.camvals["audioActive"]))
        #for each key in the settings dictionery 
            self.ui.audioBitRate.setCurrentText(str(self.camvals["audioBitRate"]))
            self.ui.audioSampleRate.setCurrentText(str(self.camvals["audioSampleRate"]))
            self.ui.audioFileFormat.setCurrentText(str(self.camvals["audioFileFormat"]))
            self.ui.videoBitRate.setCurrentText(str(self.camvals["videoBitRate"]))                
            self.ui.videoQuality.setCurrentText(str(self.camvals["videoQuality"]))
            self.ui.soundDevices.setCurrentText(str(self.camvals["soundDevices"]))
            if self.camvals["mux"] == "true":
                state = True
            else:
                state = False
            self.ui.mux.setChecked(state)
            if self.camvals["audioActive"] == "true":
                state = True
            else:
                state = False
            self.ui.audioActive.setChecked(state)
            self.ui.videoProfile.setCurrentText(str(self.camvals["videoProfile"]))
            self.ui.videoLevel.setCurrentText(str(self.camvals["videoLevel"]))
            self.ui.iso.setCurrentText(str(self.camvals["iso"]))


    def setCamValFromCombo(self, str):
        if self.comboItemsAdded == True:
            print(str)
            self.camvals[self.sender().objectName()] = str
            #setattr(self.camera,self.sender().objectName(),str)

    def setIso(self,str):
        if self.comboItemsAdded == True:
            self.camvals["iso"] = int(str)
            self.camera.iso = int(str)
        

    def doMux(self, state):
        #print ("The value of state is: ", state)
        if state == True:
            self.camvals["mux"] = "true"
        else:
            self.camvals["mux"] = "false"
        

    def isAudioActive(self, state):
        #print ("The value of state is: ", state)
        if state == True:
            self.camvals["audioActive"] = "true"
        else:
            self.camvals["audioActive"] = "false"


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


"""
https://en.wikipedia.org/wiki/Advanced_Video_Coding#Levels

Profiles
By far the most commonly used profile is the High Profile. 


High Profile (HiP, 100)
The primary profile for broadcast and disc storage applications, particularly for high-definition television applications 
(for example, this is the profile adopted by the Blu-ray Disc storage format and the DVB HDTV broadcast service).

available for us:
profile - The H.264 profile to use for encoding. Defaults to ‘high’, but can be one of 
‘baseline’, ‘main’, ‘extended’, ‘high’, or ‘constrained’.

Levels
As the term is used in the standard, a "level" is a specified set of constraints that indicate a degree of required decoder 
performance for a profile. For example, a level of support within a profile specifies the maximum picture resolution, frame rate, 
and bit rate that a decoder may use. A decoder that conforms to a given level must be able to decode all bitstreams encoded for 
that level and all lower levels.


level - The H.264 level to use for encoding. Defaults to ‘4’, but can be any H.264 level up to ‘4.2’.
                max bit rate max res/framerate
4	245,760	8,192	20,000	2,048×1,024@30.0 (4)
4.1	245,760	8,192	50,000	2,048×1,024@30.0 (4)
4.2	522,240	8,704	50,000	2,048×1,080@60.0 (4)


bitrate - The bitrate at which video will be encoded. Defaults to 17000000 (17Mbps) if not specified. The maximum value depends 
on the selected H.264 level and profile. 

Bitrate 0 indicates the encoder should not use bitrate control (the encoder is limited by the quality only).

quality - Specifies the quality that the encoder should attempt to maintain. For the 'h264' format, use values between 
10 and 40 where 10 is extremely high quality, and 40 is extremely low (20-25 is usually a reasonable range for H.264 encoding). 

For the mjpeg format, use JPEG quality values between 1 and 100 (where higher values are higher quality). 
Quality 0 is special and seems to be a “reasonable quality” default.

END COMMENTS
"""