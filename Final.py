import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import time


# Set up camera
width, height = 640, 420
frameR = 100

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Variables
pTime = 0

# Set gesture threshold
gestureThreshold = 300

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Screen Width and Height
wScr, hScr = pyautogui.size()

while True:
    # Read frame from camera
    success, img = cap.read()

    # Detect hand and fingers
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands:
        # Get hand information
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        hand = hands[0]
        lmList = hand['lmList']

        if len(lmList) != 0:
            fingers = detector.fingersUp(hand)

            x1, y1 = lmList[8][0], lmList[8][1]
            x2, y2 = lmList[12][0], lmList[12][1]

            cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)
            if fingers == [0, 1, 0, 0, 0]:
                print("Cursor")
                cv2.putText(img, "Cursor", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                # Move cursor0
                x3 = np.interp(x1, (frameR, width - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, height - frameR), (0, hScr))

                 # Move Mouse
                pyautogui.moveTo(wScr + 10 - x3, y3)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            if fingers == [0, 1, 1, 0, 0]:
                distance, img, info = detector.findDistance((x1, y1), (x2, y2), img)
                if distance < 35:

                    # Mouse Click
                    pyautogui.click()


        # Check hand position and gesture
        if cy <= gestureThreshold:
            if fingers == [1, 0, 0, 0, 0]:
                # Fast Forward
                print("Fast Forward")
                cv2.putText(img, "Fast Forward", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.press('right')
            elif fingers == [0, 0, 0, 0, 1]:
                # Rewind
                print("Rewind")
                cv2.putText(img, "Rewind", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.press('left')
            elif fingers == [1, 1, 1, 1, 1]:
                # Play / Pause
                print("Play / Pause")
                cv2.putText(img, "Play / Pause", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.press('space')
            elif fingers == [0, 1, 1, 1, 0]:
                # Volume Up
                print("Volume Up")
                cv2.putText(img, "Volume Up", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.hotkey('shift', 'up')
            elif fingers == [0, 1, 1, 1, 1]:
                # Volume Down
                print("Volume Down")
                cv2.putText(img, "Volume Down", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.hotkey('shift', 'down')
            elif fingers == [1, 1, 1, 0, 0]:
                print("Scroll Down")
                cv2.putText(img, "Scroll Down", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.scroll(-100)
            elif fingers == [0, 0, 1, 1, 1]:
                print("Scroll Up")
                cv2.putText(img, "Scroll Up", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                pyautogui.scroll(100)

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display annotated image
    cv2.imshow("Image", img)

    # Check for key

    key = cv2.waitKey(10)
    if key == ord('q'):
        # Quit if 'q' is pressed
        break

# Release camera and close window
cap.release()
cv2.destroyAllWindows()
