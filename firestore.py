import firebase_admin
from firebase_admin import credentials, firestore


class Users:
    # Khởi tạo Firebase Admin SDK với tệp json bạn đã tải về
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'garden-app-v1.appspot.com'
    })

    # Lấy tham chiếu đến Firestore
    db = firestore.client()

    # Lấy collection từ Firestore.
    collection_ref = db.collection("users")

    # Lấy dữ liệu từ collection "users"
    docs = collection_ref.stream()

    # Danh sách đường dẫn đến các tệp ảnh bạn muốn tải xuống
    users = []

    for doc in docs:
        if doc.exists:
            # Lấy dữ liệu từ các trường (fields) cụ thể
            data = doc.to_dict()
            userName = data.get("name")
            userEmail = data.get("email")

            if (userName is not None) & (userEmail != 'admin@gmail.com'):
                users.append(doc)
                print("lấy dữ liệu thành công")
            else:
                print("Trường không tồn tại trong tài liệu.")



