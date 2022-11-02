import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import cv2
import datetime


class WebCam():
    def __init__(self, device=0,   newsize=224, roi=[60,60+1140,128,128+393]):
        self.device = device
        self.roi = roi
        self.newsize = newsize

        self.cap = cv2.VideoCapture(device, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 860)

    def getOriginImage(self):
        if not self.cap.isOpened():
            return None
        else:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                img = frame.copy()
                self.cap.release()
                return img

    def cropImage(self, img, roi=None,   newsize=None):
        if roi is None:
            roi = self.roi

        if newsize is None:
            newsize = self.newsize

        imgs = []

        x_min, x_max, y_min, y_max = roi

        img = img[y_min:y_max, x_min:x_max] # roi crop(bbox)

        fryer_1 = cv2.resize(img[22:22+361, 26:26+512], (newsize, newsize))
        fryer_2 = cv2.resize(img[24:24+360, 610:610+525], (newsize, newsize))
        imgs.append(cv2.resize(fryer_1[:, :76], (newsize, newsize)))
        imgs.append(cv2.resize(fryer_1[:, 69:69+82], (newsize, newsize)))
        imgs.append(cv2.resize(fryer_1[:, 148:], (newsize, newsize)))
        imgs.append(cv2.resize(fryer_2[:, :76], (newsize, newsize)))
        imgs.append(cv2.resize(fryer_2[:, 69:69+82], (newsize, newsize)))
        imgs.append(cv2.resize(fryer_2[:, 148:], (newsize, newsize)))

        
        return imgs


            

def cropFryerSection(sectionNumber):
    cam = WebCam(device=1,  newsize=224, roi=[60,60+1140,128,128+393])    
    sectionNumber += sectionNumber
    originImage = cam.getOriginImage()
    if originImage is not None:
        images = cam.cropImage(img=originImage)
        cv2.imwrite(f'./img/{datetime.datetime.now()}.jpg',images[sectionNumber])
        return images[sectionNumber]
    else:
        print("Error Can't Get Images From Camera")
        return