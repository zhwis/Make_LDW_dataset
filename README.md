# Make_LDW_dataset
include choose frame, convert binary image, generate lanenet input data format

### extract frame and resize img size from real record video
python auto choose_crop_frame.py -v input_video_dir -s extract_frame_dir

### Split gt_image data into n copies
python allocate_data.py -i input_sub_image_file -o out_file_dir -f total_image_path

### use .json file gennerate binary image
python labelme_generate_binary.py json_dir -o save_binary_dir

### use gt_image and gt_image_binary, splite training dataset(incude *.txt, tfrecord)
python lanenet_data_feed_pipline.py -i image_dir -o tf_save_dir
