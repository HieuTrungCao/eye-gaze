"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
from screeninfo import get_monitors

def getMonitors():
    return get_monitors()[0]

gaze = GazeTracking('model/shape_predictor_68_face_landmarks.dat')
webcam = cv2.VideoCapture(0)
cv2.namedWindow("Demo", cv2.WINDOW_AUTOSIZE)
(wdX, wdY, wdW, wdH) = cv2.getWindowImageRect("Demo")
monitor = getMonitors()
x, y = 0, 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    # if text != "":    
    #     print(text)
    if gaze.is_up():
        text = "Looking up"
    elif gaze.is_down():
        text = "Looking donw"
    elif gaze.is_center():
        text = "Looking center"
    # if text != "":
    #     print(text)
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)


    if gaze.horizontal_ratio() != None:
        x = gaze.horizontal_ratio()
        print("hRatio:" + str(x))
        if x > 1: x = 1
    if gaze.vertical_ratio() != None:
        y = gaze.vertical_ratio()
        print("vRatio:" + str(y))
        if y > 1: y = 1
    gazeX = monitor.width * x
    gazeY = monitor.height * y
    # print("GazeX: " + str(gazeX))
    # print("GazeY: " + str(gazeY))
    cv2.putText(frame, "gazeX:  " + str(gazeX), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "gazeY: " + str(gazeY), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    cv2.moveWindow("Demo", (int)((monitor.width - wdW)/2), (int)((monitor.height - wdH)/2))
    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()