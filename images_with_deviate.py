import os
import numpy as np
import cv2
from pathlib import Path
from numpy import random
from PIL import ImageOps, Image
from operator import add



class FixedMotionImage:
    def __init__(self, size, augmentation=True, channels=3, offsets=None):
        self.size = size
        self.augmentation = augmentation
        self.buffer = []
        self.diff = None
        self.channels = channels
        self.offsets = offsets
        self.frame_num = 0

    def on_frame(self, image_pil: Image, box) -> (np.array, float, bool, np.array):
        if self.channels == 3:
            image_np = np.array(ImageOps.grayscale(image_pil))
        else:
            image_np = np.array(image_pil)
        self.buffer.append(image_np)
        if len(self.buffer) == 3:
            try:
                diff2 = np.abs(self.buffer[2] - self.buffer[1])
                if self.diff is not None:
                    diff1 = self.diff
                else:
                    diff1 = np.abs(self.buffer[1] - self.buffer[0])
                if self.channels == 3:
                    result_image_np = np.stack((diff2, self.buffer[1], diff1), axis=2)
                else:
                    result_image_np = np.concatenate((diff2, self.buffer[1], diff1), axis=2)
                im, offset = self.crop_image(result_image_np, box)
                self.frame_num += 1
                self.buffer.pop(0)
                self.diff = diff2
                im_pil = Image.fromarray(im)
                return im_pil, 1.0, False, offset
            except ValueError as e:
                print(self.buffer[0].shape, self.buffer[1].shape, self.buffer[2].shape)
                raise e
        return None

    def crop_image(self, im, box):
        margin = int(self.size / 2)
        h, w, _ = im.shape

        if self.offsets is not None:
            offset = self.offsets[self.frame_num]

            if len(offset) != 2:
                print('bad offset found', offset)
                offset = (0, 0)
        else:
            center = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
            center_deviation = self.deviate(center, w, h)
            pos = list(map(lambda a, b: int(add(a, b)), center, center_deviation))
            offset = (max(0, pos[0] - margin), max(0, pos[1] - margin))

        left, top = offset
        right = left + 2 * margin
        bottom = top + 2 * margin
        right_diff = w - right
        if right_diff < 0:
            right += right_diff
            left += right_diff

        bottom_diff = h - bottom
        if bottom_diff < 0:
            bottom += bottom_diff
            top += bottom_diff

        offset = (left, top)
        cropped = im[top:bottom, left:right]
        return cropped, offset

    def deviate(self, center, w, h):
        if not self.augmentation:
            return [0, 0]

        max_shift = self.size / 2 - 50
        max_left = int(min(center[0], max_shift))
        max_right = int(min(w - center[0], max_shift))
        offset_x = random.randint(-max_left, max_right)
        max_up = int(min(center[1], max_shift))
        max_down = int(min(h - center[1], max_shift))
        offset_y = random.randint(-max_up, max_down)
        return [offset_x, offset_y]

path_to_datasets_for_warmup = str("C:\\Users\\misha\\golf-trajectory_project\\test_data\\stabil_11_14")  # path to stabil_11_14
dir_of_videos_list = os.listdir(path_to_datasets_for_warmup)
for dir_name in range(len(dir_of_videos_list)):
    img_list = os.listdir(os.path.join(path_to_datasets_for_warmup, dir_of_videos_list[dir_name]))  # opt.source
    path_to_ground_truth_file = os.path.join(path_to_datasets_for_warmup, os.path.join(dir_of_videos_list[dir_name], "groundtruth.txt"))
    im_file = os.path.join(path_to_datasets_for_warmup, os.path.join(dir_of_videos_list[dir_name],
                           img_list[1])) # opt.source
    im_in = np.array(cv2.imread(im_file))
    file = open(path_to_ground_truth_file, mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    coordinates_from_ground_trth_file_for_cutting = np.empty((len(lines), 4), dtype="float64")
    for i in range(len(lines)):
        for j in range(4):
            if j == 0:  # left top x
                coordinates_from_ground_trth_file_for_cutting[i][j] = float(lines[i].split(",")[0])
            elif j == 1:  # left top y
                coordinates_from_ground_trth_file_for_cutting[i][j] = float(lines[i].split(",")[1])
            elif j == 2:  # right bottom x
                coordinates_from_ground_trth_file_for_cutting[i][j] = float(lines[i].split(",")[0]) + float(
                    lines[i].split(",")[2])
            else:  # right bottom y
                coordinates_from_ground_trth_file_for_cutting[i][j] = float(lines[i].split(",")[1]) + float(
                    lines[i].split(",")[3])

    file.close()
    zero = 0
    size_of_cutting = 640

    for i in range(len(img_list)-2):

        image = os.path.join(path_to_datasets_for_warmup, os.path.join(dir_of_videos_list[dir_name],
                                                                     img_list[i]))
        im_in = np.array(cv2.imread(image))
        path_dir = Path(dir_of_videos_list[dir_name])
        path_img = Path(img_list[i])
        destination_path_for_img = os.path.join("C:\\Users\\misha\\golf-trajectory_project\\test_data\\images",
                                        str(path_dir.stem.split(".")[0]) + "_" + str(img_list[i]))
        object = FixedMotionImage(size_of_cutting)
        new_img, offset = object.crop_image(im=im_in, box=[coordinates_from_ground_trth_file_for_cutting[i][0],
                                                      coordinates_from_ground_trth_file_for_cutting[i][1],
                                                      coordinates_from_ground_trth_file_for_cutting[i][2],
                                                      coordinates_from_ground_trth_file_for_cutting[i][3]])
        cv2.imwrite(destination_path_for_img, new_img)

        file_with_annotation = open(os.path.join("C:\\Users\\misha\\golf-trajectory_project\\test_data\\annotations",
                                str(path_dir.stem.split(".")[0]) + "_" + str(path_img.stem) + ".txt"),
                                mode='a', encoding='utf-8')
        file_with_annotation.write(str(
            str(zero) + str(" ") + str((coordinates_from_ground_trth_file_for_cutting[i][0] +
            coordinates_from_ground_trth_file_for_cutting[i][2] - 2*offset[0]) / (2*size_of_cutting)) + str(" ") +
            str((coordinates_from_ground_trth_file_for_cutting[i][1] + coordinates_from_ground_trth_file_for_cutting[i][3]
            - 2*offset[1]) / (2*size_of_cutting)) + str(" ") + str(((coordinates_from_ground_trth_file_for_cutting[i][0] +
            coordinates_from_ground_trth_file_for_cutting[i][2]) / 2 -
            coordinates_from_ground_trth_file_for_cutting[i][0]) / size_of_cutting) + str(" ") +
            str(((coordinates_from_ground_trth_file_for_cutting[i][1] +
            coordinates_from_ground_trth_file_for_cutting[i][3]) / 2 -
            coordinates_from_ground_trth_file_for_cutting[i][1]) / size_of_cutting)).replace('\п»ї', ''))
        file_with_annotation.close()
