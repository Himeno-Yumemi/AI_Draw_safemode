import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ims.v20201229 import ims_client, models
from .config import get_config

secretId = get_config('Tencent', 'secretId')
secretKey = get_config('Tencent', 'secretKey')

async def get_score(image_base):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(secretId, secretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ims.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ims_client.ImsClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ImageModerationRequest()
        params = {
            "BizType": "ai_image_check",
            "FileContent": ""
        }
        params["FileContent"]=image_base
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ImageModerationResponse的实例，与请求对象对应
        resp = client.ImageModeration(req)
        # 输出json格式的字符串回包
        #print(resp.to_json_string())
        score=json.loads(resp.to_json_string())["Score"]
        return score
    except TencentCloudSDKException as err:
        return 0