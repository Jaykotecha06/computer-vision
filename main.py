import os
from cvzone.HandTrackingModule import HandDetector

import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/Background.png")
# importing all the modes images in the list
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)  # here only name of the images not of the actual images
listImgModes = []  # here actual images not a path...
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModePath)))
print(listImgModes)

# importing all the icons in the list
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathModes)  # here only name of the images not of the actual images
listImgIcons = []  # here actual images not a path...
for imgIconsPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons,imgIconsPath)))


modeType = 0 # changing the selection mode
selection = -1  # here i am not choose 0 bcs 0 is also selector
counter = 0
selectionSpeed = 7
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1,-1,-1]

while True:
    success,img = cap.read()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    # Place the captured frame onto imgBackground at position (139, 50)
    imgBackground[139:139+480,50:50+640] = img
    # Place the first mode image from listImgModes onto imgBackground at position (0, 847)
    imgBackground[0:720,847:1280] = listImgModes[modeType]

    if hands and counterPause == 0 and modeType < 3:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)
        if fingers1 == [0,1,0,0,0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        # elif fingers1 == [0, 1, 1, 1, 1]:
        #     if selection != 4:
        #         counter = 1
        #     selection = 4

        else:
            selection = -1
            counter = 0
        if counter > 0:
            counter += 1
            print(counter)
            cv2.ellipse(imgBackground,modePositions[selection - 1],(103, 103), 0, 0, counter * selectionSpeed, (0, 255, 0), 20)
            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

    # To pause after each selection is made
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:  # it means 2second
           counterPause = 0

    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]
        # Displaying
        # cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)




