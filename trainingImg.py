import cv2
import numpy as np
import os
from PIL import Image
from firebase.firestore import Users

# neu bi loi => mo cmd(run as adm): pip uninstall opencv-contrib-python => pip install opencv-contrib-python
recognizer = cv2.face.LBPHFaceRecognizer_create()

paths = []

for user in Users.users:
    if user.to_dict().get('email') != 'admin@gmail.com':
        paths.append(f"dataSet/{user.to_dict().get('name')}")


def getImageWithId(paths):
    face_list = []
    id_list = []
    for path in paths:
        # truy cap vao tat ca cac file trong thu muc dataSet
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]

        for image_path in image_paths:
            face_img = Image.open(image_path).convert('L')

            face_np = np.array(face_img, 'uint8')

            u_id = int(image_path.split('.')[1])

            face_list.append(face_np)
            id_list.append(u_id)

            cv2.imshow('Traning', face_np)
            cv2.waitKey(10)
    return face_list, id_list


faces, ids = getImageWithId(paths)

recognizer.train(faces, np.array(ids))

if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainingData.yml')

cv2.destroyAllWindows()
