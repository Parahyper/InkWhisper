def setting(font="宋体", font_size=16, theme="litera",llms="deepseek",bg="white", fg="black"):
    f = open("config.txt", 'w', encoding='utf-8')
    print(font,font_size,bg,fg,theme)
    text = 'font:'+font+'\n'+'font_size:'+str(font_size)+'\n'+'bg:'+bg+'\n'+'fg:'+fg+'\n'+'theme:'+theme+'\n'+'llms:'+llms
    f.write(text)
    f.close()