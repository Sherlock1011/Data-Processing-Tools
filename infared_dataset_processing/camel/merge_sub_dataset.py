import os
import shutil
from pathlib import Path
def merge_sub_datasets(source_dir, target_dir):
    images_dir = Path(target_dir) / 'images'
    labels_dir = Path(target_dir) / 'labels'
    
    # 创建目标目录中的images和labels文件夹
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    count = 1 # 开始的文件编号
    
    # 遍历指定目录下的所有子目录
    for sub_dir in Path(source_dir).iterdir():
        # 检查images和labels文件夹是否存在
        sub_images_dir = sub_dir / 'images'
        sub_labels_dir = sub_dir / 'labels'
        if sub_images_dir.exists() and sub_labels_dir.exists():
            images_files = sorted(sub_images_dir.iterdir())
            labels_files = sorted(sub_labels_dir.iterdir())
            
            # 使用zip确保images和labels的数量和顺序一一对应
            for image_file, label_file in zip(images_files, labels_files):
                if image_file.is_file() and label_file.is_file():
                    image_new_name = f"{count:06}.jpg"
                    label_new_name = f"{count:06}.txt"
                    
                    shutil.copy(image_file, images_dir / image_new_name)
                    shutil.copy(label_file, labels_dir / label_new_name)
                    
                    count += 1
        print(f"{sub_dir.name}已完成")         
        
        
if __name__ == '__main__':
    source_dir = '/home/yangzeyu/dataset/infrared/CAMEL/sub'
    target_dir = '//home/yangzeyu/dataset/infrared/CAMEL/datasets'
    merge_sub_datasets(source_dir, target_dir)