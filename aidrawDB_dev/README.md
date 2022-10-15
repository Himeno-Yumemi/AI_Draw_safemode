# AI_Draw_safemode

<b>本分支为 AI_Draw_safemode 的测试版本<b>

## 项目地址

仓库:<a href="https://github.com/jiyemengmei/AI_Draw_safemode/tree/dev/aidrawDB_dev" target="_BLANK">https://github.com/jiyemengmei/AI_Draw_safemode/tree/dev/aidrawDB_dev</a>

## 更新日志
### 2022/10/15
更新测试版本

## 具体操作
1、下载aidrawDB文件夹内全部内容，放到<code>hoshino/modules/aidrawDB</code>文件夹中\
2、在<code>hoshino/config/**bot**.py</code>文件中，<code>MODULES_ON</code>里添加 "aidrawDB_dev"\
3、【重要！！】<b>打开 config_example.config，填入NovelAI的token和腾讯云的两个secret，保存后重命名为config.json</b>\
4、【重要！！】安装依赖：①<code>pip install tencentcloud-sdk-python-ims</code>\
②<code>pip install --upgrade tencentcloud-sdk-python-common tencentcloud-sdk-python-cvm</code>\
腾讯云需要开启ai鉴黄，具体流程：\
1、https://console.cloud.tencent.com/cms 开启图像内容安全\
2、进入策略管理，创建，名称随便填，Biztype名称填ai_image_check\
3、行业分类填：社交/即时通讯/群聊\
4、图片识别填：色情：性器官裸露/性行为\
5、获取密钥：https://console.cloud.tencent.com/cam/capi \
6、其中的SecretId和SecretKey填到config.json里对应位置
## 功能指令

| 指令                                                | 说明                             | 具体                               |
| --------------------------------------------------- | -------------------------------- | ---------------------------------- |
| <b>绘图数据库帮助</b>                               | 查看该功能的全部指令             | 以图片形式生成                     |
| 上传<b>[参数]</b>                                   | 上传图片和 tag 至数据库内        | <b>[参数]</b>为 ai 绘图的指令      |
| <b>'回复'</b>[bot 昵称]上传                         | 通过回复他人的 ai 绘图来进行上传 | <b>具体下方使用演示</b>            |
| 炼金大全                                            | 查询炼金手册全部内容             | 若图片过大，修改 23 行质量         |
| 炼金手册<b>[序号]</b>                               | 查询炼金手册内容                 | <b>[序号]</b>为页数，每页显示 8 张 |
| 查看配方<b>[序号]</b>                               | 查询炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 修改配方<b>[序号][tags]</b>                         | 修改炼金配方内容                 | <b>目前禁用</b>          |
| 使用配方<b>[序号]</b>                               | 使用炼金配方内容                 | <b>[序号]</b>为图片标签            |
| 点赞配方<b>[序号]</b>                               | 点赞炼金配方内容                 | <b>[序号]</b>为图片标签            |
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
还有冲冲、Se、季落佬的代码帮助

## 友情链接
<a href="https://github.com/CYDXDianXian/AI_image_gen" target="_BLANK">AI_image_gen</a>

## API
<a href="" target="_BLANK">路路佬的 API</a>
