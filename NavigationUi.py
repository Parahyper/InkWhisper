import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# import tkinter.ttk as ttk
import tkinter.font
import SettingPage
import BookListPage
import threading
import BookOpen
from functools import partial
import InitIW
import LLMs_api
import re


def setup_navigation_tab(ui_instance):
    # 书架页设计
    # 本地书架标题设置其位置，字体，字体大小
    tk.Label(
        ui_instance.tab1,
        text='本地书架',
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    ).place(relx=0.48, rely=0.01)
    # 书籍列表显示
    ui_instance.local_case_box = tk.Listbox(
        ui_instance.tab1,
        font=(ui_instance.config['font'],
              ui_instance.config['font_size'])
    )
    ui_instance.local_case_box.place(relx=0.02, rely=0.052, relwid=0.96, relhei=0.9)
    # 刷新，阅读，删除按钮
    local_refresh_btn = tk.Button(
        ui_instance.tab1,
        text='刷新',
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.local_fresh
    )
    local_refresh_btn.place(relx=0.7, rely=0.007, relwid=0.08, relhei=0.04)
    local_case_btn = tk.Button(
        ui_instance.tab1,
        text='阅读',
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.open_local_book
    )
    local_case_btn.place(relx=0.8, rely=0.007, relwid=0.08, relhei=0.04)
    local_del_btn = tk.Button(
        ui_instance.tab1,
        text='删除',
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.del_local_book
    )
    local_del_btn.place(relx=0.9, rely=0.007, relwid=0.08, relhei=0.04)
