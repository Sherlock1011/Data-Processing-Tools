import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
from PIL import Image



def drawRoBBs(fr=None, ann_path=None, img_save=None, lab_save=None):
    '''Draws rotated bounding boxes to the corresponding image and returns the annotated image
    This function can be called in two separate ways. 
    
    Args:
    fr: RGB Image in uint8 format
    ann_dir: Path of the annotation file
    
    returns:
    anoted RGB image in uint8 format  
    '''
    fr_out = fr.copy()
    fr_out = np.array(fr_out)
    if os.path.exists(ann_path):
        objects = np.loadtxt(ann_path, dtype=str)
        print(len(objects), type(objects))
        f_txt = open(lab_save, 'w')
        for obj in objects:
            # print(objects, objects.dtype, type(obj), isinstance(obj, str))
            if isinstance(obj, str):
                print("====================================================")
                # print(isinstance(objects[0], list))  # <class 'numpy.ndarray'>
                f_txt = open(lab_save, 'w')
                print(objects[0], objects[1], objects[2], objects[3], objects[4], objects[5], objects[6], objects[7])
                # 写yolov8_obb格式的标签  不做特殊处理，直接处理成原始的输出格式
                x1,y1 = float(objects[0]),float(objects[1])
                x2,y2 = float(objects[2]),float(objects[3])
                x3,y3 = float(objects[4]),float(objects[5])
                x4,y4 = float(objects[6]),float(objects[7])
                
                print("111=======",x1, y1, x2, y2, x3, y3, x4, y4)
                
                # 计算中心点
                center_x = (x1 + x2 + x3 + x4) / 4
                center_y = (y1 + y2 + y3 + y4) / 4
                
                # 定义顶点列表，以便于操作
                vertices = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                
                # 找到中心点左侧且最上方的顶点作为新起始点
                new_start_point = min((p for p in vertices if p[0] < center_x), key=lambda p: p[1])

                # 确定新顺序
                # 找到新起始点在原列表中的索引
                start_index = vertices.index(new_start_point)
                # 从新起始点开始到列表结束，然后接上列表开头到新起始点前的部分
                reordered_vertices = vertices[start_index:] + vertices[:start_index]

                
                x1_new, y1_new = reordered_vertices[0]
                x2_new, y2_new = reordered_vertices[1]
                x3_new, y3_new = reordered_vertices[2]
                x4_new, y4_new = reordered_vertices[3]
                print("222=======",x1_new, y1_new, x2_new, y2_new, x3_new, y3_new, x4_new, y4_new)
                # 原有的顺序
                # f_txt.write("%s %s %s %s %s %s %s %s person 0\n" % (x1, y1, x2, y2, x3, y3, x4, y4))
                # 以中心点左边最上面的点为起始点
                f_txt.write("%s %s %s %s %s %s %s %s person 0\n" % (x1_new, y1_new, x2_new, y2_new, x3_new, y3_new, x4_new, y4_new))
                # 改变顺序后的contours
                contours = np.array([[int(x1_new), int(y1_new)], [int(x2_new), int(y2_new)], [int(x3_new), int(y3_new)], [int(x4_new), int(y4_new)]])
                cv2.polylines(fr_out, pts=[contours], color=(0, 0, 255), isClosed=True, thickness=3)
                
                # 为每个顶点画一个红色圆圈
                contours = contours.reshape((-1, 1, 2))
                radius = 3
                color = (0, 0, 255)
                thickness = 2
                for point in contours:
                    cv2.circle(fr_out, center=tuple(point.squeeze()), radius=radius, color=color, thickness=thickness)

                # 设置文本标签的属性
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                text_color = (255, 255, 255)
                text_thickness = 2
                
                # 在每个顶点旁边添加文本标签（0, 1, 2, 3）
                for i, point in enumerate(contours):
                    offset = 10
                    text_position = (point[0][0] + offset, point[0][1] + offset)
                    cv2.putText(fr_out, str(i), text_position, font, font_scale, text_color, text_thickness)
            
                f_txt.close()
                cv2.imwrite(filename=img_save, img=fr_out)
            else:
                f_txt = open(lab_save, 'a')
                # print(obj, obj.dtype, obj[0], obj[7])
                print("1111111111111", obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7])
                
                # 写yolov8_obb格式的标签  不做特殊处理，直接处理成原始的输出格式
                x1,y1 = float(obj[0]),float(obj[1])
                x2,y2 = float(obj[2]),float(obj[3])
                x3,y3 = float(obj[4]),float(obj[5])
                x4,y4 = float(obj[6]),float(obj[7])
                
                print("111=======",x1, y1, x2, y2, x3, y3, x4, y4)
                
                # 计算中心点
                center_x = (x1 + x2 + x3 + x4) / 4
                center_y = (y1 + y2 + y3 + y4) / 4
                
                # 定义顶点列表，以便于操作
                vertices = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                
                # 找到中心点左侧且最上方的顶点作为新起始点
                new_start_point = min((p for p in vertices if p[0] < center_x), key=lambda p: p[1])

                # 确定新顺序
                # 找到新起始点在原列表中的索引
                start_index = vertices.index(new_start_point)
                # 从新起始点开始到列表结束，然后接上列表开头到新起始点前的部分
                reordered_vertices = vertices[start_index:] + vertices[:start_index]

                
                x1_new, y1_new = reordered_vertices[0]
                x2_new, y2_new = reordered_vertices[1]
                x3_new, y3_new = reordered_vertices[2]
                x4_new, y4_new = reordered_vertices[3]
                print("222=======",x1_new, y1_new, x2_new, y2_new, x3_new, y3_new, x4_new, y4_new)
                # 原有的顺序
                # f_txt.write("%s %s %s %s %s %s %s %s person 0\n" % (x1, y1, x2, y2, x3, y3, x4, y4))
                # 以中心点左边最上面的点为起始点
                f_txt.write("%s %s %s %s %s %s %s %s person 0\n" % (x1_new, y1_new, x2_new, y2_new, x3_new, y3_new, x4_new, y4_new))
                # 改变顺序后的contours
                contours = np.array([[int(x1_new), int(y1_new)], [int(x2_new), int(y2_new)], [int(x3_new), int(y3_new)], [int(x4_new), int(y4_new)]])
                cv2.polylines(fr_out, pts=[contours], color=(0, 0, 255), isClosed=True, thickness=3)
                
                # 为每个顶点画一个红色圆圈
                contours = contours.reshape((-1, 1, 2))
                radius = 3
                color = (0, 0, 255)
                thickness = 2
                for point in contours:
                    cv2.circle(fr_out, center=tuple(point.squeeze()), radius=radius, color=color, thickness=thickness)

                # 设置文本标签的属性
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                text_color = (255, 255, 255)
                text_thickness = 2
                
                # 在每个顶点旁边添加文本标签（0, 1, 2, 3）
                for i, point in enumerate(contours):
                    offset = 10
                    text_position = (point[0][0] + offset, point[0][1] + offset)
                    cv2.putText(fr_out, str(i), text_position, font, font_scale, text_color, text_thickness)
            
            f_txt.close()
            cv2.imwrite(filename=img_save, img=fr_out)
    return fr_out

