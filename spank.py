import os
import time
import random
import threading
import sounddevice as sd
import numpy as np
import pygame
import argparse

# Configuration thresholds (you may need to tweak these depending on your microphone sensitivity)
LIGHT_THRESHOLD = 2.0
MEDIUM_THRESHOLD = 5.0
HARD_THRESHOLD = 15.0
COOLDOWN_SECONDS = 1.0

# Global state
last_hit_time = 0
forced_intensity = None

def play_random_sound(intensity):
    """Pick a random sound from the intensity folder and play it."""
    folder = os.path.join("sounds", intensity)
    if not os.path.exists(folder):
        return
    
    # Read available sound files dynamically
    files = [f for f in os.listdir(folder) if f.endswith(('.mp3', '.wav'))]
    if not files:
        return
        
    sound_file = os.path.join(folder, random.choice(files))
    
    # Play sound using pygame (this is non-blocking)
    try:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

def audio_callback(indata, frames, time_info, status):
    """Callback function for the audio stream to process microphone input."""
    global last_hit_time, forced_intensity
    
    if status:
        pass # Ignore status warnings like underflow for simplicity
        
    # Calculate audio amplitude using numpy's norm
    volume = np.linalg.norm(indata)
    
    current_time = time.time()
    
    # Cooldown check
    if current_time - last_hit_time < COOLDOWN_SECONDS:
        return
        
    # Classify the hit intensity
    if volume > LIGHT_THRESHOLD:
        if forced_intensity:
            print(f"Hit detected. Playing preferred spank: {forced_intensity}")
            play_random_sound(forced_intensity)
            last_hit_time = current_time
        elif volume > HARD_THRESHOLD:
            print("Hard hit detected")
            play_random_sound("hard")
            last_hit_time = current_time
        elif volume > MEDIUM_THRESHOLD:
            print("Medium hit detected")
            play_random_sound("medium")
            last_hit_time = current_time
        else:
            print("Light hit detected")
            play_random_sound("light")
            last_hit_time = current_time

def main():
    global forced_intensity
    
    parser = argparse.ArgumentParser(description="Laptop Spank - Reacts when you slap your laptop")
    parser.add_argument('--spank', type=str, choices=['light', 'medium', 'hard'], 
                        help='Force a specific spank intensity (e.g., hard)')
    args = parser.parse_args()
    
    if args.spank:
        forced_intensity = args.spank
        
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Ensure sound folders exist so it doesn't crash if folders are empty
    for intensity in ["light", "medium", "hard"]:
        os.makedirs(os.path.join("sounds", intensity), exist_ok=True)
        
    print("Listening... slap your laptop.")
    
    try:
        # Continuously listen to microphone input
        with sd.InputStream(callback=audio_callback):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting Laptop Spank. Goodbye!")
    except Exception as e:
        print(f"Error starting microphone stream: {e}")

if __name__ == "__main__":
    main()
