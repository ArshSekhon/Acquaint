#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('database.db')

#Create database if it doesn't exist

try:
	conn.execute('CREATE TABLE members(mid INTEGER PRIMARY KEY AUTOINCREMENT, google_id INTEGER, email TEXT NOT NULL, name TEXT NOT NULL, token TEXT)')
	conn.commit()
	print("Database successfully created")
#Database exists already
except:
	print("Database already exists")
#close database
conn.close()
