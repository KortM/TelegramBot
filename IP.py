import ipaddress
import bs4
import csv
import requests
from pymongo import MongoClient


class IP_interface:
    def __init__(self):
        self.client = MongoClient('mongodb://kort:mar02031812@localhost:27017/')
        #self.client = MongoClient('mongodb+srv://kort:mar02031812@cluster0.nlzma.mongodb.net/bot_data?retryWrites=true&w=majority')

    def calc_ip(self, ip) -> str:
        '''Метод расчета ip по маске подсети'''
        try:
            #ip_list = list(ipaddress.ip_network(ip, False).hosts())
            args = ip.split('/')
            address = args[0]
            min_host = ipaddress.ip_network(ip, False)[1]
            broadcast = ipaddress.ip_network(ip, False).broadcast_address
            max = str(broadcast).split('.')
            max_host = "{}.{}.{}.{}".format(
                max[0], max[1], max[2], int(max[3]) - 1)
            wildcard = ipaddress.ip_network(ip, False).hostmask
            hosts = ipaddress.ip_network(ip, False).num_addresses - 2
            network = ipaddress.ip_network(ip, False).exploded
            mask = ipaddress.ip_network(ip, False).netmask
            private = ipaddress.ip_network(ip, False).is_private
            print(min_host, max_host, broadcast,
                  wildcard, hosts, mask, private, network)
            return {"Address": str(address), "Netmask": str(mask), "Wildcard": str(wildcard), "Network": str(network),
                    "Broadcast": str(broadcast), "HostMin": str(min_host), "HostMax": str(max_host), "Hosts/Net": str(hosts),
                    "Private": str(private)}
        except Exception:
            return None

    def update_mac_data(self):
        db = self.client['bot_data']
        try:
            db.mac_data.drop()
        except Exception:
            print("Error delete mac_data")
        with requests.get('http://standards-oui.ieee.org/oui/oui.csv', stream=True) as result:
            result.raise_for_status()
            with open('src/mac-data.csv', 'wb') as f:
                for line in result.iter_content(chunk_size=8192):
                    f.write(line)
            print('Success load and write mac data')
        print('Write in db')
        with open('src/mac-data.csv', 'r') as f:
            reader = csv.DictReader(f, 'utf8')
            for line in reader:
                db.mac_data.insert(
                    {
                        'Assignment': line['t'], 
                        'Organization Name': line['f'],
                        'Organization Address': line['8']
                    })
                
            print('Done write to db')

    def get_mac(self, value: str) -> str or None:
        print(value)
        result = self.client.bot_data.mac_data.find({"Assignment": value})
        data =[
            
            f'Organization Name:\n{i["Organization Name"]}\nOrganization Address:\n{i["Organization Address"]}' for i in result]
        print(data)
        return ''.join(data) if data else None

    def test_update_many(self):
        db = self.client.mac_data
        db.mac_data.update_one('')
if __name__ == '__main__':
    #print(calc_ip("2.2.2.2/5"))
    ip = IP_interface()
    ip.update_mac_data()
    print(ip.get_mac('5C415A'))
