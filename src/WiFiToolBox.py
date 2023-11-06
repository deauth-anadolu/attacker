from AirTools import Airmon, Airodump, Aireplay
from ProcessHandler import SubProcess as sp


class InterfaceManager:
    @staticmethod
    def switch_to_monitor_mode(interface_name):
        return Airmon.switch_to_monitor_mode(interface_name)
    @staticmethod
    def switch_to_managed_mode(interface_name_monitor):
        return Airmon.switch_to_managed_mode(interface_name_monitor)
    
    @staticmethod
    def interface_down(name):
        return sp.interface_down(name)
    @staticmethod
    def interface_up(name):
        return sp.interface_up(name)
    
    
class Scanner:
    @staticmethod
    def detect_access_points(interface_name_monitor, fname):
        return Airodump.detect_access_points(interface_name_monitor, fname)
    @staticmethod
    def detect_clients(channel, bssid, interface_name_monitor, fname):
        return Airodump.detect_clients(channel, bssid, interface_name_monitor, fname)
    

class Dropper:
    @staticmethod
    def drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages, run_silent=False):
        return Aireplay.drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages, run_silent=False)


class Cracker:
    ...



class Operator:
    @staticmethod
    def detect_access_points(interface_name_monitor, fname):
        Scanner.detect_access_points(interface_name_monitor, fname)
    @staticmethod
    def detect_clients(channel, bssid, interface_name_monitor, fname):
        Scanner.detect_clients(channel, bssid, interface_name_monitor, fname)
    @staticmethod
    def drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages, run_silent=False):
        Dropper.drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages, run_silent=False)

    