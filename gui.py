from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import time
import sys




class Worker(QThread):

    hrsSignal, minsSignal, secsSignal, timeExpressionSignal = Signal(str), Signal(str), Signal(str), Signal(str)

    def __init__(self):
        super().__init__()
        self.runningStatus = True
    def run(self):
        print("Timer has started.")
        self.tCINS = self.hrs * 3600 + self.mins * 60 + self.secs
        for i in range(self.tCINS + 1):
            if(self.runningStatus == True):
                time.sleep(1)
                self.timeExpression = f"{self.hrs}h{self.mins}m{self.secs}s"
                self.secs -= 1
                if(self.secs == -1):
                    self.mins -= 1
                    self.secs = 59
                    if(self.mins == -1):
                        if(self.hrs > 0):
                            self.hrs -= 1
                            self.mins = 59
                        else:
                            self.hrs = 0
                            self.mins = 59   
                self.hrsSignal.emit(str(self.hrs))
                self.minsSignal.emit(str(self.mins))
                self.secsSignal.emit(str(self.secs))
                self.timeExpressionSignal.emit(str(self.timeExpression))
            else:
                break

    def stop(self):
        self.runningStatus = False
        print('Timer has stopped.')
        self.hrs, self.mins, self.secs = 0, 0, 0
    def pause(self):
        self.runningStatus = False


class Window(QWidget):
    def __init__(self):
        self.programStatus = ""
        super().__init__()



        self.setStyleSheet('background-color: #171515; color: #151515;')
        self.setWindowTitle("jRemite")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('tragedy.png'))
        self.resize(700, 300)
        self.initGui()

    def initGui(self):



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




        self.endTimeLabel = QLabel(parent=self, text='Time Until End: ')
        self.endTimeLabel.setFont(QFont('Times New Roman', 12))
        self.endTimeLabel.setStyleSheet('color: white;')
        self.endTimeLabel.setAlignment(Qt.AlignCenter)
        self.endTimeLabel.move(400, self.height() - 40)





        self.buttonsList = [QPushButton(parent=self, text='Start'), QPushButton(parent=self, text='Pause'), QPushButton(parent=self, text='Stop')]
        self.labelsList = [QLabel(parent=self, text='Hours'), QLabel(parent=self, text='Minutes'), QLabel(parent=self, text='Seconds')]
        self.entriesList = [QLineEdit(parent=self, text='00'), QLineEdit(parent=self, text='00'), QLineEdit(parent=self, text='00')]

        self.mainLayout = QVBoxLayout(self)
        self.buttonsLayout = QHBoxLayout(parent=self.mainLayout)
        self.labelsLayout = QHBoxLayout(parent=self.mainLayout)
        self.entriesLayout = QHBoxLayout(parent=self.mainLayout)





        self.buttonsList[0].setStyleSheet('background-color: #070036; color: white;')
        self.buttonsList[0].clicked.connect(lambda: self.buttonsList[0].setEnabled(False))
        self.buttonsList[0].clicked.connect(lambda: self.buttonsList[1].setEnabled(True))
        self.buttonsList[0].clicked.connect(lambda: self.buttonsList[2].setEnabled(True))
        self.buttonsList[0].clicked.connect(lambda: self.entriesList[0].setEnabled(False))
        self.buttonsList[0].clicked.connect(lambda: self.entriesList[1].setEnabled(False))
        self.buttonsList[0].clicked.connect(lambda: self.entriesList[2].setEnabled(False))
        self.buttonsList[0].clicked.connect(self.beginTimer)


    
        self.buttonsList[1].setStyleSheet('background-color: #005B6F; color: white;')
        self.buttonsList[1].clicked.connect(lambda: self.timerWorker.pause())
        self.buttonsList[1].clicked.connect(lambda: self.buttonsList[0].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.buttonsList[1].setEnabled(False))
        self.buttonsList[1].clicked.connect(lambda: self.buttonsList[2].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.entriesList[0].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.entriesList[1].setEnabled(True))
        self.buttonsList[1].clicked.connect(lambda: self.entriesList[2].setEnabled(True))
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
        self.buttonsList[2].clicked.connect(lambda: self.timerWorker.stop())
        self.buttonsList[2].setEnabled(False)


        for i in range(len(self.entriesList)):
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
        for j in range(len(self.labelsList)):
            self.labelsList[j].setStyleSheet('background-color: #171515; color: white;')
            self.labelsList[j].setAlignment(Qt.AlignCenter)
            self.labelsList[j].setFont(QFont('Times New Roman', 20))
        for k in range(len(self.labelsList)):
            self.labelsLayout.addWidget(self.labelsList[k])
        for i in range(len(self.buttonsList)):
            self.buttonsList[i].setFixedHeight(30)
            self.buttonsLayout.addWidget(self.buttonsList[i])
        for j in range(len(self.entriesList)):
            self.entriesLayout.addWidget(self.entriesList[j])

        self.mainLayout.addLayout(self.labelsLayout)
        self.mainLayout.addLayout(self.entriesLayout)
        self.mainLayout.addLayout(self.buttonsLayout)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setSpacing(40)


        self.setLayout(self.mainLayout)



    def start_button_pressed(self):
        pass

    def pause_button_pressed(self):
        pass

    def stop_button_pressed(self):
        pass

    def entry_enter_key_pressed(self):
        pass




    def beginTimer(self):
        # I don't know how to solve this.
        self.timerThread = QThread(parent=self)
        self.timerWorker = Worker()
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
            print("The timer has reached its end.")
            for k in range(len(self.entriesList)):
                self.entriesList[k].setText('00')
            self.buttonsList[0].setEnabled(True)
            self.entriesList[0].setEnabled(True)
            self.entriesList[1].setEnabled(True)
            self.entriesList[2].setEnabled(True)
            self.timerWorker.stop()
        else:
            print("The timer is ongoing.")
            pass
    

            
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(QColor('#B3B6B7'), 10, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, self.width(), self.height()))
        painter.end()


    def closeEvent(self, event):
        try:
            self.timerWorker.terminate()
            self.timerThread.terminate()
            print('Closed with threads.')
        except:
            print('Closed without threads.')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = QPoint(event.position().x(),event.position().y())
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if(self.offset is not None and event.buttons() == Qt.LeftButton):
            self.move(self.pos() + QPoint(event.scenePosition().x(),event.scenePosition().y()) - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


