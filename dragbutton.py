from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

# there is code at bottom to implement a double click functionality
class DragButton(qtw.QPushButton):
    posChanged = qtc.pyqtSignal(int,int)
    global newPos
    def __init__(self, win, bWidth = 22, bHeight = 22):
        # win is the containing window
        # bullet width and height
        self.bWidth = bWidth
        self.bHeight = bHeight
        # win is the containing frame or widget
        super().__init__(win)
        self.setText(u'\u26ab')
        # we may want to make fixedSize settable. a method setDragButtonSize
        self.setFixedSize(self.bWidth, self.bHeight)
        #get frame size so that we can constrain the drgbuttons movements
        self.containerWidth = win.frameGeometry().width()
        self.containerHeight = win.frameGeometry().height()
        qtc.QMetaObject.connectSlotsByName(self)

    def setContainerSize(self, x, y):
        self.containerWidth = x
        self.containerHeight = y

    def setDragButtonSize(self,w,h):
        self.setFixedSize(w,h)
        self.bWidth = w
        self.bHeight = h


    # mousePressEevent
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == qtc.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        global newPos
        if event.buttons() == qtc.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos

            newPos = self.mapFromGlobal(currPos + diff)
            #print(newPos)
            # get the x val
            if newPos.x() > (self.containerWidth -self.bWidth):
                x = (self.containerWidth - self.bWidth)
            elif newPos.x() < 0:
                x = 0
            else:
                x = newPos.x()
            # get the y val
            if newPos.y() > (self.containerHeight - self.bHeight):
                y = (self.containerHeight - self.bHeight)
            elif newPos.y() < 0:
                y = 0
            else:
                y = newPos.y()
            #print(x,y)
            self.sendPos((x,y))

            self.move(x,y)
            self.__mouseMovePos = globalPos
        super(DragButton, self).mouseMoveEvent(event)

    def moveButtonToOrigin(self):
        self.move(0,0)

    def sendPos(self, pos):
        #print(pos)
        self.posChanged.emit(pos[0], pos[1])

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(DragButton, self).mouseReleaseEvent(event)

def clicked():
    pass

if __name__ == "__main__":
    app = qtw.QApplication([])
    w = qtw.QWidget()
    w.resize(800,600)

    button = DragButton("Drag", w)
    button.clicked.connect(clicked)

    w.show()
    app.exec_()

    """
    import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.button = QDoublePushButton("Test", self)
        self.button.clicked.connect(self.on_click)
        self.button.doubleClicked.connect(self.on_doubleclick)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.resize(120, 50)
        self.show()

    @pyqtSlot() 
    def on_click(self):
        print("Click")

    @pyqtSlot()
    def on_doubleclick(self):
        print("Doubleclick")

app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())
    """