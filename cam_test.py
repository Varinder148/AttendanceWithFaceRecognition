# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 13:11:10 2018

@author: Lenovo
"""
import atexit
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import mysql.connector

# setting up db connection and db cursor
mydb = mysql.connector.connect(
  host="localhost",             
  user="root",
  passwd="shubh"                                   # mysql password
)
mycursor = mydb.cursor()

# creating window and its elements
width, height = 450, 410
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.title("Attendace System Using Face Recognition")
MainFrame=tk.Frame(root)
UpperFrame=tk.Frame(MainFrame)
MidFrame=tk.Frame(MainFrame)
MidFrame1=tk.Frame(MidFrame)
MidFrame2=tk.Frame(MidFrame)
LowerFrame=tk.Frame(MainFrame)
label_title=tk.Label(UpperFrame , text = "Attendance Using Face Recognition" ,  font=("Times New Roman" , 20))
label_title.pack()
lmain = tk.Label(MidFrame1 , relief=tk.RAISED)
lmain.pack()
label_atnLog=tk.Label(MidFrame2 , text="Attendace Log")
label_atnLog.pack()
text=tk.Text(MidFrame2 , height=20,width=50)
text.pack()
# entry for a new student
def newStudent(roll,name):
    mycursor.execute("insert into test1 values("+str(roll)+",'"+name+",0,0,0);")
    mydb.commit()

def addStudent():
    print("new student")
    



addNewStudBtn=tk.Button(LowerFrame, text= "Add New Student" ,command = addStudent)
addNewStudBtn.pack()
UpperFrame.pack()
MidFrame1.pack(side=tk.LEFT,padx=10,pady=10)
MidFrame2.pack(side=tk.RIGHT,padx=10,pady=10)
MidFrame.pack()
LowerFrame.pack(side=tk.BOTTOM, padx=10,pady=10)
MainFrame.pack()
 # function for creating webcam frame
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

show_frame()

# checking if databse and table exists 
mycursor.execute("SHOW DATABASES;")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)
# if databse found , use it , else create the database and table
if any("test" in s for s in myresult):
    mycursor.execute("use test;")
    mycursor.execute("select rollno,name,cur_attn from test1")
    myresult=mycursor.fetchall();
    text.delete(1.0,tk.END)
    for x in myresult:
        rollno, name , curatn = x
        atn="absent"
        if curatn==1:
            atn="present"
        text.insert(tk.END,str(rollno) + "  "+ name + " is "+atn+"\n")
else :
    mycursor.execute("create database test;")
    mycursor.execute("use test;")
    mycursor.execute("create table test1(rollno int , name varchar(20) , class varchar(20) , attn int , total_attn int , cur_attn int);")
    mydb.commit()
    

# marking attendance
def markAttendace(roll):
    mycursor.execute("update test1 set cur_attn = 1 where roll="+ roll)
    mydb.commit()
    mycursor.execute("select rollno,name,cur_attn from test1")
    myresult=mycursor.fetchall();
    text.delete(1.0,tk.END)
    for x in myresult:
        rollno, name , curatn = x
        atn="absent"
        if curatn==1:
            atn="present"
        text.insert(tk.END,str(rollno) + "  "+ name + " is "+atn+"\n")
# function executed while closing of program
def my_function():
    print("exiting")
    mycursor.execute("update test1 set attn = attn + cur_attn;")
    mycursor.execute("update test1 set cur_attn = 0;")
    mycursor.execute("update test1 set total_attn = total_attn+1;")
    mydb.commit()
    root.destroy()
    cap.release()


        
root.protocol( "WM_DELETE_WINDOW", my_function )

root.mainloop()