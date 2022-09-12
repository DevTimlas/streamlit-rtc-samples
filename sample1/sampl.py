import streamlit as st
import av
from streamlit_webrtc import *

def livestream():
	class VideoProcessor():
		def recv(self, frame):
			arr = frame.to_ndarray(format="bgr24")
			
			return av.VideoFrame.from_ndarray(arr, format="bgr24")
			
			
			
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
					
					video_processor_factory=VideoProcessor)
					
					
livestream()
