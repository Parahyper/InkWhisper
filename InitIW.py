# 操作系统交互模块
import os


def init_book():
    # 初始化图书信息
    #返回目录下的所有文件列表
    list_dir = os.listdir()
    if "book" not in list_dir:
        os.mkdir("book")
        print("初始化图书信息成功！")

def init_config():
    list_dir = os.listdir()
    if "config" not in list_dir:
        f = open("config.txt","w", encoding='utf-8')
        config = ['font:宋体','font_size:16','bg:white','fg:black']
        f.write('\n'.join(config))
        f.close()
        print("初始化配置信息成功！")

