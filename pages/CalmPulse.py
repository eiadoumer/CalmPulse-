import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go

# Load synthetic data
heartbeat_df = pd.read_csv("heartBeat.csv")
audio_volume_df = pd.read_csv("audio_volume.csv")

# Simulated transcript
transcript = "I... I don't want to go. I don't want to. Please. Please. It's too loud. It's too loud. I don't like it. I want to go home. I want mom. I want mom."

# Analyze sentiment
analyzer = SentimentIntensityAnalyzer()
sentiment_score = analyzer.polarity_scores(transcript)

# Detect word repetition
words = transcript.lower().replace('.', '').split()
repetition_count = sum([1 for i in range(1, len(words)) if words[i] == words[i-1]])

# Emotion detection logic
high_bpm = heartbeat_df['bpm'].max() > 100
high_volume = audio_volume_df['volume'].mean() > 0.4
repetition_alert = repetition_count >= 2
negative_sentiment = sentiment_score['compound'] < -0.3

# Emotion label
if high_bpm and high_volume and repetition_alert and negative_sentiment:
    emotion = "Anxious / Needs Help"
else:
    emotion = "Stable"

# Streamlit UI
st.set_page_config(page_title="Autism Emotion Detector", layout="wide")
st.title("🧠 Autism Emotion Detection MVP")

# Display emotion state
st.subheader("Current Detected Emotion")
st.markdown(f"### {emotion}")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Heartbeat Over Time")
    fig, ax = plt.subplots()
    ax.plot(pd.to_datetime(heartbeat_df['timestamp']), heartbeat_df['bpm'], marker='o')
    ax.set_ylabel("BPM")
    ax.set_xlabel("Time")
    ax.set_title("Heartbeat Data")
    st.pyplot(fig)

with col2:
    st.subheader("Voice Volume Levels")
    fig2, ax2 = plt.subplots()
    ax2.plot(audio_volume_df['time_step'], audio_volume_df['volume'], color='orange', marker='s')
    ax2.set_ylabel("Volume")
    ax2.set_xlabel("Time Step")
    ax2.set_title("Audio Volume Over Time")
    st.pyplot(fig2)

# Transcript analysis
st.subheader("Speech Transcript")
st.text_area("Transcript:", transcript, height=150)

st.markdown("---")
st.write("🔍 Sentiment Score:", sentiment_score)
st.write("🔁 Repetition Count:", repetition_count)
st.write("❤️ Max BPM:", heartbeat_df['bpm'].max())
st.write("🔊 Avg Volume:", round(audio_volume_df['volume'].mean(), 2))

# Normalize and prepare radar chart values
max_bpm_norm = min(heartbeat_df['bpm'].max() / 150, 1)  # assuming 150 BPM max for scale
avg_volume_norm = min(audio_volume_df['volume'].mean(), 1)  # volume already 0-1 scale
repetition_norm = 1 if repetition_alert else 0
negative_sentiment_norm = abs(sentiment_score['compound']) if sentiment_score['compound'] < 0 else 0

labels = ['Max BPM', 'Avg Volume', 'Repetition Alert', 'Negative Sentiment']
values = [max_bpm_norm, avg_volume_norm, repetition_norm, negative_sentiment_norm]

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=values + [values[0]],  # Close the loop
    theta=labels + [labels[0]],
    fill='toself',
    name='Emotion Indicators',
    line_color='crimson'
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )
    ),
    showlegend=False,
    title="Emotion Radar Chart"
)

st.plotly_chart(fig_radar, use_container_width=True)
