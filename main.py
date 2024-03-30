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
win.resize(600,400)
win.setWindowTitle('RGC monitoring')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)



Hor_layout =  QtWidgets.QHBoxLayout()
cw.setLayout(Hor_layout)

Ver_layout = QtWidgets.QVBoxLayout()
Hor_layout.addLayout(Ver_layout)

Settings_group = QtWidgets.QGroupBox("Settings")
Settings_group.setStyleSheet("QGroupBox{font: 12px;}")
vbox = QtWidgets.QVBoxLayout()
Settings_group.setLayout(vbox)

Ver_layout.addWidget(Settings_group)


monitor_group = QtWidgets.QGroupBox("Monitor")
monitor_group.setStyleSheet("QGroupBox{font: 12px;}")
vbox = QtWidgets.QVBoxLayout()
monitor_group.setLayout(vbox)
Ver_layout.addWidget(monitor_group)



plot_layout = QtWidgets.QVBoxLayout()
Hor_layout.addLayout(plot_layout)

pressure_plot = pg.PlotWidget()
TemperatureA_plot = pg.PlotWidget()
TemperatureB_plot = pg.PlotWidget()
plot_layout.addWidget(pressure_plot)
plot_layout.addWidget(TemperatureA_plot)
plot_layout.addWidget(TemperatureB_plot)



formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


win.show()

def update_all():
    pass




if __name__ == '__main__':
    pg.exec()