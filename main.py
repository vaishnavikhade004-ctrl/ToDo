from flask import Flask,  render_template, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Boolean

app= Flask(__name__, template_folder="template")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'


db=SQLAlchemy (app)


class TodoTable(db.Model):
    id =  Column(Integer,primary_key=True)
    task = Column(Text,nullable=False)
    des = Column(Text,nullable=False)
    is_done = Column(Boolean, default=False)

# Create database
with app.app_context():
    db.create_all()



@app.route('/')
def index():
    allData = TodoTable.query.all()
    return render_template('index.html',todo = allData)

@app.route('/add',methods =['POST'])
def add():
    task = request.form.get('todo')
    des = request.form.get('des')

    if task:
        data = TodoTable(task=task, des=des)
        db.session.add(data)
        db.session.commit()
        print("ok")

    return redirect(url_for('index'))


@app.route("/delete/<int:id>", methods=['POST'])
def taskDelete(id):
    row = TodoTable.query.get(id)
    if row:
        db.session.delete(row)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>')
def update(id):
    row = TodoTable.query.get(id)
    if row:
        row.is_done = not row.is_done
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)
