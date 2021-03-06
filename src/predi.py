# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'predi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

#main import for the QT window
from PyQt5 import QtCore, QtGui, QtWidgets

#imports to the graph works with the QT window
import sys
import time
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure

#imports to update the graph with the data from sensors
import os
import threading
from kpredictor import *
from read_routine import *
from save_routine import *

# import to the slide window of the canvas work
from collections import deque

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, screen_size):

        # Graphs settings
        self.firstChange = True
        self.list_canvas = []
        #list_toolbar = []
        list_dynamic_canvas = []
        self.list__dynamic_ax = []
        self.min_fft = [0, 0, 0]
        self.max_fft = [0, 0, 0]
        self.min_axis = [0, 0, 0, 0, 0, 0]
        self.max_axis = [0, 0, 0, 0, 0, 0]
        self.gap = [0, 8]

        # Save button settings
        self.state_button = True

        MainWindow.setObjectName("MainWindow")
        max_height = screen_size.height() * 0.93
        MainWindow.resize(screen_size.width(), max_height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Graphs first configurations
        for i in range(6):
        
            self.list_canvas.append(QtWidgets.QVBoxLayout())
            self.list_canvas[i].setObjectName("canvas"+str(i))

            list_dynamic_canvas.append(FigureCanvas(Figure(figsize=(8,2), dpi=90)))

            #list_toolbar.append(NavigationToolbar2QT(list_dynamic_canvas[i], MainWindow))
            #self.list_canvas[i].addWidget(list_toolbar[i])

            self.list_canvas[i].addWidget(list_dynamic_canvas[i])
            self.list__dynamic_ax.append(list_dynamic_canvas[i].figure.subplots())
            self._timer = list_dynamic_canvas[i].new_timer(
                0.1, [(self._update_canvas, (), {})])
        self._timer.start()

        # Setting the layout of the lateral menu
        w = screen_size.width() * 0.09
        self.lateralMenuLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.lateralMenuLayoutWidget.setGeometry(QtCore.QRect(screen_size.width() * 0.005, 1, w, max_height))
        self.lateralMenuLayoutWidget.setObjectName("lateralMenuLayoutWidget")
        self.lateralMenuLayout = QtWidgets.QVBoxLayout(self.lateralMenuLayoutWidget)
        self.lateralMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.lateralMenuLayout.setObjectName("lateralMenuLayout")

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem)
        
        # Line of the STATE label
        self.line0Layout = QtWidgets.QHBoxLayout()
        self.line0Layout.setObjectName("line0Layout")

        self.state_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        #self.state_label.setGeometry(QtCore.QRect(
        #    w * 0.1, max_height * 0.02, w * 0.4, max_height * 0.02))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(80)
        self.state_label.setFont(font)
        self.state_label.setObjectName("state_label")

        self.ok_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        #self.ok_label.setGeometry(QtCore.QRect(
        #    w * 0.5, max_height * 0.02, w * 0.4, max_height * 0.04))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(80)
        self.ok_label.setFont(font)
        self.ok_label.setObjectName("ok_label")

        self.line0Layout.addWidget(self.state_label)
        self.line0Layout.addWidget(self.ok_label)

        self.lateralMenuLayout.addLayout(self.line0Layout)

        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem2)

        # INPUT section
        self.txtlineLayout = QtWidgets.QHBoxLayout()
        self.txtlineLayout.setObjectName("txtlineLayout")

        self.txtlineLayout2 = QtWidgets.QHBoxLayout()
        self.txtlineLayout2.setObjectName("txtlineLayout2")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")

        self.txt_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        self.txt_label.setObjectName("txt_label")

        self.txtlineLayout.addWidget(self.txt_label)
        self.txtlineLayout2.addWidget(self.textEdit)

        self.lateralMenuLayout.addLayout(self.txtlineLayout)
        self.lateralMenuLayout.addLayout(self.txtlineLayout2)

        # SAVE section
        self.savelineLayout = QtWidgets.QHBoxLayout()
        self.savelineLayout.setObjectName("savelineLayout")

        self.save_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.save_label.setFont(font)
        self.save_label.setObjectName("save_label")

        self.save_button = QtWidgets.QPushButton(self.lateralMenuLayoutWidget)
        self.save_button.setObjectName("save_button")
        self.save_button.setStyleSheet("background-color: rgb(0, 255, 0);")


        self.savelineLayout.addWidget(self.save_label)
        self.savelineLayout.addWidget(self.save_button)

        self.lateralMenuLayout.addLayout(self.savelineLayout)

        def save():
            if self.state_button == True:
                self.state_button = False
                self.changetoSTOP()
                textboxValue = self.textEdit.toPlainText()
                SaveRoutine().start(textboxValue)
                self.textEdit.clear()
            else:
                self.state_button = True
                self.changetoSTART()
                SaveRoutine().stop()

        self.save_button.clicked.connect(save)

        spacerItemSave = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItemSave)

        '''
        # Control of the FIRST graph
        self.line1Layout = QtWidgets.QHBoxLayout()
        self.line1Layout.setObjectName("line1Layout")

        self.graph1_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.graph1_label.setFont(font)
        self.graph1_label.setObjectName("graph1_label")

        self.graph1_decrease = QtWidgets.QPushButton(self.lateralMenuLayoutWidget)
        self.graph1_decrease.setObjectName("graph1_decrease")

        #def dec0FFT():
        #    self.decreaseFFT(0)

        #def inc0FFT():
        #    self.increaseFFT(0)

        #self.graph1_decrease.clicked.connect(dec0FFT)

        self.graph1_increase = QtWidgets.QPushButton(self.lateralMenuLayoutWidget)
        self.graph1_increase.setObjectName("graph1_increase")

        

        #self.graph1_increase.clicked.connect(inc0FFT)

        self.line1Layout.addWidget(self.graph1_decrease)
        self.line1Layout.addWidget(self.graph1_increase)

        self.lateralMenuLayout.addWidget(self.graph1_label)
        self.lateralMenuLayout.addLayout(self.line1Layout)

        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem3)

        # Control of the SECOND graph
        self.line2Layout = QtWidgets.QHBoxLayout()
        self.line2Layout.setObjectName("line2Layout")

        self.graph2_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.graph2_label.setFont(font)
        self.graph2_label.setObjectName("graph2_label")

        self.graph2_decrease = QtWidgets.QPushButton(self.lateralMenuLayoutWidget)
        self.graph2_decrease.setObjectName("graph2_decrease")

        #def dec1FFT():
        #    self.decreaseFFT(1)

        #def inc1FFT():
        #    self.increaseFFT(1)
        #self.graph2_decrease.clicked.connect(dec1FFT)

        self.graph2_increase = QtWidgets.QPushButton(self.lateralMenuLayoutWidget)
        self.graph2_increase.setObjectName("graph2_increase")

        #self.graph2_increase.clicked.connect(inc1FFT)

        self.line2Layout.addWidget(self.graph2_decrease)
        self.line2Layout.addWidget(self.graph2_increase)

        self.lateralMenuLayout.addWidget(self.graph2_label)
        self.lateralMenuLayout.addLayout(self.line2Layout)

        spacerItem4 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem4)

        # Control of the THIRD graph
        self.line3Layout = QtWidgets.QHBoxLayout()
        self.line3Layout.setObjectName("line3Layout")

        self.graph3_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.graph3_label.setFont(font)
        self.graph3_label.setObjectName("graph3_label")

        #def dec2FFT():
        #    self.decreaseFFT(2)

        #def inc2FFT():
        #    self.increaseFFT(2)

        self.graph3_decrease = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph3_decrease.setObjectName("graph3_decrease")

        #self.graph3_decrease.clicked.connect(dec2FFT)

        self.graph3_increase = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph3_increase.setObjectName("graph3_increase")

        #self.graph3_increase.clicked.connect(inc2FFT)

        self.line3Layout.addWidget(self.graph3_decrease)
        self.line3Layout.addWidget(self.graph3_increase)

        self.lateralMenuLayout.addWidget(self.graph3_label)
        self.lateralMenuLayout.addLayout(self.line3Layout)

        spacerItem5 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem5)

        # Control of the FOURTH graph
        self.line4Layout = QtWidgets.QHBoxLayout()
        self.line4Layout.setObjectName("line4Layout")

        self.graph4_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.graph4_label.setFont(font)
        self.graph4_label.setObjectName("graph4_label")

        #def dec3FFT():
        #    self.decreaseFFT(3)

        #def inc3FFT():
        #    self.increaseFFT(3)

        self.graph4_decrease = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph4_decrease.setObjectName("graph4_decrease")

        #self.graph4_decrease.clicked.connect(dec3FFT)

        self.graph4_increase = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph4_increase.setObjectName("graph4_increase")

        #self.graph4_increase.clicked.connect(inc3FFT)

        self.line4Layout.addWidget(self.graph4_decrease)
        self.line4Layout.addWidget(self.graph4_increase)

        self.lateralMenuLayout.addWidget(self.graph4_label)
        self.lateralMenuLayout.addLayout(self.line4Layout)

        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem6)

        # Control of the FIFTH graph
        self.line5Layout = QtWidgets.QHBoxLayout()
        self.line5Layout.setObjectName("line5Layout")

        self.graph5_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.graph5_label.setFont(font)
        self.graph5_label.setObjectName("graph5_label")

        #def dec4FFT():
        #    self.decreaseFFT(4)

        #def inc4FFT():
        #    self.increaseFFT(4)

        self.graph5_decrease = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph5_decrease.setObjectName("graph5_decrease")

        #self.graph5_decrease.clicked.connect(dec4FFT)

        self.graph5_increase = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph5_increase.setObjectName("graph5_increase")

        #self.graph5_increase.clicked.connect(inc4FFT)

        self.line5Layout.addWidget(self.graph5_decrease)
        self.line5Layout.addWidget(self.graph5_increase)

        self.lateralMenuLayout.addWidget(self.graph5_label)
        self.lateralMenuLayout.addLayout(self.line5Layout)

        spacerItem7 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem7)

        # Control of the SIXTH graph
        self.line6Layout = QtWidgets.QHBoxLayout()
        self.line6Layout.setObjectName("line6Layout")

        self.graph6_label = QtWidgets.QLabel(self.lateralMenuLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.graph6_label.setFont(font)
        self.graph6_label.setObjectName("graph6_label")

        #def dec5FFT():
        #    self.decreaseFFT(5)

        #def inc5FFT():
        #    self.increaseFFT(5)

        self.graph6_decrease = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph6_decrease.setObjectName("graph6_decrease")

        #self.graph6_decrease.clicked.connect(dec5FFT)

        self.graph6_increase = QtWidgets.QPushButton(
            self.lateralMenuLayoutWidget)
        self.graph6_increase.setObjectName("graph6_increase")

        #self.graph6_increase.clicked.connect(inc5FFT)

        self.line6Layout.addWidget(self.graph6_decrease)
        self.line6Layout.addWidget(self.graph6_increase)

        self.lateralMenuLayout.addWidget(self.graph6_label)
        self.lateralMenuLayout.addLayout(self.line6Layout)

        spacerItem8 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lateralMenuLayout.addItem(spacerItem8)
        '''

        #######################################################################################################
        # Graphs things
        w = screen_size.width() * 0.90
        w_ini = screen_size.width() * 0.10
        h = max_height * 0.33
        
        self.firstLineLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.firstLineLayoutWidget.setGeometry(QtCore.QRect(w_ini, 1, w, h))
        self.firstLineLayoutWidget.setObjectName("firstLineLayoutWidget")
        self.firstLineLayout = QtWidgets.QHBoxLayout(
            self.firstLineLayoutWidget)
        self.firstLineLayout.setContentsMargins(0, 0, 0, 0)
        self.firstLineLayout.setObjectName("firstLineLayout")
        
        self.secondLineLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.secondLineLayoutWidget.setGeometry(QtCore.QRect(w_ini, h + 1, w, h))
        self.secondLineLayoutWidget.setObjectName("secondLineLayoutWidget")
        self.secondLineLayout = QtWidgets.QHBoxLayout(
            self.secondLineLayoutWidget)
        self.secondLineLayout.setContentsMargins(0, 0, 0, 0)
        self.secondLineLayout.setObjectName("secondLineLayout")

        self.thirdLineLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.thirdLineLayoutWidget.setGeometry(QtCore.QRect(w_ini, h * 2, w, h))
        self.thirdLineLayoutWidget.setObjectName("thirdLineLayoutWidget")
        self.thirdLineLayout = QtWidgets.QHBoxLayout(
            self.thirdLineLayoutWidget)
        self.thirdLineLayout.setContentsMargins(0, 0, 0, 0)
        self.thirdLineLayout.setObjectName("thirdLineLayout")       

        self.firstLineLayout.addLayout(self.list_canvas[0])
        self.firstLineLayout.addLayout(self.list_canvas[3])
        self.secondLineLayout.addLayout(self.list_canvas[1])
        self.secondLineLayout.addLayout(self.list_canvas[4])
        self.thirdLineLayout.addLayout(self.list_canvas[2])
        self.thirdLineLayout.addLayout(self.list_canvas[5])
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 58, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    '''
    def decreaseFFT(self, n_graph):
        if self.firstChange == True:
            limY = self.list__dynamic_ax[n_graph].get_ylim()
            self.min_fft[n_graph] = limY[0] - 0.1
            self.max_fft[n_graph] = limY[1] + 0.1
        else:
            self.min_fft[n_graph] = self.min_fft[n_graph] - 0.1
            self.max_fft[n_graph] = self.max_fft[n_graph] + 0.1

    def decreaseAxis(self, n_graph):
        if self.firstChange == True:
            limY = self.list__dynamic_ax[n_graph].get_ylim()
            self.min_axis[n_graph] = limY[0] - 0.1
            self.max_axis[n_graph] = limY[1] + 0.1
        else:
            self.min_axis[n_graph] = self.min_axis[n_graph] - 0.1
            self.max_axis[n_graph] = self.max_axis[n_graph] + 0.1

    def increaseFFT(self, n_graph):
        if self.firstChange == True:
            limY = self.list__dynamic_ax[n_graph].get_ylim()
            self.min_fft[n_graph] = limY[0] + 0.1
            self.max_fft[n_graph] = limY[1] - 0.1
        else:
            self.min_fft[n_graph] = self.min_fft[n_graph] + 0.1
            self.max_fft[n_graph] = self.max_fft[n_graph] - 0.1

    def increaseAxis(self, n_graph):
        if self.firstChange == True:
            limY = self.list__dynamic_ax[n_graph].get_ylim()
            self.min_axis[n_graph] = limY[0] + 0.1
            self.max_axis[n_graph] = limY[1] - 0.1
        else:
            self.min_axis[n_graph] = self.min_axis[n_graph] + 0.1
            self.max_axis[n_graph] = self.max_axis[n_graph] - 0.1
    '''
    def _update_canvas(self):
        for i in range(6):
            self.list__dynamic_ax[i].clear()

        t1, xfft = ReadRoutine().sensors.list_s[0].a[0].getxyFFT(
            ReadRoutine().sensors.rtc)
        t2, yfft = ReadRoutine().sensors.list_s[0].a[1].getxyFFT(
            ReadRoutine().sensors.rtc)
        t3, zfft = ReadRoutine().sensors.list_s[0].a[2].getxyFFT(
            ReadRoutine().sensors.rtc)
        t4, x = ReadRoutine().sensors.list_s[0].a[0].getxy(
            ReadRoutine().sensors.rtc)
        t5, y = ReadRoutine().sensors.list_s[0].a[1].getxy(
            ReadRoutine().sensors.rtc)
        t6, z = ReadRoutine().sensors.list_s[0].a[2].getxy(
            ReadRoutine().sensors.rtc)

        if len(t4) != 0:
            if t4[-1] >= self.gap[1]:
                self.gap[0] += 1
                self.gap[1] += 1

        self.list__dynamic_ax[0].plot(t1, xfft)
        self.list__dynamic_ax[0].set_ylabel('X-FFT')

        self.list__dynamic_ax[1].plot(t2, yfft)
        self.list__dynamic_ax[1].set_ylabel('Y-FFT')

        self.list__dynamic_ax[2].plot(t3, zfft)
        self.list__dynamic_ax[2].set_ylabel('Z-FFT')

        self.list__dynamic_ax[3].plot(t4, x)
        self.list__dynamic_ax[3].set_ylabel('X-axis')

        self.list__dynamic_ax[4].plot(t5, y)
        self.list__dynamic_ax[4].set_ylabel('Y-axis')

        self.list__dynamic_ax[5].plot(t6, z)
        self.list__dynamic_ax[5].set_ylabel('Z-axis')

        for i in range(3):
            self.list__dynamic_ax[i].set_xlim([-5, 155])
            #self.list__dynamic_ax[i].set_ylim([self.min_fft[i], self.max_fft[i]])
            #print(self.list__dynamic_ax[i].get_ylim())
            self.list__dynamic_ax[i].figure.canvas.draw()
        for i in range(3, 6):
            self.list__dynamic_ax[i].set_xlim([self.gap[0], self.gap[1]])
            #self.list__dynamic_ax[i].set_ylim([self.min_axis[i], self.max_axis[i]])
            self.list__dynamic_ax[i].figure.canvas.draw()
        self.firstChange = False
    def changetoSTART(self):
        #self.save_label.setText("Press to start")
        self.save_button.setText("START")
        self.save_button.setStyleSheet("background-color: rgb(0, 255, 0);")

    def changetoSTOP(self):
        #self.save_label.setText("Press to stop")
        self.save_button.setText("STOP")
        self.save_button.setStyleSheet("background-color: rgb(255, 0, 0);")

    def changetoOK(self):
        self.ok_label.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                        "color: rgb(0, 0, 0);")
        self.ok_label.setText("OK")

    def changetoERROR(self):
        self.ok_label.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                        "color: rgb(0, 0, 0);")
        self.ok_label.setText("ERROR")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.state_label.setText(_translate("MainWindow", "State: "))
        self.ok_label.setText(_translate("MainWindow", "OK"))

        self.save_label.setText(_translate("MainWindow", "Press to: "))
        self.save_button.setText(_translate("MainWindow", "SAVE"))

        self.txt_label.setText(_translate("MainWindow", "Insert a name"))
        '''
        self.graph1_label.setText(_translate("MainWindow", "View X-FFT"))
        self.graph1_decrease.setText(_translate("MainWindow", "-"))
        self.graph1_increase.setText(_translate("MainWindow", "+"))

        self.graph2_label.setText(_translate("MainWindow", "View Y-FFT"))
        self.graph2_decrease.setText(_translate("MainWindow", "-"))
        self.graph2_increase.setText(_translate("MainWindow", "+"))

        self.graph3_label.setText(_translate("MainWindow", "View Z-FFT"))
        self.graph3_decrease.setText(_translate("MainWindow", "-"))
        self.graph3_increase.setText(_translate("MainWindow", "+"))

        self.graph4_label.setText(_translate("MainWindow", "View X-axis"))
        self.graph4_decrease.setText(_translate("MainWindow", "-"))
        self.graph4_increase.setText(_translate("MainWindow", "+"))

        self.graph5_label.setText(_translate("MainWindow", "View Y-axis"))
        self.graph5_decrease.setText(_translate("MainWindow", "-"))
        self.graph5_increase.setText(_translate("MainWindow", "+"))

        self.graph6_label.setText(_translate("MainWindow", "View Z-axis"))
        self.graph6_decrease.setText(_translate("MainWindow", "-"))
        self.graph6_increase.setText(_translate("MainWindow", "+"))
        '''
