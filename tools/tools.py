import subprocess
import sys,pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from settings.config import forbidden_commands
import os
class tools:
    def __init__(self):
        pass
    def send_notification(self,title, message):
        os_type = os.uname().sysname
        if os_type == "Darwin":
            cmd = f'osascript -e \'display notification "{message}" with title "{title}"\''
        elif os_type == "Linux":
            cmd = f'notify-send "{title}" "{message}"'
        elif os_type == "Windows":
            cmd = f'powershell -Command "Add-Type –AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show(\'{message}\', \'{title}\')"'
        else:
            return {"error": f"Unsupported OS: {os_type}"}
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return {"success": True, "title": title, "message": message}
        except Exception as e:
            return {"error": str(e)}