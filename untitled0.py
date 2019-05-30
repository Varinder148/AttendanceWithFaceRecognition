# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:55:48 2018

@author: Lenovo
"""

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="shubh"
)
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES LIKE 'test';")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)

if any("test" in s for s in myresult):
    print(1)
