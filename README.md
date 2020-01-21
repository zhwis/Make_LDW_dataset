# Make_LDW_dataset
include choose frame, convert binary image, generate lanenet input data format

#### extract frame and resize img size from real record video
>> 根据录制的视频帧，提取出合格的帧，并根据具体情况进行分辨率转换
```python auto choose_crop_frame.py -v input_video_dir -s extract_frame_dir```

#### Split gt_image data into n copies
```python allocate_data.py -i input_sub_image_file -o out_file_dir -f total_image_path```

#### use .json file gennerate binary image
>> 根据labelme生成的 json，转二值化图
```python labelme_generate_binary.py json_dir -o save_binary_dir```

### use gt_image and gt_image_binary, splite training dataset(incude *.txt, tfrecord)
>> 在有image 和 binary的路径下执行，可生成包含train.txt, val.txt, test.txt及*.tfrecords
```python lanenet_data_feed_pipline.py -i image_dir -o tf_save_dir```
