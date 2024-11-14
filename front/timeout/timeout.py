from PyQt5.QtCore import *
from .timeoutMsgbox import *

class timeoutClass :

    #Class_Variables
    timeout_Time = 3 * 60
    add_Time = 60
    remain_Time = timeout_Time

    def __init__(self, parent) :
        self.timer = QTimer()
        self.parent = parent
        self.timer.timeout.connect(self.update_timer)

    def timeout_Start(self, timeValue) :
        self.timer.start(1000)      #interval(ms)
        self.remain_Time = timeValue
        self.parent.lcd_Timer.display(self.remain_Time)

    def timeout_Do(self) :
        self.parent.set_MainPage_Index(0)
 
    def update_timer(self) :
        if self.remain_Time > 0 :
            self.remain_Time -= 1
            self.parent.lcd_Timer.display(self.remain_Time)
        else :
            self.timeout_Stop()
            timeoutMsgbox = timeoutMsgBox()
            timeoutMsgbox.showModal()

            timeoutFlag = timeoutMsgbox.timeoutFlag
            if timeoutFlag == True :
                timeoutMsgbox.close()
                self.timeout_Do()
            else :
                timeoutMsgbox.close()
                self.timeout_Start(self.timeout_Time)
    
    def timeout_Stop(self) :
        self.timer.stop()

    def timeout_Pause(self) :
        self.pause_Time = self.remain_Time
        self.parent.lcd_Timer.display(self.pause_Time)
        self.timer.stop()

    def timeout_Resume(self, timeValue) :
        self.timer.start(1000)      #interval(ms)
        self.remain_Time = timeValue
        self.parent.lcd_Timer.display(self.remain_Time)

