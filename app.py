from flask import Flask, render_template, request
from database import get_connection

app = Flask(__name__)

# ログイン画面
@app.route("/")
def login():
    return render_template("Login.html")

# 在庫一覧表示
@app.route("/inventory")
def inventory_list():
    return render_template("Inventory_List.html")

# 検索フォーム
@app.route("/search")
def search_form():
    return render_template("Inventory_Search.html")

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
def inventory_register():
    return render_template("Inventory_Register.html")

# おすすめ商品表示
@app.route("/recommend")
def recommendation():
    return render_template("Recommend.html")

if __name__ == "__main__":
    app.run(debug=True)
