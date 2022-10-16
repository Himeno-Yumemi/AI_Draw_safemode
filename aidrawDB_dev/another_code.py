import re
import base64
import json
import asyncio
from io import BytesIO
from PIL import Image
from base64 import b64encode
from hoshino import aiorequests
from hoshino.config import NICKNAME
from aiocqhttp.exceptions import ActionFailed
from .config import get_config
from .limit import guolv
from .txcloud import get_score
from .bdcloud import porn_pic_index

#获取机器人昵称
if type(NICKNAME) == str:
    NICKNAME = [NICKNAME]
tencentAI_check = get_config('Tencent', 'TencentAI_check')
baiduAI_check =get_config('Baidu', 'BaiduAI_check')

async def re_url(image_msg):
    try:
        image_url = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(image_msg))
        pic_url = image_url.group(2)
        return 0 if not pic_url else pic_url
    except:
        raise Exception('图片链接发生错误')

async def image_to_base64(data):
    base64_en=b64encode(data)
    base64_de=str(base64_en.decode())
    image='base64://' + base64_de
    return base64_en,image

async def http_get(url):
    try:
        res = await aiorequests.get(url)
        image = await res.content
        img = Image.open(BytesIO(image))
    except:
        return 0,0,0,0,0
    size = f'{img.width}x{img.height}'
    try:
        load_data = json.loads(re.findall('{"steps".+?}', str(image))[0])
        seed=str(load_data['seed'])
        scale=str(load_data['scale'])
    except:
        seed=0
        scale=11
    base64_en,pic=await image_to_base64(image)
    return base64_en,pic,seed,scale,size

async def gpic_get(url):
    res = await aiorequests.get(url)
    image = await res.content
    img = Image.open(BytesIO(image))
    size = f'{img.width}x{img.height}'
    base64_en,pic=await image_to_base64(image)
    return base64_en,size

async def re_info(msg):
    try:
        seed=scale=shape=ntags=''
        msg_list=re.split('&',msg)
        for index,i in enumerate(msg_list):
            if index == 0:
                tags=i
            else:
                info = i.split('=')
                if info[0] == 'seed':
                    seed=info[1]
                elif info[0] == 'scale':
                    scale=info[1]
                elif info[0] == 'shape':
                    shape=info[1]
                elif info[0] == 'ntags':
                    ntags=info[1]
        return seed,scale,tags,shape,ntags
    except:
        raise Exception('配方保存发生错误')

async def another_info(msg):
    try:
        seed=scale=shape=ntags=''
        try:
            seed_list=re.split('seed:',msg)
            msg_list=seed_list[1].split('scale:')
            seed=msg_list[0].strip()
        except:
            seed=0
        try:
            scale=msg_list[1].split('tags:')[0].strip()
        except:
            scale=11
        try:
            tags=msg_list[1].split('tags:')[1].split('&')[0].strip()
            req_info='&'.join(msg_list[1].split('tags:')[1].split('&'))
            try:
                req_list = re.split('&',req_info)
                for i in req_list:
                    info = i.split('=')
                    if info[0] == 'seed':
                        seed=info[1]
                    elif info[0] == 'scale':
                        scale=info[1]
                    elif info[0] == 'shape':
                        shape=info[1]
                    elif info[0] == 'ntags':
                        ntags=info[1]
            except:
                info = req_list[0].split('=')
                if info[0] == 'seed':
                    seed=info[1]
                elif info[0] == 'scale':
                    scale=info[1]
                elif info[0] == 'shape':
                    shape=info[1]
                elif info[0] == 'ntags':
                    ntags=info[1]
        except:
            tags=msg_list[1].split('tags:')[1].strip()
        return seed,scale,tags,shape,ntags
    except:
        raise Exception('配方保存发生错误')


""" async def another_info(msg):
    try:
        seed=scale=shape=ntags=''
        msg_list=re.split('seed:',msg)
        for idx,x in enumerate(msg_list):
            if idx == 1:
                msg_info = re.split(':',x)
        for index,i in enumerate(msg_info):
            if index == 0:
                seed=i.split('scale')[0].strip()
            elif index == 1:
                scale=i.split('tags')[0].strip()
            elif index ==2:
                try:
                    tags_list=i.split('&')
                    tags=tags_list[0].strip()
                    ntags_list=re.split('&',msg)
                    for x in ntags_list:
                        info = x.split('=')
                        if info[0] == 'ntags':
                            ntags=info[1]
                except:
                    tags=i
        return seed,scale,tags,shape,ntags
    except:
        raise Exception('配方保存发生错误') """


