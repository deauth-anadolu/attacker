
import pandas as pd 


class AccessPoint:
    _clients = ...
    def __init__(self, bssid, essid, channel, signal_level):
        self.bssid = bssid
        self.essid = essid
        self.channel = channel
        # signal levels are negative numbers. "-40" signal level is the highest acceptable signal level. Higher than that level (like -30) is "too strong". It should not be that strong.
        self.signal_level = signal_level
    @property
    def clients(self):
        return self._clients
    @clients.setter
    def clients(self, value):
        self._clients = value




    @classmethod
    def from_csv(cls, csv_file, sort_by_signal_level=False, sort_by_channel=False):
        if sort_by_signal_level and sort_by_channel:
            raise ValueError("sort_by_signal_level and sort_by_channel can't be active simultaneousy.")
        
        aps = []

        try:
            # CSV dosyasını pandas kullanarak oku
            df = pd.read_csv(csv_file, delimiter=";")

            # Sütunları seçerek Nesne listesi oluştur
            for index, row in df.iterrows():
                if "BSSID" in row and "ESSID" in row and "Channel" in row and "BestQuality"in row:
                    bssid = row.get("BSSID")
                    essid = row.get("ESSID")
                    channel = row.get("Channel")
                    best_signal = row.get("BestQuality")
                    
                    ap = cls(bssid, essid, int(channel), int(best_signal))
                    aps.append(ap)

                    if sort_by_signal_level:
                        aps = AccessPoint._sort_by_signal_level(aps)
                    elif sort_by_channel:
                        aps = AccessPoint._sort_by_channel(aps)
                else:
                    print("BSSID, ESSID, Channel veya BestQuality eksik bir satır atlandı.")
        except pd.errors.ParserError:
            print("Parser error occurred. Skipping problematic lines.")


        return aps
    
    
    @classmethod
    def _sort_by_signal_level(cls, aps):
        def __get_signal_level(ap):
            return ap.signal_level
        
        return sorted(aps, reverse=True, key=__get_signal_level)
    
    @classmethod
    def _sort_by_channel(cls, aps):
        def __get_channel(ap):
            return ap.channel
        
        return sorted(aps, reverse=True, key=__get_channel)

        