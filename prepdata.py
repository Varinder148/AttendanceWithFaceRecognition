import cv2
cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('model.xml')
faceid = input('id=')
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
cam.release()
cv2.destroyAllWindows()



