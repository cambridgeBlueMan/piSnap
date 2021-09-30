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
import math
#TODO running a zoom should have it's own little player ie starts, pause,stop 
#TODO ending camera recording at end of a zoom should be switchable
class ZoomTab(QtWidgets.QWidget):
    def __init__(self, camvals, camera):
        super().__init__()
        
        self.camvals = camvals
        self.camera = camera
 
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # are these two values available from PiCamera
        self.sensorWidth = self.camvals["sensorWidth"]
        self.sensorHeight = self.camvals["sensorHeight"]

        ########################
        # what to do with this?
        ########################
        self.previewDivider = 3
        # 
        self.ui.getZoom.setInvertedAppearance(True)
        # TODO dont think the next two lines are used?
        #self.pixelWidth  = 1/self.sensorWidth
        #self.pixelHeight = 1/self.sensorHeight

        #set to bullet point
        self.ui.adjustZoomXYPos.setText(u"\u26AB")

        # set to player control chars
        self.ui.playRows.setText(u"\u23F5")
        self.ui.nextZoom.setText(u"\u23ED")
        self.ui.restartZoom.setText(u"\u23EA")

        # initialise flags for playRows
        self.nextZoom = False
        self.abortZoom = False
        self.restartZoom = False
        self.endRecWithZoom = False
        self.initControls()
        self.initModelStuff()

    def initModelStuff(self):
        # ZoomTableModel is subclassed from QAbstractTableModel
        self.zTblModel = ZoomTableModel()
        # associate the zTblView widget created in designer with the zTblModel
        self.ui.zTblView.setModel(self.zTblModel)

    def initControls(self):
        # TODO limited functionality for stills, including disabling stuff

        """ we make the zoom the maximum possible for the given resolution """
        self.zoom = [0,0, self.camvals["vidres"][0] /self.sensorWidth, self.camvals["vidres"][0] /self.sensorWidth]
        self.startZoom = self.zoom[:]
        self.endZoom = self.zoom[:]
        """ 
        getZoom is a slider
        minimum is set in designer at 1920 (HD) , 
        max is set in designer at 3470, I'm not sure where that figure comes from?
        but i am sure  that it is a good figue !!!!! 
        represents 0.855 of sensor size. This may have to do with modes?
        
        """

        self.ui.getZoom.setMinimum(self.camvals["vidres"][0] )

        # QUERY should the following be set to max rather than min?
        self.ui.getZoom.setValue(self.camvals["vidres"][0] )

        # dragbutton size varies according to the current res
        # QUERY if previous QUERY is set to max then drag button size should be set accordingly
        self.ui.adjustZoomXYPos.setDragButtonSize(self.camvals["vidres"][0] /8, self.camvals["vidres"][1] /8)

        # initialise to top left
        self.ui.adjustZoomXYPos.move(0,0)
        
        # set speed 
        self.ui.getSpeed.setValue(self.camvals["zoomSpeed"])
        

        # QUERY do we want to set the actual camera zoom here, same with line after
        # set camera zoom!!!
        self.camera.zoom = self.zoom[:]

        # now we can set the resolution on the camera itself
        self.camera.resolution = (self.camvals["vidres"][0] , self.camvals["vidres"][1] )

    def convertZoomSpeedToLoopSize(self, zoomSpeed):
        return 100 + (8*zoomSpeed)

    def mapXToY(self, value):
        # TODO describe this method
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
        print("in set zoom with button")
        self.setXZoom(x*8)
        y = self.mapXToY(y)
        self.setYZoom(y*8)

    def doScrollZoom(self,val):

        print("in doScrollZoom!")
        gearing = 40
        if val > 1:
            val = self.ui.getZoom.value() + 1*gearing
            self.ui.getZoom.setValue(val)
            self.setZoom(val)
        else:
            val = self.ui.getZoom.value() - 1*gearing
            self.ui.getZoom.setValue(val)
            self.setZoom(val)
        
    def setXZoom(self, val):
        self.zoom[0] = val/self.sensorWidth
        # set camera zoom!!!
        self.camera.zoom = self.zoom[:]

    def setYZoom(self, val):
        self.zoom[1] = val/self.sensorWidth
        # set camera zoom!!!
        self.camera.zoom = self.zoom[:]

    def setZoom(self, val):
        self.zoom[2] = val/self.sensorWidth
        self.zoom[3] = val/self.sensorWidth
        height = self.mapXToY(val)
        self.ui.adjustZoomXYPos.setDragButtonSize(val/8, height/8)
 
        self.camera.zoom = self.zoom[:]

    def setSpeed(self,val):
        self.camvals["zoomSpeed"] = val
        self.loopSize = self.convertZoomSpeedToLoopSize(val) 
        #pass
        print(val)

    def doSetStart(self):
        """
        adds a row to the model and populates it with the current x,y,width,speed and
        pause values.
        Marks the model as dirty """

        self.startZoom = self.zoom[:]
        zdata = [self.startZoom[0], self.startZoom[1], self.startZoom[2], self.camvals["zoomSpeed"], 1.0]
        # insert rows (position, numrows, parent, data)
        self.zTblModel.insertRows(self.zTblModel.rowCount(None),1, self.zTblModel.parent(), zdata)
        # mark the model dirty
        self.zTblModel.dirty = True

    def doNextZoom(self):
        """ flag to say break from inner zoom loop """
        self.nextZoom = True

    def doRestartZoom(self):
        self.restartZoom = True
    
    def playSelectedRows(self):
        """ runs a series of zooms defined with the adjustZoomXYPos, setZoom and speed control widgets"""
        # if icon is 'play' icon
        if self.ui.playRows.text() == u"\u23F5":
            selected = self.ui.zTblView.selectedIndexes()
            # gather rows in a set and then see how many you got
            num_rows = len(set(index.row() for index in selected))
            if num_rows == 0:
                psFunctions.printT(self.window(),"No rows are currently selected!!")
            elif num_rows == 1:
                psFunctions.printT (self.window(),"you need more than just one row to run a zoom")
            else:
                # change from play icon to stop icon
                self.ui.playRows.setText(u"\u23F9")  
                # pass start row and number of rows to new thread
                _thread.start_new_thread(self.outerZoomLoop, (selected[0], num_rows))
        else:
            # if it is stop icon then change to play and stop zoom
            self.ui.playRows.setText(u"\u23F5")
            self.abortZoom = True

    
    def outerZoomLoop(self, startIx, num_rows):  
        """ holds the outer loop that iterates through the rows, then passes off the actual zoom loop
        to the method runMultiZoomLoop """      

        for i in range(startIx.row(), (startIx.row() + num_rows - 1)):
            if self.abortZoom == True:
                self.abortZoom = False
                break
            if self.restartZoom == True:
                self.restartZoom = False
                i = i-1
                break

            myData = self.zTblModel.getZoomData(i)
            self.loopSize = self.convertZoomSpeedToLoopSize(myData[3])
            pause = myData[4]

            # set increments
            xInc = abs(myData[0] - myData[5])/self.loopSize
            yInc = abs(myData[1] - myData[6])/self.loopSize
            zInc = abs(myData[2] - myData[7])/self.loopSize

            startZoom = [
                myData[0], 
                myData[1], 
                myData[2], 
                myData[2]
            ]
            startZoom = startZoom[:]

            endZoom = [
                myData[5], 
                myData[6], 
                myData[7], 
                myData[7]
            ]
            endZoom = endZoom[:]
            # pass on
            self.innerZoomLoop (xInc, yInc, zInc, startZoom, endZoom, self.loopSize, pause) # )

        # outer loop now ended 
        self.ui.playRows.setText(u"\u23F5")
        self.abortZoom = False
    
        if self.camera.recording and self.endRecWithZoom == True:
            self.window().mWidget.doStopVid()

    def innerZoomLoop(self,xInc, yInc, zInc, startZoom, endZoom, loopSize, pause):
        """ iterates a zoom """
        deltaX = 0
        deltaY = 0
        deltaZ = 0
        endZoom = endZoom[:]
        startZoom = startZoom[:]
        zoom = startZoom[:]
        self.camera.zoom = startZoom
        print(loopSize)
        j = 0
        while j < loopSize-1:

            if self.abortZoom == True:
                self.ui.playRows.setText(u"\u23F5")
                break
            if self.nextZoom == True:
                self.nextZoom = False
                psFunctions.printT(self.window(), "Moving to next zoom point")
                break
            if self.restartZoom == True:
                self.restartZoom = False
                psFunctions.printT(self.window(), "Restarting this zoom")
                deltaX = 0
                deltaY = 0
                deltaZ = 0
                endZoom = endZoom[:]
                startZoom = startZoom[:]
                zoom = startZoom[:]
                self.camera.zoom = startZoom
                print(loopSize)
                j = 0

            # pause for a bit
            sleep(1/self.camvals["framerate"])
            
            # if start and end zoom dimension are equal then do nothing
            if startZoom[0] == endZoom[0]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif startZoom[0] < endZoom[0]:
                deltaX  = deltaX + xInc
                if startZoom[0] + deltaX >= endZoom[0]:
                    break
                zoom[0] = startZoom[0] + deltaX
            # otherwise we start high and are decreasing
            else:
                deltaX = deltaX + xInc
                if startZoom[0] - deltaX <= endZoom[0]:
                    break
                zoom[0] = startZoom[0] - deltaX

            # if start = end then do nothing
            if startZoom[1] == endZoom[1]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif startZoom[1] < endZoom[1]:
                deltaY = deltaY + yInc
                if startZoom[1] + deltaY >= endZoom[1]:
                    break
                zoom[1] = startZoom[1] + deltaY
            # otherwise we start high and are decreasing
            else:
                deltaY = deltaY + yInc
                if startZoom[1] - deltaY <= endZoom[1]:
                    break
                zoom[1] = startZoom[1] - deltaY

            # if start and end are equal then do nothing
            if startZoom[2] == endZoom[2]:
                pass
            # if start is smaller than end then we start low and are increasing
            elif startZoom[2] < endZoom[2]:
                deltaZ = deltaZ + zInc
                if startZoom[2] + deltaX >= endZoom[2]:
                    break
                zoom[2] = startZoom[2] + deltaZ
                zoom[3] = startZoom[3] + deltaZ
            # otherwise we start high and are decreasing
            else:
                deltaZ = deltaZ + zInc
                if startZoom[2] - deltaZ <= endZoom[2]:
                    break
                zoom[2] = startZoom[2] - deltaZ
                zoom[3] = startZoom[3] - deltaZ


            self.camera.zoom = zoom[:]
        j = j + 1
        sleep(pause)

    def deleteSelectedRow(self):
        selected = self.ui.zTblView.selectedIndexes()
        num_rows = len(set(index.row() for index in selected))
        if selected:
            self.zTblModel.removeRows(selected[0].row(), num_rows, None)
        self.disableZoomRecordOptionBoxes()
        self.dirty = True

    def isCurrentZoomSelRecordable(self, ix):
        selected = self.ui.zTblView.selectedIndexes()
        # gather rows in a set and then see how many you got
        num_rows = len(set(index.row() for index in selected))
        if num_rows > 1:
            self.window().mWidget.ui.useZoomOnRecord.setEnabled(True)
            self.window().mWidget.ui.endRecWhenZoomEnds.setEnabled(True)
        else:
            self.disableZoomRecordOptionBoxes()
            
    def disableZoomRecordOptionBoxes(self):
            self.window().mWidget.ui.useZoomOnRecord.setChecked(False)
            self.window().mWidget.ui.useZoomOnRecord.setEnabled(False)
            self.window().mWidget.ui.endRecWhenZoomEnds.setChecked(False)
            self.window().mWidget.ui.endRecWhenZoomEnds.setEnabled(False)

    def showThisZoomStart(self, ix):
        """ moves the preview to show the start of the shift-clicked zoom row """
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            myData = self.zTblModel.getZoomData(ix.row(), True)
            myData = myData[:]
            self.camera.zoom = (
                myData[0],
                myData[1],
                myData[2],
                myData[2]
            )
    
