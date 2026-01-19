# VORTEX LOGIC 👁️‍🗨️
> **Advanced Static Binary Analysis Suite**

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3-blue?style=for-the-badge)

**VortexLogic** is a premium reverse engineering tool designed for malware analysts and security researchers. It provides a comprehensive dashboard for statically analyzing Windows PE executables (`.exe`, `.dll`, `.sys`).

## ⚡ Features
*   **Deep Inspection**: Analyze File Headers, Optional Headers, and Sections.
*   **Entropy Visualization**: Visual progress bars to instantly detect packed or encrypted code sections.
*   **Capstone Disassembler**: Integrated x86/x64 disassembler to view the Entry Point code in real-time.
*   **Strings & Hex**: Native extractor for ASCII/Unicode strings and raw Hex dump viewer.
*   **Cyberpunk UI**: Modern, dark-themed interface built with CustomTkinter for maximum usability.

## 🚀 Quick Start
No installation required. Just run the script.

### Prerequisites
*   Python 3.x
*   Dependencies: `customtkinter`, `pefile`, `capstone`

```bash
pip install -r requirements.txt
```

### Launch
```bash
python main.py
```
*Wait for the initialization sequence to complete.*

## 📂 Structure
*   `main.py` - Core GUI and Logic entry point.
*   `analyzer.py` - Analysis engine (PEFile wrapper).
*   `test_bin/` - Contains dummy binaries for testing.

---
*Created by Neil*
