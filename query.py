import pymysql


def getFryerSection():
    """
        사용 가능한 튀김기 조회
    Returns:
        튀김기 세션 넘버
    """
    sql = "SELECT section FROM fryer_condition WHERE fryer_status = 'N' ORDER BY section ASC LIMIT 0,1;"
    result = queryToDB(sql)
    if len(result) == 0:
        return 0
    return  result[0][0]

def updateFryerUse(section):
    """
        바스켓을 넣으려는 튀김기를 N->Y  상태변경
    Args:
        section : 튀김기번호
    Returns:
        없음
    """
    sql = f" update fryer_condition set fryer_status = 'Y' where section = '{section}';"
    result = queryToDB(sql)
    return  result

def updateFryerUnUse(section):
    """
        바스켓을 넣으려는 튀김기를 Y->N  상태변경
    Args:
        section : 튀김기번호
    Returns:
        없음
    """
    sql = f" update fryer_condition set fryer_status = 'N' where section = '{section}';"
    result = queryToDB(sql)
    return  result

def updateFryerReset():
    """
        모든 튀김기 상태를 N으로 만든다
    Args:
        section : 튀김기번호
    Returns:
        없음
    """
    sql = f" update fryer_condition set fryer_status = 'N';"
    result = queryToDB(sql)
    return  result


def insertFryerHistoryStartTime(section):
    """
        튀김기 세션 사용 히스토리 관리
    Args:
        section : 튀김기번호
    Returns:
        없음
    """
    sql = f"insert into fryer_history (section,start_time) values ({section},now());"
    queryToDB(sql)

def updateFryerHistoryEndTime(section):
    """
        튀김기 세션 사용 히스토리 관리
    Args:
        section : 튀김기번호
    Returns:
        없음
    """
    sql = f"update fryer_history set end_time = now() where section = {section};"
    queryToDB(sql)

def getFryerHistoryCount():
    """
        튀김기 세션 사용 히스토리 카운팅
    Args:
        section : 튀김기번호
    Returns:
        없음
    """    
    sql = f'SELECT COUNT(b.section) AS COUNT,a.section FROM fryer_condition a LEFT JOIN fryer_history b ON a.section = b.section GROUP BY b.section ORDER BY section ASC;'
    result = queryToDB(sql)
    return result[0]

def queryToDB(sql):
    con = pymysql.connect(host='localhost', user='root', password='test', db='test', charset='utf8') 
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    rows = cur.fetchall()
    con.close()
    return rows