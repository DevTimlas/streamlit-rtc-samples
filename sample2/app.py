import streamlit as st
import av
from streamlit_webrtc import *
import mediapipe as mp
import cv2
import time

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
drawing_spec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

# nose_landmarks = [49, 279, 197, 2, 5]
nose_landmarks = [127, 93, 58, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 288, 323, 356, 70, 63, 105, 66, 55,
                 285, 296, 334, 293, 300, 168, 6, 195, 4, 64, 60, 94, 290, 439, 33, 160, 158, 173, 153, 144, 398, 385,
                 387, 466, 373, 380, 61, 40, 39, 0, 269, 270, 291, 321, 405, 17, 181, 91, 78, 81, 13, 311, 306, 402, 14,
                 178, 162, 54, 67, 10, 297, 284, 389]



def livestream():
	class VideoProcessor():
		def recv(self, frame):
			arr = frame.to_ndarray(format="bgr24")
			frame = cv2.resize(arr, (640, 480))
			rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			results = faceMesh.process(rgb)
	
			if results.multi_face_landmarks:
				for face_landmarks in results.multi_face_landmarks:
					mpDraw.draw_landmarks(frame, face_landmarks, mpFaceMesh.FACEMESH_CONTOURS, drawing_spec)
					
					for lm_id, lm in enumerate(face_landmarks.landmark):
						h, w, c = rgb.shape
						
						x, y = int(lm.x * w), int(lm.y * h)
						
						if lm_id in nose_landmarks:
							cv2.putText(frame, str(lm_id), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3, (0, 0, 255), 1)
			
			return av.VideoFrame.from_ndarray(frame, format="bgr24")
			
			
			
	webrtc_streamer(key="example",
					rtc_configuration={"iceServers":[
					
					{"urls":"stun:openrelay.metered.ca:80",},
					
					{"urls":"turn:openrelay.metered.ca:80",
					"username":"openrelayproject",
					"credential":"openrelayproject",},
					
					{"urls":"turn:openrelay.metered.ca:443",
					"username":"openrelayproject",
					"credential":"openrelayproject",},
					
					{"urls":"turn:openrelay.metered.ca:443?transport=tcp",
					"username":"openrelayproject",
					"credential":"openrelayproject",},],},
					
					video_processor_factory=VideoProcessor,
					media_stream_constraints={"video":True, "audio":False})
					
					
livestream()
