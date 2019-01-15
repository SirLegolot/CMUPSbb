from flask import Flask, render_template, request
import os


app = Flask(__name__)

fields = ["SMC: ", "First name: ", "Last name: "]
filename = "testing shit.txt"

@app.route('/')
def root():
    return render_template('queue.html', data = fields)
 
@app.route('/submitted')
def poll():
    smc = request.args.get("SMC: ")
    firstname = request.args.get("First name: ")
    lastname = request.args.get("Last name: ")

    out = open(filename, 'a')
    out.write(smc+" "+firstname+" "+lastname+"\n")
    out.close()

    return "Thanks! You are now in the queue."


if __name__ == "__main__":
    app.run(debug=True)