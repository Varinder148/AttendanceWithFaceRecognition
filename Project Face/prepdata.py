import cv2
import mysql.connector

# setting up db connection and db cursor
mydb = mysql.connector.connect(
  host="localhost",             
  user="root",
  passwd="shubh"                                   # mysql password
)
mycursor = mydb.cursor()
mycursor.execute("use test;")
mycursor.execute("select max(id) from attendance;")
testid=mycursor.fetchone()
cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('model.xml')
#faceid = input('id=')
faceid=testid[0]+1
count = 0
while(True):

    _, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces =detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 1)     
        count += 1
        cv2.imwrite(r"dataset/" + str(faceid) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w]-100)
        cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count >= 70: 
        break
print("enter the credentials of new student")
rollno=input('Roll number = ')
name=input('Name = ')
mycursor.execute("insert into attendance values(" + str(faceid) + " , " + str(rollno) + " , '"+name+"',1,0);")
mydb.commit()
print("new student's entry added successfully!")
mycursor.execute("select roll,name,attn from attendance;")
myresult=mycursor.fetchall()
print("\n\n\nRefreshed list of students\n\n+-----------------------+---------------+----------------+\n|Roll No\t\t|Name\t\t|Total Attendance|\n+-----------------------+---------------+----------------+")
for x in myresult :
    roll , name ,attn= x
    if(roll != 0):
        print("|"+str(roll)+"\t\t\t|"+name+"\t|"+str(attn)+"\t\t |")
      
print("+-----------------------+---------------+----------------+")
mydb.commit()
cam.release()
cv2.destroyAllWindows()



