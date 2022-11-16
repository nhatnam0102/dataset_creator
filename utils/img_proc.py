import os
from constants import *
import re
import shutil
import cv2
import random
import numpy as np
import utils.file_proc
from rembg import remove
import os
from PIL import Image
import utils.common
from utils import file_proc
from constants import (ROOT, LOGGER, ROOT1, SLASH, UNDERLINE, JPG, PNG, TXT, PACK,
                       PACK_UE, A1, A2, A3, A12, A23, A13, CASE, A123, TAN_TO_PACK, join, NUM, basename)


def id_product(file):
    return file.split('_')[0]


def camera_angle(file):
    return file.split('-')[0]


def name_no_ext(file):
    return file[:-4]


def resize_contract(path, save,resize1=0.6, resize2=0.3, plus=0.8, minus=1.3):  # For case
    f, _ = file_proc.all_file_and_subdir_from_dir(path)
    if resize1>0:
        for im in f:
            img = cv2.imread(im, cv2.IMREAD_UNCHANGED)
            img_rs1, img_rs2 = cv2.resize(img, (0, 0), fx=resize1, fy=resize1), cv2.resize(img, (0, 0), fx=resize2,
                                                                                           fy=resize2)
            cv2.imwrite(join(save, basename(im)[:-4]+f"-{resize1}{PNG}"), img_rs1)
            cv2.imwrite(join(save, basename(im)[:-4]+f"-{resize2}{PNG}"), img_rs2)
    f1, _ = file_proc.all_file_and_subdir_from_dir(save)
    alpha = 1.5

    if plus>0:
        for im in f1:
            img = cv2.imread(im, cv2.IMREAD_UNCHANGED)
            crop_plus_contras, crop_minus_contras = cv2.convertScaleAbs(img, alpha, plus), cv2.convertScaleAbs(img, alpha,
                                                                                                               minus)
            cv2.imwrite(join(save, basename(im)[:-4]+f"-{plus}{PNG}"), crop_plus_contras)
            cv2.imwrite(join(save, basename(im)[:-4]+f"-{minus}{PNG}"), crop_minus_contras)


def is_not_file_exist(file, check_dir):
    pattern = re.compile(str(basename(file)[:-4]))
    is_not_exist = True
    fr_id = join(check_dir, id_product(basename(file)))
    os.makedirs(fr_id, exist_ok=True)
    fr_locate = join(fr_id, camera_angle(basename(file)))
    os.makedirs(fr_locate, exist_ok=True)
    if len(os.listdir(fr_locate)) > 0:
        for f in os.listdir(fr_locate):
            if pattern.search(str(f)):
                is_not_exist = False
                break
    return is_not_exist


def is_not_file_exist1(file, check_dir):
    pattern = re.compile(str(basename(file)[:-4]))
    is_not_exist = True
    if len(os.listdir(check_dir)) > 0:
        for f in os.listdir(check_dir):
            if pattern.search(str(f)):
                is_not_exist = False
                break
    return is_not_exist


def extract_frame_from_video(video_src, dir_to_save_frame, frame_value=1):
    list_videos, list_subdirs = utils.file_proc.all_file_and_subdir_from_dir(video_src)
    if len(list_videos) == 0:
        return
    LOGGER.info("Product ID %s is extracting . . ." % (basename(video_src)))
    for video in list_videos:
        if not is_not_file_exist(video, dir_to_save_frame):
            print(" %s  da ton tai" % (basename(video)))
            return

        if video.endswith('mp4') or video.endswith('avi'):
            cap = cv2.VideoCapture(video)
            ret, frame = cap.read()
            stt, idx = 1, 0
            while True:
                fr_id = join(dir_to_save_frame, id_product(basename(video)))
                os.makedirs(fr_id, exist_ok=True)
                fr_locate = join(fr_id, camera_angle(basename(video)))
                os.makedirs(fr_locate, exist_ok=True)
                filename = join(fr_locate, name_no_ext(basename(video))) + '-' + str(stt) + PNG
                if idx % int(frame_value) == 0:
                    cv2.imwrite(filename, frame)
                stt += 1
                ret, frame = cap.read()
                idx += 1
                if not ret:
                    break
        if video.endswith('jpg') or video.endswith('png'):
            old = video
            fr_id = join(dir_to_save_frame, id_product(basename(video)))
            os.makedirs(fr_id, exist_ok=True)
            fr_locate = join(fr_id, camera_angle(basename(video)))
            os.makedirs(fr_locate, exist_ok=True)
            new = join(fr_locate, basename(video))
            shutil.copy(old, new)

    LOGGER.info(" - - - > Product ID %s is extracted" % (basename(video_src)))


