# ROM Structure Analysis

![Platform](https://img.shields.io/badge/platform-ESP32-blue)
![Language](https://img.shields.io/badge/language-C%20%7C%20Python-orange)
![Status](https://img.shields.io/badge/status-experimental-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

## 📌 Overview

This project explores the analysis of a 16-bit ROM dump acquired using an ESP32-based reader.  
It focuses on reconstructing data from separate MSB/LSB buses and identifying structural patterns within the memory.

## ⚙️ Features

- ROM data acquisition using ESP32 GPIO
- MSB/LSB reconstruction into 16-bit values
- CSV to binary conversion
- Data visualization and pattern analysis using Python
- Exploration of memory structure and repeating patterns

## 🛠️ Technologies

- C (ESP-IDF)
- Python (data processing and visualization)
- ESP32

## 🚀 How It Works

1. ESP32 reads ROM using address and data buses  
2. Data is exported as CSV (`ADDR, DATA`)  
3. Python scripts reconstruct 16-bit values  
4. Data is analyzed for patterns and structure  

## 📊 Goals

- Understand ROM organization at a low level  
- Identify repeating structures and encoded data  
- Explore possible waveform or lookup table regions  

## 📎 Notes

This is an experimental project focused on learning and reverse engineering concepts in embedded systems.
