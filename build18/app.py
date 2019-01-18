from tkinter import *
import sqlite3
from sqlite3 import Error
import string

def connect(database):
	conn = sqlite3.connect(database)
	return conn

def createTable(conn, stringEXE):
	c = conn.cursor()
	c.execute(stringEXE)

def setupBins(conn, stringEXE, num):
	c = conn.cursor()
	for i in range(1,num+1):
		c.execute(stringEXE,(i,))
	conn.commit()

def init():
	database = "data.db"
	create_Bin_Table = """CREATE TABLE IF NOT EXISTS bins(
		                            num integer PRIMARY KEY,
		                            status text NOT NULL
            						);"""
	create_Packages_Table = """CREATE TABLE IF NOT EXISTS packages(
										smc integer NOT NULL,
										lastname text NOT NULL,
										firstname text NOT NULL,
										barcode integer NOT NULL,
										bin integer NOT NULL,
										andrew text NOT NULL
										);"""
	create_People_Table = """CREATE TABLE IF NOT EXISTS people(
										smc integer NOT NULL,
										lastname text NOT NULL,
										firstname text NOT NULL,
										andrew text NOT NULL
										);"""
	create_Queue_Table = """CREATE TABLE IF NOT EXISTS queue(
										smc integer NOT NULL,
										bin integer NOT NULL,
										barcode integer NOT NULL,
										);"""
	setup_Bins = """INSERT OR IGNORE INTO bins(num, status) VALUES(?, "Available");"""
	conn = connect("data.db")
	if conn is not None:
		createTable(conn, create_Bin_Table)
		createTable(conn, create_Packages_Table)
		createTable(conn, create_People_Table)
		createTable(conn, create_Queue_Table)
		setupBins(conn, setup_Bins, 10)
	else:
		print("Error! cannot create the database connection.")
	conn.close()


def scanFunction():
	string = """r = o no
an!“ Manned

a:>!A.las lelsod (“NO

amou

US POSTAGE PAID
Pitney Bowes
10/16/2018 ComBasPrice
90111921621 NO SURCHARGE
0 lbs 4 025
024Po037629820

USPS FIRST-CLASSTM PKG

EMESA TEC? NOLOG Y 1
4352 i: LA PAJMA fivt
ANA HEI CA 9781}? 1 836

0000

Co99
RIShABH JAIN
1 Sm: 2395

5032 Forbes Ave

Plttsburgh PA 15289-2000

-‘<

USPS TRACKING

lillllllllllll Il 11111

9400 1096 9993 9373 1787 02"""
	barcode = 12345678
	return string, barcode

def run():
	global currBin
	global status
	conn = connect("data.db")
	c = conn.cursor()
	c.execute("""SELECT num FROM bins WHERE status='Available'""")
	try:
		currBin = int(c.fetchone()[0])
		status="Available"
	except:
		currBin = "-"
		status = "All bins are full"
	if status=="Available":
		color = "green"
	else:
		color = "red"
	conn.close()

	scanScreen = Tk()
	scanScreen.title("Scanning Station")
	scanScreen.geometry("700x500")

	def fillBin():
		global currBin
		global status
		color = "red"
		binNumLabel.configure(bg=color)
		status = "Full"
		binStatus.configure(text = "Status: "+status)
		conn = connect("data.db")
		c = conn.cursor()
		c.execute("UPDATE bins SET status = ? WHERE num = ?",(status,currBin,))
		conn.commit()
		conn.close()

	def switchBin():
		global currBin
		global status
		conn = connect("data.db")
		c = conn.cursor()
		c.execute("""SELECT * FROM bins""")
		allBins = c.fetchall()
		def select():
			global currBin
			global status
			try:
				item = listBox.get(listBox.curselection())
				currBin = int(item.split(" ")[0])
				c.execute("""SELECT status FROM bins WHERE num = ?""", (currBin,))
				status = c.fetchone()[0]
				if status=="Available":
					color = "green"
				else:
					color = "red"
				binNumLabel.configure(text=str(currBin), bg=color)
				binStatus.configure(text = "Status: "+status)
				conn.close()
				binScreen.destroy()
			except:
				pass
		
		binScreen = Toplevel()
		notButtonFrame = Frame(binScreen)
		scrollbar = Scrollbar(notButtonFrame)
		listBox = Listbox(notButtonFrame, font="Arial 12", yscrollcommand = scrollbar.set)
		scrollbar.configure(command=listBox.yview)
		selectButton = Button(binScreen, text = "OK", command = select)
		listBox.pack(side=LEFT, fill=BOTH, expand=1)
		scrollbar.pack(side=RIGHT, fill=Y)
		notButtonFrame.pack(side=TOP, fill=BOTH, expand=1)
		selectButton.pack(side=BOTTOM)
		for item in allBins:
			listBox.insert(END, str(item[0])+" - "+item[1])
		binScreen.mainloop()

	def scanning():
		global currBin
		global status
		outString, barcode = scanFunction()
		outString = outString.replace("5032","")
		outString = outString.lower()
		while " " in outString:
			outString = outString.replace(" ","")
		index = outString.find("forbes")
		smc = None
		for i in range(index-20, index+20):
			if outString[i] in string.digits:
				if outString[i+1] in string.digits:
					if outString[i+2] in string.digits:
						if outString[i+3] in string.digits:
							smc = int(outString[i:i+4])
		if smc!=None:
			conn = connect("data.db")
			c = conn.cursor()
			c.execute("""SELECT smc, firstname, lastname, andrew FROM people WHERE smc=?""",(smc,))
			pdata = c.fetchone()
			smc = pdata[0]
			firstname = pdata[1]
			lastname = pdata[2]
			andrew = pdata[3]
			if lastname in outString:
				c.execute("""INSERT INTO packages(smc, lastname, firstname, barcode, bin, andrew)
							 VALUES(?,?,?,?,?,?)""", (smc, lastname, firstname, barcode, currBin, andrew,))
				print("Package added for "+firstname+" "+lastname)
			else: 
				print("SMC does not match lastname")
			conn.commit()
			conn.close()
		else:
			print("No SMC found")

	binFrame = Frame(scanScreen)
	binLabel = Label(binFrame, text = "Current Bin", font = "Arial 15")
	binNumLabel = Label(binFrame, text = str(currBin), font = "Arial 150 bold", bg=color, height = 1, width = 2)
	binStatus = Label(binFrame, text = "Status: "+status, font = "Arial 12")
	buttonFrame = Frame(binFrame)
	binFullButton = Button(buttonFrame, text = "Bin filled", command = fillBin)
	binSwitchButton = Button(buttonFrame, text = "Switch Bin", command = switchBin)
	scanButton = Button(scanScreen, text = "Scan", borderwidth=50, command = scanning)
	scanButton.grid(row=0, column=1, padx = 25)
	binFrame.grid(row=0,column=0)
	binLabel.pack(side=TOP)
	buttonFrame.pack(side=BOTTOM, pady=10)
	binFullButton.pack(side=LEFT, padx=5)
	binSwitchButton.pack(side=RIGHT, padx=5)
	binStatus.pack(side=BOTTOM)
	binNumLabel.pack(side=BOTTOM)
	scanScreen.mainloop()

if __name__ == "__main__":
	init()
	run()
