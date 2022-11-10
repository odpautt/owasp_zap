import time
from zapv2 import ZAPv2

# The URL of the application to be tested
target = 'http://10.65.50.11:8280/portal/CRMPortal/Consultas'
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'zap'

# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apiKey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8086', 'https': 'http://127.0.0.1:8086'})

print('Spidering target {}'.format(target))

# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)
print(scanID)
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))
# If required post process the spider results

# TODO: Explore the Application more with Ajax Spider or Start scanning the application for vulnerabilities