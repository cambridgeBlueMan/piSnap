#!/usr/bin/python3
# import necessary modules
import sys
import json
import pickle
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from qualityTab import QualityTab
from adjustmentsTab import Adjustments
from resolutionsTab import ResolutionsTab
from shooter import Shooter
from adjustmentsTab import Adjustments
from zoomTab import ZoomTab
from keyboardslider import KeyboardSlider
from psSettings import PSSettings
#from picamera import PiCamera
import picamera
from quit import Quit
from preferences import Preferences
import psFunctions
#from picamera import PiCamera

class PiSnap(qtw.QMainWindow): #declare a method to initialize empty window
    def __init__(self):  #first initialize the super class QWidget
        super().__init__() 
        # get the settings
        # VICKY put try statement in to catch lack of a camera!
        try:
            self.camera = picamera.PiCamera()
        except picamera.PiCameraError as err:
            print(err)
            print('======================================================================')
            print('This error can be caused if no camera is attached to the Raspberry Pi!')
            print('======================================================================')
            sys.exit()
        except picamera.PiCameraMMALError:
            print('======================================================================')
            print('Camera already in use! Please close relevant application and try again')
            print('======================================================================')
            
            sys.exit()
        # pass the main window and camera objects to a settings object
        self.settings = PSSettings(self, self.camera)
        self.camvals = self.settings.camvals
        #now start drawing the GUI
        ##################################  WHATS THIS?????????
        self.setObjectName("pisnapApp")
        ####################################
        self.initUI()
        # if focus changes then deal with the preview appropriately
        app.focusChanged.connect(self.on_focusChanged)

    def on_focusChanged(self, then, now):
        """
        turn on or off the preview depending on whether the app has focus 
        and whether preview is active 

        """
        if then == None or now == None:
            if self.isActiveWindow():
                if self.mWidget.ui.previewVisible.isChecked():
                    self.mWidget.showPreview(True)
            else:
                if now == None:
                    if self.mWidget.ui.previewVisible.isChecked():
                        self.mWidget.camera.stop_preview()   

    def moveEvent(self, e):
        # if the preview is currently visibe
        if self.statusBarPreviewCheckBox.isChecked():
            # stop it!
            self.mWidget.showPreview(False)
            # then call showPreview so pos can update
            self.mWidget.showPreview(True)

        #print(self.pos())
        super(PiSnap, self).moveEvent(e)



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
                                     qtw.QMessageBox.Cancel | qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.Yes)

        if reply == qtw.QMessageBox.Yes:
            x = json.dumps(self.camvals, indent=4)
            with open('settings.json', 'w') as f:
                f.write(x)
                f.close() 
                self.camera.close()
                event.accept()
        if reply == qtw.QMessageBox.No:
            self.camera.close()
            event.accept()
        if reply == qtw.QMessageBox.Cancel:
            # TODO if preview was on then turn it back on 
            event.ignore()
        
      

    def initUI(self):
        self.setWindowTitle('PiSnap!')
        self.makeMenu() # run makemenu method
        self.makeStatusBar()
        self.addMainWidgets() 
        self.setWidgetSizes()
        #print(self.mWidget)
        #self.previewVisible.clicked.connect(Form.showPreview)

        self.show()
        #print("end init")
        
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
        openAction = qtw.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(lambda:qtw.QFileDialog.getOpenFileName(self))
        
        saveAction = qtw.QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.doSave)
        
        saveAsAction = qtw.QAction('Save As', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.triggered.connect(self.doSaveAs)

        saveZoomAction = qtw.QAction('Save &zoom', self)
        saveZoomAction.setShortcut('Ctrl+Z')
        saveZoomAction.triggered.connect(self.doSaveZoom)

        openZoomAction = qtw.QAction('&Open zoom', self)
        openZoomAction.setShortcut('Ctrl+Shift+Z')
        openZoomAction.triggered.connect(self.doOpenZoom)

    

        
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
        fileMenu.addAction(openZoomAction)
        fileMenu.addAction(saveZoomAction)
        fileMenu.addAction(exitAction)

        #create edit menu and add actions
        editMenu= menuBar.addMenu('&Edit')
        editMenu.addAction(prefsAction)
        editMenu.addAction(undoAction)
        undoAction.setShortcut('Ctrl+Z')
        prefsAction.triggered.connect(self.openPreferencesDialogue)

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

    def openPreferencesDialogue(self):
        self.prefs=Preferences(self,self.camvals,self.camera)
        self.prefs.show()
        print(self.prefs)

    def doOpenZoom(self):
        # TODO falls over if no file selected
        # you need to check the data cell by cell for validity, I suspect       
        
        filename = qtw.QFileDialog.getOpenFileName(
            self,
            "Open a zoom file...",
            qtc.QDir.homePath(),
            "Zoom Files (*.zoom)"
        )
        if filename:
            with open(filename[0], "rt") as fp:   # Unpickling
                zoomData = json.load(fp)
                print(zoomData)

            # TODO apply the current res got from the file to the app
            # possibly convert to json rather than pickle
            self.camvals["vidres"]=zoomData[0]
            self.resolutionsTab.applySettings()
            print("length of zoomData: ", len(zoomData))
            #self.zoomTab.model.insertRows(self.zoomTab.model.rowCount(None),len(zoomData), self.zoomTab.model.parent(), zoomData)
            for item in zoomData[1]:
                # insert rows (position, numrows, parent, data)
                self.zoomTab.zTblModel.insertRows(self.zoomTab.zTblModel.rowCount(None),1, self.zoomTab.zTblModel.parent(), item)
            self.zoomTab.zTblModel.dirty = True
    def doSaveZoom(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Select the file to save to…",
            qtc.QDir.homePath(),
            'Zoom files (*.zoom)'
        )
        if filename:
            try:
                #res = json.dumps(self.camvals["vidres"])
                data = json.dumps([self.camvals["vidres"], self.zoomTab.zTblModel._data])
                with open(filename, 'w') as fp:
                    fp.write(data)
                    fp.close()  

                self.zoomTab.zTblModel.dirty = False
            except Exception as e:
                # Errata:  Book contains this line:
                #qtw.QMessageBox.critical(f"Could not save file: {e}")
                # It should read like this:
                print("bloto bloto!", e)
                #qtw.QMessageBox.critical(self, f"Could not load file: {e}")
        #with open("test.zoom", "wb") as fp:   #Pickling
        #    pickle.dump(self.zoomTab.model._data, fp)
        

    def doSave(self):
        print('Save code here')

    def setPreviewAlpha(self,val):
        try:
        #print('alpha')
            self.camera.preview.alpha=val
        except: 
            psFunctions.printT(self, "Preview not currently active!")
            #self.terminalWidget.appendPlainText("Preview not currently active!")

    def doSaveAs(self):
        print('Save As code here')

    def addMainWidgets(self):
        ##########################################################
        #             DEFINE THE CONTAINER BOXES
        ##########################################################
        # set a central widget
        self.centralWidget = qtw.QWidget()
        self.centralWidget.setObjectName("centralWidget")
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
        self.mWidget = Shooter(self.settings.camvals, self.camera)
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
        self.settingsWidget.setObjectName("settingsWidget")

        # now make and add ththe terminal window
        self.terminalWidget = qtw.QPlainTextEdit()
        self.terminalWidget.setReadOnly(True)
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

        # #################################################################
        # make a resolutions tab widget, and pass the settings dictionary to it
        self.zoomTab = ZoomTab(self.settings.camvals, self.camera)
        self.resolutionsTab = ResolutionsTab(self.settings.camvals, self.camera, self.centralWidget, self.zoomTab)
        # now register it to the settings class
        self.settings.registerWidget(self.resolutionsTab)
        # now add it to the tab
        self.settingsWidget.addTab(self.resolutionsTab,"Resolutions")


        # ##################################################################
        # make a brightness object and domWidget" the same 
        self.adjustmentsTab = Adjustments(self.settings.camvals, self.camera)
        self.settings.registerWidget(self.adjustmentsTab)
        self.settingsWidget.addTab(self.adjustmentsTab, "Adjustments")  

        # ##################################################################
        # make a zoomer object
        self.zoomTab.setObjectName("zoomTab")
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
    app.setStyle('Fusion')
    palette = qtg.QPalette()
    palette.setColor(qtg.QPalette.Window, qtg.QColor(53, 53, 53)) # background color for windows
    palette.setColor(qtg.QPalette.WindowText, qtc.Qt.white) # text color for windows
    palette.setColor(qtg.QPalette.Base, qtg.QColor(25, 25, 25)) # background of text entry widgets, combo box drop down lists and toolbar handles
    palette.setColor(qtg.QPalette.AlternateBase, qtg.QColor(53, 53, 53)) # alternate base used for stripes
    palette.setColor(qtg.QPalette.ToolTipBase, qtc.Qt.white) # is in inactive group
    palette.setColor(qtg.QPalette.ToolTipText, qtc.Qt.black) # is in inactive group
    palette.setColor(qtg.QPalette.Text, qtc.Qt.white) # text color for widgets wit base background
    #palette.setColor(qtg.QPalette.      #PlaceholderText, qtc.Qt.white) # text color for widgets wit base background

    palette.setColor(qtg.QPalette.Button, qtg.QColor(53, 53, 53)) # button background color
    palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.BrightText, qtc.Qt.red)
    palette.setColor(qtg.QPalette.Link, qtg.QColor(42, 130, 218))
    palette.setColor(qtg.QPalette.Highlight, qtg.QColor(42, 130, 218))
    palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)
    palette.setColor(qtg.QPalette.Disabled, qtg.QPalette.WindowText,  qtg.QColor(128,128,128))
    palette.setColor(qtg.QPalette.Disabled, qtg.QPalette.Window,  qtg.QColor(128,128,128))
    palette.setColor(qtg.QPalette.Disabled, qtg.QPalette.Text,  qtg.QColor(128,128,128))

    
    app.setPalette(palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    app.setStyleSheet("QComboBox:disabled { color: #808080; }")
    # disabled has no meaning within the context of a label?
    # app.setStyleSheet("QLabel: disabled { color: #808080; }")


    window = PiSnap()
    
    sys.exit(app.exec_())

