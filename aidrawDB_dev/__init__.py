from asyncio import Lock
from os.path import dirname, join, exists
from hoshino import Service,priv,aiorequests
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.config import NICKNAME,SUPERUSERS
from aiocqhttp.exceptions import ActionFailed
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
from base64 import decode,b64encode
from .default_config import config_default
from .config import get_config
from .db_code import DBCounter
from .image_draw import *
from .another_code import *


import traceback
import json
import time,calendar
import threading
import re
import requests as req
import sqlite3
import os

sv_help = '''
【AI绘图数据库】
-----------------------------------------------------------
-【上传【参数】】  上传图片和tag至数据库内，[参数]为ai绘图的指令
-【'回复'[bot昵称]上传】  同为上传
-【炼金大全】  查询炼金手册全部内容
-【炼金手册[序号]】  查询炼金手册内容，[序号]为页数
-【查看配方[序号]】  查询炼金配方内容，[序号]为图片标签
-【使用配方]序号]】  使用炼金配方内容，[序号]为图片标签
-【点赞配方]序号]】  点赞炼金配方内容，[序号]为图片标签
-【删除配方[序号]】  删除炼金配方内容，[序号]为图片标签
PS:上传仅限管理员使用，删除仅限超级管理员使用
-----------------------------------------------------------
-【测试[tags]】  进行ai绘图，返回种子和分数
-【分数排行[序号]】  查看图片分数排行，[序号]为TOP数
-【分数排行总榜】  查看全部图片分数排行
-【清理分数排行】  清除除排行前15的所有数据
'''
sv = Service(
    name = 'AI绘图安全版',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #是否可见
    enable_on_default = True, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(('帮助', '数据库帮助', '绘图帮助'), only_to_me=True)
async def bangzhu(bot, ev):
    await bot.send(ev, await word_image(sv_help), at_sender=True)

pathcfg = os.path.join(os.path.dirname(__file__), 'config.json')
if not os.path.exists(pathcfg):
	try:
		with open(pathcfg, 'w') as cfgf:
			json.dump(config_default, cfgf, ensure_ascii=False, indent=4)
			hoshino.logger.error('[WARNING]未找到配置文件，已根据默认配置模板创建，请打开插件目录内config.json查看和修改。')
	except:
		hoshino.logger.error('[ERROR]创建配置文件失败，请检查插件目录的读写权限及是否存在config.json。')
		traceback.print_exc()

lock=Lock()
tlmt = DailyNumberLimiter(get_config('base', 'daily_max'))
flmt = FreqLimiter(get_config('base', 'freq_limit'))
flmt_cd =get_config('base', 'freq_cd')

word2img_url = f"{get_config('NovelAI', 'api')}got_image?tags="
token = f"&token={get_config('NovelAI', 'token')}"

default_tags = get_config('default_tags', 'tags')

ntags_stats = get_config('default_ntags', 'ntags_stats')
default_ntags = get_config('default_ntags', 'ntags')

bot_name = get_config('default', 'bot_name')
bot_uid = get_config('default', 'bot_uid')
trigger_word = get_config('default','trigger_word')
    
cd_stats = 0

def time_handler():
    global cd_stats
    cd_stats = 0

def TimerStart(num):
    global cd_stats
    if cd_stats == 0 and num==0:
        cd_stats=1
        timer=threading.Timer(12,time_handler)
        timer.start()

async def check_lmt(uid, num,cd):
    if uid in SUPERUSERS:
        return 0, ''
    if not tlmt.check(uid):
        return 1, f"今日魔力已经用完，请明天再来~"
    if num > 1 and (get_config('base', 'daily_max') - tlmt.get_num(uid)) < num:
        return 1, f"今日剩余炼金次数为{get_config('base', 'daily_max') - tlmt.get_num(uid)}次"
    if not flmt.check(uid):
        return 1, f'魔力回复中！{round(flmt.left_time(uid))}秒后再来吧~'
    tlmt.increase(uid, num)
    flmt.start_cd(uid,cd)
    return 0, ''

@sv.on_prefix(('上传'))
async def upload_header(bot, ev):
    global lock
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, '上传配方仅限管理员使用', at_sender=True)
        return
    async with lock:
        try:
            image=''
            for i in ev.message:
                if i.type == "image":
                    image=str(i)
                    break
            if image == '':
                await bot.send(ev,"未获取到图片",at_sender=True)
                return
            pic_url = await re_url(image)
            base64_en,size=await gpic_get(pic_url)
            image_base64=str(base64_en).replace("b'","").replace("'","")
            seed,scale,tags,shape,ntags=await re_info(str(ev.message).replace("amp;",""))
            tags,error_msg,tags_guolu=await process_tags(tags)
            if shape == '':
                shape = await size_to_shape(size)
            if scale == '':
                scale = 11
            tags=tags.split(']')[1]
            DBCounter()._insert_tagdata(scale,shape,tags,seed,image_base64,0,ntags)
            rowid=DBCounter()._get_tagrowid()
            await bot.send(ev, f'已保存配方为:{rowid}', at_sender=True)
        except Exception as e:
            traceback.print_exc()
            await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
            return

