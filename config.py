# ===============================
# Configuration File (config.py)
# ===============================

# ---------- Proxy Settings ----------
PROXY_ENABLED = True  # Set to False to disable proxy
PROXY_ADDRESS = "http://127.0.0.1"  # Change this to your proxy server
PROXY_PORT = 8080
PROXY_MODE = "transparent"  # Options: "transparent", "anonymous", "elite"

# ---------- User-Agent (Mimic Real Browser) ----------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

# ---------- Logging Configuration ----------
LOG_FILE = "data/otps_log.txt"  # Log file for captured OTPs
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"

# ---------- Database Settings ----------
DB_FILE = "data/captured_otps.db"  # SQLite database file

# ---------- OTP Capture Keywords ----------
OTP_KEYWORDS = [
    "OTP", "One-Time Password", "Verification Code", "Auth Code",
    "Security Code", "Login Code", "2FA Code", "Authentication Code",
    "Access Code", "PIN Code", "SMS Code", "Verification PIN"
]

# ---------- Advanced Security Settings ----------
ENCRYPT_OTP_STORAGE = True  # Enable AES-256 encryption for OTP storage
AUTO_DELETE_OLD_OTPS = True  # Automatically delete OTPs after a set time
OTP_EXPIRY_TIME = 300  # Time in seconds before OTPs auto-delete (if enabled)

# ---------- QR Code Sharing (Optional) ----------
ENABLE_QR_CODE = False  # Set to True to enable QR code generation for OTPs

# ---------- GUI Settings ----------
GUI_THEME = "dark"  # Options: "light", "dark"
