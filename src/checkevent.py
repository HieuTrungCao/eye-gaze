import cv2
import numpy as np

def getMousPos(event , x, y, flags, param):
    global clickedX, clickedY
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        print(x,y)
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
    #     print(x,y)
        mouseX, mouseY = x, y