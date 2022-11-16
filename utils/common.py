import utils.img_proc
from constants import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import utils.style_sheet
import time
import threading
import utils.file_proc
from constants import (ROOT, LOGGER, ROOT1, SLASH, UNDERLINE, JPG, PNG, TXT, PACK,
                       PACK_UE, A1, A2, A3, A12, A23, A13, CASE, A123, TAN_TO_PACK, join, basename)

s_video = "video"
s_dataset = "image_process"
s_extracted = "extracted"
s_yakult = "yakult"
s_cosmetic = "cosmetic"
s_food = "food"


class Product:
    def __init__(self):
        self.finnish_date = None
        self.product_code = None
        self.product_name = None
        self.product_classification = None
        self.cnt_product_single = None
        self.cnt_product_pack = None
        self.cnt_product_case = None

    def set(self, finnish_date, product_code, product_name, product_classification, cnt_product_single,
            cnt_product_pack,
            cnt_product_case):
        self.finnish_date = finnish_date
        self.product_code = product_code
        self.product_name = product_name
        self.product_classification = product_classification
        self.cnt_product_single = cnt_product_single
        self.cnt_product_pack = cnt_product_pack
        self.cnt_product_case = cnt_product_case

    def get(self):
        return {"finnish_date": self.finnish_date,
                "product_code": self.product_code,
                "product_name": self.product_name,
                "product_classification": self.product_classification,
                "cnt_product_single": self.cnt_product_single,
                "cnt_product_pack": self.cnt_product_pack,
                "cnt_product_case": self.cnt_product_case, }


def show_message_dialog(text, OK="OK", Cancel="取消"):
    try:
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout()
        dlg_widget = QGroupBox("報告")
        dlg_widget.setStyleSheet(utils.style_sheet.QGroupBoxStyle1(border_width=2))
        dlg_layout = QVBoxLayout()
        mes = QLabel(text)
        mes.setStyleSheet(utils.style_sheet.QLabelStyle())
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.btnBox = QDialogButtonBox(btn)
        dlg.btnBox.button(QDialogButtonBox.Cancel).setText(Cancel)
        dlg.btnBox.button(QDialogButtonBox.Ok).setText(OK)
        dlg.btnBox.setStyleSheet(utils.style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        set_shadow(dlg.btnBox)

        dlg.btnBox.rejected.connect(dlg.reject)
        dlg.btnBox.accepted.connect(dlg.accept)
        dlg_layout.addWidget(QLabel(""), 0, QtCore.Qt.AlignCenter)
        dlg_layout.addWidget(mes, 0, QtCore.Qt.AlignCenter)
        dlg_layout.addWidget(QLabel("―――――――――――――――――――――"), 0, QtCore.Qt.AlignCenter)
        dlg_layout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)

        dlg_widget.setLayout(dlg_layout)

        layout.addWidget(dlg_widget)
        dlg.setLayout(layout)
        if dlg.exec():
            return True
        else:
            return False
    except Exception as e:
        print(e)


def check_dataset(src, path_move):
    images, labels = [], []
    for f in os.listdir(src):
        images.append(f[:-4]) if basename(f).endswith("txt") else labels.append(f[:-4])

    # List of image and label does not match name
    list_not_match = list(set(images).difference(labels))

    # Move doesn't match file to path move
    if len(list_not_match) > 0:
        for f in [delete.join(PNG) for delete in list_not_match]:
            m1, m2 = join(src, f), join(path_move, f)
            shutil.move(m1, m2)


def create_dataset(dataset_path, images_path, bg_dir):
    # Init Dataset Directory
    path_img_train, path_img_valid = join(dataset_path, 'images', 'train'), join(dataset_path, 'images', 'valid')
    path_lbl_train, path_lbl_valid = join(dataset_path, 'labels', 'train'), join(dataset_path, 'labels', 'valid')
    os.makedirs(path_img_train, exist_ok=True)
    os.makedirs(path_img_valid, exist_ok=True)
    os.makedirs(path_lbl_train, exist_ok=True)
    os.makedirs(path_lbl_valid, exist_ok=True)

    images, labels = [], []
    for file in os.listdir(images_path):
        images.append(file) if file.endswith('png') else labels.append(file)

    num_of_valid = len(images) // 5
    print(f'Len of images : {len(images)}\nLen of labels : {len(labels)}\nLen valid : {num_of_valid}')

    random_images = []
    for i in range(0, num_of_valid, 1):
        while True:
            img_ran = random.choice(images)
            if img_ran not in random_images:
                random_images.append(img_ran[:-4])
                break

    for img in os.listdir(images_path):
        # Add valid image and label to Dataset Directory
        if img[:-4] in random_images:
            shutil.copy(join(images_path, img), join(path_img_valid, img)) if img.endswith(
                'png') else shutil.copy(join(images_path, img), join(path_lbl_valid, img))

        # Add train image and label to Dataset Directory
        else:
            shutil.copy(join(images_path, img), join(path_img_train, img)) if img.endswith(
                'png') else shutil.copy(join(images_path, img), join(path_lbl_train, img))

    # Add background image to train dataset
    for img in os.listdir(bg_dir):
        shutil.copy(join(bg_dir, img), join(path_img_train, img))


