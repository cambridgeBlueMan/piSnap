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
from zoomTab import ZoomTab
from keyboardslider import KeyboardSlider
from psSettings import PSSettings
from psPiCamera import PSPiCamera
from quit import Quit
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
        ##################################  WHATS THIS?????????
        self.setObjectName("pisnapApp")
        ####################################
        self.initUI()
    def closeEvent(self, event):
        """
        overrides closEvent of QWidget, so we can save the
        settings file before we quit
        :param event:
        :return:
        """
        self.camera.stop_preview()
        
        """ quit = qtw.QDialog(self)
        ui = Quit()
        ui.setupUi(quit)                        
        quit.setModal(True)
        quit.show() """
        reply = qtw.QMessageBox.question(self, 'Window Close', 'Do you want to save the settings file?',
                                     qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)

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
        #print(self.mWidget)
        #self.previewVisible.clicked.connect(Form.showPreview)

        self.show()

    def makeStatusBar(self):
        self.statusBar = qtw.QStatusBar()
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('This is a status bar')
        self.statusBarPreviewCheckBox = qtw.QCheckBox()
        self.statusBar.addPermanentWidget(self.statusBarPreviewCheckBox)
        self.statusBarPreviewCheckBox.setText("Show preview")
        self.statusBarPreviewCheckBox.setObjectName("statusBarPreviewCheckBox") 

        # processsing for preview check box


    def makeMenu(self): #create menu
        #create actions for file menu
        openAction = qtw.QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(lambda:qtw.QFileDialog.getOpenFileName(self))
        saveAction = qtw.QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.doSave)
        saveAsAction = qtw.QAction('Save As', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.triggered.connect(self.doSaveAs)
        exitAction = qtw.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        #create actions for edit menu
        undoAction = qtw.QAction('&Undo',self)
        prefsAction = qtw.QAction('Preferences', self)

        #create menubar
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)

        #create file menu and add actions
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(exitAction)

        #create edit menu and add actions
        editMenu= menuBar.addMenu('&Edit')
        editMenu.addAction(prefsAction)
        editMenu.addAction(undoAction)
        undoAction.setShortcut('Ctrl+Z')

        #create preview menu and add actions
        previewMenu = menuBar.addMenu('&Preview')
        self.visibleAction = qtw.QAction('&Visible',self)
        self.visibleAction.setObjectName("visibleAction")
        previewMenu.addAction(self.visibleAction)
        self.visibleAction.setShortcut('Ctrl+P')
        self.visibleAction.setCheckable(True)
        #self.visibleAction.toggled.connect(self.mWidget.showPreview)
        #visibleAction.triggered.connect(self.mWidget.showPreview)
        alpha255Action = qtw.QAction('&255%', self)
        previewMenu.addAction(alpha255Action)
        alpha255Action.setShortcut('255')
        alpha255Action.triggered.connect(lambda:self.setPreviewAlpha(255))
        alpha75Action = qtw.QAction('&75%', self)
        previewMenu.addAction(alpha75Action)
        alpha75Action.setShortcut('7')
        alpha75Action.triggered.connect(lambda:self.setPreviewAlpha(75))
        alpha50Action = qtw.QAction('&50%', self)
        previewMenu.addAction(alpha50Action)
        alpha50Action.setShortcut('5')
        alpha50Action.triggered.connect(lambda:self.setPreviewAlpha(50))
        alpha25Action = qtw.QAction('&25%', self)
        previewMenu.addAction(alpha25Action)
        alpha25Action.setShortcut('2')
        alpha25Action.triggered.connect(lambda:self.setPreviewAlpha(25))
        

    def doSave(self):
        print('Save code here')

    def setPreviewAlpha(self,val):
        try:
        #print('alpha')
            self.camera.preview.alpha=val
        except: 
            self.terminalWidget.appendPlainText("Preview not currently active!")

    def doSaveAs(self):
        print('Save As code here')

    def addMainWidgets(self):
        ##########################################################
        #             DEFINE THE CONTAINER BOXES
        ##########################################################
        # set a central widget
        self.centralWidget = qtw.QWidget()
        self.centralWidget.setObjectName("centralWidget")
        print("central widget", self.centralWidget)
        self.setCentralWidget(self.centralWidget)
        # define some layouts
        self.hlayout = qtw.QHBoxLayout()
        self.hlayout.setObjectName("hlayout")
        self.vlayout = qtw.QVBoxLayout()
        self.vlayout.setObjectName("vlayout")
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
        self.mWidget.setObjectName("mWidget")
        self.statusBarPreviewCheckBox.clicked.connect(self.mWidget.showPreview)
        self.visibleAction.toggled.connect(self.mWidget.showPreview)
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
        self.terminalWidget.setStyleSheet("background-color:#252526;color:SpringGreen;")
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

        # ##################################################################
        # make a zoomer object
        self.zoomTab = ZoomTab(self.settings.camvals, self.camera)
        self.settings.registerWidget(self.zoomTab)
        self.settingsWidget.addTab(self.zoomTab, "Zooming Tool")  

       





    def setWidgetSizes(self):
        self.settingsWidget.setMinimumHeight(700)
        self.settingsWidget.setMinimumWidth(510)
        self.mWidget.setMinimumWidth(1300)
        self.terminalWidget.setMinimumHeight(200)
    

    #end of class

#run the program
if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    window = PiSnap()
    print("main window", window)
    sys.exit(app.exec_())

