import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Page configuration
st.set_page_config(
    page_title="NeuroPath",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧠"
)

# Simulated transcript
transcript = "I... I don't want to go. I don't want to. Please. Please. It's too loud. It's too loud. I don't like it. I want to go home. I want mom. I want mom."

# Analyze sentiment
analyzer = SentimentIntensityAnalyzer()
sentiment_score = analyzer.polarity_scores(transcript)

# Detect word repetition
words = transcript.lower().replace('.', '').split()
repetition_count = sum([1 for i in range(1, len(words)) if words[i] == words[i-1]])

# Simulated flags for demonstration
high_bpm = True
high_volume = True
repetition_alert = repetition_count >= 2
negative_sentiment = sentiment_score['compound'] < -0.3

# Determine emoji and label based on emotion state
if high_bpm and high_volume and repetition_alert and negative_sentiment:
    emotion = "Anxious"
    emoji = "😰"
elif negative_sentiment:
    emotion = "Sad"
    emoji = "😢"
elif sentiment_score['compound'] > 0.3:
    emotion = "Happy"
    emoji = "😊"
else:
    emotion = "Neutral"
    emoji = "😐"

# Main title
st.title("🧠 NeuroPath")

# Animated emoji box in center of page
st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; height: 80vh;'>
        <div style='width: 400px; height: 400px; border-radius: 200px; background-color: #f0f2f6;
                    display: flex; flex-direction: column; align-items: center; justify-content: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3); animation: pulse 2s infinite;'>
            <div style='font-size: 300px; line-height: 300px;'>{emoji}</div>
            <div style='font-size: 32px; font-weight: bold; margin-top: 20px; color: black;'>{emotion}</div>
            
    </div>

     <style>
    @keyframes pulse {{
      0% {{ transform: scale(1); }}
      50% {{ transform: scale(1.05); }}
      100% {{ transform: scale(1); }}
    }}
    </style>
""", unsafe_allow_html=True)
