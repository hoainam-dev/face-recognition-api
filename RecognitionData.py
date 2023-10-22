import cv2
import sqlite3

# Traning hinh anh nhan dien vs thu vien nhan dien khuon mat
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("./recognizer/trainingData.yml")


# get profile by id from database
def getProfile(id):
    conn = sqlite3.connect('data.db')
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cuscor = conn.execute(query)

    profile = None

    for row in cuscor:
        profile = row

    conn.close()
    return profile


cap = cv2.VideoCapture('http://192.168.1.121:8080/video')

fontface = cv2.FONT_HERSHEY_COMPLEX

while (True):
    ret, frame = cap.read()

    resize_fr = cv2.resize(frame, (800, 600))

    gray = cv2.cvtColor(resize_fr, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(resize_fr, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roi_gray = gray[y: y + h, x: x + w]

        id, confidence = recognizer.predict(roi_gray)

        if confidence < 50:
            profile = getProfile(id)
            if profile != None:
                cv2.putText(resize_fr, "name:" + str(profile[1]) + "id:" + str(profile[0]), (x + 10, y + h + 30), fontface,
                            1, (0, 255, 0), 2)
        else:
            cv2.putText(resize_fr, "Unknow", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)

    cv2.imshow('Image', resize_fr)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
