from Class.compressor import MockUp as Compressor
from Class.lakeshore import MockUp as LakeShore
import logging
from logging.handlers import TimedRotatingFileHandler
import Class.Loggers as Logs
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PySide6.QtGui import QBrush,QColor,QTransform
from PySide6.QtCore import Qt,QTimer
import time



rate = 1
num_of_points= 1024*3
updateTimer = QTimer()

def btn_press():
    global rate, num_of_points
    rate = float(poll_rate.text())
    updateTimer.setInterval(rate*1000)
    num_of_points = float(num_of_points_line.text())

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

num_of_points_line = QtWidgets.QLineEdit()
num_of_points_line.setText(str(num_of_points))
settings_form.addRow("num. of points: ", num_of_points_line)

SettingsVBOX.addLayout(settings_form)
settingsBtn = QtWidgets.QPushButton("Set")
settingsBtn.clicked.connect(btn_press)
SettingsVBOX.addWidget(settingsBtn)



plot_layout = QtWidgets.QVBoxLayout()
Hor_layout.addLayout(plot_layout)

pressure_plot = pg.PlotWidget(symbol='o',symbolBrush=(0,0,200),axisItems = {'bottom': pg.DateAxisItem()})
TemperatureA_plot = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})
TemperatureB_plot = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})
plot_layout.addWidget(pressure_plot)
pressure_curve = pressure_plot.plot()
firstStage_curve = TemperatureA_plot.plot()
sectStage_curve = TemperatureB_plot.plot()
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



win.show()





monitoring_formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
monitoring_headers = 'Compressor pressure (psi) - Water Temperature (C) - first stage (K) -  second stage (K)'
monitoring_backup = "C:/Users/Scienta Omicron/OneDrive - Technion/ARPES Data/Monitoring"
physLogger = Logs.MyLogger('monitoring', "./logs/Monitoring/monitoring.log", logging.INFO, 'midnight', 1, 30,
                           monitoring_formatter, monitoring_headers, monitoring_backup)


Time = []
pressures = []
firstStages = []
secStages = []
def update_all():
    global pressure_curve,sectStage_curve,firstStage_curve
    if len(Time) > num_of_points:
        Time.pop(0)
        pressures.pop(0)
        firstStages.pop(0)
        secStages.pop(0)


    now = time.time()
    Time.append(now)

    pressure = compressor.read_pressure()
    pressureValue.setText(str(round(pressure,2)))
    pressures.append(pressure)
    pressure_curve.setData(Time,pressures)

    waterTemp = compressor.read_water_temperature()
    WaterTempLine.setText(str(round(waterTemp,2)))


    firstStg = lakeshore.TemperatureA()
    firstStageLine.setText(str(round(firstStg,2)))
    firstStages.append(firstStg)
    firstStage_curve.setData(Time,firstStages)

    secStg = lakeshore.TemperatureB()
    secStageLine.setText(str(round(secStg,2)))
    secStages.append(secStg)
    sectStage_curve.setData(Time,secStages)

    all_phys = "{0} - {1} - {2} - {3}".format(str(pressure),str(waterTemp),str(firstStg),str(secStg))
    physLogger.logger.info(all_phys)




if __name__ == "__main__":
    updateTimer.timeout.connect(update_all)
    updateTimer.start(rate*1000)
    pg.exec()