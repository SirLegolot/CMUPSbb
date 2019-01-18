from flask import Flask, render_template, request
import os
import sqlite3


app = Flask(__name__)

fields = ["andrewID: ", "SMC: ", "Last name: "]
filename = "queue.txt"

def connect(database):
	conn = sqlite3.connect(database)
	return conn

@app.route('/')
def root():
    return render_template('queue.html', data = fields)
 
@app.route('/submitted')
def poll():
	andrew = request.args.get("andrewID: ").lower()
	smc = request.args.get("SMC: ")
	lastname = request.args.get("Last name: ").lower()
	conn = connect("data.db")
	c = conn.cursor()
	c.execute("""SELECT bin FROM packages WHERE andrew = ? AND smc = ? AND lastname = ?""",(andrew,smc,lastname,))
	result = c.fetchall()
	if len(result)!=0:
		out = open(filename, 'a')
		out.write(smc+" "+andrew+" "+lastname+"\n")
		out.close()
		return "Thanks! You are now in the queue. You have "+str(len(result))+"packages."
	else:
		return "You don't have any packages in the mailroom."



if __name__ == "__main__":
    app.run(debug=True)
