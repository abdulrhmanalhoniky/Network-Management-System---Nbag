import socket

def scan_port(target, port):
  
    try:
      
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5) 
        
        result = s.connect_ex((target, int(port))) 
        s.close()
        
        if result == 0:
            return f"[✔]port: {port} open on  {target}\n"
        else:
            return f"[-] port: {port} close on {target}\n"
            
    except socket.gaierror:
        return f"[-] Error: couldn find the website or the IP address\n"
    except Exception as e:
        return f"[-]Unknown Error: {str(e)}\n"