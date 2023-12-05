import cv2
import mediapipe as mp
import numpy as np
import dlib

class Coordinate:

    def __init__(self, screen_w, screen_h):
        
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

    def midpoint(self, ps):
        x = 0
        y = 0

        for p in ps:
            x += p.x
            y += p.y
    
        return (int(x / len(ps)), int(y / len(ps)))

    def compute_center(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        for face in faces:

            landmarks = self.predictor(gray, face)
            left_point = (landmarks.part(36).x, landmarks.part(36).y)
            right_point = (landmarks.part(39).x, landmarks.part(39).y)

            left_eye = [36, 37, 38, 39, 40, 41]
            left_point = [landmarks.part(i) for i in left_eye]
            center_left = self.midpoint(left_point)

            right_eye = [42, 43, 44, 45, 46, 47]
            right_point = [landmarks.part(i) for i in right_eye]
            center_right = self.midpoint(right_point)

            return center_left, center_right
        return(0, 0), (0, 0)
    
    def center(self, points):
        x = 0
        y = 0
        for p in points:
            x += p[0]
            y += p[1]
        return (x / len(points), y / len(points))
        
    def scale_point_to_frame(self, points, w, h):
        ps = []
        for p in points:
            x = int(p[0]*w)
            y = int(p[1]*h)
            ps.append((x, y))
        return ps

    def scale_point_to_screen(self, points, w_screen, h_screen, w_frame, h_frame):
        dx = int((w_screen - w_frame) / 2)
        dy = int((h_screen - h_frame) / 2)

        ps = []
        for p in points:
            x = p[0] + dx
            y = p[1] + dy
            ps.append((x, y))
        return ps

    def cal_coe(self, p1, p2):
        a = p1[0]
        b = p1[1]
        c = p2[0]
        d = p2[1]

        return (b - d, c - a, a * (b - d) + b * (c - a))

    def intersection_point(self, coe1, coe2, center1, center2):
        a1, b1, c1 = coe1
        a2, b2, c2 = coe2

        if (a2*b1-a1*b2) == 0:
            x, y = self.center([center1, center2])
            return (int(x), int(y))
        
        y = int((a2*c1 - a1*c2)/(a2*b1-a1*b2))
        x = int((b1*c2 - b2*c1)/(a2*b1-a1*b2))

        return (x, y)
        
    def detect_condinate(self, frame):
        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = self.face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame = cv2.resize(frame, None, fx=5, fy=5)
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark

            right_eye = [385, 387, 373, 380, 473]
            left_eye = [160, 158, 153, 144, 468]

            right_points = [(landmarks[id].x, landmarks[id].y) for id in right_eye]
            left_points = [(landmarks[id].x, landmarks[id].y) for id in left_eye]
            # center_right = self.center(right_points[: -1])
            # center_left = self.center(left_points[: -1])

            # right_points.append(center_right)
            # left_points.append(center_left)

            pupil_right = self.scale_point_to_frame([right_points[-1]], frame_w, frame_h)
            pupil_left = self.scale_point_to_frame([left_points[-1]], frame_w, frame_h)
            pupil_right = self.scale_point_to_screen(pupil_right, self.screen_w, self.screen_h, frame_w, frame_h)[0]
            pupil_left = self.scale_point_to_screen(pupil_left, self.screen_w, self.screen_h, frame_w, frame_h)[0]
            
            center_left, center_right = self.compute_center(frame)
            center_right = self.scale_point_to_screen([center_right], self.screen_w, self.screen_h, frame_w, frame_h)[0]
            center_left = self.scale_point_to_screen([center_left], self.screen_w, self.screen_h, frame_w, frame_h)[0]

            coe_right = self.cal_coe(center_right, pupil_right)
            coe_left = self.cal_coe(center_left, pupil_left)

            x, y = self.intersection_point(coe_right, coe_left, center_left, center_right)
            return (x, y)
        else:
            return (1, 0)


        
# def compute_center(frane):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = detector(gray)
#     for face in faces:

#         landmarks = predictor(gray, face)
#         left_point = (landmarks.part(36).x, landmarks.part(36).y)
#         right_point = (landmarks.part(39).x, landmarks.part(39).y)

#         left_eye = [36, 37, 38, 39, 40, 41]
#         left_point = [landmarks.part(i) for i in left_eye]
#         center_left = midpoint(left_point)

#         right_eye = [42, 43, 44, 45, 46, 47]
#         right_point = [landmarks.part(i) for i in right_eye]
#         center_right = midpoint(right_point)

#         return center_left, center_right
#     return(0, 0), (0, 0)

# while True:
#     _, frame = cap.read()
#     frame = cv2.flip(frame, 1)
#     center_left, center_right = compute_center(frame)

#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = face_mesh.process(rgb_frame)
#     landmark_points = output.multi_face_landmarks
#     # frame = cv2.resize(frame, None, fx=5, fy=5)
#     frame_h, frame_w, _ = frame.shape
#     if landmark_points:
#         landmarks = landmark_points[0].landmark

#         right_eye = [473]
#         left_eye = [468]

#         for r in right_eye:
#             x = int(landmarks[r].x * frame_w)
#             y = int(landmarks[r].y * frame_h)
#             cv2.circle(frame, (x, y), 2, (255, 0, 0), 2)
        
#         for r in left_eye:
#             x = int(landmarks[r].x * frame_w)
#             y = int(landmarks[r].y * frame_h)
#             cv2.circle(frame, (x, y), 2, (255, 0, 0), 2)

        
#         cv2.circle(frame, center_left, 2, (0, 255, 0), 2)
#         cv2.circle(frame, center_right, 2, (0, 255, 0), 2)


#     cv2.imshow('Eye Controlled Mouse', frame)

#     if cv2.waitKey(1) == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()