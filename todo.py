from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "todo"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/PC/Desktop/Python/Flask/Flask-To Do App/ToDoApp/todo.db"  # Db oluşturuldu
db = SQLAlchemy(app)  # SQLAlchemy sayesinde db ve uygulama arasındaki ORM oluşturuldu

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Bu muhabbet Blog oluştururken user verisinde eklediğmiz id ile aynı artan, özel sayı
    title = db.Column(db.String(80))  # Max uzunluğu 80 olan string sütun
    complete = db.Column(db.Boolean)  # Boolean mantık sütunu, belirtmeyince False

@app.route("/")
def index():
    todos = ToDo.query.all()
    return render_template("index.html", todos = todos)

@app.route("/add", methods = ["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        if title == "":
            flash("Uygun bir başlık giriniz", "warning")
            return redirect(url_for("index"))
        else:
            newTodo = ToDo(title = title, complete = False)
            db.session.add(newTodo)
            db.session.commit()
            return redirect(url_for("index"))
    elif request.method == "GET":
        flash("Bu erşime yetkiniz bulunmamaktadır.", "warning")
        return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = ToDo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete = False
    else:                       
        todo.complete = True"""  # Bunu yapmak yerine aşağıdakini yaparız.
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = ToDo.query.filter_by(id = id).first()
    db.session.delete(todo)  # Anlam biraz uzun sürmüş olsa da ORM ile db veri analizi yaparken sessionlar oluşturuluyor, yukarıda query ile bir veri çektik ve şimdide db.session ile değişiklik yaptık.
    db.session.commit()
    return redirect(url_for("index")) 

if __name__ == "__main__":
    db.create_all()  # Bununla db.Model ile oluşturulmuş tüm classlar tablo olarak eklenecek
    app.run(debug=True)  # Burada debug=True terminalden programın çalışması ile alakalı olarak ekleniyor, tam detayını bilmiyorum. Hatırladım, sanırsam dosyalardaki değişikliklerin direk yansımasıydı.
