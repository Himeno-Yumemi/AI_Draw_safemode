# AI_Draw_safemode
<b>本插件为AI_image_gen的扩展插件，目前已内置无冲突AI_image_gen(测试用)<b>
## 功能介绍
通过上传图片参数至数据库，来实现快捷的图片预览、图片TAG获取、对应标签的ai图片生成，图片打分，分数排行显示等功能。若不想使用ai鉴黄，后续将更新纯净版。
## 具体操作
1、下载<code>aidraw_db.py</code>和<code>check_iamge.py</code>,<code>fz.TTF</code>，放到<code>hoshino/modules/aidrawDB</code>文件夹中\
2、在<code>hoshino/config/__bot__.py</code>文件中，<code>MODULES_ON</code>里添加 "aidrawDB"\
3、【重要！！】<b>打开aidraw_db.py，在21行填入ai绘图的API接口，在22行填入个人token</b>\
4、【重要！！】<b>打开check_image.py，在5行填入百度图像审核API Key，在6行填入百度图像审核Secret Key</b>\
具体获取流程参考:\
<a href="https://github.com/pcrbot/SetuScore" target="_BLANK">SetuScore</a>\
PS:若不喜欢本字体可自行更换，但文件名必须是<code>fz.TTF</code>
## 功能指令
|  指令   | 说明  | 具体  |
|  ----  | ----  | ----  |
| <b>绘图数据库帮助</b>  |  查看该功能的全部指令  | 以图片形式生成  |
| 上传<b>[参数]</b>  | 上传图片和tag至数据库内  | <b>[参数]</b>为ai绘图的指令  |
| <b>'回复'</b>[bot昵称]上传  | 通过回复他人的ai绘图来进行上传  | <b>具体下方使用演示</b>  |
| 炼金大全  | 查询炼金手册全部内容  | 若图片过大，修改23行质量  |
| 炼金手册<b>[序号]</b>  | 查询炼金手册内容  | <b>[序号]</b>为页数，每页显示8张  |
| 查看配方<b>[序号]</b>  | 查询炼金配方内容  | <b>[序号]</b>为图片标签  |
| 修改配方<b>[序号][tags]</b>  | 修改炼金配方内容  | <b>具体看下方使用演示</b>  |
| 使用配方<b>[序号]</b>  | 使用炼金配方内容  | <b>[序号]</b>为图片标签  |
| 删除配方<b>[序号]</b>  | 删除炼金配方内容  | <b>[序号]</b>为图片标签  |
| 测试[tags]  | 进行ai绘图，返回种子和分数  |
| 分数排行[序号  | 查看图片分数排行  | [序号]为TOP数 
| 分数排行总榜  | 查看全部图片分数排行  |
| 清理分数排行  | 清除除排行前15的所有数据  |
PS:上传与修改仅限管理员使用，删除仅限超级管理员使用  |
## 使用演示
<b>绘图数据库帮助:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E7%BB%98%E5%9B%BE%E6%95%B0%E6%8D%AE%E5%BA%93%E5%B8%AE%E5%8A%A9.png)\
<b>上传[参数]:</b>\
![image](https://github.com/jiyemengmei/AI_Draw_safemode/blob/main/image/%E4%B8%8A%E4%BC%A0.png)\
<b>'回复'[bot昵称]上传:</b>\
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
还有群友们的DEBUG测试
## 友情链接
<a href="https://github.com/CYDXDianXian/AI_image_gen" target="_BLANK">AI_image_gen</a>
## API
<a href="" target="_BLANK">路路佬的API</a>
## 更新日志
### 2022/10/9
首次上传
### 2022/10/11
重构代码\
新增回复消息上传(减轻刷屏)，修改配方，数据库内容总览\
### 2022/10/12
修复BUG\
新增图片分数显示，图片ai鉴黄筛选，分数排行榜