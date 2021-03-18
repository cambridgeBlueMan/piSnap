from PyQt5 import QtCore, QtGui, QtWidgets


class DragButton(QtWidgets.QPushButton):

    """ ok, so we start by inheriting from QPushButton """
    global newPos
    # mousePressEevent
    def mousePressEvent(self, event):
        print(type(event))
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        global newPos
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos

            newPos = self.mapFromGlobal(currPos + diff)
            print(newPos)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                print(newPos.x())
                return
            print(newPos)
        super(DragButton, self).mouseReleaseEvent(event)

def clicked():
    print ("click as normal!")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = QtWidgets.QWidget()
    w.resize(800,600)

    button = DragButton("Drag", w)
    button.clicked.connect(clicked)

    w.show()
    app.exec_()