# YOLO object detection on KITTI dataset - vehicle orientation classification

This project provides instructions on how to setup YOLO to detect objects in the KITTI dataset. Moreover, the weights and configuration files can be used to detect the orientation of the vehicles in the images. 

predictions.jpg shows the output of the system for image 00032.jpg, which is also provided here.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

If you wish to label more images in the kitti dataset, use relabel.py. Converting from kitti to yolo notation is done with convert.py.
Generating anchors: gen_anchors.py.
Splitting the dataset and saving the test/train images to files: train_test.py.

### Prerequisites

You will need * [Darknet Framework](https://pjreddie.com/darknet/yolo/) to run this.
Dataset: http://www.cvlibs.net/datasets/kitti/eval_object.php


### Installing

Move the 'kitti.data' and 'kitti.cfg' files inside darknet/cfg folder.

'vehicle.names' file contains the names of the classes and should be placed in the darknet/data folder.

For testing purposes, move the two images provided here to darknet/.

Assuming you are currently in the darknet folder, the following command will run the system on image 000032.jpg:

The weights file is split into 4 smaller files. To generate it, run the following command in the repository's top folder:
```
cat weights/* > kitti.weights
```


```
./darknet detector test cfg/kitti.data cfg/kitti.cfg kitti.weights path/to/000032.jpg

```


## Acknowledgments

* [pjreddie](https://github.com/pjreddie/darknet/wiki/YOLO:-Real-Time-Object-Detection)
* [AlexeyAB](https://github.com/AlexeyAB/darknet#how-to-train-pascal-voc-data)