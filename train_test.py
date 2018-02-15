import os, random

extension = '.jpg'
image_folder = 'vehicle_img/'

files = [f for f in os.listdir(image_folder) if f.endswith(extension)]

wd = os.getcwd()

train_file = open("vehicle_train.txt", 'w')
test_file = open("vehicle_test.txt", 'w')

image_number = len(files)
percent = 0.8


trainFiles = random.sample(files, int(image_number * percent))
testFiles = [f for f in files if f not in trainFiles]

if __name__ == '__main__':
    for file in sorted(trainFiles):
        train_file.write(wd + '/' + image_folder + file + '\n')
    for file in sorted(testFiles):
        test_file.write(wd + '/' + image_folder + file + '\n')