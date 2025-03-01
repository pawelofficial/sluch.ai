import sounddevice as sd
import wave
import os 
import sounddevice as sd
import yaml 
import datetime

from sluchai.utils import setup_logger,purge_dir,CONFIG


import sounddevice as sd
import numpy as np

#device_index = 15  # Your Stereo Mix device
#def callback(indata, frames, time, status):
#    if status:
#        print(status)
#    volume_norm = np.linalg.norm(indata) * 10
#    print(f"Volume level: {volume_norm:.2f}")
#
#with sd.InputStream(device=device_index, channels=2, callback=callback, samplerate=48000, dtype='int16'):
#    sd.sleep(5000)
#exit(1)




this_dir=os.path.dirname(os.path.abspath(__file__))
data_dir=os.path.join(this_dir,"data")
input_data_dir=os.path.join(this_dir,"input_data")
purge_dir(data_dir)
logs_path=os.path.join(this_dir,"logs")
LOGGER=setup_logger("windows_record",fp=os.path.join(logs_path,'windows_recorder.log') )


# Configuration
samplerate = CONFIG['SAMPLERATE'] # 48000.0  # Standard CD quality
channels = int(CONFIG['CHANNELS'])  # Stereo
duration = int(CONFIG['DURATION'])  # Record in 30s chunks
device_index = int(CONFIG['DEVICE_INDEX'])  # "Stereo Mix (Realtek(R) Audio), Windows WASAPI"
overlap=int(CONFIG['OVERLAP'])



def find_device(device_name="Stereo Mix (Realtek(R) Audio)"):
    devices=sd.query_devices()
    for i,device in enumerate(devices):
        if device_name in device['name']:
            return i        
    
    print(f"Device {device_name} not found")
    print("Available devices:")
    for i,device in enumerate(devices):
        print(f" found {i}: {device['name']}")
    raise ValueError(f"Device {device_name} not found")


def check_devices(device_index=8):
    device_index = device_index  # Use your WASAPI Stereo Mix device
    device_info = sd.query_devices(device_index)
    s=[]
    s.append(f"Device: {device_info['name']}")
    s.append(f"Supported Sample Rate: {device_info['default_samplerate']}")
    s.append(f"number of channels : {device_info['max_input_channels']}")
    devices=sd.query_devices()
    s.append(str(devices))
    LOGGER.info("\n".join(s))


def record_audio(filename,device_index):
    print(f"Recording {filename}...")
    # Capture system audio
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16', device=device_index)
    sd.wait()  # Wait for recording to finish
    # Save to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    print(f"Saved: {filename}")

# Loop to continuously save 30s chunks
def start_recording(device_index=device_index):
    purge_dir(data_dir)
    file_counter = 1
    while True:
        now=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{file_counter:04d}_recording_{now}.wav"
        fp=os.path.join(data_dir,filename)
        record_audio(fp,device_index)
        file_counter += 1


def mp3_to_wav(filename,dir=None):
    if not dir:
        dir=input_data_dir  
    # Convert MP3 to WAV
    mp3_fp = os.path.join(dir, filename)
    wav_fp = os.path.join(dir, filename.replace('.mp3', '.wav'))
    os.system(f"ffmpeg -i {mp3_fp} {wav_fp}")
    print(f"Converted {mp3_fp} to {wav_fp}")
    return wav_fp


def slice_file(filename, overlap=5, core_slice=30,dir=None):
    if not dir:
        dir=input_data_dir
    fp = os.path.join(dir, filename)
    
    purge_dir(os.path.join(this_dir, 'slices'))
    output_dir = os.path.join(this_dir, 'slices')

    with wave.open(fp, 'rb') as wf:
        sample_width = wf.getsampwidth()
        channels = wf.getnchannels()
        framerate = wf.getframerate()
        total_frames = wf.getnframes()

        core_slice_frames = int(core_slice * framerate)
        overlap_frames = int(overlap * framerate)

        # Read the full audio data
        audio_data = wf.readframes(total_frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        if channels > 1:
            audio_array = audio_array.reshape(-1, channels)

        chunk_idx = 1
        for core_start in range(0, total_frames, core_slice_frames):
            core_end = core_start + core_slice_frames
            # Extend slice by overlap on both sides (if available)
            slice_start = max(0, core_start - overlap_frames)
            slice_end = min(total_frames, core_end + overlap_frames)
            chunk = audio_array[slice_start:slice_end]

            start_seconds=int(slice_start / framerate)
            end_seconds=int(slice_end / framerate)
            chunk_filename = os.path.join(output_dir, f"{chunk_idx:03d}_slice_{start_seconds}_{end_seconds}.wav")
            with wave.open(chunk_filename, 'wb') as wf_chunk:
                wf_chunk.setnchannels(channels)
                wf_chunk.setsampwidth(sample_width)
                wf_chunk.setframerate(framerate)
                wf_chunk.writeframes(chunk.tobytes())

            print(f"Saved {chunk_filename}")
            chunk_idx += 1

    print("Chunking complete!")
