import os
import json
import urllib.request

# GitHubの秘密の金庫からGeminiの鍵を取り出す
API_KEY = os.environ.get("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# AIへの最強のプロンプト
prompt = """
あなたは歴史上の偉人や、世界を旅する賢者です。
ユーザーの心を温かく照らし、今日を生きる活力を与えるような「癒やしと励ましの名言」を【96個】作成してください。
1つの名言は短く（30文字〜60文字程度）してください。
出力は絶対に以下のJSONフォーマットのみとし、余計な文章は一切含めないでください。
[
  {"author": "偉人や賢者の名前", "quote": "名言の内容"},
  ...
]
"""

data = {
    "contents": [{"parts": [{"text": prompt}]}]
}

# AIにお願いを送信！
req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    text = result['candidates'][0]['content']['parts'][0]['text']
    
    # AIがたまに付けるマークダウンのゴミをお掃除
    text = text.replace("```json", "").replace("```", "").strip()

    # quotes.json というファイルに上書き保存！
    with open("quotes.json", "w", encoding="utf-8") as f:
        f.write(text)
    print("✨ 96個の名言の錬成に成功しました！")
except Exception as e:
    print(f"❌ エラーが発生しました: {e}")
