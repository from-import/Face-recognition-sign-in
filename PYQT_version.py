import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QDialog,
    QLineEdit,
    QMessageBox,
    QInputDialog,
)
from PyQt5.QtGui import QPixmap
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

class AdminLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("管理员登录")
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("请输入管理员账号")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("请输入管理员密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("登录", self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        admin_username = "admin"
        admin_password = "password"

        username = self.username_input.text()
        password = self.password_input.text()

        if username == admin_username and password == admin_password:
            QMessageBox.information(None, "登录成功", "管理员登录成功")
            self.accept()
        else:
            QMessageBox.warning(None, "登录失败", "管理员账号或密码错误")

class AdminFunctionality(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        add_photo_button = QPushButton("增加照片", self)
        add_photo_button.clicked.connect(self.add_photo)
        layout.addWidget(add_photo_button)

        delete_photo_button = QPushButton("删除照片", self)
        delete_photo_button.clicked.connect(self.delete_photo)
        layout.addWidget(delete_photo_button)

        exit_button = QPushButton("退出", self)
        exit_button.clicked.connect(self.accept)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def add_photo(self):
        # Add a photo to the training dataset
        new_photo_path, new_photo_ok = QFileDialog.getOpenFileName(None, "选择新照片的文件", "", "Images (*.jpg *.png)")
        if new_photo_ok:
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
                    QMessageBox.information(None, "成功", f"照片 '{name}' 已添加到训练集。")
                else:
                    QMessageBox.warning(None, "错误", "未能识别到人脸，请尝试其他照片。")
            else:
                QMessageBox.warning(None, "错误", "文件路径不存在，请重新输入。")

    def delete_photo(self):
        # Delete a photo from the training dataset
        items = [f"{i + 1}. {name}" for i, name in enumerate(known_face_names)]
        item, item_ok = QInputDialog.getItem(None, "删除照片", "已知人脸列表:", items, editable=False)
        if item_ok:
            delete_index = int(item.split(".")[0]) - 1
            if 0 <= delete_index < len(known_face_names):
                deleted_name = known_face_names.pop(delete_index)
                deleted_encoding = known_face_encodings.pop(delete_index)
                QMessageBox.information(None, "成功", f"已删除照片 '{deleted_name}'。")
            else:
                QMessageBox.warning(None, "错误", "无效的编号，请重新输入。")

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Face Recognition Login')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.user_signin_button = QPushButton('用户签到', self)
        self.user_signin_button.clicked.connect(self.user_signin)
        self.layout.addWidget(self.user_signin_button)

        self.admin_login_button = QPushButton('管理员登录', self)
        self.admin_login_button.clicked.connect(self.admin_login)
        self.layout.addWidget(self.admin_login_button)

        self.quit_button = QPushButton('退出', self)
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

    def user_signin(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择用户照片', '', 'Images (*.jpg *.png)', options=options
        )
        if file_path:
            image = Image.open(file_path)
            pixmap = QPixmap(file_path)
            self.display_image(pixmap)
            user_sign_in(image)

    def admin_login(self):
        admin_dialog = AdminLoginDialog()
        if admin_dialog.exec_() == QDialog.Accepted:
            admin_func = AdminFunctionality()
            admin_func.exec_()

    def display_image(self, pixmap):
        label = QLabel(self)
        label.setPixmap(pixmap)
        self.layout.addWidget(label)

def user_sign_in(login_image):
    input_image = login_image
    input_image = input_image.convert("RGB")
    input_image = np.array(input_image)
    face_locations = face_recognition.face_locations(input_image)
    face_encodings = face_recognition.face_encodings(input_image, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        match_indices = np.where(face_distances <= custom_threshold)[0]

        if len(match_indices) > 0:
            best_match_index = match_indices[np.argmin(face_distances[match_indices])]
            name = known_face_names[best_match_index]
            accuracy = 1 - face_distances[best_match_index]
            accuracy_percent = round(accuracy * 100, 2)
            if accuracy_percent > 0.3:
                QMessageBox.information(None, "用户签到成功", f"{name} 用户签到成功，识别准确度：{accuracy_percent}%")
        else:
            name = "Unknown"
            QMessageBox.information(None, "未识别用户", "未识别用户，准确度不适用")

        face_names.append(name)

    for name in face_names:
        if name != "Unknown":
            break

def main():
    app = QApplication(sys.argv)
    mainWindow = FaceRecognitionApp()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
