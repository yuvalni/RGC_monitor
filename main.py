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
from PySide6.QtCore import Qt,QObject,Signal
from threading import Thread, Lock
import time
from time import sleep

import datetime



class MainWindow(QtWidgets.QMainWindow):
    update_graph_signal = Signal()

    def __init__(self):
        super().__init__()
        self.vector_lock = Lock()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.lakeshore = LakeShore()
        self.compressor = Compressor()
        self.rate = 5
        self.num_of_points = 100

        self.Time = []
        self.pressures = []
        self.firstStages = []
        self.secStages = []


        self.update_graph_signal.connect(self.update_graph)
        self.monitoring_formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        self.monitoring_headers = 'Compressor pressure (psi) - Water Temperature (C) - first stage (K) -  second stage (K)'
        self.monitoring_backup = "C:/Users/Scienta Omicron/OneDrive - Technion/ARPES Data/Monitoring"
        self.physLogger = Logs.MyLogger('monitoring', "./logs/Monitoring/monitoring.log", logging.INFO, 'midnight', 1, 30,
                               monitoring_formatter, monitoring_headers, monitoring_backup)

        self.createLayout()

    def createLayout(self):
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)


        Hor_layout =  QtWidgets.QHBoxLayout()
        cw.setLayout(Hor_layout)

        Ver_layout = QtWidgets.QVBoxLayout()
        Hor_layout.addLayout(Ver_layout)


        self.LED = QtWidgets.QRadioButton()
        self.LED.setEnabled(False)
        self.LED.setText("Reading")
        self.LED.setStyleSheet("QRadioButton::indicator:checked"
                                        "{"
                                        "background-color : lightgreen"
                                        "}"
                        "QRadioButton::indicator:unchecked"
                        "{"
                        "background-color : red"
                        "}"
                        )

        Ver_layout.addWidget(self.LED)

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

        self.poll_rate = QtWidgets.QLineEdit()
        self.poll_rate.setText(str(self.rate))
        settings_form.addRow("polling rate: (s)", self.poll_rate)

        self.num_of_points_line = QtWidgets.QLineEdit()
        self.num_of_points_line.setText(str(self.num_of_points))
        settings_form.addRow("num. of points: ", self.num_of_points_line)

        SettingsVBOX.addLayout(settings_form)

        settingsBtn = QtWidgets.QPushButton("Set")
        settingsBtn.clicked.connect(self.btn_press)
        SettingsVBOX.addWidget(settingsBtn)


        clear_graph_Btn = QtWidgets.QPushButton("clear graph")
        clear_graph_Btn.clicked.connect(self.clear_graph)
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
        self.pressure_curve = pressure_plot.plot(pen=(0,0,0),name="compressor pressure")
        #firstStage_curve = TemperatureA_plot.plot(pen=(0,0,0),symbolBrush=(0,0,0),symbolSize = 5,symbol ='p',name="1st stage")
        self.firstStage_curve = TemperatureA_plot.plot(pen=(0,0,0),name="1st stage")
        self.sectStage_curve = TemperatureB_plot.plot(pen=(0,0,0),name="2nd stage")

        plot_layout.addWidget(TemperatureA_plot)
        plot_layout.addWidget(TemperatureB_plot)


        values_form = QtWidgets.QFormLayout()
        self.pressureValue = QtWidgets.QLineEdit()
        self.pressureValue.setEnabled(False)
        self.pressureValue.setText("")
        values_form.addRow("pressure (psi):", self.pressureValue)

        self.WaterTempInLine = QtWidgets.QLineEdit()
        self.WaterTempInLine.setEnabled(False)
        self.WaterTempInLine.setText("")
        values_form.addRow("water temp. in (C):", self.WaterTempInLine)

        self.WaterTempOutLine = QtWidgets.QLineEdit()
        self.WaterTempOutLine.setEnabled(False)
        self.WaterTempOutLine.setText("")
        values_form.addRow("water temp. out (C):", self.WaterTempOutLine)

        self.He_capsuleTempLine = QtWidgets.QLineEdit()
        self.He_capsuleTempLine.setEnabled(False)
        self.He_capsuleTempLine.setText("")
        values_form.addRow("He capsule temp. (C):", self.He_capsuleTempLine)


        self.firstStageLine = QtWidgets.QLineEdit()
        self.firstStageLine.setEnabled(False)
        self.firstStageLine.setText("")
        values_form.addRow("1st stage (K):", self.firstStageLine)


        self.secStageLine = QtWidgets.QLineEdit()
        self.secStageLine.setEnabled(False)
        self.secStageLine.setText("")
        values_form.addRow("2nd stage (K):", self.secStageLine)

        MonitorVbox.addLayout(values_form)

    def btn_press(self):
        self.rate = float(self.poll_rate.text())
        self.num_of_points = float(self.num_of_points_line.text())

    def clear_graph(self):
        self.vector_lock.acquire()
        self.Time = []
        self.pressures = []
        self.firstStages = []
        self.secStages = []
        self.vector_lock.release()


    def update_graph(self):
        self.vector_lock.acquire()
        try:
            self.pressure_curve.setData(self.Time,self.pressures)
            self.firstStage_curve.setData(self.Time,self.firstStages)
            self.sectStage_curve.setData(self.Time,self.secStages)
        except Exception as e:
            print(e)
        self.vector_lock.release()





    def update_all(self):
        print("update started")
        while True:
            self.vector_lock.acquire()
            self.LED.setChecked(True)
            if len(self.Time) > self.num_of_points:
                self.Time.pop(0)
                self.pressures.pop(0)
                self.firstStages.pop(0)
                self.secStages.pop(0)


            now = time.time()
            self.Time.append(now)
            self.LED.setChecked(True)
            pressure = self.compressor.read_pressure()
            self.LED.setChecked(False)
            self.pressureValue.setText(str(round(pressure,2)))
            self.pressures.append(pressure)

            self.LED.setChecked(True)
            He_capsule,waterTempOut,waterTempIn = self.compressor.read_water_temperature()
            self.LED.setChecked(False)
            self.WaterTempOutLine.setText(str(round(waterTempOut,2)))
            self.WaterTempInLine.setText(str(round(waterTempIn, 2)))
            self.He_capsuleTempLine.setText(str(round(He_capsule, 2)))
            self.LED.setChecked(True)
            firstStg = self.lakeshore.read_TemperatureA()
            self.LED.setChecked(False)
            self.firstStageLine.setText(str(round(firstStg,2)))
            self.firstStages.append(firstStg)

            self.LED.setChecked(True)
            secStg = self.lakeshore.read_TemperatureB()
            self.LED.setChecked(False)
            self.secStageLine.setText(str(round(secStg,2)))
            self.secStages.append(secStg)


            all_phys = "{0} - {1} - {2} - {3} - {4} - {5}".format(str(pressure),str(waterTempIn),str(waterTempOut),str(He_capsule),str(firstStg),str(secStg))
            self.physLogger.logger.info(all_phys)
            self.LED.setChecked(False)
            self.LED.setText(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            self.vector_lock.release()
            self.update_graph_signal.emit()
            sleep(self.rate)





if __name__ == "__main__":
    app = pg.mkQApp("RGC monitor")
    win = MainWindow()

    update_thread = Thread(target=win.update_all,daemon=True)
    update_thread.start()

    win.resize(600,400)
    win.setWindowTitle('RGC monitoring')
    win.show()
    pg.exec()
