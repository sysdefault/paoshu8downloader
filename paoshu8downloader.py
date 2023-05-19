# pip install requests bs4 -i https://pypi.mirrors.ustc.edu.cn/simple
import os, random, time, requests, bs4

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
site = "http://www.paoshu8.com"
Y = 0

print("功能：下载给定的泡书吧网(http://www.paoshu8.com/)小说，并保存至脚本所在路径")
url = input("请输入小说章节目录页网址(例http://www.paoshu8.com/60_60363/)：\n")
print("分析中，请稍后...")
soup = bs4.BeautifulSoup(requests.get(url, headers = headers).content, 'html.parser', from_encoding="utf-8")
chapter_list = [chapter.get('href') for chapter in soup.find_all('div', id='list')[0].find_all('a')][9:]
book_title = soup.find('div', id='info').find('h1').text.strip()
begin = int(input(f"《{book_title}》共{len(chapter_list)}章\n你想从第几章开始下载：\n"))
end = int(input("你想下载至第几章结束：\n"))
choice = input("分章保存(各个章节单独保存)输入 1\n整本保存(所选章节存入一个文件)输入 2\n请选择保存方式：\n")

def parse_chapter(chapter, headers):
    soup = bs4.BeautifulSoup(requests.get(chapter, headers=headers).content, "html.parser", from_encoding="utf-8")
    chapter_name = soup.find("div", class_="bookname").h1.string
    text_list = [chapter_name, "\n\n"] + [p.text for p in soup.find('div', id='content').find_all('p')]
    return text_list, chapter_name

def increment_Y():
    global Y
    Y += 1
    return Y

def download_progress(chapter_name, Y, begin, end, book_title, download_path):
    print(f"{chapter_name} 下载完成 进度{increment_Y()}/{end - begin + 1}")
    if Y + 1 == end - begin + 1:
        print(f"已下载《{book_title}》第{begin}章至第{end}章，共{end - begin + 1}章，已保存至{download_path}，退出...")
        exit()
    time.sleep(random.randint(4, 6))

if choice == "1":
    print(f"将下载《{book_title}》第{begin}章至第{end}章，共{end - begin + 1}章，分章保存，开始下载...")
    for i in range(end - begin + 1):
        chapter = site + chapter_list[begin + i - 1]
        text_list, chapter_name = parse_chapter(chapter, headers)
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), book_title)
        os.makedirs(download_path, exist_ok=True)
        file_path = os.path.join(download_path, chapter_name + ".txt")
        text_all = "".join(text_list[:2])
        text_all += "\n".join(text_list[2:])
        text_all += "\n"
        with open(file_path, "w", encoding = "utf-8") as f:
            f.write(text_all)
        download_progress(chapter_name, Y, begin, end, book_title, download_path)

elif choice == "2":
    print(f"将下载《{book_title}》第{begin}章至第{end}章，共{end - begin + 1}章，整本保存，开始下载...")
    for i in range(end - begin + 1):
        chapter = site + chapter_list[begin + i - 1]
        text_list, chapter_name = parse_chapter(chapter, headers)
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), book_title + ".txt")
        text_all = "".join(text_list[:2])
        text_all += "\n".join(text_list[2:])
        text_all += "\n\n"
        with open(download_path, "a", encoding = "utf-8") as f:
            f.write(text_all)
        download_progress(chapter_name, Y, begin, end, book_title, download_path)

else:
    print("保存方式选择无效")
    exit()