async def size_to_shape(size):
    size_info=str(size).split('x')
    size_width=size_info[0]
    size_height=size_info[1]
    if (size_width > size_height[1]):
        image_shape = "Landscape"
    elif (size_width == size_height[1]):
        image_shape = "Square"
    else:
        image_shape = "Portrait"
    return image_shape

async def reply_msg(bot,ev):
    try:
        seg=ev.message[0]
        if ev.message[0].type != 'reply':
            return 0,0,0
        tmid = seg.data['id']
        cmd = ev.message.extract_plain_text()
        flag1 = 0
        flag2 = 0
        flag3 = 0
        for m in ev.message[2:]:
            if m.type == 'at' and m.data['qq'] == ev.self_id:
                flag1 = 1
        for name in NICKNAME:
            if name in cmd:
                flag1 = 1
                break
        for pfcmd in ['上传', '窃取']:
            if pfcmd in cmd:
                flag2 = 1
                if '窃取' in cmd:
                    flag3 = 1
        if not (flag1 and flag2):
            return 0,0,0
        try:
            tmsg = await bot.get_msg(self_id=ev.self_id, message_id=int(tmid))
        except ActionFailed:
            raise Exception ('该消息已过期，请重新转发~')
        image_url = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(tmsg["message"]))
        if not image_url:
            raise Exception ('未找到图片~')
        file = image_url.group(1)
        pic_url = image_url.group(2)
        if ',subType=' in pic_url:
            sbtype=pic_url.split('=')[-1]
            pic_url = pic_url.split(',')[0]
        elif ',subType=' in file:
            sbtype=file.split('=')[-1]
            file = file.split(',')[0]
        else:
            sbtype=None
        if 'c2cpicdw.qpic.cn/offpic_new/' in pic_url:
            md5 = file[:-6].upper()
            pic_url = f"http://gchat.qpic.cn/gchatpic_new/0/0-0-{md5}/0?term=2"
        return pic_url,tmsg,flag3
    except Exception as e:
        raise Exception('回复模块发生错误')


#合并转发
async def render_forward_msg(msg,image, uid,name):
    data_all = []
    for i in range(0,2):
        if i ==0:
            data={
                "type": "node",
                "data": {
                    "name": str(name),
                    "uin": str(uid),
                    "content": msg
                        }
                            }
        else:
            data={
                "type": "node",
                "data": {
                    "name": str(name),
                    "uin": str(uid),
                    "content": image
                        }
                            }
        data_all.append(data)
    return data_all


async def process_tags(tags):
    error_msg ="" #报错信息
    tags_guolu="" #过滤词信息
    try:
        tags,tags_guolu = guolv(tags)#过滤屏蔽词
    except Exception as e:
        error_msg = "过滤屏蔽词失败"
    return tags,error_msg,tags_guolu

async def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

async def check_imgscore(data):
    if tencentAI_check == True:
        score = await get_score(data)
        if score >=75:
            return f"图片太涩了，分数高达{score}，不予显示"
        else:
            return score
    elif baiduAI_check == True:
        score,porn = await porn_pic_index(data)
        if score >=75:
            return f"图片太涩了，分数高达{score}，不予显示"
        else:
            return score
    else:
        return -1

""" #协程锁
async def retry_task(get_task, delay=1, max_retry=10):
    finished = asyncio.Semaphore(0)
    result_lock = asyncio.Lock()
    result = None
    err = None
    tasks = []
    async def wrapper():
        nonlocal result, err
        try:
            res = await get_task()
            async with result_lock:
                if result: return
                result, err = res
                finished.release()
        except:
            pass
    for _ in range(max_retry):
        tasks.append(asyncio.get_event_loop().create_task(wrapper()))
        try:
            await asyncio.wait_for(finished.acquire(), delay)
        except asyncio.exceptions.TimeoutError:
            pass
        if result: return result, err
    await asyncio.gather(*tasks)
    return result, err

async def get_imgdata(url):
    await retry_task(lambda: http_get(url)) """
