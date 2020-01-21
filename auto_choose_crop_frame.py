"""
extract frame and resize img size from record video  

"""
import cv2
import os
import argparse
import fnmatch
from tqdm import tqdm
import glog as log

VID_FORMAT = 'mp4'

def init_args():
    """
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video_dir', type=str, default='/zhihui/LDW/ldw_data/realCar_Fisheye', help='The read video path')
    parser.add_argument('-s', '--save_dir', type=str, default='/zhihui/LDW/ldw_data/realCar_Fish_frame', help='save choose frame to the path')

    return parser.parse_args()

def find_files(directory, pattern):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                file_list.append(filename)
    
    return file_list

def process_frame(frame, iou):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    img = frame[:iou[0],iou[1]:iou[2]]
    img_res = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_NEAREST)
    return img_res

def create_files(save_dir, vid_name):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    file_name = vid_name.split('/')[-1].split('.')[0]
    if not os.path.isdir(os.path.join(save_dir, file_name)):
        os.makedirs(os.path.join(save_dir, file_name))
    return file_name
         
def process_video(video_dir, save_dir):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    for sig_vid in tqdm(find_files(video_dir, '*.{}'.format(VID_FORMAT))):
        
        vc = cv2.VideoCapture(sig_vid) 
        width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        rig_bot_height, rig_bot_width = height // 2, width // 2

        if rig_bot_height == 540 and rig_bot_width == 960:
            # right bottom, r_h, l_w, r_w
            iou = [390, 90, 890]

        elif rig_bot_height == 720 and rig_bot_width == 1280:
            log.info('high resolution video, please confirm iou param')

        else:
            assert 'please confirm video resolution'

        count = 0
        cout_save = 0

        while vc:   
            rval, frame = vc.read()   

            if rval == True:
                count += 1
                # fisheye extract front preview
                ext_region = frame[rig_bot_height:, rig_bot_width:]
                cv2.imshow('ori frame', ext_region)

                key = cv2.waitKey(0) & 0xFF
                if key == ord('q'):
                    break

                elif key == ord('s'):          
                    # Interval 20 frame save 
                    if cout_save % 20 == 0 or cout_save > 20:          
                        file_name = create_files(save_dir, sig_vid)
                        img_res = process_frame(ext_region, iou)
                        cv2.imwrite(os.path.join(save_dir, file_name)+"/"+ file_name+"_{}.jpg".format(count),img_res)
                        cout_save = 0
                        log.info('successful save current frame {}'.format(count))

                    else:
                        cout_save += 1
                        continue
                    cout_save += 1

                else:
                    # skip current frame and cout pre save frame interval
                    if cout_save > 0:
                        cout_save += 1
                    continue

            else:
                break
        
        vc.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':

    # init args
    args = init_args()
    process_video(args.video_dir, args.save_dir)