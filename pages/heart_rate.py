import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Heart Rate Monitor - NeuroPath",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="❤️"
)

def show_heartbeat_detector():
    """Display animated heartbeat detector with real-time monitoring"""
    
    # Try to load actual heartbeat data, fallback to simulated data
    try:
        heartbeat_df = pd.read_csv("heartBeat.csv")
        current_bpm = heartbeat_df['bpm'].iloc[-1]  # Get latest BPM
        avg_bpm = heartbeat_df['bpm'].mean()
        max_bpm = heartbeat_df['bpm'].max()
        min_bpm = heartbeat_df['bpm'].min()
    except:
        # Simulated heartbeat data if CSV not available
        current_bpm = random.randint(85, 120)
        avg_bpm = 95
        max_bpm = 130
        min_bpm = 70
    
    # Determine heartbeat status
    if current_bpm > 100:
        status = "High"
        color = "#ff4444"
        pulse_speed = "0.6s"
        status_emoji = "🔴"
    elif current_bpm < 60:
        status = "Low" 
        color = "#4444ff"
        pulse_speed = "1.2s"
        status_emoji = "🔵"
    else:
        status = "Normal"
        color = "#44ff44"
        pulse_speed = "0.8s"
        status_emoji = "🟢"
    
    # Animated heartbeat visualization
    heartbeat_animation = f"""
    <style>
    @keyframes heartbeat {{
        0%, 100% {{ 
            transform: scale(1); 
            opacity: 1;
        }}
        25% {{ 
            transform: scale(1.3); 
            opacity: 0.8;
        }}
        50% {{ 
            transform: scale(1.1); 
            opacity: 1;
        }}
        75% {{ 
            transform: scale(1.4); 
            opacity: 0.7;
        }}
    }}
    
    @keyframes pulse-ring {{
        0% {{
            transform: scale(1);
            opacity: 1;
        }}
        100% {{
            transform: scale(2.5);
            opacity: 0;
        }}
    }}
    
    .heartbeat-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 30px 0;
        position: relative;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }}
    
    .heart-icon {{
        font-size: 120px;
        color: {color};
        animation: heartbeat {pulse_speed} ease-in-out infinite;
        z-index: 2;
        position: relative;
        filter: drop-shadow(0 0 10px {color});
    }}
    
    .pulse-ring {{
        position: absolute;
        width: 150px;
        height: 150px;
        border: 4px solid {color};
        border-radius: 50%;
        animation: pulse-ring {pulse_speed} ease-out infinite;
    }}
    
    .pulse-ring:nth-child(2) {{
        animation-delay: 0.3s;
    }}
    
    .bpm-display {{
        font-size: 48px;
        font-weight: bold;
        color: white;
        margin-top: 20px;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .status-display {{
        font-size: 24px;
        color: #f0f0f0;
        margin-top: 10px;
        text-align: center;
        font-weight: 600;
    }}
    </style>
    
    <div class="heartbeat-container">
        <div class="pulse-ring"></div>
        <div class="pulse-ring"></div>
        <div class="heart-icon">❤️</div>
        <div class="bmp-display">{current_bpm} BPM</div>
        <div class="status-display">{status_emoji} {status}</div>
    </div>
    """
    
    st.markdown(heartbeat_animation, unsafe_allow_html=True)
    
    return current_bpm, status, avg_bpm, max_bpm, min_bpm

