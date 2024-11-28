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

        self.__timeoutFlag = True

    @property
    def timeoutFlag(self) :
        return self.__timeoutFlag

    @timeoutFlag.setter
    def timeoutFlag(self, val) :
        if type(val) != bool :
            raise TypeError('bool 형식만 가능합니다.')
        self.__timeoutFlag = val

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
    TIMEOUT_TIME = 3 * 60         # Constant
    ADD_TIME = 60                 # Constant
    __remain_Time = TIMEOUT_TIME

    def __init__(self, parent) :
        self.__timer = QTimer()
        self.__parent = parent

        # Interval마다 실행할 함수 설정
        self.timer.timeout.connect(self.update_timer)

    # Getter
    @property
    def remain_Time(self) :
        return self.__remain_Time
    @property
    def timer(self) :       # QTimer객체
        return self.__timer
    @property
    def parent(self) :
        return self.__parent

    # Setter
    @remain_Time.setter
    def remain_Time(self, val) :
        self.__remain_Time = val

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
                self.timeout_Start(self.TIMEOUT_TIME)
    
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

    #Timer_AddTime/타이머 시간추가
    def add_timer(self) :
        self.remain_Time += self.ADD_TIME
        self.parent.lcd_Timer.display(self.remain_Time)


