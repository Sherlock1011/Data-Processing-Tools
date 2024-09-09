import os
import shutil
import random
from tqdm import tqdm

def get_files_recursive(root_dir):
    """
    递归获取所有文件的完整路径。
    Args:
        root_dir (str): 根目录路径。
    Returns:
        list of str: 包含所有文件完整路径的列表。
    """
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def split_dataset(images_dir, labels_dir, output_dir, train_ratio=0.8):
    """
    按照一定比例将数据集划分为训练集和验证集，并显示进度条。
    Args:
        images_dir (str): 源图片路径
        labels_dir (str): 源标签路径
        output_dir (str): 划分结果保存路径
        train_ratio (float, optional): 训练集比例. Defaults to 0.8.
    """
    # 定义路径
    train_images_dir = os.path.join(output_dir, 'images/train')
    val_images_dir = os.path.join(output_dir, 'images/val')
    train_labels_dir = os.path.join(output_dir, 'labels/train')
    val_labels_dir = os.path.join(output_dir, 'labels/val')

    # 创建训练和验证目录
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)

    # 获取所有文件
    images_files = get_files_recursive(images_dir)
    labels_files = get_files_recursive(labels_dir)

    # 将文件进行排序确保文件一一对应
    images_files.sort()
    labels_files.sort()

    # 确保文件数目一致
    assert len(images_files) == len(labels_files), "文件数量不一致"

    # 将数据集打乱
    data_pairs = list(zip(images_files, labels_files))
    random.shuffle(data_pairs)

    # 根据比例划分训练集和验证集
    train_size = int(len(data_pairs) * train_ratio)
    train_data = data_pairs[:train_size]
    val_data = data_pairs[train_size:]

    # 复制文件到训练和验证目录
    for image_file, label_file in tqdm(train_data, desc='训练数据进度'):
        shutil.copy(image_file, os.path.join(train_images_dir, os.path.basename(image_file)))
        shutil.copy(label_file, os.path.join(train_labels_dir, os.path.basename(label_file)))

    for image_file, label_file in tqdm(val_data, desc='验证数据进度'):
        shutil.copy(image_file, os.path.join(val_images_dir, os.path.basename(image_file)))
        shutil.copy(label_file, os.path.join(val_labels_dir, os.path.basename(label_file)))

    print("数据集划分完成，训练集和验证集已保存至：", output_dir)

if __name__ == '__main__':
    images_dir = '/home/yangzeyu/dataset/fish/obb/original/web_data/images'
    labels_dir = '/home/yangzeyu/dataset/fish/obb/original/web_data/labels_v8_2'
    output_dir = '/home/yangzeyu/dataset/fish/obb/train/web'
    
    split_dataset(images_dir, labels_dir, output_dir)
