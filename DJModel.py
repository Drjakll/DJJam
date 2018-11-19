import sys, os, wave, pyaudio, time, audioop, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class DJModel(QWidget):
    def __init__(self):
        super().__init__()
        self.startX = 350
        self.startY = 350
        self.winX = 800
        self.winY = 600
        self.mouseX = 0
        self.mouseY = 0
        self.tracktime = time.time()
        self.dx = 1
        self.dy = 0
        self.arc = 0
        self.trackList = []
        self.clipList = []
        self.video1 = DJMovie()
        self.video2 = DJMovie()
        self.playRateReset1 = QPushButton('Reset')
        self.playRateReset2 = QPushButton('Reset')
        self.rightScratchMode = QLabel("Scratch: Off")
        self.leftScratchMode = QLabel("Scratch: Off")
        self.playRateSlider1 = QSlider(Qt.Vertical)
        self.playRateSlider2 = QSlider(Qt.Vertical)
        self.crossFadeControl = QSlider(Qt.Vertical)
        self.track1Volume = QSlider(Qt.Vertical)
        self.track2Volume = QSlider(Qt.Vertical)
        self.trackControl = QHBoxLayout()
        self.track1Widget = QGroupBox("Left Audio")
        self.track2Widget = QGroupBox("Right Audio")
        self.track1 = TrackPlayer()
        self.track2 = TrackPlayer()
        self.windowLayout = QVBoxLayout()
        self.tracklist = QHBoxLayout()
        self.listWidget = QGroupBox()
        self.controlWidget = QGroupBox()
        self.leftScratch = False
        self.rightScratch = False

    #This is where I save all the setting into a json file  
    def saveSetting(self):
        self.jsonObj['track1']['fileName'] = self.track1.getTitle()
        self.jsonObj['track2']['fileName'] = self.track2.getTitle()
        self.jsonObj['track1']['duration'] = self.track1.getDuration()
        self.jsonObj['track2']['duration'] = self.track2.getDuration()
        self.jsonObj['track1']['position'] = self.track1.getPosition()
        self.jsonObj['track2']['position'] = self.track2.getPosition()
        self.jsonObj['track1']['volume'] = self.track1.getVolume()
        self.jsonObj['track2']['volume'] = self.track2.getVolume()
        self.jsonObj['track1']['crossfade'] = self.track1.getCrossFade()
        self.jsonObj['track2']['crossfade'] = self.track2.getCrossFade()
        self.jsonObj['clip1']['fileName'] = self.video1.getTitle()
        self.jsonObj['clip2']['fileName'] = self.video2.getTitle()
        self.jsonObj['clip1']['duration'] = self.video1.getDuration()
        self.jsonObj['clip2']['duration'] = self.video2.getDuration()
        self.jsonObj['clip1']['position'] = self.video1.getPosition()
        self.jsonObj['clip2']['position'] = self.video2.getPosition()
        return self.jsonObj

    #This is to retrieve the setting from the file if it's available, otherwise, it'll set all the settings to empty
    def getJsonObj(self):
        try:
            with open('setting.txt', 'r') as file:
                self.jsonObj = json.load(file)
        except:
            print("Cannot find previous saved setting")
            self.jsonObj = {'track1': {'fileName': '', 'duration': 0, 'position': 0, 'volume': 100, 'crossfade': .5}, 'track2': {'fileName': '', 'duration': 0, 'position': 0, 'volume': 100, 'crossfade' : .5}, 'clip1': {'fileName': '', 'duration': 0, 'position':0, 'volume': 0}, 'clip2': {'fileName': '', 'duration': 0, 'position':0, 'volume': 0}}                 

    #After the setting was retrieved from the file, the program will call this function to set up the settings
    def setupSetting(self):
        self.getJsonObj()
        self.track1.setUp(self.jsonObj['track1']['fileName'], self.jsonObj['track1']['duration'], self.jsonObj['track1']['position'], self.jsonObj['track1']['crossfade'])
        self.track2.setUp(self.jsonObj['track2']['fileName'], self.jsonObj['track2']['duration'], self.jsonObj['track2']['position'], self.jsonObj['track2']['crossfade'])
        self.track1.volumeControl(self.jsonObj['track1']['volume'])
        self.track2.volumeControl(self.jsonObj['track2']['volume'])
        self.video1.setUp(self.jsonObj['clip1']['fileName'], self.jsonObj['clip1']['duration'], self.jsonObj['clip1']['position'])
        self.video2.setUp(self.jsonObj['clip2']['fileName'], self.jsonObj['clip2']['duration'], self.jsonObj['clip2']['position'])
        self.track1Volume.setSliderPosition(self.jsonObj['track1']['volume'])
        self.track2Volume.setSliderPosition(self.jsonObj['track2']['volume'])
        self.crossFadeControl.setSliderPosition(self.jsonObj['track2']['crossfade']*100)

    def keyPressEvent(self, event):
        #Control for scratch (On and off)
        if event.key() == 81:
            if self.leftScratch == False:
                self.leftScratch = True
                self.leftScratchMode.setText("Scratch: On")
            else:
                self.leftScratch = False
                self.leftScratchMode.setText("Scratch: Off")
        elif event.key() == 87:
            if self.rightScratch == False:
                self.rightScratch = True
                self.rightScratchMode.setText("Scratch: On")
            else:
                self.rightScratch = False
                self.rightScratchMode.setText("Scratch: Off")
        #Controls for volume
        elif event.key() == 65:
            changeVolume = self.track1Volume.value() + 1
            if(changeVolume > 100):
                return
            self.track1Volume.setSliderPosition(changeVolume)
            
        elif event.key() == 90:
            changeVolume = self.track1Volume.value() - 1
            if(changeVolume < 0):
                return
            self.track1Volume.setSliderPosition(changeVolume)
            
        elif event.key() == 83:
            changeVolume = self.track2Volume.value() + 1
            if(changeVolume > 100):
                return
            self.track2Volume.setSliderPosition(changeVolume)
            
        elif event.key() == 88:
            changeVolume = self.track2Volume.value() - 1
            if(changeVolume < 0):
                return
            self.track2Volume.setSliderPosition(changeVolume)
        #Controls for playback rate
        elif event.key() == 68:
            changeRate = self.playRateSlider1.value() + 1
            if(changeRate > 150):
                return
            self.playRateSlider1.setSliderPosition(changeRate)
            
        elif event.key() == 67:
            changeRate = self.playRateSlider1.value() - 1
            if(changeRate < 50):
                return
            self.playRateSlider1.setSliderPosition(changeRate)
            
        elif event.key() == 70:
            changeRate = self.playRateSlider2.value() + 1
            if(changeRate > 150):
                return
            self.playRateSlider2.setSliderPosition(changeRate)
            
        elif event.key() == 86:
            changeRate = self.playRateSlider2.value() - 1
            if(changeRate < 50):
                return
            self.playRateSlider2.setSliderPosition(changeRate)
        #Crossfade Control
        elif event.key() == 69:
            crossChange = self.crossFadeControl.value() - 1
            if(crossChange < 0):
                return
            self.crossFadeControl.setSliderPosition(crossChange)

        elif event.key() == 82:
            crossChange = self.crossFadeControl.value() + 1
            if(crossChange > 100):
                return
            self.crossFadeControl.setSliderPosition(crossChange)

    def closeEvent(self, event):
        settings = self.saveSetting()
        with open('setting.txt', 'w') as outfile:
            json.dump(settings, outfile)

    def mouseMoveEvent(self,event):
        difference = event.globalX() - self.mouseX
        self.mouseX = event.globalX()
        if self.leftScratch == True:
            if(difference > 0):
                self.track1.setScratchInfo(1)
            else:
                self.track1.setScratchInfo(-1)

        if self.rightScratch == True:
            if(difference > 0):
                self.track2.setScratchInfo(-1)
            else:
                self.track2.setScratchInfo(1)
                
