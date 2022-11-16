import os
import threading
import time
import xlrd
import json
from datetime import datetime

import utils.file_proc
from constants import *
from utils import common, style_sheet
from utils.common import LOGGER
from widget.right_widget import RightWidget
from widget.switch_button import QSwitchButton
from widget.custom_button import CustomQToolButton


class Yakult:
    def __init__(self):
        self.list_update_products = []
        self.list_insert_products = []


class Cosmetic:
    def __init__(self):
        self.list_update_products = []
        self.list_insert_products = []


class Food:
    def __init__(self):
        self.list_update_products = []
        self.list_insert_products = []


class CreateVideoWidget(QtWidgets.QWidget):
    yakult = Yakult()
    cosmetic = Cosmetic()
    food = Food()
    signal_auto_complete = pyqtSignal(object)
    signal_cm1 = pyqtSignal(object)
    signal_cm2 = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.btn_product_checked = None
        self.sw_open_camera = None
        self.product_type = None
        self.txt_classification = None
        self.box = None
        self.product_code = None
        self.data = None
        self.txt_product_name1 = None
        self.txt_product_name3 = None
        self.txt_product_name2 = None
        self.btn_open_folder_2 = None
        self.status = None
        self.btn_open_folder_1 = None
        self.btn_product_check = None
        self.line_edit = None
        self.model_classes_name = []
        self.product_list = []
        self.btn_take_photo2 = None
        self.btn_create_video2 = None
        self.status2 = None
        self.hori_camera_control_widget = None
        self.time_started1 = None
        self.time_started2 = None
        self.btn_take_photo1 = None
        self.btn_create_video1 = None
        self.top_camera_control_widget = None
        self.btn_swap_camera = None
        self.isServer = None
        self.txt_save_dir = None
        self.set_focus = None
        self.lb_focus = None
        self.current_focus = 24
        self.btn_back = None
        self.set_fps = None
        self.btn_show_folder = None
        self.hori_camera_start_record = None
        self.top_camera_start_record = None
        self.last_index_product = None
        self.list_product = None
        self.txt_product_name_id = None
        self.btn_select_product = None
        self.select_exist_product_widget = None
        self.fr_locate3 = None
        self.fr_locate2 = None
        self.fr_locate1 = None
        self.settingLayout = None
        self.input_id_widget = None
        self.create_video_layout = None
        self.cb_category = None
        self.btnRecord = None
        self.btn_choose_file = None
        self.txt_set_limit_time = None
        self.time_label2 = None
        self.time_label1 = None
        self.camera2 = None
        self.camera1 = None
        self.cb_camera2 = None
        self.hori_camera_widget = None
        self.cb_camera1 = None
        self.top_camera_widget = None
        self.cb_product_case = None
        self.cb_product_pack = None
        self.cb_product = None
        self.txt_product_name = None
        self.lb_product_name = None
        self.txtCategory = None
        self.count = 0
        self.arr_camera_indexes = None
        self.current_product_index = None
        self.current_product_name = None
        self.current_product_name_folder = None
        self.path = None
        self.root = None
        self.is_open_camera = None
        self.source = None
        self.camera_widget_indexes = [0, 1]
        self.take_photo1 = None
        self.take_photo2 = None
        self.save_vid1 = None
        self.save_vid2 = None
        self.type = None
        self.create_ui()

    def create_ui(self):
        LOGGER.info("Init Create Video Widget")

        self.create_video_layout = QHBoxLayout()
        main_widget = QtWidgets.QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        top_widget = QtWidgets.QWidget()
        # top_widget.setMaximumHeight(250)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # region product setting widget
        product_setting_widget = QGroupBox("商品設定")
        product_setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())
        layout = QHBoxLayout()
        product_widget = QtWidgets.QWidget()
        product_layout = QGridLayout()

        product_type_widget = QGroupBox("分類")
        product_type_widget.setStyleSheet(
            style_sheet.QGroupBoxStyle(border_width=0,
                                       tile_background_color="white",
                                       margin_top=8,
                                       position="top left",
                                       padding_title_1=10,
                                       title_color="black"))

        product_type = QHBoxLayout()
        self.cb_category = QComboBox()
        self.cb_category.setMinimumHeight(40)
        self.cb_category.setMaximumSize(200, 60)
        self.cb_category.setStyleSheet(style_sheet.QComboBoxStyle())
        self.cb_category.adjustSize()
        self.cb_category.addItems(['ヤクルト'])  # , '化粧', '食品'
        self.cb_category.activated.connect(self.on_product_item_selected)

        # product_type.addWidget(lb_category)
        product_type.addWidget(self.cb_category)
        product_type_widget.setLayout(product_type)

        # Select product widget
        select_product_widget = QGroupBox("商品コード")
        select_product_widget.setStyleSheet(
            style_sheet.QGroupBoxStyle(border_width=0,
                                       tile_background_color="white",
                                       margin_top=8,
                                       position="top left",
                                       padding_title_1=10,
                                       title_color="black"))

        select_product_layout = QHBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setMinimumHeight(40)
        self.line_edit.adjustSize()
        # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        # input_validator = QRegExpValidator(reg_ex, self.line_edit)
        # self.line_edit.setValidator(input_validator)
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit.setStyleSheet(style_sheet.QLineEditStyle())

        self.btn_product_check = QToolButton()
        common.set_shadow(self.btn_product_check)
        self.btn_product_check.setText("商品確認")
        self.btn_product_check.setMaximumHeight(50)
        self.btn_product_check.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=5, margin_left=15))
        self.btn_product_check.clicked.connect(self.on_btn_product_checked)

        select_product_layout.addWidget(self.line_edit)
        select_product_widget.setLayout(select_product_layout)

        # self.signal_auto_complete.connect(self.line_edit.setCompleter)
        f = open("./data/json/master_data.json", "r", encoding="utf8")
        self.data = json.loads(f.read())
        codes = [f"{a['product_code']}：{a['product_name']}" for a in self.data]

        # completer = QCompleter(codes)
        model = QStringListModel()
        model.setStringList(codes)
        completer = QCompleter()
        completer.setModel(model)

        completer.popup().setStyleSheet("font-size:18px;")
        completer.activated.connect(self.on_completer_selected)
        self.line_edit.setCompleter(completer)
        # completer.setCaseSensitivity(Qt.CaseSensitive)
        # self.signal_auto_complete.emit(completer)

        product_layout.addWidget(product_type_widget, 1, 1)
        product_layout.addWidget(select_product_widget, 1, 2)
        product_layout.addWidget(self.btn_product_check, 2, 2)
        product_widget.setLayout(product_layout)

        product_info_widget = QGroupBox()
        product_info_widget.setStyleSheet(style_sheet.QGroupBoxStyle2())
        common.set_shadow(product_info_widget, blur_radius=10, offset=1)
        product_info_widget.setMinimumHeight(150)
        product_info_layout = QGridLayout()

        product_name_widget = QtWidgets.QWidget()
        product_name_layout = QHBoxLayout()
        lb_product_name = QLabel("分類コード")
        lb_product_name.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_classification = QLabel("")
        self.txt_classification.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_classification.setStyleSheet(
            style_sheet.QLabelStyle1(border_width=1, border_radius=5, background_color="Gainsboro"))
        product_name_layout.addWidget(lb_product_name, 4, QtCore.Qt.AlignLeft)
        product_name_layout.addWidget(self.txt_classification, 6)
        product_name_widget.setLayout(product_name_layout)

        product_name_widget1 = QtWidgets.QWidget()
        product_name_layout1 = QHBoxLayout()
        lb_product_name1 = QLabel("終了日")
        lb_product_name1.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_product_name1 = QLabel("")
        self.txt_product_name1.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_product_name1.setStyleSheet(
            style_sheet.QLabelStyle1(border_width=1, border_radius=5, background_color="Gainsboro"))
        product_name_layout1.addWidget(lb_product_name1, 4, QtCore.Qt.AlignLeft)
        product_name_layout1.addWidget(self.txt_product_name1, 6)
        product_name_widget1.setLayout(product_name_layout1)

        product_name_widget2 = QtWidgets.QWidget()
        product_name_layout2 = QHBoxLayout()
        lb_product_name2 = QLabel("タイプ")
        lb_product_name2.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_product_name2 = QLabel("")
        self.txt_product_name2.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_product_name2.setStyleSheet(
            style_sheet.QLabelStyle1(border_width=1, border_radius=5, background_color="Gainsboro"))
        product_name_layout2.addWidget(lb_product_name2, 4, QtCore.Qt.AlignLeft)
        product_name_layout2.addWidget(self.txt_product_name2, 6)
        product_name_widget2.setLayout(product_name_layout2)

        product_name_widget3 = QtWidgets.QWidget()
        product_name_layout3 = QHBoxLayout()
        lb_product_name3 = QLabel("数")
        lb_product_name3.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_product_name3 = QLabel("")
        self.txt_product_name3.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_product_name3.setStyleSheet(
            style_sheet.QLabelStyle1(border_width=1, border_radius=5, background_color="Gainsboro"))
        product_name_layout3.addWidget(lb_product_name3, 4, QtCore.Qt.AlignLeft)
        product_name_layout3.addWidget(self.txt_product_name3, 6)
        product_name_widget3.setLayout(product_name_layout3)

        product_info_layout.addWidget(product_name_widget, 1, 1)
        product_info_layout.addWidget(product_name_widget1, 1, 2)
        product_info_layout.addWidget(product_name_widget2, 2, 1)
        product_info_layout.addWidget(product_name_widget3, 2, 2)
        product_info_widget.setLayout(product_info_layout)

        layout.addWidget(product_widget, 5)
        layout.addWidget(product_info_widget, 5)
        product_setting_widget.setLayout(layout)

        # endregion
        # region Camera setting widget
        camera_setting_widget = QGroupBox("カメラ設定")
        camera_setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())

        camera_setting_layout = QVBoxLayout()

        # Choose file Widget
        choose_file_widget = QtWidgets.QWidget()
        choose_file_layout = QHBoxLayout()

        self.txt_save_dir = QLineEdit()
        # self.txt_save_dir.setPlaceholderText("ローカルを使用する場合は空白のままにし、サーバーを使用する場合はsを入力してください。")
        self.txt_save_dir.setMaximumSize(900, 50)
        self.txt_save_dir.setStyleSheet(style_sheet.QLineEditStyle(font_size=16, height=50))
        #

        self.btn_show_folder = QPushButton()
        self.btn_show_folder.setIcon(QIcon("./data/resource/open-folder.png"))
        self.btn_show_folder.setIconSize(QtCore.QSize(50, 50))
        # common.set_shadow(self.btn_show_folder)
        self.btn_show_folder.setStyleSheet(style_sheet.QPushButtonStyle(font_size=20, ))
        self.btn_show_folder.clicked.connect(self.on_open_folder_click)
        #
        # choose_file_layout.addWidget(self.btn_choose_file)
        choose_file_layout.addWidget(self.txt_save_dir)
        choose_file_layout.addWidget(self.btn_show_folder)
        choose_file_widget.setLayout(choose_file_layout)

        btn_start_widget = QtWidgets.QWidget()
        btn_start_widget.setMaximumSize(900, 70)
        btn_start_layout = QHBoxLayout()
        lb_input_time = QLabel("時間入力")
        lb_input_time.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_set_limit_time = QLineEdit()
        self.txt_set_limit_time.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_set_limit_time.setText('15')
        self.txt_set_limit_time.setMaximumSize(70, 50)
        self.txt_set_limit_time.setStyleSheet(style_sheet.QLineEditStyle())

        lb_fps = QLabel("FPS")
        lb_fps.setStyleSheet(style_sheet.QLabelStyle())
        self.set_fps = QLineEdit()
        self.set_fps.setAlignment(QtCore.Qt.AlignCenter)
        self.set_fps.setText('25')
        self.set_fps.setMaximumSize(70, 50)
        self.set_fps.setStyleSheet(style_sheet.QLineEditStyle())

        self.lb_focus = QLabel("フォーカス")
        self.lb_focus.setStyleSheet(style_sheet.QLabelStyle())
        self.set_focus = QSlider(Qt.Horizontal)
        # self.set_focus.setGeometry(30, 40, 100, 30)
        self.set_focus.valueChanged.connect(self.on_set_focus_change_value)
        self.set_focus.setStyleSheet(style_sheet.QSliderStyle())

        btn_start_layout.addWidget(lb_input_time)
        btn_start_layout.addWidget(self.txt_set_limit_time)
        btn_start_layout.addWidget(lb_fps)
        btn_start_layout.addWidget(self.set_fps)
        btn_start_layout.addWidget(self.lb_focus)
        btn_start_layout.addWidget(self.set_focus)
        btn_start_widget.setLayout(btn_start_layout)

        camera_setting_layout.addWidget(choose_file_widget)
        camera_setting_layout.addWidget(btn_start_widget)
        camera_setting_widget.setLayout(camera_setting_layout)

        top_layout.addWidget(product_setting_widget, 6, QtCore.Qt.AlignVCenter)
        top_layout.addWidget(camera_setting_widget, 4, QtCore.Qt.AlignVCenter)
        top_widget.setLayout(top_layout)

        # endregion

        # region Camera widget
        camera_widget = QGroupBox()
        camera_widget.setStyleSheet(style_sheet.QGroupBoxStyle2())
        set_camera_layout = QGridLayout()

        # show frame of top camera
        self.camera1 = QLabel()
        self.camera1.setPixmap(common.get_bitmap_blank_image(mode=0))
        self.camera1.setScaledContents(True)
        self.signal_cm1.connect(self.camera1.setPixmap)

        # show frame of horizontal camera
        self.camera2 = QLabel()
        self.camera2.setPixmap(common.get_bitmap_blank_image(mode=0))
        self.camera2.setScaledContents(True)
        self.signal_cm2.connect(self.camera2.setPixmap)

        self.btn_swap_camera = QToolButton()
        self.btn_swap_camera.setIcon(QIcon("./data/resource/swap.png"))
        self.btn_swap_camera.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=0, padding_top=0))
        self.btn_swap_camera.setMaximumSize(50, 50)
        self.btn_swap_camera.clicked.connect(self.on_btn_swap_click)

        # show limit time of camera1
        self.top_camera_control_widget = QtWidgets.QWidget()
        top_camera_control_layout = QGridLayout()

        self.status = QLabel()
        self.status.setStyleSheet(style_sheet.QLabelStyle(text_color="red", font_size=20))

        self.btn_create_video1 = CustomQToolButton(set_text=False,
                                                   icon_path="./data/resource/play.png",
                                                   icon_size=(80, 80))
        self.btn_create_video1.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=30,
                                                                          padding_top=0,
                                                                          width=60,
                                                                          height=60))
        self.btn_create_video1.clicked.connect(self.on_btn_create_video1_click)

        self.btn_take_photo1 = CustomQToolButton(set_text=False, icon_path="./data/resource/focus.png",
                                                 icon_size=(50, 50))
        self.btn_take_photo1.setStyleSheet(
            style_sheet.QToolButtonStyle(border_radius=25, padding_top=0, width=50, height=50))
        self.btn_take_photo1.clicked.connect(self.on_take_photo1_click)

        self.time_label1 = QLabel("0s")
        self.time_label1.setStyleSheet(style_sheet.QLabelStyle(font_size=30))

        self.btn_open_folder_1 = QToolButton()
        self.btn_open_folder_1.setIcon(QIcon("./data/resource/open-folder.png"))
        self.btn_open_folder_1.setIconSize(QtCore.QSize(50, 50))
        common.set_shadow(self.btn_open_folder_1)
        self.btn_open_folder_1.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=25,
                                                                          padding_top=0,
                                                                          width=50,
                                                                          height=50))
        self.btn_open_folder_1.clicked.connect(self.on_open_folder_1_click)

        top_camera_control_layout.addWidget(self.status, 1, 1, QtCore.Qt.AlignLeft)
        top_camera_control_layout.addWidget(self.btn_create_video1, 1, 2)
        top_camera_control_layout.addWidget(self.btn_take_photo1, 1, 3)
        top_camera_control_layout.addWidget(self.btn_open_folder_1, 1, 4)
        top_camera_control_layout.addWidget(self.time_label1, 1, 5, QtCore.Qt.AlignRight)
        self.top_camera_control_widget.setLayout(top_camera_control_layout)

        self.hori_camera_control_widget = QtWidgets.QWidget()
        hori_camera_control_layout = QGridLayout()

        self.status2 = QLabel()
        self.status2.setStyleSheet(style_sheet.QLabelStyle(text_color="red", font_size=20))

        self.btn_create_video2 = QToolButton()
        common.set_shadow(self.btn_create_video2)
        self.btn_create_video2.setIcon(QIcon("./data/resource/play.png"))
        self.btn_create_video2.setIconSize(QtCore.QSize(80, 80))
        self.btn_create_video2.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=30,
                                                                          padding_top=0,
                                                                          width=60,
                                                                          height=60))
        self.btn_create_video2.clicked.connect(self.on_btn_create_video2_click)

        self.btn_take_photo2 = CustomQToolButton(set_text=False, icon_size=(50, 50),
                                                 icon_path="./data/resource/focus.png")
        self.btn_take_photo2.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=25,
                                                                        padding_top=0,
                                                                        width=50,
                                                                        height=50))
        self.btn_take_photo2.clicked.connect(self.on_take_photo2_click)

        self.time_label2 = QLabel("0s")
        self.time_label2.setStyleSheet(style_sheet.QLabelStyle(font_size=30))

        self.btn_open_folder_2 = CustomQToolButton(set_text=False, icon_size=(50, 50),
                                                   icon_path="./data/resource/open-folder.png")
        self.btn_open_folder_2.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=25,
                                                                          padding_top=0,
                                                                          width=50,
                                                                          height=50))
        self.btn_open_folder_2.clicked.connect(self.on_open_folder_2_click)

        hori_camera_control_layout.addWidget(self.status2, 1, 1, QtCore.Qt.AlignLeft)
        hori_camera_control_layout.addWidget(self.btn_create_video2, 1, 2)
        hori_camera_control_layout.addWidget(self.btn_take_photo2, 1, 3)
        hori_camera_control_layout.addWidget(self.btn_open_folder_2, 1, 4)
        hori_camera_control_layout.addWidget(self.time_label2, 1, 5, QtCore.Qt.AlignRight)
        self.hori_camera_control_widget.setLayout(hori_camera_control_layout)

        self.sw_open_camera = QSwitchButton()
        self.sw_open_camera.clicked.connect(self.on_sw_frame_click)

        lb_top = QLabel("上カメラ")
        lb_top.setStyleSheet(style_sheet.QLabelStyle())
        lb_yoko = QLabel("横カメラ")
        lb_yoko.setStyleSheet(style_sheet.QLabelStyle())

        set_camera_layout.addWidget(lb_top, 1, 1, QtCore.Qt.AlignCenter)
        set_camera_layout.addWidget(self.sw_open_camera, 1, 2, QtCore.Qt.AlignCenter)
        set_camera_layout.addWidget(lb_yoko, 1, 3, QtCore.Qt.AlignCenter)
        set_camera_layout.addWidget(self.camera1, 2, 1)
        set_camera_layout.addWidget(self.btn_swap_camera, 2, 2)
        set_camera_layout.addWidget(self.camera2, 2, 3)
        set_camera_layout.addWidget(self.top_camera_control_widget, 3, 1)
        set_camera_layout.addWidget(self.hori_camera_control_widget, 3, 3)
        camera_widget.setLayout(set_camera_layout)

        # endregion

        main_layout.addWidget(top_widget, 1, QtCore.Qt.AlignTop)
        main_layout.addWidget(camera_widget, 9, QtCore.Qt.AlignVCenter)
        main_widget.setLayout(main_layout)

        self.btn_back = QToolButton()
        self.btn_back.setMaximumSize(50, 50)
        self.btn_back.setContentsMargins(0, 0, 0, 0)
        self.btn_back.setIcon(QIcon("./data/resource/undo.png"))
        self.btn_back.setIconSize(QtCore.QSize(40, 40))
        common.set_shadow(self.btn_back)
        self.btn_back.setStyleSheet(style_sheet.QToolButtonStyle(border_radius=10,
                                                                 padding_top=0,
                                                                 width=50,
                                                                 height=50,
                                                                 ))
        self.create_video_layout.addWidget(self.btn_back, 1, QtCore.Qt.AlignTop)
        self.create_video_layout.addWidget(main_widget, 9, QtCore.Qt.AlignTop)
        self.setLayout(self.create_video_layout)

        self.init()

    def init(self):
        self.on_product_item_selected()
        self.widget_disable(self.top_camera_control_widget)
        self.widget_disable(self.hori_camera_control_widget)

    def get_product_list(self):
        pass

    def on_completer_selected(self):
        self.btn_product_checked = False
        self.sw_open_camera.setChecked(False)
        self.widget_disable(self.top_camera_control_widget)
        self.widget_disable(self.hori_camera_control_widget)
        self.is_open_camera = False
        self.product_code = self.line_edit.text().split("：")[0]
        self.product_type = None
        for cd in self.data:
            if cd["product_code"] == self.product_code:
                self.txt_classification.setText(cd["product_classification"])
                self.txt_product_name1.setText(cd["finnish_date"])
                if cd["cnt_product_single"] == "1":
                    self.product_type = "バラ"
                if cd["cnt_product_pack"] == "1":
                    self.product_type = "パーク"
                if cd["cnt_product_case"] == "1":
                    self.product_type = "ケース"
                self.txt_product_name2.setText(self.product_type)
                self.txt_product_name3.setText(cd["cnt_product_single"])
                break

    def on_btn_product_checked(self):
        self.btn_product_checked = False
        try:
            with open("./data/cls_nm_master_data.txt", 'r', encoding="UTF-8") as f1:
                for line1 in f1:
                    self.model_classes_name.append(str(line1.strip()))
            if len(self.line_edit.text()) == 0:
                return
            if len(self.cb_category.currentText()) == 0:
                return
            self.current_product_name_folder = self.product_code if self.product_code is not None else self.current_product_name_folder
            is_exist = False
            if self.model_classes_name is not None:
                for id in self.model_classes_name:
                    if id == self.product_code:
                        is_exist = True
            if is_exist:
                dlg = common.show_message_dialog("クラスIDが存在しています。動画を変更しますか？", OK="変更")
                if not dlg:
                    return
                fr_id = join(self.txt_save_dir.text(), self.product_code)
                os.makedirs(fr_id, exist_ok=True)
                self.fr_locate1 = join(fr_id, str(self.current_product_name_folder + "_01"))
                self.fr_locate2 = join(fr_id, str(self.current_product_name_folder + "_02"))
                self.fr_locate3 = join(fr_id, str(self.current_product_name_folder + "_03"))
                os.makedirs(self.fr_locate1, exist_ok=True)
                os.makedirs(self.fr_locate2, exist_ok=True)
                os.makedirs(self.fr_locate3, exist_ok=True)
                # if self.type=="単品" or self.type=="パーク":
                #     f,_=utils.file_proc.all_file_and_subdir_from_dir(self.fr_locate1)
                #     if len(f)==0:
                #
                #
            else:
                dlg = common.show_message_dialog("NEWクラスIDを追加します。よろしいでしょうか？", OK="追加")
                if not dlg:
                    return
                with open("./data/cls_nm_master_data.txt", 'a', encoding="UTF-8") as f:
                    f.write(self.line_edit.text().split("：")[0] + "\n")
                fr_id = join(self.txt_save_dir.text(), self.product_code)
                os.makedirs(fr_id, exist_ok=True)
                self.fr_locate1 = join(fr_id, str(self.current_product_name_folder + "_01"))
                self.fr_locate2 = join(fr_id, str(self.current_product_name_folder + "_02"))
                self.fr_locate3 = join(fr_id, str(self.current_product_name_folder + "_03"))
                os.makedirs(self.fr_locate1, exist_ok=True)
                os.makedirs(self.fr_locate2, exist_ok=True)
                os.makedirs(self.fr_locate3, exist_ok=True)

            self.btn_product_checked = True
            if self.product_type in ["バラ", "パーク"]:
                self.open_camera(mode=TOP)
                self.widget_enable(self.top_camera_control_widget)
                self.widget_disable(self.hori_camera_control_widget)
            elif self.product_type in ["ケース"]:
                self.open_camera(mode=YOKO)
                self.widget_enable(self.hori_camera_control_widget)
                self.widget_disable(self.top_camera_control_widget)
            elif self.product_type is None:
                self.open_camera(mode=None)
                self.widget_enable(self.top_camera_control_widget)
                self.widget_enable(self.hori_camera_control_widget)
        except Exception as e:
            LOGGER.error(e)

    def widget_disable(self, widget: QtWidgets.QWidget):
        widget.setEnabled(False)

    def widget_enable(self, widget: QtWidgets.QWidget):
        widget.setEnabled(True)

    def open_camera(self, widget_index=-1, mode=None):
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.is_open_camera = True
        if widget_index != -1:
            if widget_index == 0:
                t1 = threading.Thread(target=self.vid_cap_event,
                                      args=[int(self.arr_camera_indexes["TOP"]), self.signal_cm1, TOP])
                t1.start()
            elif widget_index == 1:
                t1 = threading.Thread(target=self.vid_cap_event,
                                      args=[int(self.arr_camera_indexes["YOKO"]), self.signal_cm2, YOKO])
                t1.start()

        elif len(self.arr_camera_indexes.keys()) >= 2:
            if mode is None:
                t1 = threading.Thread(target=self.vid_cap_event,
                                      args=[int(self.arr_camera_indexes["TOP"]), self.signal_cm1, TOP])
                t2 = threading.Thread(target=self.vid_cap_event,
                                      args=[int(self.arr_camera_indexes["YOKO"]), self.signal_cm2, YOKO])
                t1.start()
                t2.start()

            if mode == TOP:
                t1 = threading.Thread(target=self.vid_cap_event,
                                      args=[int(self.arr_camera_indexes["TOP"]), self.signal_cm1, TOP])
                t1.start()
            if mode == YOKO:
                t2 = threading.Thread(target=self.vid_cap_event,
                                      args=[int(self.arr_camera_indexes["YOKO"]), self.signal_cm2, YOKO])

                t2.start()

    def release_camera(self):
        self.is_open_camera = False
        time.sleep(1)

    def on_btn_swap_click(self):
        self.release_camera()
        if len(self.arr_camera_indexes.keys()) >= 2:
            if self.product_type is None:
                yoko = self.arr_camera_indexes["TOP"]
                self.arr_camera_indexes["TOP"] = self.arr_camera_indexes["YOKO"]
                self.arr_camera_indexes["YOKO"] = yoko
                # self.arr_camera_indexes = self.arr_camera_indexes[1], self.arr_camera_indexes[0]
                self.open_camera()
            if self.product_type in ["バラ", "パーク"]:
                yoko = self.arr_camera_indexes["TOP"]
                self.arr_camera_indexes["TOP"] = self.arr_camera_indexes["YOKO"]
                self.arr_camera_indexes["YOKO"] = yoko
                self.open_camera(self.camera_widget_indexes[0])
                self.widget_enable(self.top_camera_control_widget)
                self.widget_disable(self.hori_camera_control_widget)
            if self.product_type in ["ケース"]:
                yoko = self.arr_camera_indexes["TOP"]
                self.arr_camera_indexes["TOP"] = self.arr_camera_indexes["YOKO"]
                self.arr_camera_indexes["YOKO"] = yoko
                self.open_camera(self.camera_widget_indexes[1])
                self.widget_enable(self.hori_camera_control_widget)
                self.widget_disable(self.top_camera_control_widget)

        else:
            self.camera_widget_indexes = self.camera_widget_indexes[1], self.camera_widget_indexes[0]
            self.open_camera(self.camera_widget_indexes[0])

    def on_btn_create_video1_click(self):
        if not self.check_before(self.status):
            return
        if not self.save_vid1:
            self.save_vid1 = True
            self.time_started1 = time.time()
            self.btn_create_video1.setIcon(QIcon("./data/resource/stop-button.png"))
            self.btn_create_video1.setIconSize(QtCore.QSize(40, 40))
        else:
            self.time_started1 = 0
            self.time_label1.setText("0s")
            self.save_vid1 = False
            self.btn_create_video1.setIcon(QIcon("./data/resource/play.png"))
            self.btn_create_video1.setIconSize(QtCore.QSize(70, 70))

    def on_btn_create_video2_click(self):
        if not self.check_before(self.status2):
            return
        if not self.save_vid2:
            self.save_vid2 = True
            self.time_started2 = time.time()
            self.btn_create_video2.setIcon(QIcon("./data/resource/stop-button.png"))
            self.btn_create_video2.setIconSize(QtCore.QSize(40, 40))
        else:
            self.time_started2 = 0
            self.time_label2.setText("0s")
            self.save_vid2 = False
            self.btn_create_video2.setIcon(QIcon("./data/resource/play.png"))
            self.btn_create_video2.setIconSize(QtCore.QSize(70, 70))

    def set_emty(self):
        self.status.setText("")
        self.status2.setText("")

    def on_take_photo1_click(self):
        if not self.check_before(status=self.status):
            return
        self.take_photo1 = True
        self.status.setText("")
        self.status.setText("画像を保存しました。")
        try:
            QTimer.singleShot(3000, self.set_emty)
        except Exception as e:
            print(e)

    def on_take_photo2_click(self):
        if not self.check_before(status=self.status2):
            return
        self.take_photo2 = True
        self.status2.setText("")
        self.status2.setText("画像を保存しました。")
        try:
            QTimer.singleShot(3000, self.set_emty)
        except Exception as e:
            print(e)

    def on_open_folder_click(self):
        try:
            if self.txt_save_dir.text() is not None:
                print(self.txt_save_dir.text())
                os.startfile(self.txt_save_dir.text())
        except Exception as e:
            print(e)

        # os.startfile(join(os.getcwd(), "image_process"))

    def on_open_folder_1_click(self):
        if self.fr_locate1 is not None and len(self.fr_locate1) > 0:
            try:
                self.status.setText("")
                os.startfile(self.fr_locate1)
            except Exception as e:
                print(e)
        else:
            self.status.setText("商品確認ボタンをチェックしてください。")

    def on_open_folder_2_click(self):
        if self.fr_locate3 is not None and len(self.fr_locate3) > 0:
            try:
                self.status.setText("")
                os.startfile(self.fr_locate3)
            except Exception as e:
                print(e)
        else:
            self.status.setText("商品確認ボタンをチェックしてください。")

    def on_set_focus_change_value(self, value):
        self.current_focus = value
        self.lb_focus.setText("フォーカス %s " % value)

    def get_area(self):
        pass

    def on_sw_frame_click(self):

        if not self.btn_product_checked:
            return
        self.release_camera()
        common.show_loading(2000)
        if self.sw_open_camera.isChecked():
            self.open_camera(mode=None)
            self.widget_enable(self.top_camera_control_widget)
            self.widget_enable(self.hori_camera_control_widget)
        else:
            if self.product_type in ["バラ", "パーク"]:
                self.open_camera(mode=TOP)
                self.widget_enable(self.top_camera_control_widget)
                self.widget_disable(self.hori_camera_control_widget)
            elif self.product_type in ["ケース"]:
                self.open_camera(mode=YOKO)
                self.widget_enable(self.hori_camera_control_widget)
                self.widget_disable(self.top_camera_control_widget)
            elif self.product_type is None:
                self.open_camera(mode=None)
                self.widget_enable(self.top_camera_control_widget)
                self.widget_enable(self.hori_camera_control_widget)

    def on_product_item_selected(self):
        if self.cb_category.currentText() == "":
            self.txt_save_dir.setText("")
            return
        try:
            if len(self.txt_save_dir.text()) == 0:
                self.isServer = False
                self.root = join(os.getcwd(), "image_process", "video")
                print(self.root)
            elif self.txt_save_dir.text() == "s" or self.txt_save_dir.text() == "S":
                self.root = join(r"\\192.168.0.241\yakult_project", "image_process", "video")
                self.isServer = True
            else:
                if not self.isServer:
                    self.root = join(os.getcwd(), "image_process", "video")
                    self.isServer = False
            path = None
            if self.cb_category.currentText() == "ヤクルト":
                path = join(self.root, "yakult")
            if self.cb_category.currentText() == "化粧":
                path = join(self.root, "cosmetic")
            if self.cb_category.currentText() == "食品":
                path = join(self.root, "food")

            os.makedirs(path, exist_ok=True)
            self.txt_save_dir.setText("")
            self.txt_save_dir.setText(path)
        except Exception as e:
            print(e)

    def set_camera_indexes(self):
        r = common.get_camera_indexes()
        self.arr_camera_indexes, self.box = r[0], r[1]

    def get_camera_indexes(self):
        return self.arr_camera_indexes

    def choose_folder_dialog(self):
        file = QFileDialog.getExistingDirectory(self, "フォルダ選択", os.getcwd())
        f = file.replace('/', '\\')
        self.txt_save_dir.setText(f)

    def check_before(self, status: QLabel):
        is_ok = True
        if len(self.cb_category.currentText()) == 0:
            status.setText("製品のタイプを選んでください!")
            is_ok = False
        if len(self.line_edit.text()) == 0:
            status.setText("製品のコードを選んでください!")
            is_ok = False

        if self.fr_locate1 is None or len(self.fr_locate1) == 0:
            self.status.setText("商品確認ボタンをチェックしてください。")
            is_ok = False
        if self.fr_locate3 is None or len(self.fr_locate3) == 0:
            self.status.setText("商品確認ボタンをチェックしてください。")
            is_ok = False
        return is_ok

    def vid_cap_event(self, source0, signal, is_camera):
        LOGGER.info(f"OPEN CAMERA {is_camera}")
        cap = cv2.VideoCapture(source0, cv2.CAP_DSHOW)
        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
        except Exception as e:
            LOGGER.error(e)
        f_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        f_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"{f_width}x{f_height}")
        ratio = float(960 / f_width)

        # fourcc for AVI
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        # fourcc for MP4
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = None
        while True:
            r, frame = cap.read()
            if not r:
                cap.release()
                LOGGER.info(f"{is_camera} RELEASED -- r")
                break
            if not self.is_open_camera:
                cap.release()
                signal.emit(common.get_bitmap_blank_image(mode=1))
                LOGGER.info(f"{is_camera} RELEASED -- is_open_camera")
                break
            cap.set(cv2.CAP_PROP_FOCUS, int(self.current_focus))
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)

            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
            signal.emit((QPixmap.fromImage(img)))

            # camera.setPixmap((QPixmap.fromImage(img)))
            if is_camera == TOP:
                if self.save_vid1:
                    if writer is None:
                        if self.txt_save_dir.text() is None:
                            self.txt_save_dir.setText(os.getcwd())
                        now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        writer = cv2.VideoWriter(join(self.fr_locate1,
                                                      f"{self.current_product_name_folder}_01-{now}.avi"), fourcc,
                                                 int(self.set_fps.text()) if self.set_fps is not None else 15,
                                                 (self.box[2], self.box[3]) if self.box is not None else (
                                                     f_height - 200, f_height - 200))
                        # check_list, _ = utils.file_proc.all_file_and_subdir_from_dir(self.fr_locate1)
                        # if len(check_list) == 0:
                        #     now=datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        #
                        #     writer = cv2.VideoWriter(join(self.fr_locate1,
                        #                                   f"{self.current_product_name_folder}_01-{}.avi"), fourcc,
                        #                              int(self.set_fps.text()) if self.set_fps is not None else 15,
                        #                              (self.box[2], self.box[3]) if self.box is not None else (
                        #                                  f_height - 200, f_height - 200))
                        #     print(f"{self.box[2]}x{self.box[3]}")
                        # else:
                        #     writer = cv2.VideoWriter(
                        #         join(self.fr_locate1,
                        #              f"{self.current_product_name_folder}_01-{len(check_list) + 1}.avi"),
                        #         fourcc,
                        #         int(self.set_fps.text()) if self.set_fps is not None else 15,
                        #         (self.box[2], self.box[3]) if self.box is not None else (
                        #             f_height - 200, f_height - 200))

                    if writer is not None:
                        if time.time() - self.time_started1 <= int(self.txt_set_limit_time.text()):
                            self.time_label1.setText(f"{int(time.time() - self.time_started1)}s")
                            try:
                                if self.box is not None:
                                    crop = frame[self.box[1]:self.box[1] + self.box[3],
                                           self.box[0]:self.box[0] + self.box[2]]
                                else:
                                    crop = frame[100:f_height - 100,
                                           abs(f_width - f_height) // 2 + 100: abs(
                                               f_width - f_height) // 2 + (f_height - 100)]
                                writer.write(crop)
                            except Exception as e:
                                LOGGER.error(e)
                        else:
                            self.save_vid1 = False
                            writer.release()
                            writer = None
                            self.btn_create_video1.setIcon(QIcon("./data/resource/play.png"))
                            self.btn_create_video1.setIconSize(QtCore.QSize(70, 70))
                            self.time_label1.setText('0s')
                if not self.save_vid1:
                    if writer is not None:
                        writer.release()
                        writer = None
                if self.take_photo1:
                    if self.box is not None:
                        img_crop = frame[self.box[1]:self.box[1] + self.box[3],
                                   self.box[0]:self.box[0] + self.box[2]]
                    else:
                        img_crop = frame[100:f_height - 100,
                                   abs(f_width - f_height) // 2 + 100: abs(
                                       f_width - f_height) // 2 + (f_height - 100)]
                    photo_now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    cv2.imwrite(join(self.fr_locate1, f"{self.current_product_name_folder}_01-{photo_now}.png"),
                                img_crop)
                    # check_list, _ = utils.file_proc.all_file_and_subdir_from_dir(self.fr_locate1)
                    # cv2.imwrite(join(self.fr_locate1, f"{self.current_product_name_folder}_01-{1}.png"),
                    #             img_crop) if len(check_list) == 0 else cv2.imwrite(
                    #     join(self.fr_locate1, f"{self.current_product_name_folder}_01-{len(check_list) + 1}.png"),
                    #     img_crop)

                    self.take_photo1 = False

            if is_camera == YOKO:

                if self.save_vid2:
                    if writer is None:
                        if self.txt_save_dir.text() is None:
                            self.txt_save_dir.setText(os.getcwd())
                        now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        writer = cv2.VideoWriter(join(self.fr_locate3,
                                                      f"{self.current_product_name_folder}_03-{now}.avi"), fourcc,
                                                 int(self.set_fps.text()) if self.set_fps is not None else 15,
                                                 (f_height - 200, f_height - 200))
                        # check_list, _ = utils.file_proc.all_file_and_subdir_from_dir(self.fr_locate3)
                        # if len(check_list) == 0:
                        #
                        #     writer = cv2.VideoWriter(
                        #         join(self.fr_locate3, f"{self.current_product_name_folder}_03-{1}.avi"),
                        #         fourcc,
                        #         int(self.set_fps.text()) if self.set_fps is not None else 15,
                        #         (self.box[2], self.box[3]) if self.box is not None else (
                        #             f_height - 200, f_height - 200))
                        # else:
                        #     writer = cv2.VideoWriter(
                        #         join(self.fr_locate3,
                        #              f"{self.current_product_name_folder}_03-{len(check_list) + 1}.avi"),
                        #         fourcc,
                        #         int(self.set_fps.text()) if self.set_fps is not None else 15,
                        #         (self.box[2], self.box[3]) if self.box is not None else (
                        #             f_height - 200, f_height - 200))

                    if writer is not None:
                        if time.time() - self.time_started2 <= int(self.txt_set_limit_time.text()):
                            self.time_label2.setText(f"{int(time.time() - self.time_started2)}s")
                            try:
                                crop = frame[100:f_height - 100,
                                       abs(f_width - f_height) // 2 + 100: abs(
                                           f_width - f_height) // 2 + (f_height - 100)]
                                writer.write(crop)
                            except Exception as e:
                                LOGGER.error(e)
                        else:
                            self.save_vid2 = False
                            writer.release()
                            writer = None
                            self.btn_create_video2.setIcon(QIcon("./data/resource/play.png"))
                            self.btn_create_video2.setIconSize(QtCore.QSize(70, 70))
                            self.time_label2.setText('0s')
                if not self.save_vid2:
                    if writer is not None:
                        writer.release()
                        writer = None
                if self.take_photo2:
                    # img_crop = frame[100:f_height - 300,
                    #            abs(f_width - f_height) // 2 + 50: abs(
                    #                f_width - f_height) // 2 + (f_height - 50)]
                    photo_now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    cv2.imwrite(join(self.fr_locate3, f"{self.current_product_name_folder}_03-{photo_now}.png"),
                                frame)
                    # check_list, _ = utils.file_proc.all_file_and_subdir_from_dir(self.fr_locate3)
                    # cv2.imwrite(join(self.fr_locate3, f"{self.current_product_name_folder}_03-{1}.png"),
                    #             img_crop) if len(check_list) == 0 else cv2.imwrite(
                    #     join(self.fr_locate3, f"{self.current_product_name_folder}_03-{len(check_list) + 1}.png"),
                    #     img_crop)
                    self.take_photo2 = False
