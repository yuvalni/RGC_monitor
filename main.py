from Class.compressor import MockUp as Compressor
from Class.lakeshore import MockUp as LakeShore
import logging
from logging.handlers import TimedRotatingFileHandler

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PySide6.QtGui import QBrush,QColor,QTransform
from PySide6.QtCore import Qt,QTimer




rate = 1
updateTimer = QTimer()
def btn_press():
    global rate
    rate = float(poll_rate.text())
    updateTimer.setInterval(rate*1000)
    print(rate)

lakeshore = LakeShore()
compressor = Compressor() 

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
Ver_layout.addStretch()
Ver_layout.addWidget(Settings_group)

settings_form = QtWidgets.QFormLayout()
poll_rate = QtWidgets.QLineEdit()
poll_rate.setText(str(rate))
settings_form.addRow("polling rate: (s)", poll_rate)
SettingsVBOX.addLayout(settings_form)
settingsBtn = QtWidgets.QPushButton("Set")
settingsBtn.clicked.connect(btn_press)
SettingsVBOX.addWidget(settingsBtn)



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

WaterTempLine = QtWidgets.QLineEdit()
WaterTempLine.setEnabled(False)
WaterTempLine.setText("12")
values_form.addRow("water temp. (C):", WaterTempLine)


firstStageLine = QtWidgets.QLineEdit()
firstStageLine.setEnabled(False)
firstStageLine.setText("41.2")
values_form.addRow("1st stage (K):", firstStageLine)


secStageLine = QtWidgets.QLineEdit()
secStageLine.setEnabled(False)
secStageLine.setText("3.6")
values_form.addRow("2nd stage (K):", secStageLine)

MonitorVbox.addLayout(values_form)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


win.show()




def update_all():
    pressure = compressor.read_pressure()
    pressureValue.setText(str(round(pressure,2)))


    waterTemp = compressor.read_water_temperature()
    WaterTempLine.setText(str(round(waterTemp,2)))

    firstStg = lakeshore.TemperatureA()
    firstStageLine.setText(str(round(firstStg,2)))

    secStg = lakeshore.TemperatureB()
    secStageLine.setText(str(round(secStg,2)))




if __name__ == "__main__":
    updateTimer.timeout.connect(update_all)
    updateTimer.start(rate*1000)
    pg.exec()