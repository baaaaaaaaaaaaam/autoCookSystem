import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import cv2


class WebCam():
    def __init__(self, device=0, newsize=224, roi=[60,60+1140,128,128+393]):
        self.device = device
        self.roi = roi
        self.newsize = newsize

        self.cap = cv2.VideoCapture(device, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 860)

    def getOriginImage(self):
        if not self.cap.isOpened():
            print(1)
            return None
        else:
            while self.cap.isOpened():
                print(2)
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


            

def getImages(sectionNumber):
    cam = WebCam(device=1,  newsize=224, roi=[60,60+1140,128,128+393])    
    originImage = cam.getOriginImage()
    # cv2.imwrite(f'originImage.jpg',originImage)
    if originImage is not None:
        images = cam.cropImage(img=originImage)
        # for i,k in enumerate(images):
            # cv2.imwrite(f'test{i}.jpg',k)
        return images[sectionNumber]
    else:
        print("Error Can't Get Images From Camera")
        return
    


getImages(1)




import cv2


# img = cv2.imread('./img/fryer_2.jpg')
# x_pos,y_pos,width,height=cv2.selectROI('location',img,False)
# print(f'x_pos = {x_pos}, y_pos = {y_pos}')
# print(f'width = {width}, height = {height}')
# cv2.destroyAllWindows()

# 전체 튀김기 67,128,1140,393
# 1번 튀김기 26,22,512,361
# 2번 튀김기 610,24,525,360

newsize = 224
img = cv2.imread('./img/originImage_1.jpg')
x_min, x_max, y_min, y_max = 60,60+1140,128,128+393
img = img[y_min:y_max, x_min:x_max]
# # cv2.imwrite(f'./img/fryer.jpg',img)
# h, w, c = img.shape


fryer_1 = cv2.resize(img[22:22+361, 26:26+512], (newsize, newsize))
fryer_2 = cv2.resize(img[24:24+360, 610:610+525], (newsize, newsize))
# # cv2.imwrite(f'./img/fryer_1.jpg',fryer_1)
# # cv2.imwrite(f'./img/fryer_2.jpg',fryer_2)

imgs = []
imgs.append(cv2.resize(fryer_1[:, :76], (newsize, newsize)))
imgs.append(cv2.resize(fryer_1[:, 69:69+82], (newsize, newsize)))
imgs.append(cv2.resize(fryer_1[:, 148:], (newsize, newsize)))
imgs.append(cv2.resize(fryer_2[:, :76], (newsize, newsize)))
imgs.append(cv2.resize(fryer_2[:, 69:69+82], (newsize, newsize)))
imgs.append(cv2.resize(fryer_2[:, 148:], (newsize, newsize)))

for i ,k in enumerate(imgs):
    cv2.imwrite(f'./img/section_{i}.jpg',k)