import cv2
import numpy
import rand
import csv
import math
import sys
import os

sys.path.append('.')

imgFolder = 'image_2/'
labelFolder = 'label_2/'
outFolder = 'labels_orientation/'

'''
    Use WASD to select the orientation of the car with the bounding box.
    Press enter after choosing the correct orientation.
    Press 'R' to restart labeling the current car.
'''


def keys_to_label(keys):
    left = 97
    right = 100
    down = 115
    up = 119

    if left in keys and right in keys:
        return 'error'
    if up in keys and down in keys:
        return 'error'

    if left in keys and down in keys:
        return '225'
    if left in keys and up in keys:
        return '135'
    if right in keys and down in keys:
        return '315'
    if right in keys and up in keys:
        return '45'
    if left in keys:
        return '180'
    if right in keys:
        return '0'
    if up in keys:
        return '90'
    if down in keys:
        return '180'


def get_keys(img, imgName):
    cv2.namedWindow(imgName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(imgName,cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.putText(img,imgName,(20,20),cv2.FONT_HERSHEY_SIMPLEX,1,(23,232,89),2)
    keys = []
    key = -1
    while key is -1:
        cv2.imshow(imgName, img)
        key = cv2.waitKey(10)

    if key == 8:
        return ['back']
    if key == 10:
        return ['skip']
    if key == 27:
        return ['stop']
    if key == 114:
        return ['restart']

    keys.append(key)

    key = -1
    while key is -1:
        cv2.imshow(imgName, img)
        key = cv2.waitKey(10)
        if key == keys[0]:
            key = -1

    if key == 8:
        return ['back']
    if key == 27:
        return ['stop']
    if key == 114:
        return ['restart']
    if key == 10:
        return keys

    keys.append(key)

    key = -1
    while key is -1:
        cv2.imshow(imgName, img)
        key = cv2.waitKey(10)

    if key == 8:
        return ['back']
    if key == 114:
        return ['restart']
    if key == 10:
        return keys
    else:
        return ['restart']


def save_labels(BBs, name):
    out_file = open(outFolder+name,'w')
    for box in BBs:
        if box:
            out_file.write(box[0] + " " + " ".join([str(x) for x in box[1:]]) + "\n")

    out_file.close()


def relabel(imgFile,label):
    img = cv2.imread(imgFolder + imgFile)

    with open(labelFolder + label) as f:
        reader = csv.reader(f)
        l = []
        for row in reader:
            label = row[0].split()[0]
            l.append([label]+[int(float(x)) for x in row[0].split()[4:8]])

        f.close()

    l = [label for label in l if label[0] in ['Car', 'Truck', 'Van','Tram']]
    new_labels = []
    i = 0
    while i < len(l):
        box = l[i]
        tmp = img.copy()

        cv2.rectangle(tmp, (box[1],box[2]),(box[3],box[4]),(255,0,255))

        keys = get_keys(tmp,imgFile)

        if 'skip' in keys:
        	new_labels.append([])
        	i += 1
        	continue
        if 'stop' in keys:
            cv2.destroyAllWindows()
            return ['stop']
        if 'restart' in keys:
            print('restarting')
            continue
        if 'back' in keys:
            print('back')
            if i == 0:
                cv2.destroyAllWindows()
                return ['back']
            else:
                i -= 1
                if new_labels:
                    del new_labels[-1]
                continue

        label = keys_to_label(keys)
        if label == 'error':
            print("ERROR!!")
            print([chr(k) for k in keys])
            continue

        new_labels.append([box[0]+'_'+label]+box[1:5])
        i += 1

    cv2.destroyAllWindows()

    return new_labels


def contains_vehicle(label):
    with open(labelFolder + label) as f:
        reader = csv.reader(f)
        l = []
        for row in reader:
            label = row[0].split()[0]
            l.append(label)

        f.close()

    for label in ['Car', 'Truck', 'Van', 'Tram']:
        if label in l:
            return True

    return False


if __name__ == '__main__':

    tmp_images = sorted(os.listdir(imgFolder))
    images = sorted([im for im in os.listdir(imgFolder) if im.endswith('.jpg')])
    labels = sorted(os.listdir(labelFolder))

    bak = open('last_image.bak')
    last_img = bak.readline()
    if last_img == '':
        i = 0
    else:
        i = images.index(last_img)

    while i < len(images):
        new_labels = relabel(images[i],labels[i])
        print(new_labels)
        if new_labels:
            if 'stop' in new_labels:
                backup = open('last_image.bak','w')
                backup.write(images[i])
                break
            elif 'back' in new_labels:
                if i != 0:
                    i -= 1
                    while not contains_vehicle(labels[i]):
                        i -= 1
                    continue
            else:
                save_labels(new_labels,labels[i])
        i += 1

    if i == len(images):
	    print("FINALLYYY!!!!!")
