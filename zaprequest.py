import sys, requests, json, time, re
from urllib.parse import urlunparse



def send_request(request):
    return requests.get(request)


def run_spider_scan(url):
    request = f'http://localhost:8088/JSON/spider/action/scan/?apikey=zap&url={url}&maxChildren=&recurse=&contextName=&subtreeOnly='
    return json.loads(send_request(request).text)['scan']


def spider_status(id):
    request= f'http://localhost:8088/JSON/spider/view/status/?apikey=zap&scanId={id}'
    return json.loads(send_request(request).text)['status']


def spider_result(id):
    request = f'http://localhost:8088/JSON/spider/view/results/?apikey=zap&scanId={id}'
    return json.loads(send_request(request).text)['results']


def runActiveScan(url):
    target = url
    request = f'http://localhost:8088/JSON/ascan/action/scan/?apikey=zap&url={url}&recurse=true&inScopeOnly=false&scanPolicyName=&method=&postData=&contextId='
    r = send_request(request)
    return json.loads(r.text)['scan']


def active_scan_progress(id):
    request = f'http://localhost:8088/JSON/ascan/view/scanProgress/?apikey=zap&scanId={id}'
    return send_request(request)


def active_scan_status(id):
    request = f'http://localhost:8088/JSON/ascan/view/status/?apikey=zap&scanId={id}'
    return send_request(request)


def while_process_ends(status):
    in_progress = True
    while in_progress:
        time.sleep(5)
        status = status
        if status == "100":
            print("[+] Ejecucion Finalizada !!!")
            in_progress = False
        else:
            print(f'[+]... {status}% ...')

### inicia el programa

url = sys.argv[1]

print(f"[+] Inicia el Spider Scan, Target: {url}")

id_spider_scan = run_spider_scan(url)

in_progress = True
while in_progress:
    time.sleep(5)
    status = spider_status(id_spider_scan)
    if status == "100":
        print("[+] Ejecucion Finalizada !!!")
        in_progress= False
    else:
        print(f'[+]... {status}% ...')
print("[+] Spider Result: ")
for result in spider_result(id_spider_scan):
    print(f"[+] {result}")

print(f"[+] Inicia el Active Scan, Target: {url}")


id = runActiveScan(url)
in_progress = True

while in_progress:
    time.sleep(5)
    status = json.loads(active_scan_status(id).text)['status']
    if status == "100":
        print("[+] Ejecucion finalizada !!")
        in_progress = False
    else:
        print(f'[+]... {status}% ...')


process = active_scan_progress(id).text
print(process)

