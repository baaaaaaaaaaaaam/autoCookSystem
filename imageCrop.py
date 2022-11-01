import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import cv2


class WebCam():
    def __init__(self, device=0, numoffryer=2, newsize=224, roi=[20, 1639, 218, 1015]):
        self.device = device
        self.roi = roi
        self.numoffryer = numoffryer
        self.newsize = newsize

        self.cap = cv2.VideoCapture(device, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def getOriginImage(self):
        if not self.cap.isOpened():
            return None
        else:
            while self.cap.isOpened():
                print(2)
                ret, frame = self.cap.read()
                img = frame.copy()
                self.cap.release()
                return img

    def cropImage(self, img, roi=None, numoffryer=None, newsize=None):
        if roi is None:
            roi = self.roi

        if numoffryer is None:
            numoffryer = self.numoffryer
        
        if newsize is None:
            newsize = self.newsize

        imgs = []

        x_min, x_max, y_min, y_max = roi

        img = img[y_min:y_max, x_min:x_max] # roi crop(bbox)

        h, w, c = img.shape
        
        w = w // numoffryer
            
        for i in range(numoffryer):
            if i == 0:
                fryer = cv2.resize(img[:, :w], (newsize, newsize))
                imgs.append(cv2.resize(fryer[:, :newsize//2], (newsize, newsize)))
                imgs.append(cv2.resize(fryer[:, newsize//2:], (newsize, newsize)))
            else:
                fryer = cv2.resize(img[:, w*i:w*(i+1)], (newsize, newsize))
                imgs.append(cv2.resize(fryer[:, :newsize//2], (newsize, newsize)))
                imgs.append(cv2.resize(fryer[:, newsize//2:], (newsize, newsize)))
        
        return imgs


            

def getImages(sectionNumber):
    cam = WebCam(device=0, numoffryer=2, newsize=224, roi=[20, 1639, 218, 1015])    
    originImage = cam.getOriginImage()
    if originImage is not None:
        images = cam.cropImage(img=originImage)
        return images[sectionNumber]
    else:
        print("Error Can't Get Images From Camera")
        return