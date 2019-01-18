from tkinter import *
import sqlite3
from sqlite3 import Error
import string

def connect(database):
	conn = sqlite3.connect(database)
	return conn


def run():
	global currBin
	global status
	
	queue = [1234, 1256, 9023]
	
	conn = connect("data.db")
	c = conn.cursor()
	c.execute("""SELECT * FROM packages WHERE smc='Available'""")
	
	result = c.fetchall()
	
	
	
	queueScreen = Tk()
	queueScreen.title("Pickup Queue")
	queueScreen.geometry("700x500")

	listbox = Listbox(queueScreen, selectmode = SINGLE)
	listbox.pack()
	
	labelText = StringVar()
	labelColor = StringVar()
	labelColor.set("red")
	bin_num = Label(queueScreen, textvariable = labelText)
		
	bin_num.pack()
	
	def displayBin(event):
		sel_index = listbox.curselection()[0]
		num = 1
		labelText.set("Bin: " + str(num))
		bin_num.config(fg = labelColor.get())
		bin_num.pack()
	
	listbox.bind("<Double-Button-1>", displayBin)	
	
	def updateList():
		listbox.delete(0, END)
		for item in queue:
			listbox.insert(END, item)
	def done():
		del queue[listbox.curselection()[0]]
		listbox.delete(listbox.curselection()[0])
	
	b = Button(queueScreen, text = "Done", command = done, anchor = E)
	b.pack()
	
	updateList()
		
	queueScreen.mainloop()

if __name__ == "__main__":
	#init()
	run()
