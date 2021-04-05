from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

class DragButton(qtw.QPushButton):
    posChanged = qtc.pyqtSignal(int,int)
    global newPos
    def __init__(self, win):
        super().__init__(win)
        self.setText(u'\u26ab')
        self.setFixedSize(22, 22)
        self.containerWidth = win.frameGeometry().width()
        self.containerHeight = win.frameGeometry().height()
        qtc.QMetaObject.connectSlotsByName(self)

    def setContainerSize(self, x, y):
        self.containerWidth = x
        self.containerHeight = y

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
            if newPos.x() > (self.containerWidth -22):
                x = (self.containerWidth - 22)
            elif newPos.x() < 0:
                x = 0
            else:
                x = newPos.x()
            # get the y val
            if newPos.y() > (self.containerHeight - 22):
                y = (self.containerHeight - 22)
            elif newPos.y() < 0:
                y = 0
            else:
                y = newPos.y()
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