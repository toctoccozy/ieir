import requests
from bs4 import BeautifulSoup
import re
import os
import time

# --- 設定 ---
INPUT_FILE = "urls.txt"       # URLリストのファイル名
OUTPUT_DIR = "output_files"   # 保存先のフォルダ名
SLEEP_TIME = 1.0              # 待機時間（秒）

# ここから下の部分は切り捨てる（キーワード）
STOP_KEYWORD = "下カートボタンstart"

# 保存先ディレクトリ作成
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def extract_and_save(url):
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
            save_path = os.path.join(OUTPUT_DIR, filename)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(extracted_content)
            
            print(f"[成功] {filename} (id={target_div.get('id')}) を保存しました")
        else:
            print(f"[警告] wrapper/wrappar が見つかりませんでした: {url}")

    except Exception as e:
        print(f"[エラー] {url}: {e}")

# --- メイン処理 ---
def main():
    if not os.path.exists(INPUT_FILE):
        print(f"エラー: {INPUT_FILE} が見つかりません。")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"合計 {len(urls)} 件のURLを処理します...")

    for url in urls:
        extract_and_save(url)
        time.sleep(SLEEP_TIME)

    print("すべての処理が完了しました。")

if __name__ == "__main__":
    main()
    