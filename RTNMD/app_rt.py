import cv2

from streamlit_webrtc import *
import streamlit as st
import os
import av
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
from tensorflow_addons import metrics as mt
import numpy as np
# from rtnmt1 import make_predict


F1Score = mt.F1Score(num_classes=2, threshold=.5)

model = load_model('./streamlit-rtc-samples/RTNMD/model.h5',
 compile=False, custom_objects={'F1Score':F1Score})

results={0:'mask',1:'no mask'}
GR_dict={0:(0,0,255),1:(0,255,0)}

rect_size = 4


haarcascade = cv2.CascadeClassifier('./streamlit-rtc-samples/RTNMD/haarcascade_frontalface_default.xml')

def livestream():
	class VideoProcessor():
		def recv(self, frame):
			im = frame.to_ndarray(format="bgr24")
			im=cv2.flip(im,1,1)
			
			rerect_size = cv2.resize(im, (im.shape[1] // rect_size, im.shape[0] // rect_size))
			faces = haarcascade.detectMultiScale(rerect_size)
			for f in faces:
				(x, y, w, h) = [v * rect_size for v in f] 
				
				face_img = im[y:y+h, x:x+w]
				rerect_sized=cv2.resize(face_img,(224,224))
				normalized=rerect_sized/255.0
				reshaped=np.reshape(normalized,(1,224,224,3))
				reshaped = np.vstack([reshaped])
				
				result=model.predict(reshaped)

        
				label=np.argmax(result,axis=1)[0]
			  
				cv2.rectangle(im,(x,y),(x+w,y+h),GR_dict[label],2)
				cv2.rectangle(im,(x,y-40),(x+w,y),GR_dict[label],-1)
				cv2.putText(im, results[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
			
			
			return av.VideoFrame.from_ndarray(im, format="bgr24")
		
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
