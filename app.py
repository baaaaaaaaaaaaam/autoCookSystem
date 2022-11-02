import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import service
import time
import query
import api
import imageCrop
from PyQt5.QtCore import *
from threading import Thread



form_class = uic.loadUiType("cook.ui")[0]
class MyApp(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('robot cooking program')
        self.btn_1.setStyleSheet("background-color: #DCDCDC")
        self.btn_2.setStyleSheet("background-color: #DCDCDC")
        self.btn_1.clicked.connect(self.cookingBone)
        self.btn_2.clicked.connect(self.cookingBoneless)
        self.menuLabelList = [self.fr_1_lb_menu,self.fr_2_lb_menu,self.fr_3_lb_menu,self.fr_4_lb_menu,self.fr_5_lb_menu,self.fr_6_lb_menu]
        self.countLabelList = [self.fr_1_lb_count,self.fr_2_lb_count,self.fr_3_lb_count,self.fr_4_lb_count,self.fr_5_lb_count,self.fr_6_lb_count]
        self.secLabelList = [self.fr_1_lb_sec,self.fr_2_lb_sec,self.fr_3_lb_sec,self.fr_4_lb_sec,self.fr_5_lb_sec,self.fr_6_lb_sec]
        self.updateFryerReset()
        self.getFryerHistoryCount()
        self.customsignal = CustomSignal() #Mysignal 클래스의 객체 선언
        self.customsignal.signal.connect(self.threadMessage) #객체에 대한시그널 및 슬롯 설정
        print(f'5-1. UI Rendering')

    def cookingBone(self):
        self.cooking('뼈')

    def cookingBoneless(self):
        self.cooking('순살')
        
        

    def cooking(self,menu):
        print(f'6-1. {menu} 메뉴 조리 요청')
        sectionNumber = int(self.getFryerSection())

        if sectionNumber == 0:
            # 0인경우 빈 튀김기가 없다는 알람을 화면에 표시한다. 1~4인 경우 사용가능한 튀김기 번호이다.
            QMessageBox.about(self,'info','빈 튀김기가 없습니다.')
            return
        
        
        # sectionImage='empty.jpg'
        sectionImage = self.cropFryerSection(sectionNumber)

        if self.basketInference(sectionImage) == 1:
            # 이미지를 torchserver에 요청 한 후 바스켓이 비어있는경우 0, 비어있지않는 경우 1을 반환한다.
            QMessageBox.about(self,'error','이미 튀김기가 들어있습니다.')
            return 
        else:
            pass
            QMessageBox.about(self,'info','정상')

        # 튀김기 상태 업데이트 
        self.updateFryerUse(sectionNumber)
        recipe = self.getRecipe()
        self.sendInput(menu,recipe,sectionNumber)
        

        
    




    def getFryerSection(self):
        # db에 사용가능한 fryer 상태를 체크한다
        result = query.getFryerSection()
        print(f'6-2. {result} 튀김기 사용 가능')
        return result
    
    def cropFryerSection(self,sectionNumber):
        # 전체 이미지를 확인 crop 하여 그중에 sectionNumber를 2차 crop 한다
        print(f'6-3. ${sectionNumber} 튀김기 이미지 crop')
        return imageCrop.cropFryerSection(sectionNumber)
    
    def basketInference(self,sectionImage):
        # crop 한 이미지를 torch serve로 전송하여 추론결과를 받아온다
        result = api.apiBasketInference(sectionImage)
        print(f'6-4. ${sectionImage} 검사 결과 = {result}')
        return result
    
    def getRecipe(self):
        print(f'6-5. recipe 가져오기')
        return ['input','wait','output']

    def sendInput(self,menu,recipe,sectionNumber):
        ## 이부분 스레드로 동작해야함
        print(f'6-6. 레시피 스케줄링 스레드로 실행 {recipe}')
        for motion in recipe:
            if motion == 'input': 
                action = 1
                self.menuLabelList[sectionNumber-1].setText(menu)
                self.appendQueue(motion,action,sectionNumber)

        
    def recipeScheduling(self,menu,recipe,sectionNumber):
        ## 이부분 스레드로 동작해야함
        print(f'6-6. 레시피 스케줄링 스레드로 실행 {recipe}')
        for motion in recipe:
            if motion == 'input':
                pass
            elif motion == 'wait':
                self.waitTimer(menu,sectionNumber)
            elif motion == 'output':
                action = 4
                self.appendQueue(motion,action,sectionNumber)

    
    def appendQueue(self,motion,action,sectionNumber):
        # 서비스에 생성한 queue에 레시피를 append 한다
        actionName = f"{action}{sectionNumber}"
        print(f'6-7.  {motion} {actionName}queue 에 추가')

        service.appendQueue(actionName)
        
    
    def waitTimer(self,menu,sectionNumber):
        count =0
        if menu == '뼈':
            count = 30
        else:
            count = 40
            
        print(f'6-7.  {menu} wait {count} ')
        while count > 0 :
            time.sleep(1.0)
            count-=1
            self.secLabelList[sectionNumber-1].setText(str(count))
            
     
    def updateFryerUse(self,section):
        # 튀김기 상태 사용 불 가능으로 변경
        query.updateFryerUse(section)
        
    def updateFryerUnUse(self,section):
        # 튀김기상태 사용가능으로 변경
        query.updateFryerUnUse(section)
    
    def updateFryerReset(self):
        query.updateFryerReset()
    
    def insertFryerHistoryStartTime(self,sectionNumber):
        query.insertFryerHistoryStartTime(sectionNumber)
    
    def updateFryerHistoryEndTime(self,sectionNumber):
        query.updateFryerHistoryEndTime(sectionNumber)
    
    @pyqtSlot(str)    
    def threadMessage(self,text):
        print(text)
        action = int(text[0])
        sectionNumber = int(text[1])
        if action == 1 :
            self.insertFryerHistoryStartTime(sectionNumber)
            menu = self.menuLabelList[sectionNumber-1].text()
            recipe = self.getRecipe()
            thread = Thread(target=self.recipeScheduling, args=(menu,recipe,sectionNumber))
            thread.start()
        if action == 4 :
            self.updateFryerUnUse(sectionNumber)
            self.updateFryerHistoryEndTime(sectionNumber)
            self.menuLabelList[sectionNumber-1].setText('없음')
            self.getFryerHistoryCount()
        
        
        
    def getFryerHistoryCount(self):
        result = query.getFryerHistoryCount()
        for idx , obj in enumerate(result):
            self.countLabelList[idx].setText(str(obj))
        
        

 
class CustomSignal(QObject):
    signal = pyqtSignal(str) #반드시 클래스 변수로 선언할 것

    def run(self,text):
        # text = "emit으로 전달"
        self.signal.emit(text) #customFunc 메서드 실행시 signal의 emit 메서드사용
   
if __name__ == "__main__" :
    # 로봇을 기본 상태로 만든다. 로봇은 기본상태에서 10.0.2.29로 소캣 연결을 요청한다
    service.connectRobot('10.0.2.7')
    
    # 로봇의 연결 요청을 받을 소켓서버를 만든다
    service.openSocketServer('10.0.2.29','5678')
    
    # 로봇과 연결되면 큐를 선언한다.
    service.makingQueue()

    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #MyApp myWindow 생성
    myWindow = MyApp() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    # 큐 사이즈를 체크할 스레드를 생성한다. 큐사이즈가 1이상일경우 맨 처음 큐를 꺼내서 소켓을 통해 로봇에게 보내고 end 메시지를 대기한다.
    thread = service.QueueCheckThread()
    thread.setApp(myWindow)
    thread.start()

    

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    sys.exit(app.exec_())