def show_breathing_activity():
    """Guided breathing exercise with animation"""
    
    st.subheader("🫁 Guided Breathing Exercise")
    st.info("Follow the breathing circle to help lower your heart rate")
    
    # Define the animated breathing circle
    animated_circle = """
    <style>
    @keyframes breathe {
        0%, 100% { 
            transform: scale(1); 
            background: linear-gradient(45deg, #a2d5f2, #7fb3d3);
        }
        50% { 
            transform: scale(1.5); 
            background: linear-gradient(45deg, #7fb3d3, #5b9bd5);
        }
    }

    .breath-circle {
        width: 200px;
        height: 200px;
        background: linear-gradient(45deg, #a2d5f2, #7fb3d3);
        border-radius: 50%;
        margin: 50px auto 20px auto;
        animation: breathe 8s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(162, 213, 242, 0.6);
    }
    </style>

    <div class="breath-circle"></div>
    """

    static_circle = """
    <style>
    .breath-circle {
        width: 200px;
        height: 200px;
        background: linear-gradient(45deg, #a2d5f2, #7fb3d3);
        border-radius: 50%;
        margin: 50px auto 20px auto;
        box-shadow: 0 0 20px rgba(162, 213, 242, 0.4);
    }
    </style>

    <div class="breath-circle"></div>
    """

    # Display breathing circle and instruction text
    circle_placeholder = st.empty()
    text_placeholder = st.empty()
    progress_bar = st.progress(0)

    # Display animated circle
    circle_placeholder.markdown(animated_circle, unsafe_allow_html=True)

    # Breathing loop with progress
    total_cycles = 3
    for cycle in range(total_cycles):
        # Breathe in
        text_placeholder.markdown("<h2 style='text-align: center; color: #003366;'>🌬️ Breathe in slowly...</h2>", unsafe_allow_html=True)
        for i in range(40):
            progress_bar.progress((cycle * 100 + i * 2.5) / (total_cycles * 100))
            time.sleep(0.1)
        
        # Hold
        text_placeholder.markdown("<h2 style='text-align: center; color: #005577;'>⏸️ Hold your breath...</h2>", unsafe_allow_html=True)
        time.sleep(2)
        
        # Breathe out
        text_placeholder.markdown("<h2 style='text-align: center; color: #003366;'>💨 Breathe out slowly...</h2>", unsafe_allow_html=True)
        for i in range(40):
            progress_bar.progress((cycle * 100 + 40 + i * 2.5) / (total_cycles * 100))
            time.sleep(0.1)

    # Complete
    progress_bar.progress(100)
    circle_placeholder.markdown(static_circle, unsafe_allow_html=True)
    text_placeholder.markdown("<h2 style='text-align: center; color: #003366;'>✨ Excellent! Well done! ✨</h2>", unsafe_allow_html=True)
    
    st.balloons()

