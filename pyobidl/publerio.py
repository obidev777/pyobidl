import requests
import json
import time

HEADERS={'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive',"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}


class PublerIOInfo(object):
    def __init__(self, jsondata):
        self.url = jsondata['path']
        self.type = jsondata['type']
        self.name = jsondata['name']
        self.caption = jsondata['caption']
        self.source = jsondata['source']
        self.cors = jsondata['cors']
        self.force = jsondata['force']


def get_publerio_info(url):
    # Create a RequestsCookieJar object
    cookies = requests.cookies.RequestsCookieJar()
    sess = requests.Session()
    sess.cookies = cookies
    jsondata = {'url':url,'iphone':False}
    resp = sess.post('https://app.publer.io/hooks/media',json=jsondata,headers=HEADERS)
    if resp.status_code==200:
        data = json.loads(resp.text)
        if 'job_id' in data:
            job_id = data['job_id']
            working = True
            while working:
                time.sleep(1)
                resp = sess.get(f'https://app.publer.io/api/v1/job_status/{job_id}',headers=HEADERS)
                if resp.status_code==200:
                    data = json.loads(resp.text)
                    if 'status' in data:
                        if(data['status']=='complete'):
                            response = json.loads(resp.text)['payload'][0]
                            if not 'error' in response:
                                return PublerIOInfo(response)
                            else:
                                return None
                    else:
                        break
    return None