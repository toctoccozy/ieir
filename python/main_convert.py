import os
import re
import sys
import html as html_lib
from bs4 import BeautifulSoup

# --- 設定 ---
# パスの設定（実行場所からの相対パス）
INPUT_DIR = "output_files"
FORMAT_DIR = "../format"
OUTPUT_DIR = "../products"

FORMAT_01 = "format_01.html"  # 単一タイプ
FORMAT_02 = "format_02.html"  # 複数タイプ

# カテゴリ（output_files / products 内のサブフォルダ名）
CATEGORIES = ["gallery", "jewelry", "mens", "treasure", "women"]

IMAGE_BASE = "/image/goods/"

# 2枚横並びの条件: 幅がこれ以下・縦長(高さ≧幅)で、縦横比の差がこの倍率以内
PAIR_IMG_MAX_WIDTH = 400
PAIR_RATIO_TOLERANCE = 1.5

# 商品詳細エリアのインデント
IND = " " * 20

# 商品詳細エリアの部品ごとのclass（format_01/02の商品詳細の見本と同じ内容にそろえること）
CSS = {
    "p": "text-start px-1 sm:p-3 leading-relaxed",
    "img": "w-full max-w-2xl mx-auto h-auto p-4",
    "h2": "text-white rounded-md font-bold text-lg c-bg-collection-gradient text-center sm:p-3 py-2 mx-1",
    "pair_wrap": "flex flex-col md:flex-row md:items-start gap-2",
    "pair_img": "w-full max-w-[350px] mx-auto h-auto p-4",
    "float_wrap": "flex flex-col sm:items-start",
    "float_img": "mx-auto max-w-[10rem] p-3 sm:m-3 object-contain",
    "box_wrap": "p-3 m-1 border c-border-collection-gradient border-1 rounded-md",
    "box_h3": "font-bold p-2",
    "box_h3_logo": "font-bold p-2 flex items-center gap-2",
    "box_logo": "max-h-8 max-w-[12rem] w-auto h-auto object-contain",
    "box_text": "leading-relaxed flex p-2 flex-col sm:flex-row sm:items-start gap-3",
    "box_photo": "w-32 sm:w-36 h-auto object-contain shrink-0 mx-auto sm:mx-0",
    "box_dl": "leading-relaxed p-2 text-sm",
    "box_img": "w-full max-w-sm mx-auto h-auto p-4",
    "box_pair_wrap": "flex flex-col md:flex-row md:items-start justify-center gap-2",
    "box_pair_img": "w-full max-w-[10rem] mx-auto md:mx-0 h-auto p-2",
    "movie_wrap": "w-full max-w-2xl mx-auto p-4",
    "movie": "w-full aspect-video",
    "spec_img": "block w-full max-w-xs mt-2 mb-4",  # 仕様欄のサイズ表など（PCで小さめ表示）
}

# --- ユーティリティ関数 ---

def flat_text(elem):
    """要素のテキストを取り出し、改行・<br>・行頭のタブ等を除いて1行にする"""
    if elem is None:
        return ""
    text = elem.get_text("\n") if hasattr(elem, "get_text") else str(elem)
    return "".join(line.strip() for line in text.splitlines())

def add_br_by_period(text, indent):
    """句点「。」ごとに<br>を入れる（「。」」のように閉じ括弧が続く場合はその後ろ）"""
    text = re.sub(r"。([」』）)]*)(?!$)", r"。\1<br>\n" + indent, text.strip())
    return text

def img_src(img):
    """画像パスを /image/goods/ 始まりにそろえる"""
    src = img.get("src", "").strip()
    if src.startswith("/") or src.startswith("http"):
        return src
    return IMAGE_BASE + src.split("/")[-1]

def img_alt(img):
    alt = "".join(line.strip() for line in img.get("alt", "").splitlines())
    return html_lib.escape(alt, quote=True)

def split_by_br(elem):
    """<br>区切りで行に分割する（空行も保持）"""
    parts = re.split(r"<br\s*/?>", elem.decode_contents(), flags=re.IGNORECASE)
    return [flat_text(BeautifulSoup(p, "html.parser")) for p in parts]

