import subprocess
import sys,pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from settings.config import forbidden_commands
import os
class tools:
    def __init__(self):
        pass
    def execute_bash(self,command):
        for cmd in forbidden_commands:
            if command.split()[0] in forbidden_commands:
                return {"error": f"Command {command} is forbidden."}
            
        try:
            output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return {"output": output.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {"error": f"Command {command} failed with an error: {e.stderr}"}
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

# Test it
print(tools().send_notification("Flux", "Task completed!"))