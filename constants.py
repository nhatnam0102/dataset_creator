import glob
import shutil
import cv2
import random
import numpy as np
from rembg import remove
from threading import Thread
import threading
import time
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import logging
from logging import *

ROOT = '/home/upc/WorkSpaces/nam/yakult_project/image_fol/'
ROOT1 = '/home/upc/WorkSpaces/nam/yakult_project/'
SLASH = '/'
UNDERLINE = '-'
JPG = '.jpg'
PNG = '.png'
TXT = '.txt'
PACK = ['0004', '0007', '0010', '0013', '0016', '0019', '0022', '0024', '0026', '0029', '0032', '0035']
PACK_UE = ['0004', '0007', '0010', '0013', '0016', '0019', '0026', '0029', '0032']
CASE = ['0005', '0008', '0011', '0014', '0017', '0020', '0027', '0030', '0033']
A1 = ['01']
A2 = ['02']
A3 = ['03']
A12 = ['01', '02']
A13 = ['01', '03']
A23 = ['02', '03']
A123 = ['01', '02', '03']
TAN_TO_PACK = {'0': '1', '2': '3', '5': '6', '8': '9', '11': '12', '14': '15', '17': '18', '24': '25', '27': '28',
               '30': '31'}
TOP = "TOP"
YOKO = "YOKO"
NUM = 10
join = os.path.join
basename = os.path.basename


def set_logging(log_name,
                file_log_name,
                formatter="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    # Format with pathname and lineno
    # formatter=Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] %(message)s]')

    # Save log to file
    # f_handler = FileHandler(join(os.getcwd(), "data", "log", file_log_name))
    # f_handler.setLevel(logging.INFO)
    # f_handler.setFormatter(Formatter(formatter))
    # logger.addHandler(f_handler)

    # Show log in terminal(for DEBUG)
    s_handler = StreamHandler()
    s_handler.setLevel(logging.INFO)
    s_handler.setFormatter(Formatter(formatter))

    logger.addHandler(s_handler)

    return logger


# LOGGER
LOGGER = set_logging("DATASET GENERATOR", "mylog.log")
