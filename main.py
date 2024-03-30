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
SettingsVBOX = QtWidgets.QVBoxLayout()
Settings_group.setLayout(SettingsVBOX)




monitor_group = QtWidgets.QGroupBox("Monitor")
monitor_group.setStyleSheet("QGroupBox{font: 12px;}")
MonitorVbox = QtWidgets.QVBoxLayout()
monitor_group.setLayout(MonitorVbox)
Ver_layout.addWidget(monitor_group)
Ver_layout.addWidget(Settings_group)

settings_form = QtWidgets.QFormLayout()
poll_rate = QtWidgets.QLineEdit()
poll_rate.setText("3.6")
settings_form.addRow("polling rate: (s)", poll_rate)
SettingsVBOX.addLayout(settings_form)

plot_layout = QtWidgets.QVBoxLayout()
Hor_layout.addLayout(plot_layout)

pressure_plot = pg.PlotWidget()
TemperatureA_plot = pg.PlotWidget()
TemperatureB_plot = pg.PlotWidget()
plot_layout.addWidget(pressure_plot)
plot_layout.addWidget(TemperatureA_plot)
plot_layout.addWidget(TemperatureB_plot)


values_form = QtWidgets.QFormLayout()
pressureValue = QtWidgets.QLineEdit()
pressureValue.setEnabled(False)
pressureValue.setText("120")
values_form.addRow("pressure (psi):", pressureValue)

WaterTemp = QtWidgets.QLineEdit()
WaterTemp.setEnabled(False)
WaterTemp.setText("12")
values_form.addRow("water temp. (C):", WaterTemp)


firstStage = QtWidgets.QLineEdit()
firstStage.setEnabled(False)
firstStage.setText("41.2")
values_form.addRow("1st stage (K):", firstStage)


secStage = QtWidgets.QLineEdit()
secStage.setEnabled(False)
secStage.setText("3.6")
values_form.addRow("2nd stage (K):", secStage)

MonitorVbox.addLayout(values_form)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


win.show()

def update_all():
    pass




if __name__ == "__main__":
    pg.exec()