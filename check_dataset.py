#A datachecking and cleaning pipeline for object detection tasks that supports the YOLOv5 annotation format

# images and corresponding labels are assumed to exit in one dir. i.e dataset_path
# and images missing labels and any labels missing images will be moved to corresponding folders, i.e img_move_path and txt_move_path
# it is assumed that img_move_path and txt_move_path will exist beforehand

# do not pass the txt_move_path if you want to place the moved images and txts into the same folder

import os
import argparse
from tqdm import tqdm
import shutil

img_formats = ('.bmp', '.dng', '.jpeg', '.jpg', '.mpo', '.png', '.tif', '.tiff', '.webp', '.pfm')

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dataset_path', type=str, required=True, help='Absolute path to folder containing all the dataset')
parser.add_argument('-i', '--img_move_path', type=str, required=True, help='Absolute path to folder where the images will be moved')
parser.add_argument('-t', '--txt_move_path', type=str, help='Absolute path to folder where the labels will be moved')

args = parser.parse_args()
img_move_dir = args.img_move_path
txt_move_dir = args.txt_move_path

if not txt_move_dir:
    txt_move_dir = img_move_dir

dirr = args.dataset_path

list_dir = os.listdir(dirr)

img_with_no_txt = 0
img_with_txt = 0
img_with_no_txt_moved = 0

txt_with_no_img = 0
txt_with_img = 0
txt_with_no_img_moved = 0

for file_path in tqdm(list_dir):
    if file_path.lower().endswith(img_formats):
        file_name_wo_ext = os.path.splitext(file_path)[0]
        label_path = file_name_wo_ext + ".txt"
        if os.path.isfile(dirr+"/"+label_path): 
            img_with_txt +=1
        else:
            shutil.move(dirr+"/"+file_path, img_move_dir+"/"+file_path)
            img_with_no_txt_moved += 1
            img_with_no_txt+=1

    elif file_path.lower().endswith(".txt"):
        file_name_wo_ext = os.path.splitext(file_path)[0]
        img_paths = [file_name_wo_ext + ext for ext in img_formats]
        exists = [os.path.isfile(dirr+"/"+img_path) for img_path in img_paths]
        if any(exists):
            txt_with_img += 1
        else:
            shutil.move(dirr+"/"+file_path, txt_move_dir+"/"+file_path)
            txt_with_no_img += 1
            txt_with_no_img_moved += 1

    else:
        print(os.path.splitext(file_path))



print("img_with_txt:  ",img_with_txt)
print("txt_with_img:  ",txt_with_img)
if img_with_txt != txt_with_img:
    print("*****img_with_txt != txt_with_img \n *****Something is Wrong, please check")

print("img_with_no_txt:  ",img_with_no_txt)
print("txt_with_no_img:  ",txt_with_no_img)

print("img_with_no_txt_moved:  ",img_with_no_txt_moved)
print("txt_with_no_img_moved:  ",txt_with_no_img_moved)