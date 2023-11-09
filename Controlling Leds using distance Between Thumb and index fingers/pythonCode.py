# Importing Libraries 
import cv2 
import mediapipe as mp 
from math import hypot 
import serial 
import numpy as np 
previous = ""

com_port = 'COM3'  
baud_rate = 115200 



  
mpHands = mp.solutions.hands 
hands = mpHands.Hands( 
	static_image_mode=False, 
	model_complexity=1, 
	min_detection_confidence=0.75, 
	min_tracking_confidence=0.75, 
	max_num_hands=2) 

Draw = mp.solutions.drawing_utils 

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('http://192.168.1.11:4747/video')
# cap = cv2.VideoCapture('http://100.71.43.213:8080/video') 

while True: 
	
	_, frame = cap.read() 
	frame = cv2.flip(frame, 1) 
	frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
	Process = hands.process(frameRGB) 

	landmarkList = [] 
	if Process.multi_hand_landmarks: 
		for handlm in Process.multi_hand_landmarks: 
			for _id, landmarks in enumerate(handlm.landmark):  
				height, width, color_channels = frame.shape 
 
				x, y = int(landmarks.x*width), int(landmarks.y*height) 
				landmarkList.append([_id, x, y]) 

			Draw.draw_landmarks(frame, handlm, 
								mpHands.HAND_CONNECTIONS) 


	if landmarkList != []: 
		x_1, y_1 = landmarkList[4][1], landmarkList[4][2] 
		x_2, y_2 = landmarkList[8][1], landmarkList[8][2] 
		cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED) 
		cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED) 
		L = hypot(x_2-x_1, y_2-y_1) 
		b_level = np.interp(L, [15, 220], [0, 100]) 
		if(int(b_level) <= 30):
			cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 0, 255), 3)
		elif((int(b_level) > 30) and (int(b_level) <= 60)):
			cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)
		else:
			cv2.line(frame, (x_1, y_1), (x_2, y_2), (255, 0, 0), 3)
		if(int(b_level) <= 30):
			if(previous != "LED 1 ON"):
				print("LED 1 ON")
				ser = serial.Serial(com_port, baud_rate)
				ser.write("LED 1 ON".encode())
				ser.close()
				previous = "LED 1 ON"
		elif((int(b_level) > 30) and (int(b_level) <= 60)):
			if(previous != "LED 2 ON"):
				print("LED 2 ON")
				ser = serial.Serial(com_port, baud_rate)
				ser.write("LED 2 ON".encode())
				ser.close()
				previous = "LED 2 ON"
		else:
			if(previous != "LED 3 ON"):
				print("LED 3 ON")
				ser = serial.Serial(com_port, baud_rate)
				ser.write("LED 3 ON".encode())
				ser.close()
				previous = "LED 3 ON"
	cv2.imshow('Image', frame) 
	if cv2.waitKey(1) & 0xff == ord('q'): 
		break
