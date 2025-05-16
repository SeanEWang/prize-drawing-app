"""
Prize Drawing Application

A Streamlit web app for conducting prize drawings with animation effects.
"""
import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
import io
import base64

from utils import calculate_probabilities, select_winner, save_to_csv, load_from_csv
from animations import draw_animation, celebration_animation
from localization import get_text, get_available_languages
from sounds import play_sound

# Configure page settings
st.set_page_config(
    page_title="Prize Drawing App",
    page_icon="🎁",
    layout="wide"
)

# Initialize session state variables
if 'participants' not in st.session_state:
    # Default participants from the user's example
    default_participants = [
        {"name": "祥懿教練", "tickets": 5},
        {"name": "Lulu", "tickets": 3},
        {"name": "David", "tickets": 2},
        {"name": "Emily", "tickets": 4},
        {"name": "John", "tickets": 1}
    ]
    st.session_state.participants = default_participants

if 'winner' not in st.session_state:
    st.session_state.winner = None

if 'drawing_in_progress' not in st.session_state:
    st.session_state.drawing_in_progress = False
    
if 'show_stats' not in st.session_state:
    st.session_state.show_stats = False

if 'language' not in st.session_state:
    st.session_state.language = "中文"  # Default to Chinese

if 'drawing_title' not in st.session_state:
    st.session_state.drawing_title = "體重管理挑戰賽 8888"  # Default title from user example

# Function to get translated text
def t(key):
    return get_text(key, st.session_state.language)

def add_participant():
    """Add a new participant to the list."""
    if st.session_state.new_name and st.session_state.new_tickets > 0:
        # Check for duplicates
        existing_names = [p["name"].lower() for p in st.session_state.participants]
        if st.session_state.new_name.lower() in existing_names:
            # Update tickets if the name already exists
            for p in st.session_state.participants:
                if p["name"].lower() == st.session_state.new_name.lower():
                    p["tickets"] = st.session_state.new_tickets
                    break
        else:
            # Add new participant
            st.session_state.participants.append({
                "name": st.session_state.new_name,
                "tickets": st.session_state.new_tickets
            })
        
        # Reset input fields
        st.session_state.new_name = ""
        st.session_state.new_tickets = 1
        st.rerun()

def reset_drawing():
    """Reset the drawing state."""
    st.session_state.winner = None
    st.session_state.drawing_in_progress = False

def start_drawing():
    """Start the drawing animation process."""
    if not st.session_state.participants:
        st.warning(t("no_participants"))
        return
    
    # Play a drum roll sound when starting the drawing
    play_sound("drum_roll")
    
    st.session_state.drawing_in_progress = True
    st.session_state.winner = None
    st.rerun()

def display_probability_chart():
    """Display a bar chart of winning probabilities."""
    if not st.session_state.participants:
        return
    
    # Calculate probabilities
    probs = calculate_probabilities(st.session_state.participants)
    
    # Sort by probability in descending order
    probs = sorted(probs, key=lambda x: x["probability"], reverse=True)
    
    # Create a DataFrame for plotting
    df = pd.DataFrame(probs)
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(df["name"], df["probability"], color="skyblue")
    
    # Add probability values as text
    for bar, prob in zip(bars, df["probability"]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f"{prob:.1f}%", va='center')
    
    # Add labels and title
    ax.set_xlabel(t("probability"))
    ax.set_title(f"{t('drawing_title')}: {t('probability')}")
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def download_participants():
    """Generate a CSV download link for current participants."""
    csv_data = save_to_csv(st.session_state.participants)
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="participants.csv">{t("save")}</a>'
    return href

def toggle_statistics():
    """Toggle display of statistics charts."""
    st.session_state.show_stats = not st.session_state.show_stats

# Main app layout
st.title(t("app_title"))