def is_image_only(elem):
    return elem.find("img") is not None and not flat_text(elem)

# --- 旧ページの解析 ---

def parse_specs(soup):
    """仕様<dd>を行リストと画像リスト（サイズ表など）で取得"""
    dd = None
    dt = soup.find("dt", string=re.compile(r"仕\s*様"))
    if dt:
        dd = dt.find_next_sibling("dd")
    if dd is None:
        dd = soup.find("dd")
    if dd is None:
        return [], []
    # 画像は文章と分けて取り出す
    imgs = []
    for img in dd.find_all("img"):
        imgs.append(img)
        holder = img.parent if img.parent is not dd and not flat_text(img.parent) else img
        holder.extract()
    lines = split_by_br(dd)
    while lines and not lines[-1]:
        lines.pop()
    return lines, imgs

def split_specs_by_type(lines, item_nos):
    """
    【見出し】ごとに仕様を分割し、商品番号と対応づける。
    末尾の※注記は全タイプ共通として各タイプに付ける。
    分割できない・数が合わない場合は None を返す（共通扱い）。
    """
    prefix, groups = [], []
    for line in lines:
        if re.fullmatch(r"【.+?】", line):
            groups.append([])
        elif groups:
            groups[-1].append(line)
        else:
            prefix.append(line)

    if not groups:
        return None
    if len(groups) != len(item_nos):
        print(f"  [注意] 仕様の【】の数({len(groups)})とタイプ数({len(item_nos)})が一致しないため共通扱いにします")
        return None

    # 最後のグループ末尾の※注記を共通注記として取り出す
    notes = []
    last = groups[-1]
    while last and not last[-1]:
        last.pop()
    if "" in last:
        tail_start = len(last) - last[::-1].index("")
        tail = last[tail_start:]
        if tail and all(t.startswith("※") for t in tail):
            notes = tail
            del last[tail_start - 1:]

    result = []
    for item_no, group in zip(item_nos, groups):
        while group and not group[-1]:
            group.pop()
        spec = prefix + group + ([""] + notes if notes else [])
        result.append((item_no, spec))
    return result

def convert_h2(elem):
    """h2 → 見出し（<br>とソース上の改行の位置で<br>を入れる）"""
    elem = BeautifulSoup(str(elem), "html.parser").find("h2")
    for br in elem.find_all("br"):
        br.replace_with("\n")
    lines = [line.strip() for line in elem.get_text().splitlines()]
    text = "<br>".join(line for line in lines if line)
    return (f'{IND}<h2 class="{CSS["h2"]}">\n'
            f'{IND}    {text}\n'
            f'{IND}</h2>')

def convert_p(text):
    return (f'{IND}<p class="{CSS["p"]}">\n'
            f'{IND}    {add_br_by_period(text, IND + "    ")}\n'
            f'{IND}</p>')

def convert_img(img):
    return f'{IND}<img src="{img_src(img)}" alt="{img_alt(img)}" loading="lazy" class="{CSS["img"]}">'

def convert_img_pair(imgs):
    lines = [f'{IND}<div class="{CSS["pair_wrap"]}">']
    for img in imgs:
        lines.append(f'{IND}    <img src="{img_src(img)}" alt="{img_alt(img)}" loading="lazy" class="{CSS["pair_img"]}">')
    lines.append(f'{IND}</div>')
    return "\n".join(lines)

def convert_float(img, text, reverse=False):
    """画像＋テキスト横並び（flt-l: 画像左 / flt-r: 画像右）"""
    direction = "sm:flex-row-reverse" if reverse else "sm:flex-row"
    return (f'{IND}<div class="{CSS["float_wrap"]} {direction}">\n'
            f'{IND}    <img src="{img_src(img)}" alt="{img_alt(img)}" loading="lazy" class="{CSS["float_img"]}">\n'
            f'{IND}    <p class="{CSS["p"]}">\n'
            f'{IND}        {add_br_by_period(text, IND + "        ")}\n'
            f'{IND}    </p>\n'
            f'{IND}</div>')

