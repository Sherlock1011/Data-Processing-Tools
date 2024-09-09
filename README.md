# 划分数据集
将制定文件夹下的数据按照一定比例划分为训练集和验证集，并保存到指定文件夹下。

`split_dataset`

| **参数名称** | **参数介绍** |
| :---: | --- |
| **images_dir** | str 源图片路径 |
| **labels_dir** | str源标签路径 |
| **output_dir** | str 划分结果保存路径 |
| **train_ratio** | flot 训练集比例。默认值为0.8 |


用例

```plain
images_dir = '/path/to/dataset/images_dir'
labels_dir = '/path/to/dataset/labels_dir'
output_dir = '/path/to/dataset/output_dir'
    
split_dataset(images_dir, labels_dir, output_dir)
```
