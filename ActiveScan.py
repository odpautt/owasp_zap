import sys
import time
from pprint import pprint

from zapv2 import ZAPv2


def zapScanExecute(argv):
    target = argv[1]
    apiKey = 'zap'
    #target = 'http://10.65.50.11:8280/portal/CRMPortal/Consultas'
    zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8086', 'https': 'http://127.0.0.1:8086'})

    print('[+] Running Spider scan...')
    print('[+] Spidering target {}'.format(target))
    # The scan returns a scan id to support concurrent scanning
    scanID = zap.spider.scan(target)
    while int(zap.spider.status(scanID)) < 100:
        # Poll the status until it completes
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)

    print('[+] Spider has completed!')
    # Prints the URLs the spider has crawled
    print('\n[+] '.join(map(str, zap.spider.results(scanID))))

    print('[+] Running active scan...')
    # TODO : explore the app (Spider, etc) before using the Active Scan API, Refer the explore section
    print('[+] Active Scanning target {}'.format(target))
    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        # Loop until the scanner has finished
        print('[+] Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)
    print(f'[+] ScanID: {scanID}')
    print('[+] Active Scan completed')
    # Print vulnerabilities found by the scanning
    print('[+] Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('[+] Alerts: ')
    pprint(zap.core.alerts(baseurl=target), indent=5)


if __name__ == '__main__':
    zapScanExecute(sys.argv)
