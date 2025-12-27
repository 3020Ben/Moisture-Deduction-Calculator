# ui_main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox,
    QMenuBar, QFormLayout, QRadioButton, QButtonGroup,
    QCheckBox, QComboBox
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from calculations import deducted_weight, moisture_content_range, payment_weight


# -------------------------------------------------
# THEMES
# -------------------------------------------------
LIGHT_THEME = """
QWidget {
    font-size: 18px;
    font-family: Segoe UI;
}
QGroupBox {
    font-size: 20px;
    font-weight: bold;
}
"""

DARK_THEME = """
QWidget {
    background-color: #2b2b2b;
    color: #e6e6e6;
    font-size: 18px;
    font-family: Segoe UI;
}
QLineEdit, QTextEdit {
    background-color: #3c3f41;
    color: white;
}
QPushButton {
    background-color: #555;
    padding: 6px;
}
QGroupBox {
    font-size: 20px;
    font-weight: bold;
}
"""


# ------------------------------
# Highlight-on-focus LineEdit
# ------------------------------
class HighlightLineEdit(QLineEdit):
    def __init__ (self):
        super().__init__()
        self.setAlignment(Qt.AlignRight)

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
        self.auto_compute_enabled = False
        self.suppress_auto = False
        self.setStyleSheet(LIGHT_THEME)
        self.build_ui()

    # -------------------------------------------------
    # Helper
    # -------------------------------------------------
    def create_allowable_moisture_group(self, default=12):
        group = QButtonGroup(self)
        layout = QHBoxLayout()
        for value in (10, 12, 14):
            btn = QRadioButton(f"{value}%")
            group.addButton(btn, value)
            layout.addWidget(btn)
            if value == default:
                btn.setChecked(True)

        return group, layout
    
    def current_net_weight_field(self):
        return self.ded_net if self.auto_select.currentText() == "Deduction" else self.moist_net
    
    def show_auto_input_error(self, field_name, clear_callback):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Missing Input")
        msg.setText(f"{field_name} cannot be empty in Auto Compute mode.")
        msg.setInformativeText("What would you like to do?")
        msg.setStandardButtons(
            QMessageBox.Retry | QMessageBox.Reset | QMessageBox.Close
        )
        msg.button(QMessageBox.Retry).setText("Enter Value")
        msg.button(QMessageBox.Reset).setText("Clear Fields")
        msg.button(QMessageBox.Close).setText("Exit Program")

        choice = msg.exec_()

        if choice == QMessageBox.Reset:
            self.reset_with_suppression(clear_callback)
        elif choice == QMessageBox.Close:
            self.close()

    def reset_with_suppression(self, clear_callback):
        self.suppress_auto = True
        self.auto_compute_enabled = False
        self.auto_toggle.setChecked(False)

        clear_callback()

        self.suppress_auto = False


    # ------------------------------
    # UI Builder
    # ------------------------------
    def build_ui(self):
        main_layout = QVBoxLayout()


        # ---------------- MENU BAR ----------------
        menubar = QMenuBar(self)

        file_menu =  menubar.addMenu("File")
        file_menu.addAction("Export to CSV")
        file_menu.addAction("Export to PDF")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Dark Mode").triggered.connect(
            lambda: self.theme_toggle.setChecked(not self.theme_toggle.isChecked())
        )

        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Clear All").triggered.connect(self.clear_all_fields)

        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About").triggered.connect(
            lambda: QMessageBox.information(self, "About", "Moisture & Deduction Calculator v1.0")
        )

        main_layout.setMenuBar(menubar)


         # ---------------- TOGGLES ----------------
        toggle_layout = QHBoxLayout()
        self.auto_toggle = QCheckBox("Auto Compute")
        self.auto_toggle.toggled.connect(self.toggle_auto_compute)
      
        self.auto_select = QComboBox()
        self.auto_select.addItems(["Deduction", "Moisture Range"])
        self.auto_select.setEnabled(True)

        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.toggled.connect(self.toggle_theme)

        toggle_layout.addWidget(self.auto_toggle)
        toggle_layout.addWidget(self.auto_select)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.theme_toggle)
        main_layout.addLayout(toggle_layout)


        # ---------------- DEDUCTION PANEL ----------------
        ded_group = QGroupBox("Deduction Calculator")
        ded_form = QFormLayout()

        self.ded_net = HighlightLineEdit()
        self.ded_net.setValidator(QIntValidator(1, 30000))

        self.ded_moist = HighlightLineEdit()
        self.ded_moist.setValidator(QDoubleValidator(5.00, 59.99, 2))

        # Allowable Moisture Switch (10 / 12 / 14)
        self.allow_group1, allow_layout1 = self.create_allowable_moisture_group()
    
        self.ded_result = HighlightLineEdit()
        self.ded_result.setReadOnly(True)
        self.ded_payment = HighlightLineEdit()
        self.ded_payment.setReadOnly(True)

        ded_btn = QPushButton("Compute Deduction")
        ded_btn.setFixedHeight(32)
        ded_btn.clicked.connect(self.calculate_deduction)

        ded_clear_btn = QPushButton("Clear Deduction Fields")
        ded_clear_btn.setFixedHeight(32)
        ded_clear_btn.clicked.connect(self.clear_deduction_fields)

        ded_form.addRow("Allowable Moisture (%): ", allow_layout1)
        ded_form.addRow("Net Weight (kg): ", self.ded_net)
        ded_form.addRow("Moisture Content (%): ", self.ded_moist)
        ded_form.addRow("Deduction (kg): ", self.ded_result)
        ded_form.addRow("Payment Weight (kg): ", self.ded_payment)
        ded_form.addRow(ded_btn)
        ded_form.addRow(ded_clear_btn)
    
        ded_group.setLayout(ded_form)


        # ---------------- MOISTURE PANEL ----------------
        moist_group = QGroupBox("Moisture Content Calculator")
        moist_form = QFormLayout()

        self.moist_net = HighlightLineEdit()
        self.moist_net.setValidator(QIntValidator(1, 30000))

        self.moist_ded = HighlightLineEdit()
        self.moist_ded.setValidator(QIntValidator(1, 10000))

        self.moist_payment = HighlightLineEdit()
        self.moist_payment.setReadOnly(True)
        self.moist_result = HighlightLineEdit()
        self.moist_result.setReadOnly(True)

        self.allow_group2, allow_layout2 = self.create_allowable_moisture_group()

        moist_btn = QPushButton("Compute Moisture Range")
        moist_btn.setFixedHeight(32)
        moist_btn.clicked.connect(self.calculate_moisture_range)

        moist_clear_btn = QPushButton("Clear Moisture Fields")
        moist_clear_btn.setFixedHeight(32)
        moist_clear_btn.clicked.connect(self.clear_moisture_fields)

        moist_form.addRow("Allowable Moisture (%): ", allow_layout2)
        moist_form.addRow("Net Weight (kg) :", self.moist_net)
        moist_form.addRow("Desired Deduction (kg) :", self.moist_ded)
        moist_form.addRow("Payment Weight (kg) :", self.moist_payment)
        moist_form.addRow("Moisture Range (%) :", self.moist_result)
        moist_form.addRow(moist_btn)
        moist_form.addRow(moist_clear_btn)
        
        moist_group.setLayout(moist_form)


        # ---------------- LAYOUT ----------------
        calc_layout = QHBoxLayout()
        calc_layout.addWidget(ded_group)
        calc_layout.addWidget(moist_group)
        main_layout.addLayout(calc_layout)


        # ---------------- EXIT ----------------
        exit_layout = QHBoxLayout()
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        exit_layout.addStretch()
        exit_layout.addWidget(exit_btn)
        main_layout.addLayout(exit_layout)

        self.setLayout(main_layout)

        
        # ---------------- AUTO-COMPUTE (FIELD BASED) ----------------
        self.ded_net.textChanged.connect(self.update_auto_toggle_state)
        self.moist_net.textChanged.connect(self.update_auto_toggle_state)

        self.ded_net.textChanged.connect(self.auto_deduction)
        self.ded_moist.textChanged.connect(self.auto_deduction)

        self.moist_net.textChanged.connect(self.auto_moisture)
        self.moist_ded.textChanged.connect(self.auto_moisture)


    # -------------------------------------------------
    # AUTO COMPUTE CONTROL
    # -------------------------------------------------
    def update_auto_toggle_state(self):
        net = self.current_net_weight_field().text()
        self.auto_toggle.setEnabled(bool(net.strip()))

    def toggle_auto_compute(self, checked):
        if checked and not self.current_net_weight_field().text().strip():
            QMessageBox.warning(self, "Missing Input", "Please input Net Weight first.")
            self.auto_toggle.setChecked(False)
            return
        self.auto_compute_enabled = checked


    # -------------------------------------------------
    # THEME TOGGLE
    # -------------------------------------------------
    def toggle_theme(self, dark):
        self.setStyleSheet(DARK_THEME if dark else LIGHT_THEME)


    # -------------------------------------------------
    # AUTO-COMPUTE WORKING PATTERN
    # -------------------------------------------------
    def auto_deduction(self):
        if self.suppress_auto:
            return
        if not self.auto_compute_enabled and self.auto_select.currentText() == "Deduction":
            return
        if not self.ded_moist.text().strip():
            self.show_auto_input_error(
                "Moisture Content",
                self.clear_deduction_fields
            )
            return
        self.calculate_deduction(auto=True)

    def auto_moisture(self):
        if self.suppress_auto:
            return
        if not self.auto_compute_enabled and self.auto_select.currentText() == "Moisture Range":
            return
        if not self.moist_ded.text().strip():
            self.show_auto_input_error(
                "Desired Deduction",
                self.clear_moisture_fields
            )
            return

        self.calculate_moisture_range(auto=True)


    # -------------------------------------------------
    # CALCULATIONS
    # -------------------------------------------------
    def calculate_deduction(self, auto=False):
        if not self.ded_net.text() or not self.ded_moist.text():
            QMessageBox.warning(self, "Missing Input", "Please enter Net Weight and Moisture Content.")
            return
        
        net_weight = int(self.ded_net.text())
        moisture_content = float(self.ded_moist.text())
        allowable_moisture = self.allow_group1.checkedId()

        result = deducted_weight(net_weight, moisture_content, allowable_moisture)
        self.ded_result.setText(str(result["deducted_weight"]))
        self.ded_payment.setText(str(result["payment_weight"]))

    def calculate_moisture_range(self, auto=False):
        if not self.moist_net.text() or not self.moist_ded.text():
            QMessageBox.warning(self, "Missing Input", "Please enter Net Weight and Desired Deduction.")
            return
        
        net_weight = int(self.moist_net.text())
        desired_deduction = int(self.moist_ded.text())
        allowable_moisture = self.allow_group2.checkedId()

        low, high = moisture_content_range(net_weight, desired_deduction, allowable_moisture)

        self.moist_payment.setText(str(payment_weight(net_weight, desired_deduction)))
        self.moist_result.setText(f"{low: .2f} - {high: .2f}")


    # ---------------------------------------------------------
    # CLEAR BUTTONS
    # ---------------------------------------------------------
    def clear_all_fields(self):
        self.suppress_auto = True
        self.auto_toggle.setChecked(False)
        self.auto_compute_enabled = False

        self.ded_net.clear()
        self.ded_moist.clear()
        self.moist_net.clear()
        self.moist_ded.clear()
        self.ded_result.clear()
        self.ded_payment.clear()
        self.moist_result.clear()
        self.moist_payment.clear()

        self.suppress_auto = False

    def clear_deduction_fields(self):
        self.suppress_auto = True
        self.ded_net.clear()
        self.ded_moist.clear()
        self.ded_result.clear()
        self.ded_payment.clear()
        self.ded_net.setFocus()
        self.suppress_auto = False

    def clear_moisture_fields(self):
        self.suppress_auto = True
        self.moist_net.clear()
        self.moist_ded.clear()
        self.moist_payment.clear()
        self.moist_result.clear()
        self.moist_net.setFocus()
        self.suppress_auto = False


# ---------------------------------------------------------
# Run App
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
