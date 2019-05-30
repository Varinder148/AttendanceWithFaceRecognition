import cv2
import numpy as np
from PIL import Image
import os

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
names = ['None', 'Varinder','Manjot','Shubhreet','Sanket',"Rao"] 
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
        if (confidence <100 ):
            id = names[id]
        else:
            id = "Anonymous"
        cv2.putText(img, str(id), (x+5,y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
        cv2.putText(img, str(round(confidence)), (x,y+10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff
    if k == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
