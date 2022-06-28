from cgi import MiniFieldStorage
import time, datetime
from PySide6.QtCore import *

class TimerWorker(QThread):

    hrsSignal, minsSignal, secsSignal, timeExpressionSignal = Signal(str), Signal(str), Signal(str), Signal(str)

    def __init__(self):
        super().__init__()
        self.runningStatus = True
    def run(self):
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

class TimeWorker(QThread):
    currentTimeSignal = Signal(str)
    def run(self):
        while(True):
            time.sleep(1)
            self.current_time = datetime.datetime.now()
            self.current_time_text = self.current_time.strftime("%I:%M:%S")
            self.currentTimeSignal.emit(self.current_time_text)

