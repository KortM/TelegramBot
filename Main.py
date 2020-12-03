from urllib import request
from Config import Session, Mac, Country, RussianNubmers, CountryCode
import csv, bs4
import urllib3, json
from ipwhois import IPWhois
from IP import calc_ip
import re

class Worker():
    def __init__(self):
        self.s = Session()

    def load_in_csv(self):
        f = open("Chapter_4.csv", encoding="cp1251")
        reader = csv.DictReader(f, "cp1251")
        code = ''
        start_number = ''
        end = ''
        cap = ''
        operator = ''
        region = ''
        for line in reader:
            try:
                sp = line["c"]
                split_line = str(sp).split(';')
                print(split_line)
                code = split_line[0]
                start_number = split_line[1]
                end = split_line[2]
                cap = split_line[3]
                operator = split_line[4]
                region = split_line[5]
                self.update_telephone_number(code, start_number, end, cap, operator, region)
            except:
                region = ''
                self.update_telephone_number(code, start_number, end, cap, operator, region)
            region = ''

    def search_ip_addr(self, ip:str) -> str:
        try:
            obj = IPWhois(ip)
            results = obj.lookup_whois()
            data = []
            [data.append(f'{key}: {value}\n'.title()) for key, value in results['nets'][0].items()]
            return ''.join(data)
        except:
            return 'Unfortunately, no information was found. You may have entered an incorrect ip address.'

    def claculate_ip(self, ip:str)-> str:
        res = calc_ip(ip)
        if res:
            tmp = [f'{k}:{v}\n'for k,v in res.items()]
            return ''.join(tmp)
        else:
            return 'Failed to calculate the number of hosts. \n' \
            'Please make sure that the ip address and prefix are entered correctly.'

    def search_mac_info(self, value:str) -> str:
        res = re.findall(r'[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5}|(?:[0-9a-fA-F]{12})|(?:[0-9a-fA-F]{4}(?:[.:-][0-9a-fA-F]{4}){2})', value)
        if res:
            res = ''.join(re.split(r'[.:-]',res[0]))
            
        else: return 'Invalid Mac address!'


    def search_tel_number(self, number):
        prefix = number[0:1]
        p_out_number = ''
        if prefix == '+':
            p_out_number = number[1:]
            return str(self.find_code(p_out_number))
        new_prefix = number[0:3]
        if new_prefix == '810':
            p_out_number = number[3:]
            return str(self.find_code(p_out_number))
        if prefix == '8':
            p_out_number = number[1:]
            return str(self.find_operator_code(p_out_number))



    def find_code(self, p_out_number):
        count = 0
        result = ''
        while count <= len(p_out_number):
            i = p_out_number[:count]
            if i == str(7):
                return self.find_operator_code(p_out_number[count:])
            n = self.s.query(CountryCode).filter_by(code=i).first()
            if n is not None:
                result = n
            count = count + 1
        return "Код: "+str(result.code)+'\n' + "Страна: "+str(result.country)

    def find_operator_code(self, number):
        count = 0
        find_count = 0
        code = ''
        start_number = ''
        end_number = ''
        cap = ''
        operator = ''
        region = ''
        country = "Россия"
        while count <= 3:
            i = number[:count]
            n = self.s.query(RussianNubmers).filter_by(code=str(i)).all()
            if n is not None:
                for a in n:
                    start = number[count:]
                    if int(start) >= a.start_number and int(start) <= a.end_number:
                        code = a.code
                        start_number = a.start_number
                        end_number = a.end_number
                        cap = a.cap
                        operator = a.operator
                        region = a.region
                        find_count = find_count + 1
            count = count + 1
        if find_count <1:
            return "Ничего не найдено =( "
        else:
            return "Код оператора: "+ str(code) +'\n' + "Начало диапозона: "+str(start_number) + '\n' + "Конец диапозона: "+str(end_number)\
        +'\n'+"Емкость: "+str(cap)+'\n'+"Оператор: "+str(operator)+'\n'+"Регион: "+str(region)+'\n'+"Страна: "+country

    """def search_tel_number(self, line):
        print("Телефон", line)
        result = request.urlopen("http://ostranah.ru/_lists/phone_codes.php")
        b = bs4.BeautifulSoup(result, "html.parser")
        f = open('code_country.csv', 'w')
        writer = csv.writer(f)
        list_code = []

        for row in b.findAll('table')[0].tbody.findAll('tr'):
            first_column = row.findAll('a')[0].contents
            third_column = row.findAll('td')[1].contents
            self.update_tel_country_code(str(first_column)[2:len(first_column)-3], int(str(third_column)[3:len(third_column)-3]))
            #local_list = [str(first_column)[2:len(first_column)-3], str(third_column)[3:len(third_column)-3]]
            #print(local_list)
            #list_code.append(local_list)
        #for row in list_code:
        #    writer.writerow(row)
"""


if __name__ == '__main__':
    u = Worker()
    #u.search_ip_addr('8.8.8.8')
    #print(u.claculate_ip('192.168.1.1/'))
    u.search_mac_info('AA:BB:CC:AA:BB:CC')
    u.search_mac_info('AA-BB-CC-AA-BB-CC')
    u.search_mac_info('AABBCCAABBCC')
    u.search_mac_info('AABB.CCAA.BBCC')
    u.search_mac_info('AABB:CCAA:BBCC')
    u.search_mac_info('dfghfghfg')
    #print(u.search_tel_number("8108124472309"))
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