def check_exist_dir(check_path, file_name):
    fr_id = join(check_path, id_product(basename(file_name)))
    os.makedirs(fr_id, exist_ok=True)
    fr_locate = join(fr_id, camera_angle(basename(file_name)))
    os.makedirs(fr_locate, exist_ok=True)
    return join(fr_locate, basename(file_name))


def remove_background(src, src_save):
    list_file, list_dirs = utils.file_proc.all_file_and_subdir_from_dir(src)
    if len(list_file) == 0:
        return
    LOGGER.info("Product ID %s is removing background . . ." % (basename(src)))
    for im in list_file:
        # if not is_not_file_exist(im, src_save):
        #     print(" %s  da ton tai" % (basename(im)))
        #     return
        if im.rindex('.png'):
            save_path = check_exist_dir(src_save, im)
            with open(im, 'rb') as i:
                with open(save_path, 'wb') as o:
                    input1 = i.read()
                    output = remove(input1)
                    o.write(output)
    LOGGER.info(" - - - - - >Product ID %s is removed" % (basename(src)))


# def change_transparent_background_to_white(fg_path, path_to_get_lbl):
#     for fg_img_path in glob.glob(os.path.join(fg_path, '*.png')):
#         fg_img = cv2.imread(fg_img_path, cv2.IMREAD_UNCHANGED)
#         h1, w1 = fg_img.shape[:2]
#         fr_img = Image.open(fg_img_path)
#         bg_img1 = np.zeros((h1, w1, 3), np.uint8)
# #         r1 = 255
# #         g1 = 255
# #         b1 = 255
# #         bg_img1[:, :] = (r1, g1, b1)
# #         back_im1 = bg_img1.copy()
# #         back_im1 = Image.fromarray(back_im1, 'RGB')
#         h, w = bg_img1.shape[:2]
#         cx, cy = (h - h1) // 2, (w - w1) // 2
#         back_im1.paste(fr_img, (cy, cx), fr_img)
#         save_path = check_exist_dir(path_to_get_lbl, fg_img_path)
#
#         result_img1 = join(save_path, basename(fg_img_path)[:-4]) + '-' + basename(fg_img_path)[
#                                                                           basename(
#                                                                               fg_img_path).rindex(
#                                                                               '.'):]
#
#         back_im1.save(result_img1)

