import sys, os, wave, pyaudio
from stat import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from DJModel import *

class DJView(DJModel):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JAM DJ")
        self.setGeometry(self.startX,self.startY, self.winX,self.winY)
        self.showMaximized()

        self.buildList()
        if len(self.trackList) > len(self.clipList):
            row = len(self.trackList)
        else:
            row = len(self.clipList)
        self.setUpCrossFadeControl()
        self.setVolumeControl1()
        self.setVolumeControl2()
        self.setupPlaybackRateBar1()
        self.setupPlaybackRateBar2()
        self.getJsonObj()
        self.setupSetting()
        self.table = self.buildTable(row, 2)
        self.fillTable(self.trackList, self.clipList)
        self.setupLayout()
        self.show()

    #Create the table widget
    def buildTable(self, row, column):
        table = QTableWidget()
        table.setRowCount(row)
        table.setColumnCount(column)
        return table

    #It's to search for available media files and save these file names in an array
    def buildList(self):
        self.trackList.clear()
        self.clipList.clear()
        for x in os.listdir():
            if x.endswith('.avi') or x.endswith('.mp3') or x.endswith('.mpg') or x.endswith('.wav'):
                self.clipList.append(x)
                self.trackList.append(x)

    #I have to populate the table with file names available for playing
    def fillTable(self, obj1, obj2):
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Title'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Clips'))
        for i in range(0, len(self.trackList), 1):
            item = QLineEdit(obj1[i])
            item.setDragEnabled(True)
            item.setReadOnly(True)
            self.table.setCellWidget(i, 0, item)
        for t in range(0, len(self.clipList), 1):
            item = QLineEdit(obj2[t])
            item.setDragEnabled(True)
            item.setReadOnly(True)
            self.table.setCellWidget(t, 1, item)

    def setupPlaybackRateBar1(self):
        self.playRateSlider1.setRange(50, 150)
        self.playRateSlider1.setSliderPosition(100)
        self.playRateSlider1.setTickInterval(1)
        self.playRateSlider1.valueChanged.connect(self.changePlayRate1)
        self.playRateReset1.clicked.connect(self.playrateReset1)

    def playrateReset1(self):
        self.track1.setPlaybackRate(1.0)
        self.playRateSlider1.setSliderPosition(100)

    def changePlayRate1(self):
        rate = self.playRateSlider1.value()/100
        self.track1.setPlaybackRate(rate)

    def setupPlaybackRateBar2(self):
        self.playRateSlider2.setRange(50, 150)
        self.playRateSlider2.setSliderPosition(100)
        self.playRateSlider2.setTickInterval(1)
        self.playRateSlider2.valueChanged.connect(self.changePlayRate2)
        self.playRateReset2.clicked.connect(self.playrateReset2)

    def playrateReset2(self):
        self.track2.setPlaybackRate(1.0)
        self.playRateSlider2.setSliderPosition(100)

    def changePlayRate2(self):
        rate = self.playRateSlider2.value()/100
        self.track2.setPlaybackRate(rate)

    def setUpCrossFadeControl(self):
        self.crossFadeControl.setRange(0, 100)
        self.crossFadeControl.setSliderPosition(50)
        self.crossFadeControl.setTickInterval(1)
        self.crossFadeControl.valueChanged.connect(self.crossFadeController)

    #When crossfade value changes, this function will be called to update the volumes
    def crossFadeController(self):
        value = self.crossFadeControl.value()/100
        self.track2.crossVolumeControl(value)
        self.track1.crossVolumeControl(1 - value)

    def setVolumeControl1(self):
        self.track1Volume.setRange(0,100)
        self.track1Volume.setSliderPosition(100)
        self.track1Volume.setTickInterval(1)
        self.track1Volume.valueChanged.connect(self.volume1)

    #When volume seeker bar value changes, this will be called to alter the changes in volume
    def volume1(self):
        percentVolume = self.track1Volume.value()
        self.track1.volumeControl(percentVolume)

    def setVolumeControl2(self):
        self.track2Volume.setRange(0,100)
        self.track2Volume.setSliderPosition(100)
        self.track2Volume.setTickInterval(1)
        self.track2Volume.valueChanged.connect(self.volume2)

    def volume2(self):
        percentVolume = self.track2Volume.value()
        self.track2.volumeControl(percentVolume)

    def setupLayout(self):
        self.track1Widget.setLayout(self.track1)
        self.track2Widget.setLayout(self.track2)
        self.trackControl.addWidget(self.track1Volume)
        self.trackControl.addWidget(self.track1Widget)
        
        #Layout for playrate slider and a button
        self.playrateBarHolder1 = QVBoxLayout()
        self.playrateBarHolder1.addWidget(self.playRateSlider1)
        self.playrateBarHolder1.addWidget(self.playRateReset1)
        self.playrateBarHolder1.addWidget(self.leftScratchMode)
        self.box1 = QGroupBox('Playrate')
        self.box1.setLayout(self.playrateBarHolder1)
        self.trackControl.addWidget(self.box1)
        
        self.trackControl.addWidget(self.video1)
        self.trackControl.addWidget(self.crossFadeControl)
        self.trackControl.addWidget(self.video2)
        
        #Layout for playrate slider and a button
        self.playrateBarHolder2 = QVBoxLayout()
        self.playrateBarHolder2.addWidget(self.playRateSlider2)
        self.playrateBarHolder2.addWidget(self.playRateReset2)
        self.playrateBarHolder2.addWidget(self.rightScratchMode)
        self.box2 = QGroupBox('Playrate')
        self.box2.setLayout(self.playrateBarHolder2)
        self.trackControl.addWidget(self.box2)

        self.trackControl.addWidget(self.track2Widget)
        self.trackControl.addWidget(self.track2Volume)
        self.controlWidget.setLayout(self.trackControl)
        self.windowLayout.addWidget(self.controlWidget)
        self.tracklist.addWidget(self.table)
        self.listWidget.setLayout(self.tracklist)
        self.windowLayout.addWidget(self.listWidget)
        self.setLayout(self.windowLayout)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = DJView()
    sys.exit(app.exec_())
