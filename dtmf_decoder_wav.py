# Libraries import
import argparse
import math
import numpy as np
from scipy.io import wavfile

# Hyperparameter settings
BLOCK_SIZE = 2048
POWER_THRESHOLD = 800

# Goertzel algorithm
def get_power_at_freq(samples, freq, sample_rate):
    coeff = 2.0 * math.cos(2.0 * math.pi * freq / sample_rate)
    
    s_prev = 0.0
    s_prev2 = 0.0
    
    for sample in samples:
        s = sample + (coeff * s_prev) - s_prev2
        s_prev2 = s_prev
        s_prev = s
        
    power = s_prev2**2 + s_prev**2 - (coeff * s_prev * s_prev2)
    return power

# Definine notes (standard DTMF notes)
LOW_FREQS = [697.0, 770.0, 852.0, 941.0]
HIGH_FREQS = [1209.0, 1336.0, 1477.0, 1633.0]

# Lookup dictionary for all numers, * and #
DTMF_MAP = {
    (697.0, 1209.0): '1', (697.0, 1336.0): '2', (697.0, 1477.0): '3',
    (770.0, 1209.0): '4', (770.0, 1336.0): '5', (770.0, 1477.0): '6',
    (852.0, 1209.0): '7', (852.0, 1336.0): '8', (852.0, 1477.0): '9',
    (941.0, 1209.0): '*', (941.0, 1336.0): '0', (941.0, 1477.0): '#',
}

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='Path to wav file')
    args = parser.parse_args()

    print(f"Starting DTMF File Decoder")
    print(f"File: {args.file}")
    print(f"Threshold: {POWER_THRESHOLD}")

    # Keep track of the last button pressed so we don't print something continuously
    last_detected_tone = None
    
    # List to store the history of all unique tones heard
    detected_tones = []

    try:
        # Read the wav file
        sample_rate, data = wavfile.read(args.file)

        # Convert to float and normalize if necessary (to match sounddevice's -1.0 to 1.0 range)
        if data.dtype == np.int16:
            data = data / 32768.0
        elif data.dtype == np.int32:
            data = data / 2147483648.0
            
        # Handle stereo (take first channel)
        if len(data.shape) > 1:
            data = data[:, 0]

        # Iterate over audio data in blocks
        total_samples = len(data)
        
        for i in range(0, total_samples, BLOCK_SIZE):
            # Slice audio data
            samples = data[i:i + BLOCK_SIZE]
            
            # Skip incomplete blocks at the end
            if len(samples) < BLOCK_SIZE:
                continue

            # Find loudest low frequency
            best_low_freq = None
            max_low_power = 0
            
            for f in LOW_FREQS:
                power = get_power_at_freq(samples, f, sample_rate)
                if power > max_low_power:
                    max_low_power = power
                    best_low_freq = f

            # Find loudest high frequency
            best_high_freq = None
            max_high_power = 0
            
            for f in HIGH_FREQS:
                power = get_power_at_freq(samples, f, sample_rate)
                if power > max_high_power:
                    max_high_power = power
                    best_high_freq = f

            # Calculation for decision to print
            if max_low_power > POWER_THRESHOLD and max_high_power > POWER_THRESHOLD:
                
                # Lookup tone
                current_tone = DTMF_MAP.get((best_low_freq, best_high_freq))
                
                # If tone, print it
                if current_tone and current_tone != last_detected_tone:
                    print(f"Detected: {current_tone}")
                    detected_tones.append(current_tone)
                    last_detected_tone = current_tone
            
            else:
                # After silence reset the tone, so multiple tones can be played in sequence
                last_detected_tone = None

        # Output final list
        print(f"\nFinal Sequence Heard: {detected_tones}")
        print(f"Sequence String: {''.join(detected_tones)}")

    # Print error if there is one
    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    main()