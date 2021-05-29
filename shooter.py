from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
#from qtw import QMessageBox, QPushButton
from picamera import PiCamera
from psSettings import PSSettings
from shooterGui import Ui_Form
from io import BytesIO
from time import sleep
# used to test if file exists
import os.path
import datetime
import subprocess # allows access to command line
import signal
from os import path
import json
import vlc
import _thread
#import regexp
#from  import *
#from settings import camvals
#print(camvals)

class Shooter(qtw.QWidget):

    def __init__(self, camvals, camera):
        super().__init__()
        # instantiate the QtDesigner generated class
        self.ui = Ui_Form()
        # use its setupUi method to draw the widgets into the main window
        self.ui.setupUi(self)

        # now show the main window with its widgets (only necessary if this class is stand alone)
        #self.show()

        # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals

        # camera passed in on initialisation
        self.camera = camera
        self.initStuffFromCamvals()

        # do we want to record zoom?
        self.recordZoom = False

        # set text to medium bullet
        self.ui.previewButton.setText(u"\u26AB")

        self.resDivider = 2
        
        # next line assumes that video is the chosen default in the designer class
        self.setupVideoCapture()   

        self.setupVLCPlayer()

    def initStuffFromCamvals(self):
        # do we want to capture audio?
        if self.camvals["audioActive"] == "false":
            self.getAudio = False
        else: 
            self.getAudio = True
        self.ui.stillFileRoot.setText(self.camvals["stillFileRoot"])
        self.ui.videoFileRoot.setText(self.camvals["vidFileRoot"])

        
    def setupVLCPlayer(self):
        
        self.timer = qtc.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateVidPosSlider)
        # is_paused indicates whether video is paused or not
        self.is_paused = False
        self.vlcObj = vlc.Instance()
        self.media = None
        self.mediaplayer = self.vlcObj.media_player_new()
        #self.is_paused = False 

    
    def snapAndSave(self):  
        """ takes a still picture and automatically generates a file name """

        # build a file name
        filename = self.camvals["defaultPhotoPath"]+self.camvals["stillFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"]) + '.' + self.camvals["stillFormat"]
        # does the file exist? if not then write it
        if path.exists(filename):
            # if file exists then put the picture to a stream object
            stream = BytesIO()
            self.camera.capture(stream, 'jpeg')
            # now find out what to do with it
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle("FileExists")
            msgBox.setIcon(qtw.QMessageBox.Warning)
            msgBox.setText("This file exists, do you want to overwrite it?")
            msgBox.setStandardButtons(qtw.QMessageBox.Save|qtw.QMessageBox.Cancel)
            appendButton = qtw.QPushButton( "append timestamp")
            msgBox.addButton(appendButton, qtw.QMessageBox.YesRole)
            msgBox.setDefaultButton(appendButton)
            
            ret = msgBox.exec_()
            if ret == qtw.QMessageBox.Save:
                # if save then overwite existing file
                with open (filename, 'wb') as f:
                    #print(stream)
                    f.write(stream.getbuffer())
                    self.showImage(filename)
            if ret == qtw.QMessageBox.Cancel:
                # if cancel then get rid of the buffer
                stream.close()
                pass
            if ret == 0: #appendButton:
                # if save with an appended timestamp then save the buffer/stream with the timestamp
                filename = self.camvals["defaultPhotoPath"]+self.camvals["stillFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"]) \
                + str(datetime.datetime.now()).replace(':','_') + '.'+ self.camvals["stillFormat"]
                with open (filename, 'wb') as f:
                    f.write(stream.getbuffer())
                    self.showImage(filename)
        else:
            # take a picture and increment the counter
            self.camera.capture(filename)
            self.incFileCounter()
            self.showImage(filename)
    
    def showImage(self, filename):
        """ displays a graphic file in the picture window """
        pixmap = qtg.QPixmap(filename)
        pixmapResized = pixmap.scaled(self.camvals["imgres"][0]/2, self.camvals["imgres"][1]/2, qtc.Qt.KeepAspectRatio)
        self.ui.imgContainer.setPixmap(pixmapResized) #.scaled(size,Qt.keepAspectRatio))

        # then add it to the selector widget
        self.myIcon = qtg.QIcon(filename) 
        self.myItem = qtw.QListWidgetItem(self.myIcon, filename, self.ui.thumbnails)        
        
    def incFileCounter(self):
        """ increments the file counter and saves it to the settings file """
        #print(self)
        self.camvals["fileCounter"] = self.camvals["fileCounter"] + 1
        with open("settings.json", "w") as settings:
            json.dump(self.camvals, settings, indent = 4)
            
    def imgToStream(self):
        """ uses camera to take a still picture and returns that in a stream/buffer object """
        stream = BytesIO()
        ##issue
        """
        all of the camera settings should be being made elsewhere and they shuld therefore be in place 
        ready for when a shot is taken

        """
        self.camera.capture(stream, 'jpeg')
        return stream.getbuffer()
    
    def snapAndHold(self):
        """ take a still picture and store in a stream object """
        #print("in snap and hold")
        stream = self.imgToStream()
        # save for this scenario
        with open ("aPic.jpg", 'wb') as f:
            f.write(stream)

    
    #################################################################################################
    #
    #                                      start of video stuff
    #
    #################################################################################################
    def setRecordZoomFlag(self,bool):
        self.recordZoom=bool
        
    def doVideoStabilization(self,bool):
        self.camera.video_stabilization=bool
        self.camvals["video_stabilization"] = str(bool)

    def setFrameRate(self,myvar):
        self.camera.framerate = int(myvar)
        self.camvals["framerate"] = int(myvar)
    
    def updateTerminalWidgetWhileRecording(self, camera, str):
        while camera.recording == True: #camera.recording:
            self.window().terminalWidget.moveCursor(qtg.QTextCursor.End)
            self.window().terminalWidget.insertPlainText(" .")
            sleep(1)


    def doRecordVid(self, test):
        """ record a video stream to a file with automatically generated name """
        # waqtch out for!!!!
        # picamera.exc.PiCameraValueError: output resolution and framerate 
        # # exceeds macroblocks/s limit (245760) for the selected H.264 profile and level
        
        # do nothing if recording is in progress
        if self.camera.recording:
            self.window().terminalWidget.appendPlainText("Camera is already recording!")
        else:
            # start recording video, automatically generate file name
            # this means has to have time stamp
            # various settings for video
            self.camera.framerate = self.camvals["framerate"]
            self.vidRoot = self.camvals["vidFileRoot"] + str(datetime.datetime.now()).replace(':','_') + '.'
            filename = self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["videoFormat"]
            print("file name is: ", filename)
            #self.media = self.vlcObj.media_new(filename)
            #self.mediaplayer.set_media(self.media)

            # record audio if required
            if self.getAudio == True:
                self.proc = subprocess.Popen(["rec", (self.vidRoot + "wav"),]) ## Run program
            # you could capture here a small still
            # do you want too incude a zoom in the reocrding
            #self.recordZoom = True
            if self.recordZoom == True:
                #print(self.window().zoomTab)
                self.window().zoomTab.doRunZoom(self.window().zoomTab)
            try:
                self.camera.start_recording(filename, bitrate=int(self.camvals["videoBitRate"]))
            except PiCamera.exc.PiCameraValueError as err:
                print("hello!!!", err)


            sleep(1)
            self.window().terminalWidget.clear()
            self.window().terminalWidget.setPlainText("Camera currently recording!")

            _thread.start_new_thread (self.updateTerminalWidgetWhileRecording, ((self.camera, str) ))

            '''while True:
                if self.camera.recording==True:
                    sleep(1)
                    self.window().terminalWidget.appendPlainText(".")
                else:
                    break'''
            

    def doStopVid(self, what):
         # if camera is playing then stop playing  
        if self.mediaplayer.is_playing() == 1:
            #print("media playing")
            self.mediaplayer.stop() # vlcObj.vlm_stop_media(self.vlcObj, str_to_bytes(self.media))
            #self.mediaplayer.set_position(0)
        # if camera is recording then stop recording
        if self.camera.recording:
            self.camera.stop_recording() # picamera method
            if self.getAudio == True:
                #print(type(self.proc))
                self.proc.send_signal(signal.SIGINT) ## Send interrupt signal
                vidInput = self.camvals["defaultVideoPath"] + "/" +self.vidRoot + self.camvals["videoFormat"]
                audioInput = self.vidRoot + "wav"
                output = self.camvals["defaultVideoPath"] + "/" +self.vidRoot + "mp4"
                #print(vidInput)
                #print(audioInput)
                #print(output)
                self.proc = subprocess.Popen(["ffmpeg",  "-i",  vidInput,  "-i",  audioInput,  "-c:v",  "copy","-c:a",  "aac",  output])
            else:
                output = self.camvals["defaultVideoPath"] + "/"  + self.vidRoot + self.camvals["videoFormat"]  
            self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))

            #self.mediaplayer.set_position(0)
            self.addToMediaList()
            self.media = self.vlcObj.media_new(output)
            self.mediaplayer.set_media(self.media)
            self.mediaplayer.play()
            self.mediaplayer.set_pause(1)

       
                
    def doPlayVid(self, test): 
        #print (test)
        #print(self.ui.imgContainer)
        self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))
        self.mediaplayer.set_position(0)
        #print(self.mediaplayer.video_take_snapshot(0 , "filename.jpeg", 80, 60))
        self.mediaplayer.play()
        #print(self.mediaplayer.video_take_snapshot(0 , "filename2.jpeg", 80, 60))        
        self.timer.start()
        # play the current video
        
    def doPauseVid(self, test):
        #print ("in pause vid")
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            #self.playbutton.setText("Play")
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.get_position() == 1:
                self.mediaplayer.stop()
            self.mediaplayer.pause()
            self.timer.start()
            self.is_paused = False
            
      
    def setPosition(self, pos):
        # called from vid pos slider
        #print ("in position vid")
        #print(pos)
        self.timer.stop()
        self.mediaplayer.set_position(pos / 1000.0)
        self.timer.start()

    
    def updateVidPosSlider(self):
        """
        Updates the user interface
        """

        # Set the slider's position to its corresponding media position 
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        media_pos = int(self.mediaplayer.get_position() * 1000)
        #print(self.mediaplayer.get_position())
        self.ui.vidPosSlider.setValue(media_pos)
        if self.mediaplayer.get_position() == 1.0:
            #self.mediaplayer.set_position(0)
            #print("hello everybody")
            self.mediaplayer.stop()
            #print(self.mediaplayer.video_take_snapshot(0 , "filename.jpeg", 240, 180 ))

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            #if not self.is_paused:
            #    self.stop()

    def doThumbnailClicked(self,vid):
        # get the dimensions of the media
        vid = vid.text()
        dimensions = self.getVideoDimensions(vid)
        print("dimensions:", dimensions)
        # resize the imgContainer
        self.ui.imgContainer.resize(dimensions[0]/self.resDivider, dimensions[1]/self.resDivider)
        # set the x window
        self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))
        self.mediaplayer.set_position(0)
        # start playing the selected video
        # put the file name to the video player?
        self.media = self.vlcObj.media_new(vid)
        self.mediaplayer.set_media(self.media)
        #print(self.mediaplayer.video_take_snapshot(0 , "filename.jpeg", 80, 60))
        
        self.mediaplayer.play()
        #print(self.mediaplayer.video_take_snapshot(0 , "filename2.jpeg", 80, 60))        
        self.timer.start()

    def getVideoDimensions(self, vid):
        """ 
        This method uses a combination of subprocess and ffprobe to get the dimensions of the 
        passed video.
        
         """
        vid = str(vid)
        print(vid)
        result = subprocess.run(['ffprobe', '-v', 'error', '-hide_banner', '-of', 'default=noprint_wrappers=0', 
        '-print_format', 'json',  '-select_streams', 'v:0', '-show_entries', 'stream=width,height', 
        vid], capture_output=True, text=True)
        # as indicated in the ffprobe command the output is returned as json
        result = json.loads(result.stdout)
        print(result) # uncomment this line to see full json
        sleep(1)
        width =  (result["streams"][0]["width"])
        height = (result["streams"][0]["height"])
        #print(width, height)
        return (width, height)
        
    def setFileRoot(*args):
        pass

    def updateStillRoot(self):
        #self.ui.stillFileRoot.text()
        self.camvals["stillFileRoot"] = self.ui.stillFileRoot.text()

    def updateVideoRoot(self):
        #self.ui.videoFileRoot.text()
        self.camvals["vidFileRoot"] = self.ui.videoFileRoot.text()

    def isDateStamp(*args):
        pass
    def isCounter(*args):
        pass

    def movePreview(self):
        pass
  
    def movePreviewOrigin(self, x,y):
        """ 
        previewPos is a slot which is called whenever the bullet point
        moves. it receives two integers which are x and y values.
         """
        # stops the preview
        self.camera.stop_preview
        #print("in pos", x, y, self.camera.resolution)
        # sets the self.width and self.height for the preview
        # 
        # note that self.width and self.height are here being derivded form the camers's
        # resolution settings and not from camvals
        self.width = int(self.camera.resolution[0]/self.resDivider)
        self.height = int(self.camera.resolution[1]/self.resDivider) 
        self.ui.previewVisible.setChecked(True)
        # I believe that the size of the bulletpoint container is 1/10 of the size of current resolution
        self.camera.start_preview(fullscreen=False, window = (x*10, y*10,self.width,self.height))
        self.window().findChild(qtw.QCheckBox,"statusBarPreviewCheckBox" ).setChecked(True)
        self.window().findChild(qtw.QAction,"visibleAction" ).setChecked(True)
     
    #when checked will enable unlockPreview   
    def setPreviewLockState(self,state):
        if state == True:
            self.ui.previewFrame.setEnabled(True)
            self.ui.previewButton.setEnabled(True)
        else:
            self.ui.previewFrame.setEnabled(False)
            self.ui.previewButton.setEnabled(False)
            x=self.ui.previewVisible.isChecked()
            self.showPreview(x)
            self.ui.previewButton.move(0,0)
            

    def showPreview(self, state, xPos=0, yPos=0):
        #print("hello")

        """ on/off toggle for preview. 'state' is boolean on/off value. Typically passed from one of 
        several tick boxes around the place

        """
        #print("what is the index  of the tab?: ", self.ui.captureTab.currentIndex())
        if self.ui.captureTab.currentIndex() == 1:
            self.width = int(self.camvals["vidres"][0]/self.resDivider)
            self.height = int(self.camvals["vidres"][1]/self.resDivider)
        if self.ui.captureTab.currentIndex() == 0:
            self.width = int(self.camvals["imgres"][0]/self.resDivider)
            self.height = int(self.camvals["imgres"][1]/self.resDivider)
        #print ("w, h: ", self.width, self.height)
        self.geometry().x()
        # resize the frame
        self.ui.imgContainer.resize(self.width, self.height)
        #
        if state == True:
            """ divider is currently hard coded at 2. This should be settable via a preview
            size gui control
            """
            #print("sender: ", self.sender())
            #print("current index: ", self.ui.captureTab.currentIndex() )
            # calculate x and y position for preview
            x = self.ui.imgContainer.geometry().x() + self.geometry().x() + self.window().geometry().x()
            y = self.ui.imgContainer.geometry().y() + self.geometry().y() + self.window().geometry().y() + 27
            # show the preview
            #print ("2ND TIME, w, h: ", self.width, self.height)
            self.camera.stop_preview
            self.camera.start_preview(fullscreen=False, window = (x, y,self.width, self.height))
            #update all the various tick boxes around the place
            if self.sender() == None:
                pass
            else:
                # update stae of all the different preview checkboxes
                if self.ui.previewVisible.isChecked() != True:
                    self.ui.previewVisible.setChecked(True)
                if self.sender().objectName != "statusBarPreviewCheckBox":
                    self.window().findChild(qtw.QCheckBox,"statusBarPreviewCheckBox" ).setChecked(True)
                if self.sender().objectName != "visibleAction":
                    self.window().findChild(qtw.QAction, "visibleAction").setChecked(True)

        else:
            #print(state)
            self.camera.stop_preview()
            if self.sender() == None:
                pass
            else:
                if self.ui.previewVisible.isChecked():
                    self.ui.previewVisible.setChecked(False)
                if self.sender().objectName != "statusBarPreviewCheckBox":
                    self.window().findChild(qtw.QCheckBox,"statusBarPreviewCheckBox" ).setChecked(False)
                if self.sender().objectName != "visibleAction":
                    self.window().findChild(qtw.QAction, "visibleAction").setChecked(False)
           
    def updatePreviewCheckboxesState(self):
        # to be implemented
        pass


    def setPreviewSize(*args):
        pass 
    
    def addToMediaList(self):
        """ 
        Use ffmpegthumbnailer to create a thumbnail image to represent the video
        and display the thumbnail and file name in a ListWidget

        """

        # ffmpeg -i twat.h264 -frames:v 1 -f image2 frame.png

        makeThumbnail = subprocess.Popen(["ffmpeg",  "-i" ,  
        (self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["videoFormat"]),
        "-frames:v", "1",  "-f",  "image2",   (self.camvals["defaultVideoPath"] + "/" 
        + self.vidRoot + self.camvals["stillFormat"])])
        
        # mpeg conversion takes a little time, so we wait for it before loading into the list widget item
        # I think in an  ideal world this should be a BytesIO object rather than a file.
        # much easier to clean all that up at end of session

        sleep(2)
        self.thumb = (self.camvals["defaultVideoPath"] + "/"  + self.vidRoot + self.camvals["stillFormat"]) 
        self.myIcon = qtg.QIcon(self.thumb) 
        self.myItem = qtw.QListWidgetItem(self.myIcon, self.vidRoot + self.camvals["videoFormat"], self.ui.thumbnails)        
        # then add it to the widget


    def setCaptureMode(self, ix):
        """
        slot called from the still/video tab selector currentChanged signal
        """
        #print("index is: ", self, ix)
        # if video is selected then instantiate the vlc stuff
        if ix == 1:
            self.setupVideoCapture()
            
        else:
            # clean it all up, still to write
            self.setupStillCapture()
        state = self.ui.previewVisible.isChecked()   # previewVisible.isChecked()
        #print("current state is: ", state)
        self.showPreview(state)


    def setupVideoCapture(self):
        """ make all relevant settings appropriate for video capture """   
        self.ui.frameRate.setCurrentText(str(self.camvals["framerate"]))
        self.camera.framerate=(self.camvals["framerate"])
        # set camera.resolution for video
        self.resetResolutionStuff("vidres")

    def setupStillCapture(self):
        """ make all relevant settings for still capture """
        self.resetResolutionStuff("imgres")

    def resetResolutionStuff(self, imgType):
        self.camera.resolution = tuple(self.camvals[imgType])
        print("in reset resolutionsStuff", self.camvals[imgType])
        self.ui.imgContainer.resize(self.camvals[imgType][0]/self.resDivider, self.camvals[imgType][1]/self.resDivider)
        
        # get the size of the monitor
        sizeObject = qtw.QDesktopWidget().screenGeometry(-1)
        self.ui.previewFrame.resize(((sizeObject.width()/10) + 22), ((sizeObject.height()/10) + 22))
        self.ui.previewButton.setContainerSize((sizeObject.width()/10) + 22,  (sizeObject.height()/10) + 22) 
        self.ui.previewButton.setDragButtonSize(self.camera.resolution[0]/20 +22, self.camera.resolution[1]/20 + 22)
        #print("button size: ", (self.camera.resolution[0]/20)) # + 22)
        self.ui.previewButton.moveButtonToOrigin()
        

if __name__ == "__main__":
    import sys
   
    # instiantiate an app object from the QApplication class 
    app = qtw.QApplication(sys.argv)
    # instantiate an object containing the logic code
    mw = Shooter(None)
    sys.exit(app.exec_())