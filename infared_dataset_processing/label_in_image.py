import os
import cv2
import glob

def draw_yolo_boxes(image_folder, label_folder, output_folder, class_names):
    # 创建结果文件夹，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历图片文件夹中的所有图片
    for image_file in os.listdir(image_folder):
        # 获取图像文件的完整路径
        image_path = os.path.join(image_folder, image_file)
        # 加载图像
        image = cv2.imread(image_path)
        
        # 获取图像的宽度和高度
        height, width, _ = image.shape

        # 获取对应的标签文件名（假设标签文件与图像文件同名，扩展名为.txt）
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(label_folder, label_file)

        # 读取标签文件
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f.readlines():
                    # 分割每一行的数据
                    parts = line.strip().split()
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    box_width = float(parts[3])
                    box_height = float(parts[4])

                    # 将归一化的坐标转换为图像上的像素坐标
                    x_center_pixel = int(x_center * width)
                    y_center_pixel = int(y_center * height)
                    box_width_pixel = int(box_width * width)
                    box_height_pixel = int(box_height * height)

                    # 计算左上角和右下角的坐标
                    x1 = int(x_center_pixel - box_width_pixel / 2)
                    y1 = int(y_center_pixel - box_height_pixel / 2)
                    x2 = int(x_center_pixel + box_width_pixel / 2)
                    y2 = int(y_center_pixel + box_height_pixel / 2)

                    # 画矩形框在图像上
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # 在框的上方标注类别名称
                    label = class_names[class_id] if class_id < len(class_names) else f'Class {class_id}'
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # 将图像保存到输出文件夹中
            output_path = os.path.join(output_folder, image_file)
            cv2.imwrite(output_path, image)
        else:
            print(f"标签文件不存在: {label_path}")
            
def draw_all_dataset(dataset_dir):
    class_names = ['person', 'cat', 'car']
    sub_dataset_path = [os.path.join(dataset_dir, folder) for folder in os.listdir(dataset_dir)]
    for path in sub_dataset_path:
        image_folder = os.path.join(path, 'images')
        label_folder = os.path.join(path, 'labels')
        output_folder = os.path.join(path, 'results')
        draw_yolo_boxes(image_folder, label_folder, output_folder, class_names)
        print(os.path.basename(path) + "已完成！")
        
    
if __name__ == '__main__':
    dataset_dir = '/home/yangzeyu/dataset/infrared/OpenThermalPose/'

    # 用法示例
    image_folder = dataset_dir + 'images'  # 替换为图像文件夹路径
    label_folder = dataset_dir + 'labels'  # 替换为标签文件夹路径
    output_folder = dataset_dir + 'labeled'  # 替换为保存结果的文件夹路径

    # 类别名称列表，按YOLO标签中类别的索引顺序排列
    class_names = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck', 'cat', 'dog']  # 替换为你的实际类别名称

    draw_yolo_boxes(image_folder, label_folder, output_folder, class_names)
    # dataset_dir = '/home/yangzeyu/dataset/infrared/CAMEL'
    # draw_all_dataset(dataset_dir)
