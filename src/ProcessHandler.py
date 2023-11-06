import os
import subprocess as sp

class DefaultTerminal:
    @staticmethod
    def run_command(command):
        try:
            result = os.system(command)
            if result == 0:
                return True, "Command executed successfully."
            else:
                return False, f"Command failed with return code {result}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def airmon_start(interface_name):
        command = f"airmon-ng start {interface_name}"
        return DefaultTerminal.run_command(command)

    @staticmethod
    def airmon_stop(interface_name_monitor):
        command = f"airmon-ng stop {interface_name_monitor}"
        return DefaultTerminal.run_command(command)

    @staticmethod
    def remove_files(files_path):
        command = f"rm -rf {files_path}"
        return DefaultTerminal.run_command(command)



class XtermTerminal:
    @staticmethod
    def run_command(command, timeout=True):
        _timeout = ""
        if timeout: _timeout = "timeout -s 9 10"
        try:
            xterm_command = f"xterm -e {_timeout} {command}"
            result = os.system(xterm_command)
            if result == 0:
                return True, f"Executed successfully:\n{command}"
            else:
                return False, f"Failed with return code {result}:\n{command}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def detect_access_points(interface_name_monitor: str, fname: str):
        command = f"airodump-ng -w {fname} --output-format kismet.csv {interface_name_monitor}"
        return XtermTerminal.run_command(command)

    @staticmethod
    def detect_clients(channel: int, bssid: str, interface_name_monitor: str, fname: str):
        command = f"airodump-ng -c {channel} --bssid {bssid} -w {fname} --output-format csv {interface_name_monitor}"
        return XtermTerminal.run_command(command)

    @staticmethod
    def drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages):
        command = f"aireplay-ng --deauth {number_of_packages} -a {ap_bssid} -c {client_mac} --ignore-negative-one {interface_name_monitor}"
        return XtermTerminal.run_command(command, timeout=False)


class SubProcess:
    @staticmethod
    def run_command(command):
        try:
            result = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True, text=True)
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
        
    @staticmethod
    def which(package_name):
        command = ['which', package_name]
        return SubProcess.run_command(command)

    @staticmethod
    def interface_down(interface_name):
        command = ["ifconfig", interface_name, "down"]
        return SubProcess.run_command(command)

    @staticmethod
    def interface_up(interface_name):
        command = ["ifconfig", interface_name, "up"]
        return SubProcess.run_command(command)

    @staticmethod
    def change_mac_address(interface_name, mac_address):
        command = ["ifconfig", interface_name, "hw", "ether", mac_address]
        return SubProcess.run_command(command)

    @staticmethod
    def interface_info(interface_name):
        command = ["ifconfig", interface_name]
        return SubProcess.run_command(command)

    @staticmethod
    def get_interface_output():
        command = "iw dev | grep Interface"
        return SubProcess.run_command(command)

    @staticmethod
    def get_interface_mode_output():
        command = "iw dev | grep type"
        return SubProcess.run_command(command)
    
    @staticmethod
    def drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages):
        command = f"aireplay-ng --deauth {number_of_packages} -a {ap_bssid} -c {client_mac} --ignore-negative-one {interface_name_monitor}"
        return SubProcess.run_command(command)