def show_heart_rate_history():
    """Display heart rate trends and history"""
    
    try:
        heartbeat_df = pd.read_csv("heartBeat.csv")
        
        # Convert timestamp to datetime if it's not already
        if 'timestamp' in heartbeat_df.columns:
            heartbeat_df['timestamp'] = pd.to_datetime(heartbeat_df['timestamp'])
        else:
            # Create timestamps for demo
            heartbeat_df['timestamp'] = pd.date_range(
                start=datetime.now() - timedelta(hours=len(heartbeat_df)/60),
                periods=len(heartbeat_df),
                freq='1min'
            )
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Heart Rate Over Time', 'Heart Rate Distribution'),
            vertical_spacing=0.1,
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )
        
        # Line chart
        fig.add_trace(
            go.Scatter(
                x=heartbeat_df['timestamp'],
                y=heartbeat_df['bpm'],
                mode='lines+markers',
                name='BPM',
                line=dict(color='red', width=3),
                marker=dict(size=6)
            ),
            row=1, col=1
        )
        
        # Add threshold lines
        fig.add_hline(y=100, line_dash="dash", line_color="orange", 
                     annotation_text="High BPM Threshold", row=1, col=1)
        fig.add_hline(y=60, line_dash="dash", line_color="blue", 
                     annotation_text="Low BPM Threshold", row=1, col=1)
        
        # Histogram
        fig.add_trace(
            go.Histogram(
                x=heartbeat_df['bpm'],
                nbinsx=20,
                name='BPM Distribution',
                marker_color='lightcoral',
                opacity=0.7
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Heart Rate Analysis Dashboard",
            height=600,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Time", row=1, col=1)
        fig.update_yaxes(title_text="BPM", row=1, col=1)
        fig.update_xaxes(title_text="BPM", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Could not load heart rate history: {e}")
        
        # Generate sample data for demo
        sample_data = {
            'timestamp': pd.date_range(start=datetime.now() - timedelta(hours=2), 
                                     periods=120, freq='1min'),
            'bpm': np.random.normal(85, 15, 120).astype(int)
        }
        sample_df = pd.DataFrame(sample_data)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(sample_df['timestamp'], sample_df['bpm'], 'r-', linewidth=2, alpha=0.8)
        ax.axhline(y=100, color='orange', linestyle='--', alpha=0.7, label='High BPM')
        ax.axhline(y=60, color='blue', linestyle='--', alpha=0.7, label='Low BPM')
        ax.set_ylabel('BPM')
        ax.set_xlabel('Time')
        ax.set_title('Sample Heart Rate Data')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

def show_heart_rate_insights(current_bpm, avg_bpm, max_bpm, min_bpm):
    """Display insights and recommendations based on heart rate data"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current BPM", f"{current_bpm}", 
                 delta=f"{current_bpm - avg_bpm:.0f} vs avg")
    
    with col2:
        st.metric("Average BPM", f"{avg_bpm:.0f}")
    
    with col3:
        st.metric("Max BPM", f"{max_bpm}")
    
    with col4:
        st.metric("Min BPM", f"{min_bpm}")
    
    # Health insights
    st.subheader("📊 Heart Rate Insights")
    
    if current_bpm > 100:
        st.warning("""
        **Elevated Heart Rate Detected**
        - Your heart rate is above normal resting range
        - This could indicate stress, anxiety, or physical activity
        - Consider trying relaxation techniques
        """)
    elif current_bpm < 60:
        st.info("""
        **Low Heart Rate Detected**
        - Your heart rate is below typical resting range
        - This could be normal for athletes or indicate relaxation
        - Monitor how you're feeling overall
        """)
    else:
        st.success("""
        **Normal Heart Rate Range**
        - Your heart rate is in a healthy resting range (60-100 BPM)
        - This suggests good cardiovascular health
        - Keep up the good work!
        """)

# Main page content
st.title("❤️ Heart Rate Monitor")
st.markdown("### Real-time cardiovascular monitoring for autism support")

# Real-time heart rate display
current_bpm, status, avg_bpm, max_bpm, min_bpm = show_heartbeat_detector()

# Quick action buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🫁 Start Breathing Exercise", use_container_width=True, type="primary"):
        show_breathing_activity()

with col2:
    if st.button("📊 Refresh Reading", use_container_width=True):
        st.rerun()

with col3:
    if st.button("🔄 Reset Monitor", use_container_width=True):
        st.success("Monitor reset! Taking new reading...")
        time.sleep(1)
        st.rerun()

# Heart rate insights
st.markdown("---")
show_heart_rate_insights(current_bpm, avg_bpm, max_bpm, min_bpm)

# Heart rate history
st.markdown("---")
st.subheader("📈 Heart Rate History")
show_heart_rate_history()

# Recommendations based on current state
st.markdown("---")
st.subheader("💡 Personalized Recommendations")

if current_bpm > 100:
    st.error("""
    **High Heart Rate - Immediate Actions:**
    - 🫁 Try deep breathing exercises (available above)
    - 🪑 Sit or lie down in a comfortable position
    - 💧 Drink cool water
    - 🌬️ Get fresh air if possible
    - 📱 Contact support person if symptoms persist
    """)
elif current_bpm < 60:
    st.info("""
    **Low Heart Rate - Monitor and Support:**
    - ☕ Consider a warm drink
    - 🚶‍♀️ Try gentle movement or stretching
    - 🌞 Get some natural light
    - 💧 Stay hydrated
    - 📞 Contact healthcare provider if concerned
    """)
else:
    st.success("""
    **Optimal Heart Rate - Maintain Wellness:**
    - ✅ Continue current activities
    - 🏃‍♀️ Good time for regular exercise
    - 🧘‍♀️ Practice mindfulness
    - 📈 Keep monitoring regularly
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
        💓 Your heart health matters. Regular monitoring helps maintain wellness. 💓<br>
        <strong>Emergency:</strong> If you feel chest pain, dizziness, or severe discomfort, seek immediate medical attention.
    </div>
""", unsafe_allow_html=True)