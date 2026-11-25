import subprocess
import time
import urllib.request
import sys

print("Starting Streamlit server on port 8505...")
proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true", "--server.port=8505"])
try:
    time.sleep(6)
    req = urllib.request.urlopen("http://localhost:8505", timeout=5)
    print("HTTP Response Code:", req.getcode())
    html = req.read().decode('utf-8', errors='ignore')
    print("Page Title in HTML:", "<title>" in html.lower())
    print("Server successfully probed and running!")
finally:
    proc.terminate()
    proc.wait()
    print("Server cleanly stopped.")
