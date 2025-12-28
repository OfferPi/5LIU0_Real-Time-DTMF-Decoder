import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time

# Configuration (Matches your DTMF script settings)
SAMPLE_RATE = 44100
CHANNELS = 1
OUTPUT_FILENAME = "dtmf_test_sequence.wav"

def record_until_interrupt():
    print(f"--- Recording to '{OUTPUT_FILENAME}' ---")
    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print("Press Ctrl+C to stop recording and save the file.")
    print("---------------------------------------------")

    # List to hold the audio data chunks
    recorded_audio = []

    try:
        # Open the stream
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS) as stream:
            start_time = time.time()
            
            while True:
                # Read chunks of audio (1024 frames is a standard buffer)
                data, overflow = stream.read(1024)
                
                # Copy the data to our list
                recorded_audio.append(data)
                
                # Visual indicator that it is running
                elapsed = int(time.time() - start_time)
                print(f"Recording... {elapsed}s", end='\r')

    except KeyboardInterrupt:
        print("\n\nStopping recording...")
        
        # Concatenate all chunks into one NumPy array
        if len(recorded_audio) > 0:
            final_recording = np.concatenate(recorded_audio, axis=0)
            
            # Save to WAV file
            # sounddevice returns floats, scipy can write floats directly
            print(f"Saving {len(final_recording)} samples...")
            write(OUTPUT_FILENAME, SAMPLE_RATE, final_recording)
            print(f"Successfully saved to {OUTPUT_FILENAME}")
        else:
            print("No audio recorded.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    record_until_interrupt()