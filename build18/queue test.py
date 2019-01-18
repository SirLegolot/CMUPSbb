import socket
import sqlite3


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



def receive():
	while True:
		data = conn.recv(1024).decode("utf-8")
		smc = int(data)
		connDB = connect("dataNEW.db")
		c = connDB.cursor()
		c.execute("""SELECT * FROM queue WHERE smc = ?""", (smc,))
		alreadyIn = c.fetchall()
		if len(alreadyIn)>0:
			conn.send(str.encode("IN QUEUE ALREADY"))
		else:
			c.execute("""SELECT * FROM packages WHERE smc = ?""",(smc,))
			result = c.fetchall()
			numPacks = len(result)
			print(numPacks)
			if numPacks!=0:
				for item in result:
					newSMC = item[0]
					newBin = item[4]
					newBarcode = item[3]
					c.execute("""INSERT INTO queue(smc,bin,barcode) VALUES(?,?,?)""",(newSMC,newBin,newBarcode,))
					connDB.commit()
				conn.send(str.encode("YES"))
			else:
				conn.send(str.encode("NO"))
			connDB.close()

receive()