from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
#from qtw import QMessageBox, QPushButton
from picamera import PiCamera
from psSettings import PSSettings
from gui.shooterGui import Ui_Form
from io import BytesIO
from time import sleep
import picamera
# used to test if file exists
import os.path
import datetime
import subprocess # allows access to command line
import signal
from os import path
from PIL import Image
from PIL import ImageQt

import json
import math
import vlc
import _thread
import psFunctions
class Shooter(qtw.QWidget):

    def __init__(self, camvals, camera):
        super().__init__()
        # instantiate the QtDesigner generated class
        self.ui = Ui_Form()
        # use its setupUi method to draw the widgets into the main window
        self.ui.setupUi(self)
        #reference qline edit widget
        rx = qtc.QRegExp("^[-_A-Za-z0-9]{1,25}")
        self.ui.stillFileRoot.setValidator(qtg.QRegExpValidator(rx))
        self.ui.videoFileRoot.setValidator(qtg.QRegExpValidator(rx))
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

        self.resDivider = 2
        
        # next line assumes that video is the chosen default in the designer class
        self.setupVideoCapture()   

        self.setupVLCPlayer()

    def initStuffFromCamvals(self):
        # do we want to capture audio?
        """
        if self.camvals["audioActive"] == "false":
            self.getAudio = False
        else: 
            self.getAudio = True
        """
        self.ui.stillFileRoot.setText(self.camvals["stillFileRoot"])
        self.ui.videoFileRoot.setText(self.camvals["vidFileRoot"])
        if self.camvals["fileNameFormat"] == "counter":
            self.ui.isCounter.setChecked(True)
        else:
            self.ui.isDatestamp.setChecked(True)

        
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
        # QUERY consider using uuid to generate unique file names

        # import uuid

        # print(str(uuid.uuid4()))
        """ takes a still picture and automatically generates a file name """
        self.camera.zoom = self.window().zoomTab.zoom[:]
        # build a file name

        # make file name, less extension
        if self.camvals["fileNameFormat"] == "counter":
            self.imgRoot = self.camvals["stillFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"])
        else:
            formattedDateTime = str(datetime.datetime.now()).replace(':','_')
            formattedDateTime = formattedDateTime.replace(' ', '-')
            formattedDateTime = formattedDateTime.replace('.', '_')
            self.imgRoot = self.camvals["stillFileRoot"] + formattedDateTime
        # now add the extension
        filename = self.camvals["defaultPhotoPath"]+ "/" + self.imgRoot + '.' + self.camvals["stillFormat"]

        # capture the image to a BytesIO
        imgAsBytes = BytesIO()
        self.camera.capture(imgAsBytes, self.camvals["stillFormat"])
        save = True

        # does the file exist?
        if path.exists(filename):            
            # now find out what to do with it

            # turn off preview so we can see dialog
            if self.ui.previewVisible.isChecked():
                self.camera.stop_preview()   
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle("FileExists")
            msgBox.setIcon(qtw.QMessageBox.Warning)
            msgBox.setText("This file exists, do you want to overwrite it?")
            msgBox.setStandardButtons(qtw.QMessageBox.Save|qtw.QMessageBox.Cancel)
            appendButton = qtw.QPushButton( "append timestamp")
            msgBox.addButton(appendButton, qtw.QMessageBox.YesRole)
            msgBox.setDefaultButton(appendButton)

            # save file unless told otherwise in logic
            ret = msgBox.exec_()
            if ret == qtw.QMessageBox.Save:
                # then pass leaving sdave true
                pass
            if ret == qtw.QMessageBox.Cancel:
                # if cancel then get rid of the buffer
                save = False
                imgAsBytes.close()
            if ret == 0: #appendButton:
                # if save with an appended timestamp then save the buffer/stream with the timestamp
                formattedDateTime = str(datetime.datetime.now()).replace(':','_')
                formattedDateTime = formattedDateTime.replace(' ', '-')
                formattedDateTime = formattedDateTime.replace('.', '_')

                filename = self.camvals["defaultPhotoPath"]+  "/" + self.imgRoot \
                + formattedDateTime + '.'+ self.camvals["stillFormat"]  
            # turn preview back on
            self.showPreview(True)
        if save == True:
            # now make the thumbnail and save the stream to file
            with open (filename, 'wb') as f:
                f.write(imgAsBytes.getbuffer())
            if self.camvals["fileNameFormat"] == "counter":
                self.incFileCounter()
            self.showImage(filename)
    
    def showImage(self, filename):
        """ displays a graphic file in the picture window """
        
        # open the file as a PIL image
        image = Image.open(filename)  

        # set max size 
        MAX_SIZE = (138,138)
        
        # thumbnail function modifies the image object in place
        image.thumbnail(MAX_SIZE)
        
        # saving it for diagnostics
        #image.save("thumb.jpeg", "JPEG")

        # myImg is a ImageQt object which is subclassed from Qimage
        myImg = ImageQt.ImageQt(image)

        # convert to pixmap
        myPixMap = qtg.QPixmap.fromImage(myImg)

        # save the pixmap for diagnostics
        myPixMap.save("tempicon.jpeg")

        myIcon = qtg.QIcon("tempicon.jpeg") #qtg.QImage(thumb) 

        # add the icon and the filename to the thumbnail list
        myItem = qtw.QListWidgetItem(myIcon, filename, self.ui.thumbnails)        
        
    def incFileCounter(self):
        """ increments the file counter and saves it to the settings file """
        self.camvals["fileCounter"] = self.camvals["fileCounter"] + 1
        with open("settings.json", "w") as settings:
            json.dump(self.camvals, settings, indent = 4)
            
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
            try:
                self.window().terminalWidget.moveCursor(qtg.QTextCursor.End)
                self.window().terminalWidget.insertPlainText(" .")
                """ if subproc.poll() == 2:
                    raise subprocess.SubprocessError(2,self.cmd) """
            except subprocess.SubprocessError: # as err:
                    psFunctions.printT(self.window(), "Audio failed!!" )
                    #psFunctions.printT(self.window(), str(err) , True)
            sleep(1)

    def checkAudio(self,subproc):
        while True:
            if subproc.poll()==2:
                raise subproc.SubprocessError(2,self.cmd)
            sleep (1)

        #psFunctions.printT("Camera stopped recording!", True)

