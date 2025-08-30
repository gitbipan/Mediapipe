import serial as ser
import cv2
import mediapipe as mp

webcam=cv2.VideoCapture(0)
mp_face=mp.solutions.face_mesh
mp_drawing=mp.solutions.drawing_utils
arduino=ser.Serial('com8',9600)
# necessary modules and variable
    