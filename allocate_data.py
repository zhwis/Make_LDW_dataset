"""
allocate data to someone
"""
import cv2
import os
import argparse
from tqdm import tqdm
import glog as log
import shutil
import math
import  random

from auto_choose_crop_frame import find_files

IMG_FORMAT = 'jpg'

def init_args():
    """
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', type=str, default='/zhihui/LDW/ldw_data/realCar_Fish_frame', help='The read video path')
    parser.add_argument('-o', '--output_dir', type=str, default='/zhihui/LDW/ldw_data/realCar_Fish_frame_alloc', help='save choose frame to the path')
    parser.add_argument('-f', '--file_name', type=str, default='gt_image', help='save choose frame to the path')

    return parser.parse_args()

def copy_alldata2target(input_dir, output_dir, file_name):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    if not os.path.isdir(os.path.join(output_dir, file_name)):
        os.makedirs(os.path.join(output_dir, file_name))
    for img_dex in tqdm(find_files(input_dir, '*.{}'.format(IMG_FORMAT))):
        shutil.copy(img_dex, os.path.join(output_dir, file_name))
    log.info('copy all data to Image complete')

def random_alloc(output_dir, file_name):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    imgPath = os.listdir(os.path.join(output_dir, file_name))
    random.shuffle(imgPath)
    length = len(imgPath)
    num = 19
    for i in range(num):
        if not os.path.isdir(os.path.join(output_dir, str(i))):
            os.makedirs(os.path.join(output_dir, str(i)))  
        target_file = imgPath[math.floor(i / num * length):math.floor((i + 1) / num * length)] 
        for pic in target_file:              
            shutil.copy(os.path.join(output_dir, file_name+'/'+pic), os.path.join(output_dir, str(i)+'/')) 
    log.info('allocate data to subfile complete')

if __name__ == '__main__':

    # init args
    args = init_args()
    copy_alldata2target(args.input_dir, args.output_dir, args.file_name)
    random_alloc(args.output_dir, args.file_name)