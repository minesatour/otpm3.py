from mitmproxy.tools.main import mitmweb
import subprocess

def start_proxy():
    """Start the mitmproxy in transparent mode"""
    subprocess.Popen(["mitmweb", "--mode", "transparent", "--web-port", "8081"])

def stop_proxy():
    """Kill all mitmproxy instances"""
    subprocess.run(["pkill", "-f", "mitmweb"])

