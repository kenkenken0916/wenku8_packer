import os
import requests
import time


def download_pictures(base_url, start_num, ext, out_dir="pics", max_fail=3, sleep=0.3):
    """
    下載圖片函數
    
    參數:
        base_url: 圖片基礎 URL (例如: "https://pic.777743.xyz/3/3453/150446/")
        start_num: 起始圖片編號 (例如: 185078)
        ext: 圖片擴展名 (例如: "jpg")
        out_dir: 輸出目錄 (默認: "pics")
        max_fail: 連續失敗幾次就停止 (默認: 3)
        sleep: 每張圖間隔秒數 (默認: 0.3)
    
    返回:
        下載成功的圖片數量
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.wenku8.net/",
    }

    os.makedirs(out_dir, exist_ok=True)

    session = requests.Session()
    session.headers.update(headers)

    fail_count = 0
    num = start_num
    saved = 0

    while True:
        url = f"{base_url}{num}.{ext}"
        out_path = os.path.join(out_dir, f"{saved + 1}.{ext}")

        try:
            r = session.get(url, timeout=10)
            if r.status_code != 200 or len(r.content) < 1024:
                raise Exception("download failed")

            with open(out_path, "wb") as f:
                f.write(r.content)

            print(f"✔ {out_path}")
            saved += 1
            fail_count = 0
            num += 1
            time.sleep(sleep)

        except Exception:
            print(f"✘ 停止於 {url}")
            fail_count += 1
            num += 1
            if fail_count >= max_fail:
                break

    print(f"\n完成，共下載 {saved} 張圖片")
    return saved


# 支持直接執行（向後兼容）
if __name__ == "__main__":
    BASE_URL = "https://pic.777743.xyz/3/3453/150446/"
    START_NUM = 185078
    EXT = "jpg"
    OUT_DIR = "pics"
    
    download_pictures(BASE_URL, START_NUM, EXT, OUT_DIR)
