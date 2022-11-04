from zapv2 import ZAPv2
from pprint import pprint


def results():
    # The URL of the application to be tested
    target = 'http://10.65.50.11:8280/portal/CRMPortal/Consultas'
    # Change to match the API key set in ZAP, or use None if the API key is disabled
    apiKey = 'zap'

    # By default ZAP API client will connect to port 8080
    zap = ZAPv2(apikey=apiKey)
    # Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
    zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8086', 'https': 'http://127.0.0.1:8086'})

    # TODO: Check if the scanning has completed

    # Retrieve the alerts using paging in case there are lots of them
    st = 0
    pg = 5000
    alert_dict = {}
    alert_count = 0
    alerts = zap.alert.alerts(baseurl=target, start=st, count=pg)
    blacklist = [1, 2]
    risk_high = []
    risk_medium = []
    risk_low = []
    risk_informational = []
    while len(alerts) > 0:
        #print('Reading ' + str(pg) + ' alerts from ' + str(st))
        alert_count += len(alerts)
        for alert in alerts:
            plugin_id = alert.get('pluginId')

            if plugin_id in blacklist:
                continue

            if alert.get('risk') == 'High':
                risk_high.append([alert.get('alertRef'), alert.get('name'), alert.get('solution')])

            if alert.get('risk') == 'Medium':
                risk_medium.append([alert.get('alertRef'), alert.get('name'), alert.get('solution')])

            if alert.get('risk') == 'Low':
                risk_low.append([alert.get('alertRef'), alert.get('name'), alert.get('solution')])

            if alert.get('risk') == 'Informational':
                risk_informational.append([alert.get('alertRef'), alert.get('name'), alert.get('solution')])

        st += pg
        alerts = zap.alert.alerts(start=st, count=pg)

    print("[+]  Results: ")
    print(f'[+] Number of alerts risk High: {len(risk_high)}\n[+] Number of alerts risk Medium: {len(risk_medium)}\n'
          f'[+] Number of alerts risk Low: {len(risk_low)}\n[+] Number of alerts risk Informational: {len(risk_informational)}')
    print('[+] Total number of alerts: ' + str(alert_count))
    pprint(risk_low)


if __name__ == "__main__":
    results()
