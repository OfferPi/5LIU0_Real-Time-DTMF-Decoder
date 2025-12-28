#!/opt/lcd_project/venv/bin/python3

# Libraries import
import sounddevice as sd
import numpy as np
import math
import sys
import time
from RPLCD.i2c import CharLCD

# Parameter settings
SAMPLE_RATE = 44100
BLOCK_SIZE = 2048
POWER_THRESHOLD = 800
DEVICE_ID = None

# LCD parameters
I2C_ADDRESS = 0x27
I2C_EXPANDER = 'PCF8574'

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

# Goertzel algorithm
def get_power_at_freq(samples, freq):
    coeff = 2.0 * math.cos(2.0 * math.pi * freq / SAMPLE_RATE)
    s_prev = 0.0
    s_prev2 = 0.0
    
    for sample in samples:
        s = sample + (coeff * s_prev) - s_prev2
        s_prev2 = s_prev
        s_prev = s
        
    power = s_prev2**2 + s_prev**2 - (coeff * s_prev * s_prev2)
    return power

def main():
    # Initialize LCD
    try:
        lcd = CharLCD(i2c_expander=I2C_EXPANDER, address=I2C_ADDRESS, port=1,
                      cols=16, rows=2, dotsize=8, backlight_enabled=True)
        lcd.clear()
        lcd.write_string("DTMF Listener")
        lcd.cursor_pos = (1, 0)
        print("LCD Initialized. Starting Audio Stream...")
        
    except IOError:
        print("Error: Could not connect to LCD. Check wiring/address.")
        sys.exit(1)

    # Keep track of the last button pressed so we don't print something continuously
    last_detected_tone = None
    detected_sequence = ""

    try:
        # Open the microphone
        with sd.InputStream(device=DEVICE_ID, channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE) as stream:
            
            while True:
                # Read audio
                data, overflow = stream.read(BLOCK_SIZE)
                if overflow:
                    continue

                # Flatten data 
                samples = data[:, 0]

                # Find loudest low frequency
                best_low_freq = None
                max_low_power = 0
                for f in LOW_FREQS:
                    power = get_power_at_freq(samples, f)
                    if power > max_low_power:
                        max_low_power = power
                        best_low_freq = f

                # Find loudest high frequency
                best_high_freq = None
                max_high_power = 0
                for f in HIGH_FREQS:
                    power = get_power_at_freq(samples, f)
                    if power > max_high_power:
                        max_high_power = power
                        best_high_freq = f

                # Calculation for decision to print
                if max_low_power > POWER_THRESHOLD and max_high_power > POWER_THRESHOLD:
                    current_tone = DTMF_MAP.get((best_low_freq, best_high_freq))

                    # If tone, print it
                    if current_tone and current_tone != last_detected_tone:
                        print(f"Detected: {current_tone}")
                        
                        # Clear screen if '#' is pressed
                        if current_tone == '#':
                            detected_sequence = ""
                            lcd.clear()
                            lcd.write_string("Cleared")
                            time.sleep(0.5)
                            lcd.clear()
                            lcd.write_string("DTMF Listener")
                        else:
                            # Append to sequence
                            if len(detected_sequence) >= 16:
                                detected_sequence = detected_sequence[1:]
                            
                            detected_sequence += current_tone
                            
                            # Update LCD bottom line
                            lcd.cursor_pos = (1, 0)
                            lcd.write_string(detected_sequence.ljust(16))

                        last_detected_tone = current_tone
                else:
                    # After silence reset the tone, so multiple tones can be played in sequence
                    last_detected_tone = None

        # Allow for keyboard interruption
    except KeyboardInterrupt:
        print("\nStopping...")
        lcd.clear()
        lcd.write_string("Stopped")
    # Print error if there is one
    except Exception as e:
        print(f"\nError: {e}")
        lcd.clear()
        lcd.write_string("Error")

if __name__ == "__main__":
    main()
