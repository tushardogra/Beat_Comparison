from st_audiorec import st_audiorec
import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt

def play_audio(file):
    audio_bytes = open(file, "rb").read()
    st.audio(audio_bytes, format="audio/wav")

st.title("Beat Comparison App")

bpm_options = [30, 35, 40, 45, 50, 60, 120, 240, 480]
user_bpm = st.selectbox("Select the BPM of your audio", options=bpm_options, index=5)
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    # Provide the option to download the recorded audio
    st.audio(wav_audio_data, format='audio/wav')
    user_audio_file = f"user_audio_{user_bpm}BPM.wav"
    with open(user_audio_file, "wb") as audio_file:
        audio_file.write(wav_audio_data)

ideal_audio_file = f'{user_bpm}BPM.wav'
play_audio(ideal_audio_file)
y1, sr1 = librosa.load(ideal_audio_file, sr=None)
onset_frames1 = librosa.onset.onset_detect(y=y1, sr=sr1, units='frames')
beat_time_instances1 = librosa.frames_to_time(onset_frames1, sr=sr1)

def calculate_beat_times(audio_file, bpm):
    y, sr = librosa.load(audio_file, sr=None)
    beat_interval_seconds = 60 / bpm
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='frames')
    beat_time_instances = librosa.frames_to_time(onset_frames, sr=sr)
    return beat_time_instances

if wav_audio_data is not None and user_bpm > 0:
    try:

        if st.button("Calculate Result"):
            user_beat_times = calculate_beat_times(user_audio_file, user_bpm)
            st.write("Ideal Beat Times:", [f"{beat_time:.2f}" for beat_time in calculate_beat_times(ideal_audio_file, user_bpm)])
            st.write("User Beat Times:", [f"{beat_time:.2f}" for beat_time in user_beat_times])
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(beat_time_instances1, label='Actual Beat', marker='o', linestyle='-', color='r')
            ax.plot(user_beat_times, label='User Beat', marker='o', linestyle='-', color='g')
            ax.set_xlabel('Beat Number')
            ax.set_ylabel('Time (s)')
            ax.legend()
            ax.set_title('Beat Time Instances')
            ax.grid()

        # Show the Matplotlib plot in the Streamlit app
            st.pyplot(fig)

            if np.allclose(calculate_beat_times(ideal_audio_file, user_bpm), user_beat_times, atol=0.05):
                st.success("Beat times match the ideal audio!")
            else:
                st.error("Beat times do not match the ideal audio.")
    except:
        st.error(f"The file is not of the correct BPM")
