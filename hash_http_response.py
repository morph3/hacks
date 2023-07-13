import requests
import sys
import hashlib


VERBOSE = True
VERBOSE = False

def hash_response(url, level=2):
    """
    This function will hash the http response of the given url
    The way this function will work is 
    
    sha256(response.status_code + response.reason +  response.headers + response.body )
    """
    my_headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"}
    try:
        response = requests.get(url, allow_redirects=False, headers=my_headers timeout=4, verify=False)

        body = response.text
        headers = ""
        for header in response.headers:
            headers += header + ": " + response.headers[header] + "\r\n"
        status_code = str(response.status_code)
        reason = response.reason

        if VERBOSE:
            print(f"{status_code} {reason}")
            print(headers)
            print(body)

        # level 1 = body 
        # level 2 = body + status_code + reason
        # level 3 = body + headers + status_code + reason


        if level == 1:
            raw_response = body
        elif level == 2:
            raw_response = body + status_code + reason
        elif level == 3:
            raw_response = status_code + reason + body + headers

        hash = hashlib.sha256(raw_response.encode()).hexdigest()
        return hash
    
    except Exception:
        return None



if __name__ == "__main__":
    url = sys.argv[1]

    if len(sys.argv) > 2:
        level = int(sys.argv[2])
    else:
        level = 2
    
    
    
    # check if url has schema in it (http/https)
    if "http" not in url:
        # just check http for now
        url = "http://" + url
    
    # compare levels
    # level 1 = body 
    # level 2 = body + status_code + reason
    # level 3 = body + headers + status_code + reason
    # level 2 is default

    hash = hash_response(url, level)
    print(f"{url}:{hash}")
