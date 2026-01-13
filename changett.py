import os
import zipfile
import xml.etree.ElementTree as ET

EPUB_DIR = "."
EXT = ".epub"

for fname in os.listdir(EPUB_DIR):
    if not fname.lower().endswith(EXT):
        continue

    epub_path = os.path.join(EPUB_DIR, fname)
    title = os.path.splitext(fname)[0]

    print(f"修正 {fname} → title = {title}")

    with zipfile.ZipFile(epub_path, 'r') as zin:
        items = {info.filename: zin.read(info.filename) for info in zin.infolist()}

    # 找 content.opf 或 *.opf
    opf_name = None
    for name in items:
        if name.endswith(".opf"):
            opf_name = name
            break

    if not opf_name:
        print(f"⚠️ 找不到 OPF: {fname}")
        continue

    # 修改 <dc:title>
    tree = ET.fromstring(items[opf_name])
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    for dc_title in tree.findall(".//dc:title", ns):
        dc_title.text = title

    # 將修改後的 OPF bytes
    new_opf = ET.tostring(tree, encoding='utf-8', xml_declaration=True)

    # 寫回 EPUB
    with zipfile.ZipFile(epub_path, 'w') as zout:
        for name, data in items.items():
            if name == opf_name:
                zout.writestr(name, new_opf)
            else:
                zout.writestr(name, data)
