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