def image_process(path, save_path, resize_value1=0, resize_value2=0):
    try:

        list_file, _ = utils.file_proc.all_file_and_subdir_from_dir(path)
        if len(list_file) == 0:
            return
        LOGGER.info("Product ID %s is processing . . ." % (basename(path)))
        for img in list_file:
            if not is_not_file_exist1(img, save_path):
                print(" %s  da ton tai" % (basename(img)))
                return

            save = join(save_path, basename(img))
            im = cv2.imread(img, cv2.IMREAD_UNCHANGED)
            im_to_crop = cv2.imread(img, cv2.IMREAD_UNCHANGED)

            alpha_channel = im[:, :, 3]
            rgb_channel = im[:, :, :3]
            white_background = np.ones_like(rgb_channel, dtype=np.uint8) * 255

            alpha_factor = alpha_channel[:, :, np.newaxis].astype(np.float32) / 255.0
            alpha_factor = np.concatenate((alpha_factor, alpha_factor, alpha_factor), axis=2)

            base = rgb_channel.astype(np.float32) * alpha_factor
            white = white_background.astype(np.float32) * (1 - alpha_factor)
            final_im = base + white
            final_im = final_im.astype(np.uint8)

            gray = cv2.cvtColor(final_im, cv2.COLOR_BGR2GRAY)
            r1, t1 = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            # t1=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
            c1, h1 = cv2.findContours(t1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            cnt = sorted(c1, key=cv2.contourArea, reverse=True)
            x, y, w, h = cv2.boundingRect(cnt[0])
            crop = im_to_crop[y:y + h, x:x + w]
            cv2.imwrite(save, crop)

            if resize_value1 > 0:
                crop_rz_1 = cv2.resize(crop, (0, 0), fx=resize_value1, fy=resize_value1)
                cv2.imwrite(save[:-4] + '-' + str(resize_value1) + PNG, crop_rz_1)

            if resize_value2 > 0:
                crop_rz_2 = cv2.resize(crop, (0, 0), fx=resize_value2, fy=resize_value2)
                cv2.imwrite(save[:-4] + '-' + str(resize_value2) + PNG, crop_rz_2)
        LOGGER.info("Product ID %s is processed" % (basename(path)))

    except Exception as e:
        LOGGER.error(e)


def affine_image(path, save_path):
    list_file, _ = utils.file_proc.all_file_and_subdir_from_dir(path)
    for img in list_file:
        if img.endswith('png'):
            im = cv2.imread(img, cv2.IMREAD_UNCHANGED)
            h, w = im.shape[:2]
            if h < w:
                pts1, pts2 = np.float32([[0, 0], [w, 0], [w / 2, h]]), np.float32([[0, h / 2], [w, h / 2], [w / 2, h]])
                M = cv2.getAffineTransform(pts1, pts2)
                img_affine = cv2.warpAffine(im, M, (w, h))
                save = save_path + SLASH + str(basename(img)[:-4]) + UNDERLINE + 'affine' + PNG
                crop = img_affine[0 + int(h / 2):0 + h, 0:0 + w]
                cv2.imwrite(save, crop)
            else:
                pts1, pts2 = np.float32([[0, h / 2], [w, 0], [w, h]]), np.float32(
                    [[0, h / 2], [w / 2, 0], [w / 2, h / 2]])
                M = cv2.getAffineTransform(pts1, pts2)
                img_affine = cv2.warpAffine(im, M, (w, h))
                save = save_path + SLASH + str(basename(img)[:-4]) + UNDERLINE + 'affine' + PNG
                crop = img_affine[0:0 + h, 0:0 + int(w / 2)]
                cv2.imwrite(save, crop)


def yolobox_to_rec_box(box, img_size):
    x, y, w, h = box
    x1 = int((x - w / 2) * img_size[1])
    w1 = int((x + w / 2) * img_size[1])
    y1 = int((y - h / 2) * img_size[0])
    h1 = int((y + h / 2) * img_size[0])
    if x1 < 0:
        x1 = 0
    if w1 > img_size[1] - 1:
        w1 = img_size[1] - 1
    if y1 < 0:
        y1 = 0
    if h1 > img_size[0] - 1:
        h1 = img_size[0] - 1
    return x1, y1, w1 - x1, h1 - y1


def id_angles(file_name):
    f = basename(file_name).split('-')[0].split('_')
    id_product1 = f[0]
    angle = f[1]
    return id_product1, angle


def save_img(f_im_p, bg, name, min_num, max_num, pack_yoko, folder_save_merged_image, image_name, product_id):
    for i in range(min_num, max_num, 1):
        b_im_path = random.choice(bg)
        bg_im = Image.open(b_im_path)
        bw, bh = bg_im.size
        background_image = bg_im.copy()
        cur_h, cur_w, max_h, max_w = 0, 0, 0, 0
        is_write = False
        while True:
            foreground_image = Image.open(f_im_p).convert("RGBA")
            fw, fh = foreground_image.size  # Background size

            if max_h < fh:
                max_h = fh - NUM
            if (cur_w + fw) >= bw:
                cur_w = 0
                cur_h += max_h
            if (cur_h + fh) >= bh:
                break
            x, y = 0, 0
            if cur_w > 0:
                if cur_h == 0:
                    background_image.paste(foreground_image, (cur_w - NUM, cur_h), foreground_image)
                    x, y = cur_w - NUM, cur_h
                else:
                    background_image.paste(foreground_image, (cur_w, cur_h - NUM), foreground_image)
                    x, y = cur_w, cur_h - NUM
            else:
                background_image.paste(foreground_image, (cur_w, cur_h), foreground_image)
                x, y = cur_w, cur_h
            box = (x, y, fw, fh)
            yolo_box = bnd_box_to_yolo_line(box, (bh, bw))
            cls = int(basename(f_im_p)[:-4].split('_')[0]) - 1
            if pack_yoko:
                for k, v in TAN_TO_PACK.items():
                    if str(cls) == str(k):
                        cls = int(v)

            with open(join(folder_save_merged_image,
                           image_name) + UNDERLINE + product_id + UNDERLINE + name + UNDERLINE + str(i) + TXT,
                      'a') as f:
                f.write(
                    str(cls) + ' ' + str(yolo_box[0]) + ' ' + str(yolo_box[1]) + ' ' + str(yolo_box[2]) + ' ' + str(
                        yolo_box[3]) + '\n')
            is_write = True
            cur_w += fw - NUM

        if is_write:
            background_image.save(join(folder_save_merged_image,
                                       image_name) + UNDERLINE + product_id + UNDERLINE + name + UNDERLINE + str(
                i) + PNG)


def merge_by_product_degree(f_product,
                            product_id,
                            background_folder,
                            folder_save_merged_image,
                            min_num=1,
                            max_num=5,
                            image_name='merge_by_product',
                            pack_yoko=False,
                            ):
    min_w_image, min_h_image = "", ""
    product_lists = []
    min_w, min_h = 10000, 10000
    for img in f_product:
        if utils.img_proc.id_product(basename(img)) == product_id:
            ID, GOC = id_angles(img)
            if pack_yoko:
                if GOC in A3:
                    product_lists.append(img)
            else:
                product_lists.append(img)
    if len(product_lists) == 0:
        return
    for img in product_lists:
        img_tmp = Image.open(img).convert("RGBA")
        w, h = img_tmp.size
        if w < min_w:
            min_w = w
            min_w_image = img
        if h < min_h:
            min_h = h
            min_h_image = img
    backs = []
    for bg_im_p in glob.glob(join(background_folder, '*')):
        backs.append(bg_im_p)
    save_img(min_w_image, backs, "w", min_num, max_num, pack_yoko, folder_save_merged_image, image_name, product_id)
    save_img(min_h_image, backs, "h", min_num, max_num, pack_yoko, folder_save_merged_image, image_name, product_id)


def merge_by_product(f_product,
                     product_id,
                     background_folder,
                     folder_save_merged_image,
                     min_num=1,
                     max_num=10,
                     image_name='merge_by_product',
                     pack_yoko=False,
                     ):
    product_lists = []
    for img in f_product:
        if utils.img_proc.id_product(basename(img)) == product_id:
            ID, GOC = id_angles(img)
            if pack_yoko:
                if GOC in A3:
                    product_lists.append(img)
            else:
                if GOC in A1:
                    product_lists.append(img)
    if len(product_lists) == 0:
        return
    backs = []
    for bg_im_p in glob.glob(join(background_folder, '*')):
        backs.append(bg_im_p)
    for i in range(min_num, max_num, 1):
        b_im_path = random.choice(backs)
        bg_im = Image.open(b_im_path)
        bw, bh = bg_im.size
        background_image = bg_im.copy()
        cur_h, cur_w, max_h, max_w = 0, 0, 0, 0
        is_write = False
        while True:
            f_im_p = random.choice(product_lists)
            foreground_image = Image.open(f_im_p).convert("RGBA")
            fw, fh = foreground_image.size  # Background size

            if max_h < fh:
                max_h = fh - NUM
            if (cur_w + fw) >= bw:
                cur_w = 0
                cur_h += max_h
            if (cur_h + fh) >= bh:
                break

            x, y = 0, 0
            try:
                if cur_w > 0:
                    if cur_h == 0:
                        background_image.paste(foreground_image, (cur_w - NUM, cur_h), foreground_image)
                        x, y = cur_w - NUM, cur_h
                    else:
                        background_image.paste(foreground_image, (cur_w, cur_h - NUM), foreground_image)
                        x, y = cur_w, cur_h - NUM
                else:
                    background_image.paste(foreground_image, (cur_w, cur_h), foreground_image)
                    x, y = cur_w, cur_h
            except Exception as e:
                print(f_im_p)
            box = (x, y, fw, fh)
            yolo_box = bnd_box_to_yolo_line(box, (bh, bw))
            cls = int(basename(f_im_p)[:-4].split('_')[0]) - 1
            if pack_yoko:
                for k, v in TAN_TO_PACK.items():
                    if str(cls) == str(k):
                        cls = int(v)

            with open(join(folder_save_merged_image, image_name) + UNDERLINE + product_id + UNDERLINE + str(i) + TXT,
                      'a') as f:
                f.write(
                    str(cls) + ' ' + str(yolo_box[0]) + ' ' + str(yolo_box[1]) + ' ' + str(yolo_box[2]) + ' ' + str(
                        yolo_box[3]) + '\n')
            is_write = True
            cur_w += fw - NUM

        if is_write:
            background_image.save(
                join(folder_save_merged_image, image_name) + UNDERLINE + product_id + UNDERLINE + str(i) + PNG)


def merge_random(images,
                 background_folder,
                 folder_save_merged_image,
                 min_num=1,
                 max_num=1001,
                 image_name='merged',
                 pack_yoko=False,
                 is_single_ue=False,
                 is_pack_ue=False):
    cv2_imgs = []
    NUM = 10
    for img_path in glob.glob(join(images, '*.png')):
        ID, GOC = id_angles(img_path)
        if is_single_ue:
            if (ID not in PACK) and (GOC not in A23):
                cv2_imgs.append(img_path)
        if is_pack_ue:
            if (ID in PACK) and (GOC in A1):
                cv2_imgs.append(img_path)
        if pack_yoko:
            if GOC in A3:
                cv2_imgs.append(img_path)
    if len(cv2_imgs) == 0:
        return
    backs = []
    for bg_im_p in glob.glob(join(background_folder, '*')):
        backs.append(bg_im_p)
    for i in range(min_num, max_num, 1):
        b_im_path = random.choice(backs)
        bg_im = Image.open(b_im_path)
        bw, bh = bg_im.size
        background_image = bg_im.copy()
        cur_h, cur_w, max_h, max_w = 0, 0, 0, 0
        is_write = False
        while True:
            f_im_p = random.choice(cv2_imgs)
            foreground_image = Image.open(f_im_p).convert("RGBA")
            fw, fh = foreground_image.size  # Background size

            if max_h < fh:
                max_h = fh - NUM
            if (cur_w + fw) >= bw:
                cur_w = 0
                cur_h += max_h
            if (cur_h + fh) >= bh:
                break
            x, y = 0, 0
            try:
                if cur_w > 0:
                    if cur_h == 0:
                        background_image.paste(foreground_image, (cur_w - NUM, cur_h), foreground_image)
                        x, y = cur_w - NUM, cur_h
                    else:
                        background_image.paste(foreground_image, (cur_w, cur_h - NUM), foreground_image)
                        x, y = cur_w, cur_h - NUM
                else:
                    background_image.paste(foreground_image, (cur_w, cur_h), foreground_image)
                    x, y = cur_w, cur_h
            except Exception as e:
                print(f_im_p)
            box = (x, y, fw, fh)
            yolo_box = bnd_box_to_yolo_line(box, (bh, bw))
            cls = int(basename(f_im_p)[:-4].split('_')[0]) - 1
            if pack_yoko:
                for k, v in TAN_TO_PACK.items():
                    if str(cls) == str(k):
                        cls = int(v)

            with open(join(folder_save_merged_image, image_name) + UNDERLINE + str(i) + TXT, 'a') as f:
                f.write(
                    str(cls) + ' ' + str(yolo_box[0]) + ' ' + str(yolo_box[1]) + ' ' + str(yolo_box[2]) + ' ' + str(
                        yolo_box[3]) + '\n')
            is_write = True
            cur_w += fw - NUM

        if is_write:
            background_image.save(join(folder_save_merged_image, image_name) + UNDERLINE + str(i) + PNG)


def merge_random2(images,
                  background_folder,
                  folder_save_merged_image,
                  image_name='merged_ano',
                  pack_yoko=False,
                  is_single_ue=False,
                  is_pack_ue=False):
    cv2_imgs = []
    ANO_NUM = 300
    images, _ = file_proc.all_file_and_subdir_from_dir(images)
    backgrounds, _ = file_proc.all_file_and_subdir_from_dir(background_folder)

    for img_path in images:
        ID, GOC = id_angles(img_path)
        if is_single_ue:
            if (ID not in PACK) and (GOC not in A23):
                cv2_imgs.append(img_path)
        if is_pack_ue:
            if (ID in PACK) and (GOC in A1):
                cv2_imgs.append(img_path)
        if pack_yoko:
            if GOC in A3:
                cv2_imgs.append(img_path)
    if len(cv2_imgs) == 0:
        return
    backs = []
    dictionary = {}
    for bg_im_p in backgrounds:
        backs.append(bg_im_p)
    idx = 1
    while True:
        if len(cv2_imgs) == 0:
            break
        b_im_path = random.choice(backs)
        bg_im = Image.open(b_im_path)
        bw, bh = bg_im.size
        background_image = bg_im.copy()
        cur_h, cur_w, max_h, max_w = 0, 0, 0, 0
        is_write = False
        while True:
            if len(cv2_imgs) == 0:
                break
            f_im_p = random.choice(cv2_imgs)
            id_, goc_ = id_angles(f_im_p)
            if id_ not in dictionary:
                dictionary.update({id_: 1})
            if dictionary[id_] > ANO_NUM:
                print(f" paste : {id_}:{dictionary[id_]}")
                for im in cv2_imgs:
                    if id_angles(im)[0] == id_:
                        cv2_imgs.remove(im)
                continue

            foreground_image = Image.open(f_im_p).convert("RGBA")
            fw, fh = foreground_image.size  # Background size

            if max_h < fh:
                max_h = fh - NUM
            if (cur_w + fw) >= bw:
                cur_w = 0
                cur_h += max_h
            if (cur_h + fh) >= bh:
                break
            x, y = 0, 0
            try:
                if cur_w > 0:
                    if cur_h == 0:
                        background_image.paste(foreground_image, (cur_w - NUM, cur_h), foreground_image)
                        x, y = cur_w - NUM, cur_h
                    else:
                        background_image.paste(foreground_image, (cur_w, cur_h - NUM), foreground_image)
                        x, y = cur_w, cur_h - NUM
                else:
                    background_image.paste(foreground_image, (cur_w, cur_h), foreground_image)
                    x, y = cur_w, cur_h
            except Exception as e:
                print(e)
            box = (x, y, fw, fh)
            yolo_box = bnd_box_to_yolo_line(box, (bh, bw))
            cls = int(basename(f_im_p)[:-4].split('_')[0]) - 1
            if pack_yoko:
                for k, v in TAN_TO_PACK.items():
                    if str(cls) == str(k):
                        cls = int(v)

            with open(join(folder_save_merged_image, image_name) + UNDERLINE + str(idx) + TXT, 'a') as f:
                f.write(f"{cls} {yolo_box[0]} {yolo_box[1]} {yolo_box[2]} {yolo_box[3]}\n")
            is_write = True
            dictionary.update({id_: dictionary[id_] + 1})
            cur_w += fw - NUM

        if is_write:
            background_image.save(join(folder_save_merged_image, image_name) + UNDERLINE + str(idx) + PNG)

        idx += 1


# h,w= shape[:2]
# pascal_voc [x_min,y_min,x_max,y_max]
# albumentation [x_min/w,y_min/w,x_max/h,y_max/h]
# coco [x_min,y_min,width,height]
# yolo [x_center,y_center, width,height]
# x_center=((x_max+x_min)/2)/width,y_center=((y_max+y_min)/2)/h,width=width/w,height=height/w
def bnd_box_to_yolo_line(box, img_size):
    (x_min, y_min) = (box[0], box[1])
    (w, h) = (box[2], box[3])
    x_max = x_min + w
    y_max = y_min + h

    x_center = float((x_min + x_max)) / 2 / img_size[1]
    y_center = float((y_min + y_max)) / 2 / img_size[0]

    w = float((x_max - x_min)) / img_size[1]
    h = float((y_max - y_min)) / img_size[0]

    return x_center, y_center, w if w < 1 else 1.0, h if h < 1 else 1.0


def create_dataset(dataset_path, folder_img_path):
    path_img_train, path_img_valid = join(dataset_path, 'images', 'train'), join(dataset_path, 'images', 'valid')
    path_lbl_train, path_lbl_valid = join(dataset_path, 'labels', 'train'), join(dataset_path, 'labels', 'valid')
    os.makedirs(path_img_train, exist_ok=True)
    os.makedirs(path_img_valid, exist_ok=True)
    os.makedirs(path_lbl_train, exist_ok=True)
    os.makedirs(path_lbl_valid, exist_ok=True)
    img_arr, lbl_arr = [], []
    for file in os.listdir(folder_img_path):
        if file.endswith('png'):
            img_arr.append(file)
        if file.endswith('txt'):
            lbl_arr.append(file)
    print('Len of  img : ' + str(len(img_arr)))
    print('len of lbl : ' + str(len(lbl_arr)))
    valid_num, rans = len(img_arr) // 5, []
    print('len valid : ' + str(valid_num))
    for i in range(0, valid_num, 1):
        while True:
            img_ran = random.choice(img_arr)
            if img_ran not in rans:
                rans.append(img_ran[:-4])
                break

    print(len(rans))
    for img in os.listdir(folder_img_path):
        if img[:-4] in rans:
            if img.endswith('png'):
                old, new = join(folder_img_path, img), join(path_img_valid, img)
                shutil.copy(old, new)
            elif img.endswith('txt'):
                old, new = join(folder_img_path, img), join(path_lbl_valid, img)
                shutil.copy(old, new)
        else:
            if img.endswith('png'):
                old, new = join(folder_img_path, img), join(path_img_train, img)
                shutil.copy(old, new)
            elif img.endswith('txt'):
                old, new = join(folder_img_path, img), join(path_lbl_train, img)
                shutil.copy(old, new)


def compare_in_folder():
    path_move = join(ROOT, 'image_fol', 'img_process', 'original_pack')
    path_src = join(ROOT, 'image_fol', 'img_process', 'original')

    img_list = []
    lbl_list = []
    lbl_move = []
    for lbl in os.listdir(path_src):
        if lbl[lbl.rindex('.') + 1:] == 'txt':
            lbl_list.append(lbl[:-4])
    for img in os.listdir(path_src):
        if img[img.rindex('.') + 1:] == 'png' or img[img.rindex('.') + 1:] == 'PNG':
            img_list.append(img[:-4])

    diff_arr = list(set(img_list).difference(lbl_list))
    delete_file = []
    if len(diff_arr) == 0:
        print("No dif")
    else:
        for dell in diff_arr:
            dell = dell + '.png'
            delete_file.append(dell)
    for file_move in delete_file:
        m1 = path_src + file_move
        m2 = path_move + file_move
        shutil.move(m1, m2)


def compare(path, move_path):
    img_list = []
    lbl_list = []
    for lbl in os.listdir(path):
        if lbl.endswith('txt'):
            lbl_list.append(lbl[:-4])
        if lbl.endswith('png'):
            img_list.append(lbl[:-4])

    diff_arr = list(set(img_list).difference(lbl_list))
    delete_file = []
    if len(diff_arr) == 0:
        print("No dif")
    else:
        for dell in diff_arr:
            dell = dell + '.png'
            delete_file.append(dell)
    for file_move in delete_file:
        m1 = path + SLASH + file_move
        m2 = move_path + SLASH + file_move
        shutil.move(m1, m2)


def img_rotated(img, degree, border_value):
    w, h = img.shape[:2]
    cX, cY = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -degree, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), borderValue=border_value)
    return rotated
    # special_degrees = [0, 90, 180, 270]
    # if degrees is special_degrees:
    #     M = cv2.getRotationMatrix2D((cX, cY), -degree, 1.0)
    #     rotated = cv2.warpAffine(img, M, (w, h))
    #     return rotated
    # else:
    #     M = cv2.getRotationMatrix2D((cX, cY), -degree, 1.0)
    #     cos = np.abs(M[0, 0])
    #     sin = np.abs(M[0, 1])
    #     # compute the new bounding dimensions of the image
    #     nW = int((h * sin) + (w * cos))
    #     nH = int((h * cos) + (w * sin))
    #
    #     M[0, 2] += (nW / 2) - cX
    #     M[1, 2] += (nH / 2) - cY
    #     rotated = cv2.warpAffine(img, M, (nW, nH), borderValue=border_value)
    #     return rotated


