import face_recognition
from PIL import Image


def Face_Extraction(image_path):
    # 加载图像
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    print(len(face_locations))
    result = []
    # 检查是否检测到了人脸
    for i in range(0,len(face_locations)):

        # 获取第一个检测到的人脸位置
        top, right, bottom, left = face_locations[i]

        # 使用Pillow打开原始图像
        img = Image.open(image_path)

        # 剪切人脸区域
        face_image = img.crop((left, top, right, bottom))
        result.append(face_image)

        # 保存人脸到新文件
        face_image.save(f"{image_path}_result{i}.png")
        print(f"人脸已保存到{image_path}_result{i}.png")


image_path = "many_face.png"
Face_Extraction(image_path)
