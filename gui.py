from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import time
import sys

"""
to do:
- fix timer functionality: DONE!
- file that stores previously selected timers: SOLVED. IN PROCESS OF INTEGRATION.
- show when the timer will end: ONGOING.
- implement multithreading and multiprocessing: DONE!.
- implement proper stop button: DONE!
- fix ui look: DONE!
I won't back away. I'm moving forward. Just like a centipede.
"""


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
        self.programStatus = False



class Window(QWidget):
    def __init__(self):
        self.programStatus = ""
        super().__init__()




        self.setStyleSheet('background-color: #171515; color: #151515;')
        self.setWindowTitle("jRemite")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(600, 300)
        self.initGui()

    def initGui(self):

        

        self.onlyInt = QIntValidator()
        
        self.buttonLayout = QHBoxLayout(self)


        self.startTimerButton = QPushButton(parent=self)
        self.startTimerButton.setText('Start')
        self.startTimerButton.setStyleSheet('background-color: #070036; color: white;')
        self.startTimerButton.clicked.connect(lambda: self.startTimerButton.setEnabled(False))
        self.startTimerButton.clicked.connect(lambda: self.stopTimerButton.setEnabled(True))
        self.startTimerButton.clicked.connect(self.beginTimer)


        

        self.pauseTimerButton = QPushButton(parent=self)
        self.pauseTimerButton.setText('Pause')
        self.pauseTimerButton.setStyleSheet('background-color: #B3B6B7; color: white;')
        self.pauseTimerButton.setEnabled(False)

        """
        self.pauseTimerButton.clicked.connect(lambda: self.startTimerButton.setEnabled(True))
        self.pauseTimerButton.clicked.connect(lambda: self.stopTimerButton.setEnabled(False))
        self.pauseTimerButton.clicked.connect(lambda: self.timerWorker.stop())
        self.pauseTimerButton.clicked.connect(lambda: self.hrsBox.setText('00'))
        self.pauseTimerButton.clicked.connect(lambda: self.minsBox.setText('00'))
        self.pauseTimerButton.clicked.connect(lambda: self.secsBox.setText('00'))
        """


        self.stopTimerButton = QPushButton(parent=self)
        self.stopTimerButton.setText('Stop')
        self.stopTimerButton.setStyleSheet('background-color: #2C0000; color: white;')
        self.stopTimerButton.setEnabled(False)

        self.stopTimerButton.clicked.connect(lambda: self.startTimerButton.setEnabled(True))
        self.stopTimerButton.clicked.connect(lambda: self.stopTimerButton.setEnabled(False))
        self.stopTimerButton.clicked.connect(lambda: self.timerWorker.stop())
        self.stopTimerButton.clicked.connect(lambda: self.hrsBox.setText('00'))
        self.stopTimerButton.clicked.connect(lambda: self.minsBox.setText('00'))
        self.stopTimerButton.clicked.connect(lambda: self.secsBox.setText('00'))
        


        self.startTimerButton.setFixedWidth(120)
        self.pauseTimerButton.setFixedWidth(120)
        self.stopTimerButton.setFixedWidth(120)




        self.hrsBox = QLineEdit(self)
        self.hrsBox.setFixedSize(410/3, 60)
        self.hrsBox.move(90, 90)

        self.minsBox = QLineEdit(self)
        self.minsBox.setFixedSize(410/3, 60)
        self.minsBox.move(85 + 410/3, 90)

        self.secsBox = QLineEdit(self)
        self.secsBox.setFixedSize(410/3 + 10, 60)
        self.secsBox.move(80 + 2 * 410/3, 90)



        self.hrsBox.setStyleSheet('color: white;')
        self.minsBox.setStyleSheet('color: white;')
        self.secsBox.setStyleSheet('color: white;')


        self.hrsBox.setText('00')
        self.minsBox.setText('00')
        self.secsBox.setText('00')

        self.hrsBox.setFont(QFont('Arial', 25))
        self.minsBox.setFont(QFont('Arial', 25))
        self.secsBox.setFont(QFont('Arial', 25))


        self.hrsBox.setAlignment(Qt.AlignCenter)
        self.minsBox.setAlignment(Qt.AlignCenter)
        self.secsBox.setAlignment(Qt.AlignCenter)


        self.hrsBox.setValidator(self.onlyInt)
        self.minsBox.setValidator(self.onlyInt)
        self.secsBox.setValidator(self.onlyInt)


        self.hrsBox.setMaxLength(2)
        self.minsBox.setMaxLength(2)
        self.secsBox.setMaxLength(2)


        self.hrsBox.returnPressed.connect(self.beginTimer)
        self.minsBox.returnPressed.connect(self.beginTimer)
        self.secsBox.returnPressed.connect(self.beginTimer)



        self.hoursLabel = QLabel(self)
        self.hoursLabel.setText('Hours')
        self.hoursLabel.setStyleSheet('background-color: #171515; color: #565656;')
        self.hoursLabel.setFont(QFont('Times New Roman', 20))
        self.hoursLabel.move(120, 50)


        self.minutesLabel = QLabel(self)
        self.minutesLabel.setText('Minutes')
        self.minutesLabel.setStyleSheet('background-color: #171515; color: #565656;')
        self.minutesLabel.setFont(QFont('Times New Roman', 20))
        self.minutesLabel.move(240, 50)


        self.secondsLabel = QLabel(self)
        self.secondsLabel.setText('Seconds')
        self.secondsLabel.setStyleSheet('background-color: #171515; color: #565656;')
        self.secondsLabel.setFont(QFont('Times New Roman', 20))
        self.secondsLabel.move(370, 50)

        



    def beginTimer(self):
        # I don't know how to solve this.
        self.timerThread = QThread(parent=self)
        self.timerWorker = Worker()
        self.timerWorker.moveToThread(self.timerThread)
        self.timerWorker.start()
        self.timerWorker.hrs = int(self.hrsBox.text())
        self.timerWorker.mins = int(self.minsBox.text())
        self.timerWorker.secs = int(self.secsBox.text())
        self.timerWorker.hrsSignal.connect(self.hrsBox.setText)
        self.timerWorker.minsSignal.connect(self.minsBox.setText)
        self.timerWorker.secsSignal.connect(self.secsBox.setText)
        self.timerWorker.timeExpressionSignal.connect(lambda: self.checkTimerExpression())




        

    def checkTimerExpression(self):
        if(self.timerWorker.timeExpression == '0h0m0s'):
            print("The timer has reached its end.")
            self.hrsBox.setText('00')
            self.minsBox.setText('00')
            self.secsBox.setText('00')
            self.startTimerButton.setEnabled(True)
            self.timerWorker.stop()
        else:
            print("The timer is ongoing.")
            pass
    


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(QColor('#333333'), 40, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(0, 0, 600, 300)
        painter.end()


    def closeEvent(self, event):
        try:
            print('Closed with threads.')
            self.timerWorker.terminate()
            self.timerThread.terminate()
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

