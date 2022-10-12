# AI_Draw_safemode

<b>本插件为 AI_image_gen 的扩展插件，目前已内置无冲突 AI_image_gen(测试用)<b>

## 项目地址

仓库:<a href="https://github.com/jiyemengmei/AI_Draw_safemode" target="_BLANK">https://github.com/jiyemengmei/AI_Draw_safemode</a>\
群内一般也会更新，建议查看群内文件日期与仓库日期是否一致\
<a href="#更新日志" target="_BLANK">更新日期</a>

## 功能介绍

通过上传图片参数至数据库，来实现快捷的图片预览、图片 TAG 获取、对应标签的 ai 图片生成，图片打分，分数排行显示等功能。若不想使用 ai 鉴黄，后续将更新纯净版。

## 具体操作

1、下载<code>aidraw_db.py</code>和<code>check_iamge.py</code>,<code>fz.TTF</code>，放到<code>hoshino/modules/aidrawDB</code>文件夹中\
2、在<code>hoshino/config/**bot**.py</code>文件中，<code>MODULES_ON</code>里添加 "aidrawDB"\
3、【重要！！】<b>打开 aidraw_db.py，在 21 行填入 ai 绘图的 API 接口，在 22 行填入个人 token</b>\
4、【重要！！】<b>打开 check_image.py，在 5 行填入百度图像审核 API Key，在 6 行填入百度图像审核 Secret Key</b>\
具体获取流程参考:\
<a href="https://github.com/pcrbot/SetuScore" target="_BLANK">SetuScore</a>\
PS:若不喜欢本字体可自行更换，但文件名必须是<code>fz.TTF</code>

## 功能指令

| 指令                                                | 说明                             | 具体                               |
| --------------------------------------------------- | -------------------------------- | ---------------------------------- |
| <b>绘图数据库帮助</b>                               | 查看该功能的全部指令             | 以图片形式生成                     |
| 上传<b>[参数]</b>                                   | 上传图片和 tag 至数据库内        | <b>[参数]</b>为 ai 绘图的指令      |
| <b>'回复'</b>[bot 昵称]上传                         | 通过回复他人的 ai 绘图来进行上传 | <b>具体下方使用演示</b>            |
| 炼金大全                                            | 查询炼金手册全部内容             | 若图片过大，修改 23 行质量         |
| 炼金手册<b>[序号]</b>                               | 查询炼金手册内容                 | <b>[序号]</b>为页数，每页显示 8 张 |
| 查看配方<b>[序号]</b>                               | 查询炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 修改配方<b>[序号][tags]</b>                         | 修改炼金配方内容                 | <b>具体看下方使用演示</b>          |
| 使用配方<b>[序号]</b>                               | 使用炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 删除配方<b>[序号]</b>                               | 删除炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 测试<b>[tags]</b>                                   | 进行 ai 绘图，返回种子和分数     |
| 分数排行<b>[序号]</b>                               | 查看图片分数排行                 | <b>[序号]</b>为 TOP 数             |
| 分数排行总榜                                        | 查看全部图片分数排行             |
| 清理分数排行                                        | 清除除排行前 15 的所有数据       |
| PS:上传与修改仅限管理员使用，删除仅限超级管理员使用 |

## 使用演示

<b>绘图数据库帮助:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E7%BB%98%E5%9B%BE%E6%95%B0%E6%8D%AE%E5%BA%93%E5%B8%AE%E5%8A%A9.png)\
<b>上传[参数]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E4%B8%8A%E4%BC%A0.png)\
<b>'回复'[bot 昵称]上传:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E6%8C%87%E4%BB%A4%E4%B8%8A%E4%BC%A0.png)\
<b>炼金大全:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E7%82%BC%E9%87%91%E5%A4%A7%E5%85%A8.png)\
<b>炼金手册[序号]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E7%82%BC%E9%87%91%E6%89%8B%E5%86%8C.png)\
<b>查看配方[序号]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E6%9F%A5%E7%9C%8B%E9%85%8D%E6%96%B9.png)\
<b>修改配方[序号]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E4%BF%AE%E6%94%B9%E9%85%8D%E6%96%B9.png)\
<b>使用配方[序号]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E4%BD%BF%E7%94%A8%E9%85%8D%E6%96%B9.png)\
<b>删除配方[序号]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E5%88%A0%E9%99%A4%E9%85%8D%E6%96%B9.png)

## 鸣谢

<a href="https://github.com/Mrs4s/go-cqhttp" target="_BLANK">go-cqhttp</a>\
<a href="https://github.com/Ice-Cirno/HoshinoBot" target="_BLANK">HoshinoBot</a>\
还有群友们的 DEBUG 测试

## 友情链接

<a href="https://github.com/CYDXDianXian/AI_image_gen" target="_BLANK">AI_image_gen</a>

## API

<a href="" target="_BLANK">路路佬的 API</a>

## 更新日志

### 2022/10/9

首次上传

### 2022/10/11

重构代码\
新增回复消息上传(减轻刷屏)，修改配方，数据库内容总览\

### 2022/10/12

修复 BUG\
新增图片分数显示，图片 ai 鉴黄筛选，分数排行榜
