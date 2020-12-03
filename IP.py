import ipaddress


def calc_ip(ip) -> str:
        '''Метод расчета ip по маске подсети'''
        try:
            #ip_list = list(ipaddress.ip_network(ip, False).hosts())
            args = ip.split('/')
            if len(args) > 1:
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
                return {"Address": str(address), "Netmask": str(mask), "Wildcard": str(wildcard), "Network": str(network),
                    "Broadcast": str(broadcast), "HostMin": str(min_host), "HostMax": str(max_host), "Hosts/Net": str(hosts),
                    "Private": str(private)}
        except ValueError:
            return None

if __name__ == '__main__':
    print(calc_ip("2.2.2.2/5"))
