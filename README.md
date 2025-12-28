# DTMF Decoder

## Introduction

This project implements a DTMF (Dual-Tone Multi-Frequency) decoder capable of detecting and decoding telephone keypad tones in real-time or from audio files. DTMF tones are used in telephone systems to represent digits 0-9, *, and # by combining two specific frequencies.

The decoder uses the Goertzel algorithm for efficient frequency detection and can operate in multiple modes:
- Real-time decoding from microphone input
- Decoding from WAV audio files
- Raspberry Pi version with LCD display output

## Features

- **Real-time DTMF detection** from audio input devices
- **WAV file analysis** for offline decoding
- **Raspberry Pi support** with I2C LCD display
- **Configurable parameters** (sample rate, block size, power threshold)
- **Test utilities** for data collection and validation
- **Performance evaluation** across different noise levels

## Directory Structure

```
dtmf-decoder/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── results.md                     # Performance test results
├── dtmf_decoder.py               # Real-time microphone decoder
├── dtmf_decoder_wav.py           # WAV file decoder
├── dtmf_decoder_rpi.py           # Raspberry Pi version with LCD
├── dtmf_number_generator.py      # Test sequence generator
├── data_collector.py             # Audio recording utility
└── data_dir/                     # Test audio files directory
    ├── dtmf_test_sequence_25-35_db.wav
    ├── dtmf_test_sequence_35-45_db.wav
    ├── dtmf_test_sequence_45-55_db.wav
    └── dtmf_test_sequence_65-75_db.wav
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dtmf-decoder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

For Raspberry Pi LCD support, ensure I2C is enabled on your system.

## Usage

### Real-time Decoding

Decode DTMF tones from your microphone in real-time:

```bash
python dtmf_decoder.py
```

### WAV File Decoding

Decode DTMF tones from a WAV audio file:

```bash
python dtmf_decoder_wav.py -f path/to/audio.wav
```

### Raspberry Pi with LCD

Run the decoder on Raspberry Pi with LCD output:

```bash
./dtmf_decoder_rpi.py
```

### Generate Test Sequences

Generate random DTMF test sequences:

```bash
python dtmf_number_generator.py -r <run_number>
```

### Record Audio

Record audio for testing:

```bash
python data_collector.py
```

## Configuration

Default parameters in the decoder scripts:

- **Sample Rate**: 44100 Hz
- **Block Size**: 2048 samples
- **Power Threshold**: 800
- **DTMF Frequencies**:
  - Low: 697, 770, 852, 941 Hz
  - High: 1209, 1336, 1477, 1633 Hz