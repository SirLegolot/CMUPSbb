from tkinter import *
import sqlite3
from sqlite3 import Error
import string

class queueEntry:
	smc = 0
	bin = 0
	barcode = 0
	def __init__(self, smc, bin, barcode):
		self.smc = smc
		self.bin = bin
		self.barcode = barcode
	def get_smc(self):
		return self.smc
	def get_bin(self):
		return self.bin
	def get_barcode(self):
		return self.barcode

def connect(database):
	conn = sqlite3.connect(database)
	return conn

def run():
	global currBin
	global status
		
	conn = connect("data.db")
	c = conn.cursor()
	
	queue = get_queue()
	
	def get_queue():
		queue = []
		for row in c.execute("""SELECT * FROM queue"""):
			k = queueEntry(row[0], row[1], row[2])
			queue.append(k)
			print(k.get_smc())
		return queue
	
	#result = c.fetchall()
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
			listbox.insert(END, item.get_smc())
	def done():
		k = queue[listbox.curselection()[0]].get_barcode()
		c.execute("""DELETE FROM queue WHERE barcode = ?""", (k,))
		conn.commit()
		del queue[listbox.curselection()[0]]
		listbox.delete(listbox.curselection()[0])
	
	b = Button(queueScreen, text = "Done", command = done, anchor = E)
	b.pack()
	
	updateList()
		
	queueScreen.mainloop()

if __name__ == "__main__":
	#init()
	run()
