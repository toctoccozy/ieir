import requests
from bs4 import BeautifulSoup
import re
import os
import time

# --- 設定 ---
INPUT_FILE = "urls.txt"       # URLリストのファイル名
OUTPUT_DIR = "output_files"   # 保存先のフォルダ名
SLEEP_TIME = 1.0              # 待機時間（秒）

# カテゴリ（output_files 内のサブフォルダ名）
CATEGORIES = ["gallery", "jewelry", "mens", "treasure", "women"]

# ここから下の部分は切り捨てる（キーワード）
STOP_KEYWORD = "下カートボタンstart"

# 保存先ディレクトリ作成
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def extract_and_save(url, category):
    try:
        # 1. URLから5桁の数字を抽出（ファイル名用）
        match = re.search(r'\d{5}', url)
        if match:
            file_id = match.group(0)
            filename = f"{file_id}.txt"
        else:
            print(f"[スキップ] URLに5桁の数字なし: {url}")
            return

        # 2. データ取得
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # 文字化け対策
        response.encoding = response.apparent_encoding

        # 3. 解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # 4. wrapper または wrappar を探す
        target_div = soup.find("div", id=re.compile(r"wrapp[ea]r"))

        if target_div:
            # wrapper内部のHTMLをすべて文字列として取得
            full_html = target_div.decode_contents()

            # 5. キーワードで分割して、前半部分だけを使う
            if STOP_KEYWORD in full_html:
                # キーワードより前の部分を抽出
                extracted_content = full_html.split(STOP_KEYWORD)[0]
                # ※もし「<!-- 」のようなコメント開始タグが末尾に残るのが気になる場合は、
                #   ここでさらに微調整できますが、基本はこのままで大丈夫です。
            else:
                # キーワードがない場合はwrapperの中身全部
                extracted_content = full_html

            # 6. ファイルに保存
            save_path = os.path.join(OUTPUT_DIR, category, filename)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(extracted_content)
            
            print(f"[成功] {category}/{filename} (id={target_div.get('id')}) を保存しました")
        else:
            # wrapperがない場合は判別用に空ファイルを作成
            save_path = os.path.join(OUTPUT_DIR, category, f"{file_id}_notext.txt")
            open(save_path, "w", encoding="utf-8").close()
            print(f"[警告] wrapper/wrappar が見つかりませんでした: {url} → {category}/{file_id}_notext.txt を作成")

    except Exception as e:
        print(f"[エラー] {url}: {e}")

# --- メイン処理 ---
def main():
    if not os.path.exists(INPUT_FILE):
        print(f"エラー: {INPUT_FILE} が見つかりません。")
        return

    # [カテゴリ名] の行で、以降のURLのカテゴリを切り替える
    targets = []
    category = None
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            header = re.fullmatch(r"\[(.+)\]", line)
            if header:
                category = header.group(1).strip()
                if category not in CATEGORIES:
                    print(f"[警告] 不明なカテゴリ: [{category}]（以降のURLはスキップ）")
                    category = None
            elif category:
                targets.append((line, category))
            else:
                print(f"[スキップ] カテゴリ未指定: {line}")

    print(f"合計 {len(targets)} 件のURLを処理します...")

    for url, category in targets:
        os.makedirs(os.path.join(OUTPUT_DIR, category), exist_ok=True)
        extract_and_save(url, category)
        time.sleep(SLEEP_TIME)

    print("すべての処理が完了しました。")

if __name__ == "__main__":
    main()
    