#This is a holder that holds all the widgets      
class DJMovie(QGroupBox):
    def __init__(self):
        super().__init__()
        self.file = ""
        self.videoplayer = MoviePlayer(self)
        self.setUpButtons()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.file = e.mimeData().text()
        self.loadVideo(self.file)

    def loadVideo(self, file):
        self.videoplayer.loadVideo(file)

    def setUpButtons(self):
        self.play = QPushButton('play')
        self.play.clicked.connect(self.playV)
        self.pause = QPushButton('pause')
        self.pause.clicked.connect(self.pauseV)
        self.stop = QPushButton('stop')
        self.stop.clicked.connect(self.stopV)
        self.VLayout = QVBoxLayout()
        self.VLayout.addWidget(self.videoplayer)
        self.VLayout.addWidget(self.videoplayer.getSlider())
        self.control = QGroupBox('Video Controls')
        self.HLayout = QHBoxLayout()
        self.HLayout.addWidget(self.play)
        self.HLayout.addWidget(self.pause)
        self.HLayout.addWidget(self.stop)
        self.control.setLayout(self.HLayout)
        self.VLayout.addWidget(self.control)
        self.setLayout(self.VLayout)

    def playV(self):
        self.videoplayer.getMedia().play()

    def pauseV(self):
        self.videoplayer.getMedia().pause()
        
    def stopV(self):
        self.videoplayer.getMedia().stop()

    def getPosition(self):
        return self.videoplayer.getMedia().position()

    def getDuration(self):
        return self.videoplayer.getMedia().duration()

    def getTitle(self):
        return self.file

    def setUp(self, file, duration, position):
        self.file = file
        self.videoplayer.setUp(self.file, duration, position)

