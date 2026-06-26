from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)

PASSCODE = "1234"

#ログイン画面
@app.route("/", methods=["GET", "POST"])
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

if __name__ == "__main__":
    app.run(debug=True)
