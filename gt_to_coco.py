import os
import numpy as np
import cv2
from pathlib import Path
import shutil

path_to_datasets_for_warmup = str("C:\\Users\\misha\\golfTrajectory\\stabil_11_14_1\\stabil_11_14")  # path to stabil_11_14
dir_of_videos_list = os.listdir(path_to_datasets_for_warmup)
for dir_name in range(len(dir_of_videos_list)):
    img_list = os.listdir(os.path.join(path_to_datasets_for_warmup, dir_of_videos_list[dir_name]))  # opt.source
    path_to_ground_truth_file = os.path.join(path_to_datasets_for_warmup, os.path.join(dir_of_videos_list[dir_name], "groundtruth.txt"))
    im_file = os.path.join(path_to_datasets_for_warmup, os.path.join(dir_of_videos_list[dir_name],
                           img_list[1])) # opt.source
    im_in = np.array(cv2.imread(im_file))
    file = open(path_to_ground_truth_file, mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    coordinates_from_ground_truth_file = np.empty((len(lines), 4), dtype="float32")
    for i in range(len(lines)):
        for j in range(4):
            if j == 0:  # center_x
                coordinates_from_ground_truth_file[i][j] = (float(lines[i].split(",")[0]) + float(lines[i].split(",")[0])
                                                           + float(lines[i].split(",")[2])) / (2 * im_in.shape[1])
            elif j == 1:  # center_y
                coordinates_from_ground_truth_file[i][j] = (float(lines[i].split(",")[1]) + float(lines[i].split(",")[1])
                                                           + float(lines[i].split(",")[3])) / (2 * im_in.shape[0])
            elif j == 2:  # width
                coordinates_from_ground_truth_file[i][j] = ((float(lines[i].split(",")[0]) + float(lines[i].split(",")[0])
                                                            + float(lines[i].split(",")[2])) / 2 -
                                                           float(lines[i].split(",")[0])) / im_in.shape[1]
            else:  # height
                coordinates_from_ground_truth_file[i][j] = ((float(lines[i].split(",")[1]) + float(lines[i].split(",")[1])
                                                           + float(lines[i].split(",")[3])) / 2 -
                                                           float(lines[i].split(",")[1])) / im_in.shape[0]
    file.close()

    zero = 0

    for i in range(len(img_list)-2):
        image = os.path.join(path_to_datasets_for_warmup, os.path.join(dir_of_videos_list[dir_name],
                                                                     img_list[i]))
        path_dir = Path(dir_of_videos_list[dir_name])
        path_img = Path(img_list[i])
        destination_path_for_img = os.path.join("C:\\Users\\misha\\golfTrajectory\\stabil_11_14_1\\images",
                                        str(path_dir.stem.split(".")[0]) + "_" + str(img_list[i]))
        shutil.move(image, destination_path_for_img)

        file_with_annotation = open(os.path.join("C:\\Users\\misha\\golfTrajectory\\stabil_11_14_1\\annotations",
                                str(path_dir.stem.split(".")[0]) + "_" + str(path_img.stem) + ".txt"),
                                mode='a', encoding='utf-8')
        file_with_annotation.write(str(
        str(zero) + str(" ") + str(coordinates_from_ground_truth_file[i][0]) + str(" ") +
        str(coordinates_from_ground_truth_file[i][1]) + str(" ") + str(coordinates_from_ground_truth_file[i][2]) +
        str(" ") + str(coordinates_from_ground_truth_file[i][3])).replace('\п»ї', ''))
        file_with_annotation.close()
