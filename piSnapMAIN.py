# import necessary modules
import sys
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 
from PyQt5 import QAction as qa


class PiSnap(qtw.QMainWindow): #declare a method to initialize empty window
    def __init__(self):  #first initialize the super class QWidget
        super().__init__() #now start drawing the GUI
        self.initUI()
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('PiSnap!')
        self.makeMenu() # run makemenu method 
    def makeMenu(self): #create menu
        #create actions for file menu
        vwopen = QAction('&Open', self)
        vwopen.setShortcut('Ctrl+O')
        vwopen.triggered.connect(lambda: QFileDialog.getOPenFileName(self))
        vwsave = QAction('&Save', self)
        vwsave.setShortcut('Ctrl+S', self)
        vwsave.triggered.connect(self.saveToFile)
        vwsaveas = QAction('Save As', self)
        vwsaveas.setShortcut('Ctrl+Shift+S')
        vwsaveas.triggered.connect()
        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        #create actions for edit menu
        undo = QAction('&Undo',self)
        preferences = QAction('Preferences', self)

        #create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        #create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(vwopen)
        file_menu.addAction(vwsave)
        file_menu.addAction(vwsaveas)
        file_menu.addAction(exit_act)

        #create edit menu and add actions
        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(preferences)
        edit_menu.addAction(undo)
        undo.setShortcut('Ctrl+Z')
        


        self.addWidget()
        self.show()
    def addWidget(parent):
       label = qtw.QLabel('This is a label',parent)

#end of class

    #run the program
if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    window = PiSnap()
    sys.exit(app.exec_())


