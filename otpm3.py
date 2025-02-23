import json
import re
import sqlite3
import threading
import time
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium_stealth import stealth
from PIL import Image
import pytesseract
import requests

# CONFIGURATIONS
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
OTP_STORAGE_FILE = "captured_otps.db"
ALLOWED_SITES_FILE = "allowed_sites.txt"
OTP_EXPIRY_HOURS = 24

# OTP Detection Patterns
OTP_PATTERNS = [r"\b\d{6}\b", r"\b[A-Z0-9]{8}\b"]
OTP_KEYWORDS = [ "Your OTP is", "Enter this code", "Verification code",
    "Security code", "2FA code", "One-time password",
    "Login code", "Confirm your identity", "Authenticate with this code"
    "OTP", "One-Time Password", "Verification Code", "Auth Code", "Secure Code", "Passcode",
    "Your verification code", "Your login code", "Enter your code", "Use this code",
    "Transaction Code", "Bank Code", "Security Code", "Payment Code", "Card Code", "Deposit Code",
    "Email Verification Code", "Account Code", "Login Code", "Confirmation Code", "Identity Code",
    "Reset Password Code", "Password Recovery Code", "Security Alert Code",
    "Instagram Code", "Facebook Code", "WhatsApp Code", "Telegram Code", "Google Code", "Apple ID Code",
    "Amazon OTP", "eBay Code", "Shopify Code", "Order Verification", "Delivery Confirmation Code",
    "Two-Factor Authentication", "2FA Code", "Authenticator Code", "Login Confirmation",
    "SIM Activation Code", "Phone Verification", "Carrier Code", "Mobile Code" ]

    
# Proxy API Configuration
PROXY_API_URL = "https://proxyprovider.com/api/get_proxy"

# SETUP DATABASE
def setup_database():
    conn = sqlite3.connect(OTP_STORAGE_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY, 
            otp TEXT, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# STORE OTP IN DATABASE
def store_otp(otp):
    conn = sqlite3.connect(OTP_STORAGE_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO otps (otp) VALUES (?)", (otp,))
    conn.commit()
    conn.close()

# CLEANUP OLD OTPs
def cleanup_otps():
    conn = sqlite3.connect(OTP_STORAGE_FILE)
    c = conn.cursor()
    c.execute(f"DELETE FROM otps WHERE timestamp < datetime('now', '-{OTP_EXPIRY_HOURS} hours')")
    conn.commit()
    conn.close()

# GUI TO DISPLAY OTP
class OTPGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Captured OTP")
        self.master.geometry("350x250")
        self.master.configure(bg="#121212")
        self.otp_label = tk.Label(master, text="Waiting for OTP...", font=("Arial", 12), fg="white", bg="#121212")
        self.otp_label.pack(pady=20)

        self.capture_button = tk.Button(master, text="Start OTP Capture", command=self.start_capturing, bg="#1E90FF", fg="white")
        self.capture_button.pack(pady=10)
        
        self.stop_button = tk.Button(master, text="Stop OTP Capture", command=self.stop_capturing, bg="#FF4500", fg="white")
        self.stop_button.pack(pady=10)

        self.capturing = False

    def start_capturing(self):
        self.capturing = True
        self.otp_label.config(text="Capturing OTP...", fg="yellow")

    def stop_capturing(self):
        self.capturing = False
        self.otp_label.config(text="Stopped", fg="red")

    def update_otp(self, otp):
        store_otp(otp)
        self.otp_label.config(text=f"Captured OTP: {otp}", fg="green")
        messagebox.showinfo("OTP Captured", f"OTP: {otp}")

# PROXY HANDLING
def get_proxy():
    try:
        response = requests.get(PROXY_API_URL)
        proxy_data = response.json()
        return proxy_data.get("proxy")
    except Exception as e:
        print(f"⚠ Proxy Fetch Error: {e}")
        return None

# CHROME DRIVER SETUP
def launch_chrome(target_url, use_proxy=False):
    chrome_options = ChromeOptions()
    chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")

    if use_proxy:
        proxy = get_proxy()
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")
            print(f"🌐 Using Proxy: {proxy}")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.get(target_url)
    return driver

# LOAD ALLOWED SITES
def load_allowed_sites():
    try:
        with open(ALLOWED_SITES_FILE, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Allowed sites file not found. Please create 'allowed_sites.txt'.")
        return []

# OTP INTERCEPTION
def intercept_otp(driver, gui, allowed_sites):
    while gui.capturing:
        time.sleep(random.uniform(2, 5))
        try:
            if any(site in driver.current_url for site in allowed_sites):
                page_source = driver.page_source
                for pattern in OTP_PATTERNS:
                    otp_candidates = re.findall(pattern, page_source)
                    for otp in otp_candidates:
                        if any(keyword in page_source for keyword in OTP_KEYWORDS):
                            gui.update_otp(otp)
                            print(f"✅ Captured OTP: {otp}")
                            return
        except Exception as e:
            print(f"⚠ OTP Interception Error: {e}")

# MENU
def menu():
    print("1. Run with Proxy")
    print("2. Run without Proxy")
    choice = input("Choose an option: ")
    return choice == "1"

# MAIN FUNCTION
def main():
    setup_database()
    cleanup_otps()
    use_proxy = menu()

    root = tk.Tk()
    gui = OTPGUI(root)

    allowed_sites = load_allowed_sites()
    target_url = simpledialog.askstring("Target Website", "Enter the OTP website URL:")

    driver = launch_chrome(target_url, use_proxy)
    intercept_thread = threading.Thread(target=intercept_otp, args=(driver, gui, allowed_sites))
    intercept_thread.daemon = True
    intercept_thread.start()

    root.mainloop()
    driver.quit()

if __name__ == "__main__":
    main()
