from app import app
from flask import Flask,url_for,render_template,request,flash,redirect,session,g
from functools import wraps
import sqlite3

def login_required(f):
	@wraps(f)
	def func(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Login first')
		 	return redirect(url_for('login'))
	return func

# @ signifies a decorator : Used to wrap a function

@app.route('/',)
@login_required
def welcome():
	return render_template("welcome.html")

@app.route('/form',methods=['GET','POST'])
@login_required
def form():
	if request.method=="POST":
		nm=request.form['name']
		em=request.form['email']
		cont=request.form['contact']
		params=(nm,em,cont)
		with sqlite3.connect("practice.db") as connection:
			c=connection.cursor()

			c.execute('INSERT INTO practice VALUES(NULL,?,?,?)',params)
			c.close()
			del c
		flash("DATA SAVED IN DATABASE")
		return redirect(url_for('form'))
	return render_template("form.html")

@app.route('/login',methods=["GET","POST"])
def login():
	error = None
	if request.method=='POST':
		if request.form['username']!='hj' or request.form['pass']!='hj':
			error='Invalid Credentials'

		else:
			session['logged_in']=True
			flash("You logged in")
			return redirect(url_for('form'))

	if 'logged_in' in session:
		flash('Already Logged In')
		return redirect(url_for('form'))
	return render_template("login.html",error=error)

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You logged out')
	return redirect(url_for('login'))

@app.route('/view',methods=['GET','POST'])
@login_required
def view():
	g=connect_db()
	c=g.cursor();
	c.execute("SELECT * FROM practice")
	post=[]
	for r in c.fetchall():
		post.append(dict(name=r[1],email=r[2],contact=r[3],id=r[0]))
	return render_template('view.html',post=post)

@app.route('/viewspecific/<id>',methods=['GET','POST'])
@login_required
def viewspecific(id):
	g.db=connect_db()
	quer=g.db.execute("SELECT name,contact,email FROM practice WHERE id=?",(id,))
	post=[]
	for r in quer.fetchall():
		post.append(dict(name=r[0],contact=r[1],email=r[2]))
	return render_template("viewspecific.html",post=post)

@app.route('/deletedata/<id>')
@login_required
def deletedata(id):
	with sqlite3.connect("practice.db") as connection:
			c=connection.cursor()
			quer=c.execute('DELETE FROM practice WHERE id=?',(id,))
	return redirect(url_for('view'))
@app.route('/see')
def see():
	with sqlite3.connect("practice.db") as connection:
			c=connection.cursor()
			quer=c.execute("SELECT * FROM practice where name=?",('nm[]',))
			data = []
			for item in c.fetchall():
				data.append(item)

	post=[]
	for r in quer.fetchall():
		nm.append(dict(name=r[0]))
	return render_template("see.html",post='nm')




def connect_db():
	return sqlite3.connect(app.database)
