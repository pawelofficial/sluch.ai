import streamlit as st 
import sys 
import os 
import utils as stu
import time 

# append dir above 
sys.path.append(os.path.abspath('.'))
import sluchai as sai 

stu.init_session_state()



if not stu.is_logged():
    stu.login()
    st.stop()  # stop until login is done
stu.bottom_placeholder()    



#import streamlit as st
#
#audio_bytes = st.audio_input("Record some audio")
#if audio_bytes:
#    st.audio(audio_bytes, format="audio/wav")
    