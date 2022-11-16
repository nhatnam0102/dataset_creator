from constants import *
from constants import (ROOT, LOGGER, ROOT1, SLASH, UNDERLINE, JPG, PNG, TXT, PACK,
                       PACK_UE, A1, A2, A3, A12, A23, A13, CASE, A123, TAN_TO_PACK, join, basename)
import csv


def all_file_and_subdir_from_dir(path_dir):
    file_list, dir_list = [], []
    for rdir, subdir, files in os.walk(path_dir):
        file_list.extend([join(rdir, f) for f in files])
        dir_list.extend([join(rdir, d) for d in subdir])
    return file_list, dir_list


def count_annotation(path_txt, file_classes_name, write_to_csv=False):
    annotation_dic = {}
    f_name = open(file_classes_name, 'r')
    d_name = f_name.readlines()
    f_name.close()
    names = []
    for d in d_name:
        names.append(d.rstrip('\n'))
    for txt in os.listdir(path_txt):
        if txt.endswith('txt'):
            txt_path = path_txt + SLASH + txt
            f1 = open(txt_path, 'r')
            data = f1.readlines()
            f1.close()
            for dt in data:
                cls, x, y, w, h = map(float, dt.split(' '))
                if cls not in annotation_dic.keys():
                    annotation_dic[int(cls)] = 1
                else:

                    annotation_dic[int(cls)] += 1

    for index, id_cls in enumerate(names):
        if index not in annotation_dic.keys():
            annotation_dic[index] = 0

    if write_to_csv:
        header = names
        data = []
        for k, v in sorted(annotation_dic.items()):
            data.append(v)

        with open('./data/test.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)


def rename_file_by_folder_name(path):
    for ID in os.listdir(path):
        f_ID = join(path,ID)
        for ID_GOC in os.listdir(f_ID):
            file = join(f_ID,ID_GOC)
            idx = 1
            for video in os.listdir(file):
                os.rename(join(file ,video), join(file, ID_GOC + '-' + str(idx) + video[video.rindex('.'):]))
                idx += 1


def change_file_extension(filename_path, old_ex, new_ex):
    num = len(old_ex)
    if filename_path[-num:] == old_ex:
        old = filename_path
        new = filename_path[:-num] + new_ex
        os.rename(old, new)


def mkdir_with_range(path_folder,min, max, angle_count, len_range):
    for i in range(min, max + 1, 1):
        path_f = path_folder + SLASH + str(i).rjust(len_range, '0')
        os.makedirs(path_f, exist_ok=True)
    for f in os.listdir(path_folder):
        for i in range(1, angle_count + 1, 1):
            folder_path = path_folder + SLASH + f + SLASH + f + '_0' + str(i)
            os.mkdir(folder_path)


def mkdir_with_angle(path_dir, angle_count):
    for f in os.listdir(path_dir):
        for i in range(1, angle_count, 1):
            folder_path = path_dir + SLASH + f + SLASH + f + '_0' + str(i)
            os.mkdir(folder_path)
