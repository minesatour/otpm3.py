import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton

class OTPDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Captured OTPs")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Captured OTP Codes:")
        self.layout.addWidget(self.label)

        self.otp_list = QListWidget()
        self.layout.addWidget(self.otp_list)

        self.refresh_btn = QPushButton("Refresh OTPs")
        self.refresh_btn.clicked.connect(self.load_otps)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_otps()

    def load_otps(self):
        """Fetch OTPs from database and display them"""
        self.otp_list.clear()
        conn = sqlite3.connect("data/captured_otps.db")
        cursor = conn.cursor()
        cursor.execute("SELECT otp FROM otps ORDER BY id DESC LIMIT 10")
        otps = cursor.fetchall()
        conn.close()
        for otp in otps:
            self.otp_list.addItem(otp[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OTPDisplay()
    window.show()
    sys.exit(app.exec())
