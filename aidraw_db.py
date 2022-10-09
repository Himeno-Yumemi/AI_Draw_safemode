from asyncio import Lock
from os.path import dirname, join, exists
from hoshino import Service,priv,aiorequests
from hoshino.util import FreqLimiter, DailyNumberLimiter
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO

import base64
import json
import time,calendar
import re
import requests as req
import sqlite3
import os

####替换成自己的API URL
word2img_url = ""   #绘图API接口
token = ""  #个人token


lmt = FreqLimiter(60) #频率限制(s)
dlmt_ = 20 # 每日次数限制
dlmt = DailyNumberLimiter(dlmt_)

sv_help = '''
【AI绘图数据库】
-[上传[参数]]  上传图片和tag至数据库内，[参数]为ai绘图的指令
-[炼金手册[序号]]  查询炼金手册内容，[序号]为页数，每页显示8张
-[查看配方[序号]]  查询炼金配方内容，[序号]为图片标签
-[使用配方[序号]]  使用炼金配方内容，[序号]为图片标签
-[删除配方[序号]]  删除炼金配方内容，[序号]为图片标签
PS:上传仅限管理员使用，删除仅限超级管理员使用
'''

sv = Service(
    name = 'AI绘图数据库',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["绘图数据库帮助"])
async def bangzhu(bot, ev):
    await bot.send(ev, await wordimage(sv_help), at_sender=True)

lock = Lock()
curpath = dirname(__file__)
image_list_db = join(curpath, 'save_tags.db')   #保存tags数据库
save_image_path= join(curpath,'SaveImage')  # 保存图片路径

#创建数据库图片存放文件夹
if not exists(save_image_path):
    os.mkdir(save_image_path)

#创建数据库文件并新建一个aitag表
if not exists(image_list_db):
    conn = sqlite3.connect(image_list_db)
    cur = conn.cursor()
    sql_title = '''CREATE TABLE aitag
           (权重 TINYINT,
            形状 CHAR,
            标签 TEXT,
            种子 INT,
            图片 BLOB);'''
    cur.execute(sql_title)
    cur.close()
    conn.close()

