import ipaddress
import os
import bs4
import csv
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient
from Config import Session, CodesOfCountry, InternationTelephonyCodes
import threading
import asyncpg


class Telephony_Interface:

    def __init__(self):
        self.client = MongoClient('mongodb://kort:mar02031812@localhost:27017/')
        #self.client = MongoClient('mongodb+srv://kort:mar02031812@cluster0.nlzma.mongodb.net/bot_data?retryWrites=true&w=majority')
        self.sql_session = Session()

    def update_tel_db(self):
        db = self.client['bot_data']
        try:
            db.tel_data.drop()
        except Exception:
            print("Error delete mac_data")
        files = [
            'https://rossvyaz.gov.ru/data/ABC-3xx.csv',
            'https://rossvyaz.gov.ru/data/ABC-4xx.csv',
            'https://rossvyaz.gov.ru/data/ABC-8xx.csv',
            'https://rossvyaz.gov.ru/data/DEF-9xx.csv'
        ]
        thread_control = []
        count = 1
        for value in files:
            try:
                th = threading.Thread(
                    target=self.download_files, args=(value, count))
                th.start()
                thread_control.append(th)
                count += 1
            except:
                print('Problem threads')
        [f'Thread is complete {th.join()}' for th in thread_control]

    def download_files(self, url, name) -> str:
        db = self.client['bot_data']
        with requests.get(url, stream=True, verify=False) as result:
            result.raise_for_status()
            with open(f'src/tel_{name}.csv', 'wb') as f:
                for line in result.iter_content(chunk_size=8192):
                    f.write(line)
            print(f'Done load and write tel_{name} as file csv')

        with open(f'src/tel_{name}.csv', 'r') as f:
            reader = csv.DictReader(f, 'cp1251')
            for line in reader:
                try:
                    sp = line["c"]
                    split_line = str(sp).split(';')
                    code = split_line[0]
                    start_number = split_line[1]
                    end = split_line[2]
                    cap = split_line[3]
                    operator = split_line[4]
                    region = split_line[5]
                    
                    db['tel_data'].insert(
                        
                            {
                                "Code": code,
                                "Start of the range": int(start_number),
                                "The end of the range": int(end),
                                "Capacity": cap,
                                "Operator": operator,
                                "Region": region
                            }
                        
                    )
                    
                except Exception as e:
                    print(e)
            print('Done write to db')

    def get_telephony_info(self, code: str, number: int) -> str:
        result = self.client.bot_data.tel_data.find(
            {
                '$and':
                [
                    {"Code": code, }, {"Start of the range": {"$lte": number}}, {
                        "The end of the range": {"$gte": number}}
                ]
            })
        
        for i in result:
            return ("Code:{}\nStart of the range: {}\nThe end of the range: {}\nCapacity:{}\nOperator: {}\nRegion: {}\nCountry: {}" \
                .format(
                    i['Code'],
                    i['Start of the range'],
                    i['The end of the range'],
                    i['Capacity'],
                    i['Operator'],
                    i['Region'],
                    'Россия'
                ), self.find_flag_by_country('Россия'))

    def update_internation_numbers(self):
        result = requests.get("http://ostranah.ru/_lists/phone_codes.php")
        b = bs4.BeautifulSoup(result.content, "html.parser")
        for row in b.findAll('table')[0].tbody.findAll('tr'):
            self.sql_session.add(InternationTelephonyCodes(code=row.findAll('td')[1].text.strip(), title=row.find('a').text.strip()))
            self.sql_session.commit()
    
    def find_international_number(self, number: str):
        count = 0
        result = ''
        for i in number:
            count +=1
            tmp = self.sql_session.query(InternationTelephonyCodes).filter_by(code=number[:-count]).first()
            if tmp: result = tmp
        
        if result:
            if result.title == 'Южно-Африканская Республика': 
                flag = self.find_flag_by_country('ЮАР')
            else:
                flag = self.find_flag_by_country(result.title)
            return (f'Code: {result.code}\nCountry: {result.title}', flag)

    def update_country(self):
        with open(f'src/country.csv', 'r') as f:
            reader = csv.DictReader(f, 'cp1251')
            for line in reader:
                self.sql_session.add(CodesOfCountry(country=line['c'], title=line['p']))
                self.sql_session.commit()
            print('Success update codes of country')
    
    def find_flag_by_country(self, country):
        try:
            flag_title = self.sql_session.query(CodesOfCountry).filter_by(title=country).first()
            return open(f'src/flags-normal/{flag_title.country.lower()}.png', 'rb')          
        except Exception as e:
            print('Country is not found', e)
    
    def resize_flags(self):
        for addr, dirs, files in os.walk('src/flags'):
            for images in files:
                image = Image.open(f'src/flags/{images}')
                resized_image = image.resize((int(image.size[0]/2), int(image.size[1]/2)))
                resized_image.save(f'src/flags-normal/{images}')

async def main():
    tel = Telephony_Interface()

if __name__ == '__main__':
    tel = Telephony_Interface()
    #tel.update_tel_db()
    #tel.update_country()
    #tel.find_flag_by_country('Россия')
    #print(tel.get_telephony_info(code='950', number=6628028))
    #tel.update_internation_numbers()
    #tel.resize_flags()
    
    #tel.find_international_number('27545121545')
    #print(tel.find_international_number('9506628028'))
