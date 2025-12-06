import os
import re
import shutil
from bs4 import BeautifulSoup, Comment

# --- 設定 ---
# パスの設定（実行場所からの相対パス）
INPUT_DIR = "output_files"
FORMAT_DIR = "../format"
OUTPUT_DIR = "../products"

FORMAT_01 = "format_01.html"
FORMAT_02 = "format_02.html"

# ディレクトリ作成
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- ユーティリティ関数 ---

def clean_text_with_br(text):
    """
    テキストから既存の改行や<br>を削除し、句点「。」の後に<br>を入れる。
    """
    if not text:
        return ""
    # 改行と既存<br>を除去
    text = text.replace('\n', '').replace('\r', '')
    text = re.sub(r'<br\s*/?>', '', text, flags=re.IGNORECASE)
    # 句点のあとに<br>を入れる
    text = text.replace("。", "。<br>")
    return text

def extract_specs_from_dd(dd_element, is_multi=False):
    """
    <dd>タグから仕様テキストを抽出する。
    複数タイプ(is_multi=True)の場合は、【】で区切られているか解析して辞書で返す。
    """
    full_text = dd_element.get_text("\n", strip=True)
    
    if not is_multi:
        return {"common": clean_text_with_br(full_text)}

    # 複数タイプの場合、【見出し】で分割を試みる
    # 例: 【掛け軸】... 【飾り額】...
    pattern = r'【(.*?)】(.*?)(?=【|$)'
    matches = re.findall(pattern, full_text, re.DOTALL)
    
    if matches:
        specs = {}
        # matches は [('掛け軸', '内容...'), ('飾り額', '内容...')] のリスト
        for i, (title, content) in enumerate(matches):
            specs[i] = clean_text_with_br(f"【{title}】{content}")
        return specs
    else:
        # 分割できない場合は共通として返す
        return {"common": clean_text_with_br(full_text)}

