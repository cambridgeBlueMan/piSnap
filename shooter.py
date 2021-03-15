from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
#from qtw import QMessageBox, QPushButton
from psPiCamera import PSPiCamera
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
#import regexp
#from  import *
#from settings import camvals
#print(camvals)

class PSSnapper(qtw.QWidget):

    def __init__(self, camvals, camera):
        super().__init__()

        # instantiate a camera from the extended camera class
        #self.camera = MyCamera(self)

        # instantiate the QtDesigner class
        self.ui = Ui_Form()
        # use its setupUi method to draw the widgets into the main window
        self.ui.setupUi(self)
        # now show the main window with its widgets
        #self.show()

       # camvals = None means we are running the code as stand alone
        # so we need to load the settings file
        if camvals == None:
            with open("settings.json", "r") as settings:
                self.camvals = json.load(settings)
        else:
            self.camvals = camvals

        self.camera = camera
        # do we want to capture audio?
        self.getAudio = False
        # apply settings derived from settings file
        self.setupVideoCapture()   

        self.doTimerStuff()

    def doTimerStuff(self):
        self.timer = qtc.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateUi)
        # is_paused indicates whether video is paused or not
        self.is_paused = False
        self.vlcObj = vlc.Instance()
        self.media = None
        self.mediaplayer = self.vlcObj.media_player_new()
        self.is_paused = False 

    
    def snapAndSave(self):  
        """ takes a still picture and automatically generates a file name """

        # get a file name
        filename = self.camvals["stillFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"]) + '.' + self.camvals["stillFormat"]

        # set the settings for the camera
        ##issue##
        """
        all of the camera settings should be being made elsewhere and they shuld therefore be in place 
        ready for when a shot is taken

        """
        self.camera.resolution = tuple(self.camvals["imgres"])

        # does the file exist? if not then write it
        if path.exists(filename):
            # if file exists then put the picture to a stream object
            stream = BytesIO()
            self.camera.capture(stream, 'jpeg')
            # now find out what to do with it
            msgBox = QMessageBox()
            msgBox.setWindowTitle("FileExists")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("This file exists, do you want to overwrite it?")
            msgBox.setStandardButtons(QMessageBox.Save|QMessageBox.Cancel)
            appendButton = QPushButton( "append timestamp")
            msgBox.addButton(appendButton, QMessageBox.YesRole)
            msgBox.setDefaultButton(appendButton)
            
            ret = msgBox.exec_()
            if ret == QMessageBox.Save:
                # if save then overwite existing file
                with open (filename, 'wb') as f:
                    #print(stream)
                    f.write(stream.getbuffer())
                    self.showImage(filename)
            if ret == QMessageBox.Cancel:
                # if cancel then get rid of the buffer
                stream.close()
                pass
            if ret == 0: #appendButton:
                # if save with an appended timestamp then save the buffer/stream with the timestamp
                filename = self.camvals["stillFileRoot"] + '{:04d}'.format(self.camvals["fileCounter"]) \
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

    def doRecordVid(self, test):
        """ record a video stream to a file with automatically generated name """
        # do nothing if recording is in progress
        if self.camera.recording:
            print("Camera is already recording!")
        else:
            # start recording video, automatically generate file name
            # this means has to have time stamp
            # various settings for video
            self.camera.framerate = self.camvals["framerate"]
            self.vidRoot = self.camvals["vidFileRoot"] + str(datetime.datetime.now()).replace(':','_') + '.'
            filename = self.vidRoot + self.camvals["videoFormat"]
            #self.media = self.vlcObj.media_new(filename)
            #self.mediaplayer.set_media(self.media)

            # record audio if required
            if self.getAudio == True:
                self.proc = subprocess.Popen(["rec", (self.vidRoot + "wav"),]) ## Run program
            # you could capture here a small still
            self.camera.start_recording(filename)


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
                print(type(self.proc))
                self.proc.send_signal(signal.SIGINT) ## Send interrupt signal
                vidInput = self.vidRoot + self.camvals["videoFormat"]
                audioInput = self.vidRoot + "wav"
                output = self.vidRoot + "mp4"
                print(vidInput)
                print(audioInput)
                print(output)
                self.proc = subprocess.Popen(["ffmpeg",  "-i",  vidInput,  "-i",  audioInput,  "-c:v",  "copy","-c:a",  "aac",  output])
            else:
                output = self.vidRoot + "h264"    
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
        print ("in position vid")
        print(pos)
        self.timer.stop()
        self.mediaplayer.set_position(pos / 1000.0)
        self.timer.start()

    def setCaptureMode(self, ix):
        """
        slot called from the still/video tab selector currentChanged signal
        """
        #print(self, ix)
        # if video is selected then instantiate the vlc stuff
        if ix == 1:
            self.setupVideoCapture()
            
        else:
            # clean it all up, still to write
            self.setupStillCapture()

    def updateUi(self):
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
            print(self.mediaplayer.video_take_snapshot(0 , "filename.jpeg", 240, 180 ))

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            #if not self.is_paused:
            #    self.stop()

    def doThumbnailClicked(self,widg):
        # start playing the selected video
        # put the file name to the video player?
        self.media = self.vlcObj.media_new(widg.text())
        self.mediaplayer.set_media(self.media)
        self.mediaplayer.play()
        #print(self.mediaplayer.video_take_snapshot(0 , "filename2.jpeg", 80, 60))        
        self.timer.start()
        # play the current video

        #print(args[1].text())
        
    def setFileRoot(*args):
        pass
    def isDateStamp(*args):
        pass
    def isCounter(*args):
        pass
    def showPreview(self, state):
        if state == True:
            x = int(self.camera.resolution[0]/2)
            y = int(self.camera.resolution[1]/2) 
            self.camera.start_preview(fullscreen=False, window = (0, 0,x,y))
        else:
            self.camera.stop_preview()
    def setPreviewSize(*args):
        pass 
    
    def addToMediaList(self):
        """ 
        Use ffmpegthumbnailer to create a thumbnail image to represent the video
        and display the thumbnail and file name in a ListWidget

        """

        # ffmpeg -i twat.h264 -frames:v 1 -f image2 frame.png

        makeThumbnail = subprocess.Popen(["ffmpeg",  "-i" ,  (self.vidRoot + self.camvals["videoFormat"]),
        "-frames:v", "1",  "-f",  "image2",   (self.vidRoot + self.camvals["stillFormat"])])
        
        # mpeg conversion takes a little time, so we wait for it before loading into the list widget item
        # I think in an  ideal world this should be a BytesIO object rather than a file.
        # much easier to clean all that up at end of session

        sleep(2)
        self.thumb = (self.vidRoot + self.camvals["stillFormat"]) 
        self.myIcon = qtg.QIcon(self.thumb) 
        self.myItem = qtw.QListWidgetItem(self.myIcon, self.vidRoot, self.ui.thumbnails)        
        # then add it to the widget

    def setupVideoCapture(self):
        #print ("++++++++++++++++++++++++++++++++++++++++++" ,  dir(self))
        """ make all relevant settings appropriate for video capture """
        # make vlc media player
        self.vlcObj = vlc.Instance()
        self.media = None
        self.mediaplayer = self.vlcObj.media_player_new()
        self.is_paused = False
        # set resolution for video
        self.resolution = tuple(self.camvals["vidres"])
        # adjust display area for video
        ##issue##
        self.ui.imgContainer.resize(800,600)

    def setupStillCapture(self):
        #print(self)
        """ make all relevant settings for still capture """
        # set resolution for still
        self.resolution = tuple(self.camvals["imgres"])
        # adjust display area for video
        ##issue##
        self.ui.imgContainer.resize(self.resolution[0]/2, self.resolution[1]/2)



        

if __name__ == "__main__":
    import sys
   
    # instiantiate an app object from the QApplication class 
    app = qtw.QApplication(sys.argv)
    # instantiate an object containing the logic code
    mw = PSSnapper(None)
    sys.exit(app.exec_())