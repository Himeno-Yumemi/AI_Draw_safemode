import requests
from hoshino import aiorequests


API_KEY = ''   #你的API Key
SECRET_KEY = ''#你的Secret Key

host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
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
                return { 'code': r['error_code'], 'msg': r['error_msg'] }
            try:
                data = r['data']
            except:
                return { 'code': -1, 'msg': '请检查策略组中疑似区间是否拉满' }
            porn_0 = 0
            porn_1 = 0
            porn_2 = 0
            for c in data:
                #由于百度的图片审核经常给出极低分,所以不合规项置信度*500后为分数
                if c['type'] == 1 and c['subType'] == 0:
                    porn_0 = int(c['probability'] * 500)
                elif c['type'] == 1 and c['subType'] == 1:
                    porn_1 = int(c['probability'] * 500)
                elif c['type'] == 1 and c['subType'] == 10:
                    porn_2 = int(c['probability'] * 500)
            return { 'code': 0, 'msg': 'Success', 'value': max(porn_0,porn_1,porn_2) }

        else:
            return { 'code': -1, 'msg': 'API Error' }


    except FileNotFoundError:
        return { 'code': -1, 'msg': 'File not found' }