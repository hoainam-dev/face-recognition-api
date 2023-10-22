import cv2
import numpy as np
import sqlite3
import os
from firestore import Users


def insertOrUpdate(id, name):
    conn = sqlite3.connect('data.db')

    query = "SELECT * FROM people WHERE ID=" + str(id)
    cuscor = conn.execute(query)

    isRecordExist = 0

    for row in cuscor:
        isRecordExist = 1

    if (isRecordExist == 0):
        query = "INSERT INTO people(ID, Name) VALUES(" + str(id) + ", '" + str(name) + "')"
    else:
        query = "UPDATE people SET Name=' " + str(name) + " ' WHERE ID=" + str(id)
    conn.execute(query)
    conn.commit()
    conn.close()


# load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture('http://192.168.1.121:8080/video')

# Lấy dữ liệu từ collection "users"
docs = Users.users
userName = ""
userId = ""
for doc in docs:
    download_folder = f'dataSet/{doc.to_dict().get("name")}/'
    if doc.exists:
        if not os.path.exists(download_folder):
            userName = doc.to_dict().get("name")
            userId = doc.to_dict().get("faceId")
            # insert to db
            insertOrUpdate(doc.to_dict().get("faceId"), doc.to_dict().get("name"))


print(userName)
print(userId)
sampleNum = 0

while True:

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if not os.path.exists(f'dataSet/{userName}'):
            os.makedirs(f'dataSet/{userName}')

        sampleNum += 1

        cv2.imwrite(f'dataSet/{userName}/{userName}.{userId}.' + str(sampleNum) + '.jpg', gray[y: y + h, x: x + w])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if sampleNum > 70:
        break

cap.release()
cv2.destroyAllWindows()
