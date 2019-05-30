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
mycursor.execute("use test;")
mycursor.execute("select name from attendance;");
names = mycursor.fetchall()
print(names)