
import time


def init(cobot):
    result=False           
    count=30
    if cobot.IsDataSockConnect():
        cobot.SetBaseSpeed(1.0)
        time.sleep(1.0)
        result=True             # default 는 true : count 30  안에 정상 break걸림 
        while True:
            if count <= 0:
                break

            time.sleep(1.0)
            if cobot.GetCurTaskState() == cobot.TASKSTATE.RUN: # test code
                result = taskstateRun(cobot,count)
                break

            if not cobot.IsInitialized():
                count,result = cobotNotInit(cobot,count)
                    
            if not cobot.IsRobotReal():
               count,result = cobotNotReal(cobot,count)
               
                    
            if cobot.GetCurrentCobotStatus() == cobot.COBOT_STATUS.PAUSED:
                result = cobotstatusPause(cobot,count)
                break

            if cobot.GetCurCollisionState()[0] == 1 or cobot.GetCurCollisionState()[1] == 1 :
                count,result = collisionResume(cobot,count)

            if cobot.GetCurTaskState() == cobot.TASKSTATE.IDLE:
                result = taskstateIdle(cobot,count)
                break    

            elif cobot.GetCurTaskState() == cobot.TASKSTATE.PAUSED :
                taskstatePause(cobot,count)
                break
    
    return result



def taskstateRun(cobot,count):
    while True :
        count,result = checkCount(count)
        if result == False:
            print(f'2-3. taskstateRun() : 30번 이내에 RUN 못함 (2)  ','error')
            break
        cobot.TaskStop() 
        time.sleep(1.0)
        cobot.TaskPlay() 
        time.sleep(1.0)
        if cobot.GetCurTaskState() == cobot.TASKSTATE.RUN:
            print(f'2-3. taskstateRun() :  GetCurTaskState = RUN (2)  ','warning')
            break
    return result

def cobotNotInit(cobot,count):
    count,result = checkCount(count)
    cobot.CobotInit()                                                     
    if cobot.IsInitialized():
        print(f'2-3. cobotNotInit() :  IsInitialized() = True (3)   ','warning')
    return count,result

def cobotNotReal(cobot,count):
    while True:
        count,result = checkCount(count)
        if result == False:
            print(f'2-3. cobotNotReal() :  30번 이내에 IsRobotReal 못함 (4) ','error')
            break
        cobot.SetProgramMode(cobot.PG_MODE.REAL)
        if cobot.IsRobotReal():
            print(f'2-3. cobotNotReal() : 30번 이내에 IsRobotReal = True (4) >> 성공 ','warning')
            break
    return count,result

def cobotstatusPause(cobot,count):
    while True :
        count,result = checkCount(count)
        if result == False:
            print(f'2-3. cobotstatusPause() : 30번 이내에 GetCurTaskState 못함 (5) ','error')
            break
        cobot.MotionResume()
        time.sleep(1.0)
        if cobot.GetCurTaskState() == cobot.TASKSTATE.RUN:
            print(f'2-3. cobotstatusPause() : 30번 이내에 GetCurTaskState = RUN (5) ','warning')
            break
    return result


def collisionResume(cobot,count):
    print(f'2-3. collisionResume() : 충돌시 재실행 요청  (6) ','warning')

    count,result = checkCount(count)
    cobot.CollisionResume()
    if cobot.GetCurCollisionState()[0] == 0 and cobot.GetCurCollisionState()[1] == 0:
        print(f'2-3. collisionResume() : 충돌시 재실행 됨(6) ','warning')
    return count,result


def taskstateIdle(cobot,count):
    while True :
        count,result = checkCount(count)
        if result == False:
            print(f'2-3. taskstateIdle() : 30번 이내에 RUN 못함 (7) ','error')
            break
        
        time.sleep(1.0)
        cobot.TaskPlay()
        time.sleep(1.0)
        if cobot.GetCurTaskState() == cobot.TASKSTATE.RUN:
            print(f'2-3. taskstateIdle() : 30번 이내에 GetCurTaskState = RUN (7) ','warning')
            break
    return result


def taskstatePause(cobot,count):
    while True :
        count,result = checkCount(count)
        if result == False:
            print(f'2-3. taskstatePause() : 30번 이내에 RUN 못함 (8)  ','error')
            break
        cobot.MotionResume()
        time.sleep(1.0)
        if cobot.GetCurTaskState() == cobot.TASKSTATE.RUN:
            print(f'2-3. taskstatePause() : 30번 이내에 GetCurTaskState = RUN (8) ','warning')
            break
    return result
       



def checkCount(count):
    count -= 1
    if count <=0:
        return count,False
    else:
        return count,True
