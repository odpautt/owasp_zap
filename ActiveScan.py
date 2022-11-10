import json
import logging
import sys
import time
from pprint import pprint

import psycopg2
from zapv2 import ZAPv2


def execute_query_in_DB(query):
    conn = psycopg2.connect(database="owasp_zap", user="sonar", password="sonar", host='10.100.82.70', port='5434')
    cursorDB = conn.cursor()
    cursorDB.execute(query)
    conn.commit()
    print("[+] Insert finalizado")


def config_logs():
    logging.basicConfig(filename="./owasp_zap.log", filemode='w', format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def zapScanExecute(argv):
    config_logs()
    OC = argv[1]
    target = argv[2]

    apiKey = 'zap'
    # target = 'http://10.65.50.11:8280/portal/CRMPortal/Consultas'
    zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8086', 'https': 'http://127.0.0.1:8086'})
    # print(f'[+] OC = {OC}' )
    print("Iniciando Scan...")
    logging.info(f'[+] OC : {OC}')
    logging.info('[+] Running Spider scan...')
    logging.info('[+] Spidering target {}'.format(target))
    # The scan returns a scan id to support concurrent scanning
    scanID = zap.spider.scan(target)
    while int(zap.spider.status(scanID)) < 100:
        # Poll the status until it completes
        logging.info('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)

    logging.info('[+] Spider has completed!')
    # Prints the URLs the spider has crawled
    logging.info('\n[+] '.join(map(str, zap.spider.results(scanID))))

    logging.info('[+] Running active scan...')
    # TODO : explore the app (Spider, etc) before using the Active Scan API, Refer the explore section
    logging.info('[+] Active Scanning target {}'.format(target))
    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        # Loop until the scanner has finished
        logging.info('[+] Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)
    #    print(f'[+] ScanID: {scanID}')
    logging.info('[+] Active Scan completed')
    # Print vulnerabilities found by the scanning
    logging.info('[+] Hosts: {}'.format(', '.join(zap.core.hosts)))
    logging.info('[+] Alerts: ')
    # pprint(zap.core.alerts(baseurl=target), indent=5)
    logging.info(f"{zap.core.alerts(baseurl=target)}")
    print("Scan finalizado!!!")


if __name__ == '__main__':
    zapScanExecute(sys.argv)