def convert_box1(elem):
    """
    box1 → 囲み枠（spanの中は<br>不要）
    - h3内の画像（ロゴ・国章など）: タイトルの左に小さく表示
    - flt-l / flt-r の画像（人物写真など）: 文章の横に表示（flt-lは左、flt-rは右）
    - それ以外の画像: 枠内の下部に表示（1つの<p>に2枚以上ある場合は横並び）
    """
    h3 = elem.find("h3")
    h3_text = flat_text(h3)
    logo = h3.find("img") if h3 else None
    photo, photo_left = None, False
    big_imgs = []
    texts = []

    for child in elem.find_all("p"):
        if child.find_parent("dl"):
            continue
        classes = child.get("class", [])
        if is_image_only(child):
            imgs = child.find_all("img")
            if ("flt-l" in classes or "flt-r" in classes) and photo is None:
                photo, photo_left = imgs[0], "flt-l" in classes
                big_imgs.extend([img] for img in imgs[1:])
            else:
                big_imgs.append(imgs)
        else:
            texts.append(flat_text(child))

    if logo is not None:
        lines = [f'{IND}<div class="{CSS["box_wrap"]}">',
                 f'{IND}    <h3 class="{CSS["box_h3_logo"]}">',
                 f'{IND}        <img src="{img_src(logo)}" alt="{img_alt(logo)}" class="{CSS["box_logo"]}">',
                 f'{IND}        <span>{h3_text}</span>',
                 f'{IND}    </h3>']
    else:
        lines = [f'{IND}<div class="{CSS["box_wrap"]}">',
                 f'{IND}    <h3 class="{CSS["box_h3"]}">{h3_text}</h3>']

    dl = elem.find("dl")
    if dl:
        # 略歴などの dt/dd 形式
        rows = []
        for dt in dl.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            dd_text = "／".join(t for t in split_by_br(dd) if t) if dd else ""
            rows.append(f"{flat_text(dt)}　{dd_text}")
        lines.append(f'{IND}    <p class="{CSS["box_dl"]}">')
        lines.append(f'{IND}        ' + f"<br>\n{IND}        ".join(rows))
        lines.append(f'{IND}    </p>')

    if texts or not dl:
        photo_html = (f'{IND}        <img src="{img_src(photo)}" alt="{img_alt(photo)}" class="{CSS["box_photo"]}">'
                      if photo is not None else None)
        lines.append(f'{IND}    <p class="{CSS["box_text"]}">')
        if photo_html and photo_left:
            lines.append(photo_html)
        lines.append(f'{IND}        <span class="flex-1">{"".join(texts)}</span>')
        if photo_html and not photo_left:
            lines.append(photo_html)
        lines.append(f'{IND}    </p>')
    elif photo is not None:
        big_imgs.insert(0, [photo])

    for imgs in big_imgs:
        if len(imgs) == 1:
            lines.append(f'{IND}    <img src="{img_src(imgs[0])}" alt="{img_alt(imgs[0])}" loading="lazy" class="{CSS["box_img"]}">')
        else:
            lines.append(f'{IND}    <div class="{CSS["box_pair_wrap"]}">')
            for img in imgs:
                lines.append(f'{IND}        <img src="{img_src(img)}" alt="{img_alt(img)}" loading="lazy" class="{CSS["box_pair_img"]}">')
            lines.append(f'{IND}    </div>')
    lines.append(f'{IND}</div>')
    return "\n".join(lines)

def convert_iframe(iframe):
    """YouTube等の埋め込み"""
    src = iframe.get("src", "")
    return (f'{IND}<div class="{CSS["movie_wrap"]}">\n'
            f'{IND}    <iframe src="{src}" class="{CSS["movie"]}" frameborder="0" allowfullscreen></iframe>\n'
            f'{IND}</div>')

