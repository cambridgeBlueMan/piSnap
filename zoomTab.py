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

        self.initModelStuff()

    def initModelStuff(self):
        self.model = zoomTableModel()
        self.ui.zoomTableView.setModel(self.model)

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
        # add stuff for model version
        zdata = [self.zoom[0], self.zoom[1], self.zoom[2], 600, 1]
        # insert rows (position, numrows, parent, data)
        self.model.insertRows(self.model.rowCount(None),1, self.model.parent(), zdata)



    def doSetEnd(self,bool):
        self.endZoom = self.zoom[:]
        #print("end zoom: ", self.zoom)
        #self.printDiag(self)

    def doRunZoom(self, bool):
        #set the resolution on the camer itself
        #self.camera.resolution = (self.camvals["vidres"][0] , self.camvals["vidres"][1] )
        # LEA The actual speed of the zoom should be a function of not just the speed control
        # but also the distance to travel
        

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
            #self.ui.runZoom.toggle()
        else:
            self.ui.runZoom.setText("run zoom")
            self.abortZoom = True
        

    def runZoomLoop(self, loopSize, deltaX, deltaY, deltaZ, xInc, yInc, zInc):
        #j = 0
        print ("in thread")
        for j in range(loopSize):
            if self.abortZoom == True:
                self.abortZoom = False
                self.ui.runZoom.setChecked(True)
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
        self.ui.runZoom.toggle() #abortZoom = False

        #loop now ended 
        if self.camera.recording:
            self.window().mWidget.doStopVid()
            print("now in if")
        
    def doShowStart(self, bool):
        self.camera.zoom = self.startZoom[:]
    
    def doShowEnd(self, bool):
        self.camera.zoom = self.endZoom[:]

    def deleteSelectedRow(self):
        print("delete selected row")
        selected = self.ui.zoomTableView.selectedIndexes()
        # Errata:  The book contains the following code:
        #if selected:
        #    self.model.removeRows(selected[0].row(), len(selected), None)

        # This is incorrect, as len(selected) is the number of *cells* selected,
        # not the number of *rows* selected.

        # correct approach would look like this:
        num_rows = len(set(index.row() for index in selected))
        if selected:
            self.model.removeRows(selected[0].row(), num_rows, None)

    

    def playSelectedRow(self):
        #self.ui.zoomTableView.
        # TODO deal with no rows selcted case
        selected = self.ui.zoomTableView.selectedIndexes()
        # gather rows in a set and then see how many you got
        num_rows = len(set(index.row() for index in selected))
        if num_rows == 0:
            psFunctions.printT(self.window(),"No rows are currently selected!!")
        elif num_rows == 1:
            psFunctions.printT (self.window(),"you need more than just one row to run a zoom")
            print("This is start row: ",selected[0].row())
            print("and this is the row: ", self.ui.zoomTableView.rowAt(selected[0].row()))
            #pass
        else:
            # run a zoom
            psFunctions.printT(self.window(),"more than 1 row")
            #print("This is start row: ",selected[0].row())
            startRow = selected[0].row()

            for ix in range(startRow, (startRow + num_rows)):
                # increment for each step
                print("ix", self.model._data[ix])
                print("nextRow", self.model._data[ix+1])
                loopSize = self.model._data[ix][3] 
                pause = self.model._data[ix][4]
                xInc = abs(self.model._data[ix][0] - self.model._data[(ix + 1)][0])/loopSize
                yInc = abs(self.model._data[ix][1] - self.model._data[(ix + 1)][1])/loopSize
                zInc = abs(self.model._data[ix][2] - self.model._data[(ix + 1)][2])/loopSize
                #define startZoom and endZoom here!!!
                startZoom = [
                    self.model._data[ix][0], 
                    self.model._data[ix][1], 
                    self.model._data[ix][2], 
                    self.model._data[ix][2]
                ]
                endZoom = [
                    self.model._data[ix+1][0], 
                    self.model._data[ix+1][1], 
                    self.model._data[ix+1][2], 
                    self.model._data[ix+1][2]
                ]


                print("incs: ",xInc,yInc,zInc)
                #if bool == True:
                #_thread.start_new_thread(
                self.runMultiZoomLoop (xInc, yInc, zInc, startZoom, endZoom, loopSize, pause) # )
                #    self.ui.runZoom.setText("abort zoom")
                #    self.abortZoom = False
                #    #self.ui.runZoom.toggle()
                #else:
                #    self.ui.runZoom.setText("run zoom")
                #    self.abortZoom = True
                #pass
                # there would be a wait(pause) here
                # and then the loop would have ended

        print("this is data: ", self.model._data)
        
        # following does the trick
        #print(selected[0].data(), selected[1].data(), selected[2].data())


    def runMultiZoomLoop(self,xInc, yInc, zInc, startZoom, endZoom, loopSize, pause):
        print ("in thread")
        deltaX = 0
        deltaY = 0
        deltaZ = 0
        startZoom = startZoom[:]
        endZoom = endZoom[:]

        for j in range(loopSize):
            """ if self.abortZoom == True:
                self.abortZoom = False
                self.ui.runZoom.setChecked(True)
                break """
            print(j)
            sleep(1/self.framerate)
            
            # if start and end zoom dimension are equal then do nothing
            if startZoom[0] == endZoom[0]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif startZoom[0] < endZoom[0]:
                deltaX  = deltaX + xInc
                if startZoom[0] + deltaX >= endZoom[0]:
                    break
                self.zoom[0] = startZoom[0] + deltaX
            # otherwise we start high and are decreasing
            else:
                deltaX = deltaX + xInc
                if startZoom[0] - deltaX <= endZoom[0]:
                    break
                self.zoom[0] = startZoom[0] - deltaX

            # if start = end then do nothing
            if startZoom[1] == endZoom[1]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif startZoom[1] < endZoom[1]:
                deltaY = deltaY + yInc
                if startZoom[1] + deltaY >= endZoom[1]:
                    break
                self.zoom[1] = startZoom[1] + deltaY
            # otherwise we start high and are decreasing
            else:
                deltaY = deltaY + yInc
                if startZoom[1] - deltaY <= endZoom[1]:
                    break
                self.zoom[1] = startZoom[1] - deltaY

            # if start and end are equal then do nothing
            if startZoom[2] == endZoom[2]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif startZoom[2] < endZoom[2]:
                deltaZ = deltaZ + zInc
                if startZoom[2] + deltaX >= endZoom[2]:
                    break
                self.zoom[2] = startZoom[2] + deltaZ
                self.zoom[3] = startZoom[3] + deltaZ
            # otherwise we start high and are decreasing
            else:
                deltaZ = deltaZ + zInc
                if startZoom[2] - deltaZ <= endZoom[2]:
                    break
                self.zoom[2] = startZoom[2] - deltaZ
                self.zoom[3] = startZoom[3] - deltaZ


            self.camera.zoom = self.zoom[:]
            #print("iter")
        sleep(pause)
        print("loop now ended")
        self.ui.runZoom.setText("run zoom")
        self.ui.runZoom.toggle() #abortZoom = False

        #loop now ended 
        if self.camera.recording:
            self.window().mWidget.doStopVid()
            print("now in if")
        

    
    def doQuit(self):
        sys.exit()
 
    def showPreview(self):
        if self.ui.showPreview.isChecked():
            self.camera.start_preview(fullscreen = False, window = (int(self.camvals["vidres"][0] /self.previewDivider),0,
                                                                int(self.camvals["vidres"][0] /self.previewDivider), int(self.camvals["vidres"][1] /self.previewDivider)))
        else:
            self.camera.stop_preview()
        pass

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


class zoomTableModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._headers = ["X", "Y", "Width", "speed", "pause"]
        self._data = []
        """  [0,0,0.1,200,1],
            [0,0,1,300,3],
            [0,0,0.12345,200,1],
            [0,0,1,600,5],
            [0,0,1,200,1]
        ]
        """
    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        # original if statement:
        # if role == QtCore.Qt.DisplayRole:
        # Add EditRole so that the cell is not cleared when editing
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return self._data[index.row()][index.column()]

    # Additional features methods:

    def headerData(self, section, orientation, role):

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()  # needs to be emitted before a sort
        self._data.sort(key=lambda x: x[column])
        if order == QtCore.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # needs to be emitted after a sort

    # Methods for Read/Write

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    # Methods for inserting or deleting
    # position is point for insertion
    # rows is number of rows to insert - 1 in our case
    # and thee parent mode index - of no interest to us
    # The rowCount() and columnCount() functions 
    # #return the dimensions of the table
    def insertRows(self, position, rows, parent, zdata):
        # following line needed, also see end
        # parent or QtCore line stays as is
        print(zdata)
        self.beginInsertRows(
            parent or QtCore.QModelIndex(),
            position,
            position + rows - 1
        )

        for i in range(rows):
            default_row = [''] * len(self._headers)
            self._data.insert(position, zdata)
        
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(
            parent or QtCore.QModelIndex(),
            position,
            position + rows - 1
        )
        for i in range(rows):
            del(self._data[position])
        self.endRemoveRows()

    # method for saving
    def save_data(self):
        # commented out code below to fix issue with additional lines being added after saving csv file from the window.
        # with open(self.filename, 'w', encoding='utf-8') as fh:
        with open(self.filename, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow(self._headers)
            writer.writerows(self._data)




if __name__ == "__main__":
    import sys
    # instiantiate an app object from the QApplication class 
    app = QtWidgets.QApplication(sys.argv)
    # instantiate an object containing the logic code
    mw = ZoomTab(None, None)
    sys.exit(app.exec_())


