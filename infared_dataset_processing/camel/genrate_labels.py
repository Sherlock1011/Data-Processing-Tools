import os
import glob

image_width = 336
image_height = 256

def read_data_to_dict(file_path):
    """读取数据，并整理为frame number作为索引的字典

    Args:
        path (str): label信息文件
    """
    # 创建一个空白字典，用来存储数据
    data_dict = {}
    
    # 读取文件
    with open(file_path, 'r') as file:
        # 遍历文件中的每一行
        for line in file:
            # 去掉末尾的换行符，并按照制表符分割字符串
            parts = line.strip().split('\t')
            # 将分割后的数据转换为正确的类型
            frame_number = parts[0].zfill(6)
            track_id = int(parts[1])
            annoatation_class = parts[2]
            box_w = float(parts[5])
            box_h = float(parts[6])
            x = (float(parts[3]) + box_w / 2) / image_width
            y = (float(parts[4]) + box_h / 2) / image_height
            w = box_w / image_width
            h = box_h /image_height
            
            # 如果字典中不存在当前编号的键，则创建一个空列表
            if frame_number not in data_dict:
                data_dict[frame_number] = []
                
            data_dict[frame_number].append({
                'Track ID': track_id,
                "Annotation Class": annoatation_class,
                'x': x,
                'y': y,
                'w': w,
                'h': h
            })
    
    return data_dict

def generate_label_files(data_dict, label_dir):
    """根据label信息字典，生成对应图像数据的yolo格式label文件

    Args:
        data_dict (dict): 标签信息字典，索引为Frame Number
        label_dir (str): label存储路径
    """
    # # 创建标签文件夹
    if not os.path.exists(label_dir):
        os.mkdir(label_dir)
        
    for label_name in data_dict:
        label_file_path = os.path.join(label_dir, label_name+'.txt')
        with open(label_file_path, 'w') as file:
            for label_data in data_dict[label_name]:
                if label_data['Annotation Class'] == '1':
                    annotation_class = 0
                    x = label_data['x']
                    y = label_data['y']
                    w = label_data['w']
                    h = label_data['h']
                    data_str = f'{annotation_class} {x} {y} {w} {h}\n'
                    file.write(data_str)
                else:
                    continue
        
def generate_all_labels(data_dir):
    """将指定文件夹下的所有CAMLE数据生成对应的label标签，文件组织如下：
            |
            |--CAMEL
                |--seq1
                    |--images
                    |--Seq1-IR.txt
                |--seq2
                    |--images
                    |--Seq2-IR.txt
                |...

    Args:
        data_dir (str): CAMEL数据存储路径
    """
    data_folders = os.listdir(data_dir)
    for folder in data_folders:
        data_folder_path = os.path.join(data_dir, folder)
        images_path = os.path.join(data_folder_path, 'images')
        label_path = os.path.join(data_folder_path, 'labels')
        label_info_path = glob.glob(os.path.join(data_folder_path, "*.txt"))[0]
        
        # 为子数据集创建labels
        label_info_dict = read_data_to_dict(label_info_path)
        generate_label_files(label_info_dict, label_path)
        print(f'{folder}处理完成！')

if __name__ == '__main__':
    # file_path = "/home/yangzeyu/dataset/infrared/CAMEL/seq3/Seq3-IR.txt"
    # label_dir = "/home/yangzeyu/dataset/infrared/CAMEL/seq3/labels"
    # data_dict = read_data_to_dict(file_path)
    # generate_label_files(data_dict, label_dir)
    data_dir = "/home/yangzeyu/dataset/infrared/CAMEL"
    generate_all_labels(data_dir)