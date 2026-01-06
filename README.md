# Moisture & Deduction Calculator (PyQt5)

A desktop application built with **Python + PyQt5** for calculating:

- 📉 **Deducted weight** based on moisture content  
- 📊 **Moisture content range** based on a desired deduction  

Designed for simplicity, accuracy, and fast manual computation.

---

## ✨ Features

- Two calculators in one window:
  - **Deduction Calculator**
  - **Moisture Content Range Calculator**
- Input validation (integers, decimals, and limits enforced)
- Auto-highlight input fields on focus
- Read-only result fields
- Clear buttons for each calculator
- Keyboard-friendly tab navigation
- Defensive error handling using dialog alerts

---

## 🖥️ Application Overview

### Deduction Calculator
Calculates:
- Deducted weight (kg)
- Payment weight (kg)

Based on:
- Net weight
- Moisture content
- Allowable moisture percentage

### Moisture Content Range Calculator
Calculates:
- Minimum and maximum moisture content (%)  
that produces a desired deduction.

---

## 📂 Project Structure


## MoistureDeductionCalculator/
│

├── ui_main.py # Main PyQt5 GUI

├── calculations.py # Business logic / formulas

├── test_calculations.py # Business logic / formulas test calculations

├── validators.py # Input validation helpers

├── requirements.txt # Python dependencies

├── icon.ico # Application icon (optional)

└── README.md # Project documentation


---

## 🔧 Installation

### 1️⃣ Clone the repository
`bash
git clone https://github.com/your-username/moisture-deduction-calculator.git
cd moisture-deduction-calculator


### 2️⃣ Install dependencies
pip install -r requirements.txt


---

▶️ Running the Application

`bash
python ui_main.py

---

🏗 Building a Windows Executable

This project can be packaged into a standalone .exe using PyInstaller.

Install PyInstaller
Install Pillow for icon photo conversion

pip install pyinstaller
pip install Pillow

Build the executable
pyinstaller --onefile --windowed --icon=icon.ico ui_main.py


The executable will be located at:

dist/ui_main.exe
---

🧮 Formulas Used

Deduction Formula

Deducted Weight = (Net Weight × (Moisture% - Allowable%)) / (100 - Allowable%)

Payment Weight = Net Weight - Deducted Weight

Moisture Content Range Formula

(Implemented in calculations.py)

---

Moisture Content Range

Calculated iteratively in calculations.py to determine the moisture
range that results in the desired deduction.

---

💡 Future Improvements

Export results to CSV / PDF

About dialog window

Application installer (Inno Setup)

Unit tests for calculations

Configurable allowable moisture values

---

📜 License

MIT License