def get_path(combox_widget, root_dir, save_dir):
    path_dir, path_save = "", ""
    root_, save = join(os.getcwd(), "image_process", root_dir), join(os.getcwd(), "image_process", save_dir)
    if combox_widget.currentText() == "ヤクルト":
        path_dir, path_save = join(root_, "yakult"), join(save, "yakult")

    if combox_widget.currentText() == "化粧":
        path_dir, path_save = join(root_, "cosmetic"), join(save, "cosmetic")

    if combox_widget.currentText() == "食品":
        path_dir, path_save = join(root_, "food"), join(save, "food")

    os.makedirs(path_dir, exist_ok=True)
    os.makedirs(path_save, exist_ok=True)

    return path_dir, path_save


def extract_video_thread(video_dirs, save_extracted_dir, list_id_product_to_extract, value=1):
    threads = []
    # TODO get frame by fps or ??
    for v in list_id_product_to_extract:
        t = threading.Thread(target=utils.img_proc.extract_frame_from_video,
                             args=(join(video_dirs, v),  # videos directory
                                   save_extracted_dir,  # save extracted images directory
                                   value  # frame ??
                                   ))
        threads.append(t)
        t.start()

    for idx, th in enumerate(threads):
        th.join()


def remove_background_thread(video_dirs, save_remove_dir, list_removed_dir):
    threads = []
    for v in list_removed_dir:
        t = threading.Thread(
            target=utils.img_proc.remove_background, args=(
                join(video_dirs, v),  # videos directory
                save_remove_dir,  # save removed images directory
            ))
        threads.append(t)
        t.start()

    for idx, th in enumerate(threads):
        th.join()


def cut_save_thread(removed_dirs, save_cut_dir, list_cut_dir, resize1=0, resize2=0):
    threads = []
    for v in list_cut_dir:
        t = threading.Thread(target=utils.img_proc.image_process,
                             args=(
                                 join(removed_dirs, v),  # videos directory
                                 save_cut_dir,  # save processed images directory
                                 resize1,  # images resize value 1
                                 resize2,  # images resize value 2
                             ))
        threads.append(t)
        t.start()

    for idx, th in enumerate(threads):
        th.join()


def merged_image_thread(foreground_dir1, background_dir, save_pack_dir, max_value=1000, min_value=1,
                        value_per_thread=100, is_yoko=False, name="merged", merge_only=False):
    threads = []

    # Number of thread
    num_of_thread = int(max_value / value_per_thread)

    # Images name
    name = name + "_yoko" if is_yoko else name + "_top"

    # for v in range(num_of_thread):
    #     # Thread for single product
    #     t = threading.Thread(target=utils.img_proc.merge_random,
    #                          args=(foreground_dir1,  # processed images directory
    #                                background_dir,  # background images directory
    #                                save_pack_dir,  # save merged images directory
    #                                min_value,  # thread start at index
    #                                min_value + value_per_thread,  # thread end at index
    #                                name,  # name of image
    #                                is_yoko,  # for yoko
    #                                True,  # for singe product
    #                                False,  # for pack product
    #                                ))
    #     threads.append(t)
    #     t.start()
    #
    #     # Thread for single pack product
    #     # if not is_yoko:
    #     #     if num_of_thread < max_value // 3:
    #     #         t1 = threading.Thread(target=utils.img_proc.merge_random,
    #     #                               args=(foreground_dir1,  # processed images directory
    #     #                                     background_dir,  # background images directory
    #     #                                     save_pack_dir,  # save merged images directory
    #     #                                     min_value,  # thread start at index
    #     #                                     min_value + value_per_thread,  # thread end at index
    #     #                                     name,  # name of image
    #     #                                     is_yoko,  # for yoko
    #     #                                     False,  # for singe product
    #     #                                     True,  # for pack product
    #     #                                     ))
    #     #
    #     #         threads.append(t1)
    #     #         t1.start()
    #     #
    #     min_value += value_per_thread

    # Merge only one product
    if merge_only:
        # Get list image
        list_product, _ = utils.file_proc.all_file_and_subdir_from_dir(foreground_dir1)

        # Get id product
        with open("./data/class_names_by_id.txt", 'r', encoding="UTF-8") as f:
            list_yakult = [line.strip() for line in f]

            for p_id in list_yakult:
                # Merge by only one product
                t2 = threading.Thread(target=utils.img_proc.merge_by_product,
                                      args=(list_product,  # list image
                                            p_id,  # id of product
                                            background_dir,  # background images directory
                                            save_pack_dir,  # save merged image directory
                                            1,  # thread start at 1
                                            5,  # thread end at 5 (only 5 images)
                                            name + "_only",  # name of image
                                            is_yoko,  # for yoko
                                            ))

                # Merge by degree of product
                t3 = threading.Thread(target=utils.img_proc.merge_by_product_degree,
                                      args=(list_product,  # list image
                                            p_id,  # id of product
                                            background_dir,  # background images directory
                                            save_pack_dir,  # save merged image directory
                                            1,  # thread start at 1
                                            2,  # thread end at 2 (only 2 images)
                                            name + "_degree",  # name of image
                                            is_yoko,  # for yoko
                                            ))
                threads.append(t2)
                threads.append(t3)
                t2.start()
                t3.start()
    #
    for idx, th in enumerate(threads):
        th.join()