# Language selection
with st.sidebar:
    # Language selector
    selected_language = st.selectbox(
        t("language"),
        options=get_available_languages(),
        index=get_available_languages().index(st.session_state.language)
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()
    
    # Custom drawing title
    custom_title = st.text_input(
        t("custom_title"), 
        value=st.session_state.drawing_title
    )
    
    if custom_title != st.session_state.drawing_title:
        st.session_state.drawing_title = custom_title

    # Upload participants from CSV
    st.subheader(t("load"))
    uploaded_file = st.file_uploader(t("upload_file"), type=["csv"])
    
    if uploaded_file is not None:
        csv_content = uploaded_file.getvalue().decode("utf-8")
        loaded_participants = load_from_csv(csv_content)
        
        if loaded_participants:
            st.session_state.participants = loaded_participants
            st.success(t("file_loaded"))
            st.rerun()
        else:
            st.error(t("invalid_file"))
    
    # Download participants to CSV
    if st.session_state.participants:
        st.markdown(download_participants(), unsafe_allow_html=True)

# Main drawing section
st.header(st.session_state.drawing_title)

# Participant entry form
with st.form(key="add_participant_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.text_input(t("name_label"), key="new_name")
    
    with col2:
        st.number_input(
            t("tickets_label"), 
            min_value=1, 
            max_value=1000, 
            value=1,
            step=1,
            key="new_tickets"
        )
    
    submit_button = st.form_submit_button(
        label=t("add_participant"), 
        on_click=add_participant
    )

# Display participants table
if st.session_state.participants:
    st.subheader(t("participants"))
    
    # Convert to DataFrame for display
    df = pd.DataFrame(st.session_state.participants)
    
    # Calculate probability column if we have participants
    if not df.empty:
        total_tickets = df["tickets"].sum()
        df["probability"] = (df["tickets"] / total_tickets * 100).round(2)
        df["probability"] = df["probability"].astype(str) + "%"
    
    # Rename columns for display
    df = df.rename(columns={
        "name": t("name_label"),
        "tickets": t("tickets_label"),
        "probability": t("probability")
    })
    
    # Show table
    st.dataframe(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(t("draw_button"), key="draw_button"):
            start_drawing()
    
    with col2:
        if st.button(t("reset"), key="reset_button"):
            st.session_state.participants = []
            reset_drawing()
            st.rerun()
    
    with col3:
        if st.session_state.show_stats:
            if st.button(t("hide_statistics")):
                toggle_statistics()
        else:
            if st.button(t("show_statistics")):
                toggle_statistics()
    
    # Display total tickets
    total_tickets = sum(p["tickets"] for p in st.session_state.participants)
    st.info(f"{t('total_tickets')}: {total_tickets}")

# Statistics visualization
if st.session_state.show_stats and st.session_state.participants:
    chart = display_probability_chart()
    if chart:
        st.pyplot(chart)

# Drawing animation and results
if st.session_state.drawing_in_progress:
    # Display progress message
    st.subheader(t("drawing_in_progress"))
    
    # Perform drawing animation
    with st.spinner():
        winner = draw_animation(st.session_state.participants)
        st.session_state.winner = winner
        st.session_state.drawing_in_progress = False
        st.rerun()

# Display winner
if st.session_state.winner:
    st.subheader(t("winner"))
    
    # Play celebration sound
    play_sound("celebration")
    
    # Display celebration
    celebration_animation(st.session_state.winner["name"], st.session_state.language)
    
    # Winner details
    with st.container():
        st.markdown("""
        <style>
        .winner-box {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
            animation: winner-pulse 2s infinite;
        }
        @keyframes winner-pulse {
            0% { box-shadow: 0 0 0 0px rgba(255, 215, 0, 0.4); }
            100% { box-shadow: 0 0 0 20px rgba(255, 215, 0, 0); }
        }
        </style>
        """, unsafe_allow_html=True)
        
        winner_html = f"""
        <div class="winner-box">
            <h1>🏆 {st.session_state.winner["name"]} 🏆</h1>
            <h3>{t("tickets_label")}: {st.session_state.winner["tickets"]}</h3>
        </div>
        """
        st.markdown(winner_html, unsafe_allow_html=True)
        
        if st.button(t("draw_button") + " ↺"):
            start_drawing()
