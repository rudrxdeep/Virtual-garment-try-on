import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector


cap = cv2.VideoCapture("Resources/videos/1.mp4")
detector = PoseDetector()

shirtFolderPath ="Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
#print(listShirts)
fixedRatio = 262/190 #width of shirt/width of points 11 and 12
shirtRatioHeightWidth = 581/440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight=0
counterLeft=0
selectionSpeed=13

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    #img=cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        #center=bboxInfo["center"]
        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        imgShirt= cv2.imread(os.path.join(shirtFolderPath,listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)


        widthOfShirt = (lm11[0]-lm12[0])*fixedRatio
        print(widthOfShirt)
        imgShirt = cv2.resize(imgShirt, (int(widthOfShirt), int(widthOfShirt*shirtRatioHeightWidth)))
        currentScale =(lm11[0]-lm12[0])/190
        offset = int(44*currentScale),int(48*currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt,(lm12[0]-offset[0], lm12[1]-offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074,293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72,293))


        if lmList[16][1]<300:
            counterLeft+=1
            cv2.ellipse(img,(139,360),(66,66),0,0,
                        counterLeft*selectionSpeed, (0,255,0),20)
            if counterLeft * selectionSpeed >360:
                counterLeft=0
                if imageNumber< len(listShirts)-1:
                    imageNumber+=1
        elif lmList[15][1]>900:
            counterRight+=1
            cv2.ellipse(img,(1138,360),(66,66),0,0,
                        counterRight*selectionSpeed, (0,255,0),20)
            if counterRight * selectionSpeed >360:
                counterRight=0
                if imageNumber>0:
                    imageNumber-=1

        else:
            counterRight=0
            counterLeft=0


    cv2.imshow("Image",img)
    cv2.waitKey(1)