import unicodedata
from .config import get_config

wordlist = get_config('ban_word', 'wordlist')

def guolv(sent=str):
    sent_cp = unicodedata.normalize('NFKC', sent) # 中文标点转为英文
    sent_cp = sent_cp.lower() #转为小写
    sent_cp = sent_cp.replace('&shape=portrait', '&shape=Portrait')
    sent_cp = sent_cp.replace('&shape=landscape', '&shape=Landscape')
    sent_cp = sent_cp.replace('&shape=square', '&shape=Square')
    sent_list_ = sent_cp.split(",") # 从逗号处分开，返回列表
    
    sent_list = []
    for m in sent_list_:
        sent_list.append(m.strip()) # 移除空格

    # 生成过滤词列表
    tags_guolu_list = []
    for i in sent_list:
        if i in wordlist:
            tags_guolu_list.append(i)
    
    # 移除发送列表中的违禁词
    for j in tags_guolu_list:
        sent_list.remove(j)

    # 将过滤后的列表拼接为字符串
    sent_str = ",".join(sent_list)
    tags_guolu = ",".join(tags_guolu_list)
    return sent_str, tags_guolu