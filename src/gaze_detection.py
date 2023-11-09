import cv2
import dlib
import numpy as np

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

print("predictor: ", predictor)

def count_black_point(image, landmark_point):
    min_x = np.min(landmark_point[:, 0])
    max_x = np.max(landmark_point[:, 0])
    min_y = np.min(landmark_point[:, 1])
    max_y = np.max(landmark_point[:, 1])
    
    gray_eye = image[min_y: max_y, min_x: max_x]

    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)

    threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
    
    _, w, _ = threshold_eye.shape
    threshold_left_eye = threshold_eye[:, : int(w /2)]
    threshold_right_eye = threshold_eye[:, int(w/2) :]

    return threshold_left_eye.sum(), threshold_right_eye.sum()

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    value = 42 #whatever value you want to add
    hsv[:,:,2] += value
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:

        landmarks = predictor(gray, face)
        landmark_point_left = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                            (landmarks.part(37).x, landmarks.part(37).y),
                            (landmarks.part(38).x, landmarks.part(38).y),
                            (landmarks.part(39).x, landmarks.part(39).y),
                            (landmarks.part(40).x, landmarks.part(40).y),
                            (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
        
        landmark_point_right = np.array([(landmarks.part(42).x, landmarks.part(42).y),
                            (landmarks.part(43).x, landmarks.part(43).y),
                            (landmarks.part(44).x, landmarks.part(44).y),
                            (landmarks.part(45).x, landmarks.part(45).y),
                            (landmarks.part(46).x, landmarks.part(46).y),
                            (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

        threshold_left_eye_left, threshold_right_eye_left = count_black_point(image, landmark_point_left)
        threshold_left_eye_right, threshold_right_eye_right = count_black_point(image, landmark_point_right)

        if (threshold_left_eye_left + threshold_left_eye_right) > (threshold_right_eye_left + threshold_right_eye_right):
            print("left")
        elif (threshold_left_eye_left + threshold_left_eye_right) < (threshold_right_eye_left + threshold_right_eye_right):
            print("right")
        else:
            print("Center")

        # cv2.imshow("Threshold", threshold_eye)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows() 