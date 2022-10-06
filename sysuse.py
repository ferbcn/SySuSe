#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psutil as psu

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QLCDNumber, QVBoxLayout, QHBoxLayout, QApplication, QLabel, QSystemTrayIcon, QMenu)
from PyQt6.QtCore import QTimer


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        self.icon = icon
        self.menu = QMenu(parent)
        self.setIcon(icon)
        self.setVisible(True)

        self.cpu = 0
        self.mem = 0

        show = self.menu.addAction("Mini")
        show.triggered.connect(self.show_notification)
        showAction = self.menu.addAction("Show")
        showAction.triggered.connect(self.show_action)
        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit_action)
        self.setContextMenu(self.menu)
        self.setToolTip("System Stats")

    def show_notification(self):
        self.showMessage("System Stats", f"SySuSe: {self.cpu:.1f}% / MEM: {self.mem}%", self.icon, 2000)

    def show_action(self):
        self.parent.close()
        self.parent.show()

    def exit_action(self):
        self.parent.close()
        sys.exit()


class CPU(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.cpu_readings = []
        self.cpu_avg = 0
        self.memory_usage = 0

    def initUI(self):

        self.icon = QIcon("cpu_bw.png")
        self.tray_icon = SystemTrayIcon(self.icon, parent=self)

        self.setGeometry(0, 0, 150, 130)
        self.setWindowTitle('SySuSe')
        # self.show()

        self.lcd0 = QLCDNumber(self)
        self.lcd0.setDigitCount(3)
        self.lcd0.setFrameStyle(0)

        self.lcd2 = QLCDNumber(self)
        self.lcd2.setDigitCount(4)
        self.lcd2.setFrameStyle(0)

        self.label0 = QLabel("SySuSe (%)")
        self.label1 = QLabel("Freq. (GHz):")
        self.label2 = QLabel("Memory (%):")

        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout ()
        hbox0.addWidget(self.label0)
        hbox0.addWidget(self.lcd0)

        hbox2 = QHBoxLayout ()
        hbox2.addWidget (self.label2)
        hbox2.addWidget (self.lcd2)

        vbox.addLayout (hbox0)
        # vbox.addLayout (hbox1)
        vbox.addLayout (hbox2)
        self.setLayout(vbox)

        timer = QTimer(self)
        timer.timeout.connect(self.showStats)
        timer.start(500)


    def showStats(self):

        # cpu usage

        # get cpu and mem stats
        self.cpu_readings.append(psu.cpu_percent(interval=None))
        if len(self.cpu_readings) > 10:
            self.cpu_readings = self.cpu_readings[1:]
        cpu_pct = sum(self.cpu_readings)/10

        # get memory usage
        mem_usage = psu.virtual_memory()[2]

        # set color of lcd0
        if cpu_pct > 50:
            self.lcd0.setStyleSheet("color: red")
        elif cpu_pct > 25:
            self.lcd0.setStyleSheet("color: orange")
        else:
            self.lcd0.setStyleSheet("color: #228b22")

        # set color of lcd1
        if mem_usage > 50:
            self.lcd2.setStyleSheet("color: red")
        elif mem_usage > 25:
            self.lcd2.setStyleSheet("color: orange")
        else:
            self.lcd2.setStyleSheet("color: #228b22")

        # write data to LCDs
        #self.lcd1.display(cpu_freq)
        self.lcd0.display(cpu_pct)
        self.lcd2.display(mem_usage)

        # save data in tray icon object
        self.tray_icon.cpu = cpu_pct
        self.tray_icon.mem = mem_usage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = CPU()
    sys.exit(app.exec())
