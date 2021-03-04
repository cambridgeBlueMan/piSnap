# import necessary modules
import sys
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 

class PiSnap(qtw.QMainWindow): #declare a method to initialize empty window
    def __init__(self):  #first initialize the super class QWidget
        super().__init__() #now start drawing the GUI
        self.initUI()
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('PiSnap!')
        self.makeMenu() # run makemenu method
        self.addMainWidgets()
        self.cw = qtw.QWidget()
        self.setCentralWidget(self.cw)
        self.vlayout = qtw.QVBoxLayout()
        self.cw.setLayout(self.vlayout)
        self.st = qtw.QTabWidget()



        self.show()
    def makeMenu(self): #create menu
        #create actions for file menu
        vwopen = qtw.QAction('&Open', self)
        vwopen.setShortcut('Ctrl+O')
        vwopen.triggered.connect(lambda:qtw.QFileDialog.getOpenFileName(self))
        vwsave = qtw.QAction('&Save', self)
        vwsave.setShortcut('Ctrl+S')
        vwsave.triggered.connect(self.doSave)
        vwsaveas = qtw.QAction('Save As', self)
        vwsaveas.setShortcut('Ctrl+Shift+S')
        vwsaveas.triggered.connect(self.doSaveAs)
        exit_act = qtw.QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        #create actions for edit menu
        undo = qtw.QAction('&Undo',self)
        preferences = qtw.QAction('Preferences', self)

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
    #def makeStatusBar(self): #create status bar
        #self.qtw.SetStatusBar(QStatusBar(self))
        
        self.addWidget()
        
    def addWidget(parent):
       label = qtw.QLabel('This is a label',parent)
       label.setGeometry(200,200,200,200)
    def doSave(self):
        print('Save code here')
    def doSaveAs(self):
        print('Save As code here')
    def addMainWidgets(self):
        print('add main widgets')
    

#end of class

    #run the program
if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    window = PiSnap()
    sys.exit(app.exec_())


