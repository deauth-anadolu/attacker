from ProcessHandler import SubProcess as sp
import argparse
import os

CRED = '\033[41m'
CEND = '\033[0m'

text = f"""                     ▄▀░░▌
                   ▄▀▐░░░▌
                ▄▀▀▒▐▒░░░▌
     ▄▀▀▄   ▄▄▀▀▒▒▒▒▌▒▒░░▌
    ▐▒░░░▀▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒█
    ▌▒░░░░▒▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
   ▐▒░░░░░▒▒▒▒▒▒▒▒▒▌▒▐▒▒▒▒▒▀▄
    ▌▀▄░░▒▒▒▒▒▒▒▒▐▒▒▒▌▒▌▒▄▄▒▒▐
   ▌▌▒▒▀▒▒▒▒▒▒▒▒▒▒▐▒▒▒▒▒█▄█▌▒▒▌
 ▄▀▒▐▒▒▒▒▒▒▒▒▒▒▒▄▀█▌▒▒▒▒▒▀▀▒▒▐░░░▄
▀▒▒▒▒▌▒▒▒▒▒▒▒▄▒▐███▌▄▒▒▒▒▒▒▒▄▀▀▀▀
▒▒▒▒▒▐▒▒▒▒▒▄▀▒▒▒▀▀▀▒▒▒▒▄█▀░░▒▌▀▀▄▄
▒▒▒▒▒▒█▒▄▄▀▒▒▒▒▒▒▒▒▒▒▒░░▐▒▀▄▀▄░░░░▀
▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▄▒▒▒▒▄▀▒▒▒▌░░▀▄
▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▀▀▀▀▒▒▒▄▀     ▂▃▅▇█▓▒░۩۞۩ jammerDEAUTHway ۩۞۩░▒▓█▇▅▃▂"""
print(text)
print("\nHi jumppy :>\n\n")

def output_standart(func):
    def inner(*args, **kwargs):
        print(100 * "_" + "\n")
        # getting the returned value
        returned_value = func(*args, **kwargs)
        print(100 * "_" + "\n")
        # returning the value to the original frame
        return returned_value
         
    return inner

def is_package_installed(*args):
    counter = 0
    for package_name in args:
        _, which_output = sp.which(package_name)
        if not _:
            print(f"[+] {package_name} is installed!")
            counter += 1
        else:
            print(f"[-] {package_name} is NOT installed! {which_output.stdout}")
    if counter == len(args):
        return True
    else:
        return False
    


def get_user_input():
    parser = argparse.ArgumentParser(description="Tool description here")

    parser.add_argument("-t", "--target", dest="targetname", type=str, help="Specific target name to be attacked. If 'all', do NOT use this parameter.")
    parser.add_argument("-n", "--number", dest="number_of_packages", type=int, default=0, help="How many packages will be sent to the target(s). Default is 0 (unlimited).")
    parser.add_argument("-m", "--mac", dest="mac_address", type=str, help="Temporary new MAC address.")
    parser.add_argument("-q", "--quality", dest="quality_of_the_attack", type=int, default=1, choices=range(1, 21), help="Enter a number between 1 and 20. The higher the number, the higher the quality of the attack as well as the time taken. Default is 1.")

    return parser.parse_args()



def initialize(iface):
    # if not is_package_installed("airmon-ng", "xterm"): exit()
    # iface.change_mac_address()
    iface.switch_to_monitor_mode()

@output_standart
def list_avliable_aps(detected_aps):
    print("\n\nAvaliable access points to attack: ")
    print("ESSID\t\t\t\t\tBSSID\t\t\t\t\tChannel\t\t\t\t\tSignal Level")
    print(140 * "_")
    for ap in detected_aps:
        print(f"{ap.essid}\t\t\t\t\t{ap.bssid}\t\t\t\t\t{ap.channel}\t\t\t\t\t{ap.signal_level}")

@output_standart
def choose_target_ap(detected_aps):
    target_bssid = input("Choose target BSSID (Default = all targets):")
    if target_bssid != "":
        detected_aps = [ap for ap in detected_aps if ap.bssid == target_bssid]

    return detected_aps

@output_standart
def show_available_clients(ap, iface):
    print("\n\nAvaliable clients are detected: ")
    for client in ap.clients:
        print(f"MAC: {client.mac}\tESSID: {ap.essid}\tBSSID: {ap.bssid}\t{iface.name}")

def create_scan_folder(now):
    fname = f"../scans/{now}/"
    os.system(f"mkdir -m 0777 -p {fname}")
    return fname + "APs"