def set_opacity_on(widget, opacity_value: float = 1):
    opacity = QGraphicsOpacityEffect()
    opacity.setOpacity(opacity_value)
    widget.setGraphicsEffect(opacity)
    widget.setEnabled(True)


def set_opacity_off(widget,opac=0):
    opacity = QGraphicsOpacityEffect()
    opacity.setOpacity(opac)
    widget.setGraphicsEffect(opacity)
    widget.setEnabled(False)


def set_shadow(widget, blur_radius=20, offset=3):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setColor(Qt.lightGray)
    shadow.setOffset(3)
    widget.setGraphicsEffect(shadow)


def get_bitmap_blank_image(mode=0):
    img = cv2.imread('./data/resource/setting0.png') if mode == 0 else cv2.imread('./data/resource/setting.png')

    img = cv2.resize(img, (0, 0), fx=960 / img.shape[1], fy=960 / img.shape[1])
    img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
    return QPixmap.fromImage(img)


def show_message_dialog1(text, opacity=.5):
    try:
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setWindowTitle("報告")
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg.setStyleSheet("border-radius:10px;")
        dlg_layout = QVBoxLayout()

        wd = QGroupBox()
        set_opacity_on(wd, opacity_value=opacity)
        wd.setStyleSheet(utils.style_sheet.QGroupBoxStyle1())
        wd_layout = QVBoxLayout()

        mes = QLabel(text)
        btn_close = QDialogButtonBox.Close
        dlg.btnBox = QDialogButtonBox(btn_close)
        dlg.btnBox.setMaximumSize(70, 40)
        dlg.btnBox.button(QDialogButtonBox.Close).setText("閉じる")
        dlg.btnBox.setStyleSheet(utils.style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        set_shadow(dlg.btnBox)

        dlg.btnBox.rejected.connect(dlg.close)
        wd_layout.addWidget(mes, 0, QtCore.Qt.AlignCenter)
        wd_layout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)
        wd.setLayout(wd_layout)
        dlg_layout.addWidget(wd)
        dlg.setLayout(dlg_layout)
        dlg.exec()
    except Exception as e:
        print(e)


def show_toast(text, time_dur):
    try:
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents)
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setWindowTitle("報告")
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        dlg.setStyleSheet("border-radius:10px;")
        dlg.setFixedSize(300, 100)
        dlg_layout = QVBoxLayout()

        wd = QGroupBox()
        set_opacity_on(wd, opacity_value=.5)
        wd.setStyleSheet(utils.style_sheet.QGroupBoxStyle1())
        wd_layout = QVBoxLayout()

        mes = QLabel(text)
        btn_close = QDialogButtonBox.Close
        dlg.btnBox = QDialogButtonBox(btn_close)
        dlg.btnBox.setMaximumSize(70, 40)
        dlg.btnBox.button(QDialogButtonBox.Close).setText("閉じる")
        dlg.btnBox.setStyleSheet(utils.style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))

        dlg.btnBox.rejected.connect(dlg.close)
        wd_layout.addWidget(mes, 0, QtCore.Qt.AlignCenter)
        # wd_layout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)
        wd.setLayout(wd_layout)
        dlg_layout.addWidget(wd)
        dlg.setLayout(dlg_layout)
        dlg.btnBox.button(QDialogButtonBox.Close).animateClick(time_dur)
        dlg.exec()

    except Exception as e:
        print(e)


def show_loading(time_dur):
    try:
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents)
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        dlg.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        dlg.setFixedSize(300, 300)
        dlg_layout = QVBoxLayout()

        loading = QtSvg.QSvgWidget("./data/resource/200px.svg")
        btn_close = QDialogButtonBox.Close
        dlg.btnBox = QDialogButtonBox(btn_close)
        dlg.btnBox.setMaximumSize(70, 40)
        dlg.btnBox.button(QDialogButtonBox.Close).setText("閉じる")
        dlg.btnBox.setStyleSheet(utils.style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))

        dlg.btnBox.rejected.connect(dlg.close)
        dlg_layout.addWidget(loading, 0, QtCore.Qt.AlignCenter)
        # wd_layout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)

        dlg.setLayout(dlg_layout)
        dlg.btnBox.button(QDialogButtonBox.Close).animateClick(time_dur)
        dlg.exec()

    except Exception as e:
        print(e)


