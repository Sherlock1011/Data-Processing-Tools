# 数据预处理工具
## 1. 划分数据集
split_dataset/split_dataset.py

将制定文件夹下的数据按照一定比例划分为训练集和验证集，并保存到指定文件夹下。

`函数名称：split_dataset`

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

## 2. DOTA格式转换为Yolo格式
dota2yolo/Collect2yolov8obb.py

将DOTA格式的数据进行调整并转换为Yolo格式

+ **将标注工具生成的DOTA格式的角度进行调整**

![](https://cdn.nlark.com/yuque/0/2024/png/25936110/1725864908898-d395acb8-4033-4b2c-bcec-c67c30f6a977.png)

如上图，转换的思路：通过boxes的中心点作坐标轴，将左上角的点作为0点，顺时针调整点的顺序。

`函数名称：drawRoBBs`

## 3. Video转换为帧
video2frame/video2frame.py

将视频数据切为帧图片数据
