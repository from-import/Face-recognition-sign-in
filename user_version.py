from PIL import Image
import face_recognition
import cv2
import numpy as np
import os

# 训练集文件夹
train_folder = "train"

# 初始化存储已知人脸编码和姓名的数组
known_face_encodings = []
known_face_names = []

# 遍历训练集文件夹中的所有图片
for filename in os.listdir(train_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        train_image = Image.open(os.path.join(train_folder, filename))
        train_image = train_image.convert("RGB")  # 转换为RGB颜色空间
        # 将Pillow图像转换为NumPy数组
        train_image = np.array(train_image)
        # 提取人脸编码
        face_encoding = face_recognition.face_encodings(train_image)[0]
        # 使用文件名（去除文件扩展名）作为人脸编码的标识
        name = os.path.splitext(filename)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

# 设置自定义相似度阈值
custom_threshold = 0.9


def admin_login():
    # Define admin username and password (you can change these)
    admin_username = "admin"
    admin_password = "password"

    # Request username and password input
    username_input = input("请输入管理员账号: ")
    password_input = input("请输入管理员密码: ")

    # Check if the input matches the admin credentials
    if username_input == admin_username and password_input == admin_password:
        while True:
            print("\n管理员登录成功，请选择功能:")
            print("1. 增加照片")
            print("2. 删除照片")
            print("3. 退出")

            admin_choice = input("请选择功能 (1/2/3): ")

            if admin_choice == "1":
                # Add a photo to the training dataset
                new_photo_path = input("请输入新照片的文件路径: ")
                if os.path.exists(new_photo_path):
                    train_image = Image.open(new_photo_path)
                    train_image = train_image.convert("RGB")
                    train_image = np.array(train_image)
                    face_encodings = face_recognition.face_encodings(train_image)
                    if len(face_encodings) > 0:
                        # Assuming only one face per image is added to the dataset
                        known_face_encodings.append(face_encodings[0])
                        name = os.path.splitext(os.path.basename(new_photo_path))[0]
                        known_face_names.append(name)
                        print(f"照片 '{name}' 已添加到训练集。")
                    else:
                        print("未能识别到人脸，请尝试其他照片。")
                else:
                    print("文件路径不存在，请重新输入。")

            elif admin_choice == "2":
                # Delete a photo from the training dataset
                print("已知人脸列表:")
                for i, name in enumerate(known_face_names):
                    print(f"{i + 1}. {name}")

                delete_index = input("请选择要删除的照片编号 (1/2/3/...): ")
                try:
                    delete_index = int(delete_index)
                    if 1 <= delete_index <= len(known_face_names):
                        deleted_name = known_face_names.pop(delete_index - 1)
                        deleted_encoding = known_face_encodings.pop(delete_index - 1)
                        print(f"已删除照片 '{deleted_name}'。")
                    else:
                        print("无效的编号，请重新输入。")
                except ValueError:
                    print("无效的输入，请输入数字。")

            elif admin_choice == "3":
                print("退出管理员功能")
                break

            else:
                print("无效的选择，请重新输入。")

    else:
        print("管理员账号或密码不正确。")


def user_sign_in(login_image):
    # 读取待识别的图片
    input_image = login_image
    input_image = input_image.convert("RGB")  # 转换为RGB颜色空间
    input_image = np.array(input_image)  # 转换为NumPy数组

    # 在待识别的图片中查找人脸
    face_locations = face_recognition.face_locations(input_image)
    face_encodings = face_recognition.face_encodings(input_image, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # 计算人脸距离
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        # 检查是否有已知人脸在自定义阈值内
        match_indices = np.where(face_distances <= custom_threshold)[0]

        if len(match_indices) > 0:
            # 使用最接近的已知人脸
            best_match_index = match_indices[np.argmin(face_distances[match_indices])]
            name = known_face_names[best_match_index]
            accuracy = 1 - face_distances[best_match_index]  # 计算准确度
            accuracy_percent = round(accuracy * 100, 2)  # 转化为百分比形式
            if accuracy_percent>0.3:
                print(f"{name} 用户签到成功，识别准确度：{accuracy_percent}%")
        else:
            name = "Unknown"
            print(f"未识别用户，准确度不适用")

        face_names.append(name)

    for name in face_names:
        if name != "Unknown":
            break  # 如果有一个已知用户签到成功，就不再检查其他人脸




while True:
    print("\n\n\n\n选择功能:")
    print("1. 用户签到")
    print("2. 管理员登录")
    print("3. 退出")

    choice = input("请选择功能 (1/2/3): ")

    if choice == "1":
        image = Image.open("1.png")
        user_sign_in(image)
    elif choice == "2":
        admin_login()
    elif choice == "3":
        print("退出程序")
        break
    else:
        print("无效的选择，请重新输入。")