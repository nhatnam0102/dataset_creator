import sys
import time
import xlrd
import json
from datetime import datetime

from widget.create_dataset_widget import *
from widget.init_widget import InitWidget
from widget.left_widget import *
from widget.main_widget import *
from widget.setting_widget import *
from widget.toast_notification import *
from widget.action_widget import *

import utils


class CreatorForm(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CreatorForm, self).__init__(*args, **kwargs)
        self.create_dataset_widget = None
        self.main_widget = None
        self.create_video_widget = None
        self.create_dataset = None
        self.create_video = None
        self.Intro = None
        self.center_widget = None
        self.left_widget = None
        self.main_layout = None
        self.central = None
        self.center = None
        self.camera_exist = None
        self.setWindowTitle("Dataset Creator")
        self.setMinimumSize(1600, 900)
        self.create_ui()

    def create_ui(self):

        # self.setStyleSheet("background-color: white;")
        self.central = QStackedWidget()
        # self.central.setStyleSheet("background-color: white;")
        int_widget = InitWidget()
        self.main_widget = MainWidget()
        self.main_widget.btnCreateVideo.clicked.connect(self.on_create_video_click)
        self.main_widget.btnCreateDataset.clicked.connect(self.on_create_dataset_click)
        self.main_widget.btn_ai_start.clicked.connect(self.on_create_ai_click)
        self.main_widget.setting.clicked.connect(self.on_setting_click)

        self.create_video_widget = CreateVideoWidget()
        self.create_video_widget.btn_back.clicked.connect(self.on_back_btn_click)

        self.create_dataset_widget = CreateDatasetWidget()
        self.create_dataset_widget.btn_back.clicked.connect(self.on_back_btn_click)

        self.action_widget = ActionWidget()

        self.setting = SettingWidget()
        self.setting.btn_back.clicked.connect(self.on_back_btn_click)

        self.central.addWidget(int_widget)
        self.central.addWidget(self.main_widget)
        self.central.addWidget(self.create_video_widget)
        self.central.addWidget(self.create_dataset_widget)
        self.central.addWidget(self.action_widget)
        self.central.addWidget(self.setting)
        self.setCentralWidget(self.central)

        self.init()

    def closeEvent(self, event):
        # close = QtWidgets.QMessageBox.question(self,
        #                                        "QUIT",
        #                                        "Are you sure want to stop process?",
        #                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # if close == QtWidgets.QMessageBox.Yes:
        #     event.accept()
        #     self.create_video_widget.release_camera()
        # else:
        #     event.ignore()
        dlg = QDialog()
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout()
        dlg_widget = QGroupBox("報告")
        dlg_widget.setStyleSheet(utils.style_sheet.QGroupBoxStyle1(border_width=2))
        dlg_layout = QVBoxLayout()
        mes = QLabel("Are you sure want to stop process?")
        mes.setStyleSheet(utils.style_sheet.QLabelStyle())
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.btnBox = QDialogButtonBox(btn)
        dlg.btnBox.button(QDialogButtonBox.Cancel).setText("Cancel")
        dlg.btnBox.button(QDialogButtonBox.Ok).setText("OK")
        dlg.btnBox.setStyleSheet(utils.style_sheet.QPushButtonStyle(height=40, width=60, font_size=15, border_radius=5))
        common.set_shadow(dlg.btnBox)

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
            self.create_video_widget.release_camera()
            event.accept()
        else:
            event.ignore()

    def init(self):
        t1 = threading.Thread(target=self.transfer_form, args=[])
        t1.start()

    def transfer_form(self):
        # pass
        if self.central.currentIndex() == 0:
            self.create_video_widget.set_camera_indexes()
            self.central.setCurrentIndex(1)

    def on_create_video_click(self):
        try:
            if self.central.currentIndex() != 2:
                if len(self.create_video_widget.get_camera_indexes().keys()) > 0:
                    common.show_loading(time_dur=1000)
                    # self.create_video_widget.open_camera()
                    self.central.setCurrentIndex(2)
                else:
                    common.show_message_dialog1("Camera is unavailable ! ")
                    return

        except Exception as e:
            print(e)

    def on_setting_click(self):
        self.create_video_widget.set_camera_indexes()
        # common.show_message_dialog1("開発中")
        # try:
        #     if self.central.currentIndex() != 4:
        #         self.central.setCurrentIndex(4)
        #
        # except Exception as e:
        #     print(e)

    def on_create_ai_click(self):
        try:
            if self.central.currentIndex() != 4:
                self.central.setCurrentIndex(4)

        except Exception as e:
            print(e)
        # common.show_message_dialog("クラスIDが存在しています。動画を変更しますか？")
        # corner = QtCore.Qt.Corner(self.cornerCombo.currentData())
        # toast = QToaster()
        # toast.showMessage(parent=self, message="ada",icon=QtWidgets.QStyle.SP_MessageBoxCritical, corner=corner, desktop=False, timeout=2000, closable=False)

        # try:
        #     if self.central.currentIndex() != 4:
        #         self.central.setCurrentIndex(4)
        #
        # except Exception as e:
        #     print(e)

    def on_back_btn_click(self):
        try:
            if self.central.currentIndex() != 1:
                self.create_video_widget.release_camera()
                self.central.setCurrentIndex(1)


        except Exception as e:
            print(e)

    def on_create_dataset_click(self):
        try:
            if self.central.currentIndex() != 3:
                self.central.setCurrentIndex(3)

        except Exception as e:
            print(e)

    def get_master_data(self):

        master_data = xlrd.open_workbook_xls("./data/master_data.xls", )
        sheet = master_data.sheet_by_index(0)
        col_finnish_date = -1
        col_product_code = -1
        col_product_name = -1
        col_product_classification = -1
        col_product_single = -1
        col_product_pack = -1
        col_product_case = -1
        for i in range(sheet.ncols):
            if sheet.cell_value(0, i) == "商品詳細期間終了日":
                col_finnish_date = i
            if sheet.cell_value(0, i) == "表示商品コード":
                col_product_code = i
            if sheet.cell_value(0, i) == "商品名":
                col_product_name = i
            if sheet.cell_value(0, i) == "商品分類コード":
                col_product_classification = i
            if sheet.cell_value(0, i) == "ケース換算数":
                col_product_case = i
            if sheet.cell_value(0, i) == "パック換算数":
                col_product_pack = i
            if sheet.cell_value(0, i) == "バラ換算数":
                col_product_single = i

        product_indexes = []
        for j in range(1, sheet.nrows, 1):
            finnish_date_value = int(sheet.cell_value(j, col_finnish_date))
            date_str = str(finnish_date_value)
            str2date = datetime.strptime(date_str, '%Y%m%d')
            if str2date > datetime.today():
                product_indexes.append(j)

        product_dic = []

        for row in product_indexes:
            product = common.Product()
            product.set(str(int(sheet.row_values(row)[col_finnish_date])),
                        str(int(sheet.row_values(row)[col_product_code])) if
                        type(sheet.row_values(row)[col_product_code]) == float else str(
                            sheet.row_values(row)[col_product_code]),
                        sheet.row_values(row)[col_product_name],
                        sheet.row_values(row)[col_product_classification],
                        str(int(sheet.row_values(row)[col_product_single])),
                        str(int(sheet.row_values(row)[col_product_pack])),
                        str(int(sheet.row_values(row)[col_product_case]))
                        )
            product_dic.append(product.get())

        with open("./data/json/master_data.json", "w", encoding="utf8") as json_f:
            json.dump([data for data in product_dic], json_f, indent=2, ensure_ascii=False)
        pass


def show_form():
    app = QApplication(sys.argv)

    window = CreatorForm()
    window.showMaximized()

    sys.exit(app.exec())
