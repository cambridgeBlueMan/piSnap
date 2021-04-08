from PyQt5 import QtCore, QtGui, QtWidgets

# insert appropriate names here
from zoomTabGui import Ui_MainWindow
#
from picamera import PiCamera
from time import sleep
import sys
import datetime

class KeyboardSlider(QtWidgets.QSlider):
    def __init__(self,parent):
        super().__init__(parent)
        
    def keyPressEvent(self, event):
        if event.key()==16777235:
            #print('in key up')
            self.setValue(self.value() +1) # uparrow
            #print(self.value())
        if event.key() == 16777237:
            print('in key down')
            self.setValue(self.value() -1) # down arrow
            #print(self.value())

        
class Code_MainWindow(QtWidgets.QMainWindow):
    
        

    def __init__(self):
        super().__init__()
        # Ui_Form is the main designer generated class. so instantiate one. Precede the variable name with
        # the word 'self'
        
        self.ui = Ui_MainWindow()
        # now pass the main window object to it so that the setupUi method can draw all
        # the widgets into the window
        self.ui.setupUi(self)
        self.show()
        #self.ui.getXOrigin.keyPressEvent(self,event)
        # now instantiate a camera object. Again the variable name is preceded by the word 'self'
        self.camera = PiCamera()
        self.sensorWidth = 4056
        self.sensorHeight = 3040
        self.framerate = 25
        self.previewDivider = 3
        self.pixelWidth  = 1/self.sensorWidth
        self.pixelHeight = 1/self.sensorHeight
        # rsolution width and height are set by the user
        self.resolutionWidth = 1920 #self.sensorWidth
        self.resolutionHeight = 1080 #self.sensorHeight
        #self.zoomDimension = 0.5
        # set max value for ui items
        self.zoom = [0,0, self.resolutionWidth/self.sensorWidth, self.resolutionWidth/self.sensorWidth]
        self.startZoom = self.zoom[:]
        self.endZoom = self.zoom[:]
        #self.ui.getYOrigin.setMaximum((1-self.resolutionWidth/self.sensorWidth)*self.sensorWidth)
        #self.ui.getXOrigin.setMaximum((1-self.resolutionWidth/self.sensorWidth)*self.sensorWidth)
        self.ui.getZoom.setMinimum(self.resolutionWidth)
        self.ui.getZoom.setValue(self.resolutionWidth)
        #
        self.ui.adjustZoom.setDragButtonSize(self.resolutionWidth/8, self.resolutionHeight/8)

        self.camera.zoom = self.zoom
        # now we can set the resolution on the camer itself
        self.camera.resolution = (self.resolutionWidth, self.resolutionHeight)
        self.camera.start_preview(fullscreen = False, window = (0,0,
                                                                int(self.resolutionWidth/self.previewDivider), int(self.resolutionHeight/self.previewDivider)))
        #self.camera.start_preview(fullscreen = False, )
        #self.camera.sensor_mode = 1
         
    def doSnap(self):
        self.camera.capture("twattock.jpeg")

    def range(self, value):
        #value = 2028
        toRange = self.resolutionHeight
        fromRange = self.resolutionWidth
        return value*toRange/fromRange

    def setZoomWithButton(self, x, y):
        """ This is slot connected to posChanged(int,int) signal from the dragButton used to 
        position the zoomed window within the space of the whole sensor

        The values are 1/8 of the actual values, since the frame in which the dragButton 
        operates is 1/8 of full size

        """
        #print(x,y)
        #if x*8  > self.ui.getXOrigin.value():
        #   x = self.ui.getXOrigin.value()/8
        self.setXOrigin(x*8)
        y = self.range(y)
        self.setYOrigin(y*8)
        #self.ui.getYOrigin.setMaximum((1-val/self.sensorWidth)*self.sensorWidth)
        #self.ui.getXOrigin.setMaximum((1-val/self.sensorWidth)*self.sensorWidth)

    def movePosition(self):
        pass
        #print ("position moved") 

    def AnotherMethod(self):
        pass
        #print(self)
        
    def setXOrigin(self, val):
        self.zoom[0] = val/self.sensorWidth
        self.camera.zoom = self.zoom 

    def setYOrigin(self, val):
        self.zoom[1] = val/self.sensorWidth
        self.camera.zoom = self.zoom 

    def printDiag(self, bool):
        print("startZoom: ", self.startZoom)
        print("endZoom: ", self.endZoom)

    def setZoom(self, val):
        print(val)
        self.zoom[2] = val/self.sensorWidth
        self.zoom[3] = val/self.sensorWidth
        #self.ui.getYOrigin.setMaximum((1-val/self.sensorWidth)*self.sensorWidth)
        #self.ui.getXOrigin.setMaximum((1-val/self.sensorWidth)*self.sensorWidth)
        #print("max: ", self.ui.getYOrigin.setMaximum((1-val/self.sensorWidth)*self.sensorWidth))
        # 
        height = self.range(val)
        #print("height: ", height)
        self.ui.adjustZoom.setDragButtonSize(val/8, height/8)

       
        self.camera.zoom = self.zoom 
        # we need also to reset the ranges of the getYOrigin and getXOrigin sliders
        
    def doSetStart(self,bool):
        #print(args)
        self.startZoom = self.zoom[:]
        #print ("start zoom: ", self.zoom)

    def doSetEnd(self,bool):
        self.endZoom = self.zoom[:]
        #print("end zoom: ", self.zoom)

    def doRunZoom(self, bool):
        # number of steps to complete the zoom
        loopSize = 100  
        # increment for each staep
        deltaX = 0
        deltaY = 0
        deltaZ = 0
        # increment for each step
        xInc = abs(self.startZoom[0]-self.endZoom[0])/loopSize
        yInc = abs(self.startZoom[1]-self.endZoom[1])/loopSize
        zInc = abs(self.startZoom[2]-self.endZoom[2])/loopSize

        for j in range(loopSize):
            #print(j)
            sleep(1/self.framerate)
            
            # if start and end zoom dimension are equal then do nothing
            if self.startZoom[0] == self.endZoom[0]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif self.startZoom[0] < self.endZoom[0]:
                deltaX  = deltaX + xInc
                if self.startZoom[0] + deltaX >= self.endZoom[0]:
                    break
                self.zoom[0] = self.startZoom[0] + deltaX
            # otherwise we start high and are decreasing
            else:
                deltaX = deltaX + xInc
                if self.startZoom[0] - deltaX <= self.endZoom[0]:
                    break
                self.zoom[0] = self.startZoom[0] - deltaX

            # if start = end then do nothing
            if self.startZoom[1] == self.endZoom[1]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif self.startZoom[1] < self.endZoom[1]:
                deltaY = deltaY + yInc
                if self.startZoom[1] + deltaY >= self.endZoom[1]:
                    break
                self.zoom[1] = self.startZoom[1] + deltaY
            # otherwise we start high and are decreasing
            else:
                deltaY = deltaY + yInc
                if self.startZoom[1] - deltaY <= self.endZoom[1]:
                    break
                self.zoom[1] = self.startZoom[1] - deltaY

            # if start and end are equal then do nothing
            if self.startZoom[2] == self.endZoom[2]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif self.startZoom[2] < self.endZoom[2]:
                deltaZ = deltaZ + zInc
                if self.startZoom[2] + deltaX >= self.endZoom[2]:
                    break
                self.zoom[2] = self.startZoom[2] + deltaZ
                self.zoom[3] = self.startZoom[3] + deltaZ
            # otherwise we start high and are decreasing
            else:
                deltaZ = deltaZ + zInc
                if self.startZoom[2] - deltaZ <= self.endZoom[2]:
                    break
                self.zoom[2] = self.startZoom[2] - deltaZ
                self.zoom[3] = self.startZoom[3] - deltaZ


            self.camera.zoom = self.zoom[:]

    def doShowStart(self, bool):
        self.camera.zoom = self.startZoom[:]
    
    def doShowEnd(self, bool):
        self.camera.zoom = self.endZoom[:]

    
        #print(self.camera.zoom)
    def doQuit(self):
        sys.exit()
 
    def showPreview(self):
        if self.ui.showPreview.isChecked():
            self.camera.start_preview(fullscreen = False, window = (int(self.resolutionWidth/self.previewDivider),0,
                                                                int(self.resolutionWidth/self.previewDivider), int(self.resolutionHeight/self.previewDivider)))
        else:
            self.camera.stop_preview()
        pass
#######################################################################################
    #                           END OF CLASS
#######################################################################################
if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = QtWidgets.QApplication(sys.argv)
    # instantiate an object containing the logic code
    mw = Code_MainWindow()
    sys.exit(app.exec_())


