from urllib import request
from Config import Session, Mac, Country, RussianNubmers, CountryCode
import csv, bs4
import urllib3, json
from ipwhois import IPWhois


class UpdateBD():
    def __init__(self):
        self.s = Session()

    def update_MAC(self, A, B, C, title, address):
        m = Mac(A, B, C, title, address)
        self.s.add(m)
        self.s.commit()

    def update_country_code(self, code, title):
        m = Country(code=code, title=title)
        self.s.add(m)
        self.s.commit()

    def update_telephone_number(self, code, start, end, cap, operator, region):
        m = RussianNubmers(code=str(code), start_number=str(start), end_number=str(end), cap=str(cap),
                           operator=str(operator), region=str(region))
        self.s.add(m)
        self.s.commit()

    def update_tel_country_code(self, country, code):
        m = CountryCode(country=str(country), code=int(code))
        self.s.add(m)
        self.s.commit()

    def split_to_colon(self, mac):
        str = mac.split(':')
        if len(str) < 6:
            return False
        else:
            result = self.search(str[0], str[1], str[2], str[3], str[4], str[5])
            return result

    def split_to_dash(self, mac):
        str = mac.split('-')
        if len(str) < 6:
            return False
        else:
            result = self.search(str[0], str[1], str[2], str[3], str[4], str[5])
            return result

    def split_to_point(self, mac):
        str = mac.split('.')
        if len(str) < 3 or len(str) > 3:
            return False
        else:
            result = self.search(str[0][0:2], str[0][2:4], str[1][0:2], str[1][2:4], str[2][0:2],
                                 str[2][2:4])
            return result

    def split_to_space(self, mac):
        str = mac.split(' ')
        if len(str) < 6:
            return False
        else:
            result = self.search(str[0], str[1], str[2], str[3], str[4], str[5])
            return result

    def split_mac(self, mac):
        str = mac
        if len(str) < 12:
            return False
        else:
            result = self.search(str[0:2], str[2:4], str[4:6], str[6:8], str[8:10], str[10:12])
            return result

    def splitStr(self, mac):
        mac = mac.upper()
        is_find = False
        split = self.split_to_dash(mac)
        if split:
            return split, "MAC-адрес: " + mac
        else:
            is_find = False
        split = self.split_to_colon(mac)
        if split:
            return split, "MAC-адрес: " + mac
        else:
            is_find = False
        split = self.split_to_point(mac)
        if split:
            return split, "MAC-адрес: " + mac
        else:
            is_find = False
        split = self.split_to_space(mac)
        if split:
            return split, "MAC-адрес: " + mac
        else:
            is_find = False
        split = self.split_mac(mac)
        if split:
            return split, "MAC-адрес: " + mac
        else:
            is_find = False
        if not is_find:
            is_ip = self.search_ip_addr(mac.lower())
            if is_ip:
                return is_ip
            else:
                is_tel_number = self.search_tel_number(mac)
                if is_tel_number:
                    return "Номер: "+mac + '\n'+ is_tel_number
                else:
                    return 'Неверный формат MAC или IP -адреса!'

    def search(self, A, B, C, D, E, F):
        a = self.s.query(Mac).filter_by(A=str(A)).all()
        count = 0
        max_count = 0
        list_count = 0
        result_index = []
        for i in a:
            if str(B) in str(i)[3:5]:
                count = count + 1
                if C in str(i)[6:8]:
                    count = count + 1
                    if D in str(i)[9:11]:
                        count = count + 1
                        if E in str(i)[12:14]:
                            count = count + 1
                            if F in str(i)[15:17]:
                                result_index.insert(0, i)
                                result_index.insert(1, i.title)
                                result_index.insert(2, i.address)
            if count > 0:
                if max_count < count:
                    max_count = count
                    result_index.insert(0, i)
                    result_index.insert(1, i.title)
                    result_index.insert(2, i.address)
            count = 0
            list_count = list_count + 1
        if len(result_index) <= 0:
            return False
        else:
            # return str(result_index[0]).lstrip()+' Название организации: '+str(result_index[1]+' Адрес: '+str(result_index[2]))
            return 'Название организации: ' + str(
                result_index[1] + '\n' + 'Адрес: ' + str(result_index[2]))

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

    def search_ip_addr(self, ip):
        try:
            obj = IPWhois(ip)
            results = obj.lookup_whois()

            if len(results) <= 0:
                return False
            else:
                country_code = results['asn_country_code']
                a = self.s.query(Country).filter_by(code=str(country_code)).first()
                country = a.title
                register = results['asn_registry']
                cidr = results['nets'][0]['cidr']
                range = results['nets'][0]['range']
                data = results['asn_date']
                provider = results['asn_description']
                query = results['query']
                address = results['nets'][0]['address']

                return (
                            "IP: " + query + '\n' + "Регистрационная служба: " + register + '\n' + "CIDR: " + cidr + '\n' + "Диапозон: " + range + '\n'
                            + "Дата назначения: " + data + '\n' + "Провайдер: " + provider + '\n' + "Страна: " + str(
                        country) + '\n' + "Адрес: " + str(address).rstrip())
        except:
            return False

    def search_tel_number(self, number):
        prefix = number[0:1]
        p_out_number = ''
        if prefix == '+':
            p_out_number = number[1:]
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

            # print('Code: ', n)
            # print(i)
        return result

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
    u = UpdateBD()
    #print(u.search_tel_number("+78124472309"))
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
