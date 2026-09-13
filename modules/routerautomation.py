from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

def connect_and_execute(device_ip, username, password, device_type="cisco_ios", port=22, command="show ip interface brief"):
    device_params = {
        'device_type': device_type,  
        'host': device_ip,
        'username': username,
        'password': password,
        'port': int(port),           
        'timeout': 10,               
    }

    try:
        connection = ConnectHandler(**device_params)
        output = connection.send_command(command)
        connection.disconnect()
        
        return f"[✔] is connected with: {device_ip} (Device_type: {device_type}):\n\n{output}\n"

    except NetmikoAuthenticationException:
        return f"[-]Error: username or password are incorrect on: {device_ip}\n"
    except NetmikoTimeoutException:
        return f"[-]Error:Time out on: {device_ip} \n"
    except Exception as e:
        return f"[-] Unexpectet Error when trying to connect {str(e)}\n"