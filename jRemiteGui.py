from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from jRemiteGuiWorkers import TimerWorker, TimeWorker
import time, datetime, sys



"""
to do:
- fix timer functionality: DONE!
- implement multithreading and multiprocessing: DONE!.
- implement proper stop button: DONE!
- fix ui look: DONE!
- add exit, hide buttons: DONE!
- save previously used timers
- show current time
- show when timer will end
- optimize code
I won't back away. I'm moving forward. Just like a centipede.
"""




class EOTWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #080016; color: #151515;')
        self.setWindowTitle("Timer has ended")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('tragedy.png'))
        self.resize(400, 300)
        self.initGui()
        self.show()

    
    def initGui(self):
        self.exitBtn = QPushButton(parent=self, text='X')
        self.exitBtn.setFont(QFont('Arial', 12))
        self.exitBtn.setStyleSheet('color: white; border: 3px solid; font-weight: bold; border-top-color: #B3B6B7; border-bottom-color: #B3B6B7; border-left-color: #B3B6B7; border-right-color: #B3B6B7; ')        
        self.exitBtn.move(300, 0)

        self.minimizeBtn = QPushButton(parent=self, text='-')
        self.minimizeBtn.clicked.connect(self.showMinimized)
        self.minimizeBtn.setFont(QFont('Arial', 12))
        self.minimizeBtn.setStyleSheet('color: white; border: 3px solid; font-weight: bold; border-top-color: #B3B6B7; border-bottom-color: #B3B6B7; border-left-color: #B3B6B7; border-right-color: #B3B6B7; ')
        self.minimizeBtn.move(205, 0)

        self.textLabel = QLabel(self, text='Your timer has ended! Please check the jRemite appication window.')
        self.textLabel.setStyleSheet('color: white;')
        self.textLabel.setFont(QFont('Times New Roman', 18))

        self.textLabel.move(0, 200)
        

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(QColor('#B3B6B7'), 10, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, self.width(), self.height()))
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = QPoint(event.position().x(),event.position().y())
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if(self.offset != None and event.buttons() == Qt.LeftButton):
            self.move(self.pos() + QPoint(event.scenePosition().x(),event.scenePosition().y()) - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)



