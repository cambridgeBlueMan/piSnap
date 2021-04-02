# import necessary modules
import sys
import json
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 

from qualityTab import QualityTab
from adjustmentsTab import Adjustments
from shooter import PSSnapper
from adjustmentsTab import Adjustments
from psSettings import PSSettings
from psPiCamera import PSPiCamera
#from picamera import PiCamera

class PiSnap(qtw.QMainWindow): #declare a method to initialize empty window
    def __init__(self):  #first initialize the super class QWidget
        super().__init__() 
        # get the settings
        self.camera = PSPiCamera(self)
        # pass the main window and camera objects to a settings object
        self.settings = PSSettings(self, self.camera)
        self.camvals = self.settings.camvals
        #now start drawing the GUI
        self.initUI()
    def closeEvent(self, event):
        """
        overrides closEvent of QWidget, so we can save the
        settings file before we quit
        :param event:
        :return:
        """
        reply = qtw.QMessageBox.question(self, 'Window Close', 'Do you want to save the settings file?',
                                     qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)

        if reply == qtw.QMessageBox.Yes:
            x = json.dumps(self.camvals, indent=4)
            with open('settings.json', 'w') as f:
                f.write(x)
                f.close()
        event.accept()

      

    def initUI(self):
        self.setWindowTitle('PiSnap!')
        self.makeMenu() # run makemenu method
        self.makeStatusBar()
        self.addMainWidgets() 
        self.setWidgetSizes()
        self.show()

    def makeStatusBar(self):
        self.statusBar = qtw.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('This is a status bar')
        self.statusBarPreviewCheckBox = qtw.QCheckBox()
        self.statusBar.addPermanentWidget(self.statusBarPreviewCheckBox)
        self.statusBarPreviewCheckBox.setText("Show preview")

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

    def doSave(self):
        print('Save code here')

    def doSaveAs(self):
        print('Save As code here')

    def addMainWidgets(self):
        ##########################################################
        #             DEFINE THE CONTAINER BOXES
        ##########################################################
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

        # 
        ##########################################################
        #    DEFINE A SNAPPER OBJECT TO BE THE CENTRAL WIDGET
        ##########################################################
        # set a central widget

        # make a dummy widget
        """ self.dummy = qtw.QPlainTextEdit()
        self.dummy.setStyleSheet("background-color:green;")
        # add the dummy widget to the horizontal layout
        self.hlayout.addWidget(self.dummy) """
        
        #print(self.hlayout)
        self.mWidget = PSSnapper(self.settings.camvals, self.camera)
        # self.mWidget = qtw.QWidget(self)
        #self.statusBarPreviewCheckBox.stateChanged.connect(self.mWidget.showPreview(self.mWidget, True))

        #print(self.mWidget)
        self.hlayout.addWidget(self.mWidget)
        # add it to the settings registry
        self.settings.registerWidget(self.mWidget)


        ############################################################
        # MAKE THE VERTICAL STUFF: TAB WIDGET AND PLAIN TEXT WIDGET
        ############################################################

        # now add the stuff to the vertical layout
        # first make the settings QTab widget
        self.settingsWidget = qtw.QTabWidget()

        # now make and add ththe terminal window
        self.terminalWidget = qtw.QPlainTextEdit()
        self.terminalWidget.setStyleSheet("background-color:black;color:SpringGreen;")
        self.vlayout.addWidget(self.settingsWidget)
        self.vlayout.addWidget(self.terminalWidget)

        ############################################################
        # ADD VARIIOUS TABS TO THE TAB WIDGET
        ############################################################

        # #################################################################
        # make a quality tab widget, and pass the settings dictionary to it
        self.qualityTab = QualityTab(self.settings.camvals, self.camera)
        # now register it to the settings class
        self.settings.registerWidget(self.qualityTab)
        # now add it to the tab
        self.settingsWidget.addTab(self.qualityTab,"Quality")

        # ##################################################################
        # make a brightness object and do the same 
        self.adjustmentsTab = Adjustments(self.settings.camvals, self.camera)
        self.settings.registerWidget(self.adjustmentsTab)
        self.settingsWidget.addTab(self.adjustmentsTab, "Adjustments")  




    def setWidgetSizes(self):
        self.settingsWidget.setMinimumHeight(750)
        self.settingsWidget.setMinimumWidth(400)
        self.mWidget.setMinimumWidth(1300)
        self.terminalWidget.setMinimumHeight(200)
    

    #end of class

#run the program
if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    window = PiSnap()
    sys.exit(app.exec_())