def parse_old_html(html_content, product_id):
    """
    旧HTMLを解析して必要なデータを抽出する
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {
        "id": product_id,
        "type": "single", # default
        "top_image": f"{product_id}_01.jpg",
        "intro_text": "",
        "intro_list_type": "B", # default (B: border list)
        "intro_list_items": [],
        "main_content_html": "",
        "specs": {},
        "main_img_exists": False
    }

    # 1. タイプ判定 (form_cart1 があるかどうか)
    if soup.find("form", attrs={"name": re.compile(r"form_cart\d+")}):
        data["type"] = "multi"
    
    # 2. イントロテキスト (p.intro)
    intro_p = soup.find("p", class_="intro")
    if intro_p:
        # html=Trueで取得しないとタグが消えるが、今回はtextのみでbr制御するためget_text
        data["intro_text"] = clean_text_with_br(intro_p.get_text())

    # 3. イントロリスト (ul.clearfix) と 画像判定
    # main_600x600 画像があるかチェック
    if soup.find("img", src=re.compile(r"main_600x600")):
        data["main_img_exists"] = True
        data["intro_list_type"] = "A" # 画像ありレイアウト
    
    ul_list = soup.find("ul", class_="clearfix")
    if ul_list:
        for li in ul_list.find_all("li"):
            # span class="sq01" を削除して ■ に置換
            for span in li.find_all("span", class_="sq01"):
                span.decompose()
            text = li.get_text(strip=True)
            data["intro_list_items"].append(f"■{text}")

    # 4. 商品詳細 (main-content直下の要素などを走査)
    # ここは構造がバラバラなので、特定のコンテナの中を見る
    # 旧HTMLでは <div class="cd-..." id="main-content"> の中にあると想定
    content_div = soup.find("div", id="main-content")
    if not content_div:
        # idがない場合は section id="main-content" の中を探す
        content_div = soup.find("section", id="main-content")

    if content_div:
        generated_html = []
        
        # 除外するクラスやタグ
        for exclude in content_div.find_all(["p", "ul"], class_=["intro", "clearfix"]):
            # イントロやリストは別途抽出済みなのでスキップしたいが、
            # contentsループで回すのでここでは無視リストを作る等の対応が必要。
            # 今回は単純にループ中に判定する。
            pass

        for elem in content_div.contents:
            if elem.name is None:
                continue
            
            # クラス判定
            classes = elem.get("class", [])
            
            # 既に処理済みのイントロ等はスキップ
            if "intro" in classes or "clearfix" in classes or "center-img" in classes:
                # center-imgでもトップ画像(product_id_01.jpg)ならスキップ
                if elem.find("img", src=re.compile(f"{product_id}_01.jpg")):
                    continue
                # Aパターンのメイン画像もスキップ
                if elem.find("img", src=re.compile(r"main_600x600")):
                    continue
            
            # --- 各要素の変換 ---
            
            # <h2> -> フォーマットのh2スタイルへ
            if elem.name == "h2":
                text = elem.get_text(strip=True)
                h2_html = f'<h2 class="text-white rounded-md font-bold text-lg c-bg-collection-gradient text-center sm:p-3 py-2 mx-1">{text}</h2>'
                generated_html.append(h2_html)
            
            # <p class="flt-l" / "flt-r"> -> Flex layout
            elif elem.name == "p" and ("flt-l" in classes or "flt-r" in classes):
                # 画像とテキストを含む可能性がある
                img = elem.find("img")
                text = elem.get_text(strip=True)
                if img:
                    src = img.get("src")
                    alt = img.get("alt", "")
                    # brを入れない
                    html = f'''
                    <div class="flex flex-col sm:flex-row">
                        <img src="{src}" alt="{alt}" loading="lazy" class="mx-auto max-w-[10rem] p-3 sm:m-3 object-contain">
                        <p class="text-start px-1 sm:p-3 leading-relaxed">{text}</p>
                    </div>'''
                    generated_html.append(html)
            
            # <div class="box1"> -> Box layout
            elif elem.name == "div" and "box1" in classes:
                # box1の中身（h3, dl, pなど）を解析
                h3 = elem.find("h3")
                h3_text = h3.get_text(strip=True) if h3 else ""
                
                # 画像があるか
                img = elem.find("img")
                img_html = ""
                if img:
                    img_html = f'<img src="{img["src"]}" alt="{img.get("alt","")}" class="w-12 object-contain sm:mt-0 sm:ml-2 mx-auto sm:mx-0">'
                
                # テキスト（ddやp）
                body_text = ""
                # dlがある場合
                dl = elem.find("dl")
                if dl:
                     body_text = dl.get_text("<br>", strip=True) # dlは改行維持したいので簡易的に
                else:
                    # pなどから取得 (ただしh3以外)
                    for child in elem.find_all(["p", "div"]):
                        if child.find("img"): continue # 画像だけのpは飛ばす
                        body_text += child.get_text(strip=True)
                
                html = f'''
                <div class="p-3 m-1 border c-border-collection-gradient border-1 rounded-md">
                    <h3 class="font-bold p-2">{h3_text}</h3>
                    <p class="leading-relaxed flex p-2 flex-col sm:flex-row">
                        <span class="flex-1">{body_text}</span>
                        {img_html}
                    </p>
                </div>'''
                generated_html.append(html)
            
            # <p> (通常テキスト)
            elif elem.name == "p":
                # 画像のみを含むp
                if elem.find("img") and not elem.get_text(strip=True):
                    img = elem.find("img")
                    # サイズ表などの画像処理（小さめ表示の指示あり）
                    # クラス調整: max-w-2xl mx-auto h-auto p-4
                    html = f'<img src="{img["src"]}" alt="{img.get("alt","")}" loading="lazy" class="w-full max-w-2xl mx-auto h-auto p-4">'
                    generated_html.append(html)
                else:
                    # テキストp (句点改行あり)
                    text = clean_text_with_br(elem.get_text())
                    if text:
                        html = f'<p class="text-start px-1 sm:p-3 leading-relaxed">{text}</p>'
                        generated_html.append(html)
        
        data["main_content_html"] = "\n".join(generated_html)

    # 5. 仕様 (dd)
    # 仕様は通常 <div id="item-product"> の中の dl dt dd にある
    spec_dd = soup.find("dd")
    if spec_dd:
        # タイプに応じて抽出
        data["specs"] = extract_specs_from_dd(spec_dd, is_multi=(data["type"] == "multi"))

    return data

def generate_new_page(data):
    """
    データをもとにテンプレートに値を埋め込み、HTMLファイルを保存する
    """
    template_file = FORMAT_02 if data["type"] == "multi" else FORMAT_01
    template_path = os.path.join(FORMAT_DIR, template_file)
    
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # --- 共通箇所の置換 ---
    
    # 1. トップ画像
    # *****_01.jpg を置換 (テンプレート内のプレースホルダーを探す)
    html = html.replace('src="*****_01.jpg"', f'src="{data["top_image"]}"')

    # 2. 商品紹介文 (text-start sm:text-center... の中身)
    # テンプレート構造に依存するため、BeautifulSoupで置換した方が安全だが、
    # Blade構文があるため文字列置換でアプローチする。
    # 「<!-- 商品紹介文 -->」のようなコメントマーカーがないため、周辺のHTML特徴で置換
    target_intro_tag = '<p class="text-start sm:text-center leading-relaxed font-bold">'
    html = html.replace(target_intro_tag, f'{target_intro_tag}\n{data["intro_text"]}')

    # 3. イントロリスト (A/B判定)
    # テンプレートにはAとB両方書いてある前提で、不要な方を削除、必要な方にデータ注入
    list_html = "\n".join([f"<li>{item}</li>" for item in data["intro_list_items"]])
    
    # Aパターンのブロック
    block_a_start = '<!-- A:商品メイン画像＆箇条書き(main_600x600画像がある場合) -->'
    # Bパターンのブロック
    block_b_start = '<!-- B:商品メイン画像＆箇条書き(main_600x600画像がない場合) -->'
    
    # 正規表現でブロックを特定して置換するのは複雑なので、
    # テンプレートにある「<!-- 指示　ul classのclearfix部分は下記を利用 -->」を探す
    
    if data["intro_list_type"] == "A":
        # Bブロックを削除 (簡易的に文字列置換で空にするか、コメントアウト)
        # ここでは「Bのブロック全体」を消す処理が必要。
        # テンプレートの構造を知っている前提で、文字列置換を行う
        
        # main_600x600画像のパス設定
        html = html.replace('src="*****_main_600x600.jpg"', f'src="{data["id"]}_main_600x600.jpg"')
        
        # リストの中身を注入
        html = html.replace('<!-- 指示　ul classのclearfix部分は下記を利用 -->\n                        <ul class="text-start w-full md:w-[50%] md:p-3 leading-relaxed">\n                            <li></li>',
                            f'<ul class="text-start w-full md:w-[50%] md:p-3 leading-relaxed">\n{list_html}')
        
        # Bパターンを消す (簡易実装: Bの開始コメントから次のdiv閉じまで消す等)
        # 今回は「B:〜」から「<!-- 商品詳細 -->」の前までを消す
        pattern_b_removal = re.compile(r'<!-- B:商品メイン画像.*?<!-- 商品詳細 -->', re.DOTALL)
        html = pattern_b_removal.sub('<!-- 商品詳細 -->', html)
        
    else:
        # Aブロックを消す
        pattern_a_removal = re.compile(r'<!-- A:商品メイン画像.*?<!-- B:商品メイン画像', re.DOTALL)
        html = pattern_a_removal.sub('<!-- B:商品メイン画像', html)
        
        # リストの中身を注入 (Bパターン用)
        html = html.replace('<!-- 指示　ul classのclearfix部分は下記を利用 -->\n                        <ul class="border-l-4 pl-2 c-border-collection-gradient text-start w-full md:p-3 leading-relaxed">\n                            <li></li>',
                            f'<ul class="border-l-4 pl-2 c-border-collection-gradient text-start w-full md:p-3 leading-relaxed">\n{list_html}')

    # 4. 商品詳細
    # テンプレートの 「<!-- 商品詳細 -->」 以下の div container の中身を
    # 生成した main_content_html にごっそり入れ替えるのが一番確実。
    # ただしテンプレートには「<!-- 指示... -->」があるので、その親divの中身を置き換える。
    
    # 詳細エリアの開始地点
    detail_start_marker = '<!-- 商品詳細 -->'
    if detail_start_marker in html:
        # 詳細エリアのdiv開始タグを探す
        start_idx = html.find(detail_start_marker)
        # <div class="flex flex-col space-y-3 mt-6"> を探す
        div_start = html.find('<div class="flex flex-col space-y-3 mt-6">', start_idx)
        if div_start != -1:
            # このdivの閉じタグまでを探すのは正規表現では難しいが、
            # 次のセクション <!-- 価格・購入エリア --> があるのでそこまでを置換範囲とする
            section_end = html.find('<!-- 価格・購入エリア -->')
            
            before = html[:div_start]
            after = html[section_end:]
            
            new_detail_block = f'<div class="flex flex-col space-y-3 mt-6">\n{data["main_content_html"]}\n</div>\n</section>\n\n            '
            
            html = before + new_detail_block + after

    # 5. 仕様 (format_01と02で処理分岐)
    
    if data["type"] == "single":
        # format_01: 単純置換
        spec_marker = '<!-- 指示　仕様はここに記載 -->'
        if spec_marker in html:
            spec_text = data["specs"].get("common", "")
            html = html.replace(spec_marker, spec_text)
            
    else:
        # format_02: 複数タイプ
        # Bladeのループ @foreach ... @endforeach を展開する
        # ループの中身を正規表現で抽出
        loop_pattern = re.compile(r'@foreach \(\$goods->getConnectGoods\(\).*?@endforeach', re.DOTALL)
        loop_match = loop_pattern.search(html)
        
        if loop_match:
            loop_content = loop_match.group(0)
            # @foreach と @endforeach を除去して、中身のHTMLテンプレートを取り出す
            # 先頭行と末尾行を削除
            lines = loop_content.split('\n')
            template_inner = "\n".join(lines[1:-1]) 
            
            # 生成するHTML
            expanded_html = ""
            
            # 抽出した仕様の数だけループ (通常2回: AとB)
            # data["specs"] は {0: "SpecA", 1: "SpecB"} または {"common": "CommonSpec"}
            
            # 仕様が分割されているか確認
            specs_list = []
            if "common" in data["specs"]:
                # 分割されなかった場合は同じ仕様を2回繰り返す(とりあえず2回と仮定)
                # あるいはソースコードのフォーム数を見るべきだが、簡易的に2つ生成する
                specs_list = [data["specs"]["common"], data["specs"]["common"]]
            else:
                # 辞書のキー順にソートしてリスト化
                specs_list = [data["specs"][k] for k in sorted(data["specs"].keys())]
            
            for i, spec_text in enumerate(specs_list):
                # テンプレートコピー
                current_block = template_inner
                
                # 仕様を注入
                # format_02には「<!-- 指示　仕様はここに記載 -->」がないため、
                # <p class="leading-snug text-sm"> の中身として注入する
                # 注意: format_02.html の内容を見ると <p ...>\n\n </p> となっている
                target_p = '<p class="leading-snug text-sm">'
                current_block = current_block.replace(target_p, f'{target_p}\n{spec_text}')
                
                # 商品ごとの処理 (必要ならここで他の置換も可能)
                # 例: フォーム名 form_cart1, form_cart2 などに対応させる必要があれば
                # ただしBladeテンプレート変数が残っているので、
                # Bladeが正しく動くなら変える必要はない。
                # 今回は「仕様Aを商品Aに」という指示なので、
                # このループ展開により、1つ目のブロックには仕様Aが、2つ目には仕様Bが固定で入るHTMLになる。
                
                expanded_html += current_block + "\n" + '<div class="border-t border-gray-200 mx-4 mb-4"></div>' + "\n"
            
            # 元のループ部分を、展開したHTMLに置換
            html = html.replace(loop_content, expanded_html)

    # --- ファイル保存 ---
    save_filename = f"{data['id']}.html"
    save_path = os.path.join(OUTPUT_DIR, save_filename)
    
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"[完了] {save_filename} を生成しました (Type: {data['type']})")

# --- メイン処理 ---
def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
    print(f"{len(files)} 件のファイルを処理します...")

    for filename in files:
        product_id = os.path.splitext(filename)[0]
        file_path = os.path.join(INPUT_DIR, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. 解析
        parsed_data = parse_old_html(content, product_id)
        
        # 2. 生成・保存
        generate_new_page(parsed_data)

if __name__ == "__main__":
    main()
    