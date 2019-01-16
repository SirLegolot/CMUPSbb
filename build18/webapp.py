from flask import Flask, render_template, request
import os
import sqlite3


app = Flask(__name__)

fields = ["andrewID: ", "SMC: ", "Last name: "]
filename = "testing shit.txt"

def connect(database):
	conn = sqlite3.connect(database)
	return conn

@app.route('/')
def root():
    return render_template('queue.html', data = fields)
 
@app.route('/submitted')
def poll():
    andrew = request.args.get("andrewID: ")
    smc = request.args.get("SMC: ")
    lastname = request.args.get("Last name: ")

    conn = connect("data.db")
    c = conn.cursor()
    c.execute("""SELECT bin FROM packages WHERE andrew = ? WHERE smc = ? WHERE lastname = ?""",(andrew,smc,lastname,))
    result = c.fetchone()
    if len(result)>0:
    	pass


    out = open(filename, 'a')
    out.write(smc+" "+firstname+" "+lastname+"\n")
    out.close()


    return "Thanks! You are now in the queue."



if __name__ == "__main__":
    app.run(debug=True)
