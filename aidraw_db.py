from asyncio import Lock
from os.path import dirname, join, exists
from hoshino import Service,priv,aiorequests
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.config import NICKNAME
from hoshino.typing import CQEvent
from aiocqhttp.exceptions import ActionFailed
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
from .check_iamge import porn_pic_index

import base64
import json
import time,calendar
import re
import requests as req
import sqlite3
import os

####替换成自己的API
word2img_url = "http://YOURIP:PORT//got_image?tags="   #绘图API接口
token = "&token=YOURTOKEN"  #个人token

quality=100 #炼金大全总表生成图片质量，代码内置图片质量检测，一般不需要更改
lmt = FreqLimiter(5) #频率限制(s)
dlmt_ = 20 # 每日次数限制
dlmt = DailyNumberLimiter(dlmt_)

sv_help = '''
【AI绘图数据库】
-----------------------------------------------------------------
-【上传【参数】】  上传图片和tag至数据库内，[参数]为ai绘图的指令
-【'回复'[bot昵称]上传】  同为上传
-【炼金大全】  查询炼金手册全部内容
-【炼金手册[序号]】  查询炼金手册内容，[序号]为页数，每页显示8张
-【查看配方[序号]】  查询炼金配方内容，[序号]为图片标签
-【修改配方[序号][tags]】  修改炼金配方标签内容，[序号]为图片标签
[tags]为tags:xxx,xxx,xxx,xxx,xxx,xxx
-【使用配方]序号]】  使用炼金配方内容，[序号]为图片标签
-【删除配方[序号]】  删除炼金配方内容，[序号]为图片标签
PS:上传仅限管理员使用，删除仅限超级管理员使用
-----------------------------------------------------------------
-【测试[tags]】  进行ai绘图，返回种子和分数
-【分数排行[序号]】  查看图片分数排行，[序号]为TOP数
-【分数排行总榜】  查看全部图片分数排行
-【清理分数排行】  清除除排行前15的所有数据
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

@sv.on_fullmatch(('帮助', '数据库帮助', '绘图帮助'), only_to_me=True)
async def bangzhu(bot, ev):
    await bot.send(ev, await wordimage(sv_help), at_sender=True)

lock = Lock()
curpath = dirname(__file__)
image_list_db = join(curpath, 'save_tags.db')   #保存tags数据库
score_path = join(curpath,'scoreDB.db')
score_image = join(curpath,'ScoreImage')
save_image_path= join(curpath,'SaveImage')  # 保存图片路径
font_path = join(curpath,"fz.TTF")  #字体文件路径

class ScoreCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(score_path), exist_ok=True)
        self._score_table()
        if not exists(score_image):
            os.mkdir(score_image)
        
    def _connect(self):
        return sqlite3.connect(score_path)

    def _score_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS aiscore
                        (分数 TINYINT,
                        图片 BLOB,
                        标签 TEXT,
                        种子 INT,
                        形状 CHAR);''')
        except:
            raise Exception('创建表发生错误')    
        
    def _add_score(self,score,image,tags,seed,shape):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO aiscore VALUES (?,?,?,?,?)",(score,image,tags,seed,shape))
            return 1
        except:
            raise Exception('添加分数发生错误')
    
    def _delete_score(self):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT 图片 FROM aiscore WHERE rowid NOT IN ( SELECT rowid FROM aiscore where rowid ORDER BY 分数 desc LIMIT 15)").fetchall()
                num=(len(r))
                for i in range(0,len(r)):
                    os.remove(r[i][0])
                conn.execute("DELETE FROM aiscore WHERE rowid NOT IN ( SELECT rowid FROM aiscore where rowid ORDER BY 分数 desc LIMIT 15)")
            return num
        except:
            raise Exception('清除分数发生错误')

    def _get_score_list(self, num):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT 分数,图片 FROM aiscore WHERE rowid ORDER BY 分数 desc LIMIT ?",(num,)).fetchall()           
            return r if r else {}
        except:
            raise Exception('分数排行榜发生错误')

    def _vacuum_score(self):
        try:
            conn = self._connect()
            conn.execute('vacuum')
            conn.close
        except:
            raise Exception('刷新分数发生错误') 

    def _get_score_rowid(self):
        try:
            with self._connect() as conn:
                r = conn.execute("select rowid from aiscore order by rowid desc limit 1").fetchone()
            return r[0] if r else 0
        except:
            raise Exception('分数总数发生错误')

class ImageCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(image_list_db), exist_ok=True)
        self._create_table()
        
    def _connect(self):
        return sqlite3.connect(image_list_db)
        
    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS aitag
                        (权重 TINYINT,
                        形状 CHAR,
                        标签 TEXT,
                        种子 INT,
                        图片 BLOB);''')
        except:
            raise Exception('创建表发生错误')
            
    def _add_image(self, scale, size,tags,seed,saveconfig):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO aitag VALUES (?,?,?,?,?)",(scale,size,tags,seed,saveconfig))
            return "添加配方成功！"
        except:
            raise Exception('添加配方发生错误')

    def _update_image(self, tags,rowid):
        try:
            with self._connect() as conn:
                conn.execute("UPDATE aitag SET 标签 = ? WHERE rowid=?",(tags,rowid,))
            return f"修改配方{rowid}成功"
        except:
            raise Exception('修改配方发生错误')

    def _delete_image(self, rowid):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT 图片 FROM aitag WHERE rowid=?", (rowid,)).fetchone()
                os.remove(r[0])
                conn.execute("DELETE FROM aitag WHERE rowid=?", (rowid,))
            return f"删除配方{rowid}成功"
        except:
            raise Exception('删除配方发生错误')

    def _vacuum_image(self):
        try:
            conn = self._connect()
            conn.execute('vacuum')
            conn.close
        except:
            raise Exception('刷新配方发生错误')
            
    def _get_image(self, rowid):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT * FROM aitag WHERE rowid=?", (rowid, )).fetchone()
            return 0 if r is None else r
        except:
            raise Exception('查找配方发生错误')
    
    def _get_image_list(self, num):
        try:
            up_index=(num-1)*8-1
            down_index=num*8
            with self._connect() as conn:
                r = conn.execute("SELECT rowid,图片 FROM aitag WHERE rowid BETWEEN ? AND ?",(up_index,down_index)).fetchall()            
            return r if r else {}
        except:
            raise Exception('炼金手册发生错误')

    def _get_all_image_list(self):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    "select rowid,图片 FROM aitag").fetchall()        
            return r if r else {}
        except:
            raise Exception('炼金大全发生错误')

    def _get_rowid(self):
        try:
            with self._connect() as conn:
                r = conn.execute("select rowid from aitag order by rowid desc limit 1").fetchone()
            return r[0] if r else 0
        except:
            raise Exception('查找配方号发生错误')

class SaveClass:
    def __init__(self):
        if not exists(save_image_path):
            os.mkdir(save_image_path)
    
    def _re_image_msg(self,msg):
        try:
            image_url = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(msg))
            pic_url = image_url.group(2)
            return 0 if not pic_url else pic_url
        except:
            raise Exception('图片链接发生错误')

    def _save_image(self,url):
        try:
            response = req.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            image_base64 = base64.b64encode(BytesIO(response.content).read())
            imgdata=base64.b64decode(image_base64)
            datetime = calendar.timegm(time.gmtime())
            saveconfig = join(save_image_path, f'{str(datetime)}.png')
            size=f"{img.width}x{img.height}"
            pic = open(saveconfig, "wb")
            pic.write(imgdata)
            pic.close()
            return size,saveconfig
        except:
            raise Exception('图片获取发生错误')
            
    def _save_info(self,image,msg,num):
        try:
            try:
                seed_list1=str(msg).split(f"scale:")
                seed_list2=seed_list1[0].split('eed:')
                seed=seed_list2[1].strip ()
            except:
                raise Exception('种子出错')
            try:
                scale_list=seed_list1[1].split(f"tags:")
                scale=scale_list[0].strip()
            except:
                raise Exception('权重出错')
            try:
                tags_list=scale_list[1].split(f"&")
                tags=tags_list[0].strip()
            except:
                tags_list=scale_list[1].strip()
                raise Exception('标签格式出错')
            if num == 1:
                url = self._re_image_msg(str(image))
                size,saveconfig = self._save_image(url)
            else:
                size,saveconfig = self._save_image(image)
            ImageCounter()._add_image(scale, size,tags,seed,saveconfig)
            num=ImageCounter()._get_rowid()
            return f"配方保存成功,编号：{num}"
        except:
            raise Exception('配方保存发生错误')

class Another_code():
    def _size_to_shape(self,size):
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

    def _Imt_check(self,uid):
        if not lmt.check(uid):
            msg = f"魔力回复中！(剩余 {int(lmt.left_time(uid)) + 1}秒)"
            return msg
        else:
            return 0

    def _dlmt_check(self,uid):
        if not dlmt.check(uid):
            msg = f"今日魔力已经用完，请明天再来~"
            return msg
        else:
            return 0

@sv.on_prefix(('上传'))
async def upload_header(bot, ev):
    global lock
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, '上传配方仅限管理员使用', at_sender=True)
        return
    async with lock:
        try:
            for i in ev.message:
                if i.type == "image":
                    image=str(i)
                    break
        except:
            await bot.send(ev,"未获取到图片",at_sender=True)
            return
        try:
            msg = SaveClass()._save_info(image,ev.message,1)
            await bot.send(ev, msg, at_sender=True)
        except Exception as e:
            await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
            return

#获取机器人昵称
if type(NICKNAME) == str:
    NICKNAME = [NICKNAME]

#通过'回复'来进行上传
@sv.on_message('group')
async def replymessage(bot, ev: CQEvent):
    seg=ev.message[0]
    if seg.type != 'reply':
        return
    tmid = seg.data['id']
    cmd = ev.message.extract_plain_text()
    flag1 = 0
    flag2 = 0
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
    if not (flag1 and flag2):
        return
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev,f"仅限管理员上传！", at_sender=True)
        return
    try:
        tmsg = await bot.get_msg(self_id=ev.self_id, message_id=int(tmid))
    except ActionFailed:
        await bot.send(ev, '该消息已过期，请重新转发~')
        return
    image_url = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(tmsg["message"]))
    if not image_url:
        await bot.send(ev, '未找到图片~')
        return
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
    try:
        msg = SaveClass()._save_info(pic_url,tmsg["message"],0)
        await bot.send(ev, msg, at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return

@sv.on_rex((r'^炼金手册([1-9]\d*)$'))
async def alchemy_book(bot, ev):
    match = ev['match']
    page=int(match.group(1))
    image_list=ImageCounter()._get_image_list(page)
    if image_list == {}:
        await bot.send(ev, f"手册该页没有配方哦", at_sender=True)
        return
    try:
        target = Image.new('RGB', (1920,1080),(255,255,255))
        i=0
        for index in range(0,8):
            try:
                image_msg=image_list[index]
            except:
                break
            rowid = image_msg[0]
            image_path=image_msg[1]
            region = Image.open(image_path)
            region = region.convert("RGB")
            region = region.resize((int(region.width/2),int(region.height/2)))
            font = ImageFont.truetype(font_path, 36)  # 设置字体和大小
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
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_fullmatch(('清理分数排行'))
async def clear_score_rank(bot,ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, '清理分数排行榜仅限管理员使用', at_sender=True)
        return
    try:
        num = ScoreCounter()._delete_score()
        ScoreCounter()._vacuum_score()
        await bot.send(ev,f'已清理{num}条数据')
    except Exception as e:
        await bot.send(ev, f'报错:{e}', at_sender=True)

@sv.on_fullmatch(('分数排行总榜'))
async def score_all_rank(bot, ev):
    rowid=ScoreCounter()._get_score_rowid()
    image_list=ScoreCounter()._get_score_list(rowid)
    add_page=1040*((rowid-1)//8+1)
    try:
        target = Image.new('RGB', (1900,add_page),(255,255,255))
        for index in range(0,rowid):
            image_msg=image_list[index]
            score = image_msg[0]
            image_path=image_msg[1]
            region = Image.open(image_path)
            region = region.convert("RGB")
            region = region.resize((int(region.width/2),int(region.height/2)))
            font = ImageFont.truetype(font_path, 36)  # 设置字体和大小
            draw = ImageDraw.Draw(target)
            row=index//4+1  #行
            column= index%4+1   #列
            target.paste(region,(80*column+384*(column-1),50+100*(row-1)+384*(row-1)))
            draw.text((80*column+384*(column-1)+int(region.width/2)-18,80+100*(row-1)+384*(row-1)+region.height),str(score).replace(',',''),font=font,fill = (0, 0, 0))
        result_buffer = BytesIO()
        target.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
        imgByteArr = int((len(result_buffer.getvalue()))/1024000)
        if imgByteArr>=5:
            target.resize(int(target.width/2),int(target.height/2))
        imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
        resultmes = f"[CQ:image,file={imgmes}]"
        await bot.send(ev,resultmes)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^分数排行([1-9]\d*)$'))
async def score_rank(bot, ev):
    match = ev['match']
    page=int(match.group(1))
    rowid=ScoreCounter()._get_score_rowid()
    if rowid < page:
        await bot.send(ev, f"目前只能查看前{rowid}的分数排名", at_sender=True)
        return
    image_list=ScoreCounter()._get_score_list(page)
    add_page=1040*((page-1)//8+1)
    try:
        target = Image.new('RGB', (1900,add_page),(255,255,255))
        for index in range(0,page):
            image_msg=image_list[index]
            score = image_msg[0]
            image_path=image_msg[1]
            region = Image.open(image_path)
            region = region.convert("RGB")
            region = region.resize((int(region.width/2),int(region.height/2)))
            font = ImageFont.truetype(font_path, 36)  # 设置字体和大小
            draw = ImageDraw.Draw(target)
            row=index//4+1  #行
            column= index%4+1   #列
            target.paste(region,(80*column+384*(column-1),50+100*(row-1)+384*(row-1)))
            draw.text((80*column+384*(column-1)+int(region.width/2)-18,80+100*(row-1)+384*(row-1)+region.height),str(score).replace(',',''),font=font,fill = (0, 0, 0))
        result_buffer = BytesIO()
        target.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
        imgByteArr = int((len(result_buffer.getvalue()))/1024000)
        if imgByteArr>=5:
            target.resize(int(target.width/2),int(target.height/2))
        imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
        resultmes = f"[CQ:image,file={imgmes}]"
        await bot.send(ev,resultmes)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)


@sv.on_fullmatch(('炼金大全'))
async def alchemy_book_all(bot, ev):
    image_list=ImageCounter()._get_all_image_list()
    if image_list == {}:
        await bot.send(ev, f"炼金手册里没有配方哦", at_sender=True)
        return
    image_len=int(ImageCounter()._get_rowid())
    add_page=1050*((image_len-1)//8+1)
    try:
        target = Image.new('RGB', (1900,add_page),(255,255,255))
        for index in range(0,image_len):
            image_msg=image_list[index]
            rowid = image_msg[0]
            image_path=image_msg[1]
            region = Image.open(image_path)
            region = region.convert("RGB")
            region = region.resize((int(region.width/2),int(region.height/2)))
            font = ImageFont.truetype(font_path, 36)  # 设置字体和大小
            draw = ImageDraw.Draw(target)
            row=index//4+1  #行
            column= index%4+1   #列
            target.paste(region,(80*column+384*(column-1),50+100*(row-1)+384*(row-1)))
            draw.text((80*column+384*(column-1)+int(region.width/2)-18,80+100*(row-1)+384*(row-1)+region.height),str(rowid).replace(',',''),font=font,fill = (0, 0, 0))
        result_buffer = BytesIO()
        target.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
        imgByteArr = int((len(result_buffer.getvalue()))/1024000)
        if imgByteArr>=5:
            target.resize(int(target.width/2),int(target.height/2))
        imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
        resultmes = f"[CQ:image,file={imgmes}]"
        await bot.send(ev,resultmes)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^查看配方([1-9]\d*)'))
async def view_recipe(bot, ev):
    uid = str(ev['user_id'])
    cd=Another_code()._Imt_check(uid)
    if cd != 0:
        await bot.send(ev,cd,at_sender=True)
        return
    else:
        lmt.start_cd(uid,10)
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = ImageCounter()._get_image(rowid)
        if image_msg == 0:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        scale=image_msg[0]
        size=image_msg[1]
        tags=image_msg[2]
        image_path=image_msg[4]
        #seed=image_msg[3]
        pic = open(image_path, "rb")
        base64_str = base64.b64encode(pic.read())
        imgmes = 'base64://' + base64_str.decode()
        resultmes = f"[CQ:image,file={imgmes}]"
        pic.close()
        shape=Another_code()._size_to_shape(size)
        msg=f"配方序号为:{rowid}\n{resultmes}\nai绘图{tags}&scale={scale}&shape={shape}"
        await bot.send(ev,msg,at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^使用配方([1-9]\d*)'))
async def generate_recipe(bot, ev):
    uid = str(ev['user_id'])
    dImt_msg=Another_code()._dlmt_check(uid)
    if dImt_msg != 0:
        await bot.send(ev, dImt_msg, at_sender=True)
        return
    else:
        dlmt.increase(uid)
    Imt_msg=Another_code()._Imt_check(uid)
    if Imt_msg != 0:
        await bot.send(ev, Imt_msg, at_sender=True)
        return
    else:
        lmt.start_cd(uid)
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = ImageCounter()._get_image(rowid)
        if image_msg == 0:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        image_list=ImageCounter()._get_image(rowid)
        scale=image_list[0]
        size=image_list[1]
        shape=Another_code()._size_to_shape(size)
        tags=image_list[2]
        msg=f"{tags}&scale={scale}&shape={shape}".replace('&r18=1','')
        await bot.send(ev, f"\n正在炼金中，请稍后...\n(今日剩余{dlmt_-int(dlmt.get_num(uid))}次)", at_sender=True)
        image,score = await gen_pic(msg)
        await bot.send(ev,image+f"\n分数:{score}",at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^修改配方([1-9]\d*)'))
async def update_recipe(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, '修改配方仅限管理员使用', at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = ImageCounter()._get_image(rowid)
        if image_msg == 0:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        tags_list1=str(ev.message).split('tags:')
        tags_list2=tags_list1[1].split('&')
        tags=tags_list2[0]
        print(tags)
        msg=ImageCounter()._update_image(tags,rowid)
        await bot.send(ev,msg,at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^删除配方([1-9]\d*)'))
async def delete_recipe(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, '删除配方仅限超级管理员使用', at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = ImageCounter()._get_image(rowid)
        if image_msg == 0:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        msg=ImageCounter()._delete_image(rowid)
        ImageCounter()._vacuum_image()
        await bot.send(ev,msg,at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

async def gen_pic(text):
    try:
        get_url = str(word2img_url + text + token).replace('amp;','')
        res = await aiorequests.get(get_url)
        image = await res.content
        load_data = json.loads(re.findall('{"steps".+?}', str(image))[0])
        image_b64 = 'base64://' + str(base64.b64encode(image).decode())
        try:
            score = (await porn_pic_index(str(base64.b64encode(image).decode())))["value"]
        except:
            score = 0
        mes = f"[CQ:image,file={image_b64}]"
        mes += f'\nseed:{load_data["seed"]}'       
        """ mes += f'\tscale:{load_data["scale"]}\n'
        mes += f'tags:{text}' """
        return mes,score
    except Exception as e:
        print(e)
        return f"炼金失败了"

async def wordimage(word):
    bg = Image.new('RGB', (950,550), color=(255,255,255))
    font = ImageFont.truetype(font_path, 30)  # 设置字体和大小
    draw = ImageDraw.Draw(bg)
    draw.text((10,5), word, fill="#000000", font=font)
    result_buffer = BytesIO()
    bg.save(result_buffer, format='JPEG', quality=100)
    imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
    resultmes = f"[CQ:image,file={imgmes}]"
    return resultmes

@sv.on_prefix(('测试'))
async def get_image(bot,ev):
    url = (word2img_url + str(ev.message) + token).replace('amp;','')
    res = await aiorequests.get(url)
    image = await res.content
    load_data = json.loads(re.findall('{"steps".+?}', str(image))[0])
    seed=load_data['seed']
    image_base64=str(base64.b64encode(image).decode())
    image_b64 = 'base64://' + image_base64
    try:
        score = (await porn_pic_index(image_base64))["value"]
    except:
        score = 0
    resultmes = f"[CQ:image,file={image_b64}]"
    if score <460 and score !=0:
        try:
            datetime = calendar.timegm(time.gmtime())
            img = Image.open(BytesIO(image)).convert("RGB")
            saveconfig = join(score_image, f'{str(datetime)}.png')
            size=f"{img.width}x{img.height}"
            pic = open(saveconfig, "wb")
            pic.write(image)
            pic.close()
        except Exception as e:
            await bot.send(ev,f"报错:{e}",at_sender=True)
            return
        try:
            shape = Another_code()._size_to_shape(size)
            tags=(str(ev.message).split('&'))[0]
            ScoreCounter()._add_score(score,saveconfig,tags,seed,shape)
            await bot.send(ev,resultmes+f"\nseed:{seed}\t分数:{score}",at_sender=True)
        except Exception as e:
            await bot.send(ev,f"报错:{e}",at_sender=True)
            return
    elif score ==0:
        await bot.send(ev,"图片质量堪忧,不予显示",at_sender=True)
    else:
        await bot.send(ev,"图片太涩了,不予显示",at_sender=True)