# TODO Sort out video recording
    def doRecordVid(self, test):
        """ record a video stream to a file with automatically generated name """ 
        # do nothing if recording is in progress
        if self.camera.recording:
            psFunctions.printT(self.window(),"Camera currently recording!", True)
        else:
            # various settings for video
            self.camera.framerate = self.camvals["framerate"]
            # make file name, less extension
            if self.camvals["fileNameFormat"] == "counter":
                self.vidRoot = self.camvals["vidFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"]) + '.'
            else:
                self.vidRoot = self.camvals["vidFileRoot"] + str(datetime.datetime.now()).replace(':','_') + '.'
            # make vid file name
            # TODO must ensure that default video path does exist and if not 
            # deal with accordingly
            filename = self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["videoFormat"]
            #if self.getAudio == True:
            if self.camvals["audioActive"]=="true":
                # TODO add try statement to ensure safe return from subprocess
                # first build the command to run

                # arecord --device="hw:USB,0" -t wav -c 2 -f S32_LE -r 48000  helloEverybody2.wav
                """
                self.cmd = ["arecord", "-D", "hw:USB,0" "-r", self.camvals["audioSampleRate"], "-f", "S32_LE", "-c", "2", \
                    (self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["audioFileFormat"]),]
                """ 
                self.cmd = ["rec",  "-r", self.camvals["audioSampleRate"], "-b", self.camvals["audioBitRate"], \
                        (self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["audioFileFormat"]),]
                #try:
                    # try to start recording the audio
                self.proc = subprocess.Popen(self.cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True) ## Run program
                # communicate holds two element tuple of form (stdout, stderr)
                """   procRet = self.proc.communicate()
                #therefore, if we have some stderr raise an error
                if procRet[1] > "":
                    psFunctions.printT(self.window(), procRet[1])
                    psFunctions.printT(self.window(), str(self.proc.poll())) """
                #sleep(1)
                """ if self.proc.poll() == 2:
                    raise subprocess.SubprocessError(2,self.cmd) """
                #_thread.start_new_thread (self.checkAudio(), (self.proc))

                #except subprocess.SubprocessError: # as err:
                #    psFunctions.printT(self.window(), "Audio failed!!" )
                    #psFunctions.printT(self.window(), str(err) , True)
                    #self.camvals["audioActive"]="false"
            # you could capture here a small still
            # do you want too incude a zoom in the reocrding
            #self.recordZoom = True

            #try:
            # TODO take a still and make a thumbnail
            self.camera.start_recording(filename, bitrate=int(self.camvals["videoBitRate"]))
            sleep(1)
            _thread.start_new_thread (self.updateTerminalWidgetWhileRecording, (self.camera, str))
            if self.recordZoom == True:
            #print(self.window().zoomTab)
                fh = open("diags.txt", "a")
                fh.write(filename + "," + str(self.camvals["vidres"]) + "," 
                #+ str(self.window().zoomTab.startZoom[:]) + "," 
                #+ str(self.window().zoomTab.endZoom[:]) + ','
                + str(abs(self.window().zoomTab.endZoom[0] - self.window().zoomTab.startZoom[0])) + ','
                + str(abs(self.window().zoomTab.endZoom[1] - self.window().zoomTab.startZoom[1])) + ','
                + str(abs(self.window().zoomTab.endZoom[2] - self.window().zoomTab.startZoom[2])) + ','
                + str(self.camvals["zoomSpeed"])
                + "\n")
                fh.close()
                self.window().zoomTab.playSelectedRows()
            psFunctions.printT(self.window(),"Camera currently recording!")
                #self.window().terminalWidget.setPlainText("Camera currently recording!")

            #except picamera.PiCameraError as err:
            #    #print("hello!!!", err)
            #    self.window().terminalWidget.clear()
            #    txt = "Recording could not be started: " + str(err)
            #    self.window().terminalWidget.setPlainText(txt)   

    def endRecWithZoom(self,bool):
        self.window().zoomTab.endRecWithZoom = bool

    def doStopVid(self):
         # if camera is playing then stop playing  
        if self.mediaplayer.is_playing() == 1:
            self.mediaplayer.stop() # vlcObj.vlm_stop_media(self.vlcObj, str_to_bytes(self.media))
            #self.mediaplayer.set_position(0)
        # if camera is recording then stop recording
        if self.camera.recording:
            self.camera.stop_recording() # picamera method
            # if necessary increment the fileCounter
            if self.camvals["fileNameFormat"] == "counter":
                self.camvals["fileCounter"] == self.camvals["fileCounter"] + 1
            psFunctions.printT(self.window(),"Camera stopped recording!", True)
            #if self.getAudio == True:
            if self.camvals["audioActive"]=="true":
                # TODO the current frames/sec needs to be passed to the ffmpeg convesion below
                # frame rate is -r
                # TODO note that the val of audioActive could possible currently change while the video is recording
                # a fair amount of stuff needs cornering out here, I suspect
                self.proc.send_signal(signal.SIGINT) ## Send interrupt signal
                procRet  = self.proc.communicate()
                psFunctions.printT(self.window(), str(procRet[0]))
                #if procRet[0] == b'':
                psFunctions.printT(self.window(),"audio recording terminated succesfully!", True)
                #else:
                #    psFunctions.printT(self.window(),"There was a problem with the audio recording", True)
                vidInput = self.camvals["defaultVideoPath"] + "/" +self.vidRoot + self.camvals["videoFormat"]
                audioInput = self.camvals["defaultVideoPath"] + "/" +self.vidRoot + self.camvals["audioFileFormat"]
                output = self.camvals["defaultVideoPath"] + "/" +self.vidRoot + "mp4"
                self.proc = subprocess.Popen(["ffmpeg", "-loglevel",  "warning",  "-stats",  "-i",  vidInput,  "-i",  audioInput,  "-c:v",  "copy","-c:a",  "aac",  output])
            else:
                output = self.camvals["defaultVideoPath"] + "/"  + self.vidRoot + self.camvals["videoFormat"]  
            self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))

            #self.mediaplayer.set_position(0)
            self.addToMediaList(output)
            ################################################
            #filename = self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["videoFormat"]
            #self.myIcon = qtg.QIcon(filename) 
            #self.myItem = qtw.QListWidgetItem(self.myIcon, filename, self.ui.thumbnails)   
            #############################
            self.media = self.vlcObj.media_new(output)
            self.mediaplayer.set_media(self.media)
            self.mediaplayer.play()
            self.mediaplayer.set_pause(1)
     
    def doPlayVid(self, test): 
        self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))
        self.mediaplayer.set_position(0)
        self.mediaplayer.play()      
        self.timer.start()
        # play the current video
    
    def doClearImgContainer(self):
        self.ui.imgContainer.clear()
        
    def doPauseVid(self, test):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
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
        self.ui.vidPosSlider.setValue(media_pos)
        if self.mediaplayer.get_position() == 1.0:
            #self.mediaplayer.set_position(0)
            self.mediaplayer.stop()
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
        # TODO when thumbnail is clicked it should turn the preview off, if necessary
        # get rid of the preview
        self.showPreview(False)
        # get the filename from the list item
        vid = vid.text()
        # now get the dimensions of the file
        dimensions = self.getVideoDimensions(vid)
        # resize the imgContainer
        self.ui.imgContainer.resize(dimensions[0]/self.resDivider, dimensions[1]/self.resDivider)
        
        # set the x window
        ## if its a video
        #psFunctions.printT(self.window(), vid[-4:])
        if vid[-3:] == "peg":
            psFunctions.printT(self.window(), vid[-4:])
            pixmap = qtg.QPixmap(vid)
            pixmapResized = pixmap.scaled(self.camvals["imgres"][0]/2, self.camvals["imgres"][1]/2, qtc.Qt.KeepAspectRatio)
            self.ui.imgContainer.setPixmap(pixmapResized) #.scaled(size,Qt.keepAspectRatio))
        else:
            self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))
            self.mediaplayer.set_position(0)
            # start playing the selected video
            # put the file name to the video player?
            self.media = self.vlcObj.media_new(vid)
            self.mediaplayer.set_media(self.media)
            self.mediaplayer.play()    
            self.timer.start()

        # on the other hand if its a still



    def getVideoDimensions(self, vid):
        """ 
        This method uses a combination of subprocess and ffprobe to get the dimensions of the 
        passed video.
        
         """
        vid = str(vid)
        result = subprocess.run(['ffprobe', '-v', 'error', '-hide_banner', '-of', 'default=noprint_wrappers=0', 
        '-print_format', 'json',  '-select_streams', 'v:0', '-show_entries', 'stream=width,height', 
        vid], capture_output=True, text=True)
        # as indicated in the ffprobe command the output is returned as json
        result = json.loads(result.stdout)
        sleep(1)
        width =  (result["streams"][0]["width"])
        height = (result["streams"][0]["height"])
        return (width, height)
        
    def setFileRoot(*args):
        pass

    def updateStillRoot(self):
        self.camvals["stillFileRoot"] = self.ui.stillFileRoot.text()

    def updateVideoRoot(self):
        #self.ui.videoFileRoot.text()
        self.camvals["vidFileRoot"] = self.ui.videoFileRoot.text()

    def setFileNameFormat(*args):
        print(args[0].sender().objectName())
        if args[0].sender().objectName() == "isCounter":
            args[0].camvals["fileNameFormat"] = "counter"
        else:
            args[0].camvals["fileNameFormat"] = "time"

    def movePreview(self):
        pass
  #TODO Bullet point button should scale to match currently selected resolution
  #TODO single click on bullet should position preview top left
  # TODO ideally if app loses focus and preview is on then preview should disappear, 
  # reappearing when focus returns to the app
    def movePreviewOrigin(self, x,y):
        """ 
        previewPos is a slot which is called whenever the bullet point
        moves. it receives two integers which are x and y values.
         """
        # stops the preview
        self.camera.stop_preview
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
            

    def showPreview(self, state):

        """ on/off toggle for preview. 'state' is boolean on/off value. Typically passed from one of 
        several tick boxes around the place

        """
        if self.ui.captureTab.currentIndex() == 1:
            self.width = int(self.camvals["vidres"][0]/self.resDivider)
            self.height = int(self.camvals["vidres"][1]/self.resDivider)
        if self.ui.captureTab.currentIndex() == 0:
            self.width = int(self.camvals["imgres"][0]/self.resDivider)
            self.height = int(self.camvals["imgres"][1]/self.resDivider)
        self.geometry().x()
        # resize the frame
        self.ui.imgContainer.resize(self.width, self.height)
        #
        if state == True:
            """ TODO divider is currently hard coded at 2. This should be settable via a preview
            size gui control
            """
            # calculate x and y position for preview
            x = self.ui.imgContainer.geometry().x() + self.geometry().x() + self.window().geometry().x()
            y = self.ui.imgContainer.geometry().y() + self.geometry().y() + self.window().geometry().y() + 27
            # show the preview
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

    def doShowOverlay(self, bool):
        if bool == True:
            #self.addOverlay = 
            self.camera.show_overlay()
    def setPreviewSize(*args):
        pass 
    
    def addToMediaList(self, output):
        """ 
        Use ffmpegthumbnailer to create a thumbnail image to represent the video
        and display the thumbnail and file name in a ListWidget

        """

        # ffmpeg -i avid.h264 -frames:v 1 -f image2 frame.png
        # output is the full file name and path  
        # the subprocess is working and assembling the file ames from constituents
        makeThumbnail = subprocess.Popen(["ffmpeg",  "-loglevel",  "warning",  "-i" ,  
        (self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["videoFormat"]),
        "-frames:v", "1",  "-f",  "image2",   (self.camvals["defaultVideoPath"] + "/" 
        + self.vidRoot + self.camvals["stillFormat"])])
        
        # mpeg conversion takes a little time, so we wait for it before loading into the list widget item
        # I think in an  ideal world this should be a BytesIO object rather than a file.
        # much easier to clean all that up at end of session

        sleep(2)
        self.thumb = (self.camvals["defaultVideoPath"] + "/"  + self.vidRoot + self.camvals["stillFormat"]) 
        self.myIcon = qtg.QIcon(self.thumb) 
        self.myItem = qtw.QListWidgetItem(self.myIcon, output,
        self.ui.thumbnails)        
        # then add it to the widget


    def setCaptureMode(self, ix):
        """
        slot called from the still/video tab selector currentChanged signal
        """
        # if video is selected then instantiate the vlc stuff
        if ix == 1:
            self.setupVideoCapture()
            
        else:
            # clean it all up, still to write
            self.setupStillCapture()
        state = self.ui.previewVisible.isChecked()   # previewVisible.isChecked()
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
        self.ui.imgContainer.resize(self.camvals[imgType][0]/self.resDivider, self.camvals[imgType][1]/self.resDivider)
        
        # get the size of the monitor
        sizeObject = qtw.QDesktopWidget().screenGeometry(-1)
        """ self.ui.previewFrame.resize(((sizeObject.width()/10) + 22), ((sizeObject.height()/10) + 22))
        self.ui.previewButton.setContainerSize((sizeObject.width()/10) + 22,  (sizeObject.height()/10) + 22) 
        self.ui.previewButton.setDragButtonSize(self.camera.resolution[0]/20 +22, self.camera.resolution[1]/20 + 22)
        self.ui.previewButton.moveButtonToOrigin() """
        

if __name__ == "__main__":
    import sys
   
    # instiantiate an app object from the QApplication class 
    app = qtw.QApplication(sys.argv)
    # instantiate an object containing the logic code
    mw = Shooter(None)
    sys.exit(app.exec_())