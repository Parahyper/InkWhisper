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


class UiIW:
    def __init__(self):
        ######################################################################################################
        # 参数区
        # 初始化配置文件
        self.config = {}       # 系统配置
        self.local_book_list = []  # 书名 章节 作者 更新日期
        self.chapter_index = 0 # 章节索引
        self.chapter_last = [] # 章节信息
        ######################################################################################################

        ######################################################################################################
        # 初始化配置
        self.load_config()
        if "font_size" in self.config.keys():
            self.config['font_size'] = int(self.config['font_size'])
        ######################################################################################################

        ######################################################################################################
        # 替换原来的样式配置为ttkbootstrap
        # style = ttk.Style(theme='classic')  # 使用沙岩主题
        # 想要切换主题，修改theme值即可，有以下这么多的主题，自己尝试吧：['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly',
        # 'clam', 'alt', 'solar', 'minty', 'litera',
        # 'united', 'xpnative', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero', 'winnative', 'sandstone', 'default']
        # 删除或注释以下原有样式配置代码：
        # style.theme_create('T_theme', settings={...})
        # style.theme_create('new_theme', settings={...})
        # style.theme_use('new_theme')

        # 保留必要的组件样式覆盖（根据主题需要调整）
        # style.configure('TNotebook.Tab',
        #                 font=(self.config['font'], self.config['font_size']))
        # style.configure('TButton',
        #                 font=(self.config['font'], self.config['font_size']))
        # style.configure('TEntry',
        #                 font=(self.config['font'], self.config['font_size']))

        #####################################################################################################



        ######################################################################################################
        # 基础设计
        self.root = tk.Tk()
        # 主题切换
        # 替换原有的样式配置代码
        style = ttk.Style(theme=self.config['theme'])
        self.root.style = style  # 保持样式引用
        # 添加基础颜色配置映射
        self.config['bg'] = style.colors.get('bg')  # 使用主题的背景色
        self.config['fg'] = style.colors.get('fg')  # 使用主题的前景色
        # 主窗口背景色设置
        self.root.configure(background=style.colors.get('bg'))
        # 暗色cyborg darkly solar superhero亮色journal flatly minty litera united pulse cosmo lumen yeti sandstone
        # 想要切换主题['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly',
        # 'clam', 'alt', 'solar', 'minty', 'litera',
        # 'united', 'xpnative', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero', 'winnative', 'sandstone', 'default']

        # # 添加基础颜色配置映射
        # theme_colors = style.colors
        # self.config['bg'] = theme_colors.bg
        # self.config['fg'] = theme_colors.fg
        # # 主窗口背景色设置
        # self.root.configure(background=style.colors.bg)

        # 窗口设置
        # 获取屏幕宽度
        # 获取屏幕高度的90%
        w = self.root.winfo_screenwidth()
        h = int(self.root.winfo_screenheight() * 0.9)
        # 设置窗口大小和位置
        self.root.geometry("%dx%d+0+0" % (w, h))
        # 设置窗口最大化
        self.root.state("zoomed")
        # 设置窗口标题
        self.root.title("InkWhisper")

        # 主窗口设计
        # 创建一个Notebook组件，并调整其位置和大小
        self.main_page = ttk.Notebook(

            self.root
        )
        self.main_page.place(relx=0, rely=0, relwidth=1, relheight=1)
        ######################################################################################################

        ######################################################################################################
        # 分页设计
        # 书架页面设计
        # 标签页
        self.tab1 = tk.Frame(self.main_page)
        self.tab1.place(x=0, y=30)
        self.main_page.add(
            self.tab1,
            text='图书列表'
        )
        tk.Label(
            self.tab1,
            text='测试',
            font=(self.config['font'], self.config['font_size'])
        ).place(relx=0.48, rely=0.01)

        # 阅读页
        self.tab2 = tk.Frame(self.main_page)
        self.tab2.place(x=0, y=30)
        self.main_page.add(
            self.tab2,
            text='阅读'
        )
        # self.tab2 = tk.Text(
        #     self.base_tab2,
        #     font=(self.config['font'], self.config['font_size']),
        #     bg=self.config['bg'],
        #     fg=self.config['fg']
        # )
        # self.tab2.place(relx=0, rely=0, relwidth=1, relheight=1)
        # 设置页
        self.tab3 = tk.Frame(self.main_page)
        self.tab3.place(x=0, y=30)
        self.main_page.add(
            self.tab3,
            text='设置'
        )
        ######################################################################################################

        ######################################################################################################
        # 书架页设计
        # 本地书架标题设置其位置，字体，字体大小
        tk.Label(
            self.tab1,
            text='本地书架',
            font=(self.config['font'], self.config['font_size'])
        ) .place(relx=0.48, rely=0.01)
        # 书籍列表显示
        self.local_case_box = tk.Listbox(
            self.tab1,
            font=(self.config['font'],
                  self.config['font_size'])
        )
        self.local_case_box.place(relx=0.02, rely=0.052, relwid=0.96, relhei=0.9)
        # 刷新，阅读，删除按钮
        local_refresh_btn = tk.Button(
            self.tab1,
            text='刷新',
            font=(self.config['font'], self.config['font_size']),
            command=self.local_fresh
        )
        local_refresh_btn.place(relx=0.7, rely=0.007, relwid=0.08, relhei=0.04)
        local_case_btn = tk.Button(
            self.tab1,
            text='阅读',
            font=(self.config['font'], self.config['font_size']),
            command=self.open_local_book
        )
        local_case_btn.place(relx=0.8, rely=0.007, relwid=0.08, relhei=0.04)
        local_del_btn = tk.Button(
            self.tab1,
            text='删除',
            font=(self.config['font'], self.config['font_size']),
            command=self.del_local_book
        )
        local_del_btn.place(relx=0.9, rely=0.007, relwid=0.08, relhei=0.04)
        ######################################################################################################


        ######################################################################################################
        # 阅读页内容设计
        # 内容框
        self.text_area = tk.Text(
            self.tab2,
            font=(self.config['font'], self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg'],
            state='disable'
        )
        self.text_area.place(relx=0.15, rely=0, relwid=0.7, relhei=1)
        # AI回答框
        self.answer_area = tk.Text(
            self.tab2,
            font=(self.config['font'],self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg'],
            state='disable',
        )
        self.answer_area.place(relx=0.85, rely=0, relwid=0.15, relhei=0.72)
        # 书名框和章节框
        self.base_bookname_chapter = tk.Text(
            self.tab2,
            highlightthickness=0,  # 新增：隐藏高亮边框
            borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg']
        )
        self.base_bookname_chapter.place(relx=0, rely=0, relwid=0.15, relhei=1)
        # 书名框
        self.book_name = tk.Listbox(
            self.base_bookname_chapter,
            # highlightthickness=0,  # 新增：隐藏高亮边框
            borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'],self.config['font_size']),
            bg = self.config['bg'],
            fg = self.config['fg']
        )
        # 固定为单行显示
        # self.book_name.configure(wrap=tk.CHAR, height=1)
        self.book_name.place(relx=-0.01, rely=0, relwid=1.02, relhei=0.035)
        # 章节框
        self.chapter_list_box = tk.Listbox(
            self.base_bookname_chapter,
            highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg'],
            exportselection=False,
            selectmode=tk.SINGLE
        )
        self.chapter_list_box.place(relx=-0.01, rely=0.045, relwid=1.02, relhei=0.836)
        for item in range(1, 41):
            self.chapter_list_box.insert("end", item)
        # 自定义提问框
        self.Problem_Entry= tk.Text(
            self.tab2,
            wrap=tk.WORD,
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg'],
            width=20,
            height=4,
            insertofftime=0
        )
        self.Problem_Entry.place(relx=0.85, rely=0.75, relwid=0.15, relhei=0.2)
        #self.Problem_Entry.insert(0, str(self.config.get('font_size', 16)))
        self.Problem_Entry.mark_set("insert", "1.0")
        # 手动回答按钮框
        self.t1= tk.Listbox(
            self.tab2,
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'], self.config['font_size'])
        )
        self.t1.place(relx=0.8499, rely=0.949, relwid=0.152, relhei=0.05)
        # 全文提问按钮
        self.summary_ask_button = tk.Button(
            self.t1,
            text='全文提问',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg'],
            command=self.summary_ask_thread
        )
        self.summary_ask_button.place(relx=0, rely=0, relwid=0.33, relhei=1)
        # 段落提问按钮
        self.paragragh_ask_button = tk.Button(
            self.t1,
            text='段落提问',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'], self.config['font_size']),
            command=self.paragraph_ask_thread
        )
        self.paragragh_ask_button.place(relx=0.33, rely=0, relwid=0.33, relhei=1)
        # 提问按钮
        self.ask_button = tk.Button(
            self.t1,
            text='自由提问',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'], self.config['font_size']),
            command=self.ask_thread
        )
        self.ask_button.place(relx=0.66, rely=0, relwid=0.34, relhei=1)
        # 快捷方式按钮框
        self.t2 = tk.Listbox(
            self.tab2,
            highlightthickness=0,  # 新增：隐藏高亮边框
            borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'], self.config['font_size'])
        )
        self.t2.place(relx=0.8499, rely=0.72, relwid=0.152, relhei=0.032)
        # 快捷方式按钮
        # 全文总结
        self.shortcut_button1 = tk.Button(
            self.t2,
            text='全文总结',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'], round(self.config['font_size'] * 2 / 3)),
            command=self.summary_thread
        )
        self.shortcut_button1.place(relx=0, rely=0, relwid=0.25, relhei=1)
        # 段落总结
        self.shortcut_button2 = tk.Button(
            self.t2,
            text='段落总结',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'], round(self.config['font_size'] * 2 / 3)),
            command=self.paragraph_summary_thread
        )
        self.shortcut_button2.place(relx=0.25, rely=0, relwid=0.25, relhei=1)
        # 快捷方式3
        self.shortcut_button3 = tk.Button(
            self.t2,
            text='重点句子',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'],round(self.config['font_size'] * 2 / 3)),
            command=self.key_paragraph_thread
        )
        self.shortcut_button3.place(relx=0.5, rely=0, relwid=0.25, relhei=1)
        # 快捷方式4
        self.shortcut_button4 = tk.Button(
            self.t2,
            text='人物提取',
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            bg=self.config['bg'],
            fg=self.config['fg'],
            font=(self.config['font'],round(self.config['font_size'] * 2 / 3)),
            command=self.person_extract_thread
        )
        self.shortcut_button4.place(relx=0.75, rely=0, relwid=0.25, relhei=1)

        self.t3 = tk.Text(
            self.tab2,
            bg=self.config['bg'],
            fg=self.config['fg'],
            # highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
        )
        self.t3.place(relx=0, rely=0.885, relwid=0.15, relhei=0.115)

        # 阅读按钮
        self.read_button = tk.Button(
            self.tab2,
            text='阅读',
            bg=self.config['bg'],
            fg=self.config['fg'],
            highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            command=self.read_chapter_thread
        )
        self.read_button.place(relx=0.005, rely=0.9, relwid=0.06, relhei=0.04)
        # 退出按钮
        self.exit_button = tk.Button(
            self.tab2,
            text='退出',
            bg=self.config['bg'],
            fg=self.config['fg'],
            highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            command=self.exit_book
        )
        self.exit_button.place(relx=0.08, rely=0.9, relwid=0.06, relhei=0.04)
        # 上一章
        self.pre_page = tk.Button(
            self.tab2,
            text='上一章',
            bg=self.config['bg'],
            fg=self.config['fg'],
            highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            command=self.pre_page
        )
        self.pre_page.place(relx=0.005, rely=0.95, relwid=0.06, relhei=0.04)
        # 下一章
        self.next_page = tk.Button(
            self.tab2,
            text='下一章',
            bg=self.config['bg'],
            fg=self.config['fg'],
            highlightthickness=0,  # 新增：隐藏高亮边框
            # borderwidth=0,  # 新增：隐藏文本区域边框
            font=(self.config['font'], self.config['font_size']),
            command=self.next_page
        )
        self.next_page.place(relx=0.08, rely=0.95, relwid=0.06, relhei=0.04)
        ######################################################################################################

        ######################################################################################################
        # 设置页页面设计
        # 字体设置
        tk.Label(
            self.tab3,
            text='字体设置:',
            font=(self.config['font'], self.config['font_size'])
        ).place(relx=0.05, rely=0.04, relwid=0.08, relhei=0.05)
        self.font_label = ttk.Combobox(
            self.tab3,
            font=(self.config['font'], self.config['font_size'])
        )  # 创建下拉菜单
        self.font_label.place(relx=0.15, rely=0.05, relwid=0.1)  # 将下拉菜单绑定到窗体
        all_fonts = tkinter.font.families()
        chinese_fonts = [
            f for f in all_fonts
            if any(char in f for char in ['宋', '楷', '黑', '仿','华'])  # 常见中文字体特征
               and '@' not in f  # 排除部分字体
        ]
        self.font_label["value"] = sorted(set(chinese_fonts))  # 获取系统所有可用字体
        self.font_label.current(13)

        # 字体数组废弃代码
        # if self.config.get('font'):  # 保留原有默认值逻辑
        #     self.font_label.current(sorted(tkinter.font.families()).index(self.config['font']))
        # else:
        #     self.font_label.current(0)
        # self.font_label["value"] = ("宋体", "楷体", "黑体","微软雅黑")  # 给下拉菜单设定值

        # 字体大小
        tk.Label(
            self.tab3,
            text='字体大小:',
            font=(self.config['font'], self.config['font_size'])
        ).place(relx=0.3, rely=0.04, relwid=0.08, relhei=0.05)
        self.font_size = tk.Entry(
            self.tab3,
            font=(self.config['font'], self.config['font_size'])
        )
        self.font_size.place(relx=0.4, rely=0.05, relwid=0.05)
        self.font_size.insert(0, str(self.config.get('font_size', 16)))
        # 背景颜色
        # 暗色cyborg darkly solar superhero亮色journal flatly minty litera united pulse cosmo lumen yeti sandstone
        tk.Label(
            self.tab3,
            text='主题选择:',
            font=(self.config['font'], self.config['font_size'])
        ).place(relx=0.05, rely=0.14, relwid=0.08, relhei=0.05)
        self.background = ttk.Combobox(
            self.tab3,
            font=(self.config['font'], self.config['font_size'])
        )  # 创建下拉菜单
        self.background.place(relx=0.15, rely=0.15, relwid=0.1)  # 将下拉菜单绑定到窗体
        self.background["value"] = ("litera","darkly","superhero","journal","sandstone")  # 给下拉菜单设定值
        self.background.current(0)
        # 朗读音色
        tk.Label(
            self.tab3,
            text='人声朗读:',
            font=(self.config['font'], self.config['font_size'])
        ).place(relx=0.05, rely=0.24, relwid=0.08, relhei=0.05)
        read_aloud = ttk.Combobox(
            self.tab3,
            font=(self.config['font'], self.config['font_size'])
        )  # 创建下拉菜单
        read_aloud.place(relx=0.15, rely=0.25, relwid=0.1)  # 将下拉菜单绑定到窗体
        read_aloud["value"] = ("windows","女声","男声")  # 给下拉菜单设定值
        read_aloud.current(0)
        # 大模型选择
        tk.Label(
            self.tab3,
            text='模型选择:',
            font=(self.config['font'], self.config['font_size'])
        ).place(relx=0.05, rely=0.34, relwid=0.08, relhei=0.05)
        self.llms = ttk.Combobox(
            self.tab3,
            font=(self.config['font'], self.config['font_size'])
        )  # 创建下拉菜单
        self.llms.place(relx=0.15, rely=0.35, relwid=0.1)  # 将下拉菜单绑定到窗体
        self.llms["value"] = ("DeepSeek", "Doubao", "通义千问")  # 给下拉菜单设定值
        self.llms.current(0)
        # 确定设置按钮尚未绑定对应函数
        setting_button = tk.Button(
            self.tab3,
            text="确定设置",
            font=(self.config['font'], self.config['font_size']),
            command=self.setting
        )
        setting_button.place(relx=0.05, rely=0.8, relwid=0.08, relhei=0.04)
        # 热键提示框
        self.hotkey_learning = tk.Text(
            self.tab3,
            font=(self.config['font'], round(self.config['font_size'] * 1.6)),
            bg=self.config['bg'],  # 使用主题背景色
            fg = 'orange'# 使用红色固定色
        )
        self.hotkey_learning.insert('1.0',
                                    '热键提示：\n'
                                    'Ctrl+回车 - 打开书籍\n'
                                    'F5 - 刷新书库\n'
                                    'Ctrl+回车 - 打开章节\n'
                                    'Ctrl+← - 上一章\n'
                                    'Ctrl+→ - 下一章\n'
                                    'Ctrl+Esc - 退出阅读\n'
                                    'Ctrl+退格 - 清空提问框'
                                    )  # 新增插入文本
        self.hotkey_learning.place(relx=0.55, rely=0.05, relwid=0.35, relhei=0.5)
        ######################################################################################################

        ######################################################################################################
        # 热键绑定
        # 主窗口设计后添加热键绑定
        self.root.bind("<Alt-1>", lambda e: self.switch_tab(0))  # 小键盘1
        self.root.bind("<Alt-2>", lambda e: self.switch_tab(1))  # 小键盘2
        self.root.bind("<Alt-3>", lambda e: self.switch_tab(2))  # 小键盘3
        self.root.bind("<F5>", lambda e: self.local_fresh())  # F5刷新书库
        self.root.bind("<Control-Left>", lambda e: self.goto_pre())  # 左箭头上一章
        self.root.bind("<Control-Right>", lambda e: self.goto_next())  # 右箭头下一章
        self.root.bind("<Control-Escape>", lambda e: self.exit_book())  # 退出阅读
        self.root.bind("<Control-Return>", lambda e: self.enter_handler())  # 阅读
        self.root.bind("<Control-Return>", lambda e: self.enter_handler())  # 阅读
        self.root.bind("<Control-BackSpace>", lambda e: self.clear_text())  # 清除提问框
        ######################################################################################################

        self.local_fresh()
        self.setting()
        #进入消息循环
        self.root.mainloop()
    # 函数区
    ######################################################################################################
    # 加载配置文件
    def load_config(self):
       f = open("config.txt", 'r', encoding='utf-8')
       lines = f.readlines()
       for line in lines:
           key, value = line.strip().split(':')  # 添加strip()去除换行符和空格
           self.config[key] = value
           # self.config[line.split(':')[0]] = line.split(':')[1]
       f.close()
    ######################################################################################################

    ######################################################################################################
    # 设置页函数
    # 统一更新组件样式
    def update_widget_style(self):
        # 更新公共样式
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=(self.config['font'], self.config['font_size']))
        style.configure('TButton', font=(self.config['font'], self.config['font_size']))
        style.configure('TEntry', font=(self.config['font'], self.config['font_size']))
        # 更新文本框组件
        text_widgets = [
            self.text_area,
            self.answer_area,
            self.book_name,
            self.Problem_Entry,
            # self.hotkey_learning,
            self.base_bookname_chapter
        ]
        for widget in text_widgets:
            widget.configure(
                font=(self.config['font'], self.config['font_size']),
                bg=self.config['bg'],
                fg=self.config['fg']
            )
        # 更新按钮组件
        buttons = [self.paragragh_ask_button,
                   self.summary_ask_button,
                   self.ask_button,
                   self.shortcut_button1,
                   self.shortcut_button2,
                   self.shortcut_button3,
                   self.shortcut_button4,
                   self.read_button,
                   self.exit_button,
                   self.pre_page,
                   self.next_page
                   ]
        for btn in buttons:
            btn.configure(
                font=(self.config['font'], self.config['font_size']),
                # bg=self.config['bg'],
                # fg=self.config['fg']
            )
        # 更新列表组件
        self.chapter_list_box.configure(
            font=(self.config['font'], self.config['font_size']),
            bg=self.config['bg'],
            fg=self.config['fg']
        )
    # 设置页设置函数
    def setting(self):
        font = self.font_label.get()
        font_size = self.font_size.get()
        theme = self.background.get()
        llms = self.llms.get()
        print(font,font_size,theme)
        SettingPage.setting(font, font_size,theme,llms)
        # 重新加载配置并刷新界面
        self.load_config()
        self.config['font_size'] = int(self.config['font_size'])  # 确保字体大小为整数

        # 更新主题样式
        self.root.style.theme_use(self.config['theme'])
        style = ttk.Style()
        #self.root.configure(background=self.root.style.colors.get('bg'))
        # 添加基础颜色配置映射
        self.config['bg'] = style.colors.get('bg')  # 使用主题的背景色
        self.config['fg'] = style.colors.get('fg')  # 使用主题的前景色
        # 主窗口背景色设置
        self.root.configure(background=style.colors.get('bg'))
        # 更新所有组件字体和颜色
        self.update_widget_style()
        self.hotkey_learning.configure(
            font=(self.config['font'], round(self.config['font_size'] * 1.6)),
            bg=self.config['bg'],  # 直接指定暗色背景
            fg='orange'  # 固定红色字体色
        )
        pass
    ######################################################################################################

    ######################################################################################################
    # 导航页函数
    # 书架刷新函数
    def local_fresh(self):
        BookListPage.fresh()
        self.local_book_list = BookListPage.book_case_local()
        self.local_case_box.delete(0, tk.END)
        for index, item in enumerate(self.local_book_list, 1):
            # 去除换行符并添加序号
            item_clean = f"{index}. {item[0].replace('\n', '')}"  # 假设书名在第一个元素
            self.local_case_box.insert("end", item_clean)
    # 打开本地书籍
    def open_local_book(self):
        # self.course = "local"
        # 获取书籍索引
        index = self.local_case_box.curselection()[0]

        # 获取书籍的章节信息
        self.chapter_last = BookListPage.get_chapter(self.local_book_list[index][0])
        title, text = BookOpen.readbook(self.chapter_last[0][0])
        # title, text = page2.get_text(self.course, self.chapter_last[0][0])
        bookname = self.local_book_list[index][0]
        # self.book_name['state'] = tk.NORMAL
        # self.book_name.delete(1.0,'end')
        # self.book_name.insert(1.0, bookname)
        self.book_name.delete(0, tk.END)
        self.book_name.insert("end", bookname)
        # self.book_name['state'] = tk.DISABLED

        self.chapter_list_box.delete(0, tk.END)
        for item in range(1, len(self.chapter_last) + 1):
            temp = str(item) + ' ' + self.chapter_last[item - 1][-1]
            self.chapter_list_box.insert("end", temp)
        self.chapter_list_box.selection_set(0)

        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        self.text_area.insert(1.0, text)
        self.text_area['state'] = tk.DISABLED

        self.switch_tab(1)
        pass
    # 删除本地书籍
    def del_local_book(self):
        index = self.local_case_box.curselection()
        index = index[0]
        book_name = self.local_book_list[index][0]
        BookListPage.del_local_book(book_name)
        self.local_fresh()
    ######################################################################################################

    ######################################################################################################
    # 阅读页函数
    # 阅读,选中章节
    def read_chapter_thread(self):
        thread = threading.Thread(target=self.read_chapter)
        thread.start()
    def read_chapter(self):
        chapter = self.chapter_list_box.curselection()
        print(chapter)
        # 检查 chapter 是否为空
        if not chapter:
            print("未选择任何章节，请先选择章节。")
            return
        self.chapter_index = chapter[0]
        select = self.chapter_last[chapter[0]]

        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        text_title, text_content = BookOpen.readbook(select[0])
        #text_title, text_content = page2.get_text(self.course, chapter[0])
        self.text_area.insert(1.0, text_content)
        self.text_area.insert(1.0, text_title[0] + '\n')
        self.text_area['state'] = tk.DISABLED
    # 退出该本书阅读
    def exit_book(self):
        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        self.text_area['state'] = tk.DISABLED
        # self.book_name['state'] = tk.NORMAL
        self.book_name.delete(1.0, 'end')
        # self.book_name['state'] = tk.DISABLED
        self.chapter_list_box.delete(0, tk.END)
        # 新增跳转到图书列表页
        self.main_page.select(0)  # 0对应第一个标签页（图书列表）
    # 下一章
    def next_page(self):
        thread = threading.Thread(target=self.goto_next)
        thread.start()
    def goto_next(self):
        # 如果当前章节不是最后一章，则跳转到下一章
        if self.chapter_index < len(self.chapter_last) - 1:
            # 跳转到下一章
            self.chapter_index += 1
            chapter = self.chapter_last[self.chapter_index]
            self.text_area['state'] = tk.NORMAL
            self.text_area.delete(1.0, 'end')
            text_title, text_content = BookOpen.readbook(chapter[0])
            self.text_area.insert(1.0, text_content)
            self.text_area.insert(1.0, text_title[0] + '\n')
            self.text_area['state'] = tk.DISABLED
    # 上一章
    def pre_page(self):
        thread = threading.Thread(target=self.goto_pre)
        thread.start()
    def goto_pre(self):
        if self.chapter_index > 0:
            self.chapter_index -= 1
            chapter = self.chapter_last[self.chapter_index]
            self.text_area['state'] = tk.NORMAL
            self.text_area.delete(1.0, 'end')
            text_title, text_content = BookOpen.readbook(chapter[0])
            self.text_area.insert(1.0, text_content)
            self.text_area.insert(1.0, text_title[0] + '\n')
            self.text_area['state'] = tk.DISABLED
    # 自由提问函数
    def ask_thread(self):
        thread = threading.Thread(target=self.ask)
        thread.start()
    def ask(self):
        print('开始执行')
        # 获取问题
        # 聚焦输入框
        self.Problem_Entry.focus_set()
        # 选中全部内容（从开始到结束）
        self.Problem_Entry.tag_add(tk.SEL, "1.0", tk.END)
        # 保持选中状态
        self.Problem_Entry.mark_set(tk.INSERT, "1.0")
        self.Problem_Entry.see(tk.INSERT)
        problem = self.Problem_Entry.get("1.0", "end-1c")
        print(problem)
        answer = LLMs_api.get_openai_responses(problem,self.config['llms'])
        print(answer)
        self.answer_area['state'] = tk.NORMAL
        self.answer_area.delete(1.0, 'end')
        self.answer_area.insert(1.0, answer)
        # 添加光标定位和视图控制
        # self.answer_area.mark_set("insert", "1.0")  # 设置光标到起始位置
        # self.answer_area.see("1.0")  # 确保内容从左上角可见
        self.answer_area['state'] = tk.DISABLED
        print('执行结束')
    # 清空问题框
    def clear_text(self):
        self.Problem_Entry.delete(1.0, tk.END)
    # 快捷按钮函数
    # 获取文本框中所有内容
    def get_full_text(self):
        """获取文本框全部内容"""
        self.text_area['state'] = tk.NORMAL  # 临时启用编辑状态
        content = self.text_area.get("1.0", "end-1c")  # 从开始到结尾获取内容（去除结尾换行符）
        self.text_area['state'] = tk.DISABLED  # 恢复禁用状态
        return content
    # 获取文本框中选中的内容
    def get_selected_text(self):
        """获取文本框中选中的内容"""
        try:
            return self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        except tk.TclError:
            return ""
    # 段落提问函数
    def paragraph_ask_thread(self):
        thread = threading.Thread(target=self.paragraph_ask)
        thread.start()
    def paragraph_ask(self):
        print('paragraph_ask开始执行')
        # 获取选中的文本
        selected_text = self.get_selected_text()
        print(selected_text)
        # 获取输入的问题
        problem = self.Problem_Entry.get("1.0", "end-1c").strip()
        if selected_text:
            problem += f"\n\n[相关上下文]\n{selected_text}"
            print(f"完整提问内容：{problem}")
            answer = LLMs_api.get_deepseek_responses(problem)
            self.answer_area['state'] = tk.NORMAL
            self.answer_area.delete(1.0, 'end')
            self.answer_area.insert(1.0, answer)
            self.answer_area['state'] = tk.DISABLED
        elif selected_text == "":
            print("未选中任何文本")
            self.answer_area['state'] = tk.NORMAL
            self.answer_area.delete(1.0, 'end')
            self.answer_area.insert(1.0, "未选中任何文本")
            self.answer_area['state'] = tk.DISABLED
            print("paragraph_ask执行结束")
    # 全文提问函数
    def summary_ask_thread(self):
        thread = threading.Thread(target=self.summary_ask)
        thread.start()
    def summary_ask(self):
        print('summary_ask开始执行')
        # 获取选中的文本
        selected_text = self.get_full_text()
        print(selected_text)
        # 获取输入的问题
        problem = self.Problem_Entry.get("1.0", "end-1c").strip()
        if selected_text:
            problem += f"\n\n[相关上下文]\n{selected_text}"
            print(f"完整提问内容：{problem}")
            answer = LLMs_api.get_deepseek_responses(problem)
            self.answer_area['state'] = tk.NORMAL
            self.answer_area.delete(1.0, 'end')
            self.answer_area.insert(1.0, answer)
            self.answer_area['state'] = tk.DISABLED
        elif selected_text == "":
            print("未选中任何文本")
            self.answer_area['state'] = tk.NORMAL
            self.answer_area.delete(1.0, 'end')
            self.answer_area.insert(1.0, "未选中任何文本")
            self.answer_area['state'] = tk.DISABLED
            print("summary_ask执行结束")
    # 全文总结
    def summary_thread(self):
        thread = threading.Thread(target=self.summary)
        thread.start()
    def summary(self):
        print("全文总结开始执行")
        selected_text = self.get_full_text()
        # 获取输入的问题
        # problem = self.Problem_Entry.get("1.0", "end-1c").strip()

        # 自定义问题模板（可在此处修改模板格式）
        problem = f"[对以上给出的相关段落，进行大意总结]"
        if selected_text:
            problem += f"\n\n[相关上下文]\n{selected_text}"

        print(f"完整提问内容：{problem}")
        answer = LLMs_api.get_deepseek_responses(problem)

        # 显示回答
        self.answer_area['state'] = tk.NORMAL
        self.answer_area.delete(1.0, 'end')
        self.answer_area.insert(1.0, answer)
        self.answer_area['state'] = tk.DISABLED
        print('执行结束')
        pass
    # 段落总结
    def paragraph_summary_thread(self):
        thread = threading.Thread(target=self.paragraph_summary)
        thread.start()
    def paragraph_summary(self):
        print("段落总结开始执行")
        selected_text = self.get_selected_text()
        # 获取输入的问题
        # problem = self.Problem_Entry.get("1.0", "end-1c").strip()

        # 自定义问题模板（可在此处修改模板格式）
        problem = f"[对以上给出的相关段落，进行大意总结]"
        if selected_text:
            problem += f"\n\n[相关上下文]\n{selected_text}"

        print(f"完整提问内容：{problem}")
        answer = LLMs_api.get_deepseek_responses(problem)

        # 显示回答
        self.answer_area['state'] = tk.NORMAL
        self.answer_area.delete(1.0, 'end')
        self.answer_area.insert(1.0, answer)
        self.answer_area['state'] = tk.DISABLED
        print('执行结束')

        pass
    # 重点段落
    def key_paragraph_thread(self):
        thread = threading.Thread(target=self.key_paragraph)
        thread.start()
    def key_paragraph(self):
        print("重点段落开始执行")
        selected_text = self.get_full_text()
        problem = f"[对以上给出的相关段落，进行重点句子标识，并将每一句重点句子都分别返回在中括号中返回给我，中括号内只能包含未修改的原文，重点段落不能太集中在某几段。]"
        if selected_text:
            problem += f"\n\n[相关上下文]\n{selected_text}"
        print(f"完整提问内容：{problem}")
        answer = LLMs_api.get_deepseek_responses(problem)
        print(answer)
        # 提取回答中中括号内的内容，并将其存储到列表中
        answer = list(set(re.findall(r'\[(.*?)\]', answer)))
        print(answer)
        # 新增高亮逻辑
        self.text_area.tag_remove('highlight', '1.0', 'end')  # 清除旧的高亮
        self.text_area['state'] = tk.NORMAL
        for sentence in answer:
            start = '1.0'
            while True:
                pos = self.text_area.search(sentence, start, stopindex='end')
                if not pos:
                    break
                end = f"{pos}+{len(sentence)}c"
                self.text_area.tag_add('highlight', pos, end)
                start = end
        self.text_area.tag_config('highlight', foreground='red')  # 设置高亮颜色
        self.text_area['state'] = tk.DISABLED
    # 人物提取
    def person_extract_thread(self):
        thread = threading.Thread(target=self.person_extract)
        thread.start()
    def person_extract(self):
        print("人物提取开始执行")
        selected_text = self.get_full_text()
        print(selected_text)
        problem = f"[对以上给出的相关段落，进行关键人物提取，并对文中关键人物的行为和心理做简单总结。]"
        if selected_text:
            problem += f"\n\n[相关上下文]\n{selected_text}"
            print(f"完整提问内容：{problem}")
            answer = LLMs_api.get_deepseek_responses(problem)
            self.answer_area['state'] = tk.NORMAL
            self.answer_area.delete(1.0, 'end')
            self.answer_area.insert(1.0, answer)
            self.answer_area['state'] = tk.DISABLED
        elif selected_text == "":
            print("未选中任何文本")
            self.answer_area['state'] = tk.NORMAL
            self.answer_area.delete(1.0, 'end')
            self.answer_area.insert(1.0, "未选中任何文本")
            self.answer_area['state'] = tk.DISABLED
            print("paragraph_ask执行结束")
    ######################################################################################################
    # 跳转标签页函数
    def switch_tab(self, tab_index: int):
        """通过索引切换标签页（0=图书列表，1=阅读，2=设置）"""
        print("切换窗口")
        self.main_page.select(tab_index)
        pass
    # 回车事件处理函数
    def enter_handler(self):
        if self.main_page.index(self.main_page.select()) == 0:  # 在图书列表页
            self.open_local_book()
        elif self.main_page.index(self.main_page.select()) == 1:  # 在阅读页
            self.read_chapter_thread()

print("UI初始化成功！")


######################################################################################################


def toggle_listbox(listbox):
    if listbox.winfo_ismapped():
        listbox.pack_forget()  # 隐藏 Listbox
    else:
        listbox.pack(fill=tk.BOTH, expand=True)  # 显示