#通过'回复'来进行上传
@sv.on_message('group')
async def another_replymessage(bot, ev):
    try:
        if not priv.check_priv(ev, priv.ADMIN):
            return
        pic_url,tmsg,flag = await reply_msg(bot,ev)
        if pic_url == 0:
            return
        base64_en,size=await gpic_get(pic_url)
        image_base64=base64_en
        if flag == 1:
            seed,scale,tags,shape,ntags=await another_info(str(tmsg["message"]).replace("amp;",""))
        else:
            last_msg=re.split("self_id:",str(tmsg["message"]))
            for index,i in enumerate(last_msg):
                if index == 1:
                    now_msg=i.split('msg_id:')
                    self_id = now_msg[0].strip()
                    msg_id =now_msg[1].strip()
            my_msg = await bot.get_msg(self_id=int(self_id), message_id=int(msg_id))
            seed,scale,tags,shape,ntags=await re_info(str(my_msg["message"]).replace("amp;",""))
            tags=tags.replace(trigger_word,'')
            tags,error_msg,tags_guolu=await process_tags(tags)
        if shape == '':
            shape = await size_to_shape(size)
        if scale == '':
            scale = 11
        DBCounter()._insert_tagdata(scale,shape,tags,seed,image_base64,0,ntags)
        rowid=DBCounter()._get_tagrowid()
        await bot.send(ev, f'已保存配方为:{rowid}', at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return

@sv.on_rex((r'^炼金手册([1-9]\d*)$'))
async def alchemy_book(bot, ev):
    uid = str(ev['user_id'])
    result, msg = await check_lmt(uid,0,10)
    if result != 0:
        await bot.send(ev, msg,at_sender=True)
        return
    match = ev['match']
    page=int(match.group(1))
    try:
        msg= await imagelist_once_draw(page,0)
        await bot.send(ev,msg)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_fullmatch(('炼金大全'))
async def alchemy_allbook(bot, ev):
    try:
        uid = str(ev['user_id'])
        result, msg = await check_lmt(uid,0,10)
        if result != 0:
            await bot.send(ev, msg,at_sender=True)
            return
        rowid=DBCounter()._get_tagrowid()
        image=await imagelist_all_draw(rowid,0)
        msg = await render_forward_msg("炼金大全如下:",image,bot_uid,bot_name)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=msg)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_fullmatch(('分数总榜'))
async def score_all_rank(bot, ev):
    try:
        uid = str(ev['user_id'])
        result, msg = await check_lmt(uid,0,10)
        if result != 0:
            await bot.send(ev, msg,at_sender=True)
            return
        rowid=DBCounter()._get_scorerowid()
        image=await imagelist_all_draw(rowid,1)
        msg = await render_forward_msg("分数总榜如下:",image,bot_uid,bot_name)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=msg)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_prefix((trigger_word))
