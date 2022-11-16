import json

import utils.file_proc
from constants import *
from utils import common, style_sheet
from utils.common import LOGGER


class CustomQToolButton(QToolButton):
    def __init__(self, text="",
                 set_text=True,
                 set_icon=True,
                 shadow=True,
                 icon_path="",
                 icon_size=(30, 30),
                 ):
        super().__init__()
        if set_text:
            self.setText(text)
        if set_icon:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QtCore.QSize(icon_size[0], icon_size[1]))
        if shadow:
            common.set_shadow(self)
