import sqlite3, os.path
from flask import Flask, render_template, g, url_for, redirect, request
from flask_bootstrap import Bootstrap
# ------------------------configuration---------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "todo.db")

app = Flask(__name__)
Bootstrap(app)


def connect_db():
    return sqlite3.connect(db_path)


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


# ------------------------the application itself---------------------------------------

@app.route('/')
def todo_list():
    cursor = g.db.execute('select * from todo')
    todos = [dict(id=row[0], task=row[1], status=row[2]) for row in cursor.fetchall()]
    return render_template('list.html', todos=todos)


@app.route('/delete/<int:id>')
def delete_todo(id):
    g.db.execute('delete from todo where id=' + str(id))
    g.db.commit()
    return redirect(url_for('todo_list'))


@app.route('/create', methods=['GET', 'POST'])
def create_todo():
    if request.method == 'POST':

        task = request.form['task']

        g.db.execute("INSERT INTO todo (task,status) VALUES ( ? , ? )", (task, 1))
        g.db.commit()

        return redirect(url_for('todo_list'))
    else:

        return render_template('create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    cur = g.db.execute('select * from todo WHERE id = ? ', str(id))
    task = cur.fetchall()[0][1]
    print(task)

    if request.method == 'POST':

        task = request.form['task']
        g.db.execute("UPDATE todo SET task=? WHERE id=?", (task, id))
        g.db.commit()

        return redirect(url_for('todo_list'))
    else:

        return render_template('edit.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
