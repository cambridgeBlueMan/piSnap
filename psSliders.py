"""
Two classes used to provide composite sliders. One as a dial the other as a horizontal slider.
Each slider has an associated spin box to show the current value. Updates to one control automatically
update the other control. values are then passed to the main window to allow camera settings to be made
and the settings dictionary to be updated
"""
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class CompositeSlider(qtw.QWidget):
    lnValueChanged =  qtc.pyqtSignal(int)
    global lnMin, lnMax, lnDefault
    def __init__(self, parent):
        """Composite slider comprises a coupled slider and spinBox; and
        a reset button 
        """
        super().__init__(parent)
        # Main UI code goes here

        # set widget size
        self.setFixedSize(qtc.QSize(300, 60))

        # make slider, set size
        self.slider = qtw.QSlider(self)
        self.slider.setFixedSize((qtc.QSize(190, 55)))
        self.slider.setOrientation(qtc.Qt.Horizontal)
        # name slider (is this necessary?)
        self.slider.setObjectName("slider")

        # make spinbox, set size
        self.spinBox = qtw.QSpinBox(self)
        self.spinBox.setFixedSize((qtc.QSize(50, 48)))
        # position it
        self.spinBox.move(190, 7)
        # name it. necessary?
        self.spinBox.setObjectName("spinBox")
        # make a button
        self.button = qtw.QPushButton('r', self)
        self.button.setFixedSize(qtc.QSize(20,45))
        self.button.move(245, 7)
        # connect internal signals and slots
        self.slider.valueChanged['int'].connect(self.spinBox.setValue)
        self.spinBox.valueChanged['int'].connect(self.slider.setValue)
        # connect external 
        self.spinBox.valueChanged['int'].connect(self.sendValue)
        #self.slider.valueChanged[int].connect(Dialog
        self.button.clicked.connect(self.reset)
        qtc.QMetaObject.connectSlotsByName(self)

        # show it
        self.show()

    def sendValue(*args):
        args[0].lnValueChanged.emit(args[1])

    def setRanges(self, min, max, default):
        self.spinBox.setMinimum(min)
        self.spinBox.setMaximum(max)
        self.spinBox.setValue(default)
        
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(default)
        
        self.lnMin = min
        self.lnMax = max
        self.lnDefault = default
    
    def reset(self):
        self.spinBox.setValue(self.lnDefault)
        self.slider.setValue(self.lnDefault)
        #self.setRanges(self, self.lnMin, self.lnMax, self.lnDefault)
        


class DDPlayerWindow(qtw.QLabel):                       # - QWidget    + QLabel
    def __init__(self, parent):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
        #self.setText(" Accept Drops")
        #self.setStyleSheet("QLabel { background-color : #ccd; color : blue; font-size: 20px;}")

    def dragEnterEvent(self, e):
        print("DragEnter")
        e.accept()

    def dragMoveEvent(self, e):
        print("DragMove")
        e.accept()

    def dropEvent(self, e):
        print("DropEvent")
        #print (type(e))
        #print(dir(e.mimeData().dumpObjectInfo()))
        #print(dir(e.mimeData().isWidgetType()))


        #print ("Mime data: ", e.mimeData())
        position = e.pos()
        print(position)
        print(e.mimeData().text())

        #self.setText(e.mimeData().text())                #  +++
        print(e.dropAction)
        e.setDropAction(qtc.Qt.MoveAction)                   #  +++

        e.accept()
"""
class CompositeDial(qtw.QAbstractSlider):

    def __init__(self, parent):

        super().__init__(parent)
        # Main UI code goes here

        # set widget size
        self.setFixedSize(qtc.QSize(40,60))
        print("hello everybody!")
        # make slider, set size
        self.slider = qtw.QDial(self)
        self.slider.setFixedSize((qtc.QSize(55,55)))
        # name slider (is this necessary?)
        self.slider.setObjectName("slider")

        # make spinbox, set size
        self.spinBox = qtw.QSpinBox(self)
        self.spinBox.setFixedSize((qtc.QSize(20, 20)))
        # position it
        self.spinBox.move(70,7)
        # name it. necessary?
        self.spinBox.setObjectName("spinBox")
        
        self.button = qtw.QPushButton(self)
        self.button.setFixedSize(qtc.QSize(55,55))
        self.button.show()
        # connect signals and slots
        self.slider.valueChanged['int'].connect(self.spinBox.setValue)
        self.spinBox.valueChanged['int'].connect(self.slider.setValue)

        self.slider.valueChanged['int'].connect(self.doWork)
        self.spinBox.valueChanged['int'].connect(self.doWork)
        qtc.QMetaObject.connectSlotsByName(self)

        # show it
        self.show()
    
    def doWork(*args):
        print(args[0].sender())
        print(args[1])
        #args[0].parent().parent().updateCameraSettings(args[0].objectName(), args[1])
        return args[1]
        pass

    def setRanges (self, min, max, default):

        self.spinBox.setMinimum(min)
        self.spinBox.setMaximum(max)
        self.spinBox.setValue(default)

        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(default)

"""

class DDPlayerWindow(qtw.QLabel):                       # - QWidget    + QLabel
    def __init__(self, parent):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
        #self.setText(" Accept Drops")
        #self.setStyleSheet("QLabel { background-color : #ccd; color : blue; font-size: 20px;}")

    def dragEnterEvent(self, e):
        print("DragEnter")
        e.accept()

    def dragMoveEvent(self, e):
        print("DragMove")
        e.accept()

    def dropEvent(self, e):
        print("DropEvent")
        #print (type(e))
        #print(dir(e.mimeData().dumpObjectInfo()))
        #print(dir(e.mimeData().isWidgetType()))


        #print ("Mime data: ", e.mimeData())
        position = e.pos()
        print(position)
        print(e.mimeData().text())

        #self.setText(e.mimeData().text())                #  +++
        print(e.dropAction)
        e.setDropAction(qtc.Qt.MoveAction)                   #  +++

        e.accept()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = CompositeSlider()
    sys.exit(app.exec())
