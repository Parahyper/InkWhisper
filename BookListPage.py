import os
import shutil


# 显示书架上的书
def book_case_local():
    local_book = open('book_case\\local_book.txt', 'r', encoding='utf-8')
    lb_list = local_book.readlines()
    local_book.close()

    local_list = []
    for line in lb_list:
        temp = line.split(' ')
        local_list.append(temp)

    return local_list


# 更新本地书架
def fresh():
    book = []
    f = open("book_case/local_book.txt", 'w', encoding='utf-8')
    for item in os.listdir('book'):
        if 'book_message.txt' in os.listdir('book/'+ item):
            files = open('book/' + item + '/book_message.txt', 'r', encoding='utf-8')
            book.append(files.read()+'\n')
            files.close()
    # if book and book[-1].endswith('\n'):
    #     book[-1] = book[-1].rstrip('\n')
    with open("book_case/local_book.txt", 'w', encoding='utf-8') as f:
         f.writelines(book)
    f.close()


# 删除本地书籍
def del_local_book(bookname):
    shutil.rmtree("book/"+bookname)


# 获取章节信息
def get_chapter(bookname):
    bookname = bookname.rstrip()
    path = 'book/' + bookname
    answer = []
    f = open(path + '/chapter.txt', 'r', encoding='utf-8')
    chapter_name = f.readlines()
    for item in range(len(chapter_name)):
        answer.append((path+'/text/'+str(item+1)+'.txt', chapter_name[item]))
    return answer
