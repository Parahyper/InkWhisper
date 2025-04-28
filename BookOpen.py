def readbook(url):
    f = open(url, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    return '', text
