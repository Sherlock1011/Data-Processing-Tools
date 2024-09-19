import os
data_folder_dir = '/home/yangzeyu/dataset/infrared/OpenThermalPose'
pose_labels_dir = os.path.join(data_folder_dir, 'pose-labels')

def generate_labels(pose_labels_dir, labels_dir):
    # 检查labels保存路径，如果不存在则创建
    print(labels_dir)
    os.makedirs(labels_dir, exist_ok=True)
    labels_name = sorted([name for name in os.listdir(pose_labels_dir)])
    pose_labels_path = sorted([os.path.join(pose_labels_dir, name) for name in os.listdir(pose_labels_dir)])
    for idx, pose_label_path in enumerate(pose_labels_path):
        file_name = labels_name[idx]
        with open(pose_label_path, 'r') as file:
            pose_labels = [line for line in file.readlines()]
        for pose_label in pose_labels:
            pose_label_info = pose_label.split()
            class_id = 0 # 表示person
            x = pose_label_info[1]
            y = pose_label_info[2]
            w = pose_label_info[3]
            h = pose_label_info[4]
            
            with open(os.path.join(labels_dir, file_name), '+a') as file:
                data_str = f"{class_id} {x} {y} {w} {h}\n"
                file.write(data_str)
            
            
            
    

if __name__ == '__main__':
    labels_dir = os.path.join(data_folder_dir, 'labels')
    generate_labels(pose_labels_dir, labels_dir)