class Window(QWidget):
    def __init__(self):
        self.programStatus = ""
        super().__init__()
        self.setStyleSheet('background-color: #080016; color: #151515;')
        self.setWindowTitle("jRemite")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('tragedy.png'))
        self.resize(700, 300)
        self.initGui()

    def initGui(self):

        self.mainLayout = QVBoxLayout(self)
        self.buttonsLayout = QHBoxLayout(parent=self.mainLayout)
        self.labelsLayout = QHBoxLayout(parent=self.mainLayout)
        self.entriesLayout = QHBoxLayout(parent=self.mainLayout)



        self.exitBtn = QPushButton(parent=self, text='X')
        self.exitBtn.clicked.connect(self.closeEvent)
        self.exitBtn.clicked.connect(exit)
        self.exitBtn.setFont(QFont('Arial', 12))
        self.exitBtn.setStyleSheet('color: white; border: 3px solid; font-weight: bold; border-top-color: #B3B6B7; border-bottom-color: #B3B6B7; border-left-color: #B3B6B7; border-right-color: #B3B6B7; ')        
        self.exitBtn.move(600, 0)

        self.minimizeBtn = QPushButton(parent=self, text='-')
        self.minimizeBtn.clicked.connect(self.showMinimized)
        self.minimizeBtn.setFont(QFont('Arial', 12))
        self.minimizeBtn.setStyleSheet('color: white; border: 3px solid; font-weight: bold; border-top-color: #B3B6B7; border-bottom-color: #B3B6B7; border-left-color: #B3B6B7; border-right-color: #B3B6B7; ')
        self.minimizeBtn.move(505, 0)
        
 
        



        self.currentTimeLabel = QLabel(parent=self, text='Current Time: ')
        self.currentTimeLabel.setFont(QFont('Times New Roman', 12))
        self.currentTimeLabel.setStyleSheet('color: white;')
        self.currentTimeLabel.setAlignment(Qt.AlignCenter)
        self.currentTimeLabel.move(10, self.height() - 40)


        self.whatTheHellIsThis = QLabel(parent=self, text='')
        self.whatTheHellIsThis.setFont(QFont('Times New Roman', 12))
        self.whatTheHellIsThis.setStyleSheet('color: white;')
        self.whatTheHellIsThis.setAlignment(Qt.AlignCenter)
        self.whatTheHellIsThis.move(98, self.height() - 40)


        self.timeThread = QThread(parent=self)
        self.timeWorker = TimeWorker()
        self.timeWorker.moveToThread(self.timeThread)
        self.timeWorker.start()




                




        self.endTimeLabel = QLabel(parent=self, text='Time Until End: ')
        self.endTimeLabel.setFont(QFont('Times New Roman', 12))
        self.endTimeLabel.setStyleSheet('color: white;')
        self.endTimeLabel.setAlignment(Qt.AlignCenter)
        self.endTimeLabel.move(380, self.height() - 40)

        self.nandaYoKoreWa = QLabel(parent=self, text='N/A')
        self.nandaYoKoreWa.setFont(QFont('Times New Roman', 12))
        self.nandaYoKoreWa.setStyleSheet('color: white;')
        self.nandaYoKoreWa.setAlignment(Qt.AlignCenter)
        self.nandaYoKoreWa.move(488, self.height() - 40)


        self.timeWorker.currentTimeSignal.connect(self.whatTheHellIsThis.setText)
        




        self.buttonsList = [QPushButton(parent=self, text='Start'), QPushButton(parent=self, text='Pause'), QPushButton(parent=self, text='Stop')]
        self.labelsList = [QLabel(parent=self, text='Hours'), QLabel(parent=self, text='Minutes'), QLabel(parent=self, text='Seconds')]
        self.entriesList = [QLineEdit(parent=self, text='00'), QLineEdit(parent=self, text='00'), QLineEdit(parent=self, text='00')]
        self.layoutsList = [self.labelsLayout, self.entriesLayout, self.buttonsLayout]




        self.buttonsList[0].setStyleSheet('background-color: #070036; color: white;')
        self.buttonsList[0].clicked.connect(lambda: self.buttonsList[0].setEnabled(False))
        self.buttonsList[0].clicked.connect(lambda: self.buttonsList[1].setEnabled(True))
        self.buttonsList[0].clicked.connect(lambda: self.buttonsList[2].setEnabled(True))
        self.buttonsList[0].clicked.connect(lambda: self.entriesList[0].setEnabled(False))
        self.buttonsList[0].clicked.connect(lambda: self.entriesList[1].setEnabled(False))
        self.buttonsList[0].clicked.connect(lambda: self.entriesList[2].setEnabled(False))
        self.buttonsList[0].clicked.connect(self.getEOT)
        self.buttonsList[0].clicked.connect(self.beginTimer)


    
        self.buttonsList[1].setStyleSheet('background-color: #005B6F; color: white;')
        self.buttonsList[1].clicked.connect(lambda: self.timerWorker.pause())
        self.buttonsList[1].clicked.connect(lambda: self.buttonsList[0].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.buttonsList[1].setEnabled(False))
        self.buttonsList[1].clicked.connect(lambda: self.buttonsList[2].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.entriesList[0].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.entriesList[1].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.entriesList[2].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.nandaYoKoreWa.setText('N/A'))
        self.buttonsList[1].setEnabled(False)


        self.buttonsList[2].setStyleSheet('background-color: #2C0000; color: white;')
        self.buttonsList[2].clicked.connect(lambda: self.buttonsList[0].setEnabled(True))
        self.buttonsList[2].clicked.connect(lambda: self.buttonsList[1].setEnabled(False))
        self.buttonsList[2].clicked.connect(lambda: self.buttonsList[2].setEnabled(False))
        self.buttonsList[2].clicked.connect(lambda: self.entriesList[0].setEnabled(True))
        self.buttonsList[2].clicked.connect(lambda: self.entriesList[1].setEnabled(True))
        self.buttonsList[2].clicked.connect(lambda: self.entriesList[2].setEnabled(True))
        self.buttonsList[2].clicked.connect(lambda: self.entriesList[0].setText('00'))
        self.buttonsList[2].clicked.connect(lambda: self.entriesList[1].setText('00'))
        self.buttonsList[2].clicked.connect(lambda: self.entriesList[2].setText('00'))
        self.buttonsList[2].clicked.connect(lambda: self.nandaYoKoreWa.setText('N/A'))
        self.buttonsList[2].clicked.connect(lambda: self.timerWorker.stop())
        self.buttonsList[2].setEnabled(False)


        for i in range(3):
            self.entriesList[i].setStyleSheet('color: white;')
            self.entriesList[i].setAlignment(Qt.AlignCenter)
            self.entriesList[i].setValidator(QIntValidator())
            self.entriesList[i].setMaxLength(2)
            self.entriesList[i].setFont(QFont('Arial', 25))
            self.entriesList[i].returnPressed.connect(self.beginTimer)
            self.entriesList[i].returnPressed.connect(lambda: self.buttonsList[0].setEnabled(False))
            self.entriesList[i].returnPressed.connect(lambda: self.buttonsList[1].setEnabled(True))
            self.entriesList[i].returnPressed.connect(lambda: self.buttonsList[2].setEnabled(True))
            self.entriesList[i].returnPressed.connect(lambda: self.entriesList[0].setEnabled(False))
            self.entriesList[i].returnPressed.connect(lambda: self.entriesList[1].setEnabled(False))
            self.entriesList[i].returnPressed.connect(lambda: self.entriesList[2].setEnabled(False))
            self.entriesList[i].setText('00')
            self.labelsList[i].setStyleSheet('background-color: #080016; color: white;')
            self.labelsList[i].setAlignment(Qt.AlignCenter)
            self.labelsList[i].setFont(QFont('Times New Roman', 20))
            self.buttonsList[i].setFixedHeight(30)
            self.labelsLayout.addWidget(self.labelsList[i])
            self.buttonsLayout.addWidget(self.buttonsList[i])
            self.entriesLayout.addWidget(self.entriesList[i])
            self.mainLayout.addLayout(self.layoutsList[i])
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setSpacing(40)


        self.setLayout(self.mainLayout)







    def beginTimer(self):
        for i in range(len(self.entriesList)):
            if(self.entriesList[i].text() == '' or self.entriesList[i].text() == ' ' or self.entriesList[i].text() == '  '):
                self.entriesList[i].setText('00')
            else:
                continue
        self.getEOT()
        self.timerThread = QThread(parent=self)
        self.timerWorker = TimerWorker()
        self.timerWorker.moveToThread(self.timerThread)
        self.timerWorker.start()
        self.timerWorker.hrs = int(self.entriesList[0].text())
        self.timerWorker.mins = int(self.entriesList[1].text())
        self.timerWorker.secs = int(self.entriesList[2].text())
        self.timerWorker.hrsSignal.connect(self.entriesList[0].setText)
        self.timerWorker.minsSignal.connect(self.entriesList[1].setText)
        self.timerWorker.secsSignal.connect(self.entriesList[2].setText)
        self.timerWorker.timeExpressionSignal.connect(lambda: self.checkTimerExpression())
    def checkTimerExpression(self):
        if(self.timerWorker.timeExpression == '0h0m0s'):
            self.nandaYoKoreWa.setText('N/A')
            for k in range(len(self.entriesList)):
                self.entriesList[k].setText('00')
            self.buttonsList[0].setEnabled(True)
            self.entriesList[0].setEnabled(True)
            self.entriesList[1].setEnabled(True)
            self.entriesList[2].setEnabled(True)
            self.timerWorker.stop()

            self.eotWindow = EOTWindow()


        else:
            pass
    # EOT: End Of Timer
    def getEOT(self):
        
        # Instantiate the EOT expression.
        self.EOT = None


        # Get time components.
        self.time_components, self.adder_var, self.current_time = [], '', datetime.datetime.now().strftime("%I:%M:%S")
        self.current_time = self.current_time.replace(':', ' ')
        self.current_time += ' '
        for i in range(len(self.current_time)):
            if(self.current_time[i] != ' '):
                self.adder_var += self.current_time[i]
            else:
                self.time_components.append(self.adder_var)
                self.adder_var = ''

        # Add selected time to above time components.
        # The selected time is the current text of the elements in the entriesList array. 

        for i in range(len(self.time_components)):
            try:
                self.time_components[i] = int(self.time_components[i])
                self.time_components[i] += int(self.entriesList[i].text())
            except:
                continue
        # Now fix the new obtained time.

        while(self.time_components[2] > 59):
            self.time_components[2] = (self.time_components[2] - 60)
            self.time_components[1] += 1
        while(self.time_components[1] > 59):
            self.time_components[1] = (self.time_components[1] - 60)
            self.time_components[0] += 1



        # Now, let's check how many hours the user selected. From that, we'll create our EOT.


        if(self.time_components[0] > 24):
            self.EOT = f'{int(self.time_components[0] / 24)} day(s)'
        else:
            for i in range(len(self.time_components)):
                if(self.time_components[i] <= 9):
                    self.time_components[i] = str(self.time_components[i])
                    self.time_components[i] = '0' + self.time_components[i]
                else:
                    continue
            self.EOT = f'{self.time_components[0]}:{self.time_components[1]}:{self.time_components[2]}'
        # Now, set the nandaYoKoreWa Label Variable's text to self.EOT.

        self.nandaYoKoreWa.setText(self.EOT)



    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(QColor('#B3B6B7'), 10, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, self.width(), self.height()))
        painter.end()
    def closeEvent(self, event):
        self.timeWorker.terminate()
        self.timeThread.terminate()
        try:
            self.timerWorker.terminate()
            self.timerThread.terminate()
            print('Closed with timer threads.')
        except:
            print('Closed without timer threads.')
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = QPoint(event.position().x(),event.position().y())
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if(self.offset != None and event.buttons() == Qt.LeftButton):
            self.move(self.pos() + QPoint(event.scenePosition().x(),event.scenePosition().y()) - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)