#!/usr/bin/python

import sqlite3
import pandas as pd
import os

def populate_members():
	#cur.execute("INSERT INTO members (google_id, email, name, i_number) VALUES (?,?,?,?)", (google_id, email, name, inumber))
	df_peers = pd.read_csv(os.path.join(os.getcwd(), 'server', 'data', 'excel_files', 'mentors.csv'))
	emails = df_peers['email']
	names = df_peers['Name']
	inums = df_peers['i_number']
	ln = len(names)
	for i in range(ln):
		google_id = None
		email = emails[i]
		name = names[i]
		inumber = inums[i]
		conn.execute("INSERT INTO members (google_id, email, name, i_num) VALUES (?,?,?,?)",(google_id, email, name, inumber))
	#conn.commit()

def populate_interest():
	df_peers = pd.read_csv(os.path.join(os.getcwd(), 'server', 'data', 'excel_files', 'mentors.csv'))
	interests = df_peers['Interest']
	score = 1
	names = df_peers['Name']
	ln = len(names)
	for i in range(ln):
		interest_list = interests[i]
		print(interest_list)
		print(type(interest_list))
		interest_list = interest_list.strip().split()
		for j in range(len(interest_list)):
			conn.execute("INSERT INTO interest (intrst_id, interest, level) VALUES (?,?,?)",(i, interest_list[j], score))
	#conn.commit()
def populate_expertise():
	df_peers = pd.read_csv(os.path.join(os.getcwd(), 'server', 'data', 'excel_files', 'mentors.csv'))
	expertises = df_peers['Expertise']
	score = 1000
	names = df_peers['Name']
	ln = len(names)
	for i in range(ln):
		expertises_list = expertises[i]
		expertises_list = expertises_list.strip().split()
		for j in range(len(expertises_list)):
			conn.execute("INSERT INTO expertise (exprt_id, expertise, level) VALUES (?,?,?)", (i, expertises_list[j], score))
	#conn.commit()



if __name__ == "__main__":

	conn = sqlite3.connect('database.db')
	drop_members = "DROP TABLE members"
	drop_interest = "DROP TABLE interest"
	drop_expertise = "DROP TABLE expertise"
	#Create database if it doesn't exist
	try:
		conn.execute(drop_members)
	except:
		print("no member to drop")

	try:
		conn.execute(drop_interest)
	except:
		print("no interest to drop")

	try:
		conn.execute(drop_expertise)
	except:
		print("no expertise to drop")

	try:
		conn.execute('CREATE TABLE members(mid INTEGER PRIMARY KEY AUTOINCREMENT, google_id INTEGER, email TEXT NOT NULL, name TEXT NOT NULL, token TEXT, i_num TEXT)')
		conn.execute("CREATE TABLE interest(intrst_id INTEGER REFERENCES members(mid) ON UPDATE CASCADE, interest TEXT NOT NULL, level INT)")
		conn.execute('''CREATE TABLE expertise(exprt_id INTEGER REFERENCES members(mid) ON UPDATE CASCADE, expertise TEXT NOT NULL, level INT)''')
		conn.commit()
		print("Database successfully created")
	#Database exists already
	except:
		print("Database already exists")

	populate_members()
	print("Table members created successfully")


	populate_interest()
	print("Table interest created successfully")


	populate_expertise()
	print("Table expertise created successfully")



	#close database
	conn.commit()
	conn.close()