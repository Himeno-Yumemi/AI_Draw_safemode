# AI_Draw_safemode
<b>本分支为 AI_Draw_safemode 的测试版本</b>

## 项目地址
仓库:<a href="https://github.com/jiyemengmei/AI_Draw_safemode/tree/dev/aidrawDB_dev" target="_BLANK">https://github.com/jiyemengmei/AI_Draw_safemode/tree/dev/aidrawDB_dev</a>
## 更新日志
### 2022/10/15
***
>更新测试版本
***
### 2022/10/16
***
><b>本次更新为毁灭式更新，将图片以base64形式存入数据库，之前的数据库直接作废(原因：本地图片)
>- 1、换一个文件夹使用本插件
>- 2、将save_tags.db迁移出去，让程序重新生成新数据库
>- 可选：手动取出tags，进行手动上传，或者bot上传（后续更新数据库迁移）</b>
***
>修复众多bug，新增功能如下:
>- '回复'本bot指令生成的图片，自动追踪上传(配方形式不算)\
指令为：'回复'[bot昵称]上传
>- '回复'其他bot指令生成的图片，通过类型进行上传,目前仅支持这种\
格式为：[图片]seed: cale: tags:\
指令为:'回复'[bot昵称]窃取
>- 自定义绘图指令，在`config.json`里修改`trigger_word`便可实现
>- 绘图指令生成的图，若开启鉴黄则自动上传至分数表
>- 分数配方[序号]，获取对应分数编号的配方，可通过分数总榜查看编号
>- 点赞配方[序号]，点赞对应配方(后续更新点赞榜单排名)
>- 保留分数[序号]，保留除前[序号]的分数配方，其余则删除
>- 总榜类图片通过转发来发送，防止刷屏
>- 负面参数自动填写，如需关闭\
在`config.json`里修改`ntags_stats`为**false**即可
>- 双鉴黄模块，若都关闭则不会获取分数与屏蔽图片
>- 绘图指令tag中文屏蔽，目前仅限英文tag
***
### 2022/10/17
***
> 由于接口问题，设置全局cd12秒
>- 修复百度接口分数为0的问题
>- 修复ntags不生效的问题
***

## 具体操作
1、下载aidrawDB_dev文件夹内全部内容，放到<code>hoshino/modules/aidrawDB_dev</code>文件夹中\
2、在<code>hoshino/config/\_bot\_.py</code>文件中，<code>MODULES_ON</code>里添加 "aidrawDB_dev"\
3、【重要！！】**重命名`config_example.json`为`config.json`**\
4、【重要！！】**打开`config.json`，填入NovelAI的token**
***
以下是鉴黄所需要的\
1、打开config.json，将需要开启的鉴黄check设置为true

2、填写需要使用的腾讯云或百度云的两个参数，以下介绍获取方法

腾讯云：\
一、安装依赖：\
①<code>pip install tencentcloud-sdk-python-ims</code>\
②<code>pip install tencentcloud-sdk-python-common</code>\
二、获取secretId和secretKey\
1、https://console.cloud.tencent.com/cms 开启图像内容安全\
2、进入策略管理，创建，名称随便填，Biztype名称填ai_image_check\
3、行业分类填：社交/即时通讯/群聊\
4、图片识别填：色情：性器官裸露/性行为\
5、获取密钥：https://console.cloud.tencent.com/cam/capi \
6、其中的SecretId和SecretKey填到config.json里对应位置

百度智慧云：\
具体获取流程参考:\
<a href="https://github.com/pcrbot/SetuScore#%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E" target="_BLANK">SetuScore</a>
> 在策略设置的时候只需要开启**卡通色情**和**卡通女性性感**，其余都可以关

PS:若不喜欢本字体可自行更换，但文件名必须是<code>fz.TTF</code>
## 功能指令

| 指令                                                | 说明                             | 具体                               |
| --------------------------------------------------- | -------------------------------- | ---------------------------------- |
| <b>绘图数据库帮助</b>                               | 查看该功能的全部指令             | 以图片形式生成                     |
| 上传<b>[参数]</b>                                   | 上传图片和 tag 至数据库内        | <b>[参数]</b>为 ai 绘图的指令      |
| <b>'回复'</b>[bot 昵称]上传                         | 通过回复本bot的绘图结果进行上传 | <b>具体下方使用演示</b>            |
| 炼金大全                                            | 查询炼金手册全部内容             | 以转发形式发送         |
| 炼金手册<b>[序号]</b>                               | 查询炼金手册内容                 | <b>[序号]</b>为页数，每页显示 8 张 |
| 查看配方<b>[序号]</b>                               | 查询炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 修改配方<b>[序号][tags]</b>                         | 修改炼金配方内容                 | <b>目前禁用</b>          |
| 使用配方<b>[序号]</b>                               | 使用炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 点赞配方<b>[序号]</b>                               | 点赞炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 删除配方<b>[序号]</b>                               | 删除炼金配方内容                 | <b>[序号]</b>为图片标签            |
| '自设指令'<b>[tags]</b>                                   | 进行 ai 绘图，返回种子和分数     | 具体参考更新解释  |
| 分数总榜                                        | 查看全部图片分数排行             |
| 分数配方[序号]  | 获取分数编号的配方  | 可通过分数总榜查看编号
| 保留分数[序号]                                        | 保留除前[序号]的分数配方，其余删除  |
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
还有冲冲、Se、季落佬的代码帮助

## 友情链接
<a href="https://github.com/CYDXDianXian/AI_image_gen" target="_BLANK">AI_image_gen</a>

## API
<a href="" target="_BLANK">路路佬的 API</a>