if __name__ == '__main__':   
    
    src_TXT_dir = r'/home/chenmiaomiao/datasets/fisheye/datasets/fish_collect_after/collect1/label/'  # xml源路径
    src_IMG_dir = r'/home/chenmiaomiao/datasets/fisheye/datasets/fish_collect_after/collect1/image/'  # IMG原路径
    IMG_format = '.jpg'    # IMG格式
    out_dir = '/home/chenmiaomiao/datasets/fisheye/datasets/fish_collect_after/collect1/out/'  # 输出路径
    out_label_dir = '/home/chenmiaomiao/datasets/fisheye/datasets/fish_collect_after/collect1/out_v8/'  # 标签输出路径


    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(out_label_dir):
        os.makedirs(out_label_dir)
    
    txt_file = os.listdir(src_TXT_dir)  # 只返回文件名称,带后缀

    for each_TXT in txt_file:  # 遍历所有xml文件

        # 读入IMG
        txt_FirstName = os.path.splitext(each_TXT)[0]
        img_save_file = os.path.join(out_dir, txt_FirstName+IMG_format)
        label_save_file = os.path.join(out_label_dir, each_TXT)
        img_src_path = os.path.join(src_IMG_dir, txt_FirstName+IMG_format)
        txt_src_path = os.path.join(src_TXT_dir, each_TXT)
        print(img_src_path)
        print(txt_src_path)


        fr = img_src_path
        ann_path = txt_src_path
        img_save = img_save_file
        lab_save = label_save_file

        img_in = Image.open(fr)
        drawRoBBs(img_in, ann_path, img_save, lab_save)
