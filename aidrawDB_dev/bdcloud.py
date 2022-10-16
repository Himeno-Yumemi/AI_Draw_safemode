import requests
from hoshino import aiorequests
from .config import get_config

api_key = get_config('Baidu', 'api_key')
secret_key = get_config('Baidu', 'secret_key')
baiduAI_check =get_config('Baidu', 'BaiduAI_check')

if baiduAI_check == True:
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
    response = requests.get(host)
    access_token = response.json()["access_token"]
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

async def porn_pic_index(base):
    params = {"image": base}
    resp = await aiorequests.post(request_url, data=params, headers=headers)
    if resp.ok:
        data = await resp.json()
    try:
        if (data):
            r = data
            if "error_code" in r:
                return 0,0
            try:
                data = r['data']
            except:
                return 0,0
            porn_1 = 0
            porn_2 = 0
            for c in data:
                if c['type'] == 1 and c['subType'] == 1:
                    porn_1 = int(c['probability'] * 100)
                elif c['type'] == 1 and c['subType'] == 10:
                    porn_2 = int(c['probability'] * 100)
            return  porn_1,porn_2
        else:
            return 
    except FileNotFoundError:
        return 0,0