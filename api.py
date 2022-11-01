import requests
import urllib3
urllib3.disable_warnings()

def apiBasketInference(sectionImage):
    resp = requests.post(
    url='http://localhost:3800/predictions/basketclassifier',
    data=open(sectionImage, 'rb'),
    verify=False
    )
    answer = resp.json()
    if answer['result'] == '0':
        print('바스켓 검출 안됨, 사용 가능')
    else:
        print('바스켓 검출 됨, 사용 불가능')
    print(answer)
    return answer
