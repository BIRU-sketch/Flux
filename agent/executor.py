import sys,pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from tools.tools import tools
from tools.time_tools import TIME
from settings.config import forbidden_commands
from tools.media_automation import EmailSender
class execute:
    def __init__ (self):
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
    def execute_tool(self,tool_name,array_of_arguments):
        """ maximum number of arguments is 3"""
        args = array_of_arguments
        if tool_name == "schedule_alarm":
            try:
                time = args[0]
                message=args[1]
                tool=TIME()
                result = tool.schedule_alarm(time,message)
                return result
            except Exception as e:
                return {'Error': str(e)}
        elif tool_name == "send_notification":
            try:
                title = args[0]
                message = args[1]
                tool= tools()
                result = tool.send_notification(title,message)
                return result
            except Exception as e:
                return {'Error': str(e)}
        elif tool_name == "send_email":
            try:
                to=args[0]
                msg=args[1]
                subject= args[2] or "Flux Automation"
                tool = EmailSender()
                result = tool.send_email(to,msg,subject)
                return result
            except Exception as e:
                return {'Error': str(e)}
        elif tool_name == "send_email_with_atachment":
            try:
                to=args[0]
                msg=args[1]
                attachment_path=args[2]
                subject=args[3] or "Flux Automation"
                tool = EmailSender()
                result = tool.send_email_with_attachment(to,msg,attachment_path,subject)
                return result
            except Exception as e:
                return {'Error': str(e)}
        
shi=execute()
print(shi.execute_tool('schedule_alarm',['17:54','hehehe']))