def can_pair(img_a, img_b):
    """2枚横並びにできるか（どちらも小さめの縦長画像で、縦横比が近い）"""
    sizes = []
    for img in (img_a, img_b):
        try:
            w, h = int(img.get("width", "")), int(img.get("height", ""))
        except ValueError:
            return False
        if w > PAIR_IMG_MAX_WIDTH or h < w:
            return False
        sizes.append(h / w)
    return max(sizes) / min(sizes) <= PAIR_RATIO_TOLERANCE

def convert_main_content(content_div, skip_elems):
    """
    商品詳細エリアを旧ページの順番どおりに変換する。
    blocks は (種類, データ) のリストで、連続画像の横並び判定のために一旦ためてから出力する。
    """
    blocks = []
    pending_float = None  # 画像だけの flt-l / flt-r（次の<p>の文章と組にする）

    def flush_float():
        nonlocal pending_float
        if pending_float:
            blocks.append(("img", pending_float[0]))
            pending_float = None

    for elem in content_div.find_all(recursive=False):
        if any(elem is s for s in skip_elems) or elem.name == "br":
            continue
        classes = elem.get("class", [])
        iframe = elem.find("iframe") if elem.name != "iframe" else elem

        if iframe is not None:
            flush_float()
            blocks.append(("raw", convert_iframe(iframe)))

        elif elem.name == "h2":
            flush_float()
            blocks.append(("raw", convert_h2(elem)))

        elif elem.name == "div" and "box1" in classes:
            flush_float()
            blocks.append(("raw", convert_box1(elem)))

        elif is_image_only(elem):
            imgs = elem.find_all("img")
            if "flt-l" in classes or "flt-r" in classes:
                flush_float()
                pending_float = (imgs[0], "flt-r" in classes)
            elif len(imgs) >= 2:
                flush_float()
                blocks.append(("pair", imgs[:2]))
                for img in imgs[2:]:
                    blocks.append(("img", img))
            else:
                flush_float()
                blocks.append(("img", imgs[0]))

        else:
            text = flat_text(elem)
            if not text:
                continue
            img = elem.find("img")
            if pending_float:
                blocks.append(("raw", convert_float(pending_float[0], text, pending_float[1])))
                pending_float = None
            elif img is not None:
                # 画像と文章が同じ要素内（align="right"等）
                reverse = img.get("align", "").lower() == "right" or "flt-r" in classes
                blocks.append(("raw", convert_float(img, text, reverse)))
            else:
                blocks.append(("raw", convert_p(text)))
    flush_float()

    # 連続する小さめの縦長画像2枚は横並びにする
    merged = []
    for kind, data in blocks:
        if kind == "img" and merged and merged[-1][0] == "img" and can_pair(merged[-1][1], data):
            merged[-1] = ("pair", [merged[-1][1], data])
        else:
            merged.append((kind, data))

    out = []
    for kind, data in merged:
        if kind == "img":
            out.append(convert_img(data))
        elif kind == "pair":
            out.append(convert_img_pair(data))
        else:
            out.append(data)
    return "\n".join(out)

