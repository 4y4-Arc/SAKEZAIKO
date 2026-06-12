import os
import json
from flask import Flask, render_template, request, redirect,jsonify
from database import get_connection
from dotenv import load_dotenv
from google import genai
from google.genai import types

app = Flask(__name__)

#ログイン画面
@app.route("/")
def login():
    return render_template("Login.html")

#在庫一覧表示
@app.route("/inventory")
def inventory_list():
    return render_template("Inventory_List.html")

#在庫検索
@app.route("/search")
def inventory_search():
    return render_template("Inventory_Search.html")

#在庫登録・更新
@app.route("/register")
def inventory_register():
    return render_template("Inventory_Register.html")

#おすすめ商品表示
@app.route("/recommend")
def recommendation():
    return render_template("Recommend.html")


SAKURA_ENV_PATH = "/home/あなたのさくらのアカウント名/.env" #さくらインターネット環境での .env ファイルのパスを指定してください

if os.path.exists(SAKURA_ENV_PATH):
    # さくらインターネット環境用の読み込み
    load_dotenv(SAKURA_ENV_PATH)
else:
    # ローカルPC環境（app.pyと同じフォルダにある .env を自動的に読み込む）
    load_dotenv()

client = genai.Client() #Geminiクライアントの初期化（APIキーは .env から自動的に読み込まれます）

@app.route('/api/recommend', methods=['POST'])
def recommend_alcohol():
    data = request.get_json()
    
    dish_input = data.get('dish', '')
    mood_input = data.get('mood', '')
    genre_input = data.get('genre', '')
    scene_input = data.get('scene', '')

    dish = dish_input if dish_input else "特定のおつまみは無し"
    mood = mood_input if mood_input else "今日一日の終わりにリラックスして飲みたい"
    genre = genre_input if genre_input else "全ジャンル何でも可"
    scene = scene_input if scene_input else "指定なし"

    prompt = f"""
    あなたは優秀なソムリエです。以下の条件にマッチする実在するお酒を【3つ】提案してください。
    【条件】
    - 合わせる料理: {dish}
    - 今日の気分: {mood}
    - お酒のジャンル: {genre}
    - シチュエーション: {scene}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "name": types.Schema(type=types.Type.STRING),
                            "taste": types.Schema(type=types.Type.STRING),
                            "reason": types.Schema(type=types.Type.STRING),
                        },
                        required=["name", "taste", "reason"],
                    ),
                ),
            ),
        )
        return response.text, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
