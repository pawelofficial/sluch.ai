import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import numpy as np
import av

# Define an audio processing class
class AudioProcessor(AudioProcessorBase):
    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        st.session_state.audio_data = audio
        st.session_state.audio_length = len(audio)
        return frame

# Stream audio input
from streamlit_webrtc import WebRtcMode

webrtc_ctx = webrtc_streamer(
    key="audio",
    mode=WebRtcMode.SENDRECV,  # Use the correct enum value
    audio_processor_factory=AudioProcessor,
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": False, "audio": True},
    ),
)


# Display real-time audio length
if "audio_data" in st.session_state:
    st.markdown(f"Audio Length: {st.session_state.audio_length} samples")
