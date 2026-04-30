import os
import json
import urllib.request
import urllib.error
import time

# GitHubの秘密の金庫からGeminiの鍵を取り出す
API_KEY = os.environ.get("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# AIへの最強のプロンプト（賢者を心理学者にアップデート済み✨）
prompt = """
あなたは歴史上の偉人や、世界中を旅してきた一流の心理学者です。
ユーザーの心を温かく照らし、今日を生きる活力を与えるような「癒やしと励ましの名言」を【96個】作成してください。
1つの名言は短く（30文字〜60文字程度）してください。
出力は絶対に以下のJSONフォーマットのみとし、余計な文章は一切含めないでください。
[
  {"author": "偉人の名前や、心理学者のペンネーム", "quote": "名言の内容"},
  ...
]
"""

data = {
    "contents": [{"parts": [{"text": prompt}]}]
}
req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

# 🌟 激熱ハッキング：最大3回まで諦めずにリトライする！
max_retries = 3
for attempt in range(max_retries):
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # AIがたまに付けるマークダウンのゴミをお掃除
        text = text.replace("```json", "").replace("```", "").strip()

        # quotes.json というファイルに上書き保存！
        with open("quotes.json", "w", encoding="utf-8") as f:
            f.write(text)
        print("✨ 96個の名言の錬成に大成功しました！")
        break # 成功したらループを抜け出す！
        
    except urllib.error.HTTPError as e:
        print(f"⚠️ Googleのサーバーが混雑しています (試行 {attempt + 1}/{max_retries}): {e.code} {e.reason}")
        if attempt < max_retries - 1:
            print("⏳ 5秒待ってから再アタックします...")
            time.sleep(5)
        else:
            print("❌ リトライ上限に達しました。今日は諦めます...")
            exit(1) # GitHubくんに「失敗したよ！」と正しく伝える
            
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")
        exit(1) # GitHubくんに「失敗したよ！」と正しく伝える