#This is a video widget class that has all the functionalities of a video player.
class MoviePlayer(QVideoWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mediaPlayer = QMediaPlayer()
        self.seekerBar = QSlider(Qt.Horizontal)
        self.mediaPlayer.setVolume(0)
       
    def getMedia(self):
        return self.mediaPlayer

    def getSlider(self):
        return self.seekerBar

    def loadVideo(self, file):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(file))))
        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.durationChanged.connect(self.setUpSlider)

    def setUpSlider(self):
        self.seekerBar.setRange(0, self.mediaPlayer.duration())
        self.seekerBar.setTickInterval(1)
        self.seekerBar.sliderMoved.connect(self.seek)
        self.mediaPlayer.positionChanged.connect(self.autoseek)
        self.autoseek()

    def setPosition(self, pos):
        self.mediaPlayer.setPosition(pos)

    def autoseek(self):
        self.seekerBar.setSliderPosition(self.mediaPlayer.position())
        if self.mediaPlayer.position() == self.mediaPlayer.duration():
            self.mediaPlayer.setPosition(0)
            self.seekerBar.setSliderPosition(0)
            self.mediaPlayer.play()
        
    def seek(self):
        self.mediaPlayer.setPosition(self.seekerBar.sliderPosition())

    def setUp(self, file, duration, position):
        self.loadVideo(file)
        self.setPosition(position)

