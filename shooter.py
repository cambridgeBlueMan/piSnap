from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
#from qtw import QMessageBox, QPushButton
from picamera import PiCamera
from psSettings import PSSettings
from thumbnailsmodel import ThumbnailsModel
from gui.shooterGui import Ui_Form
from io import BytesIO
from time import sleep
import picamera
# used to test if file exists
import os.path
import datetime
import subprocess # allows access to command line
import signal
import copy
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

        # defines a validator for the two file root text edit widgets
        rx = qtc.QRegExp("^[-_A-Za-z0-9]{1,25}")
        self.ui.stillFileRoot.setValidator(qtg.QRegExpValidator(rx))
        self.ui.videoFileRoot.setValidator(qtg.QRegExpValidator(rx))
        

        # camera and camvals passed in on initialisation
        self.camvals = camvals
        self.camera = camera

        # model initialisation stuff
        self.model = ThumbnailsModel()
        self.ui.thumbnailAsMv.setModel(self.model)
        
        # set the still file root and the video file root from camvals
        # set isCounter option box from stored camvals 
        self.initStuffFromCamvals()

        # do we want to record zoom?
        self.recordZoom = False

        # resdivider dives actual reslotion to provide preview size
        # QUERY come back to this, does it need some refinement?

        self.resDivider = 2
        
        # next line assumes that video is the chosen default in the designer class
        """ it might be possible to add the widgets to the tabWidget somewhere here. This  way we could 
        have video and still inseperate tabs """
        self.setupVideoCapture()   

        self.setupVLCPlayer()


    def initStuffFromCamvals(self):
        """
        
        """
        self.ui.stillFileRoot.setText(self.camvals["stillFileRoot"])
        self.ui.videoFileRoot.setText(self.camvals["vidFileRoot"])
        if self.camvals["fileNameFormat"] == "counter":
            self.ui.isCounter.setChecked(True)
        else:
            self.ui.isDatestamp.setChecked(True)

        
    def setupVLCPlayer(self):
        """ creat an initial vlc instance, and then create a media player from the instance"""
        
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
                formattedDateTime = self.getFormattedDateTime()

                filename = self.camvals["defaultPhotoPath"]+  "/" + self.imgRoot \
                + formattedDateTime + '.' + self.camvals["stillFormat"]  
            # turn preview back on
            self.showPreview(True)
        if save == True:
            # now make the thumbnail and save the stream to file
            with open (filename, 'wb') as f:
                f.write(imgAsBytes.getbuffer())
            if self.camvals["fileNameFormat"] == "counter":
                self.incFileCounter()
            self.showImage(filename)

    def getFormattedDateTime(self):
        """ returns  a unique and usable filename from a date and time"""
        formattedDateTime = str(datetime.datetime.now()).replace(':','_')
        formattedDateTime = formattedDateTime.replace(' ', '-')
        formattedDateTime = formattedDateTime.replace('.', '_')
        return formattedDateTime

    
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
        myImg = qtg.QImage("tempicon.jpeg")

        # add the icon and the filename to the thumbnail list  
        #
        self.addToMediaView(filename, myImg, self.camvals["imgres"])

        
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
        try:
            self.camera.framerate = int(myvar)
            self.camvals["framerate"] = int(myvar)
        except picamera.exc.PiCameraRuntimeError as err:
            msgBox = qtw.QMessageBox()
            msgBox.move(100,400)
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("You cannot change the framerate while the camera is recording")
            msgBox.setWindowTitle("Camera is recording!")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            returnValue = msgBox.exec()

    
    def updateTerminalWidgetWhileRecording(self, camera, something):
        while camera.recording == True: #camera.recording:
            #try:
            #print("hello!")
            if self.camvals["audioActive"] == "true":
                if self.proc.poll() == None:
                    myStr = "._"
                else:
                    myStr = "There was a problem with the audio!"
            else:
                myStr = "."

            self.window().terminalWidget.moveCursor(qtg.QTextCursor.End)
            self.window().terminalWidget.insertPlainText(myStr)
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
        # BUG 
        # do nothing if recording is in progress
        if self.camera.recording:
            #####################################################################
            #if camera is recording and preview is on then we need to start showing messages for recording
            #################################################################################################
            if self.camvals["doingAssets"] == "yes":
                sleep(0.5)    
                psFunctions.printT(self.window(),"Camera recording!", True)
                _thread.start_new_thread (self.updateTerminalWidgetWhileRecording, (self.camera, None))
                if self.recordZoom == True:
                    # set the zoom to its initial position
                    # code below works, but falls over if no data selected
                    startIx = self.window().zoomTab.ui.zTblView.selectedIndexes()[0]
                    myData = self.window().zoomTab.zTblModel.getZoomData(startIx.row(), True)
                    myData = myData[:]
                    self.camera.zoom = (
                        myData[0],
                        myData[1],
                        myData[2],
                        myData[2]    
                    )
                    self.window().zoomTab.playSelectedRows()

            #################################################################################################
            #psFunctions.printT(self.window(),"Camera currently recording!", True)
            #####################################################################
        else:
            # various settings for video
            self.camera.framerate = self.camvals["framerate"]
            # make file name, less extension
            if self.camvals["fileNameFormat"] == "counter":
                self.vidRoot = self.camvals["vidFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"]) + '.'
            else:
                self.vidRoot = self.camvals["vidFileRoot"] + self.getFormattedDateTime() + '.'
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
                try:
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

                except subprocess.SubprocessError as err:
                    psFunctions.printT(self.window(), "There is a problem with the audio!" )
                    psFunctions.printT(self.window(), str(err))
                        
            if self.recordZoom == True:
                # set the zoom to its initial position
                # code below works, but falls over if no data selected
                startIx = self.window().zoomTab.ui.zTblView.selectedIndexes()[0]
                myData = self.window().zoomTab.zTblModel.getZoomData(startIx.row(), True)
                myData = myData[:]
                self.camera.zoom = (
                    myData[0],
                    myData[1],
                    myData[2],
                    myData[2]    
                )
                # now restablish exposure setting
                ####################################################################
                #sleep(1)
                ####################################################################
            # capture a still, with use_video_port set to True
            # and dimensions according to the video dimension

            # this is for thumbnail purposes
            # capture the image to a BytesIO
            imgAsBytes = BytesIO()
            rs = [138, int(138*self.camvals["vidres"][1]/self.camvals["vidres"][0])]
            self.camera.capture('tempIcon.jpeg', self.camvals["stillFormat"], resize = rs, use_video_port=True)
            # this line used by the list view 
            self.myImg = qtg.QImage("tempIcon.jpeg")
            # start recording
            try:
                self.camera.start_recording(filename, bitrate=int(self.camvals["videoBitRate"]))
                sleep(1)
                #################################################################################################
                if self.camvals["doingAssets"] != "yes":
                    _thread.start_new_thread (self.updateTerminalWidgetWhileRecording, (self.camera, None))
                #################################################################################################

                if self.recordZoom == True:
                    self.window().zoomTab.playSelectedRows()

                #################################################################################################
                if self.camvals["doingAssets"] != "yes":
                    psFunctions.printT(self.window(),"Camera currently recording!")
                #################################################################################################

            except picamera.exc.PiCameraError as err:
                psFunctions.printT(self.window(),"There was a problem with the camera!", True)
                psFunctions.printT(self.window(),str(err))
                # need to stop everything else here eg zoom, sound etc
                if self.recordZoom == True:
                    self.window().zoomTab.abortZoom = True
                if self.camvals["audioActive"]=="true":
                    self.proc.send_signal(signal.SIGINT) ## Send interrupt signal
            except picamera.exc.PiCameraRunTimeError as err:
                # typically caused by changin resolution while recording
                psFunctions.printT(self.window(),"Can't change while recording!", True)
                psFunctions.printT(self.window(),str(err))
                # need to stop everything else here eg zoom, sound etc
                if self.recordZoom == True:
                    self.window().zoomTab.abortZoom = True
                if self.camvals["audioActive"]=="true":
                    self.proc.send_signal(signal.SIGINT) ## Send interrupt signal
        




  
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
            #if self.camvals["fileNameFormat"] == "counter":
            #    self.camvals["fileCounter"] = self.camvals["fileCounter"] + 1
            psFunctions.printT(self.window(),"Camera stopped recording!", True)
            #if self.getAudio == True:
            if self.camvals["audioActive"]=="true":
                # TODO this does not legislate for mux being set to false
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
                # BUG if file already exists then you get interactive response from ffmpeg asking if you want to overwrite. This can happen currently, if you are 
                # using counter method fro file naming and thge app falls over without incrementing the counter
                self.proc = subprocess.run(["ffmpeg", "-loglevel",  "warning",  "-stats",  "-i",  vidInput,  "-i",  audioInput,  "-c:v",  "copy","-c:a",  "aac",  output])
                # report on muxing
                if self.proc.returncode == 0:
                    psFunctions.printT(self.window(),"muxing completed succesfully!", True)
                else:
                    psFunctions.printT(self.window(),"there was a problem muxing audio and video files!", True)
            else:
                output = self.camvals["defaultVideoPath"] + "/"  + self.vidRoot + self.camvals["videoFormat"]  
            # tell the media player what window to use as canvass for the video
            # TODO we need tests to establish when the muxing is complete
            # and possible a progress bar while it takes place
            self.mediaplayer.set_xwindow(int(self.ui.imgContainer.winId()))
            #self.mediaplayer.set_position(0)
            # used by list view widget
            self.addToMediaView(output, self.myImg, self.camvals["vidres"])
            ################################################
            #filename = self.camvals["defaultVideoPath"] + "/" + self.vidRoot + self.camvals["videoFormat"]
            #self.myIcon = qtg.QIcon(filename) 
            #self.myItem = qtw.QListWidgetItem(self.myIcon, filename, self.ui.thumbnails)   
            #############################
            #self.media = self.vlcObj.media_new(output)
            #print("exist?")
            #self.mediaplayer.set_media(self.media)
            #print("exist?")
            #self.mediaplayer.play()
            #print("exist?")
            #self.mediaplayer.set_pause(1)
            # if necessary increment the file counter
            if self.camvals["fileNameFormat"] == "counter":
                self.camvals["fileCounter"] = self.camvals["fileCounter"] + 1
            
     
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

    def thumbnailDoubleClicked(self, ix):
        print("in doSelectedVideo: ", ix)
        print(self.model.getVideoData(ix))
        data = self.model.getVideoData(ix)
        # [thumb, path, res]

        # get rid of the preview
        self.showPreview(False)        
        # get the filename from the list item
        vid = data[1].path()
        # now get the dimensions of the file
        dimensions = data[2]
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
        
        # on the other hand if its a still?


    
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
        # BUG will accept a blank file name 


    def updateVideoRoot(self):
        # BUG will accept a blank file name 
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
            
    def prePreview(self,state):
        """ this is only called from the gui, never from the internals"""
        ############################################################################
        print("Doing assets!")
        self.doRecordVid("fromPreview")
        self.showPreview(state)
        ##############################################################################

    
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
            ###############################################################################
            # if doingAssets is true we need to start recording here, but without 
            # any of the message reporting
            #  
            ###############################################################################
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
    
    def addToMediaList(self, output, icon):
        # add to the old listWidget
        self.myIcon = qtg.QIcon(icon) 
        self.myItem = qtw.QListWidgetItem(self.myIcon, output,
        self.ui.thumbnails) 

    def addToMediaView(self, output, img, res):

        # now add to the new listView model type widget as well
        fp = qtc.QUrl.fromLocalFile(output)
        #tp = qtc.QUrl.fromLocalFile('tempicon.jpeg')

        self.model._data.append([img, fp, res])   
        self.model.layoutChanged.emit()   
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