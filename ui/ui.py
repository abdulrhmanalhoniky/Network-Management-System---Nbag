import customtkinter as ctk
from modules.ping import execute_ping
from modules.port_scanner import scan_port
from modules.routerautomation import connect_and_execute
from modules.Packetanlayzer import analyze_packet_target

class gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nbag")
        self.geometry("800x500")

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")
        
        self.btn_ping = self.create_sidebar_button("PingCheck", self.run_ping)
        self.btn_netmiko = self.create_sidebar_button("Router Automation", self.run_netmiko)
        self.btn_netmiko = self.create_sidebar_button("PortScanner", self.run_socket)
        self.btn_netmiko = self.create_sidebar_button("PacketAnalyzer", self.run_scappy)

        self.logs_box = ctk.CTkTextbox(self, width=550, height=440, corner_radius=8)
        self.logs_box.pack(side="right", padx=20, pady=20, fill="both", expand=True)
        
        self.logs_box.insert("end", "[*] Wlecome to Nbag network administrat System \n[*] System is ready for your commands\n")
    def create_sidebar_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            command=command,
            width=160, 
            height=40, 
            corner_radius=8
        )
        btn.pack(padx=10, pady=10)
        return btn
    
    def append_log(self, text, is_error=False):

        self.logs_box.tag_config("error_tag", foreground="red") 
        self.logs_box.tag_config("success_tag", foreground="green") 

        if is_error or text.startswith("[-]"):
            self.logs_box.insert("end", text, "error_tag")
        elif text.startswith("[✔]") or text.startswith("[+]"):
            self.logs_box.insert("end", text, "success_tag")
        else:
            self.logs_box.insert("end", text)
            
        self.logs_box.see("end")

    def run_ping(self):
       
        dialog = ctk.CTkInputDialog(text="Enter the IP address", title="Ping Tool")
        target = dialog.get_input()
        
        if not target:
            return

        self.logs_box.insert("end", f"\n[+] Checking The: {target}...\n")
        self.update()
      
        result = execute_ping(target)
        
        self.append_log(result)

        self.logs_box.see("end")

    def run_netmiko(self):
   
        dialog_ip = ctk.CTkInputDialog(text="Enter the router IP", title="Router Automation")
        device_ip = dialog_ip.get_input()
        if not device_ip:
            return

        dialog_user = ctk.CTkInputDialog(text="Enter the (Username):", title="Router Automation")
        username = dialog_user.get_input()
        if not username:
            return

        dialog_pass = ctk.CTkInputDialog(text="Enter the (Password):", title="Router Automation")
        password = dialog_pass.get_input()
        if not password:
            return

        dialog_type = ctk.CTkInputDialog(text="Enter the device type(EX: cisco_ios, juniper_junos):", title="Router Automation")
        user_device_type = dialog_type.get_input()
        
        device_type = user_device_type.strip() if user_device_type else "cisco_ios"
     
        dialog_port = ctk.CTkInputDialog(text="Enter the SSH port (deafult is 22):", title="Router Automation")
        port_str = dialog_port.get_input()
        port = int(port_str) if port_str and port_str.isdigit() else 22

        self.logs_box.insert("end", f"\n[+] Connecting to: {device_ip} type: ({device_type}) port: {port}...\n")
        self.update()

        result = connect_and_execute(
            device_ip=device_ip, 
            username=username, 
            password=password, 
            device_type=device_type, 
            port=port,
            command="show ip interface brief"
        )
        
        self.append_log(result)

    def run_socket(self):
       
        dialog_target = ctk.CTkInputDialog(text="Enter the IP address or the website URL(EX:www.google.com)", title="Port Scanner")
        target = dialog_target.get_input()
        if not target:
            return
    
        dialog_port = ctk.CTkInputDialog(text="Enter the port you want to check(EX:443,80)", title="Port Scanner")
        port_str = dialog_port.get_input()
        if not port_str or not port_str.isdigit():
            self.logs_box.insert("end", "[-] Error you must Enter correct port.\n")
            return

        self.logs_box.insert("end", f"\n[+] Checking port:{port_str} on: {target}...\n")
        self.update()

        result = scan_port(target, int(port_str))
    
        self.append_log(result)
        self.logs_box.see("end")

    def run_scappy(self):

        dialog_target = ctk.CTkInputDialog(text="Enter the target's: (IP or domain EX:www.google.com):", title="Packet Analyzer")
        target = dialog_target.get_input()
        if not target:
            return

        dialog_port = ctk.CTkInputDialog(text="Enter the port: (defualt is 80)", title="Packet Analyzer")
        port_str = dialog_port.get_input()
        port = int(port_str) if port_str and port_str.isdigit() else 80

        self.logs_box.insert("end", f"\n[+] Runing the packet analyzer: {target}:{port}...\n")
        self.update()
  
        result = analyze_packet_target(target=target, port=port, count=3)
        
        self.append_log(result)