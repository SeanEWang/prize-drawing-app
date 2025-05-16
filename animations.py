"""
Animation utilities for the prize drawing application.
"""
import streamlit as st
import time
import random
from sounds import play_sound

def draw_animation(participants, duration=10.0, steps=50):
    """
    Create an animation for the drawing process.
    
    Args:
        participants: List of dictionaries with name and tickets
        duration: Total animation duration in seconds
        steps: Number of animation steps
        
    Returns:
        The winning participant
    """
    if not participants:
        return None
    
    # Create a blank placeholder for the animation
    animation_placeholder = st.empty()
    
    # Welcome message
    animation_placeholder.markdown(f"""
    <div style="text-align:center; padding: 20px;">
        <h2>🎉 歡迎來到抽獎！🎉</h2>
        <p>抽獎即將開始，準備好囉！</p>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(2)
    
    # Create the ticket pool like in the original script
    ticket_pool = []
    for p in participants:
        ticket_pool.extend([p] * p["tickets"])
    
    # Show animation message
    animation_placeholder.markdown(f"""
    <div style="text-align:center; padding: 20px;">
        <h2>🎰 正在抽出得獎者，請稍候... 🎰</h2>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)
    
    # Animation: show rapidly changing names
    start_time = time.time()
    tick_count = 0
    while time.time() - start_time < duration:
        # Select a random participant to show
        if ticket_pool:
            selected = random.choice(ticket_pool)
            
            # Display with animation effect
            animation_placeholder.markdown(f"""
            <div style="text-align:center; padding: 20px;">
                <h2>>> {selected['name']} <<</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Slow down toward the end for dramatic effect
            elapsed = time.time() - start_time
            
            # Play tick sound at intervals
            tick_count += 1
            if tick_count % 5 == 0:  # Only play sound every 5 ticks to avoid overloading
                play_sound("tick")
                
            if elapsed > duration * 0.7:
                time.sleep(0.2)
            else:
                time.sleep(0.1)
    
    # Select the actual winner
    winner = select_winner(participants)
    
    # Display the winner with a celebration effect
    animation_placeholder.markdown(f"""
    <div style="text-align:center; padding: 20px;">
        <h1>🎊 恭喜得獎者是：{winner['name']}！ 🎊</h1>
    </div>
    """, unsafe_allow_html=True)
    
    return winner

def select_winner(participants):
    """
    Select a winner based on ticket distribution.
    
    Args:
        participants: List of dictionaries with name and tickets
        
    Returns:
        Dictionary with the winner's name and tickets
    """
    # Create a ticket pool with each name appearing according to their ticket count
    ticket_pool = []
    for p in participants:
        ticket_pool.extend([p] * p["tickets"])
    
    # If no tickets, select randomly from participants
    if not ticket_pool:
        return random.choice(participants)
    
    return random.choice(ticket_pool)

def celebration_animation(winner_name, language="English"):
    """
    Display a celebration animation for the winner.
    
    Args:
        winner_name: Name of the winner
        language: Language for congratulations message
    """
    congratulations = {
        "English": "Congratulations!",
        "中文": "恭喜！",
        "Español": "¡Felicitaciones!"
    }.get(language, "Congratulations!")
    
    # Create emojis for celebration
    emojis = ["🎉", "🎊", "🏆", "✨", "🎇", "🎈", "🥳", "👏"]
    
    # Display celebration with animation
    celebration_placeholder = st.empty()
    
    for i in range(5):
        random_emojis = ' '.join(random.sample(emojis, 4))
        celebration_placeholder.markdown(f"""
        <div style="text-align:center; padding: 30px; animation: pulse 1s infinite;">
            <h1>{random_emojis}</h1>
            <h2>{congratulations}</h2>
            <h1>{winner_name}</h1>
            <h1>{random_emojis}</h1>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.5)
    
    # Final celebration display
    celebration_placeholder.markdown(f"""
    <div style="text-align:center; padding: 30px;">
        <h1>🎉 🏆 ✨</h1>
        <h2>{congratulations}</h2>
        <h1>{winner_name}</h1>
        <h1>🎊 🎈 🥳</h1>
    </div>
    """, unsafe_allow_html=True)
