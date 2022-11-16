from datetime import date
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from constants import *
from utils import common, style_sheet
from widget.create_video_widget import CreateVideoWidget
from widget.right_widget import RightWidget

from constants import (ROOT, LOGGER, ROOT1, SLASH, UNDERLINE, JPG, PNG, TXT, PACK,
                       PACK_UE, A1, A2, A3, A12, A23, A13, CASE, A123, TAN_TO_PACK, join, basename)


class CreateDatasetWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateDatasetWidget, self).__init__()
        self.frame_per_second = None
        self.list_product = None
        self.root_path = None
        self.image_per_thread = None
        self.image_start_value = None
        self.sw_frame = None
        self.btn_show_product_insert = None
        self.btn_show_product_update = None
        self.mode_insert_product = None
        self.mode_update_product = None
        self.image_amount = None
        self.txt_resize_value1 = None
        self.txt_resize_value2 = None
        self.cb_category = None
        self.list_products = None
        self.current_product_name_folder = None
        self.current_product_name = None
        self.current_product_index = None
        self.start_create_dataset = None
        self.btn_show_folder = None
        self.txtSaveDir = None
        self.chooseFile = None
        self.path = None
        self.create_ui()

    def create_ui(self):
        parent_layout = QHBoxLayout()
        self.btn_back = QToolButton()
        self.btn_back.setIcon(QIcon("./data/resource/undo.png"))
        common.set_shadow(self.btn_back)
        self.btn_back.setStyleSheet(style_sheet.QToolButtonStyle(style_sheet.QToolButtonStyle(border_radius=20,
                                                                                              padding_top=0,
                                                                                              width=40,
                                                                                              height=40)))
        parent_layout.addWidget(self.btn_back, 0, QtCore.Qt.AlignTop)

        main_widget = QtWidgets.QWidget()
        # main_widget.setStyleSheet(style_sheet.QGroupBoxStyle1(border_width=0))
        main_layout = QVBoxLayout()

        # chooseFileWidget = QtWidgets.QWidget()
        # chooseFileLayout = QHBoxLayout()
        # self.chooseFile = QPushButton('フォルダ選択')
        # common.set_shadow(self.chooseFile)
        # self.chooseFile.setMaximumSize(300, 50)
        # self.chooseFile.setStyleSheet(style_sheet.QPushButtonStyle())
        # self.chooseFile.clicked.connect(self.choose_folder_dialog)
        # self.txtSaveDir = QTextEdit("")
        # self.txtSaveDir.setMaximumSize(800, 50)
        # self.txtSaveDir.setStyleSheet(style_sheet.QTextEditStyle())
        #
        # self.btn_show_folder = QPushButton("フォルダ開く")
        # common.set_shadow(self.btn_show_folder)
        # self.btn_show_folder.setStyleSheet(style_sheet.QPushButtonStyle())
        # self.btn_show_folder.setMaximumSize(300, 50)
        # self.btn_show_folder.clicked.connect(self.on_open_folder_click)
        #
        # chooseFileLayout.addWidget(self.chooseFile, 1, QtCore.Qt.AlignVCenter)
        # chooseFileLayout.addWidget(self.txtSaveDir, 8, QtCore.Qt.AlignVCenter)
        # chooseFileLayout.addWidget(self.btn_show_folder, 1, QtCore.Qt.AlignLeft)
        # chooseFileWidget.setLayout(chooseFileLayout)

        setting_mode_widget = QGroupBox()
        # common.set_shadow(setting_mode_widget)
        setting_mode_widget.setStyleSheet(style_sheet.QGroupBoxStyle1())
        setting_mode_layout = QGridLayout()

        product_type_widget = QtWidgets.QWidget()
        product_type = QHBoxLayout()
        lb_category = QLabel("分類:")
        lb_category.setStyleSheet(style_sheet.QLabelStyle())
        self.cb_category = QComboBox()
        self.cb_category.setStyleSheet(style_sheet.QComboBoxStyle())
        self.cb_category.adjustSize()
        self.cb_category.addItems(['ヤクルト', '化粧', '食品'])
        self.cb_category.activated.connect(self.on_product_item_selected)
        product_type.addWidget(lb_category)
        product_type.addWidget(self.cb_category)
        product_type_widget.setLayout(product_type)

        self.mode_update_product = QCheckBox('製品交換')
        self.mode_update_product.setStyleSheet(style_sheet.QCheckBoxStyle())
        self.mode_update_product.stateChanged.connect(self.on_cb_product_mode_checked)

        self.mode_insert_product = QCheckBox('製品追加')
        self.mode_insert_product.setStyleSheet(style_sheet.QCheckBoxStyle())
        self.mode_insert_product.stateChanged.connect(self.on_cb_product_mode_checked)

        self.btn_show_product_update = QPushButton("製品交換のリスト")
        self.btn_show_product_update.clicked.connect(self.show_list_product_update)
        self.btn_show_product_update.setStyleSheet(style_sheet.QPushButtonStyle(background_color="Coral"))

        self.btn_show_product_insert = QPushButton("製品追加のリスト")
        self.btn_show_product_insert.clicked.connect(self.show_list_product_insert)
        self.btn_show_product_insert.setStyleSheet(style_sheet.QPushButtonStyle(background_color="Coral"))

        setting_mode_layout.addWidget(product_type_widget, 1, 1)
        setting_mode_layout.addWidget(self.mode_update_product, 1, 2)
        setting_mode_layout.addWidget(self.btn_show_product_update, 1, 3)
        setting_mode_layout.addWidget(self.mode_insert_product, 2, 2)
        setting_mode_layout.addWidget(self.btn_show_product_insert, 2, 3)
        setting_mode_widget.setLayout(setting_mode_layout)

        parameter_setting_widget = QtWidgets.QWidget()
        parameter_setting_widget.setMaximumHeight(300)
        parameter_setting_layout = QHBoxLayout()

        extract_setting_widget = QGroupBox("Extract setting")
        common.set_shadow(extract_setting_widget)
        extract_setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())

        extract_setting_layout = QGridLayout()

        lb_frame_per_second = QLabel("Turn on Frame ")
        self.frame_per_second = QTextEdit("10")
        self.frame_per_second.setMaximumHeight(50)
        self.frame_per_second.setStyleSheet(style_sheet.QTextEditStyle())

        extract_setting_layout.addWidget(lb_frame_per_second, 1, 1)
        extract_setting_layout.addWidget(self.frame_per_second, 1, 2)
        extract_setting_widget.setLayout(extract_setting_layout)

        remove_background_setting_widget = QGroupBox("Remove background setting")
        remove_background_setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())

        merge_setting_widget = QGroupBox("Merge setting")
        common.set_shadow(merge_setting_widget)
        merge_setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())
        merge_setting_layout = QGridLayout()
        lbl_image_amount = QLabel("Image amount")
        lbl_image_amount.setStyleSheet(style_sheet.QLabelStyle())
        self.image_amount = QTextEdit("10")
        self.image_amount.setMaximumHeight(50)
        self.image_amount.setStyleSheet(style_sheet.QTextEditStyle())

        lbl_image_start_value = QLabel("Image start value")
        lbl_image_start_value.setStyleSheet(style_sheet.QLabelStyle())
        self.image_start_value = QTextEdit("1")
        self.image_start_value.setMaximumHeight(50)
        self.image_start_value.setStyleSheet(style_sheet.QTextEditStyle())

        lbl_image_per_thread = QLabel("Image per thread")
        lbl_image_per_thread.setStyleSheet(style_sheet.QLabelStyle())
        self.image_per_thread = QTextEdit("2")
        self.image_per_thread.setMaximumHeight(50)
        self.image_per_thread.setStyleSheet(style_sheet.QTextEditStyle())

        merge_setting_layout.addWidget(lbl_image_amount, 1, 1)
        merge_setting_layout.addWidget(self.image_amount, 1, 2)
        merge_setting_layout.addWidget(lbl_image_start_value, 2, 1)
        merge_setting_layout.addWidget(self.image_start_value, 2, 2)
        merge_setting_layout.addWidget(lbl_image_per_thread, 3, 1)
        merge_setting_layout.addWidget(self.image_per_thread, 3, 2)

        merge_setting_widget.setLayout(merge_setting_layout)

        cut_and_resize_setting_widget = QGroupBox("Resize setting")
        common.set_shadow(cut_and_resize_setting_widget)
        cut_and_resize_setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())
        cut_and_resize_setting_layout = QGridLayout()
        lbl_resize_value1 = QLabel("Resize value 1")
        lbl_resize_value1.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_resize_value1 = QTextEdit("0")
        self.txt_resize_value1.setMaximumHeight(50)
        self.txt_resize_value1.setStyleSheet(style_sheet.QTextEditStyle())
        lbl_resize_value2 = QLabel("Resize value 2")
        lbl_resize_value2.setStyleSheet(style_sheet.QLabelStyle())
        self.txt_resize_value2 = QTextEdit("0")
        self.txt_resize_value2.setMaximumHeight(50)
        self.txt_resize_value2.setStyleSheet(style_sheet.QTextEditStyle())
        cut_and_resize_setting_layout.addWidget(lbl_resize_value1, 1, 1)
        cut_and_resize_setting_layout.addWidget(self.txt_resize_value1, 1, 2)
        cut_and_resize_setting_layout.addWidget(lbl_resize_value2, 2, 1)
        cut_and_resize_setting_layout.addWidget(self.txt_resize_value2, 2, 2)
        cut_and_resize_setting_widget.setLayout(cut_and_resize_setting_layout)

        self.start_create_dataset = QPushButton("データセット作成")
        common.set_shadow(self.start_create_dataset)
        self.start_create_dataset.setStyleSheet(style_sheet.QPushButtonStyle())
        self.start_create_dataset.clicked.connect(self.on_start_create_dataset_click)

        parameter_setting_layout.addWidget(extract_setting_widget)
        # parameter_setting_layout.addWidget(remove_background_setting_widget)
        parameter_setting_layout.addWidget(cut_and_resize_setting_widget)
        parameter_setting_layout.addWidget(merge_setting_widget)
        parameter_setting_widget.setLayout(parameter_setting_layout)

        # main_layout.addWidget(chooseFileWidget)
        main_layout.addWidget(setting_mode_widget)
        main_layout.addWidget(parameter_setting_widget)
        main_layout.addWidget(self.start_create_dataset, 0, QtCore.Qt.AlignVCenter)

        main_widget.setLayout(main_layout)

        parent_layout.addWidget(main_widget)
        self.setLayout(parent_layout)
        self.init()

    def init(self):
        self.on_product_item_selected()
        common.set_opacity_off(self.btn_show_product_update)
        common.set_opacity_off(self.btn_show_product_insert)

    def on_sw_frame_click(self):
        if self.sw_frame.isChecked():
            print("checked")
        else:
            print("unchecked")

    def show_list_product_update(self):
        create_video_widget = CreateVideoWidget()
        print(create_video_widget.yakult.list_update_products)
        try:
            dlg = QDialog()
            dlg.setWindowTitle("LIST")
            dlg.setFixedSize(350, 700)
            dialogLayout = QVBoxLayout()

            listWidget = QListWidget()
            listWidget.setMinimumSize(300, 600)

            btnClose = QDialogButtonBox.Close
            dlg.btnBox = QDialogButtonBox(btnClose)
            dlg.btnBox.setMaximumSize(70, 40)
            dlg.btnBox.button(QDialogButtonBox.Close).setText("選択")
            dlg.btnBox.setStyleSheet(style_sheet.QPushButtonStyle())

            dlg.btnBox.rejected.connect(dlg.close)
            if self.cb_category.currentText() == "ヤクルト":
                self.list_products = create_video_widget.yakult.list_update_products
            if self.cb_category.currentText() == "化粧":
                self.list_products = create_video_widget.cosmetic.list_update_products
            if self.cb_category.currentText() == "食品":
                self.list_products = create_video_widget.food.list_update_products

            listWidget.addItems(self.list_products)
            dialogLayout.addWidget(listWidget, 0, QtCore.Qt.AlignCenter)
            dialogLayout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)
            dlg.setLayout(dialogLayout)
            dlg.exec()

        except Exception as e:
            print(e)

        pass

    def show_list_product_insert(self):
        create_video_widget = CreateVideoWidget()
        try:
            dlg = QDialog()
            dlg.setWindowTitle("LIST")
            dlg.setFixedSize(350, 700)
            dialogLayout = QVBoxLayout()

            listWidget = QListWidget()

            listWidget.setMinimumSize(300, 600)

            btnClose = QDialogButtonBox.Close
            dlg.btnBox = QDialogButtonBox(btnClose)
            dlg.btnBox.setMaximumSize(70, 40)
            dlg.btnBox.button(QDialogButtonBox.Close).setText("選択")
            dlg.btnBox.setStyleSheet(style_sheet.QPushButtonStyle())

            dlg.btnBox.rejected.connect(dlg.close)
            if self.cb_category.currentText() == "ヤクルト":
                self.list_products = create_video_widget.yakult.list_insert_products
            if self.cb_category.currentText() == "化粧":
                self.list_products = create_video_widget.cosmetic.list_insert_products
            if self.cb_category.currentText() == "食品":
                self.list_products = create_video_widget.food.list_insert_products

            listWidget.addItems(self.list_products)
            dialogLayout.addWidget(listWidget, 0, QtCore.Qt.AlignCenter)
            dialogLayout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)
            dlg.setLayout(dialogLayout)
            dlg.exec()

        except Exception as e:
            print(e)

        pass

    def on_start_create_dataset_click(self):
        # common.show_message_dialog1("準備中")
        t1 = threading.Thread(target=self.create_dataset_event)
        t1.start()

    def create_dataset_event(self):
        # extract video
        try:
            # path_dir, path_save = common.get_path(self.cb_category, "video", "extracted")
            # check_list, _ = utils.file_proc.all_file_and_subdir_from_dir(path_dir)
            # if len(check_list) == 0:
            #     common.show_message_dialog1("動画が見つけられません！")
            #     return

            # TODO check list product
            #
            with open("./data/class_names_by_id.txt", 'r', encoding="UTF-8") as f:
                list_yakult = [line.strip() for line in f]
            # common.extract_video_thread(path_dir, path_save, list_yakult,
            #                             int(self.frame_per_second.toPlainText()) if self.frame_per_second is not None else 10)
            #
            # # remove background
            # path_dir, path_save = common.get_path(self.cb_category, "extracted", "removed")
            # common.remove_background_thread(path_dir, path_save, list_yakult)
            #
            # # cut and save
            # path_dir, path_save = common.get_path(self.cb_category, "removed", "processed")
            # common.cut_save_thread(path_dir, path_save, list_yakult,
            #                        resize1=float(
            #                            self.txt_resize_value1.toPlainText()) if self.txt_resize_value1.toPlainText() is not None else 0.3,
            #                        resize2=float(
            #                            self.txt_resize_value2.toPlainText()) if self.txt_resize_value2.toPlainText() is not None else 0.7)
            # # merge
            # path_dir, path_save = common.get_path(self.cb_category, "processed", "merged")
            # path_back = join(os.getcwd(), "image_process", "background")
            #
            # # merge
            # common.merged_image_thread(path_dir,
            #                            path_back,
            #                            path_save,
            #                            max_value=int(
            #                                self.image_amount.toPlainText()) if self.image_amount.toPlainText() is not None else 2000,
            #                            min_value=int(
            #                                self.image_start_value.toPlainText()) if self.image_start_value.toPlainText() is not None else 1,
            #                            value_per_thread=int(
            #                                self.image_per_thread.toPlainText()) if self.image_per_thread.toPlainText() is not None else 10,
            #                            merge_only=True)

            # create image_process
            dataset_path = join(os.getcwd(), "dataset")
            dataset_name = join(dataset_path, "dataset" + "_" + str(date.today().strftime("%Y%m%d")))
            remove_path = join(dataset_path, "dataset" + "_" + str(date.today().strftime("%Y%m%d")) + "_remove")
            os.makedirs(dataset_name, exist_ok=True)
            os.makedirs(remove_path, exist_ok=True)
            # common.check_dataset(path_save, remove_path)
            M_MODEL = 0.67, 0.75
            common.init_config(dataset_name, basename(dataset_name), len(list_yakult), list_yakult, M_MODEL)
            # common.create_dataset(dataset_name, path_save, path_back)
        except Exception as e:
            print(e)

    def on_open_folder_click(self):
        # if self.txtSaveDir.toPlainText() is not None:
        os.startfile(self.path)

    def choose_folder_dialog(self):
        file = QFileDialog.getExistingDirectory(self, "フォルダ選択", os.getcwd())
        # self.txtSaveDir.setPlainText(file)

    def show_list_product_dialog(self):
        try:
            dlg = QDialog()
            dlg.setWindowTitle("LIST")
            dlg.setFixedSize(350, 700)
            dialogLayout = QVBoxLayout()

            self.list_product = RightWidget()
            self.list_product.setMinimumSize(300, 600)

            btnClose = QDialogButtonBox.Close
            dlg.btnBox = QDialogButtonBox(btnClose)
            dlg.btnBox.setMaximumSize(70, 40)
            dlg.btnBox.button(QDialogButtonBox.Close).setText("選択")
            dlg.btnBox.setStyleSheet(style_sheet.QPushButtonStyle())

            dlg.btnBox.rejected.connect(dlg.close)
            dialogLayout.addWidget(self.list_product, 0, QtCore.Qt.AlignCenter)
            dialogLayout.addWidget(dlg.btnBox, 0, QtCore.Qt.AlignCenter)
            dlg.setLayout(dialogLayout)
            dlg.exec()
            self.current_product_index, self.current_product_name, self.current_product_name_folder = self.list_product.get_current_item()
            self.txt_product_name_id.setText(
                "・クラス: %s   ・製品名: %s    ・フォルダ名 : %s" % (self.list_product.get_current_item()))
        except Exception as e:
            print(e)

    def on_select_product_clicked(self):
        self.show_list_product_dialog()
        pass

    def on_product_item_selected(self):
        path = None
        self.root_path = join(os.getcwd(), "image_process", "extracted")
        if self.cb_category.currentText() == "ヤクルト":
            path = join(self.root_path, "yakult")
        if self.cb_category.currentText() == "化粧":
            path = join(self.root_path, "cosmetic")

        if self.cb_category.currentText() == "食品":
            path = join(self.root_path, "food")

        if path is not None:
            os.makedirs(path, exist_ok=True)
            self.path = path
            # self.txtSaveDir.setPlainText("")
            # self.txtSaveDir.setPlainText(path)

    def on_cb_product_mode_checked(self, state):
        if state == Qt.Checked:
            common.set_opacity_on(self.btn_show_product_update)
            common.set_opacity_on(self.btn_show_product_insert)

            if self.sender() == self.mode_update_product:
                self.mode_update_product.setChecked(True)
                common.set_opacity_on(self.btn_show_product_update)

                self.mode_insert_product.setChecked(False)
                common.set_opacity_off(self.btn_show_product_insert)

            elif self.sender() == self.mode_insert_product:
                self.mode_insert_product.setChecked(True)
                common.set_opacity_on(self.btn_show_product_insert)

                common.set_opacity_off(self.btn_show_product_update)
                self.mode_update_product.setChecked(False)
            else:
                self.mode_update_product.setChecked(False)
                self.mode_insert_product.setChecked(False)

                common.set_opacity_off(self.btn_show_product_update)
                common.set_opacity_off(self.btn_show_product_insert)

    def on_cb_product_type_checked(self, state):

        if state == Qt.Checked:

            if self.sender() == self.cbProduct:
                self.cbProductPack.setChecked(False)
                self.cbProductCase.setChecked(False)

            elif self.sender() == self.cbProductPack:
                self.cbProduct.setChecked(False)
                self.cbProductCase.setChecked(False)

            elif self.sender() == self.cbProductCase:
                self.cbProduct.setChecked(False)
                self.cbProductPack.setChecked(False)
