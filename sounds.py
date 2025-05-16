"""
Sound effects for the prize drawing application.
"""
import numpy as np
import io
import base64
import soundfile as sf
import streamlit as st
from typing import Tuple, Dict, List

# Global cache for sound effects
sound_cache: Dict[str, str] = {}

def generate_sine_wave(freq: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
    """Generate a sine wave of given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)

def generate_drum_roll(duration: float = 2.0, sample_rate: int = 44100) -> np.ndarray:
    """Generate a drum roll sound effect."""
    # Create an array for the sound
    sound = np.zeros(int(sample_rate * duration))
    
    # Add drum hits at regular intervals, with increasing frequency
    base_interval = 0.2  # starting interval in seconds
    for t in np.arange(0, duration, 0.01):
        # Decrease interval as we approach the end
        interval = base_interval * (1 - t/duration*0.8)
        
        # Only add sound at interval points
        if t % interval < 0.005:
            idx = int(t * sample_rate)
            if idx + 500 < len(sound):
                # Create a short drum hit
                hit = np.random.randn(500) * 0.3
                hit = hit * np.exp(-np.linspace(0, 5, len(hit)))
                sound[idx:idx+500] += hit
    
    # Normalize
    return sound / np.max(np.abs(sound))

def generate_celebration_sound(duration: float = 3.0, sample_rate: int = 44100) -> np.ndarray:
    """Generate a celebration sound effect with rising tones."""
    sound = np.zeros(int(sample_rate * duration))
    
    # Add rising tones
    for i, freq in enumerate([440, 523, 659, 784, 880, 1047, 1319, 1568]):
        t = np.linspace(0, 0.3, int(sample_rate * 0.3), False)
        tone = np.sin(2 * np.pi * freq * t)
        # Apply envelope
        envelope = np.exp(-np.linspace(0, 5, len(tone)))
        tone = tone * envelope
        start_idx = int(i * sample_rate * 0.15)
        if start_idx + len(tone) <= len(sound):
            sound[start_idx:start_idx+len(tone)] += tone
    
    # Add shimmer effect at the end
    for i in range(10):
        freq = 800 + 300 * np.random.random()
        t = np.linspace(0, 0.2, int(sample_rate * 0.2), False)
        tone = np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-np.linspace(0, 8, len(tone)))
        tone = tone * envelope * 0.5
        start_idx = int((duration - 1.0) * sample_rate + i * sample_rate * 0.08)
        if start_idx + len(tone) <= len(sound):
            sound[start_idx:start_idx+len(tone)] += tone
    
    # Normalize
    return sound / np.max(np.abs(sound))

def generate_tick_sound(duration: float = 0.1, sample_rate: int = 44100) -> np.ndarray:
    """Generate a tick sound for transitions."""
    sound = np.zeros(int(sample_rate * duration))
    freq = 1200
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-np.linspace(0, 20, len(tone)))
    return tone * envelope

def convert_audio_to_base64(audio: np.ndarray, sample_rate: int = 44100) -> str:
    """Convert audio numpy array to base64 string for HTML audio."""
    # Convert to float32
    audio = audio.astype(np.float32)
    
    # Write to a BytesIO object
    virtual_file = io.BytesIO()
    sf.write(virtual_file, audio, sample_rate, format='WAV')
    virtual_file.seek(0)
    
    # Encode as base64
    audio_base64 = base64.b64encode(virtual_file.read()).decode("utf-8")
    return audio_base64

def get_sound_html(sound_type: str) -> str:
    """Get HTML audio tag for sound with automatic play."""
    if sound_type not in sound_cache:
        # Generate and cache the sound
        if sound_type == 'drum_roll':
            audio = generate_drum_roll()
        elif sound_type == 'celebration':
            audio = generate_celebration_sound()
        elif sound_type == 'tick':
            audio = generate_tick_sound()
        else:
            # Default to tick sound
            audio = generate_tick_sound()
            
        audio_base64 = convert_audio_to_base64(audio)
        sound_cache[sound_type] = audio_base64
    else:
        audio_base64 = sound_cache[sound_type]
    
    # Create HTML audio element
    audio_html = f"""
    <audio autoplay style="display:none">
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
    </audio>
    """
    return audio_html

def play_sound(sound_type: str):
    """Play a sound effect in the Streamlit app."""
    audio_html = get_sound_html(sound_type)
    st.markdown(audio_html, unsafe_allow_html=True)