def get_camera_indexes():
    LOGGER.info("Load camera index")
    # TODO check when only get 1 camera
    arr = [0, 1]
    # res = 5000
    box = None
    # for idx in range(0, 5, 1):
    #     cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res)
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, res)
    #
    #     h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #     w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #     arr.append(str(idx)) if int(h) not in [res, 0] else arr
    # LOGGER.info('Camera index available :  ' + ', '.join(f'{x}' for x in arr))
    cameras_dic = {}
    cap_ = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap_.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
    cap_.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
    h = int(cap_.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap_.get(cv2.CAP_PROP_FRAME_WIDTH))

    while True:
        r, frame = cap_.read()
        cap_.set(cv2.CAP_PROP_FOCUS, 0)
        if not r:
            cap_.release()
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blurred = cv2.medianBlur(gray, 25)
        min_dist = 100
        param1 = 50
        param2 = 100
        min_radius1 = 0
        max_radius1 = 5000
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, min_dist, param1=param1, param2=param2,
                                   minRadius=min_radius1, maxRadius=max_radius1)
        if circles is not None:
            print("tim ra hinh tron")
            circles = np.uint16(np.around(circles))
            max_r = 0
            for i in circles[0, :]:
                if max_r < i[2]:
                    max_r = i[2]
            for i in circles[0, :]:
                if max_r == i[2]:
                    box = ((i[0] - i[2] + 20), (i[1] - i[2] + 20), (i[2] * 2 - 40), (i[2] * 2 - 40))
                    pass
            cameras_dic["TOP"] = 0
            cameras_dic["YOKO"] = 1
            cap_.release()
            break
        if circles is None:
            print("tim k ra hinh tron")
            cameras_dic["TOP"] = 1
            cameras_dic["YOKO"] = 0
            cap_.release()
            break
    print(cameras_dic)
    return cameras_dic, box


def get_pixmap(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)
    img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
    return QPixmap.fromImage(img)


def init_config(path, yk_dataset_name, number_class, list_yk, M_MODEL):
    # custom_dataset
    with open(join(path, "custom_dataset.yaml"), 'w') as f:
        custom_dataset = f"""# relative paths from folder yolov5
#  .
#  ├── custom_dataset
#  └── yolov5
train: ../yakult_project/Dataset/{yk_dataset_name}/images/train/
val: ../yakult_project/Dataset/{yk_dataset_name}/images/valid/
# number of classes
nc: {number_class}
# class names
names: {list_yk}
"""
        f.write(custom_dataset)

    # custom_model
    with open(join(path, "custom_model.yaml"), 'w') as f:
        custom_model = f"""# YOLOv5 by Ultralytics, GPL-3.0 license

# Parameters
nc: {number_class}  # number of classes
depth_multiple: {M_MODEL[0]}  # model depth multiple
width_multiple: {M_MODEL[1]}  # layer channel multiple
anchors:
  - [10,13, 16,30, 33,23]  # P3/8
  - [30,61, 62,45, 59,119]  # P4/16
  - [116,90, 156,198, 373,326]  # P5/32

# YOLOv5 v6.0 backbone
backbone:
  # [from, number, module, args]
  [[-1, 1, Conv, [64, 6, 2, 2]],  # 0-P1/2
   [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
   [-1, 3, C3, [128]],
   [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
   [-1, 6, C3, [256]],
   [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
   [-1, 9, C3, [512]],
   [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
   [-1, 3, C3, [1024]],
   [-1, 1, SPPF, [1024, 5]],  # 9
  ]

# YOLOv5 v6.0 head
head:
  [[-1, 1, Conv, [512, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 6], 1, Concat, [1]],  # cat backbone P4
   [-1, 3, C3, [512, False]],  # 13

   [-1, 1, Conv, [256, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 4], 1, Concat, [1]],  # cat backbone P3
   [-1, 3, C3, [256, False]],  # 17 (P3/8-small)

   [-1, 1, Conv, [256, 3, 2]],
   [[-1, 14], 1, Concat, [1]],  # cat head P4
   [-1, 3, C3, [512, False]],  # 20 (P4/16-medium)

   [-1, 1, Conv, [512, 3, 2]],
   [[-1, 10], 1, Concat, [1]],  # cat head P5
   [-1, 3, C3, [1024, False]],  # 23 (P5/32-large)

   [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
  ]
"""
        f.write(custom_model)
