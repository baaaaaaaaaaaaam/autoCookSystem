import unittest
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import imageCrop
class SampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        "맨 처음 오직 한번만 실행됨"
        pass

    def test_runs_1(self):
        print('인터넷 연결 상태 확인➪ ', sys._getframe(0).f_code.co_name)

    def test_runs_2(self):
        # print('인터넷 연결 상태 확인➪ ', sys._getframe(0).f_code.co_name)
        result =  imageCrop.getImages(1)
        print(result)


if __name__ == '__main__':
    unittest.main() 