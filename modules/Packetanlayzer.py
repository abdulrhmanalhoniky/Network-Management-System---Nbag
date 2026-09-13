import socket
import time
from datetime import datetime

def analyze_packet_target(target, port=80, count=3):
 
    report = []
    report.append(f"[~] start packet anlayzing on: {target} on port: {port}")
    report.append(f"[~] time and date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("-" * 50)

    try:

        ip_addr = socket.gethostbyname(target)
        report.append("[✔] Targted IP address: {ip_addr}")
    except socket.gaierror:
        return f"[-] Error: DNS resolution error on: {target}"

    success_count = 0
    total_rtt = 0

    for i in range(1, count + 1):
        start_time = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        
        try:
            result = s.connect_ex((ip_addr, int(port)))
            end_time = time.time()
            rtt = (end_time - start_time) * 1000
            
            if result == 0:
                success_count += 1
                total_rtt += rtt
                report.append(f"[Packet #{i}] condation: responsed great(SYN/ACK OK) | flow time (RTT): {rtt:.2f} ms | open port")
            else:
                report.append("[Packet #{i}]Error cannot connect (Connection Refused/Filtered) | port is closed or secured")
        except socket.timeout:
            report.append(f"[Packet #{i}] Condation:(Timeout) | There is no response")
        except Exception as e:
            report.append(f"[Packet #{i}] Error in packet {str(e)}")
        finally:
            s.close()
        
        time.sleep(0.5)

    report.append("-" * 50)
    if success_count > 0:
        avg_rtt = total_rtt / success_count
        report.append(f"[✔] Analyze result: {success_count}/{count} completed: | flow time: {avg_rtt:.2f} ms")
    else:
        report.append("[-] Analyze: error didn't recive any response")

    return "\n".join(report)