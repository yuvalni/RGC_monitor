from Class.compressor import MockUp
import logging
from logging.handlers import TimedRotatingFileHandler

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PySide6.QtGui import QBrush,QColor,QTransform
from PySide6.QtCore import Qt


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

app = pg.mkQApp("RGC monitor")

win = QtWidgets.QMainWindow()
win.resize(1600,800)
win.setWindowTitle('nano-ARPES spatial map')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)

Hor_layout =  QtWidgets.QHBoxLayout()

cw.setLayout(Hor_layout)


root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def update_all():
    pass




if __name__ == '__main__':
    pg.exec()