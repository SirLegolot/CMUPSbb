from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread

host = "127.0.0.1"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def run():
	qEntry = Tk()
	qEntry.title("Queue")
	qEntry.geometry("300x200")

	def addQueue():
		try:
			smc = int(smcTxt.get())
			smcInput.delete(0,END)
		except:
			error = Toplevel()
			error.withdraw()
			messagebox.showerror("Error", "Please enter a valid SMC number!")
		s.send(str.encode(str(smc)))

	def receive():
		while True:
			global s
			data = s.recv(1024).decode("utf-8")
			if data == "NO":
				error = Toplevel()
				error.withdraw()
				messagebox.showerror("Error", "You have no packages in the system!")
			if data == "IN QUEUE ALREADY":
				error = Toplevel()
				error.withdraw()
				messagebox.showerror("Error", "You are already in the queue!")
			else:
				error = Toplevel()
				error.withdraw()
				messagebox.showinfo("Success", "You have been added to the queue")

	smcTxt = StringVar()
	smcInput = Entry(qEntry, textvariable = smcTxt, font = "Arial 18 bold", width = 4)
	entryLabel = Label(qEntry, text = "Input your SMC #:", font = "Arial 18")
	entryButton = Button(qEntry, text = "Add to Queue", command=addQueue)
	entryLabel.pack(pady=20)
	smcInput.pack()
	entryButton.pack(pady=20)

	receiving = Thread(target=receive)
	receiving.start()
	qEntry.mainloop()


run()