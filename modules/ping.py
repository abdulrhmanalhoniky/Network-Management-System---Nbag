import subprocess
import platform

def execute_ping(target):
  
    if not target:
        return "[-]Error: IP address not entered. \n"

    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", target]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return stdout + "\n[✔] complete everything running.\n"
        else:
            return f"[-] Error: couldn't connect or there is something wrong happend. \n{stderr}\n"
            
    except Exception as e:
        return f"[-] Unexpected error occure.{str(e)}\n"