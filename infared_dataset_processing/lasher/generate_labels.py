import os
import cv2
import shutil

dataset_dir = '/home/yangzeyu/dataset/infrared/LasHeR0327/'
training_set = os.path.join(dataset_dir, 'TrainingSet/trainingset/')
target_dir = os.path.join(dataset_dir, 'results')

def get_classes_list(list_file_path):
    classes_list = []
    with open(list_file_path, 'r') as file:
        # 读取文件，去除每行末尾的空白字符
        classes_list = [line.strip() for line in file.readlines()]
    return classes_list

def get_category_dataset_dir(classes_list, match_str):
    """获取指定的类别数据集
       例如：获取所有包含cat的数据集路径 match_str填写'cat'

    Args:
        classes_list (list): 类别列表
        match_str (str): 匹配字符串
    """
    category_dataset_dir = [os.path.join(training_set, dir_name) for dir_name in classes_list if match_str in dir_name]
    return category_dataset_dir

def get_ori_labels(dataset_path):
    """获取原始box label"""
    ori_labels_path = os.path.join(dataset_path, 'infrared.txt')
    with open(ori_labels_path, 'r') as file:
        labels = [line.strip() for line in file.readlines()]
    return labels

def generate_category_yolo_labels(category_dataset_dir, class_id, class_name):
    # 创建存储image和label的文件夹
    images_dir = os.path.join(target_dir, class_name, "images")
    labels_dir = os.path.join(target_dir, class_name, "labels")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    count = 1
    for sub_data_dir in category_dataset_dir:
        ori_images_dir = os.path.join(training_set, sub_data_dir, "infrared")
        ori_labels = get_ori_labels(sub_data_dir)
        ori_images_path = [os.path.join(ori_images_dir, img_name) for img_name in os.listdir(ori_images_dir)]
        ori_images_path = sorted(ori_images_path)
        
        # 确保原数据图像和标签保持一致
        assert len(ori_images_path) == len(ori_labels), "图像与标签不一致"
        
        for img_path, label in zip(ori_images_path, ori_labels):
            image = cv2.imread(img_path)
            height, width, _ = image.shape
            # 这里的x,y是box左上角的坐标
            x,y,w,h = [float(item) for item in label.strip().split(',')]
            # 转换为yolo格式
            yolo_label = {
                'class_id': class_id,
                'x_center': (x + (w/2)) / width,
                'y_center': (y + (h/2)) / height,
                'w': w / width,
                'h': h / height
            }
            # print(f"width:{width},height:{height}. box_x:{yolo_label['x']}, box_y:{yolo_label['y']}, box_width:{yolo_label['w']}, box_height:{yolo_label['h']}")
            image_new_neme = f"{count:06}.jpg"
            label_new_name = f"{count:06}.txt"
            # 复制图像
            shutil.copy(img_path, os.path.join(images_dir, image_new_neme))
            with open(os.path.join(labels_dir, label_new_name), 'w') as file:
                data_str = f"{yolo_label['class_id']} {yolo_label['x_center']} {yolo_label['y_center']} {yolo_label['w']} {yolo_label['h']}\n"
                file.write(data_str)
            count += 1
        
        print(f"{sub_data_dir}已完成转换！")
            
            
            
    

if __name__ == '__main__':
    classes_list_path = dataset_dir + "trainingsetList.txt"
    classes_list = get_classes_list(classes_list_path)
    category_dataset_dir = get_category_dataset_dir(classes_list, 'cat')
    # ori_labels = get_ori_labels(category_dataset_dir[0])
    # for label in ori_labels:
    #     print(label)
    
    generate_category_yolo_labels(category_dataset_dir, 6, 'cat')