# Moisture & Deduction Calculator (PyQt5)

A desktop application built with **Python + PyQt5** that calculates:

- 📉 **Deduction weight** based on moisture content  
- 📊 **Moisture content range** based on desired deduction  

Designed with a clean UI, input validation, and an optional **Auto Compute mode** for faster workflows.

---

## ✨ Features

- Two calculators side-by-side:
  - **Deduction Calculator**
  - **Moisture Content Range Calculator**
- Auto Compute mode with selectable behavior:
  - Auto-compute **Deduction**
  - Auto-compute **Moisture Range**
- Input validation using PyQt validators
- Auto-highlight input fields on focus
- Clear buttons per panel + global reset
- Light / Dark mode toggle
- Defensive error handling (no crashes on empty inputs)
- Modular calculation logic

---

## 🖥️ Screens & UX Highlights

- Right-aligned numeric inputs
- Read-only result fields
- Auto-compute safeguards with user prompts
- Keyboard-friendly (Tab navigation supported)

---

## 📂 Project Structure


## MoistureDeductionCalculator/
│

├── ui_main.py # Main PyQt5 GUI

├── calculations.py # Business logic / formulas

├── test_calculations.py # Business logic / formulas test calculations

├── validators.py # External validation helpers

├── requirements.txt # Python dependencies

├── icon.ico # App icon

└── README.md # Project documentation


---

## 🔧 Installation

### 1️⃣ Clone the repository
```bash
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

Use PyInstaller:

`bash

pyinstaller --onefile --noconsole ui_main.py

Executable will be located in:

`bash

dist/ui_main.exe

---

🧮 Formulas Used

Deduction Formula

Deducted Weight = (Net Weight × (Moisture% - Allowable%)) / (100 - Allowable%)

Payment Weight = Net Weight - Deducted Weight

Moisture Content Range Formula

(Implemented in calculations.py)

---

💡 Future Improvements

CSV / PDF export

Application icon

About dialog window

Installer package (Inno Setup)

Unit tests for calculations

Configurable allowable moisture values

---

📜 License

MIT License

