from tkinter import *
import sqlite3
from sqlite3 import Error
import string
import socket
from threading import Thread
import threading
import time

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

host = "127.0.0.1" 
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("Waiting for a connection...")
s.listen(1)
conn, addr = s.accept()
print("Connection from: "+str(addr))


def run():
	global currBin
	global status
	queue = []
	lock = threading.Lock()
		
	
	def receive():
		while True:
			data = conn.recv(1024).decode("utf-8")
			smc = int(data)
			with lock:
				connDB = connect("data.db")
				c = connDB.cursor()
				c.execute("""SELECT * FROM queue WHERE smc = ?""", (smc,))
				alreadyIn = c.fetchall()
				if len(alreadyIn)>0:
					conn.send(str.encode("IN QUEUE ALREADY"))
				else:
					c.execute("""SELECT * FROM packages WHERE smc = ?""",(smc,))
					result = c.fetchall()
					numPacks = len(result)
					print("numPacks %d", numPacks)
					if numPacks!=0:
						for item in result:
							newSMC = item[0]
							newBin = item[4]
							newBarcode = item[3]
							
							c.execute("""INSERT INTO queue(smc,bin,barcode) VALUES(?,?,?)""",(newSMC,newBin,newBarcode,))
							connDB.commit()
						#Get_queue()
						print("Getting queue")
						queue.clear()
						print("In lock")
						for row in c.execute("""SELECT * FROM queue"""):
							k = queueEntry(row[0], row[1], row[2])
							queue.append(k)
							print(k.get_smc())
						print("Finished")
						
						#Update list()
						print("Updating list")
						listbox.delete(0, END)
						print(len(queue))
						for item in queue:
							listbox.insert(END, item.get_smc())
						
						conn.send(str.encode("YES"))
					else:
						conn.send(str.encode("NO"))
				connDB.close()
				time.sleep(0.500)
	
	def get_queue():
		print("Getting queue")
		conn_db = connect("data.db")
		c = conn_db.cursor()
		with lock:
			queue.clear()
			print("In lock")
			for row in c.execute("""SELECT * FROM queue"""):
				k = queueEntry(row[0], row[1], row[2])
				queue.append(k)
				print(k.get_smc())
			print("Finished")
			conn_db.close()
		
	
	#get_queue()
	#result = c.fetchall()
	
	queueScreen = Tk()
	queueScreen.title("Pickup Queue")
	queueScreen.geometry("300x400")

	listbox = Listbox(queueScreen, selectmode = SINGLE, font = "Arial 18")
	listbox.pack(pady = 30)
	
	labelText = StringVar()
	labelColor = StringVar()
	labelColor.set("red")
	bin_num = Label(queueScreen, textvariable = labelText, font = "Arial 18")
		
	bin_num.pack()
	
	def displayBin(event):
		sel_index = listbox.curselection()[0]
		num = queue[sel_index].get_bin()
		print("Change bin num %d", num)
		labelText.set("Bin: " + str(num))
		bin_num.config(fg = labelColor.get())
		bin_num.pack()
	
	listbox.bind("<Double-Button-1>", displayBin)	
	
	def updateList():
		print("Updating list")
		get_queue()
		listbox.delete(0, END)
		print(len(queue))
		for item in queue:
			listbox.insert(END, item.get_smc())
		
	def done():
		get_queue()
		k = queue[listbox.curselection()[0]].get_barcode()
		conn_db = connect("data.db")
		c = conn_db.cursor()
		with lock:
			c.execute("""DELETE FROM queue WHERE barcode = ?""", (k,))
			k = queue[listbox.curselection()[0]].get_bin()
			c.execute("""SELECT status FROM bins WHERE num = ?""", (k, ))
			res = c.fetchone()
			if(res == "Full"):
				c.execute("""UPDATE bins SET status = 'Available' WHERE num = ?""", (k, ))
			conn_db.commit()
			conn_db.close()
		del queue[listbox.curselection()[0]]
		listbox.delete(listbox.curselection()[0])
	
	b = Button(queueScreen, text = "Done", command = done)
	b.pack()
	
	updateList()
	
	receiving = Thread(target=receive)
	receiving.start()	
	queueScreen.mainloop()

if __name__ == "__main__":
	#init()
	run()
