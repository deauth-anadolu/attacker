from WiFiToolBox import InterfaceManager as IM
from ProcessHandler import SubProcess as sp
import time, re


class Interface:
    _name: str
    _mode: str

    @property
    def name(self):
        _, output = sp.get_interface_output()
        interface_name = output.split("\n")[0]  # Searching for interface name
        interface_name = interface_name[11:]  # Getting the name only
        return str(interface_name)
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def mode(self):
        _, output = sp.get_interface_mode_output()
        type_of_card = output.split("\n")[0]
        type_of_card = type_of_card[7:]
        print("--> Network Adapter Mode: ", type_of_card)

        return type_of_card
    @mode.setter
    def mode(self, value):
        self._mode = value

    def down(self):
        return IM.interface_down(self.name)
    def up(self):
        return IM.interface_up(self.name)
    
    def switch_to_monitor_mode(self):
        if not self.is_monitor():
            return IM.switch_to_monitor_mode(self.name)

    def switch_to_managed_mode(self):
        if self.is_monitor():
            return IM.switch_to_managed_mode(self.name)

    def is_monitor(self):
        if self.mode == 'monitor':
            return True
        elif self.mode == 'managed':
            print("\nYou may want to change the mode of your WiFi card manually.")
            return False
        
    def change_mac_address(self, mac_address):
        if self.is_monitor():
            self.switch_to_managed_mode()
            time.sleep(3)
        self.down()
        time.sleep(1)
        sp.change_mac_address(mac_address)
        time.sleep(1)
        self.up()
        time.sleep(3)


    def control_new_mac(interface_name):
        ifconfig = sp.interface_info()
        new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
        if new_mac:
            return new_mac.group(0)
        else:
            return None

