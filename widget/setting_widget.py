from constants import *
from utils import common, style_sheet


class SettingWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SettingWidget, self).__init__()
        main = QVBoxLayout()
        self.btn_back = QPushButton()
        self.btn_back.setIcon(QIcon("./data/resource/undo.png"))
        self.btn_back.setMaximumSize(60, 60)
        common.set_shadow(self.btn_back)
        self.btn_back.setStyleSheet(
            style_sheet.QPushButtonStyle(border_radius=20, background_color="white", text_color="black"))

        lb_setting = QLabel("設定")
        lb_setting.setStyleSheet(style_sheet.QLabelStyle(font_size=40))
        setting_widget = QGroupBox()
        setting_widget.setStyleSheet(style_sheet.QGroupBoxStyle())
        seting_layout = QVBoxLayout()

        choose_file_widget = QtWidgets.QWidget()
        choose_file_layout = QHBoxLayout()
        self.btn_choose_file = QPushButton('フォルダ選択')
        common.set_shadow(self.btn_choose_file)
        # self.btn_choose_file.setMaximumSize(200, 50)
        self.btn_choose_file.setStyleSheet(style_sheet.QPushButtonStyle())
        self.btn_choose_file.clicked.connect(self.choose_folder_dialog)

        self.txt_save_dir = QTextEdit("")
        self.txt_save_dir.setMinimumSize(800, 50)
        self.txt_save_dir.setMaximumSize(1900, 50)
        self.txt_save_dir.setStyleSheet(style_sheet.QTextEditStyle())
        choose_file_layout.addWidget(self.txt_save_dir,9,QtCore.Qt.AlignLeft)
        choose_file_layout.addWidget(self.btn_choose_file,1,QtCore.Qt.AlignLeft)
        choose_file_widget.setLayout(choose_file_layout)

        #
        seting_layout.addWidget(choose_file_widget)
        setting_widget.setLayout(seting_layout)

        main.addWidget(self.btn_back)
        main.addWidget(lb_setting)
        main.addWidget(setting_widget)
        self.setLayout(main)

    def choose_folder_dialog(self):
        file = QFileDialog.getExistingDirectory(self, "フォルダ選択", os.getcwd())
        f = file.replace('/', '\\')
        self.txt_save_dir.setPlainText(f)
