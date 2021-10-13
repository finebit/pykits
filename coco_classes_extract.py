# -*- coding: utf-8 -*-
# test.py
# Author: FineBit
import argparse
import os
import re
import shutil


# 给定文件夹，返回存在指定类别的文件名
def get_class_exist_path(l_path, c: list):
    result = []
    for root, dirs, files in os.walk(l_path):
        total = len(files)
        for i, file in enumerate(files):
            f_path = os.path.join(root, file)
            with open(f_path) as f:
                for line in f.readlines():
                    items = re.split(r"[ ]+", line)
                    if items[0] in c:
                        result.append(file)
                        break
            print("check class: %d/%d" % (i + 1, total))
        return result


def copy_txt_files(l_path, e_fs, dst_d_path):
    total = len(e_fs)
    for i, e_f in enumerate(e_fs):
        src = os.path.join(l_path, e_f)
        dst = os.path.join(dst_d_path, e_f)
        shutil.copy(src, dst)
        print("copy txt: %d/%d" % (i+1, total))


def delete_other_class(dst_l_path, c: list, renumber: bool):
    cls_num = []
    for root, dirs, files in os.walk(dst_l_path):
        total = len(files)
        for i, file in enumerate(files):
            f_path = os.path.join(dst_l_path, file)
            with open(f_path, 'r') as f:
                lines = f.readlines()
            with open(f_path, 'w') as f_w:
                for line in lines:
                    items = re.split(r"[ ]+", line)
                    if items[0] in c:
                        if not (items[0] in cls_num):
                            cls_num.append(items[0])
                        if renumber:
                            items[0] = str(cls_num.index(items[0]))
                            line = " ".join(items)
                        f_w.write(line)
            print("delete other class: %d/%d" % (i + 1, total))


def copy_images(img_dir, dst_img_dir, dst_l_path):
    for root, dirs, files in os.walk(dst_l_path):
        total = len(files)
        for i, file in enumerate(files):
            image_file = os.path.splitext(file)[0] + ".jpg"  # txt后缀替换为jpg
            src = os.path.join(img_dir, image_file)
            dst = os.path.join(dst_img_dir, image_file)
            shutil.copy(src, dst)
            print("copy images: %d/%d" % (i+1, total))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("source dir, destination dir, classes list")
    parser.add_argument('-s', "--src", dest="src_root", default="./coco_yolo/",
                        help="source root dir of coco_yolo labels and images")
    parser.add_argument('-d', "--dst", dest="dst_root", default="./coco_yolo_extract/",
                        help="destination root dir")
    parser.add_argument('-c', "--classes", dest="dst_classes", default=['0'], nargs='+',
                        help="input the classes you wanna extract, for example: --classes 0 1 2")
    parser.add_argument('-r', "--renumber", action="store_true", help="renumber the class number")
    arg = parser.parse_args()

    for item in ["train", "val"]:
        labels_path = os.path.join(arg.src_root, "labels/"+item+"2017")  # 源标签目录
        print(labels_path)
        images_dir = os.path.join(arg.src_root, "images/"+item+"2017")  # "images/train2017"  # 源图片目录
        dest_labels_path = os.path.join(arg.dst_root, "labels/"+item+"2017")  # 目标标签目录
        if not os.path.exists(dest_labels_path):
            os.makedirs(dest_labels_path)
        dest_images_dir = os.path.join(arg.dst_root, "images/"+item+"2017")  # 目标图片目录
        if not os.path.exists(dest_images_dir):
            os.makedirs(dest_images_dir)
        dest_classes = arg.dst_classes  # 要提取的类的序号
        print(dest_classes)

        # 第一步：将含有指定class的txt文件复制到指定目录
        e_files = get_class_exist_path(labels_path, dest_classes)  # 返回txt文件列表
        copy_txt_files(labels_path, e_files, dest_labels_path)

        # 第二步：删除移动后的txt中，不需要的class
        delete_other_class(dest_labels_path, dest_classes, arg.renumber)

        # 第三步：将含有指定class的images复制到指定目录
        copy_images(images_dir, dest_images_dir, dest_labels_path)
