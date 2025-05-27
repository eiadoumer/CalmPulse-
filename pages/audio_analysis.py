import streamlit as st
import speech_recognition as sr
import librosa
import soundfile as sf
import numpy as np
import tempfile
import matplotlib.pyplot as plt
from collections import Counter
import re
import time

st.set_page_config(page_title="Audio Analysis", layout="wide")

st.title("🔊 Audio Analysis")

# --- Synthwave-style Animation (CSS) ---
  
animation_placeholder = st.empty()


def record_and_analyze():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening for 5 seconds...")
        audio = r.listen(source, timeout=5)

    try:
        # Save to temp WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_path = f.name
            with open(wav_path, "wb") as out:
                out.write(audio.get_wav_data())

      
        transcript = r.recognize_google(audio)
        st.success("📝 Transcript:")
        st.write(transcript)

        # --- Term Frequency ---
        words = re.findall(r'\w+', transcript.lower())
        freq = Counter(words)
        common_words = freq.most_common(10)

        # --- Pitch Analysis ---
        y, sr_rate = librosa.load(wav_path)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr_rate)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        avg_pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0

        st.metric("🎼 Average Pitch (Hz)", f"{avg_pitch:.2f}")
        
        
        # Store values in session state after processing
       # --- Volume Analysis ---
        frame_size = int(sr_rate / 10)  # 100ms frames
        volume_data = np.array([
            np.mean(np.abs(y[i:i + frame_size]))
            for i in range(0, len(y), frame_size)
        ])
        volume_timestamps = [round(i * 0.1, 2) for i in range(len(volume_data))]  # in seconds

        # Save to session state
        st.session_state['transcript'] = transcript
        st.session_state['volume_series'] = list(volume_data)
        st.session_state['volume_timestamps'] = list(volume_timestamps)
        st.session_state['avg_volume'] = float(np.mean(volume_data))


        # --- Plot Term Frequency ---
        if common_words:
            st.subheader("🧠 Top Terms")
            words, counts = zip(*common_words)
            counts = [int(count) for count in counts]  # Ensure counts are integers
            fig1, ax1 = plt.subplots()
            ax1.bar(words, counts, color="#ff0080")
            ax1.set_ylabel("Frequency")
            ax1.set_title("Term Frequency")
            st.pyplot(fig1)

        # --- Plot Pitch over time (optional) ---
        st.subheader("📊 Pitch Over Time")
        pitch_mean = np.mean(pitches, axis=0)
        fig2, ax2 = plt.subplots()
        ax2.plot(pitch_mean, color="#7928ca")
        ax2.set_ylabel("Pitch (Hz)")
        ax2.set_xlabel("Frame")
        ax2.set_title("Pitch Variation")
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"Error analyzing voice: {e}")

# Record button
if st.button("🎤 Record and Analyze"):
    animation_placeholder.markdown("""
        <style>
        .synthwave-wave {
          background: linear-gradient(135deg, #ff0080, #7928ca);
          height: 6px;
          margin-top: 30px;
          animation: pulse 1s infinite alternate;
          border-radius: 4px;
        }
        @keyframes pulse {
          0% { width: 30%; opacity: 0.7; }
          100% { width: 100%; opacity: 1; }
        }
        </style>
        <div class="synthwave-wave"></div>
    """, unsafe_allow_html=True)
    record_and_analyze()

    time.sleep(1)  # Simulate recording delay
   

    # After analysis, remove the animation
    animation_placeholder.empty()
