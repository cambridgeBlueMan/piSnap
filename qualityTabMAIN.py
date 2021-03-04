from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg 
from PyQt5 import QtWidgets as qtw

# insert appropriate names here
from qualityTab import Ui_Form
#
from picamera import PiCamera
from time import sleep
import sys
import datetime
"""
You may need to change the line declaring the class below. It will depend on the choice you make
for your containing window: main window, dialog box etc)
"""
class QualityTab(qtw.QWidget):

    def __init__(self):
        super().__init__()
        # Ui_Form is the main designer generated class. so instantiate one. Precede the variable name with
        # the word 'self'
        
        self.ui = Ui_Form()
        # now pass the main window object to it so that the setupUi method can draw all
        # the widgets into the window

        self.ui.setupUi(self)

        self.finishUi(self)
        """
        self.show()
        # now instantiate a camera object. Again the variable name is preceded by the word 'self'
        self.camera = PiCamera()
        # you might then declare and initialise some variable which will be available across the class
        self.framerate = 50.0
        self.resolution = (1920,1080)
        # you might then invoke some methods of your camera object
        self.camera.start_preview(fullscreen = False, window = (960,0,960,540))
        # or set sone attributes
        self.camera.sensor_mode = 1
        
        Note the following line:
        
        self.framerate is a variable you named and initialised.
        self.camera.framerate is an attribute of the camera object
        the code line sets the camera's framerate to the value held in the framerate variable
        
        self.camera.framerate = self.framerate
        """
        # add your own method functions below

    def finishUi(*args):
        args[0].ui.audioBitRate.addItems(["16", "24"])
        args[0].ui.audioSampleRate.addItems(["44.1kz", "48kz"])
        args[0].ui.audioFileFormat.addItems(["wav", "aiff"])
        args[0].ui.videoBitRate.addItems(["0", "17000000"])
        args[0].ui.videoQuality.addItems(["10", "20", "25", "30", "35", "40"])


        
    def setAudioBitRate(self):
        print(self)
        
    def setAudioSampleRate(self):
        print(self)

    def setAudioFileFormat(self):
        print(self)

    def doMux(self):
        print(self)

    def isAudioActive(self):
        print(self)

    def setVideoBitRate(self):
        print(self)
    def setVideoQuality(self):
        print(self)
 

#######################################################################################
    #                           END OF CLASS
#######################################################################################
if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = qtw.QApplication(sys.argv)
    # instantiate an object containing the logic code
    qualityTab = QualityTab()
    qualityTab.show()
    sys.exit(app.exec_())


