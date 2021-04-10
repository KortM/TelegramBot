import ipaddress
import os
import bs4
import asyncpg
import asyncio
import requests
import csv
from Config import Session, CodesOfCountry, InternationTelephonyCodes
from PIL import Image


class Telephony_Interface:

    def __init__(self):
        self.client = ''
        self.sql_session = Session()
        self.event_loop = asyncio.get_event_loop()
        self.event_loop.run_until_complete(self._create_connection())

    async def _create_connection(self):
        self.client = await asyncpg.connect('postgresql://postgres:mar02031812@localhost/data')

    def update_tel_db(self):
        files = [
            'https://rossvyaz.gov.ru/data/ABC-3xx.csv',
            'https://rossvyaz.gov.ru/data/ABC-4xx.csv',
            'https://rossvyaz.gov.ru/data/ABC-8xx.csv',
            'https://rossvyaz.gov.ru/data/DEF-9xx.csv'
        ]
        count = 1

        for f in files:
            self.event_loop.run_until_complete(self._download_files(f, count))
            count += 1

    async def _download_files(self, url, name) -> str:
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

                    await self.client.copy_records_to_table(
                        'telephony',
                        records=[(int(code), int(start_number), int(
                            end), int(cap), operator, region)],
                        columns=[
                            'code', 'start_range', 'end_range', 'capacity', 'operator', 'region']
                    )

                except Exception as e:
                    print('Ошибка при загрузке cvs ', e)
            print('Done write to db tel_{name}.csv')

    async def _get_telephony_info(self, code: int, number: int) -> str:
        result = await self.client.execute('SELECT * FROM telephony WHERE code = 301 ')
        print(result)
        result = await self.client.fetch(
            '''SELECT * FROM telephony WHERE code = {} AND start_range <= {} AND end_range >={}'''
            .format(int(code), int(number), int(number))
        )
        print(result)

    def get_telephony_info(self, code: int, number: int) -> str:
        self.event_loop.run_until_complete(
            self._get_telephony_info(code, number))

    def update_internation_numbers(self):
        result = requests.get("http://ostranah.ru/_lists/phone_codes.php")
        b = bs4.BeautifulSoup(result.content, "html.parser")
        for row in b.findAll('table')[0].tbody.findAll('tr'):
            self.sql_session.add(InternationTelephonyCodes(code=row.findAll('td')[
                                 1].text.strip(), title=row.find('a').text.strip()))
            self.sql_session.commit()

    def find_international_number(self, number: str):
        count = 0
        result = ''
        for i in number:
            count += 1
            tmp = self.sql_session.query(InternationTelephonyCodes).filter_by(
                code=number[:-count]).first()
            if tmp:
                result = tmp
        flag = self.find_flag_by_country(result.title)
        if result:
            return (f'Code: {result.code}\nCountry: {result.title}', flag)

    def update_country(self):
        with open(f'src/country.csv', 'r') as f:
            reader = csv.DictReader(f, 'cp1251')
            for line in reader:
                print(line)
                self.sql_session.add(CodesOfCountry(
                    country=line['c'], title=line['p']))
                self.sql_session.commit()
            print('Success update codes of country')

    def find_flag_by_country(self, country):
        try:
            flag_title = self.sql_session.query(
                CodesOfCountry).filter_by(title=country).first()
            return open(f'src/flags-normal/{flag_title.country.lower()}.png', 'rb')
        except Exception as e:
            print('Country is not found', e)

    def resize_flags(self):
        for addr, dirs, files in os.walk('src/flags'):
            for images in files:
                image = Image.open(f'src/flags/{images}')
                resized_image = image.resize(
                    (int(image.size[0]/2), int(image.size[1]/2)))
                resized_image.save(f'src/flags-normal/{images}')


tel = Telephony_Interface()
tel.update_tel_db()
tel.get_telephony_info(301, 2110001)
#asyncio.get_event_loop().run_until_complete(create_connection())
