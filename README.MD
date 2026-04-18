# ROM Structure Analysis

![Platform](https://img.shields.io/badge/platform-ESP32-blue)
![Language](https://img.shields.io/badge/language-C%20%7C%20Python-orange)
![License](https://img.shields.io/badge/license-MIT-green)

## 📌 Overview

This project explores the analysis of a 16-bit ROM dump acquired using an ESP32-based reader.  
It focuses on reconstructing data from separate MSB/LSB buses and identifying structural patterns within the memory.

![Structure](/docs/images/breadboard.jpeg)

---

## ⚙️ Features

- ROM data acquisition using ESP32 GPIO
- MSB/LSB reconstruction into 16-bit values
- CSV to binary conversion
- Data visualization and pattern analysis using Python
- Exploration of memory structure and repeating patterns

## 🧠 How it Works

The ROM does not store full audio files. Instead, it stores
small waveform segments that are looped and processed by the
keyboard's internal sound engine.

## 🛠️ Technologies

- ESP32 (ROM dumping)
- C (ESP-IDF)
- Python (data processing and plotting)
- Audacity (audio inspection)

---

## 📐 Hardware Schematic

<p align="center">
  <img src="/docs/images/schematics.jpg" width="600"/>
</p>

ESP32 reads the ROM by iterating over a 12-bit address bus (A[0–11]),
while the ROM outputs 8-bit data (D[0–7]).

## ⚠️ Hardware Limitation

Due to the limited number of available GPIO pins on the ESP32 (~20),
not all address lines can be driven directly. As a result, higher-order
address bits (MSBs) *A[17-12]* are configured using fixed hardware logic.

---

## 🔄 Pipeline

1. Dump ROM via ESP32
2. Merge LSB/MSB into 16-bit data
3. Convert CSV → BIN
4. Analyze patterns and structures
5. Extract waveform/audio candidates
6. Generate playable audio samples

## 📊 Goals

- Understand ROM organization at a low level  
- Identify repeating structures and encoded data  
- Explore possible waveform or lookup table regions
- Extract all data from ROM addresses

---

## 📈 Data Visualization

<p align="center">
  <img src="/data/addr_100010/samples/images/700_normalized_sample_data_100010.jpeg" width="500"/>
</p>

**Note:** This graph shows the relationship between **memory address** and **stored values**,
revealing repeating patterns that indicate structured waveform data.

---

## 🔊 Results

- Identified repeating waveform patterns
- Extracted short PCM-like samples (drum-like sounds)
- Observed that most sounds are synthesized rather than stored as full audio

---

## 📎 Notes

This is an experimental project focused on learning and reverse engineering concepts in embedded systems.