async def gen_pic(bot, ev):
    if cd_stats == 1:
        await bot.send(ev,"公共CD中，请等待10秒",at_sender=True)
        return
    uid = ev['user_id']
    num = 0
    cd=int(flmt_cd)
    result, msg = await check_lmt(uid, num,cd)
    score=''
    if result != 0:
        await bot.send(ev, msg,at_sender=True)
        return
    tags = ev.message.extract_plain_text().strip()
    return_msg = await is_contain_chinese(tags)
    if return_msg == True:
        await bot.send(ev, f"tag有误", at_sender=True)
        return
    tags,error_msg,tags_guolu=await process_tags(tags)
    if len(error_msg):
        await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolu):
        await bot.send(ev, f"已过滤：{tags_guolu}", at_sender=True)
    if not len(tags):
        tags = default_tags
        await bot.send(ev, f"将使用默认tag：{default_tags}", at_sender=True)
    try:
        seed,scale,tags_now,shape,ntags=await re_info(str(ev.message).replace("amp;",""))
        if ntags == '' and ntags_stats:
            tags=tags+f'&ntags={default_ntags}'
        get_url = str(word2img_url + tags + token).replace("amp;","").replace("&r18=1",'').replace("&R18=1",'')
        base64_en,pic,seed,scale,size=await http_get(get_url)
        if type(scale) == str:
            await bot.send(ev,scale,at_sender=True)
            return
        if type(seed) == str:
            TimerStart(0)
            await bot.send(ev,seed,at_sender=True)
            return
        if base64_en==pic==seed==scale==size==0:
            TimerStart(0)
            await bot.send(ev, f"网络或接口问题未获取到图片,自动重试", at_sender=True)
            for i in range(0,10):
                flmt.start_cd(uid,11)
                base64_en,pic,seed,scale,size=await http_get(get_url)
                await asyncio.sleep(11)
                if base64_en != 0:
                    break
                if i == 9:
                    await bot.send(ev, f"重试{i+1}次无果,请自行重试", at_sender=True)
                    return
        image_base64=str(base64_en).replace("b'","").replace("'","")
        if shape == '':
            shape = await size_to_shape(size)
        if scale == '':
            scale = 11
        score = await check_imgscore(image_base64)
        if type(score) == int:
            if score != -1:
                DBCounter()._insert_scoredata(scale,shape,tags_now,seed,image_base64,score,ntags)
            else:
                score = '无'
        else:
            await bot.send(ev, score, at_sender=True)
            return
        mes = f"[CQ:image,file={pic}]\n"
        mes += f'seed:{seed}\t'
        mes += f'score:{score}\n'
        mes += f'self_id:{str(ev.self_id)}\t'
        mes += f'msg_id:{str(ev.message_id)}'
        await bot.send(ev, f'{mes}', at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^查看配方([1-9]\d*)'))
async def view_recipe(bot, ev):
    uid = str(ev['user_id'])
    result, msg = await check_lmt(uid,0,10)
    if result != 0:
        await bot.send(ev, msg,at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = DBCounter()._select_oneall_tagdata(rowid)
        if image_msg == {}:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        scale=str(image_msg[0]).strip()
        shape=str(image_msg[1]).strip()
        tags=str(image_msg[2]).strip()
        image_base64=image_msg[4]
        thumb=image_msg[5]
        ntags=str(image_msg[6]).strip()
        region = Image.open(BytesIO(base64.b64decode(image_base64)))
        region = region.convert("RGB")
        result_buffer = BytesIO()
        region.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
        imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
        resultmes = f"[CQ:image,file={imgmes}]"
        msg=f"配方序号为:{rowid}\t点赞:{thumb}\n{resultmes}\n{trigger_word}{tags}&scale={scale}&shape={shape}&ntags={ntags}"
        await bot.send(ev,msg,at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)

@sv.on_rex((r'^分数配方([1-9]\d*)'))
async def score_recipe(bot, ev):
    uid = str(ev['user_id'])
    result, msg = await check_lmt(uid,0,10)
    if result != 0:
        await bot.send(ev, msg,at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = DBCounter()._select_oneall_scoredata(rowid)
        if image_msg == {}:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        scale=str(image_msg[0]).strip()
        shape=str(image_msg[1]).strip()
        tags=str(image_msg[2]).strip()
        image_base64=image_msg[4]
        score=image_msg[5]
        ntags=str(image_msg[6]).strip()
        region = Image.open(BytesIO(base64.b64decode(image_base64)))
        region = region.convert("RGB")
        result_buffer = BytesIO()
        region.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
        imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
        resultmes = f"[CQ:image,file={imgmes}]"
        msg=f"配方序号为:{rowid}\t分数:{score}\n{resultmes}\n{trigger_word}{tags}&scale={scale}&shape={shape}&ntags={ntags}"
        await bot.send(ev,msg,at_sender=True)
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)  

@sv.on_rex((r'^使用配方([1-9]\d*)'))
async def generate_recipe(bot, ev):
    uid = str(ev['user_id'])
    cd=int(flmt_cd)
    result, msg = await check_lmt(uid,0,cd)
    if result != 0:
        await bot.send(ev, msg,at_sender=True)
        return
    try:
        match = ev['match']
        rowid=int(match.group(1))
        image_msg = DBCounter()._select_oneall_tagdata(rowid)
        if image_msg == {}:
            await bot.send(ev, f"未找到{rowid}配方哦", at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
        return
    try:
        scale=str(image_msg[0]).strip()
        shape=str(image_msg[1]).strip()
        tags=str(image_msg[2]).strip()
        thumb=image_msg[5]
        ntags=str(image_msg[6]).strip()
        send_msg=f'{tags}&shape={shape}&scale={scale}&ntags={ntags}'
        tags,error_msg,tags_guolu=await process_tags(send_msg)
        if len(error_msg):
            await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
        if len(tags_guolu):
            await bot.send(ev, f"已过滤：{tags_guolu}", at_sender=True)
        if not len(tags):
            tags = default_tags
            await bot.send(ev, f"将使用默认tag：{default_tags}", at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
    try:
        get_url = str(word2img_url + tags + token).replace("amp;","")
        base64_en,pic,seed,scale,size=await http_get(get_url)
        if base64_en==pic==seed==scale==size==0:
            await bot.send(ev, f"网络或接口问题未获取到图片,自动重试", at_sender=True)
            for i in range(0,10):
                flmt.start_cd(uid,10)
                base64_en,pic,seed,scale,size=await http_get(get_url)
                await asyncio.sleep(10)
                if base64_en != 0:
                    break
                if i == 9:
                    await bot.send(ev, f"重试{i+1}次无果,请自行重试", at_sender=True)
                    return
        image_base64=str(base64_en).replace("b'","").replace("'","")
        score = await check_imgscore(image_base64)
        if type(score) == int:
            if score != -1:
                DBCounter()._insert_scoredata(scale,shape,tags,seed,image_base64,score,ntags)
            else:
                score = '无'
        else:
            await bot.send(ev, score, at_sender=True)
            return
        mes = f"[CQ:image,file={pic}]\n"
        mes += f'seed:{seed}\t'
        mes += f'score:{score}\n'
        await bot.send(ev, f'{mes}', at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev, f"发生错误，原因：{e}", at_sender=True)
    
@sv.on_rex((r'^点赞配方([1-9]\d*)'))
async def img_thumb(bot, ev):
    try:
        match = ev['match']
        rowid=int(match.group(1))
        if rowid > DBCounter()._get_tagrowid():
            await bot.send(ev, f"配方{rowid}不存在哦", at_sender=True)
            return
        msg = DBCounter()._add_thumb(rowid)
        await bot.send(ev, msg, at_sender=True)
    except Exception as e:
        await bot.send(ev, f"报错:{e}",at_sender=True)
        traceback.print_exc()

@sv.on_rex((r'^删除配方([1-9]\d*)'))
async def del_img(bot, ev):
    try:
        if not priv.check_priv(ev,priv.SUPERUSER):
            await bot.finish(ev, "只有超管才能删除", at_sender=True)
        match = ev['match']
        rowid=int(match.group(1))
        if rowid > DBCounter()._get_tagrowid():
            await bot.send(ev, f"配方{rowid}不存在哦", at_sender=True)
            return
        msg = DBCounter()._delete_tagdata(rowid)
        DBCounter()._vacuum_data()
        await bot.send(ev, msg, at_sender=True)
    except Exception as e:
        await bot.send(ev, f"报错:{e}",at_sender=True)
        traceback.print_exc()

@sv.on_rex((r'^保留分数([1-9]\d*)'))
async def del_img(bot, ev):
    try:
        if not priv.check_priv(ev,priv.SUPERUSER):
            await bot.finish(ev, "只有超管才能删除", at_sender=True)
        match = ev['match']
        rowid=int(match.group(1))
        if rowid > DBCounter()._get_scorerowid():
            await bot.send(ev, f"配方{rowid}不存在哦", at_sender=True)
            return
        msg = DBCounter()._delete_scoredata(rowid)
        DBCounter()._vacuum_data()
        await bot.send(ev, msg, at_sender=True)
    except Exception as e:
        await bot.send(ev, f"报错:{e}",at_sender=True)
        traceback.print_exc()

@sv.on_fullmatch(('刷新数据库'))
async def del_img(bot, ev):
    try:
        if not priv.check_priv(ev,priv.SUPERUSER):
            await bot.finish(ev, "只有超级管理员才能使用", at_sender=True)
        DBCounter()._vacuum_data()
        await bot.send(ev, '清理完毕', at_sender=True)
    except Exception as e:
        await bot.send(ev, f"报错:{e}",at_sender=True)
        traceback.print_exc()
