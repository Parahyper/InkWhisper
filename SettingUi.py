import tkinter as tk
import ttkbootstrap as ttk
import tkinter.font

def setup_settings_tab(ui_instance):
    # 设置页页面设计

    # 字体设置
    tk.Label(
        ui_instance.tab3,
        text='字体设置:',
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    ).place(relx=0.05, rely=0.04, relwid=0.08, relhei=0.05)
    ui_instance.font_label = ttk.Combobox(
        ui_instance.tab3,
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )  # 创建下拉菜单
    ui_instance.font_label.place(relx=0.15, rely=0.05, relwid=0.1)  # 将下拉菜单绑定到窗体
    all_fonts = tkinter.font.families()
    chinese_fonts = [
        f for f in all_fonts
        if any(char in f for char in ['宋', '楷', '黑', '仿', '华'])  # 常见中文字体特征
           and '@' not in f  # 排除部分字体
    ]
    ui_instance.font_label["value"] = sorted(set(chinese_fonts))  # 获取系统所有可用字体
    ui_instance.font_label.current(13)

    # 字体大小
    tk.Label(
        ui_instance.tab3,
        text='字体大小:',
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    ).place(relx=0.3, rely=0.04, relwid=0.08, relhei=0.05)
    ui_instance.font_size = tk.Entry(
        ui_instance.tab3,
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )
    ui_instance.font_size.place(relx=0.4, rely=0.05, relwid=0.05)
    ui_instance.font_size.insert(0, str(ui_instance.config.get('font_size', 16)))

    # 背景颜色
    # 暗色cyborg darkly solar superhero亮色journal flatly minty litera united pulse cosmo lumen yeti sandstone
    tk.Label(
        ui_instance.tab3,
        text='主题选择:',
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    ).place(relx=0.05, rely=0.14, relwid=0.08, relhei=0.05)
    ui_instance.background = ttk.Combobox(
        ui_instance.tab3,
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )  # 创建下拉菜单
    ui_instance.background.place(relx=0.15, rely=0.15, relwid=0.1)  # 将下拉菜单绑定到窗体
    ui_instance.background["value"] = ("litera", "darkly", "superhero", "journal", "sandstone")  # 给下拉菜单设定值
    ui_instance.background.current(0)

    # 朗读音色
    tk.Label(
        ui_instance.tab3,
        text='人声朗读:',
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    ).place(relx=0.05, rely=0.24, relwid=0.08, relhei=0.05)
    read_aloud = ttk.Combobox(
        ui_instance.tab3,
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )  # 创建下拉菜单
    read_aloud.place(relx=0.15, rely=0.25, relwid=0.1)  # 将下拉菜单绑定到窗体
    read_aloud["value"] = ("windows", "女声", "男声")  # 给下拉菜单设定值
    read_aloud.current(0)

    # 大模型选择
    tk.Label(
        ui_instance.tab3,
        text='模型选择:',
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    ).place(relx=0.05, rely=0.34, relwid=0.08, relhei=0.05)
    ui_instance.llms = ttk.Combobox(
        ui_instance.tab3,
        font=(ui_instance.config['font'], ui_instance.config['font_size'])
    )  # 创建下拉菜单
    ui_instance.llms.place(relx=0.15, rely=0.35, relwid=0.1)  # 将下拉菜单绑定到窗体
    ui_instance.llms["value"] = ("DeepSeek", "Doubao", "通义千问")  # 给下拉菜单设定值
    ui_instance.llms.current(0)

    # 确定设置按钮尚未绑定对应函数
    setting_button = tk.Button(
        ui_instance.tab3,
        text="确定设置",
        font=(ui_instance.config['font'], ui_instance.config['font_size']),
        command=ui_instance.setting
    )
    setting_button.place(relx=0.05, rely=0.8, relwid=0.08, relhei=0.04)

    # 热键提示框
    ui_instance.hotkey_learning = tk.Text(
        ui_instance.tab3,
        font=(ui_instance.config['font'], round(ui_instance.config['font_size'] * 1.6)),
        bg=ui_instance.config['bg'],  # 使用主题背景色
        fg='orange'  # 使用红色固定色
    )
    ui_instance.hotkey_learning.insert('1.0',
                                '热键提示：\n'
                                'Ctrl+回车 - 打开书籍\n'
                                'F5 - 刷新书库\n'
                                'Ctrl+回车 - 打开章节\n'
                                'Ctrl+← - 上一章\n'
                                'Ctrl+→ - 下一章\n'
                                'Ctrl+Esc - 退出阅读\n'
                                'Ctrl+退格 - 清空提问框'
                                )  # 新增插入文本
    ui_instance.hotkey_learning.place(relx=0.55, rely=0.05, relwid=0.35, relhei=0.5)