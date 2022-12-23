import os
import xml.etree.ElementTree as ET

zero = 0

path_to_datasets_for_warmup = str("C:\\Users\\misha\\Golf Ball\\Golf Ball\\Detection\\Annotations")  # path to stabil_11_14
path_to_save = str("C:\\Users\\misha\\Golf Ball\\Golf Ball\\Detection\\labels")
dir_of_videos_list = os.listdir(path_to_datasets_for_warmup)
for annotation_name in range(len(dir_of_videos_list)):
    tree = ET.parse(str(os.path.join(path_to_datasets_for_warmup, (dir_of_videos_list[annotation_name]))))
    root = tree.getroot()
    file_with_annotation = open(str(os.path.join(path_to_save, dir_of_videos_list[annotation_name].split(".")[0] + ".txt")), mode='a', encoding='utf-8')
    file_with_annotation.write(
        str(zero) + " " + str((float(root[4][4][0].text) + float(root[4][4][2].text)) / (2 * float(root[2][0].text)))
        + " " + str((float(root[4][4][1].text) + float(root[4][4][3].text)) / (2 * float(root[2][1].text)))
        + " " + str(((float(root[4][4][0].text) + float(root[4][4][2].text)) / 2 - float(root[4][4][0].text)) / float(
            root[2][0].text))
        + " " + str(((float(root[4][4][1].text) + float(root[4][4][3].text)) / 2 - float(root[4][4][1].text)) / float(
            root[2][1].text)))
    file_with_annotation.close()
