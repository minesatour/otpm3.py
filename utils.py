import os

def clear_logs():
    """Delete old logs"""
    if os.path.exists("data/otps_log.txt"):
        os.remove("data/otps_log.txt")

def validate_proxy():
    """Check if proxy is running"""
    try:
        import requests
        response = requests.get("http://checkip.amazonaws.com/", proxies={"http": "http://127.0.0.1:8080"})
        return response.status_code == 200
    except:
        return False