#######################################################################################
    #                           END OF CLASS
#######################################################################################


class ZoomTableModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._headers = ["X", "Y", "Width", "speed", "pause"]
        # initialise a list of lists
        self.dirty = False
        self._data = []
        
    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    # handles requests from the view for data
    def data(self, index, role=QtCore.Qt.DisplayRole):
        # original if statement:
        # if role == QtCore.Qt.DisplayRole:
        # Add EditRole so that the cell is not cleared when editing
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):

            value = self._data[index.row()][index.column()]
            if isinstance(value,float):
                return "%.6f" % value
            else:
                return value

    # Additional features methods: 
    def getZoomData(self, row, startOnly=False):
        # we need x,y,w,zoomSpeed,pause,next x, next y, next w i.e 8 items
        thisLoop = []
        for n in range(0,5):
            thisLoop.append(self._data[row][n])
            #print(thisLoop)
        if startOnly == False:
            for n in range(0,3):
                thisLoop.append(self._data[row + 1][n])
                #print(thisLoop)
        
        return tuple(thisLoop)


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
            # TODO I think we have to validate the supplied data here
            # i.e. check that speed is in range 1 to 100
            if index.column() == 3: # if speed
                value = int(value)
                if value > 100:
                    value = 100
                if value < 1:
                    value = 1

            # and pause is float in range what? 0 to 10?
            if index.column() == 4: # if pause
                try:
                    value=float(value)
                except:
                    value = 1.0
                # max pause 10 secs
                if value > 10:
                    value = 10
                value = "%.2f" % value
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            self.dirty = True
            return True
        else:
            return False

    def insertRows(self, position, rows, parent, zdata):
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


