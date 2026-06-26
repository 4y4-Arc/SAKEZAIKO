<<<<<<< HEAD
from flask import Flask, render_template, request
=======
import os
import json
from flask import Flask, render_template, request, redirect,jsonify
>>>>>>> dd9682bc1bd06fb4d230d1dcc686776413533bcf
from database import get_connection
from dotenv import load_dotenv
from google import genai
from google.genai import types

app = Flask(__name__)

<<<<<<< HEAD
# ログイン画面
@app.route("/")
=======
PASSCODE = "1234"

#ログイン画面
@app.route("/", methods=["GET", "POST"])
>>>>>>> dd9682bc1bd06fb4d230d1dcc686776413533bcf
def login():

    if request.method == "POST":

        passcode = request.form["passcode"]

        if passcode == PASSCODE:
            return redirect("/inventory")
        
        return render_template(
            "login.html",
            error="パスコードが違います"
        )
    
    return render_template("Login.html")

# 在庫一覧表示
@app.route("/inventory")
def inventory_list():

    conn = get_connection()

    items = conn.execute(
        "SELECT * FROM inventory"
    ).fetchall()

    conn.close()

    return render_template("Inventory_List.html",items=items)

# 検索フォーム
@app.route("/search")
def search_form():
    return render_template("Inventory_Search.html")

<<<<<<< HEAD
# 検索結果
@app.route("/search/result")
def inventory_search():

    keyword = request.args.get("keyword", "")

    conn = get_connection()

    inventory_list = conn.execute(
        "SELECT * FROM inventory WHERE name LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()

    conn.close()

    return render_template(
    "Search_result.html",
    inventory_list=inventory_list
)

# 在庫登録・更新
@app.route("/register")
=======
#在庫登録
@app.route("/register", methods=["GET", "POST"])
>>>>>>> dd9682bc1bd06fb4d230d1dcc686776413533bcf
def inventory_register():

    if request.method =="POST":
        name = request.form["name"]
        category = request.form["category"]
        stock = int(request.form["stock"])
        amount = int(request.form["amount"])

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO inventory
            (name, category, stock, amount)
            VALUES(?, ?, ?, ?)
            """,
            (name, category, stock, amount)
        )

        conn.commit()
        conn.close()

        return redirect("/inventory")
    
    return render_template("Inventory_Register.html")

<<<<<<< HEAD
# おすすめ商品表示
=======
#在庫更新
@app.route("/inventory/update/<int:id>", methods=["GET", "POST"])
def inventory_update(id):

    conn = get_connection()

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        stock = int(request.form["stock"])
        amount = int(request.form["amount"])

        conn.execute(
            """
            UPDATE inventory
            SET name = ?,
                category = ?,
                stock = ?,
                amount = ?
            WHERE id = ?
            """,
            (name, category, stock, amount, id)
        )

        conn.commit()
        conn.close()

        return redirect("/inventory")

    item = conn.execute(
        """
        SELECT * FROM inventory
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "Inventory_Update.html",
        item=item
    )

#在庫削除
@app.route("/inventory/delete/<int:id>", methods=["POST"])
def inventory_delete(id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM inventory
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/inventory")
 
#おすすめ商品表示
>>>>>>> dd9682bc1bd06fb4d230d1dcc686776413533bcf
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
