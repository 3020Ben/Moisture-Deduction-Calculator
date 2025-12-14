# Moisture & Deduction Calculator (PyQt5)

A desktop application built with **Python + PyQt5** that helps compute:

✅ Deduction weight based on moisture content  
✅ Moisture content range based on desired deduction  
✅ Auto-validation of numeric inputs  
✅ Professional GUI with per-panel result display  
✅ Field auto-highlight + Tab-navigation + Clear buttons  

---

## 📸 Features

- Two calculators side-by-side:
  - **Deduction Calculator**
  - **Moisture Range Calculator**
- Auto-highlight input fields on focus
- Validators:
  - `Moisture Content` → 2 decimal float
  - `Desired Deduction` → integer only
- Clear buttons for each panel
- Exit button
- Supports future exporting (CSV/PDF)
- Beginner-friendly clean PyQt5 UI

---

## 📂 Project Structure

MoistureDeductionCalculator/
│
├── ui_main.py # Main GUI application
├── calculations.py # Formula logic
├── validators.py # (Optional) external validation helpers
├── icon.ico # (Optional) app icon
└── README.md # Project info


---

## 🔧 Installation

### 1. Install dependencies

```bash
pip install pyqt5

If you want to build an executable:
pip install pyinstaller


▶️ Running the Application
python ui_main.py

🏗 Building a Windows .exe

Use PyInstaller:
pyinstaller --onefile --noconsole ui_main.py

Executable will be located in:
dist/ui_main.exe


🧮 Formulas Used

Deduction Formula
Deducted Weight = (Net Weight × (Moisture% - Allowable%)) / (100 - Allowable%)
Payment Weight = Net Weight - Deducted Weight

Moisture Content Range Formula

(Implemented in calculations.py)


💡 Future Improvements

CSV/PDF Export UI

Add custom App Icon

Add About Window

Add Inno Setup Installer


📜 License

MIT License
