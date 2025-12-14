# ui_main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QGroupBox, QTextEdit, QFileDialog,
    QMenuBar, QFormLayout)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from calculations import deducted_weight, moisture_content_range
#from validators import validate_positive_integer, validate_positive_number

# ------------------------------
# Highlight-on-focus LineEdit
# ------------------------------
class HighlightLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.selectAll()

# ------------------------------
# Main Window
# ------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moisture & Deduction Calculator")
        self.setStyleSheet("""
            QWidget {
                font-size: 18px;
                font-family: Segoe UI;
            }
            QGroupBox {
                font-size: 20px;
                font-weight: bold;           
            }
            """)
        #self.history = []
        self.build_ui()

    # ------------------------------
    # UI Builder
    # ------------------------------
    def build_ui(self):
        layout = QVBoxLayout()

        # menubar = QMenuBar()
        # file_menu = menubar.addMenu("Export")
        # act_csv = file_menu.addAction("Export as CSV")
        # act_pdf = file_menu.addAction("Export as PDF")
        # act_csv.triggered.connect(self.export_csv_handler)
        # act_csv.triggered.connect(self.export_pdf_handler)
        # layout.addWidget(menubar)

        # ----- Deduction Calculator Panel -----
        ded_group = QGroupBox("Deduction Calculator")
        ded_form = QFormLayout()

        self.ded_net = HighlightLineEdit()
        self.ded_moist = HighlightLineEdit()

        # Float with two decimal places between 5.00 and 59.99
        moist_validator = QDoubleValidator(5.00, 59.99, 2)
        moist_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ded_moist.setValidator(moist_validator)

        self.allow_box1 = QComboBox()
        self.allow_box1.addItems(["10","12","14"])

        ded_btn = QPushButton("Compute Deduction")
        ded_btn.clicked.connect(self.calculate_deduction)

        self.ded_result = QTextEdit()
        self.ded_result.setReadOnly(True)
        self.ded_result.setFixedHeight(100)

        ded_clear_btn = QPushButton("Clear Deduction Fields")
        ded_clear_btn.clicked.connect(self.clear_deduction_fields)

        ded_form.addRow("Net Weight (kg):", self.ded_net)
        ded_form.addRow("Moisture Content (%):", self.ded_moist)
        ded_form.addRow("Allowable Moisture (%):", self.allow_box1)
        ded_form.addRow(ded_btn)
        ded_form.addRow(ded_clear_btn)
        ded_form.addRow("Result :", self.ded_result)
    
        ded_group.setLayout(ded_form)

        # ----- Moisture Range Panel -----
        moist_group = QGroupBox("Moisture Content Calculator")
        moist_form = QFormLayout()

        self.moist_net = HighlightLineEdit()
        self.moist_ded = HighlightLineEdit()
        self.moist_ded.setValidator(QIntValidator(1, 10000)) # Integers only

        self.allow_box2 = QComboBox()
        self.allow_box2.addItems(["10","12","14"])

        moist_btn = QPushButton("Compute Moisture Range")
        moist_btn.clicked.connect(self.calculate_moisture_range)

        self.moist_result = QTextEdit()
        self.moist_result.setReadOnly(True)
        self.moist_result.setFixedHeight(100)

        moist_clear_btn = QPushButton("Clear Moisture Fields")
        moist_clear_btn.clicked.connect(self.clear_moisture_fields)

        moist_form.addRow("Net Weight (kg) :", self.moist_net)
        moist_form.addRow("Desired Deduction (kg) :", self.moist_ded)
        moist_form.addRow("Allowable Moisture (%) :", self.allow_box2)
        moist_form.addRow(moist_btn)
        moist_form.addRow(moist_clear_btn)
        moist_form.addRow("Result :", self.moist_result)

        moist_group.setLayout(moist_form)

        # ---- Panels side by side ----
        calc_layout = QHBoxLayout()
        calc_layout.addWidget(ded_group)
        calc_layout.addWidget(moist_group)

        layout.addLayout(calc_layout)

        # ----- Exit Button -----
        exit_layout = QHBoxLayout()
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        exit_layout.addStretch()
        exit_layout.addWidget(exit_btn)
        layout.addLayout(exit_layout)

        self.setLayout(layout)

        # ----- Tabbing Order -----
        self.setTabOrder(self.ded_net, self.ded_moist)
        self.setTabOrder(self.ded_moist, self.allow_box1)
        self.setTabOrder(self.allow_box1, ded_btn)
        self.setTabOrder(ded_btn, ded_clear_btn)

        self.setTabOrder(ded_clear_btn, self.moist_net)
        self.setTabOrder(self.moist_net, self.moist_ded)
        self.setTabOrder(self.moist_ded, self.allow_box2)
        self.setTabOrder(self.allow_box2, moist_btn)
        self.setTabOrder(moist_btn, moist_clear_btn)

        self.setTabOrder(moist_clear_btn, exit_btn)

    # ----------------------------------------------------------------------
    # CALCULATION LOGIC
    # ----------------------------------------------------------------------
    def calculate_deduction(self):
        try:
            net_weight = int(self.ded_net.text())
            moisture_content = float(self.ded_moist.text())
            allowable_moisture = int(self.allow_box1.currentText())
            
            # Enforce exactly 2 decimal places for moisture content
            self.ded_moist.setText(f"{moisture_content: .2f}")

            result = deducted_weight(net_weight, moisture_content, allowable_moisture)
            text = (
                f"Deduction (kg):        {int(result['deducted_weight'])}\n"
                f"Payment Weight (kg):   {int(result['payment_weight'])}"
                )
            self.ded_result.setText(text)
            #self.history.append(("Deduction Calculation", net_weight, moisture_content, allowable_moisture, text))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calculate_moisture_range(self):
        try:
            net_weight = int(self.moist_net.text())
            desired_deduction = int(self.moist_ded.text())
            allowable_moisture = int(self.allow_box2.currentText())

            result = moisture_content_range(net_weight, desired_deduction, allowable_moisture)
            text = f"MC Range (%):    {result[0]: .2f} - {result[1]: .2f}"
            self.moist_result.setText(text)
            #self.history.append(("Moisture Range Calculation", net_weight, desired_deduction, allowable_moisture, text))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ---------------------------------------------------------
    # CLEAR BUTTONS
    # ---------------------------------------------------------
    def clear_deduction_fields(self):
        self.ded_net.clear()
        self.ded_moist.clear()
        self.allow_box1.setCurrentIndex(0)
        self.ded_result.clear()
        self.ded_net.setFocus()


    def clear_moisture_fields(self):
        self.moist_net.clear()
        self.moist_ded.clear()
        self.allow_box2.setCurrentIndex(0)
        self.moist_result.clear()
        self.moist_net.setFocus()

# ---------------------------------------------------------
# Run App
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