def parse_old_html(html_content, product_id):
    """旧HTMLを解析して必要なデータを抽出する"""
    soup = BeautifulSoup(html_content, "html.parser")
    data = {
        "id": product_id,
        "type": "single",
        "item_nos": [],
        "top_img": None,
        "main_img": None,
        "intro_text": "",
        "list_items": [],
        "main_content_html": "",
        "spec_lines": [],
        "spec_imgs": [],
    }

    # 1. タイプ判定（form_cart1, form_cart2 … があれば複数タイプ）
    multi_forms = soup.find_all("form", attrs={"name": re.compile(r"^form_cart\d+$")})
    if multi_forms:
        data["type"] = "multi"
        for form in multi_forms:
            inp = form.find("input", attrs={"name": "item_no"})
            if inp:
                data["item_nos"].append(inp.get("value", ""))

    # 2. メイン画像（main_600x600 があればパターンA）
    data["main_img"] = soup.find("img", src=re.compile(r"main_600x600"))

    content_div = soup.find("div", id="main-content") or soup.find("section", id="main-content")
    skip_elems = []
    if content_div:
        # 3. トップ画像（_01.jpg）
        top = content_div.find("img", src=re.compile(r"_01\.jpg$"))
        if top:
            data["top_img"] = top
            skip_elems.append(next(p for p in top.parents if p.parent is content_div))

        # 4. 商品紹介文（p.intro / div.intro）
        intro = content_div.find(["p", "div"], class_="intro")
        if intro:
            data["intro_text"] = flat_text(intro)
            skip_elems.append(intro)

        # 5. 箇条書き（ul.clearfix、無ければ最初のul）
        ul = content_div.find("ul", class_="clearfix") or content_div.find("ul", recursive=False)
        if ul:
            for li in ul.find_all("li"):
                for span in li.find_all("span", class_="sq01"):
                    span.replace_with(span.get_text())
                text = flat_text(li)
                if text:
                    data["list_items"].append(text)
            skip_elems.append(ul)

        # 6. 商品詳細
        data["main_content_html"] = convert_main_content(content_div, skip_elems)

    # 7. 仕様
    data["spec_lines"], data["spec_imgs"] = parse_specs(soup)
    return data

# --- 新ページの生成 ---

def replace_once(html, old, new, label):
    if old not in html:
        print(f"  [警告] テンプレートに{label}の目印が見つかりません")
        return html
    return html.replace(old, new, 1)

def build_intro_block(data):
    """A/Bパターンのメイン画像＆箇条書きブロック"""
    main_img = data["main_img"]
    li_lines = "\n".join(f"                        <li>{item}</li>" for item in data["list_items"])
    if main_img is not None:
        return ('                <!-- A:商品メイン画像＆箇条書き(main_600x600画像がある場合) -->\n'
                '                <div class="flex flex-col md:flex-row p-3">\n'
                f'                    <img src="{img_src(main_img)}" alt="{img_alt(main_img)}" class="w-full md:w-[50%] mx-auto h-auto p-4">\n'
                '                    <ul class="text-start w-full md:w-[50%] md:p-3 leading-relaxed">\n'
                f'{li_lines}\n'
                '                    </ul>\n'
                '                </div>\n')
    return ('                <!-- B:商品メイン画像＆箇条書き(main_600x600画像がない場合) -->\n'
            '                <div class="flex flex-col md:flex-row p-3">\n'
            '                    <ul class="border-l-4 pl-2 c-border-collection-gradient text-start w-full md:p-3 leading-relaxed">\n'
            f'{li_lines}\n'
            '                    </ul>\n'
            '                </div>\n')

def spec_html(lines, indent):
    return f"<br>\n{indent}".join(lines)

