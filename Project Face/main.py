import cv2
import numpy as np
from PIL import Image
import os
import mysql.connector
# setting up db connection and db cursor
mydb = mysql.connector.connect(
  host="localhost",             
  user="root",
  passwd="shubh"                                   # mysql password
)
mycursor = mydb.cursor()
mycursor.execute("use test;")
mycursor.execute("select roll,name,attn from attendance;")
myresult=mycursor.fetchall()
print("list of students\n\n+-----------------------+---------------+----------------+\n|Roll No\t\t|Name\t\t|Total Attendance|\n+-----------------------+---------------+----------------+")
for x in myresult :
    roll , name ,attn= x
    if(roll != 0):
       print("|"+str(roll)+"\t\t\t|"+name+"\t|"+str(attn)+"\t\t |")
       
print("+-----------------------+---------------+----------------+")
mydb.commit()
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("model.xml");

def train(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    f=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')+100
#        cv2.imshow("data",img_numpy)
#       cv2.waitKey(0)
#      cv2.destroyAllWindows()

        id = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            f.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return f,ids

faces,ids = train(path)
recognizer.train(faces, np.array(ids))

def delete(path):
    imagep = [os.path.join(path,f) for f in os.listdir(path)]
    for imag in imagep:
        os.remove(imag)
        
#delete(path)


#recognition part
id = 0
id1 = -1
mycursor.execute("select name from attendance;")
#names = ['None', 'Shubhreet','Manjot','Shubhreet','Sanket',"Rao"]
names=mycursor.fetchall() 
cam = cv2.VideoCapture(0)
while True:

    ret, img =cam.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
       )
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 1)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if (confidence <60 ):
            if(id1!=id):
                mycursor.execute("update attendance set curattn=1 where id=" + str(id) + ";" )
                mydb.commit()
            id1=id
            id = names[id]
        else:
            id = "Anonymous"
        cv2.putText(img, str(id), (x+5,y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
        cv2.putText(img, str(round(confidence)), (x,y+10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff
    if k == ord('q'):
        break
mycursor.execute("update attendance set attn=attn+curattn;")
mycursor.execute("update attendance set curattn=0;")
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
