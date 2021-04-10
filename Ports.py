from pymongo import MongoClient
clent = MongoClient('mongodb://Kort:mar02031812@ds263856.mlab.com:63856/heroku_6tmbh2c1')
db = clent.heroku_6tmbh2c1
ports = db.Ports
def get_port(n) -> int:
    port = ports.find({"Port Number":str(n)})
    if port is None and not port:
        return None
    result = ''
    for i in port:
        result = result + "{} {} {} {}".format("Service Name: "+i['Service Name']+'\n',\
                                                  "Port Number: "+i['Port Number']+'\n', \
                                                  "Transport Protocol: "+i['Transport Protocol']+'\n',\
                                                  "Description: "+i['Description']+'\n')
    return result
if __name__ == '__main__':
    print(get_port(80))