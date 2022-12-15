import os
import numpy as np
import cv2


path_to_datasets_for_warmup = str("C:\\Users\\misha\\golf-trajectory_project\\stabil_11_14\\stabil_11_14")  # path to stabil_11_14
dir_of_videos_list = os.listdir(path_to_datasets_for_warmup)
for dir_name in range(len(dir_of_videos_list)):
    img_list = os.listdir(path_to_datasets_for_warmup + r"\\" + dir_of_videos_list[dir_name])  # opt.source
    path_to_groundtruth_file = os.path.join(path_to_datasets_for_warmup + r"\\", dir_of_videos_list[dir_name] +
                                            r"\\" + "groundtruth.txt")
    im_file = os.path.join(path_to_datasets_for_warmup + r"\\" + dir_of_videos_list[dir_name],
                           img_list[1])  # opt.source
    im_in = np.array(cv2.imread(im_file))
    file = open(path_to_groundtruth_file, mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    coordinates_from_ground_truth_file = np.empty((len(lines), 4), dtype="float64")
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
    file_1 = open(path_to_groundtruth_file, mode='w', encoding='utf-8-sig')
    for i in range(len(coordinates_from_ground_truth_file)):
        file_1.write("0 ")
        for j in range(4):
            file_1.write(str(coordinates_from_ground_truth_file[i][j]) + " ")
        file_1.write("\n")
    file_1.close()
