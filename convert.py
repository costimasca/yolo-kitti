import csv
import sys
import os
import cv2

sys.path.append('.')

imgFolder = 'vehicle_img/'
labelFolder = 'labels_orientation/'
labelsOutput = 'vehicle_labels/'


#classes = ['Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc', 'DontCare']
classes = ['vehicle_0','vehicle_45','vehicle_90','vehicle_135','vehicle_180','vehicle_225','vehicle_270','vehicle_315',]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)


def convert_annotation(imgFile, label):
    img = cv2.imread(imgFolder + imgFile)
    h = int(img.shape[0])
    w = int(img.shape[1])

    in_file = open(labelFolder + label)
    out_file = open(labelsOutput + label,'w')

    reader = csv.reader(in_file)
    l = []
    for row in reader:

        l.append([row[0].split()[0]]+[int(float(x)) for x in row[0].split()[1:]])

    lines = []
    for b in l:
        cls = b[0].split('_')
        new_cls = 'vehicle_'+cls[1]
        lines.append([new_cls]+b[1:])


    in_file.close()

    for box in lines:
        cls_id = classes.index(box[0])
        b = [box[1], box[3], box[2], box[4]]
        bb = convert((w, h), b)

        out_file.write(str(cls_id) + " " + " ".join([str(x) for x in bb]) + "\n")

    out_file.close()


if __name__ == '__main__':
    images = sorted(os.listdir(imgFolder))
    images = [f for f in images if f.endswith('jpg')]
    labels = sorted(os.listdir(labelFolder))
    labels = [f for f in labels if f.endswith('txt')]

    print(len(labels))
    print(len(images))
    for i in range(len(labels)):
        convert_annotation(images[i],labels[i])
