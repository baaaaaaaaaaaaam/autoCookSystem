import cobot_rb
import cobotInit
import socket
import time
import queue
from PyQt5.QtCore import *


def connectRobot(robotIP):
    print(f'1. 로봇 초기 init')
    cobot = cobot_rb
    cobot.ConnectToCB(robotIP)
    cobotInit.init(cobot)



def openSocketServer(socketIp,socketPort):
    print(f'2-1. 소켓 서버 오픈')
    try:
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServer.bind((socketIp, int(socketPort))) 
        socketServer.listen(1) 
        global conn
        conn, addr = socketServer.accept()
        socketServer.close()
        print(f'2-2. 소켓 연결')
    except:
        print('2-3 소켓 연결 에러 발생')

def makingQueue():
    global q
    print(f'3. Queue 생성')
    q = queue.Queue()

def appendQueue(recipe):
    q.put(recipe)
    
    
class QueueCheckThread(QThread):
    def setApp(self,app):
        self.myWindow =app
    
    def run(self):
        print(f'4-1. QueueCheckThread 생성')
        while(True):
            time.sleep(1.0)
            print(f'4-2. queue 사이즈 : {q.qsize()}')
            if q.qsize() > 0:
                actionNumber  = q.get()
                print(f'4-3. actionNumber : {actionNumber}')
                conn.send(bytes(actionNumber, encoding = "utf-8"))
                data = conn.recv(1024)
                if data == b"end":
                    print(f'4-4. 로봇으로부터 받은 메시지 : {data}')
                    self.myWindow.customsignal.run(actionNumber)
                elif data == b"output":
                    print(f'4-4. 로봇으로부터 받은 메시지 : {data}')
                    data = conn.recv(1024)
                    print(f'4-4. 로봇으로부터 받은 메시지 : {data}')
                    self.myWindow.customsignal.run(actionNumber)


