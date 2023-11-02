from ProcessHandler import XtermTerminal as xt, DefaultTerminal as dt


class Airmon:
    @staticmethod
    def switch_to_monitor_mode(interface_name):
        return dt.airmon_start(interface_name)
    @staticmethod
    def switch_to_managed_mode(interface_name_monitor):
        return dt.airmon_stop(interface_name_monitor)

class Airodump:
    @staticmethod
    def detect_access_points(interface_name_monitor, fname):
        return xt.detect_access_points(interface_name_monitor, fname)
    @staticmethod
    def detect_clients(channel, bssid, interface_name_monitor, fname):
        return xt.detect_clients(channel, bssid, interface_name_monitor, fname)


class Aireplay:
    @staticmethod
    def drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages):
        return xt.drop_client(client_mac, ap_bssid, interface_name_monitor, number_of_packages)

