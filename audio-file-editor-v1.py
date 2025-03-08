import streamlit as st
from pydub import AudioSegment
import numpy as np
import os
import tempfile

st.title("🎵 Audio Editor (Trim .wav Files)")

# Upload audio file
uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file:
    # Save the uploaded file temporarily
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load audio
    audio = AudioSegment.from_wav(input_path)
    duration = len(audio) / 1000  # Convert to seconds

    # Display audio player
    st.audio(uploaded_file, format="audio/wav")

    # Select trimming range
    start_time, end_time = st.slider(
        "Select Trim Range (seconds)",
        0.0, duration, (0.0, duration), step=0.1
    )

    if st.button("Trim Audio"):
        # Convert seconds to milliseconds
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)

        # Trim audio
        trimmed_audio = audio[start_ms:end_ms]

        # Save trimmed file
        output_path = os.path.join(temp_dir, "trimmed_audio.wav")
        trimmed_audio.export(output_path, format="wav")

        # Provide download option
        st.audio(output_path, format="audio/wav")
        with open(output_path, "rb") as f:
            st.download_button("Download Trimmed Audio", f, "trimmed_audio.wav")

