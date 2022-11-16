from PyQt5 import QtSvg

from constants import *
from utils import common, style_sheet


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        main_layout = QVBoxLayout()

        intro_widget = QGroupBox()
        common.set_shadow(intro_widget)
        intro_widget.setStyleSheet(
            style_sheet.QGroupBoxStyle3(background_color_start="SteelBlue", background_color_end="PowderBlue", border_width=0,
                                        border_radius=20, ))

        intro_layout = QHBoxLayout()

        intro_text_widget = QtWidgets.QWidget()
        intro_text_layout = QVBoxLayout()

        intro1 = QLabel("DATASET GENERATOR")
        intro1.setStyleSheet(style_sheet.QLabelStyle(text_color="black", font_size=100))

        intro2 = QLabel("AIを簡単にする")
        intro2.setStyleSheet(style_sheet.QLabelStyle(text_color="black", font_size=60))

        intro3 = QLabel("Ultimate Project Company")
        intro3.setStyleSheet(style_sheet.QLabelStyle(text_color="black", font_size=40))

        intro_text_layout.addWidget(intro1, 0, QtCore.Qt.AlignTop)
        intro_text_layout.addWidget(intro2, 0, QtCore.Qt.AlignTop)
        intro_text_layout.addWidget(intro3, 0, QtCore.Qt.AlignBottom)

        intro_text_widget.setLayout(intro_text_layout)

        intro_svg_widget = QtSvg.QSvgWidget("./data/resource/ai.svg")
        intro_layout.addWidget(intro_text_widget, 0, QtCore.Qt.AlignLeft)
        intro_layout.addWidget(intro_svg_widget, 0, QtCore.Qt.AlignRight)
        intro_widget.setLayout(intro_layout)

        control_widget = QtWidgets.QWidget()
        control_layout = QHBoxLayout()

        self.btnCreateVideo = QToolButton()
        self.btnCreateVideo.setText("動画作成")
        self.btnCreateVideo.setIcon(QIcon("./data/resource/video_2.png"))
        self.btnCreateVideo.setIconSize(QSize(100, 100))
        self.btnCreateVideo.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        common.set_shadow(self.btnCreateVideo)
        self.btnCreateVideo.setStyleSheet(
            style_sheet.QToolButtonStyle(background_color="white", text_color="black", padding_top=30, font_size=30))
        self.btnCreateVideo.setMaximumSize(250, 250)
        self.btnCreateVideo.setMinimumSize(100, 100)

        self.btnCreateDataset = QToolButton()
        self.btnCreateDataset.setText("DATASET作成")
        self.btnCreateDataset.setIcon(QIcon("./data/resource/create_dataset.png"))
        self.btnCreateDataset.setIconSize(QSize(100, 100))
        self.btnCreateDataset.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        common.set_shadow(self.btnCreateDataset)
        self.btnCreateDataset.setStyleSheet(
            style_sheet.QToolButtonStyle(background_color="white", text_color="black", padding_top=30, font_size=30))
        self.btnCreateDataset.setMaximumSize(250, 250)
        self.btnCreateDataset.setMinimumSize(100, 100)

        self.btn_ai_start = QToolButton()
        self.btn_ai_start.setText("AI開始")
        self.btn_ai_start.setIcon(QIcon("./data/resource/ai_start.png"))
        self.btn_ai_start.setIconSize(QSize(100, 100))
        self.btn_ai_start.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        common.set_shadow(self.btn_ai_start)
        self.btn_ai_start.setStyleSheet(
            style_sheet.QToolButtonStyle(background_color="white", text_color="black", padding_top=30, font_size=30))
        self.btn_ai_start.setMaximumSize(250, 250)
        self.btn_ai_start.setMinimumSize(100, 100)
        common.set_shadow(self.btn_ai_start)

        self.setting = QToolButton()
        self.setting.setText("設定")
        self.setting.setIcon(QIcon("./data/resource/settings.png"))
        self.setting.setIconSize(QSize(100, 100))
        self.setting.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        common.set_shadow(self.setting)

        self.setting.setStyleSheet(
            style_sheet.QToolButtonStyle(background_color="white", text_color="black", padding_top=30, font_size=30))
        self.setting.setMaximumSize(250, 250)
        self.setting.setMinimumSize(100, 100)

        control_layout.addWidget(self.btnCreateVideo)
        control_layout.addWidget(self.btnCreateDataset)
        control_layout.addWidget(self.btn_ai_start)
        control_layout.addWidget(self.setting)

        control_widget.setLayout(control_layout)

        main_layout.addWidget(intro_widget)
        main_layout.addWidget(control_widget)

        self.setLayout(main_layout)
