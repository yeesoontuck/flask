# run using conda environment "flasktut"

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # every time a new Task is created, return the task ID
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # task_content = request.form['content'] # name of input
        task_content = request.form.get('content', '').strip() # name of input, better method
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding the task'        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # .first()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error when deleting the task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form.get('content', '').strip()

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error when updating task'

    else:
        return render_template('update.html', task=task_to_update)
    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)  