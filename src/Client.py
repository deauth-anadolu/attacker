import pandas as pd

class Client:
    def __init__(self, mac, first_time_seen, last_time_seen, power):
        self.mac = mac
        self.first_time_seen = first_time_seen
        self.last_time_seen = last_time_seen
        self.power = power

    @classmethod
    def from_csv(cls, csv_file):
        clients = []

        try:
            # CSV dosyasını pandas kullanarak oku ve ilk 3 satırı atla
            df = pd.read_csv(csv_file, skiprows=3, delimiter=",")
            # Sütun isimlerinin başındaki boşluk karakterlerini sil
            df.columns = df.columns.str.strip()

            # 'Station MAC', 'First time seen', 'Last time seen', 'Power' sütunlarını içeren satırları seç
            for index, row in df.iterrows():
                if "Station MAC" in row and "First time seen" in row and "Last time seen" in row and "Power" in row:
                    mac = row["Station MAC"]
                    first_time_seen = row["First time seen"]
                    last_time_seen = row["Last time seen"]
                    power = row["Power"]
                    
                    client = cls(mac, first_time_seen, last_time_seen, power)
                    clients.append(client)
                else:
                    print("Station MAC, First time seen, Last time seen veya Power eksik bir satır atlandı.")
        except pd.errors.ParserError:
            print("Parser error occurred. Skipping problematic lines.")

        return clients