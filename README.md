# AI_Draw_safemode
ai绘图安全版
## 功能介绍
通过上传图片参数至数据库，来实现快捷的图片预览、图片TAG获取、对应标签的ai图片生成等功能。
## 具体操作
1、下载aidraw_db.py，放到<code>hoshino/modules/aidrawDB</code>文件夹中\
2、在<code>hoshino/config/__bot__.py</code>文件中，<code>MODULES_ON</code>里添加 "aidrawDB"
## 功能指令
|  指令   | 说明  | 具体  |
|  ----  | ----  | ----  |
| <b>绘图数据库帮助</b>  |  查看该功能的全部指令  | 以图片形式生成  |
| 上传<b>[参数]</b>  | 上传图片和tag至数据库内  | <b>[参数]</b>为ai绘图的指令  |
| 炼金手册<b>[序号]</b>  | 查询炼金手册内容  | [序号]为页数，每页显示8张  |
| 查看配方<b>[序号]</b>  | 查询炼金配方内容  | [序号]为图片标签  |
| 使用配方<b>[序号]</b>  | 使用炼金配方内容  | [序号]为图片标签  |
| 删除配方<b>[序号]</b>  | 删除炼金配方内容  | [序号]为图片标签  |
PS:上传仅限管理员使用，删除仅限超级管理员使用
## 演示
绘图数据库帮助:
![image]()
上传[参数]:
![image]()
炼金手册[序号]:
![image]()
查看配方[序号]:
![image]()
使用配方[序号]:
![image]()
删除配方[序号]:
![image]()
## 鸣谢
<a href="https://github.com/Mrs4s/go-cqhttp" target="_BLANK">go-cqhttp</a>\
<a href="https://github.com/Ice-Cirno/HoshinoBot" target="_BLANK">HoshinoBot</a>\
<a href="" target="_BLANK">Cath的AI绘图源码</a>
## API
<a href="" target="_BLANK">路路佬私人API</a>
## 更新日志
### 2022/10/9
首次上传