@sv.on_prefix(('上传'))
async def upload_header(bot, ev):
    global lock
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '上传配方仅限管理员使用', at_sender=True)
        return
    """ uid = str(ev['user_id'])
    if not lmt.check(uid):
        await bot.finish(ev, f'魔力回复中！(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(uid,10) """
    async with lock:
        conn=sqlite3.connect(image_list_db)
        cur = conn.cursor()
        try:
            for i in ev.message:
                if i.type == "image":
                    image=str(i)
                    break
            image_url = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(image))
            pic_url = image_url.group(2)
            response = req.get(pic_url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            ls_f=base64.b64encode(BytesIO(response.content).read())
            imgdata=base64.b64decode(ls_f)
            datetime = calendar.timegm(time.gmtime())
            image_path= './SaveImage/'+str(datetime)+'.png'
            saveconfig = join(curpath, f'{image_path}')
            size=f"{img.width}x{img.height}"
            pic = open(saveconfig, "wb")
            pic.write(imgdata)
            pic.close()
        except:
            await bot.finish(ev, '图片格式出错', at_sender=True)
            return
        try:
            seed_list1=str(ev.message).split(f"scale:")
            seed_list2=seed_list1[0].split('eed:')
            seed=seed_list2[1].strip ()
        except:
            await bot.finish(ev, '种子格式出错', at_sender=True)
            return
        try:
            scale_list=seed_list1[1].split(f"tags:")
            scale=scale_list[0].strip()
        except:
            await bot.finish(ev, '权重格式出错', at_sender=True)
            return
        try:
            tags=scale_list[1].strip()
        except:
            await bot.finish(ev, '标签格式出错', at_sender=True)
            return
        try:
            cur.execute("INSERT INTO aitag VALUES (?,?,?,?,?)",(scale,size,tags,seed,saveconfig))
            conn.commit()
            cur.close()
            conn.close()
            await bot.send(ev, f'上传成功！', at_sender=True)
        except Exception as e:
            await bot.send(ev, f"报错:{e}",at_sender=True)

@sv.on_rex((r'^炼金手册([1-9]\d*)$'))
async def alchemy_book(bot, ev):
    conn=sqlite3.connect(image_list_db)
    match = ev['match']
    page=int(match.group(1))-1
    cur = conn.cursor()
    sql = "select rowid,图片 from aitag"
    results = cur.execute(sql)
    image_list = results.fetchall()
    cur.close()
    conn.close()
    target = Image.new('RGB', (1920,1080),(255,255,255))
    i=0
    for index in range(0+(page*8),8+(page*8)):
        try:
            image_msg=image_list[index]
        except:
            break
        rowid = image_msg[0]
        image_path=image_msg[1]
        region = Image.open(image_path)
        region = region.convert("RGB")
        region = region.resize((int(region.width/2),int(region.height/2)))
        font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\simsun.ttc', 36)  # 设置字体和大小
        draw = ImageDraw.Draw(target)
        if i<4:
            target.paste(region,(80*(i+1)+384*i,50))
            draw.text((80*(i+1)+384*i+int(region.width/2)-18,80+region.height),str(rowid).replace(',',''),font=font,fill = (0, 0, 0))
        if i>=4:
            target.paste(region,(80*(i-3)+384*(i-4),150+384))
            draw.text((80*(i-3)+384*(i-4)+int(region.width/2)-18,180+384+region.height),str(rowid).replace(',',''),font=font,fill = (0, 0, 0))
        i+=1
    result_buffer = BytesIO()
    target.save(result_buffer, format='JPEG', quality=100) #质量影响图片大小
    imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
    resultmes = f"[CQ:image,file={imgmes}]"
    await bot.send(ev,resultmes)

@sv.on_rex((r'^查看配方([1-9]\d*)'))
async def view_recipe(bot, ev):
    uid = str(ev['user_id'])
    if not lmt.check(uid):
        await bot.finish(ev, f'魔力回复中！(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(uid,30)
    match = ev['match']
    rowid=int(match.group(1))
    conn=sqlite3.connect(image_list_db)
    cur = conn.cursor()
    results=cur.execute("SELECT * FROM aitag WHERE rowid=?", (rowid,))
    peifang = results.fetchone()
    scale=peifang[0]
    size=peifang[1]
    tags=peifang[2]
    image_path=peifang[4]
    seed=peifang[3]
    pic = open(image_path, "rb")
    base64_str = base64.b64encode(pic.read())
    imgmes = 'base64://' + base64_str.decode()
    resultmes = f"[CQ:image,file={imgmes}]"
    pic.close()
    msg=f"序号为:{rowid}\n{resultmes}\n配方:ai绘图{tags}\nCFG scale: {scale}, Size:{size}"
    cur.close()
    conn.close()
    await bot.send(ev,msg,at_sender=True)

@sv.on_rex((r'^使用配方([1-9]\d*)'))
async def generate_recipe(bot, ev):
    uid = str(ev['user_id'])
    if not dlmt.check(uid):
        await bot.finish(ev, f'今日魔力已经用完，请明天再来~', at_sender=True)
        return
    if not lmt.check(uid):
        await bot.finish(ev, f'魔力回复中！(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
        return
    dlmt.increase(uid) 
    lmt.start_cd(uid)
    match = ev['match']
    rowid=int(match.group(1))
    conn=sqlite3.connect(image_list_db)
    cur = conn.cursor()
    results=cur.execute("SELECT * FROM aitag WHERE rowid=?", (rowid,))
    peifang = results.fetchone()
    scale=peifang[0]
    size=peifang[1]
    tags=peifang[2]
    msg=f"{tags}\nCFG scale: {scale}, Size:{size}".replace('&r18=1','')
    cur.close()
    conn.close()
    await bot.send(ev, f"\n正在炼金中，请稍后...\n(今日剩余{dlmt_-int(dlmt.get_num(uid))}次)", at_sender=True)
    image = await gen_pic(msg)
    await bot.send(ev,image,at_sender=True)

@sv.on_rex((r'^删除配方([1-9]\d*)'))
async def delete_recipe(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '删除配方仅限超级管理员使用', at_sender=True)
        return
    """ uid = str(ev['user_id'])
    if not lmt.check(uid):
        await bot.finish(ev, f'魔力回复中！(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(uid) """
    match = ev['match']
    rowid=int(match.group(1))
    conn=sqlite3.connect(image_list_db)
    cur = conn.cursor()
    results=cur.execute("SELECT 图片 FROM aitag WHERE rowid=?", (rowid,))
    delete_path = results.fetchone()
    delete_image=delete_path[0]
    os.remove(delete_image)
    cur.execute("DELETE FROM aitag WHERE rowid=?", (rowid,))
    conn.commit()
    cur.execute('vacuum')
    msg=f"已删除配方:{rowid}"
    cur.close()
    conn.close()
    await bot.send(ev,msg,at_sender=True)

async def gen_pic(text):
    try:
        get_url = word2img_url + text + token
        res = await aiorequests.get(get_url)
        image = await res.content
        load_data = json.loads(re.findall('{"steps".+?}', str(image))[0])
        image_b64 = 'base64://' + str(base64.b64encode(image).decode())
        mes = f"[CQ:image,file={image_b64}]"
        mes += f'\nseed:{load_data["seed"]}'
        
        """ mes += f'\tscale:{load_data["scale"]}\n'
        mes += f'tags:{text}' """
        return mes
    except Exception as e:
        return f"炼金失败了,原因:{e}"

async def wordimage(word):
    bg = Image.new('RGB', (950,300), color=(255,255,255))
    font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\simsun.ttc', 30)  # 设置字体和大小
    draw = ImageDraw.Draw(bg)
    draw.text((10,5), word, fill="#000000", font=font)
    result_buffer = BytesIO()
    bg.save(result_buffer, format='JPEG', quality=100)
    imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
    resultmes = f"[CQ:image,file={imgmes}]"
    return resultmes