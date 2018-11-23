#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('database.db')

#Create database if it doesn't exist

try:
    conn.execute('CREATE TABLE members(mid INTEGER PRIMARY KEY AUTOINCREMENT, google_id INTEGER, email TEXT NOT NULL, name TEXT NOT NULL, token TEXT, i_num TEXT)')
    conn.execute("CREATE TABLE interest(intrst_id INTEGER REFERENCES members(mid) ON UPDATE CASCADE, interest TEXT NOT NULL, level INT)")
    conn.execute('''CREATE TABLE expertise(exprt_id INTEGER REFERENCES members(mid) ON UPDATE CASCADE, expertise TEXT NOT NULL, level INT)''')
    conn.commit()
    print("Database successfully created")
#Database exists already
except:
	print("Database already exists")
#close database

def populate_members:
	cur.execute("INSERT INTO members (google_id, email, name, i_number) VALUES (?,?,?,?)", (google_id, email, name, inumber))
def populate_interest:
def populate_expertise:
def get_names:
def get_interests_from_names:
def get_expertise_from_names:
conn.close()
