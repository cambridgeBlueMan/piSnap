from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 

from picamera import PiCamera
import vlc


class PSPiCamera(PiCamera):
    def __init__(self, win):
        super().__init__()
        self.setupCamera(win)
        #filename = "/home/pi/Pictures/file1.jpg" 
    def setupCamera(self, win):
        # retrieve various stuff from a ini file
        #self.filename = filename
        #with open("settings.json", "r") as settings:
        #    self.camvals = json.load(settings)
        win.vidres = (1920,1080) #self.camvals["vidres"]
        win.imgres = (1600,1200) #self.camvals["imgres"]
        #win.resolution = tuple(win.imgres)
        #print(self.resolution)
        #pass   

        #####################################################################
        # INSTANTIATE A QT TIMER TO UPDATE A POSITION SLIDER AS A V
        # timer is used to update position slider as a video plays
        
        """  win.timer = qtc.QTimer(win)
        win.timer.setInterval(100)
        win.timer.timeout.connect(win.updateUi)
        # is_paused indicates whether video is paused or not
        win.is_paused = False
        win.vlcObj = vlc.Instance()
        win.media = None
        win.mediaplayer = win.vlcObj.media_player_new()
        win.is_paused = False  """