def generate_new_page(data, category):
    """データをもとにテンプレートに値を埋め込み、HTMLファイルを保存する"""
    template_file = FORMAT_02 if data["type"] == "multi" else FORMAT_01
    with open(os.path.join(FORMAT_DIR, template_file), "r", encoding="utf-8") as f:
        html = f.read()

    top_img = data["top_img"]
    if top_img is None:
        print("  [警告] トップ画像(_01.jpg)が見つかりません")

    # 1. トップ画像
    if top_img is not None:
        html = replace_once(html, '<img src="*****_01.jpg" alt=""',
                            f'<img src="{img_src(top_img)}" alt="{img_alt(top_img)}"', "トップ画像")

    # 2. 商品紹介文
    intro_p = '<p class="text-start leading-relaxed font-bold">\n'
    indent = " " * 24
    html = replace_once(html, intro_p,
                        f'{intro_p}{indent}{add_br_by_period(data["intro_text"], indent)}\n', "商品紹介文")

    # 3. メイン画像＆箇条書き（A/Bのうち使う方だけ残す）
    html, n = re.subn(r" *<!-- 下記はAかBどちらかを利用 -->.*?\n\n(?= *<!-- 商品詳細 -->)",
                      lambda m: build_intro_block(data) + "\n", html, count=1, flags=re.DOTALL)
    if n == 0:
        print("  [警告] テンプレートにA/Bブロックの目印が見つかりません")

    # 4. 商品詳細（見本と指示コメントを、変換した本文に入れ替え）
    html, n = re.subn(r'(<!-- 商品詳細 -->\s*<div class="flex flex-col space-y-3 mt-6">\n).*?(\n {16}</div>\n {12}</section>)',
                      lambda m: m.group(1) + data["main_content_html"] + m.group(2), html, count=1, flags=re.DOTALL)
    if n == 0:
        print("  [警告] テンプレートに商品詳細の目印が見つかりません")

    # 5. 拡大画像（format_01のみ。main_600x600が無い場合は_01.jpgを使用）
    zoom_img = data["main_img"] if data["main_img"] is not None else top_img
    if data["type"] == "single" and zoom_img is not None:
        html = replace_once(html, '<img src="*****_main_600x600.jpg"\n                            alt="altをそのまま記述"',
                            f'<img src="{img_src(zoom_img)}"\n                            alt="{img_alt(zoom_img)}"', "拡大画像")

    # 6. 仕様（サイズ表などの画像は仕様の後ろ・全タイプ共通）
    def spec_img_lines(indent):
        return "".join(f'\n{indent}<img src="{img_src(img)}" alt="{img_alt(img)}" loading="lazy" class="{CSS["spec_img"]}">'
                       for img in data["spec_imgs"])

    size_example = r"(?:\n *<!-- 指示　仕様内にサイズ表.*?-->\n *<img [^\n]*)?"
    if data["type"] == "single":
        indent = " " * 32
        spec_block = indent + spec_html(data["spec_lines"], indent) + spec_img_lines(indent)
        html, n = re.subn(r" *<!-- 指示　仕様はここに記載 -->" + size_example, lambda m: spec_block, html, count=1)
        if n == 0:
            print("  [警告] テンプレートに仕様の目印が見つかりません")
    else:
        indent = " " * 40
        typed = split_specs_by_type(data["spec_lines"], data["item_nos"])
        if typed:
            out = []
            for i, (item_no, lines) in enumerate(typed):
                keyword = "@if" if i == 0 else "@elseif"
                out.append(f"{indent}{keyword} ($connect_goods->getItemNo() == '{item_no}')")
                out.append(indent + spec_html(lines, indent))
            out.append(f"{indent}@endif")
            spec_block = "\n".join(out)
        else:
            spec_block = indent + spec_html(data["spec_lines"], indent)
        spec_block += spec_img_lines(indent)
        html, n = re.subn(r" *<!-- 指示　仕様はここに記載（.*?@endif" + size_example, lambda m: spec_block,
                          html, count=1, flags=re.DOTALL)
        if n == 0:
            print("  [警告] テンプレートに仕様の目印が見つかりません")

    # --- ファイル保存 ---
    save_dir = os.path.join(OUTPUT_DIR, category)
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{data['id']}.html")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[完了] {category}/{data['id']}.html を生成しました (Type: {data['type']})")

# --- メイン処理 ---
def main():
    # 引数で商品番号を指定した場合はその商品のみ（例: python3 main_convert.py 51303 51151）
    targets = set(sys.argv[1:])

    files = []
    for category in CATEGORIES:
        cat_dir = os.path.join(INPUT_DIR, category)
        if not os.path.isdir(cat_dir):
            continue
        for filename in sorted(os.listdir(cat_dir)):
            if not filename.endswith(".txt") or filename.endswith("_notext.txt"):
                continue
            product_id = os.path.splitext(filename)[0]
            if targets and product_id not in targets:
                continue
            files.append((category, product_id, os.path.join(cat_dir, filename)))

    missing = targets - {pid for _, pid, _ in files}
    for pid in sorted(missing):
        print(f"[スキップ] {pid}.txt がカテゴリフォルダ内に見つかりません")

    print(f"{len(files)} 件のファイルを処理します...")

    for category, product_id, file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. 解析
        parsed_data = parse_old_html(content, product_id)

        # 2. 生成・保存
        generate_new_page(parsed_data, category)

if __name__ == "__main__":
    main()
