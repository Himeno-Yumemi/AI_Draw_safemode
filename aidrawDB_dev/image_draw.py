import base64
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
from .db_code import DBCounter
from os.path import dirname, join
from .config import get_config

quality = get_config('default', 'quality')
font_path = join(dirname(__file__),"fz.TTF")  #字体文件路径

#绘制总图
async def imagelist_all_draw(rowid,num):
    try:
        #炼金总表
        if num == 0:    
            image_list=DBCounter()._select_all_tagdata()
            if image_list == {}:
                return f"炼金大全为空"
        #分数总表
        else:
            image_list=DBCounter()._select_all_scoredata(rowid)
            if image_list == {}:
                return f"分数表为空"
        result_img=''
        page=(rowid-1)//24+1
        for i in range(0,page):
            if (rowid-24*i)//4>=6:
                target = Image.new('RGB', (1920,490*6),(255,255,255))
            else:
                target = Image.new('RGB', (1920,490*((rowid-24*i)//4+1)),(255,255,255))
            for index in range(0+i*24,24+i*24):
                try:
                    image_info=image_list[index]
                except:
                    break
                id = image_info[0]
                image=image_info[1]
                info=image_info[2]
                if num == 0:
                    bianhao=f'编号:{id}'
                    dianzan=f'点赞:{info}'
                else:
                    bianhao=f'编号:{id}'
                    dianzan=f'分数:{info}'
                row=(index-i*24)//4+1  #行
                column= (index-i*24)%4+1   #列
                region = Image.open(BytesIO(base64.b64decode(image)))
                region = region.convert("RGB")
                region = region.resize((int(region.width/2),int(region.height/2)))
                font = ImageFont.truetype(font_path, 24)  # 设置字体和大小
                draw = ImageDraw.Draw(target)
                target.paste(region,(77*column+384*(column-1),50*row+36*(row-1)+384*(row-1)))
                draw.text((77*column+384*(column-1),24+50*row+36*(row-1)+384*(row-1)+region.height),str(bianhao).replace(',',''),font=font,fill = (0, 0, 0))
                draw.text((77*column+384*(column-1)+int(region.width/2),24+50*row+36*(row-1)+384*(row-1)+region.height),str(dianzan).replace(',',''),font=font,fill = (0, 0, 0))
            result_buffer = BytesIO()
            target.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
            imagmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
            result_img += f"[CQ:image,file={imagmes}]"
        return result_img
    except:
        raise Exception("绘制总图出错")

#绘制单图
async def imagelist_once_draw(page,num):
    try:
        if num == 0:    
            image_list=DBCounter()._select_once_tagdata(page)
            if image_list == {}:
                return f"手册该页没有配方哦"
        #分数单表
        else:
            image_list=DBCounter()._select_once_scoredata(num)
            if image_list == {}:
                return f"分数表11111"
        result_img=''
        target = Image.new('RGB', (1920,1080),(255,255,255))
        for index in range(0,8):
            try:
                image_info=image_list[index]
            except:
                break
            id = image_info[0]
            image=image_info[1]
            info=image_info[2]
            if num == 0:
                bianhao=f'编号:{id}'
                dianzan=f'点赞:{info}'
            else:
                bianhao=f'编号:{id}'
                dianzan=f'分数:{info}'
            region = Image.open(BytesIO(base64.b64decode(image)))
            region=region.convert("RGB")
            region=region.resize((int(region.width/2),int(region.height/2)))
            font = ImageFont.truetype(font_path, 24)  # 设置字体和大小
            draw = ImageDraw.Draw(target)
            row=index//4+1  #行
            column= index%4+1   #列
            target.paste(region,(77*column+384*(column-1),50*row+56*(row-1)+384*(row-1)))
            draw.text((77*column+384*(column-1),24+50*row+56*(row-1)+384*(row-1)+region.height),str(bianhao).replace(',',''),font=font,fill = (0, 0, 0))
            draw.text((77*column+384*(column-1)+int(region.width/2),24+50*row+56*(row-1)+384*(row-1)+region.height),str(dianzan).replace(',',''),font=font,fill = (0, 0, 0))
        result_buffer = BytesIO()
        target.save(result_buffer, format='JPEG', quality=quality) #质量影响图片大小
        imagmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
        result_img += f"[CQ:image,file={imagmes}]"
        return result_img
    except:
        raise Exception("绘制单图出错")

async def word_image(text):
    bg = Image.new('RGB', (950,600), color=(255,255,255))
    font = ImageFont.truetype(font_path, 30)  # 设置字体和大小
    draw = ImageDraw.Draw(bg)
    draw.text((10,5), text, fill="#000000", font=font)
    result_buffer = BytesIO()
    bg.save(result_buffer, format='JPEG', quality=100)
    imgmes = 'base64://' + base64.b64encode(result_buffer.getvalue()).decode()
    result_img = f"[CQ:image,file={imgmes}]"
    return result_img