from flask import Flask,render_template,request,session,url_for,redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import os
from forms import TodoForm

app=Flask("__name__")
app.config['SECRET_KEY']="mykey"

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text)
    status=db.Column(db.Boolean)

    def __init__(self,title,status):
        self.title=title
        self.status=status

@app.route('/',methods=['GET','POST'])
def index():
	form=TodoForm()
	if form.validate_on_submit():
		title=form.title.data
		status=False
		new_todo=Todo(title,status)
		db.session.add(new_todo)
		db.session.commit()
		return redirect(url_for('index'))

	todo_list=Todo.query.order_by(Todo.id.desc())
	
	return render_template("home.html",todo_list=todo_list,form=form)
@app.route('/update/<int:todo_id>')
def update(todo_id):
	todo=Todo.query.filter_by(id=todo_id).first()
	todo.status= not todo.status
	db.session.commit()

	return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
	todo=Todo.query.get(todo_id)
	db.session.delete(todo)
	db.session.commit()

	return redirect(url_for('index'))
	
if __name__ == '__main__':
		app.run(debug=True)
