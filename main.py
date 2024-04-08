from Class.compressor import Compressor as Compressor
from Class.lakeshore import Lakeshore as LakeShore
#from Class.compressor import MockUp as Compressor
#from Class.lakeshore import MockUp as LakeShore
import logging
from logging.handlers import TimedRotatingFileHandler
import Class.Loggers as Logs
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PySide6.QtGui import QBrush,QColor,QTransform
from PySide6.QtCore import Qt,QTimer,QObject, QThread,Signal
from threading import Thread
import time
from time import sleep





rate = 5
num_of_points= 1000
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

def clear_graph():
    global pressures,firstStages,secStages,Time
    Time = []
    pressures = []
    firstStages = []
    secStages = []


clear_graph_Btn = QtWidgets.QPushButton("clear graph")
clear_graph_Btn.clicked.connect(clear_graph)
SettingsVBOX.addWidget(clear_graph_Btn)



plot_layout = QtWidgets.QVBoxLayout()
Hor_layout.addLayout(plot_layout)

pressure_plot = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})
pressure_plot.addLegend(offset=(0,0))
#pressure_plot.setDownsampling(ds=True,auto=True,mode="subsample")

TemperatureA_plot = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})
TemperatureA_plot.setXLink(pressure_plot)
TemperatureA_plot.addLegend(offset=(0,0))
#TemperatureA_plot.setDownsampling(ds=True,auto=True,mode="subsample")

TemperatureB_plot = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})
TemperatureB_plot.setXLink(pressure_plot)
TemperatureB_plot.addLegend(offset=(0,0))
#TemperatureB_plot.setDownsampling(ds=True,auto=True,mode="subsample")

plot_layout.addWidget(pressure_plot)

#pressure_curve = pressure_plot.plot(pen=pg.mkPen('k', width=2),symbolBrush=(0,0,0),symbolSize = 5,symbol ='o',name="compressor pressure")
pressure_curve = pressure_plot.plot(pen=pg.mkPen('k', width=2),name="compressor pressure")
#firstStage_curve = TemperatureA_plot.plot(pen=(0,0,0),symbolBrush=(0,0,0),symbolSize = 5,symbol ='p',name="1st stage")
firstStage_curve = TemperatureA_plot.plot(pen=(0,0,0),name="1st stage")
sectStage_curve = TemperatureB_plot.plot(pen=(0,0,0),name="2nd stage")

plot_layout.addWidget(TemperatureA_plot)
plot_layout.addWidget(TemperatureB_plot)


values_form = QtWidgets.QFormLayout()
pressureValue = QtWidgets.QLineEdit()
pressureValue.setEnabled(False)
pressureValue.setText("")
values_form.addRow("pressure (psi):", pressureValue)

WaterTempInLine = QtWidgets.QLineEdit()
WaterTempInLine.setEnabled(False)
WaterTempInLine.setText("")
values_form.addRow("water temp. in (C):", WaterTempInLine)

WaterTempOutLine = QtWidgets.QLineEdit()
WaterTempOutLine.setEnabled(False)
WaterTempOutLine.setText("")
values_form.addRow("water temp. out (C):", WaterTempOutLine)

He_capsuleTempLine = QtWidgets.QLineEdit()
He_capsuleTempLine.setEnabled(False)
He_capsuleTempLine.setText("")
values_form.addRow("He capsule temp. (C):", He_capsuleTempLine)


firstStageLine = QtWidgets.QLineEdit()
firstStageLine.setEnabled(False)
firstStageLine.setText("")
values_form.addRow("1st stage (K):", firstStageLine)


secStageLine = QtWidgets.QLineEdit()
secStageLine.setEnabled(False)
secStageLine.setText("")
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
    print("update started")
    global pressure_curve,sectStage_curve,firstStage_curve
    global Time,pressures,firstStages,secStages
    while True:
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
        try:
            pressure_curve.setData(Time,pressures)
        except Exception:
            pass
        He_capsule,waterTempOut,waterTempIn = compressor.read_water_temperature()
        WaterTempOutLine.setText(str(round(waterTempOut,2)))
        WaterTempInLine.setText(str(round(waterTempIn, 2)))
        He_capsuleTempLine.setText(str(round(He_capsule, 2)))

        firstStg = lakeshore.read_TemperatureA()
        firstStageLine.setText(str(round(firstStg,2)))
        firstStages.append(firstStg)
        try:
            firstStage_curve.setData(Time,firstStages)
        except Exception:
            pass

        secStg = lakeshore.read_TemperatureB()
        secStageLine.setText(str(round(secStg,2)))
        secStages.append(secStg)
        try:
            sectStage_curve.setData(Time,secStages)
        except Exception:
            pass


        all_phys = "{0} - {1} - {2} - {3} - {4} - {5}".format(str(pressure),str(waterTempIn),str(waterTempOut),str(He_capsule),str(firstStg),str(secStg))
        physLogger.logger.info(all_phys)

        sleep(rate)





if __name__ == "__main__":
    update_thread = Thread(target=update_all,daemon=True)
    update_thread.start()
    #updateTimer.timeout.connect(update_thread.run)
    #updateTimer.start(rate*1000)
    pg.exec()
