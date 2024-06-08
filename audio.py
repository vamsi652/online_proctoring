import sounddevice as sd
import numpy as np

# Constants and thresholds
CALLBACKS_PER_SECOND = 38               # Callbacks per second (system dependent)
SUS_FINDING_FREQUENCY = 2               # Frequency to calculate "suspicious" (SUS) sound
SOUND_AMPLITUDE_THRESHOLD = 20          # Amplitude threshold for SUS calculation
FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)  # Number of frames to consider for SUS

# Placeholders and global variables
AMPLITUDE_LIST = [0] * FRAMES_COUNT
SUS_COUNT = 0
count = 0
AUDIO_CHEAT = 0

def print_sound(indata, outdata, frames, time, status):
    """
    Callback function to process the sound data.
    """
    global SUS_COUNT, count, AUDIO_CHEAT

    # Calculate the norm of the input sound data to determine its amplitude
    vnorm = int(np.linalg.norm(indata) * 10)
    
    # Update the amplitude list
    AMPLITUDE_LIST.append(vnorm)
    count += 1
    AMPLITUDE_LIST.pop(0)
    
    if count == FRAMES_COUNT:
        # Calculate the average amplitude
        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT

        if SUS_COUNT >= 2:
            # Detected suspicious activity
            AUDIO_CHEAT = 1
            SUS_COUNT = 0
        elif avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            # Increment the SUS count if the average amplitude is above the threshold
            SUS_COUNT += 1
        else:
            # Reset the SUS count and cheat flag if amplitude is below the threshold
            SUS_COUNT = 0
            AUDIO_CHEAT = 0

        # Reset the frame count
        count = 0

def sound():
    """
    Start the sound stream and analyze the incoming sound.
    """
    with sd.Stream(callback=print_sound):
        sd.sleep(-1)  # Keep the stream open indefinitely


