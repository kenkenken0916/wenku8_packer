#!/usr/bin/env python3
"""
EPUB 自動生成介面
掃描目錄中的所有 .txt 文件，並為每個文件：
1. 詢問第一張圖片的 URL
2. 清理 pics 目錄
3. 下載圖片
4. 生成 EPUB（名稱與 txt 文件相同）
"""

import os
import shutil
import glob

# 導入本地模組
from getpics import download_pictures
from maker import create_epub

# 設定常量
PICS_DIR = "pics"


def find_txt_files():
    """掃描當前目錄中的所有 .txt 文件"""
    txt_files = glob.glob("*.txt")
    if not txt_files:
        print("未找到任何 .txt 文件")
        return []
    
    print(f"\n找到 {len(txt_files)} 個 txt 文件:")
    for i, file in enumerate(txt_files, 1):
        print(f"  {i}. {file}")
    
    return txt_files


def clean_pics_dir():
    """清空 pics 目錄"""
    if os.path.exists(PICS_DIR):
        print(f"\n清理 {PICS_DIR} 目錄...")
        shutil.rmtree(PICS_DIR)
    os.makedirs(PICS_DIR, exist_ok=True)
    print(f"✔ {PICS_DIR} 目錄已清空")


def get_pic_url_info():
    """詢問用戶圖片 URL 相關信息"""
    print("\n=== 圖片下載設定 ===")
    
    # 完整 URL（包含文件名）
    full_url = input("請輸入第一張圖片的完整 URL（例如：https://pic.777743.xyz/3/3453/150446/185077.jpg）: ").strip()
    if not full_url:
        print("錯誤：URL 不能為空")
        return None
    
    # 解析 URL
    try:
        # 分離基礎 URL 和文件名
        if '/' not in full_url:
            print("錯誤：URL 格式不正確")
            return None
        
        base_url = full_url.rsplit('/', 1)[0] + '/'
        filename = full_url.rsplit('/', 1)[1]
        
        # 從文件名中提取編號和格式
        if '.' not in filename:
            print("錯誤：文件名必須包含擴展名")
            return None
        
        name_part, ext = filename.rsplit('.', 1)
        
        # 提取數字編號
        import re
        match = re.search(r'(\d+)', name_part)
        if not match:
            print("錯誤：無法從文件名中提取數字編號")
            return None
        
        start_num = int(match.group(1))
        
        # 驗證擴展名
        ext = ext.lower()
        if ext not in ["jpg", "png", "jpeg"]:
            print(f"警告：擴展名 '{ext}' 可能不支持，使用 jpg")
            ext = "jpg"
        
        print(f"\n解析結果：")
        print(f"  基礎 URL: {base_url}")
        print(f"  起始編號: {start_num}")
        print(f"  圖片格式: {ext}")
        
        return {
            "base_url": base_url,
            "start_num": start_num,
            "ext": ext
        }
        
    except Exception as e:
        print(f"錯誤：解析 URL 失敗 - {e}")
        return None


def process_txt_file(txt_file):
    """處理單個 txt 文件"""
    print("\n" + "="*60)
    print(f"處理文件：{txt_file}")
    print("="*60)
    
    # 1. 詢問圖片 URL
    pic_info = get_pic_url_info()
    if not pic_info:
        print(f"✘ 跳過 {txt_file}")
        return False
    
    # 2. 清理 pics 目錄
    clean_pics_dir()
    
    # 3. 下載圖片
    print("\n=== 開始下載圖片 ===")
    try:
        saved = download_pictures(
            pic_info["base_url"],
            pic_info["start_num"],
            pic_info["ext"],
            PICS_DIR
        )
        if saved == 0:
            print("✘ 沒有下載到任何圖片")
            return False
        print(f"✔ 圖片下載完成，共 {saved} 張")
    except Exception as e:
        print(f"✘ 圖片下載失敗：{e}")
        return False
    
    # 4. 生成 EPUB
    print(f"\n=== 開始生成 EPUB ===")
    output_epub = txt_file.rsplit('.', 1)[0] + '.epub'
    try:
        if create_epub(txt_file, output_epub, PICS_DIR):
            print(f"✔ EPUB 生成完成")
        else:
            print(f"✘ EPUB 生成失敗")
            return False
    except Exception as e:
        print(f"✘ EPUB 生成失敗：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n✔✔✔ {txt_file} 處理完成！生成文件：{output_epub}")
    return True


def main():
    """主函數"""
    print("="*60)
    print("EPUB 自動生成介面")
    print("="*60)
    
    # 掃描 txt 文件
    txt_files = find_txt_files()
    if not txt_files:
        return
    
    # 詢問處理方式
    print("\n選擇處理方式：")
    print("  1. 處理所有 txt 文件")
    print("  2. 選擇特定文件處理")
    
    choice = input("\n請輸入選擇（1/2，預設 1）: ").strip()
    
    files_to_process = []
    
    if choice == "2":
        print("\n輸入要處理的文件編號（用逗號分隔，例如：1,3,5）：")
        indices = input("> ").strip()
        try:
            selected_indices = [int(i.strip()) for i in indices.split(',')]
            for idx in selected_indices:
                if 1 <= idx <= len(txt_files):
                    files_to_process.append(txt_files[idx - 1])
                else:
                    print(f"警告：編號 {idx} 超出範圍")
        except ValueError:
            print("錯誤：輸入格式不正確")
            return
    else:
        files_to_process = txt_files
    
    if not files_to_process:
        print("沒有要處理的文件")
        return
    
    # 處理每個文件
    success_count = 0
    for txt_file in files_to_process:
        if process_txt_file(txt_file):
            success_count += 1
    
    # 總結
    print("\n" + "="*60)
    print(f"處理完成！成功：{success_count}/{len(files_to_process)}")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用戶中斷操作")
    except Exception as e:
        print(f"\n錯誤：{e}")
        import traceback
        traceback.print_exc()
