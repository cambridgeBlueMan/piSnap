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
        # set text tplayer controls

        self.ui.getZoom.setInvertedAppearance(True)
        # TODO dont think the next two lines are used?
        self.pixelWidth  = 1/self.sensorWidth
        self.pixelHeight = 1/self.sensorHeight

        #set to bullet point
        self.ui.adjustZoom.setText(u"\u26AB")

        self.ui.playRows.setText(u"\u23F5")
        self.ui.nextZoom.setText(u"\u23ED")
        # initialise flags for playRows
        self.nextZoom = False
        self.abortZoom = False
        self.initControls()

        self.initModelStuff()

    def initModelStuff(self):
        # zoomTableModel is subclassed from QAbstractTableModel, and is at end of this file
        self.model = zoomTableModel()
        # associate the zoomTableView widget with the model
        self.ui.zoomTableView.setModel(self.model)

    def initControls(self):
        # set max value for ui items

        self.zoom = [0,0, self.camvals["vidres"][0] /self.sensorWidth, self.camvals["vidres"][0] /self.sensorWidth]
        self.startZoom = self.zoom[:]
        self.endZoom = self.zoom[:]
        #  minimum is set in designer at 1920 (HD) , max is set in designer at 3470 
        self.ui.getZoom.setMinimum(self.camvals["vidres"][0] )
        # QUERY should the following be set to max rather than min?
        self.ui.getZoom.setValue(self.camvals["vidres"][0] )
        #get the name pf the speed object and set its vaue to the camvals value as per above
        self.ui.getSpeed.setValue(self.camvals["loopSize"])
        # dragbutton size varies according to the current res
        self.ui.adjustZoom.setDragButtonSize(self.camvals["vidres"][0] /8, self.camvals["vidres"][1] /8)
        # QUERY if previous QUERY is set to max then drag button size should be the following
        #self.ui.adjustZoom.setDragButtonSize(self.sensorWidth/8, self.sensorHeight/8)

        self.ui.adjustZoom.move(0,0)
        # QUERY do we want to set the actual camera zoom here, same with line after
        # set camera zoom!!!
        self.camera.zoom = self.zoom
        # now we can set the resolution on the camer itself
        self.camera.resolution = (self.camvals["vidres"][0] , self.camvals["vidres"][1] )

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
        self.setXZoom(x*8)
        y = self.mapXToY(y)
        self.setYZoom(y*8)
        
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
        self.ui.adjustZoom.setDragButtonSize(val/8, height/8)

       
        self.camera.zoom = self.zoom[:]
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
        zdata = [self.startZoom[0], self.startZoom[1], self.startZoom[2], 600, 1.0]
        # insert rows (position, numrows, parent, data)
        self.model.insertRows(self.model.rowCount(None),1, self.model.parent(), zdata)

    def doNextZoom(self):
        print ("in next zoom")
        self.nextZoom = True
    
    
        # get the currently selected rows from the table
    def playSelectedRows(self):
        """ runs a series of zooms defined with the adjustZoom, setZoom and speed control widgets"""
        print ("&&&&&&&&&&&&&&&&&&&", self.ui.playRows.text())
        # if icon is 'play' icon
        if self.ui.playRows.text() == u"\u23F5":
            selected = self.ui.zoomTableView.selectedIndexes()
            # gather rows in a set and then see how many you got
            num_rows = len(set(index.row() for index in selected))
            if num_rows == 0:
                psFunctions.printT(self.window(),"No rows are currently selected!!")
            elif num_rows == 1:
                psFunctions.printT (self.window(),"you need more than just one row to run a zoom")
            else:
                # run the zoom in a new thread
                startRow = selected[0].row()
                # change from play icon to stop icon
                self.ui.playRows.setText(u"\u23F9")
                print("££££££££££££££££££££££££££££££££££££")   
                # pass start row and number of rows to new thread
                _thread.start_new_thread(self.runZoomLoops, (startRow, num_rows))
        else:
            self.ui.playRows.setText(u"\u23F5")
            self.abortZoom = True

    def showStartPoint(self, ix):
        print(self.model._data[ix][0],self.model._data[ix][1],self.model._data[ix][2])
        #self.ui.adjustZoom.x = self.model._data[ix][0]
        #self.ui.adjustZoom.y = self.model._data[ix][1]
        #self.ui.getZoom.setValue(self.model._data[ix][2])
        self.camera.zoom = (
            self.model._data[ix][0],
            self.model._data[ix][1],
            self.model._data[ix][2],
            self.model._data[ix][2]
        )
    def showEndPoint(self, ix):
        self.camera.zoom = (
        self.model._data[ix+1][0],
        self.model._data[ix+1][1],
        self.model._data[ix+1][2],
        self.model._data[ix+1][2]
        )
        

    def runZoomLoops(self, startRow, num_rows):  
        """ holds the outer loop that iterates through the rows, then passes off the actual zoom loop
        to the method runMultiZoomLoop """      

        for ix in range(startRow, (startRow + num_rows)):
            if self.abortZoom == True:
                self.abortZoom = False
                break

            # increment for each step
            #print("actual ix: ", ix)
            #print("ix", self.model._data[ix])
            #print("nextRow", self.model._data[ix+1])
            loopSize = self.model._data[ix][3] 
            pause = self.model._data[ix][4]
            
            xInc = abs(self.model._data[ix][0] - self.model._data[(ix + 1)][0])/loopSize
            yInc = abs(self.model._data[ix][1] - self.model._data[(ix + 1)][1])/loopSize
            zInc = abs(self.model._data[ix][2] - self.model._data[(ix + 1)][2])/loopSize

            startZoom = [
                self.model._data[ix][0], 
                self.model._data[ix][1], 
                self.model._data[ix][2], 
                self.model._data[ix][2]
            ]
            startZoom = startZoom[:]

            endZoom = [
                self.model._data[ix+1][0], 
                self.model._data[ix+1][1], 
                self.model._data[ix+1][2], 
                self.model._data[ix+1][2]
            ]
            endZoom = endZoom[:]

            self.runMultiZoomLoop (xInc, yInc, zInc, startZoom, endZoom, loopSize, pause) # )

        # outer loop now ended 
        self.ui.playRows.setText(u"\u23F5")
        
        if self.camera.recording:
            self.window().mWidget.doStopVid()
            print("now in if")

    def runMultiZoomLoop(self,xInc, yInc, zInc, startZoom, endZoom, loopSize, pause):
        deltaX = 0
        deltaY = 0
        deltaZ = 0
        startZoom = startZoom[:]
        endZoom = endZoom[:]
        self.camera.zoom = startZoom

        for j in range(loopSize):
            if self.abortZoom == True:
                self.abortZoom = False
                break
            if self.nextZoom == True:
                self.nextZoom = False
                psFunctions.printT(self.window(), "Moving to next zoom point")
                break
            #print(j)
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
        #print("loop now ended")
        #self.ui.runZoom.setText("run zoom")
        #self.ui.runZoom.toggle() #abortZoom = False

        """  #loop now ended 
        if self.camera.recording:
            self.window().mWidget.doStopVid()
            print("now in if")
        
        """
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


    def showThisZoomStart(self, ix):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            #print('Shift+Click')
            self.showStartPoint(ix.row())
            #print(ix.row()
        elif modifiers == QtCore.Qt.ControlModifier:
            #print('Control+Click')
        #elif modifiers == QtCore.Qt.AlternateModifier:
        #    print('Alternate+Click')
        
        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            #print('Control+Shift+Click')
            if ix.row()+1 < len(self.model._data):
                self.showStartPoint(ix.row()+1)
            else:
                psFunctions.printT(self.window(), "No end set yet for this zoom")
        #else:
        #    print('Click')

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


