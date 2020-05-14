from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem leading that task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


@app.route("/db_trial", methods=['GET'])
def db_trial():
    my_db = mysql.connector.connect(
        host='Fleiv.mysql.pythonanywhere-services.com',
        user='pippo',
        passwd='Apprendere19',
    )
    db_cursor = my_db.cursor(buffered=True)
    db_cursor.execute("CREATE DATABASE PrimaProva")
    query1 = "CREATE TABLE MyGuests (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,firstname VARCHAR(30) NOT NULL," \
            "lastname VARCHAR(30) NOT NULL,email VARCHAR(50),reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP " \
            "ON UPDATE CURRENT_TIMESTAMP)";
    db_cursor.execute(query1)
    query2 = "INSERT INTO MyGuests (firstname, lastname, email)" \
          "VALUES('John', 'Doe', 'john@example.com')";
    db_cursor.execute(query2)
    my_db.commit()
    return render_template('create_db.html')


if __name__ == "__main__":
    app.run(debug=True)

