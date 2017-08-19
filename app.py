from flask import Flask
import sqlite3

app=Flask(__name__)
app.secret_key="private"
app.database="practice.db"

from route import *

if __name__=="__main__":
	app.run(debug=True)