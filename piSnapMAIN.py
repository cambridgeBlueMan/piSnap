# import necessary modules
import sys
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 

print('line6')
class PiSnap(qtw.QMainWindow): #declare a method to initialiZe empty window
    def __init__(self):  #first initialize the sper class QWidget
        super().__init__() #now start drawing the GUI
        self.initUI()
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('PiSnap!')
        self.addWidget()
        self.show()
    def addWidget(self):
       label = qtw.QLabel('This is a label',self)

#end of class

    #run the program
if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    window = PiSnap()
    sys.exit(app.exec_())


