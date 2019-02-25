from Config import Session, Mac
import csv
class UpdateBD():
    def __init__(self):
        self.s = Session()

    def update(self, A,B,C,title, address):
        m = Mac(A,B,C, title, address)
        self.s.add(m)
        self.s.commit()
    def splitStr(self, mac):
        mac = mac.upper()
        str = mac.split(':')
        if(len(str)<6):
            str = mac.split('.')
            if(len(str) <6):
                str = mac.split('-')
                if(len(str)<6):
                    str = mac.split('.')
                    if len(str) < 3:
                        str = mac.split(' ')
                        if len(str) <6:
                            str = mac
                            if len(str) < 12:
                                return 'Неверный формат mac-адреса!'
                            else:
                                result = self.search(str[0:2], str[2:4], str[4:6], str[6:8], str[8:10], str[10:12])
                        else:
                            result = self.search(str[0], str[1], str[2], str[3], str[4], str[5])
                    else:
                        result = self.search(str[0][0:2], str[0][2:4], str[1][0:2], str[1][2:4], str[2][0:2],
                                             str[2][2:4])
                else:
                    result=self.search(str[0], str[1], str[2], str[3], str[4], str[5])
            else:
                result = self.search(str[0], str[1], str[2], str[3], str[4], str[5])
        else:
            result = self.search(str[0], str[1], str[2], str[3], str[4], str[5])
        return result

    def search(self, A,B,C,D,E,F):
        a = self.s.query(Mac).filter_by(A=str(A)).all()
        count = 0
        max_count = 0
        list_count = 0
        result_index = []
        for i in a:
            if str(B) in str(i)[3:5]:
                count = count +1
                if C in str(i)[6:8]:
                    count = count +1
                    if D in str(i)[9:11]:
                        count = count + 1
                        if E in str(i)[12:14]:
                            count = count + 1
                            if F in str(i)[15:17]:
                                result_index.insert(0, i)
                                result_index.insert(1, i.title)
                                result_index.insert(2, i.address)
            if count >0:
                if max_count < count:
                    max_count = count
                    result_index.insert(0, i)
                    result_index.insert(1, i.title)
                    result_index.insert(2, i.address)
            count = 0
            list_count = list_count +1
        if len(result_index) <=0:
            return "Mac не найден!"
        else:
            #return str(result_index[0]).lstrip()+' Название организации: '+str(result_index[1]+' Адрес: '+str(result_index[2]))
            return 'Название организации: ' + str(
                result_index[1] +'\n'+ 'Адрес: ' + str(result_index[2]))

    def load_in_csv(self):
        f = open("macbd.csv")
        reader  = csv.DictReader(f)
        for line in reader:
            A = str(line['Assignment'])[0:2]
            B = str(line['Assignment'])[2:4]
            C = str(line['Assignment'])[4:6]
            Name = str(line['Organization Name'])
            Address  = str(line['Organization Address'])
            self.update(A, B, C, Name, Address)

    def search_ip_addr(self):
        return

"""if __name__=='__main__':
    u = UpdateBD()
    #u.load_in_csv()
    #u.load_data()
    #print(u.splitStr('ec08.6b17.3e2f'))
    #print(u.splitStr('00.1A.4B.00.00.00'))
    #print(u.splitStr('D4:9E:6D:D0:02:01'))"""
