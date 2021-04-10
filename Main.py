from ipwhois import IPWhois
from IP import IP_interface
from Telephony import Telephony_Interface
from Ports import get_port
import schedule
import time
import threading
import re


class Worker():
    def __init__(self):
        self.ip = IP_interface()
        self.telephony = Telephony_Interface()
        self.start_upgrade_controll()

    def search_ip_addr(self, ip):
        try:
            obj = IPWhois(ip)
            results = obj.lookup_whois()
            if results:
                return ''.join([f'{k}: {v}\n'.title() for k, v in results['nets'][0].items()])
        except:
            return 'No information was found for your request. Change the request and try again!'

    def handle_telephone(self, number: str):
        complete_searching = ''
        tmp = re.findall(r'(?:\+|\d)[\d\-\(\) ]{10,}', number)
        if tmp:
            tmp = re.split(r'[\-\(\)]', tmp[0])
            if len(tmp) == 1:
                if tmp[0][:2] != '+7':
                    complete_searching = self.telephony.find_international_number(tmp[0][1:])
                if tmp[0][:2] == '+7':
                    complete_searching = self.telephony.get_telephony_info(
                        tmp[0][2:5], int(tmp[0][5:]))
                if tmp[0][:1] == '8':
                    found = self.telephony.get_telephony_info(
                        tmp[0][1:4], int(tmp[0][4:]))
                    complete_searching = found if found else self.telephony.find_international_number(
                        tmp[0][1:])
                if tmp[0][:3] == '810':
                    complete_searching = self.telephony.find_international_number(
                        tmp[0][3:])
                if tmp[0][:4] == '+810':
                    complete_searching = self.telephony.find_international_number(
                        tmp[0][4:])
            
            if len(tmp) == 3:
                complete_searching = self.telephony.get_telephony_info(
                    tmp[1], int(tmp[2]))
            if len(tmp) == 6:
                complete_searching = self.telephony.get_telephony_info(
                    tmp[1], int(''.join(tmp[3:])))
            if len(tmp) == 7:
                complete_searching = self.telephony.get_telephony_info(
                    tmp[2], int(''.join(tmp[4:])))
        
        print(complete_searching)
        tmp = re.findall(r'(?:\+|\d){7,}', number)
        if tmp and not complete_searching:
            complete_searching =self.telephony.get_telephony_info('812', int(tmp[0]))
            
        return complete_searching if complete_searching else 'No information was found for your request. Change the request and try again!'

    def get_ip(self, ip) -> str:
        """Метод форматирующий и возвращающий ip """
        result = self.ip.calc_ip(ip)
        format_result = ""
        if result:
            for k, v in result.items():
                format_result = format_result + k+": "+v + '\n'
            return format_result
        else:
            return 'No information was found for your request. Change the request and try again!'

    def get_port(self, port):
        result = get_port(port)
        if result:
            return result
        else:
            return None

    def handle_mac(self, value):
        res = re.findall(
            r'[0-9a-fA-F]{2}(?:[.:-][0-9a-fA-F]{2}){5}|[0-9a-fA-F]{12}|[0-9a-fA-F]{4}(?:[.:-][0-9a-fA-F]{4}){2}', value)
        print(res)
        if res:
            print(self.ip.get_mac(''.join(re.split(r'[.:-]', res[0])).upper()[:6]))
            result = self.ip.get_mac(''.join(re.split(r'[.:-]', res[0])).upper()[:6])
            if result:
                return result
            else: return 'No information was found for your request. Change the request and try again!'
        else:
            return 'No information was found for your request. Change the request and try again!'

    def start_upgrade_controll(self):
        thread = threading.Thread(target=self.auto_upgrade, args=())
        thread.start()
        new_thread = threading.Thread(target=self.upgrade_task, args=())
        new_thread.start()
        
    def upgrade_task(self):
        try:
            self.telephony.update_internation_numbers()
            self.telephony.update_country()
            self.ip.update_mac_data()
        except Exception:
            print('Failed update mac-data. Try later')
        try:
            self.telephony.update_tel_db()
            
        except Exception:
            print('Failed update telephony data. Try later.')
        
        print('Update complete')
    
    def auto_upgrade(self):
        schedule.every().saturday.at('00:00').do(self.upgrade_task)
        print('Task is config')
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    u = Worker()
    '''u.handle_telephone('+79506628028')
    print(u.handle_telephone('88127407070'))
    print(u.handle_telephone('89506628028'))
    print(u.handle_telephone('+7(950)6628028'))
    print(u.handle_telephone('+7 (950) 6628028'))
    print(u.handle_telephone('+7-(950)-662-80-28'))
    print(u.handle_telephone('+7(950)-662-80-28'))
    print(u.handle_telephone('810333221112123'))
    print(u.handle_telephone('+810333221112123'))'''
    #print(u.handle_telephone('7407070'))
    #print(u.handle_telephone('740-70-70'))
    print(u.handle_telephone('88127407070'))

    # u.search_tel_number()
    # print(u.get_ip('192.167.1.1/30'))
    # print(u.search_ip_addr('81.23.23.1'))
    # print(u.handle_mac('ec086b173e2f'))
    # print(u.handle_mac('ec08.6b17.3e2f'))
    print(u.handle_mac('ec:08:6b:17:3e:2f'))
    # print(u.handle_mac('ec-08-6b-17-3e-2f'))
    # print(u.search_tel_number("8108124472309"))
    # u.load_in_csv()
    # u.load_data()
    # print(u.splitStr('ec08.6b17.3e2f'))
    # print(u.splitStr('00.1A.4B.00.00.00'))
    # print(u.splitStr('83.4.97.67'))
    # print(u.splitStr('D4:9E:6D:D0:02:01'))

    # print(u.splitStr('D4.9E.6D.D0.02.01'))
    # print(u.splitStr('D49E.6DD0.0201'))
    # print(u.splitStr('D4-9E-6D-D0-02-01'))
    # print(u.splitStr('D4 9E 6D D0 02 01'))
    # print(u.splitStr('D49E6DD00201'))
    # print(u.search_ip_addr('5.144.97.67'))
