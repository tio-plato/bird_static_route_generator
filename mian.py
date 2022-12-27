import argparse
from urllib import request

parser = argparse.ArgumentParser(description='Generate static route lists for bird based on region.')
parser.add_argument('--region', default=['CN'], nargs='+',
                    help='The area contained in the generated static route list. Available areas: https://www.iwik.org/ipcountry/. (default: CN)')
args = parser.parse_args()


def download_iplist():
    baseurl = 'https://www.iwik.org/ipcountry/'
    _iplist = []
    for region in args.region:
        url = baseurl + region + '.cidr'
        print('Downloading ' + url)
        r = request.urlopen(url)
        region_ip = r.read().decode('utf-8').splitlines()
        region_ip.pop(0)
        _iplist += region_ip
    return _iplist


if __name__ == '__main__':
    iplist = download_iplist()
    route_list = []
    for ip in iplist:
        route_list.append('route ' + ip + ' via "wg0";')

    with open('route_list.conf', 'w') as f:
        for route in route_list:
            f.write("%s\n" % route)
