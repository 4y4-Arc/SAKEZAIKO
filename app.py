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

    conn = get_connection()

    items = conn.execute(
        "SELECT * FROM inventory"
    ).fetchall()

    conn.close()

    return render_template("Inventory_List.html",items=items)

#在庫検索
@app.route("/search")
def inventory_search():
    return render_template("Inventory_Search.html")

#在庫登録
@app.route("/register", methods=["GET", "POST"])
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
@app.route("/recommend")
def recommendation():
    return render_template("Recommend.html")

if __name__ == "__main__":
    app.run(debug=True)
