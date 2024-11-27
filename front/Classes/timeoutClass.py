from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/Classes/timeoutClass.ui")[0]
class timeoutMsgBox(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.timeoutFlag = True

    # 창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    # 창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Buttons
    def timeout_Addtime(self) :
        self.timeoutFlag = False
        self.close()

class timeoutClass :
    timeout_Time = 3 * 60
    add_Time = 60
    remain_Time = timeout_Time

    def __init__(self, parent) :
        self.__timer = QTimer()
        self.__parent = parent
        self.timer.timeout.connect(self.update_timer)

    #Getter
    @property
    def timer(self) :
        return self.__timer
    @property
    def parent(self) :
        return self.__parent

    #Setter

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

