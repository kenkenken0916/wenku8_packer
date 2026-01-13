# wenku8_packer

將 wenku8 輕小說文字與插圖自動打包成 EPUB 的工具。

## 功能特色

- 解析文字中的章節與插圖標記  
  - 支援格式：`第x章`、`（插圖006）`
- 自動處理插圖：
  - 第一張圖作為封面
  - 若第一個插圖不是 1，自動建立「插圖章（chap0）」
  - 未被文字引用的圖片，自動附加到最後一章
- 支援 png / jpg / jpeg
- 產出標準 EPUB（ebooklib）

## 使用需求

- Python 3.10+
- ebooklib

安裝依賴：
```bash
pip install ebooklib
```
## 使用說明
將.txt file 放在同一個 dir 執行 interface.py \
根據要求放入每一本第一張"圖片"連結 要點進去圖片！！！\
根據不同書可能需要調整章節的偵測 （想想書癡的取名）\
就不吐槽取名了\
```python
#maker.py:79
pattern2 = re.compile(r'^第[一二三四五六七八九十百千零〇]+卷')
```
如果不在意也不用改，基本上不影響

## BLABBLABBLAB
輕鬆小程式\
爬蟲不想寫\
檔案不會照順序我也懶著改了\
出問題告訴我，~~我不會改~~