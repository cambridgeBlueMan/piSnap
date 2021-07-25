from PyQt5 import QtCore, QtGui, QtWidgets

# insert appropriate names here
from gui.zoomTabGui import Ui_Form
#
from picamera import PiCamera
from time import sleep
import sys
import datetime
import json
import psFunctions
import _thread

#TODO running a zoom should have it's own little player ie starts, pause,stop 
#TODO ending camera recording at end of a zoom should be switchable
class ZoomTab(QtWidgets.QWidget):
    def __init__(self, camvals, camera):
        super().__init__()
        # Ui_Form is the main designer generated class. so instantiate one. Precede the variable name with
        # the word 'self'
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals
        if camera == None:
            self.camera = PiCamera()
        else:
            self.camera = camera
        self.ui = Ui_Form()
        # now pass the main window object to it so that the setupUi method can draw all
        # the widgets into the window
        self.ui.setupUi(self)
        #self.show()
        #self.ui.getXOrigin.keyPressEvent(self,event)
        # are these two values available from PiCamera
        self.sensorWidth = self.camvals["sensorWidth"]
        self.sensorHeight = self.camvals["sensorHeight"]
        # this shouldn't be set here. is avalable as camval
        self.framerate = self.camvals["framerate"]
        ########################
        # what to do with this?
        ########################
        self.previewDivider = 3
        # 

        self.ui.getZoom.setInvertedAppearance(True)
        self.pixelWidth  = 1/self.sensorWidth
        self.pixelHeight = 1/self.sensorHeight

        self.ui.adjustZoom.setText(u"\u26AB")

        self.initControls()

    def initControls(self):
        # set max value for ui items
        self.zoom = [0,0, self.camvals["vidres"][0] /self.sensorWidth, self.camvals["vidres"][0] /self.sensorWidth]
        self.startZoom = self.zoom[:]
        self.endZoom = self.zoom[:]
        self.ui.getZoom.setMinimum(self.camvals["vidres"][0] )
        self.ui.getZoom.setValue(self.camvals["vidres"][0] )
        #get the name pf the speed object and set its vaue to the camvals value as per above
        self.ui.getSpeed.setValue(self.camvals["loopSize"])
        self.ui.adjustZoom.setDragButtonSize(self.camvals["vidres"][0] /8, self.camvals["vidres"][1] /8)

        self.ui.adjustZoom.move(0,0)

        self.camera.zoom = self.zoom
        # now we can set the resolution on the camer itself
        self.camera.resolution = (self.camvals["vidres"][0] , self.camvals["vidres"][1] )
         
    def doSnap(self):
        self.camera.capture("apic.jpeg")

    def range(self, value):
        #value = 2028
        toRange = self.camvals["vidres"][1] 
        fromRange = self.camvals["vidres"][0] 
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

    def doPrintDiag(self, bool):
        print("startZoom: ", self.startZoom)
        print("endZoom: ", self.endZoom)
        psFunctions.printT(self.window(), "startZoom: " + str(self.startZoom ))
        psFunctions.printT(self.window(), "endZoom: " + str(self.endZoom ))

    def setZoom(self, val):
        #print(val)
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
    def setSpeed(self,val):
        self.camvals["loopSize"] = val 
        #pass
        print(val)

    def doSetStart(self,bool):
        #print(args)
        self.startZoom = self.zoom[:]
        #print ("start zoom: ", self.zoom)
        #self.printDiag(self)

    def doSetEnd(self,bool):
        self.endZoom = self.zoom[:]
        #print("end zoom: ", self.zoom)
        #self.printDiag(self)

    def doRunZoom(self, bool):
        #set the resolution on the camer itself
        #self.camera.resolution = (self.camvals["vidres"][0] , self.camvals["vidres"][1] )
        """ # LEA 
        The actual speed of the zoom should be a function of not just the speed control
        but also the distance to travel
        To be clear the loopSize is exactly that and not a speed control per se. 
        It dictates how many times the loop must run
        so, if a zoom is across a large distance then it makes sense that a larger loopsize
        should be involved in getting it there

        """
        """ if bool == True
        set button text to "abort zoom"
        start the zoom
        if bool == False
        set abortZoom == True
        set button text to "run zoom"
        
        """
        print(bool)
        # number of steps to complete the zoom
        loopSize = (self.camvals["loopSize"])
        #loopSize = 1200
        # increment for each staep
        deltaX = 0
        deltaY = 0
        deltaZ = 0
        # increment for each step
        xInc = abs(self.startZoom[0]-self.endZoom[0])/loopSize
        yInc = abs(self.startZoom[1]-self.endZoom[1])/loopSize
        zInc = abs(self.startZoom[2]-self.endZoom[2])/loopSize
        if bool == True:
            _thread.start_new_thread(self.runZoomLoop, (loopSize, deltaX, deltaY, deltaZ, xInc, yInc, zInc))
            self.ui.runZoom.setText("abort zoom")
            self.abortZoom = False
        else:
            self.ui.runZoom.setText("run zoom")
            self.abortZoom = True
        """ 
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
            #print("iter")
        print("loop now ended")
        #loop now ended 
        if self.camera.recording:
            self.window().mWidget.doStopVid()
            print("now in if")
         """

    def runZoomLoop(self, loopSize, deltaX, deltaY, deltaZ, xInc, yInc, zInc):
        #j = 0
        print ("in thread")
        for j in range(loopSize):
            if self.abortZoom == True:
                self.abortZoom = False
                break
            print(j)
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
            #print("iter")
        print("loop now ended")
        self.ui.runZoom.setText("run zoom")
        self.abortZoom = False
        #loop now ended 
        if self.camera.recording:
            self.window().mWidget.doStopVid()
            print("now in if")
        
    def doShowStart(self, bool):
        self.camera.zoom = self.startZoom[:]
    
    def doShowEnd(self, bool):
        self.camera.zoom = self.endZoom[:]

    
        #print(self.camera.zoom)
    def doQuit(self):
        sys.exit()
 
    def showPreview(self):
        if self.ui.showPreview.isChecked():
            self.camera.start_preview(fullscreen = False, window = (int(self.camvals["vidres"][0] /self.previewDivider),0,
                                                                int(self.camvals["vidres"][0] /self.previewDivider), int(self.camvals["vidres"][1] /self.previewDivider)))
        else:
            self.camera.stop_preview()
        pass

    def twattock(self):
        print("hello everybody!!!")

    def resetZoomStuff(self):
        print("in reset zoom stuff")
        self.zoom = [0,0, self.camvals["vidres"][0] /self.sensorWidth, self.camvals["vidres"][0] /self.sensorWidth]
        self.startZoom = self.zoom[:]
        self.endZoom = self.zoom[:]
        self.ui.getZoom.setMinimum(self.camvals["vidres"][0] )
        self.ui.getZoom.setValue(self.camvals["vidres"][0] )
        #
        self.ui.adjustZoom.setDragButtonSize(self.camvals["vidres"][0] /8, self.camvals["vidres"][1] /8)

        self.camera.zoom = self.zoom
        # now we can set the resolution on the camer itself
        self.camera.resolution = (self.camvals["vidres"][0] , self.camvals["vidres"][1] )



#######################################################################################
    #                           END OF CLASS
#######################################################################################
if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = QtWidgets.QApplication(sys.argv)
    # instantiate an object containing the logic code
    mw = ZoomTab(None, None)
    sys.exit(app.exec_())