#This class is a holder for all the audio widgets. Which includes the buttons for the audio control and the duration that the audio has played. It's a layout class that holds these widgets basically. 
class TrackPlayer(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.audiodevice = pyaudio.PyAudio()
        self.pos = 0
        self.sleep = 4098/44100
        self.mediaPlayer = QMediaPlayer()
        self.crossPosition = .5
        self.volumeAt = 100
        self.seekerBar = QSlider(Qt.Horizontal)
        self.file = ""
        self.chunk = 4098
        self.createButtons()
        
    def createButtons(self):
        self.addWidget(self.seekerBar)
        self.dropFileHere = DropFile("Drop and click here")
        self.dropFileHere.clicked.connect(self.retrieveFile)
        self.addWidget(self.dropFileHere)
        self.playButton = QPushButton('play')
        self.playButton.resize(25,25)
        self.playButton.clicked.connect(self.playM)
        self.pauseButton = QPushButton('pause')
        self.pauseButton.resize(25,25)
        self.pauseButton.clicked.connect(self.pauseM)
        self.stopButton = QPushButton('stop')
        self.stopButton.resize(25,25)
        self.stopButton.clicked.connect(self.stopM)
        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.playButton)
        self.hBox.addWidget(self.pauseButton)
        self.hBox.addWidget(self.stopButton)
        self.box = QGroupBox()
        self.box.setLayout(self.hBox)
        self.addWidget(self.box)

    def setupSeekerBar(self):
        self.seekerBar.setRange(0, self.mediaPlayer.duration())
        self.seekerBar.setTickInterval(1)
        self.seekerBar.sliderMoved.connect(self.seek)
        self.mediaPlayer.positionChanged.connect(self.autoseek)
        self.autoseek()

    def setPositionFromScratch(self, position):
        self.seekerBar.setSliderPosition(position)
        self.mediaPlayer.setPosition(position)

    def autoseek(self):
        try:
            self.seekerBar.setSliderPosition(self.mediaPlayer.position())
        except:
            return
        
    def seek(self):
        self.mediaPlayer.setPosition(self.seekerBar.sliderPosition())

    def setScratchInfo(self, direction):
        self.pos = int(direction*self.chunk + self.pos)%self.readaudio.getnframes()
        if direction < 0:
            self.readaudio.setpos(self.pos)
            self.data = audioop.reverse(self.readaudio.readframes(self.chunk), 2)
            self.readaudio.setpos(self.pos)
        else:
            self.data = self.readaudio.readframes(self.chunk)
            self.readaudio.setpos(self.pos)
        self.stream.write(self.data)
        time.sleep(self.sleep)
        
    def playM(self):
        self.mediaPlayer.play()
       
    def pauseM(self):
        self.mediaPlayer.pause()

    def stopM(self):
        self.mediaPlayer.stop()

    def crossVolumeControl(self, value):
        self.crossPosition = value
        self.volumeControl(self.volumeAt)

    def volumeControl(self, change):
        self.mediaPlayer.setVolume(change*self.crossPosition)
        self.volumeAt = change
        
    def loadTrack(self):
        try:
            self.readaudio = wave.open("finalmix2.wav", 'rb')
            self.stream = self.audiodevice.open(format = self.audiodevice.get_format_from_width(self.readaudio.getsampwidth()), channels = self.readaudio.getnchannels(), rate = int(self.readaudio.getframerate()), output = True)
            content = QMediaContent(QUrl.fromLocalFile(os.path.abspath(self.file)))
            self.mediaPlayer.setMedia(content)
            self.mediaPlayer.durationChanged.connect(self.setupSeekerBar)
        except:
            print("File not found or file format not compatible, please use .wav file")

    def retrieveFile(self):
        self.file = self.dropFileHere.getFile()
        print("Found: ", self.file)
        self.loadTrack()

    def getPosition(self):
        return self.mediaPlayer.position()

    def getDuration(self):
        return self.mediaPlayer.duration()

    def getTitle(self):
        return self.file

    def setUp(self, file, duration, position, crossPos):
        self.file = file
        self.loadTrack()
        self.setPosition(position)
        self.crossPosition = crossPos
        
    def setPosition(self, pos):
        self.mediaPlayer.setPosition(pos)

    def getVolume(self):
        return self.volumeAt

    def getCrossFade(self):
        return self.crossPosition

    def setPlaybackRate(self, rate):
        self.mediaPlayer.setPlaybackRate(rate)


#This is a button where user can drop a file to this button and click on it so that the program can retrieve the file name and use it.
class DropFile(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.file = ""
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.file = e.mimeData().text()

    def getFile(self):
        return self.file
    

    
