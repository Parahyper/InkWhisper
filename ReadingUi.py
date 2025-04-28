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

def setup_reading_functions(ui_instance):
    # 阅读页内容设计
    # 内容框
    ui_instance.text_area = tk.Text(
        ui_instance.tab2,
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        state='disable'
    )
    ui_instance.text_area.place(relx=0.15, rely=0, relwid=0.7, relhei=1)
    # AI回答框
    ui_instance.answer_area = tk.Text(
        ui_instance.tab2,
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        state='disable',
    )
    ui_instance.answer_area.place(relx=0.85, rely=0, relwid=0.15, relhei=0.72)
    # 书名框和章节框
    ui_instance.base_bookname_chapter = tk.Text(
        ui_instance.tab2,
        highlightthickness=0,  # 新增：隐藏高亮边框
        borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg']
    )
    ui_instance.base_bookname_chapter.place(relx=0, rely=0, relwid=0.15, relhei=1)
    # 书名框
    ui_instance.book_name = tk.Listbox(
        ui_instance.base_bookname_chapter,
        # highlightthickness=0,  # 新增：隐藏高亮边框
        borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg']
    )
    # 固定为单行显示
    # ui_instance.book_name.configure(wrap=tk.CHAR, height=1)
    ui_instance.book_name.place(relx=-0.01, rely=0, relwid=1.02, relhei=0.035)
    # 章节框
    ui_instance.chapter_list_box = tk.Listbox(
        ui_instance.base_bookname_chapter,
        highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        exportselection=False,
        selectmode=tk.SINGLE
    )
    ui_instance.chapter_list_box.place(relx=-0.01, rely=0.045, relwid=1.02, relhei=0.836)
    for item in range(1, 41):
        ui_instance.chapter_list_box.insert("end", item)
    # 自定义提问框
    ui_instance.Problem_Entry = tk.Text(
        ui_instance.tab2,
        wrap=tk.WORD,
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        width=20,
        height=4,
        insertofftime=0
    )
    ui_instance.Problem_Entry.place(relx=0.85, rely=0.75, relwid=0.15, relhei=0.2)
    # ui_instance.Problem_Entry.insert(0, str(ui_instance.config.get('font_size', 16)))
    ui_instance.Problem_Entry.mark_set("insert", "1.0")
    # 手动回答按钮框
    ui_instance.t1 = tk.Listbox(
        ui_instance.tab2,
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )
    ui_instance.t1.place(relx=0.8499, rely=0.949, relwid=0.152, relhei=0.05)
    # 全文提问按钮
    ui_instance.summary_ask_button = tk.Button(
        ui_instance.t1,
        text='全文提问',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        command=ui_instance.summary_ask_thread
    )
    ui_instance.summary_ask_button.place(relx=0, rely=0, relwid=0.33, relhei=1)
    # 段落提问按钮
    ui_instance.paragragh_ask_button = tk.Button(
        ui_instance.t1,
        text='段落提问',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.paragraph_ask_thread
    )
    ui_instance.paragragh_ask_button.place(relx=0.33, rely=0, relwid=0.33, relhei=1)
    # 提问按钮
    ui_instance.ask_button = tk.Button(
        ui_instance.t1,
        text='自由提问',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.ask_thread
    )
    ui_instance.ask_button.place(relx=0.66, rely=0, relwid=0.34, relhei=1)
    # 快捷方式按钮框
    ui_instance.t2 = tk.Listbox(
        ui_instance.tab2,
        highlightthickness=0,  # 新增：隐藏高亮边框
        borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )
    ui_instance.t2.place(relx=0.8499, rely=0.72, relwid=0.152, relhei=0.032)
    # 快捷方式按钮
    # 全文总结
    ui_instance.shortcut_button1 = tk.Button(
        ui_instance.t2,
        text='全文总结',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], round(ui_instance.config['font_size'] * 2 / 3)),
        command=ui_instance.summary_thread
    )
    ui_instance.shortcut_button1.place(relx=0, rely=0, relwid=0.25, relhei=1)
    # 段落总结
    ui_instance.shortcut_button2 = tk.Button(
        ui_instance.t2,
        text='段落总结',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], round(ui_instance.config['font_size'] * 2 / 3)),
        command=ui_instance.paragraph_summary_thread
    )
    ui_instance.shortcut_button2.place(relx=0.25, rely=0, relwid=0.25, relhei=1)
    # 快捷方式3
    ui_instance.shortcut_button3 = tk.Button(
        ui_instance.t2,
        text='重点句子',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], round(ui_instance.config['font_size'] * 2 / 3)),
        command=ui_instance.key_paragraph_thread
    )
    ui_instance.shortcut_button3.place(relx=0.5, rely=0, relwid=0.25, relhei=1)
    # 快捷方式4
    ui_instance.shortcut_button4 = tk.Button(
        ui_instance.t2,
        text='人物提取',
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        font=(ui_instance.config['font'], round(ui_instance.config['font_size'] * 2 / 3)),
        command=ui_instance.person_extract_thread
    )
    ui_instance.shortcut_button4.place(relx=0.75, rely=0, relwid=0.25, relhei=1)

    ui_instance.t3 = tk.Text(
        ui_instance.tab2,
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        # highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
    )
    ui_instance.t3.place(relx=0, rely=0.885, relwid=0.15, relhei=0.115)

    # 阅读按钮
    ui_instance.read_button = tk.Button(
        ui_instance.tab2,
        text='阅读',
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.read_chapter_thread
    )
    ui_instance.read_button.place(relx=0.005, rely=0.9, relwid=0.06, relhei=0.04)
    # 退出按钮
    ui_instance.exit_button = tk.Button(
        ui_instance.tab2,
        text='退出',
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.exit_book
    )
    ui_instance.exit_button.place(relx=0.08, rely=0.9, relwid=0.06, relhei=0.04)
    # 上一章
    ui_instance.pre_page = tk.Button(
        ui_instance.tab2,
        text='上一章',
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.pre_page
    )
    ui_instance.pre_page.place(relx=0.005, rely=0.95, relwid=0.06, relhei=0.04)
    # 下一章
    ui_instance.next_page = tk.Button(
        ui_instance.tab2,
        text='下一章',
        bg=ui_instance.config['bg'],
        fg=ui_instance.config['fg'],
        highlightthickness=0,  # 新增：隐藏高亮边框
        # borderwidth=0,  # 新增：隐藏文本区域边框
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.next_page
    )
    ui_instance.next_page.place(relx=0.08, rely=0.95, relwid=0.06, relhei=0.04)