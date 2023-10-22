import os

import cv2
from firebase_admin import storage
from firestore import Users

import sqlite3
import shutil


# function to insert or update user
def insertOrUpdate(u_id, name):
    conn = sqlite3.connect('./data.db')

    query = "SELECT * FROM people WHERE ID=" + str(u_id)
    cuscor = conn.execute(query)

    isRecordExist = 0

    for row in cuscor:
        isRecordExist = 1

    if isRecordExist != 0:
        query = "UPDATE people SET Name=' " + name + " ' WHERE ID=" + str(u_id)
    else:
        query = "INSERT INTO people(ID, Name) VALUES(" + u_id + ", '" + name + "')"
    conn.execute(query)
    conn.commit()
    conn.close()


# Lấy dữ liệu từ collection "users"
docs = Users.users

# Danh sách đường dẫn đến các tệp ảnh bạn muốn tải xuống
image_paths = []

for doc in docs:
    if doc.exists:
        # Lấy dữ liệu từ các trường (fields) cụ thể
        data = doc.to_dict()
        userId = data.get("faceId")
        userName = data.get("name")

        if userName is not None:
            download_folder = f'dataSet/{userName}/'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
                for index in range(1, 16):
                    image_paths.append('faces/' + doc.id + '/' + userName + '.' + userId + '.' + str(index) + '.jpg')

                # Khởi tạo đối tượng lưu trữ Firebase
                bucket = storage.bucket()

                # Lặp qua danh sách đường dẫn và tải xuống từng ảnh
                for image_path in image_paths:
                    # Tạo đường dẫn lưu trữ đầy đủ
                    download_path = download_folder + image_path.split('/')[-1]

                    # Tải xuống tệp ảnh từ Firebase Storage
                    blob = bucket.blob(image_path)
                    blob.download_to_filename(download_path)

                    # Chuyển đổi ảnh thành ảnh xám
                    image = cv2.imread(download_path)
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(download_path, gray_image)

                    print("Tai xuong thanh cong tep: " + image_path + " va luu tai: " + download_path)
                    insertOrUpdate(userId, userName)

                    # copy anh
                    for i in range(1, 10):
                        infor = image_path.split('/')[-1].split('.')
                        copy_path = f"{download_folder}{infor[0]}.{infor[1]}.{infor[2]}{i}.jpg"
                        shutil.copy(download_path, copy_path)
                        insertOrUpdate(userId, userName)
                image_paths.clear()
            else:
                print("Da tai het cac user")
        else:
            print("Truong khong ton tai trong tai lieu.")
