import cv2
from gaze_tracking import GazeTracking
import pyautogui as pag

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)
    
    new_frame = gaze.annotated_frame()
    new_frame = cv2.flip(frame, 1)
        
    left = gaze.pupil_left_coords()
    right = gaze.pupil_right_coords()
    
    if left is not None and right is not None:
        pag.moveTo(int((left[0] + right[0])/2), int((left[1] + right[1])/2))
        print(int((left[0] + right[0])/2), int((left[1] + right[1])/2))
        
    cv2.imshow("Demo", new_frame)

    if cv2.waitKey(1) == 27:
        break