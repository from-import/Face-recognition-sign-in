from PIL import Image
import face_recognition
import cv2
import numpy as np
import os

# 训练集文件夹
train_folder = "train"

# 测试 读取待识别的图片
input_image = Image.open("1.png")
input_image = input_image.convert("RGB")  # 转换为RGB颜色空间
input_image = np.array(input_image)  # 转换为NumPy数组

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
    else:
        name = "Unknown"

    face_names.append(name)

# 将BGR颜色通道排序改为RGB
cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB, input_image)

# 显示结果
for (top, right, bottom, left), name in zip(face_locations, face_names):
    # 在图片上绘制人脸边框
    cv2.rectangle(input_image, (left, top), (right, bottom), (0, 0, 255), 2)  # 红色边框

    # 显示姓名和识别准确度
    font = cv2.FONT_HERSHEY_DUPLEX
    text = f'{name} ({1 - face_distances[best_match_index]:.2f})' if name != "Unknown" else "Unknown"
    cv2.putText(input_image, text, (left, top - 10), font, 0.4, (0, 0, 255), 1)  # 红色文字

# 保存结果图片
cv2.imwrite("result.png", input_image)
# 显示待识别图片
cv2.imshow('人脸识别', input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
