import cv2
import numpy as np
import math
import mediapipe as mp
from src.settings import *
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def euclidean_distance(point1, point2):
    x1, y1 = point1.ravel()
    x2, y2 = point2.ravel() 
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

    return distance
    
def iris_position(iris_center, right_point, left_point, r_std, l_std):
    center_to_right_d = euclidean_distance(iris_center, right_point)
    total_d = euclidean_distance(right_point, left_point)
    ratio = center_to_right_d / total_d

    iris_position = ""
    if ratio < r_std:
        iris_position = "right"
    elif ratio > l_std:
        iris_position = "left"
    else:
        iris_position = "center"

    return iris_position, ratio

def is_down(iris_center, top_point, bottom_point, d_std):
    center_to_bottom_dist = euclidean_distance(iris_center, bottom_point)
    total_distance = euclidean_distance(top_point, bottom_point)
    ratio = center_to_bottom_dist / total_distance

    iris_position = ""
    if ratio > d_std and ratio < 0.9:
        iris_position = "down"
    elif ratio >= 0.9:
        iris_position = "blink"
    else:
        iris_position = "center"

    return iris_position, ratio


RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]
LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246]
LEFT_IRIS = [469, 470, 471, 472]
RIGHT_IRIS = [474, 475, 476, 477]
L_H_LEFT = [33]  # right eye right most landmark
L_H_RIGHT = [133]  # right eye left most landmark
R_H_LEFT = [362]  # left eye right most landmark
R_H_RIGHT = [263]  # left eye left most landmark
R_V_TOP = [386]
R_V_BOTTOM = [374]
L_V_TOP = [159]
L_V_BOTTOM = [145]

def eyetracking(frame):
    #getting width and height or frame
    img_h, img_w = frame.shape[:2]
    
    # mediapipe iris Position Estimation
    with mp_face_mesh.FaceMesh(
        refine_landmarks = True,
        min_detection_confidence = 0.6,
        min_tracking_confidence = 0.6
    ) as face_mesh:
        i_results = face_mesh.process(frame)
        if i_results.multi_face_landmarks:
            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in i_results.multi_face_landmarks[0].landmark])
        
            (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            # turn center points into np array 
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            
            #cv2.circle(frame, center_left, int(l_radius), (255,0,255), 1, cv2.LINE_AA) # 왼쪽 눈동자
            #cv2.circle(frame, center_right, int(r_radius), (255,0,255), 1, cv2.LINE_AA) # 오른쪽 눈동자

            # 오른쪽 눈
            cv2.circle(frame, center_right, 2, (255, 255, 255), -1, cv2.LINE_AA) # 오른쪽 눈 중심
            cv2.circle(frame, mesh_points[R_H_RIGHT][0], 2, (255, 255, 255), -1, cv2.LINE_AA) # 오른쪽 눈 오른쪽 끝
            cv2.circle(frame, mesh_points[R_H_LEFT][0], 2, (0, 255, 255), -1, cv2.LINE_AA) # 오른쪽 눈 왼쪽 끝

            hr_iris_pos, ratio = iris_position(center_right, mesh_points[R_H_RIGHT][0], mesh_points[R_H_LEFT][0], settings.r_std, settings.l_std)
            cv2.putText(frame, f"horizontal(right eye): {hr_iris_pos} {ratio: .2f}", (30, 30), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)
            vr_iris_pos, ratio = is_down(center_right, mesh_points[R_V_TOP][0], mesh_points[R_V_BOTTOM][0], settings.d_std)
            cv2.putText(frame, f"vertical(right eye): {vr_iris_pos} {ratio: .2f}", (30, 60), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)
            
            # 왼쪽 눈
            #cv2.circle(frame, center_left, 2, (255, 255, 255), -1, cv2.LINE_AA) # 오른쪽 눈 중심
            #cv2.circle(frame, mesh_points[L_H_RIGHT][0], 2, (255, 255, 255), -1, cv2.LINE_AA) # 왼쪽 눈 오른쪽 끝
            #cv2.circle(frame, mesh_points[L_H_LEFT][0], 2, (0, 255, 255), -1, cv2.LINE_AA) # 왼쪽 눈 왼쪽 끝

            #hl_iris_pos, ratio = iris_position(center_left, mesh_points[L_H_RIGHT][0], mesh_points[L_H_LEFT][0])
            #cv2.putText(frame, f"horizontal(left eye): {hl_iris_pos} {ratio: .2f}", (30, 90), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)
            #vl_iris_pos, ratio = is_down(center_left, mesh_points[L_V_TOP][0], mesh_points[L_V_BOTTOM][0])
            #cv2.putText(frame, f"vertical(left eye): {vl_iris_pos} {ratio: .2f}", (30, 120), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)

            #print(f"r_std: {settings.r_std: .2f} l_std: {settings.l_std: .2f} d_std: {settings.d_std: .2f}")

            return hr_iris_pos, vr_iris_pos

def facedetection(frame):
    with mp_face_detection.FaceDetection( #얼굴인식
        model_selection = 0,
        min_detection_confidence = 0.5
        ) as face_detection:
            
            d_results = face_detection.process(frame)
            
            print(type(d_results.detections))

            # 자리 비움 감지
            if d_results.detections: # 사람 있음
                #for detection in d_results.detections: # 주석 그리기
                    #mp_drawing.draw_detection(frame, detection)
                if len(d_results.detections) >= 2: # 사람 2명 이상
                    return 2    
            else: # 사람 없음
                return 0

def calibration(frame):
    #getting width and height or frame
    img_h, img_w = frame.shape[:2]

    # mediapipe iris Position Estimation
    with mp_face_mesh.FaceMesh(
        refine_landmarks = True,
        min_detection_confidence = 0.6,
        min_tracking_confidence = 0.6
    ) as face_mesh:
        i_results = face_mesh.process(frame)
        if i_results.multi_face_landmarks:
            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in i_results.multi_face_landmarks[0].landmark])
        
            (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            # turn center points into np array 
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            
            
            hr_iris_pos, h_ratio = iris_position(center_right, mesh_points[R_H_RIGHT][0], mesh_points[R_H_LEFT][0], settings.r_std, settings.l_std)
            cv2.putText(frame, f"horizontal(right eye): {hr_iris_pos} {h_ratio: .2f}", (30, 30), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)
            
            vr_iris_pos, v_ratio = is_down(center_right, mesh_points[R_V_TOP][0], mesh_points[R_V_BOTTOM][0], settings.d_std)
            cv2.putText(frame, f"vertical(right eye): {vr_iris_pos} {v_ratio: .2f}", (30, 60), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 1, cv2.LINE_AA)

            return h_ratio, v_ratio