import os
import sqlite3
from os.path import dirname, join

curpath = dirname(__file__)
ImageSave_DB_PATH = join(curpath,'save_tags.db')

class DBCounter:
    #初始化数据库，没有就创建
    def __init__(self):
        os.makedirs(os.path.dirname(ImageSave_DB_PATH), exist_ok=True)
        self._create_tags_table()
        self._create_score_table()

    #连接数据库
    def _connect(self):
        return sqlite3.connect(ImageSave_DB_PATH)

    #创建配方保存表
    def _create_tags_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS aitag
                          (权重             INT    NOT NULL,
                           形状             CHAR    NOT NULL,
                           标签             TEXT   NOT NULL,
                           种子             INT    ,
                           图片             BLOB    NOT NULL,
                           点赞             INT    NOT NULL,
                           剔除             TEXT);''')
        except:
            raise Exception('创建表发生错误')

    #创建图片分数表
    def _create_score_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS aiscore
                          (权重             INT    NOT NULL,
                           形状             CHAR    NOT NULL,
                           标签             TEXT   NOT NULL,
                           种子             INT    ,
                           图片             BLOB    NOT NULL,
                           分数             INT    NOT NULL,
                           剔除             TEXT);''')
        except:
            raise Exception('创建表发生错误')

    #添加数据到指定表，数据为元组
    def _insert_tagdata(self,scale,shape,tags,seed,image_base64,thumb,ntags):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO aitag VALUES (?,?,?,?,?,?,?)",(scale,shape,tags,seed,image_base64,thumb,ntags))
            return 0
        except:
            raise Exception('添加函数发生错误')

    def _insert_scoredata(self,scale,shape,tags,seed,image_base64,score,ntags):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO aiscore VALUES (?,?,?,?,?,?,?)",(scale,shape,tags,seed,image_base64,score,ntags))
            return 0
        except:
            raise Exception('添加函数发生错误')
    
    #删除指定表的指定列数据
    def _delete_tagdata(self,rowid):
        try:
            with self._connect() as conn:
                conn.execute("DELETE FROM aitag WHERE rowid=?", (rowid,))
            return f"删除ID:{rowid}成功"
        except:
            raise Exception('删除函数发生错误')

    #删除指定表的指定列数据
    def _delete_scoredata(self,rowid):
        try:
            with self._connect() as conn:
                conn.execute("DELETE FROM aiscore WHERE rowid=?", (rowid,))
            return f"删除ID:{rowid}成功"
        except:
            raise Exception('删除函数发生错误')

    #修改指定表的指定列数据
    def _update_data(self,rowid,scale,shape,tags,seed,image_base64,ntags):
        try:
            with self._connect() as conn:
                conn.execute("UPDATE aitag SET 权重 = ? , 形状 = ? , 标签 = ? , 种子 = ? , 图片 = ? , 剔除 = ? WHERE rowid=?",(scale,shape,tags,seed,image_base64,ntags,rowid,))
            return f"修改ID:{rowid}成功"
        except:
            raise Exception('修改函数发生错误')

    #读取一行的全部数据
    def _select_oneall_tagdata(self,rowid):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT * FROM aitag WHERE rowid=?", (rowid,)).fetchone()
            return r if r else {}
        except:
            raise Exception('查找函数发生错误')

    #读取一行的全部数据
    def _select_oneall_scoredata(self,rowid):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT * FROM aiscore WHERE rowid=?", (rowid,)).fetchone()
            return r if r else {}
        except:
            raise Exception('查找函数发生错误')

    #读取分数总表数据
    def _select_all_scoredata(self,rowid):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT rowid,图片,分数 FROM aiscore WHERE rowid ORDER BY 分数 desc LIMIT ?",(rowid,)).fetchall()
            return r if r else {}
        except:
            raise Exception('查找函数发生错误')

    #读取炼金总表数据
    def _select_all_tagdata(self):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT rowid,图片,点赞 FROM aitag").fetchall()
            return r if r else {}
        except:
            raise Exception('查找函数发生错误')
    
    #读取点赞数据
    def _select_thumb_data(self,rowid):
        try:
            with self._connect() as conn:
                r = conn.execute("SELECT 点赞 FROM aitag WHERE rowid=?",(rowid,)).fetchone()
            return r[0] if r else {}
        except:
            raise Exception('查找函数发生错误')


    def _select_once_tagdata(self,num):
        try:
            up_index=(num-1)*8+1
            down_index=num*8
            with self._connect() as conn:
                r = conn.execute("SELECT rowid,图片,点赞 FROM aitag WHERE rowid BETWEEN ? AND ?", (up_index,down_index,)).fetchall()
            return r if r else {}
        except:
            raise Exception('查找函数发生错误')

    def _select_once_scoredata(self,num):
        try:
            up_index=(num-1)*8+1
            down_index=num*8
            with self._connect() as conn:
                r = conn.execute("SELECT rowid,图片,点赞 FROM ? WHERE rowid BETWEEN ? AND ?", (up_index,down_index,)).fetchall()
            return r if r else {}
        except:
            raise Exception('查找函数发生错误')

    #刷新rowid
    def _vacuum_data(self):
        try:
            conn = self._connect()
            conn.execute('vacuum')
            conn.close
        except:
            raise Exception('刷新函数发生错误')

    #获取指定表，rowid数值
    def _get_tagrowid(self):
        try:
            with self._connect() as conn:
                r = conn.execute("select rowid from aitag order by rowid desc limit 1").fetchone()
            return r[0] if r else 0
        except:
            raise Exception('查找rowid发生错误')
    
    #获取指定表，rowid数值
    def _get_scorerowid(self):
        try:
            with self._connect() as conn:
                r = conn.execute("select rowid from aiscore order by rowid desc limit 1").fetchone()
            return r[0] if r else 0
        except:
            raise Exception('查找rowid发生错误')

    #进行点赞
    def _add_thumb(self,rowid):
        try:
            num = self._select_thumb_data(rowid)
            num += 1
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE aitag SET 点赞 =? WHERE rowid =?",(num,rowid,))
            return f"点赞成功，配方:{rowid}的点赞数为{num}"
        except:
            raise Exception('点赞函数发生错误')
