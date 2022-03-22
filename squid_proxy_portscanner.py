import requests


def scan_target(target, proxy):
    for port in sorted(ports):
        try:        
            resp = requests.get(f"http://{target}:{port}", proxies=proxy)
            code = resp.status_code()
            #if code == 200 or code == 404 or code == 401 or code == 403 or code == 500:
            print(f"{target} -> {port} seems OPEN ")
        except:
            pass


if __name__ == '__main__':
    ports = [21,22,23,25,53,69,80,109,110,123,135,445,1433,5985,3000,5000,137,138,139,143,156,389,443,546,547,995,993,2086,2087,2082,2083,3306,3389,8080,8443,8009,7000,7001,2049,111,10000]
    target = "1.3.3.7"
    proxy = {
        "http":"10.9.9.9"
    }

    scan_target(target,prox,ports)