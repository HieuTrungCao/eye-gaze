import cv2
import mediapipe as mp
import pyautogui as pag
from gaze_tracking import GazeTracking

gaze = GazeTracking()

cv2.namedWindow('Eye Controlled Mouse', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Eye Controlled Mouse', 1080, 720)

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh()
screen_w, screen_h = pag.size()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    
    left = gaze.pupil_left_coords()
    right = gaze.pupil_right_coords()
    print(left, right)
    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # output = face_mesh.process(rgb_frame)
    # landmark_points = output.multi_face_landmarks
    # frame_h, frame_w, _ = frame.shape
    # results = face_mesh.process(rgb_frame)
    
    # if landmark_points:
    #     landmarks = landmark_points[0].landmark
        # for id, landmark in enumerate(landmarks[474:478]):
        #     x = int(landmark.x * frame_w)
        #     y = int(landmark.y * frame_h)
        #     cv2.circle(frame, (x, y), 3, (0, 255, 0))
            
        #     screen_x = screen_w * landmark.x
        #     screen_y = screen_h * landmark.y
        #     pyautogui.moveTo(screen_x, screen_y)
            
        # left = [landmarks[145], landmarks[159]]
        # right = [landmarks[374], landmarks[386]]

        # for landmark in right:
        #     x = int(landmark.x * frame_w)
        #     y = int(landmark.y * frame_h)
        #     cv2.circle(frame, (x, y), 3, (0, 255, 255))
        
        # for landmark in left:
        #     x = int(landmark.x * frame_w)
        #     y = int(landmark.y * frame_h)
        #     cv2.circle(frame, (x, y), 3, (0, 255, 255))

        # cv2.circle(frame, (int((left[0].x+left[1].x+right[0].x+right[1].x)* frame_w/4), int((left[0].y+left[1].y+right[0].y+right[1].y) * frame_h/4)), 3, (0, 255, 255))
        
        # pag.moveTo(int((left[0].x+left[1].x+right[0].x+right[1].x)* frame_w/4), int((left[0].y+left[1].y+right[0].y+right[1].y) * frame_h/4))
        
        # if (left[0].y - left[1].y) < 0.004:
        #     pyautogui.click()
        #     pyautogui.sleep(1)
            
    cv2.imshow('Eye Controlled Mouse', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break