def crop_and_paste(path, crop, save_path, cls):
    try:

        im = cv2.imread(path)
        txt_path = path[:-4] + '.txt'
        f1 = open(txt_path, 'r')
        data = f1.readlines()
        f1.close()
        x, y, w, h = 0, 0, 0, 0
        for dt in data:
            _, x, y, w, h = map(float, dt.split(' '))

        x, y, w, h = yolobox_to_rec_box((x, y, w, h), im.shape[:2])

        bbboxs = []
        if im.shape[0] < im.shape[1]:
            if crop:  # by x
                crop = im[y:y + h, x:x + w]
                im[y:y + h, x + w:x + w + w] = crop
                bbboxs.append(bnd_box_to_yolo_line((x + w, y, w, h), im.shape[:2]))
                im[y:y + h, x - w:x] = crop
                bbboxs.append(bnd_box_to_yolo_line((x - w, y, w, h), im.shape[:2]))
            for box in bbboxs:
                with open(save_path[:-4] + '.txt', 'a') as f:
                    f.write(str(cls) + ' ' + str(box[0]) + ' ' + str(box[1]) + ' ' + str(box[2]) + ' ' + str(
                        box[3]) + '\n')
            cv2.imwrite(save_path, im)
        if im.shape[0] > im.shape[1]:
            if crop:  # by x
                crop = im[y:y + h, x:x + w]
                if x >= x + w + w or x - w <= x:
                    im[y:y + h, x + w:x + w + w] = crop
                    bbboxs.append(bnd_box_to_yolo_line((x + w, y, w, h), im.shape[:2]))
                    im[y:y + h, x - w:x] = crop
                    bbboxs.append(bnd_box_to_yolo_line((x - w, y, w, h), im.shape[:2]))
                    for box in bbboxs:
                        with open(save_path[:-4] + TXT, 'a') as f:
                            f.write(str(cls) + ' ' + str(box[0]) + ' ' + str(box[1]) + ' ' + str(box[2]) + ' ' + str(
                                box[3]) + '\n')
                    cv2.imwrite(save_path, im)
    except Exception as e:
        print(path)
        print(e)
