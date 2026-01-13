from ebooklib import epub
import os
import re


def create_epub(txt_file, output_file, pic_dir="pics"):
    """
    從 TXT 文件和圖片創建 EPUB
    
    參數:
        txt_file: 輸入的 TXT 文件路徑
        output_file: 輸出的 EPUB 文件路徑
        pic_dir: 圖片目錄 (默認: "pics")
    
    返回:
        成功返回 True，失敗返回 False
    """
    # === 初始化書籍 ===
    # === 由 txt 檔名取得書名 ===
    book_title = os.path.splitext(os.path.basename(txt_file))[0]

    book = epub.EpubBook()
    book.set_identifier("ken_support_epub")
    book.set_title(book_title)
    book.set_language("zh")
    book.add_author("Auto")

    chapters = []
    spine = ["nav"]

    chapter_count = 0
    pic_count = 0
    used_pics = set()

    first_pic_num = None
    pre_pics = []       # chap0 用
    
    # === 工具函式 ===
    def find_image(num):
        for ext, mime in [("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg")]:
            path = os.path.join(pic_dir, f"{num}.{ext}")
            if os.path.exists(path):
                print(f"找到圖片：{path}")
                return path, ext, mime
        return None, None, None

    def add_image(num):
        nonlocal pic_count
        if num in used_pics:
            return

        path, ext, mime = find_image(num)
        if not path:
            return

        with open(path, "rb") as f:
            img = epub.EpubImage(
                uid=f"img{num}",
                file_name=f"images/{num}.{ext}",
                media_type=mime,
                content=f.read()
            )
        book.add_item(img)
        used_pics.add(num)
        print(f"加入圖片：{path}")
        pic_count += 1

    # === 讀取 TXT ===
    current_title = None
    current_html = ""

    #add_image(1)
    path, ext, _ = find_image(1)
    if path:
        with open(path, "rb") as f:
            book.set_cover(f"cover.{ext}", f.read())

    try:
        with open(txt_file, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                # === 章節 ===
                pattern = re.compile(r'插圖\s*(\d+)')
                pattern2 = re.compile(r'^第[一二三四五六七八九十百千零〇]+卷')

                if pattern2.search(line):
                    if current_title:
                        c = epub.EpubHtml(
                            title=current_title,
                            file_name=f"chap{chapter_count}.xhtml",
                            lang="zh"
                        )
                        c.content = current_html
                        book.add_item(c)
                        chapters.append(c)
                        spine.append(c)

                    chapter_count += 1
                    current_title = line
                    current_html = f"<h1>{line}</h1>\n"

                # === 插圖00n / 插圖0n / 插圖n ===
                elif pattern.search(line):
                    num = int(re.sub(r"\D", "", line))

                    if num > 1:
                        for i in range(1, num):
                            add_image(i)
                            pre_pics.append(i)
                    add_image(num)

                    # 插入圖片到章節內
                    path, ext, _ = find_image(num)
                    if path:
                        current_html += f'<img src="images/{num}.{ext}"/><br/>\n'

                # === 一般文字 ===
                else:
                    current_html += f"<p>{line}</p>\n"

        # === 最後一章 ===
        # === 補齊剩餘插圖：從 pic_count+1 開始，直到找不到圖 ===
        if chapters:
            last_chapter = chapters[-1]

            next_pic = pic_count + 1

            while True:
                path, ext, _ = find_image(next_pic)
                if not path:
                    break  # 找不到就結束

                if next_pic not in used_pics:
                    add_image(next_pic)
                    last_chapter.content += (
                        f'<hr/>\n'
                        f'<img src="images/{next_pic}.{ext}"/><br/>\n'
                    )

                next_pic += 1

        if current_title:
            c = epub.EpubHtml(
                title=current_title,
                file_name=f"chap{chapter_count}.xhtml",
                lang="zh"
            )
            c.content = current_html
            book.add_item(c)
            chapters.append(c)
            spine.append(c)

        # === chap0：插圖集（在第一章前） ===
        if pre_pics:
            html = "<h1>插圖</h1>\n"
            for n in pre_pics:
                path, ext, _ = find_image(n)
                if path:
                    html += f'<img src="images/{n}.{ext}"/><br/>\n'

            chap0 = epub.EpubHtml(
                title="插圖",
                file_name="chap0.xhtml",
                lang="zh"
            )
            chap0.content = html
            book.add_item(chap0)

            chapters.insert(0, chap0)
            spine.insert(1, chap0)  # nav 後、chap1 前

        # === EPUB 結構 ===
        book.toc = chapters
        book.spine = spine
        book.add_item(epub.EpubNav())
        book.add_item(epub.EpubNcx())

        # === 輸出 ===
        epub.write_epub(output_file, book)

        print(f"章節數量：{chapter_count}")
        print(f"圖片數量：{pic_count}")
        print("EPUB 產生完成")
        
        return True
        
    except Exception as e:
        print(f"錯誤：{e}")
        import traceback
        traceback.print_exc()
        return False


# 支持直接執行（向後兼容）
if __name__ == "__main__":
    TXT_FILE = "aaa.txt"
    OUT_FILE = "aaa.epub"
    PIC_DIR = "pics"
    
    create_epub(TXT_FILE, OUT_FILE, PIC_DIR)
