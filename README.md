# Make_LDW_dataset
include choose frame, convert binary image, generate lanenet input data format

#### 制作数据 <br>
根据录制的视频帧，提取出合格的帧，并根据具体情况进行分辨率转换 <br>
```python auto choose_crop_frame.py -v input_video_dir -s extract_frame_dir```

将收集的合格数据，等分成n份 <br>
```python allocate_data.py -i input_sub_image_file -o out_file_dir -f total_image_path```

#### 转换数据格式 <br>
1. 根据labelme生成的 json，转二值化图 <br>
```python labelme_generate_binary.py json_dir -o save_binary_dir```

2. 在有image 和 binary的路径下执行，可生成包含train.txt, val.txt, test.txt及*.tfrecords <br>
```python lanenet_data_feed_pipline.py -i image_dir -o tf_save_dir```
