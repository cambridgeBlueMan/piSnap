# import necessary modules
import sys
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 

from qualityTabMAIN import QualityTab
from cameraAppMAIN import MainWindow
from cameraSettings import CameraSettings
from myCamera import MyCamera
#from picamera import PiCamera

class PiSnap(qtw.QMainWindow): #declare a method to initialize empty window
    def __init__(self):  #first initialize the super class QWidget
        super().__init__() 
        # get the settings
        self.camera = MyCamera(self)
        # pass the main window and camera objects to a settings object
        self.settings = CameraSettings(self, self.camera)
        #now start drawing the GUI
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('PiSnap!')
        self.makeMenu() # run makemenu method
        self.addMainWidgets()
        self.setWidgetSizes()
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

    def doSave(self):
        print('Save code here')

    def doSaveAs(self):
        print('Save As code here')

    def addMainWidgets(self):
        # set a central widget
        self.centralWidget = qtw.QWidget()
        self.setCentralWidget(self.centralWidget)
        # define some layouts
        self.hlayout = qtw.QHBoxLayout()
        self.vlayout = qtw.QVBoxLayout()
        # set the horizontal layout as the central widget
        self.centralWidget.setLayout(self.hlayout)
        # add the vertical layout to the horizontal layout
        self.hlayout.addLayout(self.vlayout)

        """ # make a dummy widget
        self.dummy = qtw.QPlainTextEdit()
        self.dummy.setStyleSheet("background-color:green;")
        # add the dummy widget to the horizontal layout
        self.hlayout.addWidget(self.dummy)

         """
        self.mainWidget = MainWindow(self.settings.camvals)
        self.hLayout.addWidget(mainWidget)
        # now add the stuff to the vertical layout
        # first make the settings QTab widget
        self.settingsWidget = qtw.QTabWidget()
        # make a quality tab widget, and pass the settings dictionary to it
        self.qualityTab = QualityTab(self.settings.camvals)
        # now register it to the settings class
        self.settings.registerWidget(self.qualityTab)
        # now add it to the tab
        self.settingsWidget.addTab(self.qualityTab,"Quality")
        # now make and add ththe terminal window
        self.terminalWidget = qtw.QPlainTextEdit()
        self.terminalWidget.setStyleSheet("background-color:black;color:SpringGreen;")
        self.vlayout.addWidget(self.settingsWidget)
        self.vlayout.addWidget(self.terminalWidget)
    def setWidgetSizes(self):
        self.settingsWidget.setMinimumHeight(750)
        self.settingsWidget.setMinimumWidth(400)
        self.dummy.setMinimumWidth(1300)
        self.terminalWidget.setMinimumHeight(200)
    

    #end of class

#run the program
if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    window = PiSnap()
    sys.exit(app.exec_())

