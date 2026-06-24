import subprocess
import platform


class TIME:
    def __init__(self):
        pass
    def schedule_alarm(self,time_str, message):
        os_type = platform.system()
        if os_type == "Linux":
            cmd = f'echo "notify-send \'Alarm\' \'{message}\'" | at {time_str}'
        elif os_type == "Darwin":
            cmd = f'''osascript -e 'display notification "{message}" with title "Flux Alarm"' &'''
        elif os_type == "Windows":
            cmd = f'schtasks /create /tn "Flux_Alarm" /tr "powershell -Command \\"[System.Media.SystemSounds]::Beep.Play();\\"" /sc once /st {time_str}'
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "scheduled_for": time_str}
            else:
                return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
    