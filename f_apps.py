from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import os
import sys
import socket
from datetime import datetime
import numpy as np
import pickle
from qtwidgets import AnimatedToggle
import time
from copy import copy
import sqlite3
import matplotlib

matplotlib.use('Qt5Agg')


class HistoryPlot(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title("Trajectory Robot Pada Peta", fontsize="small")
        self.axes.set_xlabel("Koordinat X (meter)", fontsize="small",
                             weight='bold', style='italic')
        self.axes.set_ylabel("Koordinat Y (meter)", fontsize="small",
                             weight='bold', style='italic')
        self.axes.set_xlim([-1, classKirim.maxX + 1])
        self.axes.set_ylim([-1, classKirim.maxY + 1])
        self.axes.set_ylim(self.axes.get_ylim()[::-1])
        self.axes.grid(True)
        self.axes.set_axisbelow(True)
        super(HistoryPlot, self).__init__(self.figure)


class HistoryPlotPresepsi(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100, mode=0):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        if(mode == 0):
            (self.axes_astar, self.axes_imp) = self.figure.subplots(1, 2)
        else:
            self.axes_akurasi = self.figure.subplots()
        super(HistoryPlotPresepsi, self).__init__(self.figure)


class MainApp(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(1251, 820)
        window.setMinimumSize(QtCore.QSize(1250, 820))
        window.setMaximumSize(QtCore.QSize(1251, 820))
        self.mainWidget = QtWidgets.QWidget(window)
        self.mainWidget.setStyleSheet("")
        self.mainWidget.setObjectName("mainWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameApp = QtWidgets.QFrame(self.mainWidget)
        self.frameApp.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(22,22,22);\n"
                                    "    border-radius:20px;\n"
                                    "}")
        self.frameApp.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameApp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameApp.setObjectName("frameApp")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameApp)
        self.verticalLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frameTop = QtWidgets.QFrame(self.frameApp)
        self.frameTop.setMaximumSize(QtCore.QSize(16777215, 65))
        self.frameTop.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frameTop.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTop.setObjectName("frameTop")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frameTop)
        self.horizontalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frameIcons = QtWidgets.QFrame(self.frameTop)
        self.frameIcons.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameIcons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameIcons.setObjectName("frameIcons")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frameIcons)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame = QtWidgets.QFrame(self.frameIcons)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(32, 16777215))
        self.frame.setStyleSheet("QFrame {\n"
                                 "    background-color:transparent;\n"
                                 "    border-image: url(\"./assets/icon.png\") 0 0 0 0 strecth strecth;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.frameIcons)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_4.setMaximumSize(QtCore.QSize(145, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {\n"
                                 "    color:rgb(215,215,215);\n"
                                 "    padding-left:2.5px;\n"
                                 "}")
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(145, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel {\n"
                                   "    color:rgb(84,91,103);\n"
                                   "    padding-left:2.5px;\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.horizontalLayout_2.addWidget(self.frameIcons)
        self.frameEvent = QtWidgets.QFrame(self.frameTop)
        self.frameEvent.setMaximumSize(QtCore.QSize(80, 16777215))
        self.frameEvent.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameEvent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameEvent.setObjectName("frameEvent")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frameEvent)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.btnMinimize = QtWidgets.QFrame(self.frameEvent)
        self.btnMinimize.setStyleSheet("QFrame {\n"
                                       "    background-color:transparent;\n"
                                       "    border-image: url(\"./assets/minimize_grey.png\") 0 0 0 0 strecth strecth;\n"
                                       "    border-width: 0px 9.5px 0px 9.5px;\n"
                                       "}\n"
                                       "\n"
                                       "QFrame:hover{\n"
                                       "    border-image: url(\"./assets/minimize_white.png\") 0 0 0 0 strecth strecth;\n"
                                       "}")
        self.btnMinimize.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btnMinimize.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnMinimize.setObjectName("btnMinimize")
        self.horizontalLayout_9.addWidget(self.btnMinimize)
        self.btnClose = QtWidgets.QFrame(self.frameEvent)
        self.btnClose.setStyleSheet("QFrame {\n"
                                    "    background-color:transparent;\n"
                                    "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                    "    border-width:6px 9px 6px 9px\n"
                                    "}\n"
                                    "\n"
                                    "QFrame:hover{\n"
                                    "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.btnClose.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btnClose.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout_9.addWidget(self.btnClose)
        self.horizontalLayout_2.addWidget(self.frameEvent)
        self.verticalLayout_2.addWidget(self.frameTop)
        self.frameContent = QtWidgets.QFrame(self.frameApp)
        self.frameContent.setStyleSheet("")
        self.frameContent.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameContent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameContent.setObjectName("frameContent")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frameContent)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frameMenus = QtWidgets.QFrame(self.frameContent)
        self.frameMenus.setMinimumSize(QtCore.QSize(180, 0))
        self.frameMenus.setMaximumSize(QtCore.QSize(180, 16777215))
        self.frameMenus.setStyleSheet("QFrame{\n"
                                      "    background-color:rgb(27,27,27);\n"
                                      "}")
        self.frameMenus.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameMenus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMenus.setObjectName("frameMenus")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frameMenus)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_5 = QtWidgets.QFrame(self.frameMenus)
        self.frame_5.setStyleSheet("")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setContentsMargins(15, 30, 0, 15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.btnCore = QtWidgets.QFrame(self.frame_5)
        self.btnCore.setMinimumSize(QtCore.QSize(0, 50))
        self.btnCore.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btnCore.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.btnCore.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnCore.setObjectName("btnCore")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.btnCore)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.imgCore = QtWidgets.QFrame(self.btnCore)
        self.imgCore.setMaximumSize(QtCore.QSize(40, 40))
        self.imgCore.setStyleSheet("\n"
                                   "\n"
                                   "QFrame[cond = \"new\"] {\n"
                                   "    background-color:transparent;\n"
                                   "    border-image: url(\"./assets/core_white.png\") 0 0 0 0 strecth strecth;\n"
                                   "    border-width:4px;\n"
                                   "}\n"
                                   "QFrame[cond = \"last\"] {\n"
                                   "    background-color:transparent;\n"
                                   "    border-image: url(\"./assets/core_grey.png\") 0 0 0 0 strecth strecth;\n"
                                   "    border-width:4px;\n"
                                   "}")
        self.imgCore.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgCore.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgCore.setObjectName("imgCore")
        self.horizontalLayout_5.addWidget(self.imgCore)
        self.labelCore = QtWidgets.QLabel(self.btnCore)
        self.labelCore.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelCore.setFont(font)
        self.labelCore.setStyleSheet("*{\n"
                                     "    background:transparent;\n"
                                     "    padding-left:1.5px;\n"
                                     "}\n"
                                     "\n"
                                     "QLabel[cond = \"new\"] {\n"
                                     "    color:rgb(215,215,215);\n"
                                     "}\n"
                                     "\n"
                                     "QLabel[cond = \"last\"] {\n"
                                     "    color:rgb(136,149,169);\n"
                                     "}\n"
                                     "")
        self.labelCore.setObjectName("labelCore")
        self.horizontalLayout_5.addWidget(self.labelCore)
        self.hoverCore = QtWidgets.QFrame(self.btnCore)
        self.hoverCore.setMaximumSize(QtCore.QSize(3, 40))
        self.hoverCore.setStyleSheet("QFrame[cond = \"new\"] {\n"
                                     "    background-color:rgb(215,215,215);\n"
                                     "}\n"
                                     "\n"
                                     "QFrame[cond = \"last\"] {\n"
                                     "    background:transparent;\n"
                                     "}")
        self.hoverCore.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hoverCore.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hoverCore.setObjectName("hoverCore")
        self.horizontalLayout_5.addWidget(self.hoverCore)
        self.verticalLayout_7.addWidget(self.btnCore)
        self.btnSocket = QtWidgets.QFrame(self.frame_5)
        self.btnSocket.setMinimumSize(QtCore.QSize(0, 50))
        self.btnSocket.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btnSocket.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.btnSocket.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnSocket.setObjectName("btnSocket")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.btnSocket)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.imgSocket = QtWidgets.QFrame(self.btnSocket)
        self.imgSocket.setMaximumSize(QtCore.QSize(40, 40))
        self.imgSocket.setStyleSheet("QFrame[cond = \"new\"] {\n"
                                     "    background-color:transparent;\n"
                                     "    border-image: url(\"./assets/socket_white.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width:4px;\n"
                                     "}\n"
                                     "\n"
                                     "QFrame[cond = \"last\"] {\n"
                                     "    background-color:transparent;\n"
                                     "    border-image: url(\"./assets/socket_grey.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width:4px;\n"
                                     "}")
        self.imgSocket.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgSocket.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgSocket.setObjectName("imgSocket")
        self.horizontalLayout_6.addWidget(self.imgSocket)
        self.labelSocket = QtWidgets.QLabel(self.btnSocket)
        self.labelSocket.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelSocket.setFont(font)
        self.labelSocket.setStyleSheet("*{\n"
                                       "    background:transparent;\n"
                                       "    padding-left:1.5px;\n"
                                       "}\n"
                                       "\n"
                                       "QLabel[cond = \"new\"] {\n"
                                       "    color:rgb(215,215,215);\n"
                                       "}\n"
                                       "\n"
                                       "QLabel[cond = \"last\"] {\n"
                                       "    color:rgb(136,149,169);\n"
                                       "}\n"
                                       "")
        self.labelSocket.setObjectName("labelSocket")
        self.horizontalLayout_6.addWidget(self.labelSocket)
        self.hoverSocket = QtWidgets.QFrame(self.btnSocket)
        self.hoverSocket.setMaximumSize(QtCore.QSize(3, 40))
        self.hoverSocket.setStyleSheet("QFrame[cond = \"new\"] {\n"
                                       "    background-color:rgb(255,255,255);\n"
                                       "}\n"
                                       "\n"
                                       "QFrame[cond = \"last\"] {\n"
                                       "    background:transparent;\n"
                                       "}")
        self.hoverSocket.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hoverSocket.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hoverSocket.setObjectName("hoverSocket")
        self.horizontalLayout_6.addWidget(self.hoverSocket)
        self.verticalLayout_7.addWidget(self.btnSocket)
        self.btnHistory = QtWidgets.QFrame(self.frame_5)
        self.btnHistory.setMinimumSize(QtCore.QSize(0, 50))
        self.btnHistory.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btnHistory.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.btnHistory.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnHistory.setObjectName("btnHistory")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.btnHistory)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.imgHistory = QtWidgets.QFrame(self.btnHistory)
        self.imgHistory.setMaximumSize(QtCore.QSize(40, 40))
        self.imgHistory.setStyleSheet("QFrame[cond=\"new\"] {\n"
                                      "    background-color:transparent;\n"
                                      "    border-image: url(\"./assets/history_white.png\") 0 0 0 0 strecth strecth;\n"
                                      "    border-width:3px;\n"
                                      "}\n"
                                      "\n"
                                      "QFrame[cond=\"last\"] {\n"
                                      "    background-color:transparent;\n"
                                      "    border-image: url(\"./assets/history_grey.png\") 0 0 0 0 strecth strecth;\n"
                                      "    border-width:3px;\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.imgHistory.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgHistory.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgHistory.setObjectName("imgHistory")
        self.horizontalLayout_7.addWidget(self.imgHistory)
        self.labelHistory = QtWidgets.QLabel(self.btnHistory)
        self.labelHistory.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelHistory.setFont(font)
        self.labelHistory.setStyleSheet("*{\n"
                                        "    background:transparent;\n"
                                        "    padding-left:1.5px;\n"
                                        "}\n"
                                        "\n"
                                        "QLabel[cond = \"new\"] {\n"
                                        "    color:rgb(215,215,215);\n"
                                        "}\n"
                                        "\n"
                                        "QLabel[cond = \"last\"] {\n"
                                        "    color:rgb(136,149,169);\n"
                                        "}\n"
                                        "")
        self.labelHistory.setObjectName("labelHistory")
        self.horizontalLayout_7.addWidget(self.labelHistory)
        self.hoverHistory = QtWidgets.QFrame(self.btnHistory)
        self.hoverHistory.setMaximumSize(QtCore.QSize(3, 40))
        self.hoverHistory.setStyleSheet("QFrame[cond = \"new\"] {\n"
                                        "    background-color:rgb(215,215,215);\n"
                                        "}\n"
                                        "\n"
                                        "QFrame[cond = \"last\"] {\n"
                                        "    background:transparent;\n"
                                        "}")
        self.hoverHistory.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hoverHistory.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hoverHistory.setObjectName("hoverHistory")
        self.horizontalLayout_7.addWidget(self.hoverHistory)
        self.verticalLayout_7.addWidget(self.btnHistory)
        self.btnTesting = QtWidgets.QFrame(self.frame_5)
        self.btnTesting.setMinimumSize(QtCore.QSize(0, 50))
        self.btnTesting.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btnTesting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btnTesting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnTesting.setObjectName("btnTesting")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.btnTesting)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.imgTesting = QtWidgets.QFrame(self.btnTesting)
        self.imgTesting.setMaximumSize(QtCore.QSize(40, 40))
        self.imgTesting.setStyleSheet("QFrame[cond = \"new\"] {\n"
                                      "    background-color:transparent;\n"
                                      "    border-image: url(\"./assets/testing_white.png\") 0 0 0 0 strecth strecth;\n"
                                      "    border-width:4px;\n"
                                      "}\n"
                                      "QFrame[cond = \"last\"] {\n"
                                      "    background-color:transparent;\n"
                                      "    border-image: url(\"./assets/testing_grey.png\") 0 0 0 0 strecth strecth;\n"
                                      "    border-width:4px;\n"
                                      "}")
        self.imgTesting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgTesting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgTesting.setObjectName("imgTesting")
        self.horizontalLayout_8.addWidget(self.imgTesting)
        self.labelTesting = QtWidgets.QLabel(self.btnTesting)
        self.labelTesting.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelTesting.setFont(font)
        self.labelTesting.setStyleSheet("*{\n"
                                        "    background:transparent;\n"
                                        "    padding-left:1.5px;\n"
                                        "}\n"
                                        "\n"
                                        "QLabel[cond = \"new\"] {\n"
                                        "    color:rgb(215,215,215);\n"
                                        "}\n"
                                        "\n"
                                        "QLabel[cond = \"last\"] {\n"
                                        "    color:rgb(136,149,169);\n"
                                        "}\n"
                                        "")
        self.labelTesting.setObjectName("labelTesting")
        self.horizontalLayout_8.addWidget(self.labelTesting)
        self.hoverTesting = QtWidgets.QFrame(self.btnTesting)
        self.hoverTesting.setMaximumSize(QtCore.QSize(3, 40))
        self.hoverTesting.setStyleSheet("QFrame[cond = \"new\"] {\n"
                                        "    background-color:rgb(215,215,215);\n"
                                        "}\n"
                                        "\n"
                                        "QFrame[cond = \"last\"] {\n"
                                        "    background:transparent;\n"
                                        "}")
        self.hoverTesting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hoverTesting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hoverTesting.setObjectName("hoverTesting")
        self.horizontalLayout_8.addWidget(self.hoverTesting)
        self.verticalLayout_7.addWidget(self.btnTesting)
        self.verticalLayout_6.addWidget(self.frame_5, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout.addWidget(self.frameMenus)
        self.frameCore = QtWidgets.QFrame(self.frameContent)
        self.frameCore.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frameCore.setStyleSheet("QFrame {\n"
                                     "    background:transparent;\n"
                                     "}")
        self.frameCore.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameCore.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameCore.setLineWidth(1)
        self.frameCore.setObjectName("frameCore")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frameCore)
        self.verticalLayout_8.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_7 = QtWidgets.QFrame(self.frameCore)
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.labelPage = QtWidgets.QLabel(self.frame_7)
        self.labelPage.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.labelPage.setFont(font)
        self.labelPage.setStyleSheet("QLabel {\n"
                                     "    background:transparent;\n"
                                     "    color:rgb(215,215,215);\n"
                                     "}")
        self.labelPage.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelPage.setIndent(-1)
        self.labelPage.setObjectName("labelPage")
        self.verticalLayout_10.addWidget(self.labelPage)
        self.labelDescPage = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.labelDescPage.setFont(font)
        self.labelDescPage.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.labelDescPage.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelDescPage.setObjectName("labelDescPage")
        self.verticalLayout_10.addWidget(self.labelDescPage)
        self.verticalLayout_8.addWidget(self.frame_7, 0, QtCore.Qt.AlignTop)
        self.frame_8 = QtWidgets.QFrame(self.frameCore)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_9.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_8)
        self.stackedWidget.setStyleSheet("background:transparent;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.pageCore = QtWidgets.QWidget()
        self.pageCore.setObjectName("pageCore")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.pageCore)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25.setSpacing(20)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.frame_18 = QtWidgets.QFrame(self.pageCore)
        self.frame_18.setMinimumSize(QtCore.QSize(0, 440))
        self.frame_18.setMaximumSize(QtCore.QSize(16777215, 440))
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_18)
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.frame_24 = QtWidgets.QFrame(self.frame_18)
        self.frame_24.setMinimumSize(QtCore.QSize(225, 0))
        self.frame_24.setMaximumSize(QtCore.QSize(225, 16777215))
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.frame_24)
        self.verticalLayout_30.setContentsMargins(0, 0, 20, 0)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.frame_30 = QtWidgets.QFrame(self.frame_24)
        self.frame_30.setMaximumSize(QtCore.QSize(16777215, 190))
        self.frame_30.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.verticalLayout_45 = QtWidgets.QVBoxLayout(self.frame_30)
        self.verticalLayout_45.setContentsMargins(10, 10, 0, 10)
        self.verticalLayout_45.setSpacing(0)
        self.verticalLayout_45.setObjectName("verticalLayout_45")
        self.label_14 = QtWidgets.QLabel(self.frame_30)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "    margin-right:10px;\n"
                                    "}")
        self.label_14.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_45.addWidget(self.label_14)
        self.frame_60 = QtWidgets.QFrame(self.frame_30)
        self.frame_60.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_60.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_60.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_60.setObjectName("frame_60")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.frame_60)
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.frame_61 = QtWidgets.QFrame(self.frame_60)
        self.frame_61.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_61.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_61.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(195,196,196);\n"
                                    "    border-radius:10px;\n"
                                    "}")
        self.frame_61.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_61.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_61.setObjectName("frame_61")
        self.verticalLayout_52 = QtWidgets.QVBoxLayout(self.frame_61)
        self.verticalLayout_52.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_52.setObjectName("verticalLayout_52")
        self.frame_62 = QtWidgets.QFrame(self.frame_61)
        self.frame_62.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/obs_points.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_62.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_62.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_62.setObjectName("frame_62")
        self.verticalLayout_52.addWidget(self.frame_62)
        self.horizontalLayout_24.addWidget(self.frame_61)
        self.frame_85 = QtWidgets.QFrame(self.frame_60)
        self.frame_85.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_85.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_85.setObjectName("frame_85")
        self.verticalLayout_70 = QtWidgets.QVBoxLayout(self.frame_85)
        self.verticalLayout_70.setContentsMargins(10, 12, 0, -1)
        self.verticalLayout_70.setSpacing(1)
        self.verticalLayout_70.setObjectName("verticalLayout_70")
        self.label_26 = QtWidgets.QLabel(self.frame_85)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_26.setObjectName("label_26")
        self.verticalLayout_70.addWidget(self.label_26)
        self.descServer_10 = QtWidgets.QLabel(self.frame_85)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descServer_10.setFont(font)
        self.descServer_10.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.descServer_10.setObjectName("descServer_10")
        self.verticalLayout_70.addWidget(self.descServer_10)
        self.horizontalLayout_24.addWidget(self.frame_85)
        self.frameObsCond = QtWidgets.QFrame(self.frame_60)
        self.frameObsCond.setMinimumSize(QtCore.QSize(45, 35))
        self.frameObsCond.setMaximumSize(QtCore.QSize(45, 35))
        self.frameObsCond.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameObsCond.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameObsCond.setObjectName("frameObsCond")
        self.vObs = QtWidgets.QVBoxLayout(self.frameObsCond)
        self.vObs.setContentsMargins(0, 0, 0, 0)
        self.vObs.setSpacing(0)
        self.vObs.setObjectName("vObs")
        self.horizontalLayout_24.addWidget(self.frameObsCond)
        self.verticalLayout_45.addWidget(self.frame_60)
        self.frame_64 = QtWidgets.QFrame(self.frame_30)
        self.frame_64.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_64.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_64.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_64.setObjectName("frame_64")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.frame_64)
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.frame_65 = QtWidgets.QFrame(self.frame_64)
        self.frame_65.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_65.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_65.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(195,196,196);\n"
                                    "    border-radius:10px;\n"
                                    "}")
        self.frame_65.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_65.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_65.setObjectName("frame_65")
        self.verticalLayout_54 = QtWidgets.QVBoxLayout(self.frame_65)
        self.verticalLayout_54.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_54.setObjectName("verticalLayout_54")
        self.frame_66 = QtWidgets.QFrame(self.frame_65)
        self.frame_66.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/end_points.png\") 0 0 0 0 strecth strecth;\n"
                                    "    border-width:2px;\n"
                                    "}")
        self.frame_66.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_66.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_66.setObjectName("frame_66")
        self.verticalLayout_54.addWidget(self.frame_66)
        self.horizontalLayout_25.addWidget(self.frame_65)
        self.frame_86 = QtWidgets.QFrame(self.frame_64)
        self.frame_86.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_86.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_86.setObjectName("frame_86")
        self.verticalLayout_71 = QtWidgets.QVBoxLayout(self.frame_86)
        self.verticalLayout_71.setContentsMargins(10, 12, 0, -1)
        self.verticalLayout_71.setSpacing(1)
        self.verticalLayout_71.setObjectName("verticalLayout_71")
        self.label_27 = QtWidgets.QLabel(self.frame_86)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_27.setObjectName("label_27")
        self.verticalLayout_71.addWidget(self.label_27)
        self.descServer_11 = QtWidgets.QLabel(self.frame_86)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descServer_11.setFont(font)
        self.descServer_11.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.descServer_11.setObjectName("descServer_11")
        self.verticalLayout_71.addWidget(self.descServer_11)
        self.horizontalLayout_25.addWidget(self.frame_86)
        self.frameEndCond = QtWidgets.QFrame(self.frame_64)
        self.frameEndCond.setMinimumSize(QtCore.QSize(45, 35))
        self.frameEndCond.setMaximumSize(QtCore.QSize(45, 35))
        self.frameEndCond.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameEndCond.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameEndCond.setObjectName("frameEndCond")
        self.vEndPoint = QtWidgets.QVBoxLayout(self.frameEndCond)
        self.vEndPoint.setContentsMargins(0, 0, 0, 0)
        self.vEndPoint.setSpacing(0)
        self.vEndPoint.setObjectName("vEndPoint")
        self.horizontalLayout_25.addWidget(self.frameEndCond)
        self.verticalLayout_45.addWidget(self.frame_64)
        self.verticalLayout_30.addWidget(self.frame_30)
        self.frame_33 = QtWidgets.QFrame(self.frame_24)
        self.frame_33.setMinimumSize(QtCore.QSize(0, 260))
        self.frame_33.setMaximumSize(QtCore.QSize(204, 260))
        self.frame_33.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_33.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_33.setObjectName("frame_33")
        self.verticalLayout_57 = QtWidgets.QVBoxLayout(self.frame_33)
        self.verticalLayout_57.setContentsMargins(10, 10, 0, 40)
        self.verticalLayout_57.setSpacing(0)
        self.verticalLayout_57.setObjectName("verticalLayout_57")
        self.label_18 = QtWidgets.QLabel(self.frame_33)
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "    margin-right:10px;\n"
                                    "}")
        self.label_18.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_57.addWidget(self.label_18)
        self.frame_95 = QtWidgets.QFrame(self.frame_33)
        self.frame_95.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_95.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_95.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_95.setObjectName("frame_95")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout(self.frame_95)
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.frame_96 = QtWidgets.QFrame(self.frame_95)
        self.frame_96.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_96.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_96.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(195,196,196);\n"
                                    "    border-radius:10px;\n"
                                    "}")
        self.frame_96.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_96.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_96.setObjectName("frame_96")
        self.verticalLayout_75 = QtWidgets.QVBoxLayout(self.frame_96)
        self.verticalLayout_75.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_75.setObjectName("verticalLayout_75")
        self.frame_97 = QtWidgets.QFrame(self.frame_96)
        self.frame_97.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/timer_metode.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_97.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_97.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_97.setObjectName("frame_97")
        self.verticalLayout_75.addWidget(self.frame_97)
        self.horizontalLayout_32.addWidget(self.frame_96)
        self.frame_98 = QtWidgets.QFrame(self.frame_95)
        self.frame_98.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_98.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_98.setObjectName("frame_98")
        self.verticalLayout_56 = QtWidgets.QVBoxLayout(self.frame_98)
        self.verticalLayout_56.setContentsMargins(10, -1, 0, -1)
        self.verticalLayout_56.setSpacing(1)
        self.verticalLayout_56.setObjectName("verticalLayout_56")
        self.label_30 = QtWidgets.QLabel(self.frame_98)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_30.setObjectName("label_30")
        self.verticalLayout_56.addWidget(self.label_30)
        self.astar_start = QtWidgets.QLabel(self.frame_98)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start.setFont(font)
        self.astar_start.setStyleSheet("QLabel {\n"
                                       "    background:transparent;\n"
                                       "    color:rgb(84,91,103);\n"
                                       "}")
        self.astar_start.setObjectName("astar_start")
        self.verticalLayout_56.addWidget(self.astar_start)
        self.horizontalLayout_32.addWidget(self.frame_98)
        self.verticalLayout_57.addWidget(self.frame_95)
        self.frame_91 = QtWidgets.QFrame(self.frame_33)
        self.frame_91.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_91.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_91.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_91.setObjectName("frame_91")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout(self.frame_91)
        self.horizontalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_31.setSpacing(0)
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.frame_92 = QtWidgets.QFrame(self.frame_91)
        self.frame_92.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_92.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_92.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(195,196,196);\n"
                                    "    border-radius:10px;\n"
                                    "}")
        self.frame_92.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_92.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_92.setObjectName("frame_92")
        self.verticalLayout_72 = QtWidgets.QVBoxLayout(self.frame_92)
        self.verticalLayout_72.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_72.setObjectName("verticalLayout_72")
        self.frame_93 = QtWidgets.QFrame(self.frame_92)
        self.frame_93.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/path_count.png\") 0 0 0 0 strecth strecth;\n"
                                    "    border-width:2px;\n"
                                    "}")
        self.frame_93.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_93.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_93.setObjectName("frame_93")
        self.verticalLayout_72.addWidget(self.frame_93)
        self.horizontalLayout_31.addWidget(self.frame_92)
        self.frame_94 = QtWidgets.QFrame(self.frame_91)
        self.frame_94.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_94.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_94.setObjectName("frame_94")
        self.verticalLayout_73 = QtWidgets.QVBoxLayout(self.frame_94)
        self.verticalLayout_73.setContentsMargins(10, 12, 0, -1)
        self.verticalLayout_73.setSpacing(1)
        self.verticalLayout_73.setObjectName("verticalLayout_73")
        self.label_28 = QtWidgets.QLabel(self.frame_94)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_28.setObjectName("label_28")
        self.verticalLayout_73.addWidget(self.label_28)
        self.path_astar = QtWidgets.QLabel(self.frame_94)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.path_astar.setFont(font)
        self.path_astar.setStyleSheet("QLabel {\n"
                                      "    background:transparent;\n"
                                      "    color:rgb(84,91,103);\n"
                                      "}")
        self.path_astar.setObjectName("path_astar")
        self.verticalLayout_73.addWidget(self.path_astar)
        self.horizontalLayout_31.addWidget(self.frame_94)
        self.verticalLayout_57.addWidget(self.frame_91)
        self.frame_107 = QtWidgets.QFrame(self.frame_33)
        self.frame_107.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_107.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_107.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_107.setObjectName("frame_107")
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout(self.frame_107)
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.frame_108 = QtWidgets.QFrame(self.frame_107)
        self.frame_108.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_108.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_108.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_108.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_108.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_108.setObjectName("frame_108")
        self.verticalLayout_82 = QtWidgets.QVBoxLayout(self.frame_108)
        self.verticalLayout_82.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_82.setObjectName("verticalLayout_82")
        self.frame_109 = QtWidgets.QFrame(self.frame_108)
        self.frame_109.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/path_count.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width:2px;\n"
                                     "}")
        self.frame_109.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_109.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_109.setObjectName("frame_109")
        self.verticalLayout_82.addWidget(self.frame_109)
        self.horizontalLayout_35.addWidget(self.frame_108)
        self.frame_110 = QtWidgets.QFrame(self.frame_107)
        self.frame_110.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_110.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_110.setObjectName("frame_110")
        self.verticalLayout_83 = QtWidgets.QVBoxLayout(self.frame_110)
        self.verticalLayout_83.setContentsMargins(10, 12, 0, -1)
        self.verticalLayout_83.setSpacing(1)
        self.verticalLayout_83.setObjectName("verticalLayout_83")
        self.label_31 = QtWidgets.QLabel(self.frame_110)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_31.setObjectName("label_31")
        self.verticalLayout_83.addWidget(self.label_31)
        self.path_imAstar = QtWidgets.QLabel(self.frame_110)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.path_imAstar.setFont(font)
        self.path_imAstar.setStyleSheet("QLabel {\n"
                                        "    background:transparent;\n"
                                        "    color:rgb(84,91,103);\n"
                                        "}")
        self.path_imAstar.setObjectName("path_imAstar")
        self.verticalLayout_83.addWidget(self.path_imAstar)
        self.horizontalLayout_35.addWidget(self.frame_110)
        self.verticalLayout_57.addWidget(self.frame_107)
        self.verticalLayout_30.addWidget(self.frame_33, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_18.addWidget(
            self.frame_24, 0, QtCore.Qt.AlignTop)
        self.frame_25 = QtWidgets.QFrame(self.frame_18)
        self.frame_25.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.frame_25)
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.frame_26 = QtWidgets.QFrame(self.frame_25)
        self.frame_26.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.frame_26)
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.frame_27 = QtWidgets.QFrame(self.frame_26)
        self.frame_27.setMaximumSize(QtCore.QSize(490, 440))
        self.frame_27.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.frame_27)
        self.verticalLayout_29.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.label_9 = QtWidgets.QLabel(self.frame_27)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("QLabel {\n"
                                   "    color:rgb(215,215,215);\n"
                                   "}")
        self.label_9.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_29.addWidget(self.label_9)
        self.frameLapangan = QtWidgets.QFrame(self.frame_27)
        self.frameLapangan.setMinimumSize(QtCore.QSize(450, 300))
        self.frameLapangan.setMaximumSize(QtCore.QSize(450, 300))
        self.frameLapangan.setStyleSheet("")
        self.frameLapangan.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLapangan.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLapangan.setObjectName("frameLapangan")
        self.verticalLayout_46 = QtWidgets.QVBoxLayout(self.frameLapangan)
        self.verticalLayout_46.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_46.setSpacing(0)
        self.verticalLayout_46.setObjectName("verticalLayout_46")
        self.graph_view = QtWidgets.QGraphicsView(self.frameLapangan)
        self.graph_view.setStyleSheet("QGraphicsView {\n"
                                      "    background-color:transparent;\n"
                                      "    border-image: url(\"./assets/map.png\") 0 0 0 0 strecth strecth;\n"
                                      "    border-radius:0px;\n"
                                      "}")
        self.graph_view.setObjectName("graph_view")
        self.verticalLayout_46.addWidget(self.graph_view)
        self.verticalLayout_29.addWidget(self.frameLapangan)
        self.frame_28 = QtWidgets.QFrame(self.frame_27)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_28.sizePolicy().hasHeightForWidth())
        self.frame_28.setSizePolicy(sizePolicy)
        self.frame_28.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_28.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.verticalLayout_33 = QtWidgets.QVBoxLayout(self.frame_28)
        self.verticalLayout_33.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_33.setSpacing(0)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.btnStartSim = QtWidgets.QPushButton(self.frame_28)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnStartSim.sizePolicy().hasHeightForWidth())
        self.btnStartSim.setSizePolicy(sizePolicy)
        self.btnStartSim.setMinimumSize(QtCore.QSize(150, 0))
        self.btnStartSim.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnStartSim.setStyleSheet("QPushButton {\n"
                                       "    background:transparent;\n"
                                       "    border: 1px solid rgb(215,215,215);\n"
                                       "    border-radius:7.5px;\n"
                                       "    color:rgb(215,215,215);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover{\n"
                                       "    color:rgba(20,20,20,235);\n"
                                       "    background-color:rgb(215,215,215);\n"
                                       "    border:none;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color:rgb(28,28,28);\n"
                                       "    color:rgb(255,255,255);\n"
                                       "    border: 1.5px solid rgb(215,215,215);\n"
                                       "}\n"
                                       "")
        self.btnStartSim.setObjectName("btnStartSim")
        self.verticalLayout_33.addWidget(
            self.btnStartSim, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_29.addWidget(self.frame_28)
        self.frameLapangan.raise_()
        self.label_9.raise_()
        self.frame_28.raise_()
        self.verticalLayout_28.addWidget(self.frame_27)
        self.verticalLayout_27.addWidget(self.frame_26)
        self.horizontalLayout_18.addWidget(self.frame_25)
        self.verticalLayout_25.addWidget(self.frame_18)
        self.frame_23 = QtWidgets.QFrame(self.pageCore)
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.frame_23)
        self.verticalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_31.setSpacing(0)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.frame_6 = QtWidgets.QFrame(self.frame_23)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 160))
        self.frame_6.setStyleSheet("QFrame{\n"
                                   "    background-color:rgb(27,27,27);\n"
                                   "}")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_21.setContentsMargins(-1, 13, -1, 0)
        self.verticalLayout_21.setSpacing(10)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_15 = QtWidgets.QLabel(self.frame_6)
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "}")
        self.label_15.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_21.addWidget(self.label_15)
        self.frame_21 = QtWidgets.QFrame(self.frame_6)
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_21)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, -1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_29 = QtWidgets.QFrame(self.frame_21)
        self.frame_29.setMaximumSize(QtCore.QSize(225, 16777215))
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.verticalLayout_38 = QtWidgets.QVBoxLayout(self.frame_29)
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_38.setSpacing(0)
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.frame_99 = QtWidgets.QFrame(self.frame_29)
        self.frame_99.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_99.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_99.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_99.setObjectName("frame_99")
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.frame_99)
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_33.setSpacing(0)
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.frame_100 = QtWidgets.QFrame(self.frame_99)
        self.frame_100.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_100.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_100.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_100.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_100.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_100.setObjectName("frame_100")
        self.verticalLayout_76 = QtWidgets.QVBoxLayout(self.frame_100)
        self.verticalLayout_76.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_76.setObjectName("verticalLayout_76")
        self.frame_101 = QtWidgets.QFrame(self.frame_100)
        self.frame_101.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/ball.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.frame_101.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_101.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_101.setObjectName("frame_101")
        self.verticalLayout_76.addWidget(self.frame_101)
        self.horizontalLayout_33.addWidget(self.frame_100)
        self.frame_102 = QtWidgets.QFrame(self.frame_99)
        self.frame_102.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_102.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_102.setObjectName("frame_102")
        self.verticalLayout_58 = QtWidgets.QVBoxLayout(self.frame_102)
        self.verticalLayout_58.setContentsMargins(10, 5, 0, 5)
        self.verticalLayout_58.setSpacing(1)
        self.verticalLayout_58.setObjectName("verticalLayout_58")
        self.label_32 = QtWidgets.QLabel(self.frame_102)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_32.setObjectName("label_32")
        self.verticalLayout_58.addWidget(self.label_32)
        self.astar_start_2 = QtWidgets.QLabel(self.frame_102)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start_2.setFont(font)
        self.astar_start_2.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.astar_start_2.setObjectName("astar_start_2")
        self.verticalLayout_58.addWidget(self.astar_start_2)
        self.horizontalLayout_33.addWidget(self.frame_102)
        self.verticalLayout_38.addWidget(self.frame_99)
        self.frame_103 = QtWidgets.QFrame(self.frame_29)
        self.frame_103.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_103.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_103.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_103.setObjectName("frame_103")
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout(self.frame_103)
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.frame_104 = QtWidgets.QFrame(self.frame_103)
        self.frame_104.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_104.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_104.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_104.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_104.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_104.setObjectName("frame_104")
        self.verticalLayout_77 = QtWidgets.QVBoxLayout(self.frame_104)
        self.verticalLayout_77.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_77.setObjectName("verticalLayout_77")
        self.frame_105 = QtWidgets.QFrame(self.frame_104)
        self.frame_105.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/rObs.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width: -1px 2.75px -1px 2.75px;\n"
                                     "}")
        self.frame_105.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_105.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_105.setObjectName("frame_105")
        self.verticalLayout_77.addWidget(self.frame_105)
        self.horizontalLayout_34.addWidget(self.frame_104)
        self.frame_106 = QtWidgets.QFrame(self.frame_103)
        self.frame_106.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_106.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_106.setObjectName("frame_106")
        self.verticalLayout_59 = QtWidgets.QVBoxLayout(self.frame_106)
        self.verticalLayout_59.setContentsMargins(10, 5, 0, 5)
        self.verticalLayout_59.setSpacing(1)
        self.verticalLayout_59.setObjectName("verticalLayout_59")
        self.label_33 = QtWidgets.QLabel(self.frame_106)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_33.setObjectName("label_33")
        self.verticalLayout_59.addWidget(self.label_33)
        self.astar_start_3 = QtWidgets.QLabel(self.frame_106)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start_3.setFont(font)
        self.astar_start_3.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.astar_start_3.setObjectName("astar_start_3")
        self.verticalLayout_59.addWidget(self.astar_start_3)
        self.horizontalLayout_34.addWidget(self.frame_106)
        self.verticalLayout_38.addWidget(self.frame_103)
        self.horizontalLayout_4.addWidget(self.frame_29)
        self.frame_31 = QtWidgets.QFrame(self.frame_21)
        self.frame_31.setMinimumSize(QtCore.QSize(250, 0))
        self.frame_31.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_31.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_31.setObjectName("frame_31")
        self.verticalLayout_41 = QtWidgets.QVBoxLayout(self.frame_31)
        self.verticalLayout_41.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_41.setSpacing(0)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.frame_111 = QtWidgets.QFrame(self.frame_31)
        self.frame_111.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_111.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_111.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_111.setObjectName("frame_111")
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout(self.frame_111)
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.frame_112 = QtWidgets.QFrame(self.frame_111)
        self.frame_112.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_112.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_112.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_112.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_112.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_112.setObjectName("frame_112")
        self.verticalLayout_78 = QtWidgets.QVBoxLayout(self.frame_112)
        self.verticalLayout_78.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_78.setObjectName("verticalLayout_78")
        self.frame_113 = QtWidgets.QFrame(self.frame_112)
        self.frame_113.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/node_astar.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.frame_113.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_113.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_113.setObjectName("frame_113")
        self.verticalLayout_78.addWidget(self.frame_113)
        self.horizontalLayout_36.addWidget(self.frame_112)
        self.frame_114 = QtWidgets.QFrame(self.frame_111)
        self.frame_114.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_114.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_114.setObjectName("frame_114")
        self.verticalLayout_60 = QtWidgets.QVBoxLayout(self.frame_114)
        self.verticalLayout_60.setContentsMargins(10, 5, 0, 5)
        self.verticalLayout_60.setSpacing(1)
        self.verticalLayout_60.setObjectName("verticalLayout_60")
        self.label_34 = QtWidgets.QLabel(self.frame_114)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_34.setObjectName("label_34")
        self.verticalLayout_60.addWidget(self.label_34)
        self.astar_start_4 = QtWidgets.QLabel(self.frame_114)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start_4.setFont(font)
        self.astar_start_4.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.astar_start_4.setObjectName("astar_start_4")
        self.verticalLayout_60.addWidget(self.astar_start_4)
        self.horizontalLayout_36.addWidget(self.frame_114)
        self.verticalLayout_41.addWidget(self.frame_111)
        self.frame_115 = QtWidgets.QFrame(self.frame_31)
        self.frame_115.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_115.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_115.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_115.setObjectName("frame_115")
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout(self.frame_115)
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_37.setSpacing(0)
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.frame_116 = QtWidgets.QFrame(self.frame_115)
        self.frame_116.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_116.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_116.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_116.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_116.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_116.setObjectName("frame_116")
        self.verticalLayout_79 = QtWidgets.QVBoxLayout(self.frame_116)
        self.verticalLayout_79.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_79.setObjectName("verticalLayout_79")
        self.frame_117 = QtWidgets.QFrame(self.frame_116)
        self.frame_117.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/node_imastar.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.frame_117.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_117.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_117.setObjectName("frame_117")
        self.verticalLayout_79.addWidget(self.frame_117)
        self.horizontalLayout_37.addWidget(self.frame_116)
        self.frame_118 = QtWidgets.QFrame(self.frame_115)
        self.frame_118.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_118.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_118.setObjectName("frame_118")
        self.verticalLayout_61 = QtWidgets.QVBoxLayout(self.frame_118)
        self.verticalLayout_61.setContentsMargins(10, 5, 0, 5)
        self.verticalLayout_61.setSpacing(1)
        self.verticalLayout_61.setObjectName("verticalLayout_61")
        self.label_35 = QtWidgets.QLabel(self.frame_118)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_35.setObjectName("label_35")
        self.verticalLayout_61.addWidget(self.label_35)
        self.astar_start_5 = QtWidgets.QLabel(self.frame_118)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start_5.setFont(font)
        self.astar_start_5.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.astar_start_5.setObjectName("astar_start_5")
        self.verticalLayout_61.addWidget(self.astar_start_5)
        self.horizontalLayout_37.addWidget(self.frame_118)
        self.verticalLayout_41.addWidget(self.frame_115)
        self.horizontalLayout_4.addWidget(self.frame_31)
        self.frame_32 = QtWidgets.QFrame(self.frame_21)
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.verticalLayout_43 = QtWidgets.QVBoxLayout(self.frame_32)
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_43.setSpacing(0)
        self.verticalLayout_43.setObjectName("verticalLayout_43")
        self.frame_123 = QtWidgets.QFrame(self.frame_32)
        self.frame_123.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_123.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_123.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_123.setObjectName("frame_123")
        self.horizontalLayout_40 = QtWidgets.QHBoxLayout(self.frame_123)
        self.horizontalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_40.setSpacing(0)
        self.horizontalLayout_40.setObjectName("horizontalLayout_40")
        self.frame_130 = QtWidgets.QFrame(self.frame_123)
        self.frame_130.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_130.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_130.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_130.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_130.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_130.setObjectName("frame_130")
        self.verticalLayout_85 = QtWidgets.QVBoxLayout(self.frame_130)
        self.verticalLayout_85.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_85.setObjectName("verticalLayout_85")
        self.frame_131 = QtWidgets.QFrame(self.frame_130)
        self.frame_131.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/rAsli.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width: -1px 2.75px -1px 2.75px;\n"
                                     "}")
        self.frame_131.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_131.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_131.setObjectName("frame_131")
        self.verticalLayout_85.addWidget(self.frame_131)
        self.horizontalLayout_40.addWidget(self.frame_130)
        self.frame_132 = QtWidgets.QFrame(self.frame_123)
        self.frame_132.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_132.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_132.setObjectName("frame_132")
        self.verticalLayout_65 = QtWidgets.QVBoxLayout(self.frame_132)
        self.verticalLayout_65.setContentsMargins(10, 5, 0, 5)
        self.verticalLayout_65.setSpacing(1)
        self.verticalLayout_65.setObjectName("verticalLayout_65")
        self.label_39 = QtWidgets.QLabel(self.frame_132)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_39.setFont(font)
        self.label_39.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_39.setObjectName("label_39")
        self.verticalLayout_65.addWidget(self.label_39)
        self.astar_start_9 = QtWidgets.QLabel(self.frame_132)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start_9.setFont(font)
        self.astar_start_9.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.astar_start_9.setObjectName("astar_start_9")
        self.verticalLayout_65.addWidget(self.astar_start_9)
        self.horizontalLayout_40.addWidget(self.frame_132)
        self.verticalLayout_43.addWidget(self.frame_123)
        self.frame_119 = QtWidgets.QFrame(self.frame_32)
        self.frame_119.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_119.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_119.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_119.setObjectName("frame_119")
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout(self.frame_119)
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_38.setSpacing(0)
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.frame_120 = QtWidgets.QFrame(self.frame_119)
        self.frame_120.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_120.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_120.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(195,196,196);\n"
                                     "    border-radius:10px;\n"
                                     "}")
        self.frame_120.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_120.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_120.setObjectName("frame_120")
        self.verticalLayout_80 = QtWidgets.QVBoxLayout(self.frame_120)
        self.verticalLayout_80.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_80.setObjectName("verticalLayout_80")
        self.frame_121 = QtWidgets.QFrame(self.frame_120)
        self.frame_121.setStyleSheet("QFrame{\n"
                                     "    border-image: url(\"./assets/node_scc.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.frame_121.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_121.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_121.setObjectName("frame_121")
        self.verticalLayout_80.addWidget(self.frame_121)
        self.horizontalLayout_38.addWidget(self.frame_120)
        self.frame_122 = QtWidgets.QFrame(self.frame_119)
        self.frame_122.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_122.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_122.setObjectName("frame_122")
        self.verticalLayout_62 = QtWidgets.QVBoxLayout(self.frame_122)
        self.verticalLayout_62.setContentsMargins(10, 5, 0, 5)
        self.verticalLayout_62.setSpacing(1)
        self.verticalLayout_62.setObjectName("verticalLayout_62")
        self.label_36 = QtWidgets.QLabel(self.frame_122)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_36.setObjectName("label_36")
        self.verticalLayout_62.addWidget(self.label_36)
        self.astar_start_6 = QtWidgets.QLabel(self.frame_122)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.astar_start_6.setFont(font)
        self.astar_start_6.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(84,91,103);\n"
                                         "}")
        self.astar_start_6.setObjectName("astar_start_6")
        self.verticalLayout_62.addWidget(self.astar_start_6)
        self.horizontalLayout_38.addWidget(self.frame_122)
        self.verticalLayout_43.addWidget(self.frame_119)
        self.horizontalLayout_4.addWidget(self.frame_32)
        self.verticalLayout_21.addWidget(self.frame_21)
        self.verticalLayout_31.addWidget(self.frame_6)
        self.verticalLayout_25.addWidget(self.frame_23)
        self.stackedWidget.addWidget(self.pageCore)
        self.pageSocket = QtWidgets.QWidget()
        self.pageSocket.setObjectName("pageSocket")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.pageSocket)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.scrollSocket = QtWidgets.QScrollArea(self.pageSocket)
        self.scrollSocket.setStyleSheet("QScrollArea{\n"
                                        "    background:transparent;\n"
                                        "}")
        self.scrollSocket.setWidgetResizable(True)
        self.scrollSocket.setObjectName("scrollSocket")
        self.scrollSocketWidget = QtWidgets.QWidget()
        self.scrollSocketWidget.setGeometry(QtCore.QRect(0, 0, 715, 618))
        self.scrollSocketWidget.setStyleSheet("")
        self.scrollSocketWidget.setObjectName("scrollSocketWidget")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.scrollSocketWidget)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.frameSccChange = QtWidgets.QFrame(self.scrollSocketWidget)
        self.frameSccChange.setMaximumSize(QtCore.QSize(16777215, 195))
        self.frameSccChange.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSccChange.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameSccChange.setObjectName("frameSccChange")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frameSccChange)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frameSocketV = QtWidgets.QFrame(self.frameSccChange)
        self.frameSocketV.setMinimumSize(QtCore.QSize(400, 0))
        self.frameSocketV.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frameSocketV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSocketV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameSocketV.setObjectName("frameSocketV")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frameSocketV)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.frameFormSocket = QtWidgets.QFrame(self.frameSocketV)
        self.frameFormSocket.setMinimumSize(QtCore.QSize(400, 195))
        self.frameFormSocket.setMaximumSize(QtCore.QSize(400, 195))
        self.frameFormSocket.setStyleSheet("QFrame{\n"
                                           "    background-color:rgb(27,27,27);\n"
                                           "}")
        self.frameFormSocket.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameFormSocket.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameFormSocket.setObjectName("frameFormSocket")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.frameFormSocket)
        self.verticalLayout_18.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.frame_19 = QtWidgets.QFrame(self.frameFormSocket)
        self.frame_19.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_19.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.frame_19)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_4 = QtWidgets.QLabel(self.frame_19)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel {\n"
                                   "    color:rgb(215,215,215);\n"
                                   "}")
        self.label_4.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_19.addWidget(self.label_4)
        self.verticalLayout_18.addWidget(self.frame_19)
        self.frame_20 = QtWidgets.QFrame(self.frameFormSocket)
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_20)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.frame_14 = QtWidgets.QFrame(self.frame_20)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_13.addWidget(self.frame_14)
        self.frame_15 = QtWidgets.QFrame(self.frame_20)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.groupPortSocket = QtWidgets.QGroupBox(self.frame_15)
        self.groupPortSocket.setMinimumSize(QtCore.QSize(250, 55))
        self.groupPortSocket.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.groupPortSocket.setFont(font)
        self.groupPortSocket.setStyleSheet("*{\n"
                                           "    background:transparent;\n"
                                           "}\n"
                                           "\n"
                                           "QGroupBox{\n"
                                           "    border: 1px solid rgb(255,255,255);\n"
                                           "    border-radius:10px;\n"
                                           "    margin-top:0.5em;\n"
                                           "}\n"
                                           "\n"
                                           "QGroupBox::title{\n"
                                           "    subcontrol-origin:margin;\n"
                                           "    left:10px;\n"
                                           "    padding-top:-6px;\n"
                                           "    color:rgb(255,255,255);\n"
                                           "}")
        self.groupPortSocket.setObjectName("groupPortSocket")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.groupPortSocket)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.frame_22 = QtWidgets.QFrame(self.groupPortSocket)
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.frame_22)
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.linePortSocket = QtWidgets.QLineEdit(self.frame_22)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.linePortSocket.sizePolicy().hasHeightForWidth())
        self.linePortSocket.setSizePolicy(sizePolicy)
        self.linePortSocket.setStyleSheet("QLineEdit {\n"
                                          "    border:none;\n"
                                          "    margin-left:10px;\n"
                                          "    color:rgb(215,215,215);\n"
                                          "}")
        self.linePortSocket.setObjectName("linePortSocket")
        self.verticalLayout_22.addWidget(self.linePortSocket)
        self.horizontalLayout_16.addWidget(self.frame_22)
        self.imgAlertPortSocket = QtWidgets.QFrame(self.groupPortSocket)
        self.imgAlertPortSocket.setMinimumSize(QtCore.QSize(50, 0))
        self.imgAlertPortSocket.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.imgAlertPortSocket.setStyleSheet("QFrame [cond = \"err\"]{\n"
                                              "    background-color:transparent;\n"
                                              "    border-image: url(\"./assets/err.png\") 0 0 0 0 strecth strecth;\n"
                                              "    border-width:10px 13px 10px 13px;\n"
                                              "}\n"
                                              "\n"
                                              "QFrame [cond = \"scc\"]{\n"
                                              "    background-color:transparent;\n"
                                              "    border-image: url(\"./assets/scc.png\") 0 0 0 0 strecth strecth;\n"
                                              "    border-width:10px 13px 10px 13px;\n"
                                              "}")
        self.imgAlertPortSocket.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgAlertPortSocket.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgAlertPortSocket.setObjectName("imgAlertPortSocket")
        self.horizontalLayout_16.addWidget(self.imgAlertPortSocket)
        self.verticalLayout_15.addWidget(self.groupPortSocket)
        self.msgAlertPortSocket = QtWidgets.QLabel(self.frame_15)
        self.msgAlertPortSocket.setStyleSheet("* {\n"
                                              "    border:none;\n"
                                              "    margin-top:5px;\n"
                                              "    margin-left:10px;\n"
                                              "}\n"
                                              "\n"
                                              "QLabel[cond = \"err\"]{\n"
                                              "    color:rgb(226,75,59);\n"
                                              "}\n"
                                              "\n"
                                              "QLabel[cond = \"scc\"]{\n"
                                              "    color:rgb(38,224,127);\n"
                                              "}\n"
                                              "")
        self.msgAlertPortSocket.setText("")
        self.msgAlertPortSocket.setObjectName("msgAlertPortSocket")
        self.verticalLayout_15.addWidget(self.msgAlertPortSocket)
        self.verticalLayout_13.addWidget(self.frame_15)
        self.verticalLayout_18.addWidget(self.frame_20, 0, QtCore.Qt.AlignTop)
        self.frameBtnSock = QtWidgets.QFrame(self.frameFormSocket)
        self.frameBtnSock.setEnabled(True)
        self.frameBtnSock.setMinimumSize(QtCore.QSize(0, 40))
        self.frameBtnSock.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frameBtnSock.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnSock.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnSock.setObjectName("frameBtnSock")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frameBtnSock)
        self.horizontalLayout_13.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.btnSocketConn = QtWidgets.QPushButton(self.frameBtnSock)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnSocketConn.sizePolicy().hasHeightForWidth())
        self.btnSocketConn.setSizePolicy(sizePolicy)
        self.btnSocketConn.setMinimumSize(QtCore.QSize(120, 0))
        self.btnSocketConn.setStyleSheet("QPushButton {\n"
                                         "    background:transparent;\n"
                                         "    border: 1px solid rgb(215,215,215);\n"
                                         "    border-radius:7.5px;\n"
                                         "    color:rgb(215,215,215);\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "    color:rgba(20,20,20,235);\n"
                                         "    background-color:rgb(215,215,215);\n"
                                         "    border:none;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:pressed{\n"
                                         "    background-color:rgb(28,28,28);\n"
                                         "    color:rgb(215,215,215);\n"
                                         "    border: 1.5px solid rgb(215,215,215);\n"
                                         "}\n"
                                         "")
        self.btnSocketConn.setObjectName("btnSocketConn")
        self.horizontalLayout_13.addWidget(self.btnSocketConn)
        self.verticalLayout_18.addWidget(
            self.frameBtnSock, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_12.addWidget(self.frameFormSocket)
        self.horizontalLayout_12.addWidget(
            self.frameSocketV, 0, QtCore.Qt.AlignTop)
        self.frameSocketStats = QtWidgets.QFrame(self.frameSccChange)
        self.frameSocketStats.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSocketStats.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameSocketStats.setObjectName("frameSocketStats")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.frameSocketStats)
        self.verticalLayout_17.setContentsMargins(20, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.frame_35 = QtWidgets.QFrame(self.frameSocketStats)
        self.frame_35.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_35.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_35.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")
        self.verticalLayout_34 = QtWidgets.QVBoxLayout(self.frame_35)
        self.verticalLayout_34.setContentsMargins(20, 20, 20, 10)
        self.verticalLayout_34.setSpacing(0)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.label_10 = QtWidgets.QLabel(self.frame_35)
        self.label_10.setMinimumSize(QtCore.QSize(0, 25))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "}")
        self.label_10.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_34.addWidget(self.label_10)
        self.frame_17 = QtWidgets.QFrame(self.frame_35)
        self.frame_17.setStyleSheet("QFrame {\n"
                                    "    background-color:transparent;\n"
                                    "    border-radius:0pxx;\n"
                                    "}")
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.frame_17)
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.frameDescRobot = QtWidgets.QFrame(self.frame_17)
        self.frameDescRobot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameDescRobot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameDescRobot.setObjectName("frameDescRobot")
        self.verticalLayout_35 = QtWidgets.QVBoxLayout(self.frameDescRobot)
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_35.setSpacing(0)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.frame_38 = QtWidgets.QFrame(self.frameDescRobot)
        self.frame_38.setMinimumSize(QtCore.QSize(0, 71))
        self.frame_38.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_38.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_38.setObjectName("frame_38")
        self.verticalLayout_36 = QtWidgets.QVBoxLayout(self.frame_38)
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.frame_40 = QtWidgets.QFrame(self.frame_38)
        self.frame_40.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_40.setObjectName("frame_40")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_40)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.frame_43 = QtWidgets.QFrame(self.frame_40)
        self.frame_43.setMaximumSize(QtCore.QSize(50, 50))
        self.frame_43.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(195,196,196);\n"
                                    "    border-radius:15px;\n"
                                    "}")
        self.frame_43.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_43.setObjectName("frame_43")
        self.verticalLayout_39 = QtWidgets.QVBoxLayout(self.frame_43)
        self.verticalLayout_39.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.frame_49 = QtWidgets.QFrame(self.frame_43)
        self.frame_49.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/server.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_49.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_49.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_49.setObjectName("frame_49")
        self.verticalLayout_39.addWidget(self.frame_49)
        self.horizontalLayout_20.addWidget(self.frame_43)
        self.frame_44 = QtWidgets.QFrame(self.frame_40)
        self.frame_44.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_44.setObjectName("frame_44")
        self.verticalLayout_42 = QtWidgets.QVBoxLayout(self.frame_44)
        self.verticalLayout_42.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_42.setSpacing(0)
        self.verticalLayout_42.setObjectName("verticalLayout_42")
        self.label_11 = QtWidgets.QLabel(self.frame_44)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_42.addWidget(self.label_11)
        self.descServer = QtWidgets.QLabel(self.frame_44)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descServer.setFont(font)
        self.descServer.setStyleSheet("QLabel {\n"
                                      "    background:transparent;\n"
                                      "    color:rgb(84,91,103);\n"
                                      "}")
        self.descServer.setObjectName("descServer")
        self.verticalLayout_42.addWidget(self.descServer)
        self.horizontalLayout_20.addWidget(
            self.frame_44, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_36.addWidget(self.frame_40)
        self.hrLine_2 = QtWidgets.QFrame(self.frame_38)
        self.hrLine_2.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_2.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine_2.setStyleSheet("*{\n"
                                    "    background-color:rgba(136,149,169,130);\n"
                                    "}")
        self.hrLine_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_2.setObjectName("hrLine_2")
        self.verticalLayout_36.addWidget(self.hrLine_2)
        self.verticalLayout_35.addWidget(self.frame_38)
        self.frame_39 = QtWidgets.QFrame(self.frameDescRobot)
        self.frame_39.setMinimumSize(QtCore.QSize(0, 71))
        self.frame_39.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_39.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_39.setObjectName("frame_39")
        self.verticalLayout_37 = QtWidgets.QVBoxLayout(self.frame_39)
        self.verticalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_37.setSpacing(0)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.frame_41 = QtWidgets.QFrame(self.frame_39)
        self.frame_41.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_41.setObjectName("frame_41")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_41)
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.frame_46 = QtWidgets.QFrame(self.frame_41)
        self.frame_46.setMaximumSize(QtCore.QSize(50, 50))
        self.frame_46.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(195,196,196);\n"
                                    "    border-radius:15px;\n"
                                    "}")
        self.frame_46.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_46.setObjectName("frame_46")
        self.verticalLayout_40 = QtWidgets.QVBoxLayout(self.frame_46)
        self.verticalLayout_40.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.frame_50 = QtWidgets.QFrame(self.frame_46)
        self.frame_50.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/rObs.png\") 0 0 0 0 strecth strecth;\n"
                                    "    border-width: 0 5.5px 0 5.5px;\n"
                                    "}")
        self.frame_50.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_50.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_50.setObjectName("frame_50")
        self.verticalLayout_40.addWidget(self.frame_50)
        self.horizontalLayout_22.addWidget(self.frame_46)
        self.frame_45 = QtWidgets.QFrame(self.frame_41)
        self.frame_45.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_45.setObjectName("frame_45")
        self.verticalLayout_44 = QtWidgets.QVBoxLayout(self.frame_45)
        self.verticalLayout_44.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_44.setSpacing(0)
        self.verticalLayout_44.setObjectName("verticalLayout_44")
        self.label_13 = QtWidgets.QLabel(self.frame_45)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(215,215,215);\n"
                                    "}")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_44.addWidget(self.label_13)
        self.descObs = QtWidgets.QLabel(self.frame_45)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descObs.setFont(font)
        self.descObs.setStyleSheet("QLabel {\n"
                                   "    background:transparent;\n"
                                   "    color:rgb(84,91,103);\n"
                                   "}")
        self.descObs.setObjectName("descObs")
        self.verticalLayout_44.addWidget(self.descObs)
        self.horizontalLayout_22.addWidget(
            self.frame_45, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_37.addWidget(
            self.frame_41, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout_35.addWidget(self.frame_39)
        self.verticalLayout_26.addWidget(
            self.frameDescRobot, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_34.addWidget(self.frame_17)
        self.verticalLayout_17.addWidget(self.frame_35)
        self.horizontalLayout_12.addWidget(self.frameSocketStats)
        self.verticalLayout_20.addWidget(self.frameSccChange)
        self.frame_10 = QtWidgets.QFrame(self.scrollSocketWidget)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_16.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.frame_16 = QtWidgets.QFrame(self.frame_10)
        self.frame_16.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.verticalLayout_32 = QtWidgets.QVBoxLayout(self.frame_16)
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_32.setSpacing(10)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.frame_12 = QtWidgets.QFrame(self.frame_16)
        self.frame_12.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_14.setContentsMargins(20, 20, 0, 0)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_5 = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("QLabel {\n"
                                   "    color:rgb(215,215,215);\n"
                                   "}")
        self.label_5.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_14.addWidget(self.label_5)
        self.verticalLayout_32.addWidget(self.frame_12)
        self.frame_13 = QtWidgets.QFrame(self.frame_16)
        self.frame_13.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_13.setStyleSheet("")
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.frame_9 = QtWidgets.QFrame(self.frame_13)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_17.setContentsMargins(0, 0, 20, 10)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_3 = QtWidgets.QLabel(self.frame_9)
        self.label_3.setMinimumSize(QtCore.QSize(180, 0))
        self.label_3.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel {\n"
                                   "    background:transparent;\n"
                                   "    color:rgb(84,91,103);\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_17.addWidget(self.label_3)
        self.label_6 = QtWidgets.QLabel(self.frame_9)
        self.label_6.setMinimumSize(QtCore.QSize(100, 0))
        self.label_6.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("QLabel {\n"
                                   "    background:transparent;\n"
                                   "    color:rgb(84,91,103);\n"
                                   "}")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_17.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_9)
        self.label_7.setMinimumSize(QtCore.QSize(200, 0))
        self.label_7.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("QLabel {\n"
                                   "    background:transparent;\n"
                                   "    color:rgb(84,91,103);\n"
                                   "}")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_17.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_9)
        self.label_8.setMinimumSize(QtCore.QSize(124, 0))
        self.label_8.setMaximumSize(QtCore.QSize(124, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("QLabel {\n"
                                   "    background:transparent;\n"
                                   "    color:rgb(84,91,103);\n"
                                   "}")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_17.addWidget(self.label_8)
        self.verticalLayout_23.addWidget(self.frame_9)
        self.hrLine = QtWidgets.QFrame(self.frame_13)
        self.hrLine.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine.setStyleSheet("*{\n"
                                  "    background-color:rgba(136,149,169,130);\n"
                                  "}")
        self.hrLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine.setObjectName("hrLine")
        self.verticalLayout_23.addWidget(self.hrLine)
        self.frameTampungList = QtWidgets.QFrame(self.frame_13)
        self.frameTampungList.setStyleSheet("")
        self.frameTampungList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTampungList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTampungList.setObjectName("frameTampungList")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.frameTampungList)
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.verticalLayout_23.addWidget(
            self.frameTampungList, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_32.addWidget(self.frame_13)
        self.verticalLayout_16.addWidget(self.frame_16)
        self.verticalLayout_20.addWidget(self.frame_10)
        self.scrollSocket.setWidget(self.scrollSocketWidget)
        self.verticalLayout_11.addWidget(self.scrollSocket)
        self.stackedWidget.addWidget(self.pageSocket)
        self.pageHistory = QtWidgets.QWidget()
        self.pageHistory.setObjectName("pageHistory")
        self.verticalLayout_87 = QtWidgets.QVBoxLayout(self.pageHistory)
        self.verticalLayout_87.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_87.setSpacing(0)
        self.verticalLayout_87.setObjectName("verticalLayout_87")
        self.stack_history = QtWidgets.QStackedWidget(self.pageHistory)
        self.stack_history.setObjectName("stack_history")
        self.history_view = QtWidgets.QWidget()
        self.history_view.setObjectName("history_view")
        self.verticalLayout_92 = QtWidgets.QVBoxLayout(self.history_view)
        self.verticalLayout_92.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_92.setSpacing(0)
        self.verticalLayout_92.setObjectName("verticalLayout_92")
        self.frame_71 = QtWidgets.QFrame(self.history_view)
        self.frame_71.setStyleSheet("")
        self.frame_71.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_71.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_71.setObjectName("frame_71")
        self.verticalLayout_88 = QtWidgets.QVBoxLayout(self.frame_71)
        self.verticalLayout_88.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_88.setSpacing(0)
        self.verticalLayout_88.setObjectName("verticalLayout_88")
        self.scrolHistory = QtWidgets.QScrollArea(self.frame_71)
        self.scrolHistory.setWidgetResizable(True)
        self.scrolHistory.setObjectName("scrolHistory")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 633, 101))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_93 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout_93.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_93.setSpacing(0)
        self.verticalLayout_93.setObjectName("verticalLayout_93")
        self.frame_72 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_72.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_72.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_72.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_72.setObjectName("frame_72")
        self.verticalLayout_89 = QtWidgets.QVBoxLayout(self.frame_72)
        self.verticalLayout_89.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_89.setSpacing(10)
        self.verticalLayout_89.setObjectName("verticalLayout_89")
        self.frame_73 = QtWidgets.QFrame(self.frame_72)
        self.frame_73.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_73.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_73.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_73.setObjectName("frame_73")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_73)
        self.horizontalLayout_15.setContentsMargins(20, 20, 0, 0)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_17 = QtWidgets.QLabel(self.frame_73)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "}")
        self.label_17.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_15.addWidget(self.label_17)
        self.verticalLayout_89.addWidget(self.frame_73)
        self.frame_74 = QtWidgets.QFrame(self.frame_72)
        self.frame_74.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_74.setStyleSheet("")
        self.frame_74.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_74.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_74.setObjectName("frame_74")
        self.verticalLayout_90 = QtWidgets.QVBoxLayout(self.frame_74)
        self.verticalLayout_90.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_90.setSpacing(0)
        self.verticalLayout_90.setObjectName("verticalLayout_90")
        self.frame_75 = QtWidgets.QFrame(self.frame_74)
        self.frame_75.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_75.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_75.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_75.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_75.setObjectName("frame_75")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_75)
        self.horizontalLayout_19.setContentsMargins(20, 0, 0, 10)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_19 = QtWidgets.QLabel(self.frame_75)
        self.label_19.setMinimumSize(QtCore.QSize(73, 0))
        self.label_19.setMaximumSize(QtCore.QSize(73, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_19.addWidget(
            self.label_19, 0, QtCore.Qt.AlignLeft)
        self.label_20 = QtWidgets.QLabel(self.frame_75)
        self.label_20.setMinimumSize(QtCore.QSize(177, 0))
        self.label_20.setMaximumSize(QtCore.QSize(177, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_19.addWidget(
            self.label_20, 0, QtCore.Qt.AlignLeft)
        self.label_21 = QtWidgets.QLabel(self.frame_75)
        self.label_21.setMinimumSize(QtCore.QSize(213, 0))
        self.label_21.setMaximumSize(QtCore.QSize(213, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_19.addWidget(
            self.label_21, 0, QtCore.Qt.AlignLeft)
        self.label_22 = QtWidgets.QLabel(self.frame_75)
        self.label_22.setMinimumSize(QtCore.QSize(150, 0))
        self.label_22.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_19.addWidget(
            self.label_22, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_90.addWidget(self.frame_75, 0, QtCore.Qt.AlignLeft)
        self.hrLine_3 = QtWidgets.QFrame(self.frame_74)
        self.hrLine_3.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_3.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine_3.setStyleSheet("*{\n"
                                    "    background-color:rgba(136,149,169,130);\n"
                                    "}")
        self.hrLine_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_3.setObjectName("hrLine_3")
        self.verticalLayout_90.addWidget(self.hrLine_3)
        self.frame_historyV = QtWidgets.QFrame(self.frame_74)
        self.frame_historyV.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_historyV.setStyleSheet("")
        self.frame_historyV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_historyV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_historyV.setObjectName("frame_historyV")
        self.verticalLayout_91 = QtWidgets.QVBoxLayout(self.frame_historyV)
        self.verticalLayout_91.setContentsMargins(0, 10, 10, 10)
        self.verticalLayout_91.setSpacing(0)
        self.verticalLayout_91.setObjectName("verticalLayout_91")
        self.verticalLayout_90.addWidget(
            self.frame_historyV, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_89.addWidget(self.frame_74)
        self.verticalLayout_93.addWidget(self.frame_72)
        self.scrolHistory.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_88.addWidget(self.scrolHistory)
        self.verticalLayout_92.addWidget(self.frame_71)
        self.stack_history.addWidget(self.history_view)
        self.history_result = QtWidgets.QWidget()
        self.history_result.setObjectName("history_result")
        self.verticalLayout_94 = QtWidgets.QVBoxLayout(self.history_result)
        self.verticalLayout_94.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_94.setSpacing(0)
        self.verticalLayout_94.setObjectName("verticalLayout_94")
        self.frame_76 = QtWidgets.QFrame(self.history_result)
        self.frame_76.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_76.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_76.setObjectName("frame_76")
        self.verticalLayout_95 = QtWidgets.QVBoxLayout(self.frame_76)
        self.verticalLayout_95.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_95.setSpacing(0)
        self.verticalLayout_95.setObjectName("verticalLayout_95")
        self.frame_78 = QtWidgets.QFrame(self.frame_76)
        self.frame_78.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_78.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_78.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_78.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_78.setObjectName("frame_78")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_78)
        self.horizontalLayout_21.setContentsMargins(20, 0, 5, 0)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.frame_79 = QtWidgets.QFrame(self.frame_78)
        self.frame_79.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_79.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_79.setObjectName("frame_79")
        self.verticalLayout_96 = QtWidgets.QVBoxLayout(self.frame_79)
        self.verticalLayout_96.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_96.setSpacing(0)
        self.verticalLayout_96.setObjectName("verticalLayout_96")
        self.history_id = QtWidgets.QLabel(self.frame_79)
        self.history_id.setMinimumSize(QtCore.QSize(0, 30))
        self.history_id.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.history_id.setFont(font)
        self.history_id.setStyleSheet("QLabel {\n"
                                      "    color:rgb(215,215,215);\n"
                                      "}")
        self.history_id.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.history_id.setObjectName("history_id")
        self.verticalLayout_96.addWidget(
            self.history_id, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_21.addWidget(
            self.frame_79, 0, QtCore.Qt.AlignTop)
        self.quit_history = QtWidgets.QFrame(self.frame_78)
        self.quit_history.setMinimumSize(QtCore.QSize(38, 33))
        self.quit_history.setMaximumSize(QtCore.QSize(38, 33))
        self.quit_history.setStyleSheet("QFrame {\n"
                                        "    background-color:transparent;\n"
                                        "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                        "    border-width:6px 9px 6px 9px\n"
                                        "}\n"
                                        "\n"
                                        "QFrame:hover{\n"
                                        "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                        "}")
        self.quit_history.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quit_history.setFrameShadow(QtWidgets.QFrame.Raised)
        self.quit_history.setObjectName("quit_history")
        self.horizontalLayout_21.addWidget(self.quit_history)
        self.verticalLayout_95.addWidget(self.frame_78)
        self.frame_77 = QtWidgets.QFrame(self.frame_76)
        self.frame_77.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_77.setObjectName("frame_77")
        self.verticalLayout_97 = QtWidgets.QVBoxLayout(self.frame_77)
        self.verticalLayout_97.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_97.setObjectName("verticalLayout_97")
        self.frame_80 = QtWidgets.QFrame(self.frame_77)
        self.frame_80.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_80.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_80.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_80.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_80.setObjectName("frame_80")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.frame_80)
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.frame_plot_history = QtWidgets.QFrame(self.frame_80)
        self.frame_plot_history.setMinimumSize(QtCore.QSize(0, 535))
        self.frame_plot_history.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.frame_plot_history.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot_history.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot_history.setObjectName("frame_plot_history")
        self.verticalLayout_99 = QtWidgets.QVBoxLayout(self.frame_plot_history)
        self.verticalLayout_99.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_99.setSpacing(0)
        self.verticalLayout_99.setObjectName("verticalLayout_99")
        self.plot_history = QtWidgets.QVBoxLayout()
        self.plot_history.setSpacing(0)
        self.plot_history.setObjectName("plot_history")
        self.verticalLayout_99.addLayout(self.plot_history)
        self.horizontalLayout_30.addWidget(self.frame_plot_history)
        self.verticalLayout_97.addWidget(self.frame_80)
        self.verticalLayout_95.addWidget(self.frame_77, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_94.addWidget(self.frame_76)
        self.stack_history.addWidget(self.history_result)
        self.verticalLayout_87.addWidget(self.stack_history)
        self.stackedWidget.addWidget(self.pageHistory)
        self.pageTesting = QtWidgets.QWidget()
        self.pageTesting.setObjectName("pageTesting")
        self.verticalLayout_109 = QtWidgets.QVBoxLayout(self.pageTesting)
        self.verticalLayout_109.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_109.setSpacing(0)
        self.verticalLayout_109.setObjectName("verticalLayout_109")
        self.frame_139 = QtWidgets.QFrame(self.pageTesting)
        self.frame_139.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_139.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_139.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-radius:none;\n"
                                     "}")
        self.frame_139.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_139.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_139.setObjectName("frame_139")
        self.verticalLayout_110 = QtWidgets.QVBoxLayout(self.frame_139)
        self.verticalLayout_110.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_110.setSpacing(0)
        self.verticalLayout_110.setObjectName("verticalLayout_110")
        self.frame_141 = QtWidgets.QFrame(self.frame_139)
        self.frame_141.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_141.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_141.setObjectName("frame_141")
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout(self.frame_141)
        self.horizontalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_44.setSpacing(0)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.btnAkurasi = QtWidgets.QFrame(self.frame_141)
        self.btnAkurasi.setMinimumSize(QtCore.QSize(138, 0))
        self.btnAkurasi.setMaximumSize(QtCore.QSize(138, 16777215))
        self.btnAkurasi.setStyleSheet("QFrame:hover{\n"
                                      "    background-color:rgba(59,60,77,255);\n"
                                      "    border-radius: 0px;\n"
                                      "}")
        self.btnAkurasi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btnAkurasi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnAkurasi.setObjectName("btnAkurasi")
        self.verticalLayout_112 = QtWidgets.QVBoxLayout(self.btnAkurasi)
        self.verticalLayout_112.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_112.setSpacing(0)
        self.verticalLayout_112.setObjectName("verticalLayout_112")
        self.label_44 = QtWidgets.QLabel(self.btnAkurasi)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_44.setFont(font)
        self.label_44.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "    padding-left:2.5px;\n"
                                    "    margin-left:5px;\n"
                                    "}")
        self.label_44.setObjectName("label_44")
        self.verticalLayout_112.addWidget(self.label_44)
        self.horizontalLayout_44.addWidget(self.btnAkurasi)
        self.btnPresepsi = QtWidgets.QFrame(self.frame_141)
        self.btnPresepsi.setMinimumSize(QtCore.QSize(150, 0))
        self.btnPresepsi.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnPresepsi.setStyleSheet("QFrame:hover{\n"
                                       "    background-color:rgba(59,60,77,255);\n"
                                       "    border-radius: 0px;\n"
                                       "}")
        self.btnPresepsi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btnPresepsi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btnPresepsi.setObjectName("btnPresepsi")
        self.verticalLayout_113 = QtWidgets.QVBoxLayout(self.btnPresepsi)
        self.verticalLayout_113.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_113.setSpacing(0)
        self.verticalLayout_113.setObjectName("verticalLayout_113")
        self.label_45 = QtWidgets.QLabel(self.btnPresepsi)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_45.setFont(font)
        self.label_45.setStyleSheet("QLabel {\n"
                                    "    color:rgb(215,215,215);\n"
                                    "    padding-left:2.5px;\n"
                                    "    margin-left:5px;\n"
                                    "}")
        self.label_45.setObjectName("label_45")
        self.verticalLayout_113.addWidget(self.label_45)
        self.horizontalLayout_44.addWidget(self.btnPresepsi)
        self.verticalLayout_110.addWidget(
            self.frame_141, 0, QtCore.Qt.AlignLeft)
        self.hrLine_6 = QtWidgets.QFrame(self.frame_139)
        self.hrLine_6.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_6.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine_6.setStyleSheet("*{\n"
                                    "    background-color:rgb(214,215,215);\n"
                                    "\n"
                                    "}")
        self.hrLine_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_6.setObjectName("hrLine_6")
        self.verticalLayout_110.addWidget(self.hrLine_6)
        self.verticalLayout_109.addWidget(self.frame_139)
        self.frame_140 = QtWidgets.QFrame(self.pageTesting)
        self.frame_140.setStyleSheet("")
        self.frame_140.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_140.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_140.setObjectName("frame_140")
        self.verticalLayout_111 = QtWidgets.QVBoxLayout(self.frame_140)
        self.verticalLayout_111.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_111.setSpacing(0)
        self.verticalLayout_111.setObjectName("verticalLayout_111")
        self.stack_akurasi = QtWidgets.QStackedWidget(self.frame_140)
        self.stack_akurasi.setObjectName("stack_akurasi")
        self.page_akurasi = QtWidgets.QWidget()
        self.page_akurasi.setObjectName("page_akurasi")
        self.verticalLayout_114 = QtWidgets.QVBoxLayout(self.page_akurasi)
        self.verticalLayout_114.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_114.setSpacing(0)
        self.verticalLayout_114.setObjectName("verticalLayout_114")
        self.scroll_akurasi_metode = QtWidgets.QScrollArea(self.page_akurasi)
        self.scroll_akurasi_metode.setWidgetResizable(True)
        self.scroll_akurasi_metode.setObjectName("scroll_akurasi_metode")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(
            QtCore.QRect(0, 0, 715, 568))
        self.scrollAreaWidgetContents_5.setObjectName(
            "scrollAreaWidgetContents_5")
        self.verticalLayout_137 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_5)
        self.verticalLayout_137.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_137.setSpacing(0)
        self.verticalLayout_137.setObjectName("verticalLayout_137")
        self.frame_155 = QtWidgets.QFrame(self.scrollAreaWidgetContents_5)
        self.frame_155.setMinimumSize(QtCore.QSize(0, 85))
        self.frame_155.setMaximumSize(QtCore.QSize(16777215, 85))
        self.frame_155.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "    border-bottom-right-radius:0px;\n"
                                     "    border-bottom-left-radius:0px;\n"
                                     "}")
        self.frame_155.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_155.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_155.setObjectName("frame_155")
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout(self.frame_155)
        self.horizontalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_52.setSpacing(0)
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        self.frame_158 = QtWidgets.QFrame(self.frame_155)
        self.frame_158.setMaximumSize(QtCore.QSize(220, 16777215))
        self.frame_158.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_158.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_158.setObjectName("frame_158")
        self.verticalLayout_136 = QtWidgets.QVBoxLayout(self.frame_158)
        self.verticalLayout_136.setContentsMargins(8, 10, 0, 0)
        self.verticalLayout_136.setObjectName("verticalLayout_136")
        self.label_59 = QtWidgets.QLabel(self.frame_158)
        self.label_59.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_59.setFont(font)
        self.label_59.setStyleSheet("QLabel {\n"
                                    "    color:rgb(255,255,255);\n"
                                    "    margin-right:10px;\n"
                                    "}")
        self.label_59.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_59.setObjectName("label_59")
        self.verticalLayout_136.addWidget(self.label_59)
        self.chose_akurasi = QtWidgets.QComboBox(self.frame_158)
        self.chose_akurasi.setMinimumSize(QtCore.QSize(92, 36))
        self.chose_akurasi.setStyleSheet("QComboBox:focus {\n"
                                         "    border-color: #7cabf9;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox {\n"
                                         "    color: #ffffff;\n"
                                         "    background-color: #b6b6b6;\n"
                                         "    selection-color: black;\n"
                                         "    selection-background-color: #5e90fa;\n"
                                         "    border: 1px solid #b6b6b6;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-top-color: #a2a2a0;\n"
                                         "    padding: 2px 6px 2px 10px; \n"
                                         "    margin: 0px 2px 0px 2px;\n"
                                         "    min-width: 70px;\n"
                                         "    border-radius: 3px;\n"
                                         "    min-height: 30px;\n"
                                         "    margin-left:2px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox:on {\n"
                                         "    color: black;\n"
                                         "    background-color: #b6b6b6;\n"
                                         "    border-color: #7cabf9;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::drop-down {\n"
                                         "    subcontrol-origin: margin;\n"
                                         "    subcontrol-position: top right;\n"
                                         "    width: 30px;\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: transparent;\n"
                                         "    border-left-style: solid;\n"
                                         "    border-top-right-radius: 3px;\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "    background-color: qlineargradient(spread:pad, x1:1, y1:0.8, x2:1,        y2:0, stop:0 #5e90fa, stop:1 #7cabf9);\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::down-arrow {\n"
                                         "    image: url(assets/down_arrow_light.png);\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::down-arrow:on,\n"
                                         "QComboBox::down-arrow:hover,\n"
                                         "QComboBox::down-arrow:focus {\n"
                                         "    image: url(assets/down_arrow_lighter.png);\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox QAbstractItemView {\n"
                                         "    color: #ffffff;\n"
                                         "    background-color: #828282;\n"
                                         "    border-radius: 3px;\n"
                                         "    margin: 0px;\n"
                                         "    padding: 0px;\n"
                                         "    border: none;\n"
                                         "    min-height: 30px;\n"
                                         "}\n"
                                         "")
        self.chose_akurasi.setObjectName("chose_akurasi")
        self.verticalLayout_136.addWidget(self.chose_akurasi)
        self.horizontalLayout_52.addWidget(self.frame_158)
        self.frame_154 = QtWidgets.QFrame(self.frame_155)
        self.frame_154.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_154.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_154.setObjectName("frame_154")
        self.verticalLayout_138 = QtWidgets.QVBoxLayout(self.frame_154)
        self.verticalLayout_138.setContentsMargins(15, 0, 0, 0)
        self.verticalLayout_138.setSpacing(0)
        self.verticalLayout_138.setObjectName("verticalLayout_138")
        self.btn_vAkruasi = QtWidgets.QPushButton(self.frame_154)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_vAkruasi.sizePolicy().hasHeightForWidth())
        self.btn_vAkruasi.setSizePolicy(sizePolicy)
        self.btn_vAkruasi.setMinimumSize(QtCore.QSize(120, 38))
        self.btn_vAkruasi.setMaximumSize(QtCore.QSize(120, 38))
        self.btn_vAkruasi.setStyleSheet("QPushButton {\n"
                                        "    background:transparent;\n"
                                        "    border: 1px solid rgb(215,215,215);\n"
                                        "    border-radius:7.5px;\n"
                                        "    color:rgb(215,215,215);\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    color:rgba(20,20,20,235);\n"
                                        "    background-color:rgb(215,215,215);\n"
                                        "    border:none;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed{\n"
                                        "    background-color:rgb(28,28,28);\n"
                                        "    color:rgb(215,215,215);\n"
                                        "    border: 1.5px solid rgb(215,215,215);\n"
                                        "}\n"
                                        "")
        self.btn_vAkruasi.setObjectName("btn_vAkruasi")
        self.verticalLayout_138.addWidget(self.btn_vAkruasi)
        self.horizontalLayout_52.addWidget(
            self.frame_154, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout_137.addWidget(self.frame_155)
        self.frame_156 = QtWidgets.QFrame(self.scrollAreaWidgetContents_5)
        self.frame_156.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "}")
        self.frame_156.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_156.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_156.setObjectName("frame_156")
        self.verticalLayout_141 = QtWidgets.QVBoxLayout(self.frame_156)
        self.verticalLayout_141.setContentsMargins(0, 15, 0, 0)
        self.verticalLayout_141.setObjectName("verticalLayout_141")
        self.hrLine_11 = QtWidgets.QFrame(self.frame_156)
        self.hrLine_11.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_11.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine_11.setStyleSheet("*{\n"
                                     "    background-color:rgba(136,149,169,130);\n"
                                     "}")
        self.hrLine_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_11.setObjectName("hrLine_11")
        self.verticalLayout_141.addWidget(self.hrLine_11)
        self.frame_157 = QtWidgets.QFrame(self.frame_156)
        self.frame_157.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_157.setStyleSheet("")
        self.frame_157.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_157.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_157.setObjectName("frame_157")
        self.verticalLayout_139 = QtWidgets.QVBoxLayout(self.frame_157)
        self.verticalLayout_139.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_139.setSpacing(0)
        self.verticalLayout_139.setObjectName("verticalLayout_139")
        self.frame_159 = QtWidgets.QFrame(self.frame_157)
        self.frame_159.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_159.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_159.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_159.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_159.setObjectName("frame_159")
        self.horizontalLayout_53 = QtWidgets.QHBoxLayout(self.frame_159)
        self.horizontalLayout_53.setContentsMargins(20, 0, 0, 15)
        self.horizontalLayout_53.setSpacing(0)
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.label_60 = QtWidgets.QLabel(self.frame_159)
        self.label_60.setMinimumSize(QtCore.QSize(73, 0))
        self.label_60.setMaximumSize(QtCore.QSize(73, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_60.setFont(font)
        self.label_60.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_60.setObjectName("label_60")
        self.horizontalLayout_53.addWidget(self.label_60)
        self.label_61 = QtWidgets.QLabel(self.frame_159)
        self.label_61.setMinimumSize(QtCore.QSize(178, 0))
        self.label_61.setMaximumSize(QtCore.QSize(178, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_61.setFont(font)
        self.label_61.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_61.setObjectName("label_61")
        self.horizontalLayout_53.addWidget(self.label_61)
        self.label_62 = QtWidgets.QLabel(self.frame_159)
        self.label_62.setMinimumSize(QtCore.QSize(178, 0))
        self.label_62.setMaximumSize(QtCore.QSize(178, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_62.setFont(font)
        self.label_62.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_62.setObjectName("label_62")
        self.horizontalLayout_53.addWidget(self.label_62)
        self.label_63 = QtWidgets.QLabel(self.frame_159)
        self.label_63.setMinimumSize(QtCore.QSize(132, 0))
        self.label_63.setMaximumSize(QtCore.QSize(132, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_63.setFont(font)
        self.label_63.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_63.setObjectName("label_63")
        self.horizontalLayout_53.addWidget(self.label_63)
        self.label_64 = QtWidgets.QLabel(self.frame_159)
        self.label_64.setMinimumSize(QtCore.QSize(100, 0))
        self.label_64.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_64.setFont(font)
        self.label_64.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_64.setObjectName("label_64")
        self.horizontalLayout_53.addWidget(self.label_64)
        self.verticalLayout_139.addWidget(
            self.frame_159, 0, QtCore.Qt.AlignLeft)
        self.hrLine_10 = QtWidgets.QFrame(self.frame_157)
        self.hrLine_10.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_10.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine_10.setStyleSheet("*{\n"
                                     "    background-color:rgba(136,149,169,130);\n"
                                     "}")
        self.hrLine_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_10.setObjectName("hrLine_10")
        self.verticalLayout_139.addWidget(self.hrLine_10)
        self.frame_akurasiV = QtWidgets.QFrame(self.frame_157)
        self.frame_akurasiV.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_akurasiV.setStyleSheet("")
        self.frame_akurasiV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_akurasiV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_akurasiV.setObjectName("frame_akurasiV")
        self.verticalLayout_140 = QtWidgets.QVBoxLayout(self.frame_akurasiV)
        self.verticalLayout_140.setContentsMargins(0, 10, 10, 10)
        self.verticalLayout_140.setSpacing(0)
        self.verticalLayout_140.setObjectName("verticalLayout_140")
        self.verticalLayout_139.addWidget(
            self.frame_akurasiV, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_141.addWidget(self.frame_157)
        self.verticalLayout_137.addWidget(self.frame_156)
        self.scroll_akurasi_metode.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_114.addWidget(self.scroll_akurasi_metode)
        self.stack_akurasi.addWidget(self.page_akurasi)
        self.page_presepsi = QtWidgets.QWidget()
        self.page_presepsi.setStyleSheet("")
        self.page_presepsi.setObjectName("page_presepsi")
        self.verticalLayout_115 = QtWidgets.QVBoxLayout(self.page_presepsi)
        self.verticalLayout_115.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_115.setSpacing(0)
        self.verticalLayout_115.setObjectName("verticalLayout_115")
        self.scroll_akurasi = QtWidgets.QScrollArea(self.page_presepsi)
        self.scroll_akurasi.setWidgetResizable(True)
        self.scroll_akurasi.setObjectName("scroll_akurasi")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(
            QtCore.QRect(0, 0, 715, 568))
        self.scrollAreaWidgetContents_3.setObjectName(
            "scrollAreaWidgetContents_3")
        self.verticalLayout_98 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_3)
        self.verticalLayout_98.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_98.setSpacing(0)
        self.verticalLayout_98.setObjectName("verticalLayout_98")
        self.frame_89 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.frame_89.setStyleSheet("QFrame{\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "    border-top-left-radius:0px;\n"
                                    "    border-top-right-radius:0px;\n"
                                    "}")
        self.frame_89.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_89.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_89.setObjectName("frame_89")
        self.verticalLayout_118 = QtWidgets.QVBoxLayout(self.frame_89)
        self.verticalLayout_118.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_118.setObjectName("verticalLayout_118")
        self.frame_126 = QtWidgets.QFrame(self.frame_89)
        self.frame_126.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_126.setStyleSheet("")
        self.frame_126.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_126.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_126.setObjectName("frame_126")
        self.verticalLayout_104 = QtWidgets.QVBoxLayout(self.frame_126)
        self.verticalLayout_104.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_104.setSpacing(0)
        self.verticalLayout_104.setObjectName("verticalLayout_104")
        self.frame_127 = QtWidgets.QFrame(self.frame_126)
        self.frame_127.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_127.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_127.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_127.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_127.setObjectName("frame_127")
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout(self.frame_127)
        self.horizontalLayout_45.setContentsMargins(20, 0, 0, 10)
        self.horizontalLayout_45.setSpacing(0)
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.label_55 = QtWidgets.QLabel(self.frame_127)
        self.label_55.setMinimumSize(QtCore.QSize(73, 0))
        self.label_55.setMaximumSize(QtCore.QSize(73, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_55.setFont(font)
        self.label_55.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_55.setObjectName("label_55")
        self.horizontalLayout_45.addWidget(
            self.label_55, 0, QtCore.Qt.AlignLeft)
        self.label_56 = QtWidgets.QLabel(self.frame_127)
        self.label_56.setMinimumSize(QtCore.QSize(177, 0))
        self.label_56.setMaximumSize(QtCore.QSize(177, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_56.setFont(font)
        self.label_56.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_56.setObjectName("label_56")
        self.horizontalLayout_45.addWidget(
            self.label_56, 0, QtCore.Qt.AlignLeft)
        self.label_57 = QtWidgets.QLabel(self.frame_127)
        self.label_57.setMinimumSize(QtCore.QSize(213, 0))
        self.label_57.setMaximumSize(QtCore.QSize(213, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_57.setFont(font)
        self.label_57.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_57.setObjectName("label_57")
        self.horizontalLayout_45.addWidget(
            self.label_57, 0, QtCore.Qt.AlignLeft)
        self.label_58 = QtWidgets.QLabel(self.frame_127)
        self.label_58.setMinimumSize(QtCore.QSize(150, 0))
        self.label_58.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_58.setFont(font)
        self.label_58.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(84,91,103);\n"
                                    "}")
        self.label_58.setObjectName("label_58")
        self.horizontalLayout_45.addWidget(
            self.label_58, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_104.addWidget(
            self.frame_127, 0, QtCore.Qt.AlignLeft)
        self.hrLine_9 = QtWidgets.QFrame(self.frame_126)
        self.hrLine_9.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_9.setMaximumSize(QtCore.QSize(16777215, 1))
        self.hrLine_9.setStyleSheet("*{\n"
                                    "    background-color:rgba(136,149,169,130);\n"
                                    "}")
        self.hrLine_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_9.setObjectName("hrLine_9")
        self.verticalLayout_104.addWidget(self.hrLine_9)
        self.frame_presepsiV = QtWidgets.QFrame(self.frame_126)
        self.frame_presepsiV.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_presepsiV.setStyleSheet("")
        self.frame_presepsiV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_presepsiV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_presepsiV.setObjectName("frame_presepsiV")
        self.verticalLayout_116 = QtWidgets.QVBoxLayout(self.frame_presepsiV)
        self.verticalLayout_116.setContentsMargins(0, 10, 10, 10)
        self.verticalLayout_116.setSpacing(0)
        self.verticalLayout_116.setObjectName("verticalLayout_116")
        self.verticalLayout_104.addWidget(
            self.frame_presepsiV, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_118.addWidget(self.frame_126)
        self.verticalLayout_98.addWidget(self.frame_89)
        self.scroll_akurasi.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_115.addWidget(self.scroll_akurasi)
        self.stack_akurasi.addWidget(self.page_presepsi)
        self.page_presepsi_v = QtWidgets.QWidget()
        self.page_presepsi_v.setObjectName("page_presepsi_v")
        self.verticalLayout_119 = QtWidgets.QVBoxLayout(self.page_presepsi_v)
        self.verticalLayout_119.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_119.setSpacing(0)
        self.verticalLayout_119.setObjectName("verticalLayout_119")
        self.scroll_presepsi_v = QtWidgets.QScrollArea(self.page_presepsi_v)
        self.scroll_presepsi_v.setWidgetResizable(True)
        self.scroll_presepsi_v.setObjectName("scroll_presepsi_v")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(
            QtCore.QRect(0, 0, 715, 899))
        self.scrollAreaWidgetContents_4.setObjectName(
            "scrollAreaWidgetContents_4")
        self.verticalLayout_124 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_4)
        self.verticalLayout_124.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_124.setSpacing(0)
        self.verticalLayout_124.setObjectName("verticalLayout_124")
        self.frame_128 = QtWidgets.QFrame(self.scrollAreaWidgetContents_4)
        self.frame_128.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "}")
        self.frame_128.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_128.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_128.setObjectName("frame_128")
        self.verticalLayout_120 = QtWidgets.QVBoxLayout(self.frame_128)
        self.verticalLayout_120.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_120.setSpacing(0)
        self.verticalLayout_120.setObjectName("verticalLayout_120")
        self.frame_129 = QtWidgets.QFrame(self.frame_128)
        self.frame_129.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_129.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_129.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_129.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_129.setObjectName("frame_129")
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout(self.frame_129)
        self.horizontalLayout_46.setContentsMargins(20, 0, 5, 0)
        self.horizontalLayout_46.setSpacing(0)
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.frame_133 = QtWidgets.QFrame(self.frame_129)
        self.frame_133.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_133.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_133.setObjectName("frame_133")
        self.verticalLayout_121 = QtWidgets.QVBoxLayout(self.frame_133)
        self.verticalLayout_121.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_121.setSpacing(0)
        self.verticalLayout_121.setObjectName("verticalLayout_121")
        self.presepsi_id = QtWidgets.QLabel(self.frame_133)
        self.presepsi_id.setMinimumSize(QtCore.QSize(0, 25))
        self.presepsi_id.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.presepsi_id.setFont(font)
        self.presepsi_id.setStyleSheet("QLabel {\n"
                                       "    color:rgb(215,215,215);\n"
                                       "}")
        self.presepsi_id.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.presepsi_id.setObjectName("presepsi_id")
        self.verticalLayout_121.addWidget(
            self.presepsi_id, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_46.addWidget(
            self.frame_133, 0, QtCore.Qt.AlignTop)
        self.presepsi_quit = QtWidgets.QFrame(self.frame_129)
        self.presepsi_quit.setMinimumSize(QtCore.QSize(38, 33))
        self.presepsi_quit.setMaximumSize(QtCore.QSize(38, 33))
        self.presepsi_quit.setStyleSheet("QFrame {\n"
                                         "    background-color:transparent;\n"
                                         "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                         "    border-width:6px 9px 6px 9px\n"
                                         "}\n"
                                         "\n"
                                         "QFrame:hover{\n"
                                         "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                         "}")
        self.presepsi_quit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.presepsi_quit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.presepsi_quit.setObjectName("presepsi_quit")
        self.horizontalLayout_46.addWidget(self.presepsi_quit)
        self.verticalLayout_120.addWidget(self.frame_129)
        self.frame_134 = QtWidgets.QFrame(self.frame_128)
        self.frame_134.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_134.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_134.setObjectName("frame_134")
        self.verticalLayout_122 = QtWidgets.QVBoxLayout(self.frame_134)
        self.verticalLayout_122.setContentsMargins(20, 10, 20, 10)
        self.verticalLayout_122.setObjectName("verticalLayout_122")
        self.frame_142 = QtWidgets.QFrame(self.frame_134)
        self.frame_142.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_142.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_142.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_142.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_142.setObjectName("frame_142")
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout(self.frame_142)
        self.horizontalLayout_47.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.frame_plot_presepsi_v = QtWidgets.QFrame(self.frame_142)
        self.frame_plot_presepsi_v.setMinimumSize(QtCore.QSize(0, 535))
        self.frame_plot_presepsi_v.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.frame_plot_presepsi_v.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot_presepsi_v.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot_presepsi_v.setObjectName("frame_plot_presepsi_v")
        self.verticalLayout_123 = QtWidgets.QVBoxLayout(
            self.frame_plot_presepsi_v)
        self.verticalLayout_123.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_123.setSpacing(0)
        self.verticalLayout_123.setObjectName("verticalLayout_123")
        self.plot_presepsi_v = QtWidgets.QVBoxLayout()
        self.plot_presepsi_v.setSpacing(0)
        self.plot_presepsi_v.setObjectName("plot_presepsi_v")
        self.verticalLayout_123.addLayout(self.plot_presepsi_v)
        self.horizontalLayout_47.addWidget(self.frame_plot_presepsi_v)
        self.verticalLayout_122.addWidget(self.frame_142)
        self.verticalLayout_120.addWidget(self.frame_134)
        self.frame_147 = QtWidgets.QFrame(self.frame_128)
        self.frame_147.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_147.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_147.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_147.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_147.setObjectName("frame_147")
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout(self.frame_147)
        self.horizontalLayout_49.setContentsMargins(20, 0, 20, 20)
        self.horizontalLayout_49.setSpacing(10)
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.frame_148 = QtWidgets.QFrame(self.frame_147)
        self.frame_148.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_148.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_148.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_148.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_148.setObjectName("frame_148")
        self.verticalLayout_128 = QtWidgets.QVBoxLayout(self.frame_148)
        self.verticalLayout_128.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_128.setSpacing(5)
        self.verticalLayout_128.setObjectName("verticalLayout_128")
        self.presepsi_id_3 = QtWidgets.QLabel(self.frame_148)
        self.presepsi_id_3.setMinimumSize(QtCore.QSize(0, 25))
        self.presepsi_id_3.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.presepsi_id_3.setFont(font)
        self.presepsi_id_3.setStyleSheet("QLabel {\n"
                                         "    color:rgb(215,215,215);\n"
                                         "}")
        self.presepsi_id_3.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.presepsi_id_3.setObjectName("presepsi_id_3")
        self.verticalLayout_128.addWidget(self.presepsi_id_3)
        self.frame_149 = QtWidgets.QFrame(self.frame_148)
        self.frame_149.setStyleSheet("QFrame {\n"
                                     "    border-radius:0px;\n"
                                     "    background-color:rgb(255,255,255);\n"
                                     "}")
        self.frame_149.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_149.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_149.setObjectName("frame_149")
        self.verticalLayout_129 = QtWidgets.QVBoxLayout(self.frame_149)
        self.verticalLayout_129.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_129.setSpacing(0)
        self.verticalLayout_129.setObjectName("verticalLayout_129")
        self.table_prespsi_astar = QtWidgets.QTableWidget(self.frame_149)
        self.table_prespsi_astar.setStyleSheet("*{\n"
                                               "    selection-background-color: transparent;\n"
                                               "    selection-color: rgb(0,0,0);\n"
                                               "}")
        self.table_prespsi_astar.setObjectName("table_prespsi_astar")
        self.table_prespsi_astar.setColumnCount(5)
        self.table_prespsi_astar.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_astar.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_astar.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_astar.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_astar.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_astar.setHorizontalHeaderItem(4, item)
        self.verticalLayout_129.addWidget(self.table_prespsi_astar)
        self.verticalLayout_128.addWidget(self.frame_149)
        self.horizontalLayout_49.addWidget(self.frame_148)
        self.verticalLayout_120.addWidget(self.frame_147)
        self.frame_143 = QtWidgets.QFrame(self.frame_128)
        self.frame_143.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_143.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_143.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_143.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_143.setObjectName("frame_143")
        self.verticalLayout_131 = QtWidgets.QVBoxLayout(self.frame_143)
        self.verticalLayout_131.setContentsMargins(20, 0, 20, 0)
        self.verticalLayout_131.setSpacing(10)
        self.verticalLayout_131.setObjectName("verticalLayout_131")
        self.frame_144 = QtWidgets.QFrame(self.frame_143)
        self.frame_144.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_144.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_144.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_144.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_144.setObjectName("frame_144")
        self.verticalLayout_125 = QtWidgets.QVBoxLayout(self.frame_144)
        self.verticalLayout_125.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_125.setSpacing(5)
        self.verticalLayout_125.setObjectName("verticalLayout_125")
        self.presepsi_id_2 = QtWidgets.QLabel(self.frame_144)
        self.presepsi_id_2.setMinimumSize(QtCore.QSize(0, 25))
        self.presepsi_id_2.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.presepsi_id_2.setFont(font)
        self.presepsi_id_2.setStyleSheet("QLabel {\n"
                                         "    color:rgb(215,215,215);\n"
                                         "}")
        self.presepsi_id_2.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.presepsi_id_2.setObjectName("presepsi_id_2")
        self.verticalLayout_125.addWidget(self.presepsi_id_2)
        self.frame_146 = QtWidgets.QFrame(self.frame_144)
        self.frame_146.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_146.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_146.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_146.setObjectName("frame_146")
        self.horizontalLayout_50 = QtWidgets.QHBoxLayout(self.frame_146)
        self.horizontalLayout_50.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_50.setSpacing(10)
        self.horizontalLayout_50.setObjectName("horizontalLayout_50")
        self.groupPortSocket_2 = QtWidgets.QGroupBox(self.frame_146)
        self.groupPortSocket_2.setMinimumSize(QtCore.QSize(270, 55))
        self.groupPortSocket_2.setMaximumSize(QtCore.QSize(270, 55))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.groupPortSocket_2.setFont(font)
        self.groupPortSocket_2.setStyleSheet("*{\n"
                                             "    background:transparent;\n"
                                             "}\n"
                                             "\n"
                                             "QGroupBox{\n"
                                             "    border: 1px solid rgb(255,255,255);\n"
                                             "    border-radius:10px;\n"
                                             "    margin-top:0.5em;\n"
                                             "}\n"
                                             "\n"
                                             "QGroupBox::title{\n"
                                             "    subcontrol-origin:margin;\n"
                                             "    left:10px;\n"
                                             "    padding-top:-6px;\n"
                                             "    color:rgb(255,255,255);\n"
                                             "}")
        self.groupPortSocket_2.setObjectName("groupPortSocket_2")
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout(
            self.groupPortSocket_2)
        self.horizontalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_48.setSpacing(0)
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.frame_151 = QtWidgets.QFrame(self.groupPortSocket_2)
        self.frame_151.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_151.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_151.setObjectName("frame_151")
        self.verticalLayout_132 = QtWidgets.QVBoxLayout(self.frame_151)
        self.verticalLayout_132.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_132.setSpacing(0)
        self.verticalLayout_132.setObjectName("verticalLayout_132")
        self.txt_efisien_presepsi = QtWidgets.QLineEdit(self.frame_151)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_efisien_presepsi.sizePolicy().hasHeightForWidth())
        self.txt_efisien_presepsi.setSizePolicy(sizePolicy)
        self.txt_efisien_presepsi.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_efisien_presepsi.setStyleSheet("QLineEdit {\n"
                                                "    border:none;\n"
                                                "    margin-left:10px;\n"
                                                "    color:rgb(215,215,215);\n"
                                                "}")
        self.txt_efisien_presepsi.setObjectName("txt_efisien_presepsi")
        self.verticalLayout_132.addWidget(self.txt_efisien_presepsi)
        self.horizontalLayout_48.addWidget(self.frame_151)
        self.horizontalLayout_50.addWidget(self.groupPortSocket_2)
        self.btn_submit_prespsi = QtWidgets.QPushButton(self.frame_146)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_submit_prespsi.sizePolicy().hasHeightForWidth())
        self.btn_submit_prespsi.setSizePolicy(sizePolicy)
        self.btn_submit_prespsi.setMinimumSize(QtCore.QSize(120, 54))
        self.btn_submit_prespsi.setMaximumSize(QtCore.QSize(120, 54))
        self.btn_submit_prespsi.setStyleSheet("QPushButton {\n"
                                              "    background:transparent;\n"
                                              "    border: 1px solid rgb(215,215,215);\n"
                                              "    border-radius:7.5px;\n"
                                              "    color:rgb(215,215,215);\n"
                                              "    margin-top:5px;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:hover{\n"
                                              "    color:rgba(20,20,20,235);\n"
                                              "    background-color:rgb(215,215,215);\n"
                                              "    border:none;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:pressed{\n"
                                              "    background-color:rgb(28,28,28);\n"
                                              "    color:rgb(215,215,215);\n"
                                              "    border: 1.5px solid rgb(215,215,215);\n"
                                              "}\n"
                                              "")
        self.btn_submit_prespsi.setObjectName("btn_submit_prespsi")
        self.horizontalLayout_50.addWidget(self.btn_submit_prespsi)
        self.verticalLayout_125.addWidget(
            self.frame_146, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.verticalLayout_131.addWidget(self.frame_144)
        self.frame_150 = QtWidgets.QFrame(self.frame_143)
        self.frame_150.setStyleSheet("QFrame {\n"
                                     "    border-radius:0px;\n"
                                     "    background-color:rgb(255,255,255);\n"
                                     "}")
        self.frame_150.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_150.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_150.setObjectName("frame_150")
        self.verticalLayout_130 = QtWidgets.QVBoxLayout(self.frame_150)
        self.verticalLayout_130.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_130.setSpacing(0)
        self.verticalLayout_130.setObjectName("verticalLayout_130")
        self.table_prespsi_improv = QtWidgets.QTableWidget(self.frame_150)
        self.table_prespsi_improv.setStyleSheet("*{\n"
                                                "    selection-background-color: transparent;\n"
                                                "    selection-color: rgb(0,0,0);\n"
                                                "}")
        self.table_prespsi_improv.setObjectName("table_prespsi_improv")
        self.table_prespsi_improv.setColumnCount(4)
        self.table_prespsi_improv.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_improv.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_improv.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_improv.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_prespsi_improv.setHorizontalHeaderItem(3, item)
        self.verticalLayout_130.addWidget(self.table_prespsi_improv)
        self.verticalLayout_131.addWidget(self.frame_150)
        self.verticalLayout_120.addWidget(self.frame_143)
        self.verticalLayout_124.addWidget(self.frame_128)
        self.scroll_presepsi_v.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout_119.addWidget(self.scroll_presepsi_v)
        self.stack_akurasi.addWidget(self.page_presepsi_v)
        self.page_presepsi_r = QtWidgets.QWidget()
        self.page_presepsi_r.setObjectName("page_presepsi_r")
        self.verticalLayout_127 = QtWidgets.QVBoxLayout(self.page_presepsi_r)
        self.verticalLayout_127.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_127.setSpacing(0)
        self.verticalLayout_127.setObjectName("verticalLayout_127")
        self.frame_145 = QtWidgets.QFrame(self.page_presepsi_r)
        self.frame_145.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "}")
        self.frame_145.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_145.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_145.setObjectName("frame_145")
        self.verticalLayout_135 = QtWidgets.QVBoxLayout(self.frame_145)
        self.verticalLayout_135.setContentsMargins(20, 0, 0, 20)
        self.verticalLayout_135.setSpacing(10)
        self.verticalLayout_135.setObjectName("verticalLayout_135")
        self.frame_152 = QtWidgets.QFrame(self.frame_145)
        self.frame_152.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_152.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_152.setStyleSheet("")
        self.frame_152.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_152.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_152.setObjectName("frame_152")
        self.horizontalLayout_51 = QtWidgets.QHBoxLayout(self.frame_152)
        self.horizontalLayout_51.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout_51.setSpacing(0)
        self.horizontalLayout_51.setObjectName("horizontalLayout_51")
        self.frame_153 = QtWidgets.QFrame(self.frame_152)
        self.frame_153.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_153.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_153.setObjectName("frame_153")
        self.verticalLayout_133 = QtWidgets.QVBoxLayout(self.frame_153)
        self.verticalLayout_133.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_133.setSpacing(0)
        self.verticalLayout_133.setObjectName("verticalLayout_133")
        self.history_id_2 = QtWidgets.QLabel(self.frame_153)
        self.history_id_2.setMinimumSize(QtCore.QSize(0, 30))
        self.history_id_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.history_id_2.setFont(font)
        self.history_id_2.setStyleSheet("QLabel {\n"
                                        "    color:rgb(215,215,215);\n"
                                        "}")
        self.history_id_2.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.history_id_2.setObjectName("history_id_2")
        self.verticalLayout_133.addWidget(
            self.history_id_2, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_51.addWidget(
            self.frame_153, 0, QtCore.Qt.AlignTop)
        self.quit_akurasi_presepsi = QtWidgets.QFrame(self.frame_152)
        self.quit_akurasi_presepsi.setMinimumSize(QtCore.QSize(38, 33))
        self.quit_akurasi_presepsi.setMaximumSize(QtCore.QSize(38, 33))
        self.quit_akurasi_presepsi.setStyleSheet("QFrame {\n"
                                                 "    background-color:transparent;\n"
                                                 "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                                 "    border-width:6px 9px 6px 9px\n"
                                                 "}\n"
                                                 "\n"
                                                 "QFrame:hover{\n"
                                                 "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                                 "}")
        self.quit_akurasi_presepsi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quit_akurasi_presepsi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.quit_akurasi_presepsi.setObjectName("quit_akurasi_presepsi")
        self.horizontalLayout_51.addWidget(self.quit_akurasi_presepsi)
        self.verticalLayout_135.addWidget(self.frame_152)
        self.frame_plot_presepsi = QtWidgets.QFrame(self.frame_145)
        self.frame_plot_presepsi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot_presepsi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot_presepsi.setObjectName("frame_plot_presepsi")
        self.verticalLayout_134 = QtWidgets.QVBoxLayout(
            self.frame_plot_presepsi)
        self.verticalLayout_134.setContentsMargins(0, 0, 20, 0)
        self.verticalLayout_134.setSpacing(0)
        self.verticalLayout_134.setObjectName("verticalLayout_134")
        self.plot_akurasi_presepsi = QtWidgets.QVBoxLayout()
        self.plot_akurasi_presepsi.setSpacing(0)
        self.plot_akurasi_presepsi.setObjectName("plot_akurasi_presepsi")
        self.verticalLayout_134.addLayout(self.plot_akurasi_presepsi)
        self.verticalLayout_135.addWidget(self.frame_plot_presepsi)
        self.verticalLayout_127.addWidget(self.frame_145)
        self.stack_akurasi.addWidget(self.page_presepsi_r)
        self.page_akurasi_r = QtWidgets.QWidget()
        self.page_akurasi_r.setObjectName("page_akurasi_r")
        self.verticalLayout_100 = QtWidgets.QVBoxLayout(self.page_akurasi_r)
        self.verticalLayout_100.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_100.setSpacing(0)
        self.verticalLayout_100.setObjectName("verticalLayout_100")
        self.frame_160 = QtWidgets.QFrame(self.page_akurasi_r)
        self.frame_160.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "}")
        self.frame_160.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_160.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_160.setObjectName("frame_160")
        self.verticalLayout_142 = QtWidgets.QVBoxLayout(self.frame_160)
        self.verticalLayout_142.setContentsMargins(20, 0, 0, 20)
        self.verticalLayout_142.setSpacing(10)
        self.verticalLayout_142.setObjectName("verticalLayout_142")
        self.frame_161 = QtWidgets.QFrame(self.frame_160)
        self.frame_161.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_161.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_161.setStyleSheet("")
        self.frame_161.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_161.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_161.setObjectName("frame_161")
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout(self.frame_161)
        self.horizontalLayout_54.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        self.frame_162 = QtWidgets.QFrame(self.frame_161)
        self.frame_162.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_162.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_162.setObjectName("frame_162")
        self.verticalLayout_143 = QtWidgets.QVBoxLayout(self.frame_162)
        self.verticalLayout_143.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_143.setSpacing(0)
        self.verticalLayout_143.setObjectName("verticalLayout_143")
        self.history_id_3 = QtWidgets.QLabel(self.frame_162)
        self.history_id_3.setMinimumSize(QtCore.QSize(0, 30))
        self.history_id_3.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.history_id_3.setFont(font)
        self.history_id_3.setStyleSheet("QLabel {\n"
                                        "    color:rgb(215,215,215);\n"
                                        "}")
        self.history_id_3.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.history_id_3.setObjectName("history_id_3")
        self.verticalLayout_143.addWidget(
            self.history_id_3, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_54.addWidget(
            self.frame_162, 0, QtCore.Qt.AlignTop)
        self.quit_akurasi_v = QtWidgets.QFrame(self.frame_161)
        self.quit_akurasi_v.setMinimumSize(QtCore.QSize(38, 33))
        self.quit_akurasi_v.setMaximumSize(QtCore.QSize(38, 33))
        self.quit_akurasi_v.setStyleSheet("QFrame {\n"
                                          "    background-color:transparent;\n"
                                          "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                          "    border-width:6px 9px 6px 9px\n"
                                          "}\n"
                                          "\n"
                                          "QFrame:hover{\n"
                                          "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                          "}")
        self.quit_akurasi_v.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quit_akurasi_v.setFrameShadow(QtWidgets.QFrame.Raised)
        self.quit_akurasi_v.setObjectName("quit_akurasi_v")
        self.horizontalLayout_54.addWidget(self.quit_akurasi_v)
        self.verticalLayout_142.addWidget(self.frame_161)
        self.frame_plot_akurasi = QtWidgets.QFrame(self.frame_160)
        self.frame_plot_akurasi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot_akurasi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot_akurasi.setObjectName("frame_plot_akurasi")
        self.verticalLayout_101 = QtWidgets.QVBoxLayout(
            self.frame_plot_akurasi)
        self.verticalLayout_101.setContentsMargins(0, 0, 20, 0)
        self.verticalLayout_101.setSpacing(0)
        self.verticalLayout_101.setObjectName("verticalLayout_101")
        self.frame_124 = QtWidgets.QFrame(self.frame_plot_akurasi)
        self.frame_124.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_124.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_124.setObjectName("frame_124")
        self.verticalLayout_102 = QtWidgets.QVBoxLayout(self.frame_124)
        self.verticalLayout_102.setContentsMargins(0, 0, 0, 20)
        self.verticalLayout_102.setSpacing(0)
        self.verticalLayout_102.setObjectName("verticalLayout_102")
        self.plot_akurasi = QtWidgets.QVBoxLayout()
        self.plot_akurasi.setContentsMargins(-1, -1, 0, -1)
        self.plot_akurasi.setSpacing(0)
        self.plot_akurasi.setObjectName("plot_akurasi")
        self.verticalLayout_102.addLayout(self.plot_akurasi)
        self.verticalLayout_101.addWidget(self.frame_124)
        self.frame_90 = QtWidgets.QFrame(self.frame_plot_akurasi)
        self.frame_90.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_90.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_90.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_90.setObjectName("frame_90")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout(self.frame_90)
        self.horizontalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_39.setSpacing(0)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.history_id_4 = QtWidgets.QLabel(self.frame_90)
        self.history_id_4.setMinimumSize(QtCore.QSize(280, 30))
        self.history_id_4.setMaximumSize(QtCore.QSize(280, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.history_id_4.setFont(font)
        self.history_id_4.setStyleSheet("QLabel {\n"
                                        "    color:rgb(215,215,215);\n"
                                        "    margin-top:2px;\n"
                                        "}")
        self.history_id_4.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.history_id_4.setObjectName("history_id_4")
        self.horizontalLayout_39.addWidget(self.history_id_4)
        self.status_jalur = QtWidgets.QComboBox(self.frame_90)
        self.status_jalur.setMinimumSize(QtCore.QSize(92, 36))
        self.status_jalur.setMaximumSize(QtCore.QSize(200, 16777215))
        self.status_jalur.setStyleSheet("QComboBox:focus {\n"
                                        "    border-color: #7cabf9;\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox {\n"
                                        "    color: #ffffff;\n"
                                        "    background-color: #b6b6b6;\n"
                                        "    selection-color: black;\n"
                                        "    selection-background-color: #5e90fa;\n"
                                        "    border: 1px solid #b6b6b6;\n"
                                        "    border-radius: 3px;\n"
                                        "    border-top-color: #a2a2a0;\n"
                                        "    padding: 2px 6px 2px 10px; \n"
                                        "    margin: 0px 2px 0px 2px;\n"
                                        "    min-width: 70px;\n"
                                        "    border-radius: 3px;\n"
                                        "    min-height: 30px;\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox:on {\n"
                                        "    color: black;\n"
                                        "    background-color: #b6b6b6;\n"
                                        "    border-color: #7cabf9;\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox::drop-down {\n"
                                        "    subcontrol-origin: margin;\n"
                                        "    subcontrol-position: top right;\n"
                                        "    width: 30px;\n"
                                        "    border-left-width: 1px;\n"
                                        "    border-left-color: transparent;\n"
                                        "    border-left-style: solid;\n"
                                        "    border-top-right-radius: 3px;\n"
                                        "    border-bottom-right-radius: 3px;\n"
                                        "    background-color: qlineargradient(spread:pad, x1:1, y1:0.8, x2:1,        y2:0, stop:0 #5e90fa, stop:1 #7cabf9);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox::down-arrow {\n"
                                        "    image: url(assets/down_arrow_light.png);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox::down-arrow:on,\n"
                                        "QComboBox::down-arrow:hover,\n"
                                        "QComboBox::down-arrow:focus {\n"
                                        "    image: url(assets/down_arrow_lighter.png);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox QAbstractItemView {\n"
                                        "    color: #ffffff;\n"
                                        "    background-color: #828282;\n"
                                        "    border-radius: 3px;\n"
                                        "    margin: 0px;\n"
                                        "    padding: 0px;\n"
                                        "    border: none;\n"
                                        "    min-height: 30px;\n"
                                        "}\n"
                                        "")
        self.status_jalur.setObjectName("status_jalur")
        self.horizontalLayout_39.addWidget(self.status_jalur)
        self.verticalLayout_101.addWidget(
            self.frame_90, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_142.addWidget(self.frame_plot_akurasi)
        self.verticalLayout_100.addWidget(self.frame_160)
        self.stack_akurasi.addWidget(self.page_akurasi_r)
        self.page_akurasi_chart = QtWidgets.QWidget()
        self.page_akurasi_chart.setObjectName("page_akurasi_chart")
        self.verticalLayout_103 = QtWidgets.QVBoxLayout(
            self.page_akurasi_chart)
        self.verticalLayout_103.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_103.setSpacing(0)
        self.verticalLayout_103.setObjectName("verticalLayout_103")
        self.frame_163 = QtWidgets.QFrame(self.page_akurasi_chart)
        self.frame_163.setStyleSheet("QFrame{\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "}")
        self.frame_163.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_163.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_163.setObjectName("frame_163")
        self.verticalLayout_144 = QtWidgets.QVBoxLayout(self.frame_163)
        self.verticalLayout_144.setContentsMargins(20, 0, 0, 20)
        self.verticalLayout_144.setSpacing(10)
        self.verticalLayout_144.setObjectName("verticalLayout_144")
        self.frame_164 = QtWidgets.QFrame(self.frame_163)
        self.frame_164.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_164.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_164.setStyleSheet("")
        self.frame_164.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_164.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_164.setObjectName("frame_164")
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout(self.frame_164)
        self.horizontalLayout_55.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.frame_165 = QtWidgets.QFrame(self.frame_164)
        self.frame_165.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_165.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_165.setObjectName("frame_165")
        self.verticalLayout_145 = QtWidgets.QVBoxLayout(self.frame_165)
        self.verticalLayout_145.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_145.setSpacing(0)
        self.verticalLayout_145.setObjectName("verticalLayout_145")
        self.history_id_5 = QtWidgets.QLabel(self.frame_165)
        self.history_id_5.setMinimumSize(QtCore.QSize(0, 30))
        self.history_id_5.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.history_id_5.setFont(font)
        self.history_id_5.setStyleSheet("QLabel {\n"
                                        "    color:rgb(215,215,215);\n"
                                        "}")
        self.history_id_5.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.history_id_5.setObjectName("history_id_5")
        self.verticalLayout_145.addWidget(
            self.history_id_5, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_55.addWidget(
            self.frame_165, 0, QtCore.Qt.AlignTop)
        self.quit_akurasi_chart = QtWidgets.QFrame(self.frame_164)
        self.quit_akurasi_chart.setMinimumSize(QtCore.QSize(38, 33))
        self.quit_akurasi_chart.setMaximumSize(QtCore.QSize(38, 33))
        self.quit_akurasi_chart.setStyleSheet("QFrame {\n"
                                              "    background-color:transparent;\n"
                                              "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                              "    border-width:6px 9px 6px 9px\n"
                                              "}\n"
                                              "\n"
                                              "QFrame:hover{\n"
                                              "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                              "}")
        self.quit_akurasi_chart.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quit_akurasi_chart.setFrameShadow(QtWidgets.QFrame.Raised)
        self.quit_akurasi_chart.setObjectName("quit_akurasi_chart")
        self.horizontalLayout_55.addWidget(self.quit_akurasi_chart)
        self.verticalLayout_144.addWidget(self.frame_164)
        self.frame_akurasi_chart = QtWidgets.QFrame(self.frame_163)
        self.frame_akurasi_chart.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_akurasi_chart.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_akurasi_chart.setObjectName("frame_akurasi_chart")
        self.verticalLayout_146 = QtWidgets.QVBoxLayout(
            self.frame_akurasi_chart)
        self.verticalLayout_146.setContentsMargins(0, 0, 20, 0)
        self.verticalLayout_146.setSpacing(0)
        self.verticalLayout_146.setObjectName("verticalLayout_146")
        self.plot_akurasi_chart = QtWidgets.QVBoxLayout()
        self.plot_akurasi_chart.setSpacing(0)
        self.plot_akurasi_chart.setObjectName("plot_akurasi_chart")
        self.verticalLayout_146.addLayout(self.plot_akurasi_chart)
        self.verticalLayout_144.addWidget(self.frame_akurasi_chart)
        self.verticalLayout_103.addWidget(self.frame_163)
        self.stack_akurasi.addWidget(self.page_akurasi_chart)
        self.verticalLayout_111.addWidget(self.stack_akurasi)
        self.verticalLayout_109.addWidget(self.frame_140)
        self.stackedWidget.addWidget(self.pageTesting)
        self.verticalLayout_9.addWidget(self.stackedWidget)
        self.verticalLayout_8.addWidget(self.frame_8)
        self.horizontalLayout.addWidget(self.frameCore)
        self.frameStatus = QtWidgets.QFrame(self.frameContent)
        self.frameStatus.setMinimumSize(QtCore.QSize(240, 0))
        self.frameStatus.setMaximumSize(QtCore.QSize(240, 16777215))
        self.frameStatus.setStyleSheet("QFrame{\n"
                                       "    background-color:transparent;\n"
                                       "}")
        self.frameStatus.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameStatus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameStatus.setObjectName("frameStatus")
        self.verticalLayout_47 = QtWidgets.QVBoxLayout(self.frameStatus)
        self.verticalLayout_47.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_47.setSpacing(0)
        self.verticalLayout_47.setObjectName("verticalLayout_47")
        self.frame_81 = QtWidgets.QFrame(self.frameStatus)
        self.frame_81.setStyleSheet("Line {\n"
                                    "    background-color:rgb(255,255,255);\n"
                                    "}")
        self.frame_81.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_81.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_81.setObjectName("frame_81")
        self.verticalLayout_106 = QtWidgets.QVBoxLayout(self.frame_81)
        self.verticalLayout_106.setContentsMargins(0, 0, 0, 20)
        self.verticalLayout_106.setSpacing(0)
        self.verticalLayout_106.setObjectName("verticalLayout_106")
        self.frame_135 = QtWidgets.QFrame(self.frame_81)
        self.frame_135.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_135.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_135.setObjectName("frame_135")
        self.verticalLayout_107 = QtWidgets.QVBoxLayout(self.frame_135)
        self.verticalLayout_107.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_107.setSpacing(0)
        self.verticalLayout_107.setObjectName("verticalLayout_107")
        self.frame_136 = QtWidgets.QFrame(self.frame_135)
        self.frame_136.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_136.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_136.setStyleSheet("QFrame {\n"
                                     "    background-color:rgba(59,60,77,255);\n"
                                     "    border-radius: 0px;\n"
                                     "}")
        self.frame_136.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_136.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_136.setObjectName("frame_136")
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout(self.frame_136)
        self.horizontalLayout_43.setContentsMargins(15, 0, 5, 0)
        self.horizontalLayout_43.setSpacing(0)
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.label_42 = QtWidgets.QLabel(self.frame_136)
        self.label_42.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_42.setFont(font)
        self.label_42.setStyleSheet("QLabel {\n"
                                    "    color:rgb(255,255,255);\n"
                                    "    margin-right:10px;\n"
                                    "}")
        self.label_42.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_43.addWidget(self.label_42)
        self.frame_137 = QtWidgets.QFrame(self.frame_136)
        self.frame_137.setMaximumSize(QtCore.QSize(27, 16777215))
        self.frame_137.setStyleSheet("QFrame{\n"
                                     "    margin-top:7.25px;\n"
                                     "    border-image: url(\"./assets/point.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.frame_137.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_137.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_137.setObjectName("frame_137")
        self.horizontalLayout_43.addWidget(self.frame_137)
        self.verticalLayout_107.addWidget(self.frame_136)
        self.frame_138 = QtWidgets.QFrame(self.frame_135)
        self.frame_138.setStyleSheet("QFrame {\n"
                                     "    background-color:rgb(27,27,27);\n"
                                     "    border-top-left-radius:0px;\n"
                                     "    border-top-right-radius:0px;\n"
                                     "    border-bottom-left-radius:0px;\n"
                                     "}")
        self.frame_138.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_138.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_138.setObjectName("frame_138")
        self.verticalLayout_108 = QtWidgets.QVBoxLayout(self.frame_138)
        self.verticalLayout_108.setContentsMargins(15, 10, 15, 20)
        self.verticalLayout_108.setSpacing(10)
        self.verticalLayout_108.setObjectName("verticalLayout_108")
        self.label_43 = QtWidgets.QLabel(self.frame_138)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_43.setFont(font)
        self.label_43.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_43.setObjectName("label_43")
        self.verticalLayout_108.addWidget(self.label_43)
        self.f_biaya = QtWidgets.QComboBox(self.frame_138)
        self.f_biaya.setMinimumSize(QtCore.QSize(92, 36))
        self.f_biaya.setStyleSheet("QComboBox:focus {\n"
                                   "    border-color: #7cabf9;\n"
                                   "}\n"
                                   "\n"
                                   "QComboBox {\n"
                                   "    color: #ffffff;\n"
                                   "    background-color: #b6b6b6;\n"
                                   "    selection-color: black;\n"
                                   "    selection-background-color: #5e90fa;\n"
                                   "    border: 1px solid #b6b6b6;\n"
                                   "    border-radius: 3px;\n"
                                   "    border-top-color: #a2a2a0;\n"
                                   "    padding: 2px 6px 2px 10px; \n"
                                   "    margin: 0px 2px 0px 2px;\n"
                                   "    min-width: 70px;\n"
                                   "    border-radius: 3px;\n"
                                   "    min-height: 30px;\n"
                                   "}\n"
                                   "\n"
                                   "QComboBox:on {\n"
                                   "    color: black;\n"
                                   "    background-color: #b6b6b6;\n"
                                   "    border-color: #7cabf9;\n"
                                   "}\n"
                                   "\n"
                                   "QComboBox::drop-down {\n"
                                   "    subcontrol-origin: margin;\n"
                                   "    subcontrol-position: top right;\n"
                                   "    width: 30px;\n"
                                   "    border-left-width: 1px;\n"
                                   "    border-left-color: transparent;\n"
                                   "    border-left-style: solid;\n"
                                   "    border-top-right-radius: 3px;\n"
                                   "    border-bottom-right-radius: 3px;\n"
                                   "    background-color: qlineargradient(spread:pad, x1:1, y1:0.8, x2:1,        y2:0, stop:0 #5e90fa, stop:1 #7cabf9);\n"
                                   "}\n"
                                   "\n"
                                   "QComboBox::down-arrow {\n"
                                   "    image: url(assets/down_arrow_light.png);\n"
                                   "}\n"
                                   "\n"
                                   "QComboBox::down-arrow:on,\n"
                                   "QComboBox::down-arrow:hover,\n"
                                   "QComboBox::down-arrow:focus {\n"
                                   "    image: url(assets/down_arrow_lighter.png);\n"
                                   "}\n"
                                   "\n"
                                   "QComboBox QAbstractItemView {\n"
                                   "    color: #ffffff;\n"
                                   "    background-color: #828282;\n"
                                   "    border-radius: 3px;\n"
                                   "    margin: 0px;\n"
                                   "    padding: 0px;\n"
                                   "    border: none;\n"
                                   "    min-height: 30px;\n"
                                   "}\n"
                                   "")
        self.f_biaya.setObjectName("f_biaya")
        self.verticalLayout_108.addWidget(self.f_biaya)
        self.verticalLayout_107.addWidget(self.frame_138)
        self.verticalLayout_106.addWidget(self.frame_135)
        self.verticalLayout_47.addWidget(self.frame_81)
        self.frame_36 = QtWidgets.QFrame(self.frameStatus)
        self.frame_36.setMinimumSize(QtCore.QSize(0, 185))
        self.frame_36.setMaximumSize(QtCore.QSize(16777215, 185))
        self.frame_36.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "}")
        self.frame_36.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_36.setObjectName("frame_36")
        self.verticalLayout_48 = QtWidgets.QVBoxLayout(self.frame_36)
        self.verticalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_48.setSpacing(0)
        self.verticalLayout_48.setObjectName("verticalLayout_48")
        self.frame_34 = QtWidgets.QFrame(self.frame_36)
        self.frame_34.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_34.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_34.setStyleSheet("QFrame {\n"
                                    "    background-color:rgba(59,60,77,255);\n"
                                    "    border-radius: 0px;\n"
                                    "}")
        self.frame_34.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_34.setObjectName("frame_34")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_34)
        self.horizontalLayout_10.setContentsMargins(15, 0, 5, 5)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_12 = QtWidgets.QLabel(self.frame_34)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("QLabel {\n"
                                    "    color:rgb(255,255,255);\n"
                                    "    margin-right:10px;\n"
                                    "}")
        self.label_12.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_10.addWidget(self.label_12)
        self.frame_42 = QtWidgets.QFrame(self.frame_34)
        self.frame_42.setMaximumSize(QtCore.QSize(27, 16777215))
        self.frame_42.setStyleSheet("QFrame{\n"
                                    "    margin-top:7.25px;\n"
                                    "    border-image: url(\"./assets/point.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_42.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_42.setObjectName("frame_42")
        self.horizontalLayout_10.addWidget(self.frame_42)
        self.verticalLayout_48.addWidget(self.frame_34)
        self.frame_53 = QtWidgets.QFrame(self.frame_36)
        self.frame_53.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_53.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_53.setObjectName("frame_53")
        self.verticalLayout_66 = QtWidgets.QVBoxLayout(self.frame_53)
        self.verticalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_66.setSpacing(0)
        self.verticalLayout_66.setObjectName("verticalLayout_66")
        self.frame_11 = QtWidgets.QFrame(self.frame_53)
        self.frame_11.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "    border-top-left-radius:0px;\n"
                                    "    border-top-right-radius:0px;\n"
                                    "    border-bottom-left-radius:0px;\n"
                                    "}")
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_50 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_50.setContentsMargins(15, 0, 15, 0)
        self.verticalLayout_50.setSpacing(0)
        self.verticalLayout_50.setObjectName("verticalLayout_50")
        self.frame_54 = QtWidgets.QFrame(self.frame_11)
        self.frame_54.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_54.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_54.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_54.setObjectName("frame_54")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_54)
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.frame_55 = QtWidgets.QFrame(self.frame_54)
        self.frame_55.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_55.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_55.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/dinamic.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_55.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_55.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_55.setObjectName("frame_55")
        self.verticalLayout_49 = QtWidgets.QVBoxLayout(self.frame_55)
        self.verticalLayout_49.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_49.setObjectName("verticalLayout_49")
        self.horizontalLayout_23.addWidget(self.frame_55)
        self.frame_82 = QtWidgets.QFrame(self.frame_54)
        self.frame_82.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_82.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_82.setObjectName("frame_82")
        self.verticalLayout_67 = QtWidgets.QVBoxLayout(self.frame_82)
        self.verticalLayout_67.setContentsMargins(5, 12, 0, -1)
        self.verticalLayout_67.setSpacing(1)
        self.verticalLayout_67.setObjectName("verticalLayout_67")
        self.label_23 = QtWidgets.QLabel(self.frame_82)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_23.setObjectName("label_23")
        self.verticalLayout_67.addWidget(self.label_23)
        self.descServer_7 = QtWidgets.QLabel(self.frame_82)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descServer_7.setFont(font)
        self.descServer_7.setStyleSheet("QLabel {\n"
                                        "    background:transparent;\n"
                                        "    color:rgb(84,91,103);\n"
                                        "}")
        self.descServer_7.setObjectName("descServer_7")
        self.verticalLayout_67.addWidget(self.descServer_7)
        self.horizontalLayout_23.addWidget(self.frame_82)
        self.frameSimulasi = QtWidgets.QFrame(self.frame_54)
        self.frameSimulasi.setMinimumSize(QtCore.QSize(45, 35))
        self.frameSimulasi.setMaximumSize(QtCore.QSize(45, 35))
        self.frameSimulasi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSimulasi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameSimulasi.setObjectName("frameSimulasi")
        self.vSimulasi = QtWidgets.QVBoxLayout(self.frameSimulasi)
        self.vSimulasi.setContentsMargins(0, 0, 0, 0)
        self.vSimulasi.setSpacing(0)
        self.vSimulasi.setObjectName("vSimulasi")
        self.horizontalLayout_23.addWidget(self.frameSimulasi)
        self.verticalLayout_50.addWidget(self.frame_54)
        self.hrLine_4 = QtWidgets.QFrame(self.frame_11)
        self.hrLine_4.setMinimumSize(QtCore.QSize(0, 1))
        self.hrLine_4.setMaximumSize(QtCore.QSize(210, 1))
        self.hrLine_4.setStyleSheet("*{\n"
                                    "    background-color:rgb(214,215,215);\n"
                                    "\n"
                                    "}")
        self.hrLine_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.hrLine_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hrLine_4.setObjectName("hrLine_4")
        self.verticalLayout_50.addWidget(self.hrLine_4)
        self.frame_58 = QtWidgets.QFrame(self.frame_11)
        self.frame_58.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_58.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_58.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_58.setObjectName("frame_58")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.frame_58)
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.frame_59 = QtWidgets.QFrame(self.frame_58)
        self.frame_59.setMinimumSize(QtCore.QSize(40, 40))
        self.frame_59.setMaximumSize(QtCore.QSize(40, 40))
        self.frame_59.setStyleSheet("QFrame{\n"
                                    "    border-image: url(\"./assets/statis.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_59.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_59.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_59.setObjectName("frame_59")
        self.verticalLayout_51 = QtWidgets.QVBoxLayout(self.frame_59)
        self.verticalLayout_51.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_51.setObjectName("verticalLayout_51")
        self.horizontalLayout_29.addWidget(self.frame_59)
        self.frame_83 = QtWidgets.QFrame(self.frame_58)
        self.frame_83.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_83.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_83.setObjectName("frame_83")
        self.verticalLayout_68 = QtWidgets.QVBoxLayout(self.frame_83)
        self.verticalLayout_68.setContentsMargins(5, 12, 0, -1)
        self.verticalLayout_68.setSpacing(0)
        self.verticalLayout_68.setObjectName("verticalLayout_68")
        self.label_24 = QtWidgets.QLabel(self.frame_83)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_24.setObjectName("label_24")
        self.verticalLayout_68.addWidget(self.label_24)
        self.descServer_8 = QtWidgets.QLabel(self.frame_83)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descServer_8.setFont(font)
        self.descServer_8.setStyleSheet("QLabel {\n"
                                        "    background:transparent;\n"
                                        "    color:rgb(84,91,103);\n"
                                        "}")
        self.descServer_8.setObjectName("descServer_8")
        self.verticalLayout_68.addWidget(self.descServer_8)
        self.horizontalLayout_29.addWidget(self.frame_83)
        self.frameHardware = QtWidgets.QFrame(self.frame_58)
        self.frameHardware.setMinimumSize(QtCore.QSize(45, 35))
        self.frameHardware.setMaximumSize(QtCore.QSize(45, 35))
        self.frameHardware.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHardware.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameHardware.setObjectName("frameHardware")
        self.vHardware = QtWidgets.QVBoxLayout(self.frameHardware)
        self.vHardware.setContentsMargins(0, 0, 0, 0)
        self.vHardware.setSpacing(0)
        self.vHardware.setObjectName("vHardware")
        self.horizontalLayout_29.addWidget(self.frameHardware)
        self.verticalLayout_50.addWidget(self.frame_58)
        self.verticalLayout_66.addWidget(self.frame_11)
        self.verticalLayout_48.addWidget(self.frame_53)
        self.verticalLayout_47.addWidget(self.frame_36)
        self.frame_37 = QtWidgets.QFrame(self.frameStatus)
        self.frame_37.setStyleSheet("Line {\n"
                                    "    background-color:rgb(255,255,255);\n"
                                    "}")
        self.frame_37.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_37.setObjectName("frame_37")
        self.verticalLayout_53 = QtWidgets.QVBoxLayout(self.frame_37)
        self.verticalLayout_53.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout_53.setSpacing(0)
        self.verticalLayout_53.setObjectName("verticalLayout_53")
        self.frame_47 = QtWidgets.QFrame(self.frame_37)
        self.frame_47.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_47.setObjectName("frame_47")
        self.verticalLayout_55 = QtWidgets.QVBoxLayout(self.frame_47)
        self.verticalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_55.setSpacing(0)
        self.verticalLayout_55.setObjectName("verticalLayout_55")
        self.frame_48 = QtWidgets.QFrame(self.frame_47)
        self.frame_48.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_48.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_48.setStyleSheet("QFrame {\n"
                                    "    background-color:rgba(59,60,77,255);\n"
                                    "    border-radius: 0px;\n"
                                    "}")
        self.frame_48.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_48.setObjectName("frame_48")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_48)
        self.horizontalLayout_11.setContentsMargins(15, 0, 5, 5)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_16 = QtWidgets.QLabel(self.frame_48)
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("QLabel {\n"
                                    "    color:rgb(255,255,255);\n"
                                    "    margin-right:10px;\n"
                                    "}")
        self.label_16.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_11.addWidget(self.label_16)
        self.frame_51 = QtWidgets.QFrame(self.frame_48)
        self.frame_51.setMaximumSize(QtCore.QSize(27, 16777215))
        self.frame_51.setStyleSheet("QFrame{\n"
                                    "    margin-top:7.25px;\n"
                                    "    border-image: url(\"./assets/point.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_51.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_51.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_51.setObjectName("frame_51")
        self.horizontalLayout_11.addWidget(self.frame_51)
        self.verticalLayout_55.addWidget(self.frame_48)
        self.frame_56 = QtWidgets.QFrame(self.frame_47)
        self.frame_56.setStyleSheet("QFrame {\n"
                                    "    background-color:rgb(27,27,27);\n"
                                    "    border-top-left-radius:0px;\n"
                                    "    border-top-right-radius:0px;\n"
                                    "    border-bottom-left-radius:0px;\n"
                                    "}")
        self.frame_56.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_56.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_56.setObjectName("frame_56")
        self.verticalLayout_86 = QtWidgets.QVBoxLayout(self.frame_56)
        self.verticalLayout_86.setContentsMargins(20, 0, 0, 0)
        self.verticalLayout_86.setSpacing(0)
        self.verticalLayout_86.setObjectName("verticalLayout_86")
        self.frame_57 = QtWidgets.QFrame(self.frame_56)
        self.frame_57.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_57.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_57.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_57.setObjectName("frame_57")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.frame_57)
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.frame_63 = QtWidgets.QFrame(self.frame_57)
        self.frame_63.setMinimumSize(QtCore.QSize(40, 45))
        self.frame_63.setMaximumSize(QtCore.QSize(40, 45))
        self.frame_63.setStyleSheet("QFrame{\n"
                                    "    margin-top:4.0px;\n"
                                    "    border-image: url(\"./assets/img_coorx.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_63.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_63.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_63.setObjectName("frame_63")
        self.verticalLayout_63 = QtWidgets.QVBoxLayout(self.frame_63)
        self.verticalLayout_63.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_63.setObjectName("verticalLayout_63")
        self.horizontalLayout_26.addWidget(self.frame_63)
        self.frame_84 = QtWidgets.QFrame(self.frame_57)
        self.frame_84.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_84.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_84.setObjectName("frame_84")
        self.verticalLayout_69 = QtWidgets.QVBoxLayout(self.frame_84)
        self.verticalLayout_69.setContentsMargins(5, 12, 0, -1)
        self.verticalLayout_69.setSpacing(1)
        self.verticalLayout_69.setObjectName("verticalLayout_69")
        self.label_25 = QtWidgets.QLabel(self.frame_84)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_25.setObjectName("label_25")
        self.verticalLayout_69.addWidget(self.label_25)
        self.coor_x = QtWidgets.QLabel(self.frame_84)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.coor_x.setFont(font)
        self.coor_x.setStyleSheet("QLabel {\n"
                                  "    background:transparent;\n"
                                  "    color:rgb(84,91,103);\n"
                                  "}")
        self.coor_x.setObjectName("coor_x")
        self.verticalLayout_69.addWidget(self.coor_x)
        self.horizontalLayout_26.addWidget(self.frame_84)
        self.verticalLayout_86.addWidget(self.frame_57)
        self.frame_67 = QtWidgets.QFrame(self.frame_56)
        self.frame_67.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_67.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_67.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_67.setObjectName("frame_67")
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout(self.frame_67)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.frame_68 = QtWidgets.QFrame(self.frame_67)
        self.frame_68.setMinimumSize(QtCore.QSize(40, 45))
        self.frame_68.setMaximumSize(QtCore.QSize(40, 45))
        self.frame_68.setStyleSheet("QFrame{\n"
                                    "    margin-top:4.0px;\n"
                                    "    border-image: url(\"./assets/img_coory.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_68.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_68.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_68.setObjectName("frame_68")
        self.verticalLayout_64 = QtWidgets.QVBoxLayout(self.frame_68)
        self.verticalLayout_64.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_64.setObjectName("verticalLayout_64")
        self.horizontalLayout_27.addWidget(self.frame_68)
        self.frame_87 = QtWidgets.QFrame(self.frame_67)
        self.frame_87.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_87.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_87.setObjectName("frame_87")
        self.verticalLayout_74 = QtWidgets.QVBoxLayout(self.frame_87)
        self.verticalLayout_74.setContentsMargins(5, 12, 0, -1)
        self.verticalLayout_74.setSpacing(1)
        self.verticalLayout_74.setObjectName("verticalLayout_74")
        self.label_29 = QtWidgets.QLabel(self.frame_87)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_29.setObjectName("label_29")
        self.verticalLayout_74.addWidget(self.label_29)
        self.coor_y = QtWidgets.QLabel(self.frame_87)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.coor_y.setFont(font)
        self.coor_y.setStyleSheet("QLabel {\n"
                                  "    background:transparent;\n"
                                  "    color:rgb(84,91,103);\n"
                                  "}")
        self.coor_y.setObjectName("coor_y")
        self.verticalLayout_74.addWidget(self.coor_y)
        self.horizontalLayout_27.addWidget(self.frame_87)
        self.verticalLayout_86.addWidget(self.frame_67)
        self.frame_69 = QtWidgets.QFrame(self.frame_56)
        self.frame_69.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_69.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_69.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_69.setObjectName("frame_69")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout(self.frame_69)
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.frame_70 = QtWidgets.QFrame(self.frame_69)
        self.frame_70.setMinimumSize(QtCore.QSize(40, 45))
        self.frame_70.setMaximumSize(QtCore.QSize(40, 45))
        self.frame_70.setStyleSheet("QFrame{\n"
                                    "    margin-top:4.0px;\n"
                                    "    border-image: url(\"./assets/img_coorz.png\") 0 0 0 0 strecth strecth;\n"
                                    "}")
        self.frame_70.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_70.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_70.setObjectName("frame_70")
        self.verticalLayout_81 = QtWidgets.QVBoxLayout(self.frame_70)
        self.verticalLayout_81.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_81.setObjectName("verticalLayout_81")
        self.horizontalLayout_28.addWidget(self.frame_70)
        self.frame_88 = QtWidgets.QFrame(self.frame_69)
        self.frame_88.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_88.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_88.setObjectName("frame_88")
        self.verticalLayout_84 = QtWidgets.QVBoxLayout(self.frame_88)
        self.verticalLayout_84.setContentsMargins(5, 12, 0, -1)
        self.verticalLayout_84.setSpacing(1)
        self.verticalLayout_84.setObjectName("verticalLayout_84")
        self.label_37 = QtWidgets.QLabel(self.frame_88)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(214,215,215);\n"
                                    "}")
        self.label_37.setObjectName("label_37")
        self.verticalLayout_84.addWidget(self.label_37)
        self.coor_z = QtWidgets.QLabel(self.frame_88)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.coor_z.setFont(font)
        self.coor_z.setStyleSheet("QLabel {\n"
                                  "    background:transparent;\n"
                                  "    color:rgb(84,91,103);\n"
                                  "}")
        self.coor_z.setObjectName("coor_z")
        self.verticalLayout_84.addWidget(self.coor_z)
        self.horizontalLayout_28.addWidget(self.frame_88)
        self.verticalLayout_86.addWidget(self.frame_69)
        self.verticalLayout_55.addWidget(self.frame_56)
        self.verticalLayout_53.addWidget(self.frame_47)
        self.verticalLayout_47.addWidget(self.frame_37)
        self.frame_52 = QtWidgets.QFrame(self.frameStatus)
        self.frame_52.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_52.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_52.setObjectName("frame_52")
        self.verticalLayout_47.addWidget(self.frame_52)
        self.horizontalLayout.addWidget(self.frameStatus)
        self.verticalLayout_2.addWidget(self.frameContent)
        self.verticalLayout.addWidget(self.frameApp)
        window.setCentralWidget(self.mainWidget)

        self.retranslateUi(window)
        self.stackedWidget.setCurrentIndex(0)
        self.stack_history.setCurrentIndex(0)
        self.stack_akurasi.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(window)
        self.configure()

    def configure(self):
        self.window = window
        self.itemsFCost = ["Manhattan Distance", "Euclidiance Distance"]
        self.f_biaya.addItems(self.itemsFCost)
        self.f_biaya.currentIndexChanged.connect(self.changeModeFCost)

        self.window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.scrollSocket.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrolHistory.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_akurasi.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_presepsi_v.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)

        self.scroll_akurasi_metode.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)

        # Change Menu
        self.btn = [self.btnCore, self.btnSocket,
                    self.btnHistory, self.btnTesting]

        self.menuLabel = [self.labelCore, self.labelSocket,
                          self.labelHistory, self.labelTesting]

        self.hoverLabel = [self.hoverCore, self.hoverSocket,
                           self.hoverHistory, self.hoverTesting]

        self.imgLabel = [self.imgCore, self.imgSocket,
                         self.imgHistory, self.imgTesting]

        self.tempChange = [self.menuLabel, self.hoverLabel, self.imgLabel]

        self.btnEvent = [self.btnMinimize, self.btnClose]

        self.changeStyle = [["cond"], ["last", "new"]]
        self.lastBtn = 0
        self.menuTxt = [["Main App", "Socket UDP",
                         "Histori Path Planning", "Uji Coba Sistem Path Planning"]]
        self.menuDesc = [["Tampilan Simulasi Sistem Path Planning", "Tampilan Socekt UDP Komunikasi Antar Robot",
                          "Tampilan Histori Path Planning Robot", "Tampilan Uji Coba Sistem Path Planning Robot"]]

        self.labelDescPage.setText(self.menuDesc[0][0])

        for i in range(len(self.btn)):
            self.btn[i].mousePressEvent = lambda _, x=i: self.changeMenu(x)
            self.btn[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            for j in range(len(self.tempChange)):
                if(i == 0):
                    self.tempChange[j][i].setProperty(
                        self.changeStyle[0][0], self.changeStyle[1][1])
                else:
                    self.tempChange[j][i].setProperty(
                        self.changeStyle[0][0], self.changeStyle[1][0])
            if(i < 2):
                self.btnEvent[i].mousePressEvent = lambda _, x=i: self.eventApp(
                    x)
                self.btnEvent[i].setCursor(
                    QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Radio Button Simulasi
        self.toglleSimulasi = []
        self.lyt = [self.vSimulasi, self.vHardware]
        self.frm = [self.frameSimulasi, self.frameHardware]
        for i in range(len(self.lyt)):
            self.tgl = AnimatedToggle(
                checked_color="#22a79d",
                pulse_checked_color="#8dbfbb"
            )
            if(i == classKirim.isActiveSimulasi):
                self.tgl.setChecked(True)
                self.btnSocket.setHidden(not(classKirim.isActiveSimulasi))
                self.pageSocket.setHidden(not(classKirim.isActiveSimulasi))

            self.toglleSimulasi.insert(i, self.tgl)
            self.lyt[i].addWidget(self.tgl)
            self.frm[i].setLayout(self.lyt[i])
            self.tgl.clicked.connect(
                lambda _, x=i: self.updateToogleMethode(x))

        # Scrool Disable
        self.scrollSocket.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrolHistory.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)

        # Radio Button Pos
        self.condFrm = [self.frameObsCond, self.frameEndCond]
        self.condLyt = [self.vObs, self.vEndPoint]
        self.saveTg = []
        self.tglPos = []
        self.addObjectPos = -1
        for i in range(len(self.condFrm)):
            self.tgl = AnimatedToggle(
                checked_color="#22a79d",
                pulse_checked_color="#8dbfbb"
            )
            self.tgl.clicked.connect(
                lambda _, x=i: self.updatePosCond(x))
            self.tglPos.insert(i, self.tgl)
            self.condLyt[i].addWidget(self.tgl)
            self.condFrm[i].setLayout(self.condLyt[i])
            self.saveTg.insert(i, self.tgl)

        self.taskQ = TaskQuit()
        self.taskQ.key.connect(self.keyRes)

        # Object Img
        self.scene = QtWidgets.QGraphicsScene(0., 0., 450., 300.)
        self.graph_view.setScene(self.scene)

        img = QtGui.QPixmap("./assets/ball.png")
        img = img.scaled(20, 20, QtCore.Qt.IgnoreAspectRatio,
                         QtCore.Qt.SmoothTransformation)
        self.ball = QtWidgets.QGraphicsPixmapItem()
        self.ball.setPixmap(img)
        self.ball.setPos(213, 137)
        self.ball.setZValue(0)

        classKirim.cImgBall = [img.width() / 2., img.height() / 2.]

        img = QtGui.QPixmap("./assets/rAsli.png")
        img = img.scaled(25, 35, QtCore.Qt.IgnoreAspectRatio,
                         QtCore.Qt.SmoothTransformation)
        self.robot = QtWidgets.QGraphicsPixmapItem()
        self.robot.setPixmap(img)
        self.robot.setPos(240, 137)
        self.robot.setZValue(1)

        classKirim.cImgRobot = [img.width() / 2., img.height() / 2.]

        self.robot.setAcceptHoverEvents(True)
        self.robot.hoverEnterEvent = self.hoverEnterEvent
        self.robot.hoverLeaveEvent = self.hoverLeaveEvent
        self.robot.mouseReleaseEvent = self.mouseReleaseEvent
        self.robot.mousePressEvent = self.mousePressEvent
        self.robot.mouseMoveEvent = self.mouseMoveEvent

        self.moveImg = [self.ball, self.robot]
        for i in range(len(self.moveImg)):
            if(self.moveImg[i] not in self.scene.items()):
                self.scene.addItem(self.moveImg[i])

        self.frameLapangan.mousePressEvent = self.createObjImage

        # Msg Error
        self.msgErr = MsgError()
        self.msgErr.key.connect(self.keyRes)

        # Move Robot Asli
        self.isMove = 0

        # Trash
        self.trashCond = False
        img = QtGui.QPixmap("./assets/trash.png")
        img = img.scaled(30, 30, QtCore.Qt.IgnoreAspectRatio,
                         QtCore.Qt.SmoothTransformation)
        self.itemTrash = QtWidgets.QGraphicsPixmapItem()
        self.itemTrash.setPixmap(img)
        self.trashPos = np.array(
            [self.frameLapangan.width() - img.width() / 2. - 25., 25. / 2.])
        self.itemTrash.setPos(self.trashPos[0], self.trashPos[1])
        self.itemTrash.setOpacity(self.trashCond)
        if(self.itemTrash not in self.scene.items()):
            self.scene.addItem(self.itemTrash)

        self.window.keyPressEvent = self.keyPressEvent

        # Obstacle View
        self.obsV = []
        self.radiusObsV = []
        self.radiusObsOV = []

        # Start Simulation
        self.changeCusr = [QtGui.QCursor(QtCore.Qt.ForbiddenCursor), QtGui.QCursor(
            QtCore.Qt.PointingHandCursor)]

        self.btnStartSim.setCursor(self.changeCusr[1])
        self.btnStartSim.clicked.connect(self.metode)

        self.astarM = Astar()
        self.astarM.node_search.connect(self.astar_result)
        self.astarM.lock_key.connect(self.key_astar)

        # Path View
        self.pathV = []
        self.time_calculate = None
        self.path_count = [self.path_astar, self.path_imAstar]

        # Locking
        self.lock = 0
        self.btnText = ["Start Simulasi", "Kirim Ke Robot", "Simulasi"]

        # Kinematic Robot
        self.kinematic = KinematicsRobot()
        self.kinematic.realT_node.connect(self.robot_simulasi_move)
        self.isStart = 0
        self.pathSending = []
        self.path_metode = []
        self.viewLoading = 0
        self.viewOtomatis = 0

        # Question Msg
        self.question = QuestionTask()
        self.question.key.connect(self.handle_simulasi)

        # Index
        self.indexView = []

        # Frame Socket Hidden View
        self.isTrueSocket = False
        self.changeCusr = [QtGui.QCursor(QtCore.Qt.ForbiddenCursor), QtGui.QCursor(
            QtCore.Qt.PointingHandCursor)]
        self.btnSocketConn.setCursor(
            self.changeCusr[int(self.isTrueSocket)])
        self.btnSocketConn.clicked.connect(self.start_socketServer)

        self.linePortSocket.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.linePortSocket.textChanged.connect(self.changeDataSocket)

        self.isConnectLabel = ["Connect", "Disconnect"]
        self.alertSocket = [self.msgAlertPortSocket, self.imgAlertPortSocket]

        # Socket UDP
        self.socketUDP = SocketUPDServer()
        self.socketUDP.client_connect.connect(self.addObstacleUDP)
        self.isActive = [["cond"], ["dct", "act"]]
        self.txtBtn = ["Nonaktif", "Aktif"]
        self.clientV = []
        self.socketUDP.path_hardware.connect(self.robot_simulasi_hardware_move)
        self.socketUDP.hapus_client.connect(self.hapus_obs_client)
        self.socketUDP.msg.connect(self.error_socket)

        # Status Robot
        self.statRobot = ["Robot Lawan", "Robot Metode"]
        self.obsOV = []
        self.derajatLogo = u"\u00b0"
        self.coor_z.setText("Z: 0{}".format(self.derajatLogo))
        self.pathTransformation = []
        self.lastCnt = 0

        # History
        self.historyV = []
        self.indexHistoryV = []
        self.isdeleted = 0
        self.index_deleted = 0
        self.quit_history.mousePressEvent = self.changeHistoryView
        self.quit_history.setCursor(QtCore.Qt.PointingHandCursor)
        self.mode_fcost = self.f_biaya.itemText(self.f_biaya.currentIndex())
        self.presepsiV = []

        # Testing
        self.btnAkurasi.setCursor(QtCore.Qt.PointingHandCursor)
        self.btnPresepsi.setCursor(QtCore.Qt.PointingHandCursor)

        self.btnUji = [self.btnAkurasi, self.btnPresepsi]
        for i in range(len(self.btnUji)):
            self.btnUji[i].mousePressEvent = lambda _, x=i: self.changeMenuTesting(
                x)

        self.presepsi_quit.mousePressEvent = self.changePresepsiView
        self.presepsi_quit.setCursor(QtCore.Qt.PointingHandCursor)
        self.handle_view = 0

        self.table_prespsi_astar.setColumnWidth(0, 75)
        self.table_prespsi_astar.setColumnWidth(1, 125)
        self.table_prespsi_astar.setColumnWidth(2, 125)
        self.table_prespsi_astar.setColumnWidth(3, 125)
        self.table_prespsi_astar.setColumnWidth(4, 224)

        header = self.table_prespsi_astar.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_prespsi_astar.verticalHeader().setVisible(False)
        self.table_prespsi_astar.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)

        self.table_prespsi_improv.setColumnWidth(0, 75)
        self.table_prespsi_improv.setColumnWidth(1, 125)
        self.table_prespsi_improv.setColumnWidth(2, 125)
        self.table_prespsi_improv.setColumnWidth(3, 300)

        header = self.table_prespsi_improv.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_prespsi_improv.verticalHeader().setVisible(False)
        self.table_prespsi_improv.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)

        self.txt_efisien_presepsi.setAttribute(
            QtCore.Qt.WA_MacShowFocusRect, 0)
        self.btn_submit_prespsi.setCursor(QtCore.Qt.PointingHandCursor)

        self.quit_akurasi_presepsi.mousePressEvent = self.changePresepsiView
        self.quit_akurasi_presepsi.setCursor(QtCore.Qt.PointingHandCursor)

        items = ["Semua Simulasi", "Simulasi Dummy", "Simulasi Hardware"]
        self.chose_akurasi.addItems(items)
        self.chose_akurasi.currentIndexChanged.connect(
            self.changeAkurasiChoose)

        self.quit_akurasi_v.mousePressEvent = self.changeAkurasiView
        self.quit_akurasi_v.setCursor(QtCore.Qt.PointingHandCursor)

        item = ["Tidak Aman", "Aman"]
        self.status_jalur.addItems(item)

        self.btn_vAkruasi.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_vAkruasi.clicked.connect(self.resultAkurasiMetode)

        self.status_jalur.setEditable(False)
        self.status_jalur.currentIndexChanged.connect(
            self.changeDataStatusJalur)

        self.id_statusJ = 0

        self.quit_akurasi_chart.mousePressEvent = self.QChart
        self.quit_akurasi_chart.setCursor(QtCore.Qt.PointingHandCursor)

    def QChart(self, e):
        self.stack_akurasi.setCurrentIndex(0)
        self.clearLayout(self.verticalLayout_140)
        self.get_pengujianV()

    def changeDataStatusJalur(self, pos):
        stack = self.stack_akurasi.currentIndex()
        if(stack == 4):
            self.getValueAkurasi(self.id_statusJ, pos)

    def resultAkurasiMetode(self):
        query = ""
        pos = self.chose_akurasi.currentIndex()
        if(pos == 0):
            query = """SELECT COUNT(*) as total, (SELECT COUNT(*) FROM tbl_percobaan WHERE akurasi = 0) as tidak_aman, (SELECT COUNT(*) FROM tbl_percobaan WHERE akurasi = 1) as aman FROM tbl_percobaan"""
        else:
            v = self.chose_akurasi.currentText()
            query = """SELECT COUNT(*) as total, (SELECT COUNT(*) FROM tbl_percobaan WHERE akurasi = 0 AND mode LIKE '%{0}%') as tidak_aman, (SELECT COUNT(*) FROM tbl_percobaan WHERE akurasi = 1 AND mode LIKE '%{1}%') as aman FROM tbl_percobaan WHERE mode LIKE '%{2}%'""".format(
                v, v, v)

        result = db.get_manual_query(query)
        result = dict(result[0])
        total = result["total"]
        if(total > 0):
            self.plotV = HistoryPlotPresepsi(
                width=9.2, height=3, dpi=115, mode=1)
            self.toolbar = NavigationToolbar(
                self.plotV, self.frame_akurasi_chart)
            self.toolbar.setStyleSheet("background-color:transparent;")

            item = []
            for i in range(0, 2):
                item.append(self.plot_akurasi_chart.itemAt(i))

            for i in range(len(item)):
                if(item[i] != None):
                    widget = item[i].widget()
                    if(widget != None):
                        self.plot_akurasi_chart.removeWidget(widget)
                        widget.deleteLater()

            akurasi = (result["aman"] / result["total"]) * 100

            e_mutlak = abs(result["total"] - result["aman"])
            e_relatif = (e_mutlak / result["total"]) * 100

            labels = ["Akurasi", "Error Relatif"]
            explode = (0., 0.125)
            colors = ["tab:green", "tab:red"]

            sizes = [akurasi, e_relatif]
            self.plotV.axes_akurasi.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', shadow=True, startangle=240, textprops={'fontsize': 7})
            self.plotV.axes_akurasi.axis('equal')
            self.plotV.axes_akurasi.set_title(
                "Akurasi Metode Improved A* Terhadap Tabrakan", fontsize=10)

            self.plot_akurasi_chart.addWidget(self.plotV)
            self.plot_akurasi_chart.addWidget(self.toolbar)
            self.stack_akurasi.setCurrentIndex(5)
        else:
            self.activateWindow(False)
            self.msgErr.setMsg("Data History Tidak Ada")
            self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()

    def changeAkurasiView(self, e):
        self.id_statusJ = 0
        self.clearLayout(self.verticalLayout_140)
        self.get_pengujianV()
        self.stack_akurasi.setCurrentIndex(0)

    def changeAkurasiChoose(self, pos):
        self.clearLayout(self.verticalLayout_140)
        self.get_pengujianV()

    def changeUjiPresepsi(self, pos):
        try:
            jml = self.txt_efisien_presepsi.text()
            jml = int(jml)
            if(jml > 0):
                query = """UPDATE tbl_uji_presepsi SET total_presepsi = {0}""".format(
                    jml)
                db.get_manual_query(query)
            else:
                self.activateWindow(False)
                self.msgErr.setMsg("Inputan Uji Coba Harus Lebih Dari 0")
                self.msgErr.window.setWindowFlag(
                    QtCore.Qt.WindowStaysOnTopHint)
                self.msgErr.window.show()
        except Exception as e:
            self.activateWindow(False)
            self.msgErr.setMsg("Inputan Uji Coba Harus Integer")
            self.msgErr.window.setWindowFlag(
                QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()

    def changeMenuTesting(self, pos):
        if(pos == 1):
            self.get_historyV()
        self.stack_akurasi.setCurrentIndex(pos)

    def changeModeFCost(self, position):
        self.mode_fcost = self.f_biaya.itemText(position)
        self.astarM.set_fCost(position)

    def changeHistoryView(self, e):
        self.get_historyV()
        self.stack_history.setCurrentIndex(0)

    def changePresepsiView(self, e):
        self.get_historyV()
        self.stack_akurasi.setCurrentIndex(1)

    def error_socket(self, msg):
        self.activateWindow(False)
        self.msgErr.setMsg(msg)
        self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.msgErr.window.show()

    def hapus_obs_client(self, indexs):
        if(indexs >= 0):
            item = self.verticalLayout_24.takeAt(indexs)
            w = item.widget()
            if(w):
                w.deleteLater()
            self.clientV.pop(indexs)
            if(len(classKirim.obsO) > 0):
                classKirim.obsO.pop(indexs)
            if(self.obsOV[indexs] in self.scene.items()):
                self.scene.removeItem(self.obsOV[indexs])
            if(self.radiusObsOV[indexs] in self.scene.items()):
                self.scene.removeItem(self.radiusObsOV[indexs])
            self.obsOV.pop(indexs)
            self.radiusObsOV.pop(indexs)

            if(classKirim.checkMaster[0] == indexs):
                classKirim.checkMaster[0] = -1
                classKirim.checkMaster[1] = 0

            self.updateBtnHardware()
            self.updateObsEvent()

    def robot_simulasi_hardware_move(self, pose):
        selectedIndex = pose["selected"]
        x_node = pose["pos"]
        x_transformation = x_node[0]
        y_transformation = x_node[1]
        z = x_node[2]

        x_v = (x_transformation) * 100 / 2.
        y_v = (y_transformation) * 100 / 2.
        x_v -= classKirim.cImgRobot[0]
        y_v -= classKirim.cImgRobot[1]

        if(classKirim.checkMaster[0] != -1):
            classKirim.start = (x_transformation, y_transformation)
            if(self.lock == 1):
                if(len(self.pathSending) > 0):
                    self.f_biaya.setEnabled(False)
                    t = True
                    cond = 2

                    self.viewLoading += 1

                    if(self.viewLoading >= 750):
                        self.viewLoading = 0
                        self.viewOtomatis += 1

                    if(self.viewOtomatis >= 5):
                        self.viewOtomatis = 0

                    point = "Simulasi"
                    point += " ." * self.viewOtomatis

                    counter = pose["counter"]

                    end_p = np.array(classKirim.end)
                    pose_p = np.array(classKirim.start)
                    err = end_p - pose_p
                    err = np.linalg.norm(err)

                    if(self.lastCnt != counter and counter < len(self.pathSending)):
                        self.lastCnt = counter
                        index = self.indexView[self.lastCnt - 1]
                        self.pathV[index].setBrush(QtCore.Qt.green)
                        t = False

                    if(self.lastCnt == len(self.pathSending) or err <= 0.165):
                        self.lock = 0
                        self.lastCnt = 0
                        t = True
                        point = self.btnText[self.lock]
                        self.f_biaya.setEnabled(True)

                    self.btnText[cond] = point
                    self.btnStartSim.setEnabled(t)
                    self.btnStartSim.setText(self.btnText[cond])

            self.coor_x.setText("X: {} m.".format(
                round(classKirim.start[0], 3)))
            self.coor_y.setText("Y: {} m.".format(
                round(classKirim.start[1], 3)))
            self.coor_z.setText("Z: {}{}".format(
                round(z, 2), self.derajatLogo))
            self.robot.setPos(x_v, y_v)

        if(len(classKirim.obsO) > 0):
            if(classKirim.checkMaster[0] != selectedIndex):
                classKirim.obsO[selectedIndex] = (
                    x_transformation, y_transformation)
                self.obsOV[selectedIndex].setPos(x_v, y_v)
                self.radiusObsOV[selectedIndex].setPos(x_v, y_v)

        total = len(classKirim.obs) + len(classKirim.obsO)
        v_tot = "Total : {}".format(total)
        self.descObs.setText(v_tot)

    def addObstacleUDP(self, object, index):
        self.frameUser = QtWidgets.QFrame(self.frameTampungList)
        self.frameUser.setContentsMargins(0, 0, 0, 0)
        self.frameUser.setMinimumSize(QtCore.QSize(0, 59))
        self.frameUser.setMaximumSize(QtCore.QSize(16777215, 59))
        self.frameUser.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameUser.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameUser.setObjectName("frameUser")
        self.frameUser.setStyleSheet(
            "QFrame:hover{\n""background-color:#2e2e2e;\n""border-radius:0px;\n""}")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frameUser)
        self.horizontalLayout_18.setContentsMargins(18, 10, 0, 0)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.imgList = QtWidgets.QFrame(self.frameUser)
        self.imgList.setMinimumSize(QtCore.QSize(0, 35))
        self.imgList.setMaximumSize(QtCore.QSize(35, 35))
        self.imgList.setStyleSheet(
            "QFrame {\n""    background-color:transparent;\n""    border-image: url(\"./assets/icon_client.png\") 0 0 0 0 strecth strecth;\n""}")
        self.imgList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgList.setObjectName("imgList")
        self.horizontalLayout_18.addWidget(self.imgList)
        self.ipSocket = QtWidgets.QLabel(self.frameUser)
        self.ipSocket.setMinimumSize(QtCore.QSize(163, 0))
        self.ipSocket.setMaximumSize(QtCore.QSize(163, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.ipSocket.setFont(font)
        self.ipSocket.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(136,149,169);\n"
                                    "    padding-left:0.75px;\n"
                                    "}")
        self.ipSocket.setObjectName("ipSocket")
        self.horizontalLayout_18.addWidget(self.ipSocket)
        self.idSocket = QtWidgets.QLabel(self.frameUser)
        self.idSocket.setMinimumSize(QtCore.QSize(119, 0))
        self.idSocket.setMaximumSize(QtCore.QSize(119, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.idSocket.setFont(font)
        self.idSocket.setStyleSheet("QLabel {\n"
                                    "    background:transparent;\n"
                                    "    color:rgb(136,149,169);\n"
                                    "}")
        self.idSocket.setObjectName("idSocket")
        self.horizontalLayout_18.addWidget(self.idSocket)
        self.timeSocket = QtWidgets.QLabel(self.frameUser)
        self.timeSocket.setMinimumSize(QtCore.QSize(224, 0))
        self.timeSocket.setMaximumSize(QtCore.QSize(224, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.timeSocket.setFont(font)
        self.timeSocket.setStyleSheet("QLabel {\n"
                                      "    background:transparent;\n"
                                      "    color:rgb(136,149,169);\n"
                                      "}")
        self.timeSocket.setObjectName("timeSocket")
        self.horizontalLayout_18.addWidget(self.timeSocket)
        self.btnSet = QtWidgets.QPushButton(self.frameUser)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnSet.sizePolicy().hasHeightForWidth())
        self.btnSet.setSizePolicy(sizePolicy)
        self.btnSet.setMinimumSize(QtCore.QSize(118, 30))
        self.btnSet.setMaximumSize(QtCore.QSize(118, 30))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(13)
        self.btnSet.setFont(font)
        self.btnSet.setStyleSheet("QPushButton[cond = \"act\"]{\n"
                                  "    background:transparent;\n"
                                  "    border: 1px solid rgb(56,204,105);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(56,204,105);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton[cond = \"act\"]:hover{\n"
                                  "    background:rgb(56,204,105);\n"
                                  "    border: 1px solid rgb(215,215,215);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(215,215,215);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton[cond = \"act\"]:pressed{\n"
                                  "    background:rgb(56,204,105);\n"
                                  "    border: 1px solid rgb(215,215,215);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(215,215,215);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton[cond = \"dct\"]{\n"
                                  "    background:transparent;\n"
                                  "    border: 1px solid rgb(243,68,85);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(243,68,85);\n"
                                  " }\n"
                                  "\n"
                                  "QPushButton[cond = \"dct\"]:hover{\n"
                                  "    background:rgb(243,68,85);\n"
                                  "    border: 1px solid rgb(215,215,215);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(215,215,215);\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton[cond = \"dct\"]:pressed{\n"
                                  "    background:rgb(243,68,85);\n"
                                  "    border: 1px solid rgb(215,215,215);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(215,215,215);\n"
                                  "\n"
                                  "}")
        self.horizontalLayout_18.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.btnSet.setObjectName("btnSet")
        self.btnSet.setProperty(self.isActive[0][0], self.isActive[1][0])
        self.horizontalLayout_18.addWidget(self.btnSet)
        temp_view = {"ip": self.ipSocket, "id": self.idSocket,
                     "datetime": self.timeSocket, "frame": self.frameUser, "btn": self.btnSet}
        for view in object:
            temp_view[view].setText(str(object[view]))
        self.btnSet.setText(self.txtBtn[0])
        self.verticalLayout_24.addWidget(self.frameUser)

        self.clientV.insert(index, temp_view)

        img = QtGui.QPixmap("./assets/rObs.png")
        img = img.scaled(25, 35, QtCore.Qt.IgnoreAspectRatio,
                         QtCore.Qt.SmoothTransformation)
        new_obstacle = QtWidgets.QGraphicsPixmapItem()
        new_obstacle.setPixmap(img)
        new_obstacle.setZValue(1)

        radius = QtWidgets.QGraphicsEllipseItem()
        x = img.width() / 2**2 * -1
        y = img.height() / 2**2 - 1.5
        radius.setRect(QtCore.QRectF(
            x, y, 2 * classKirim.radius, 2 * classKirim.radius))
        radius.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        radius.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        brush = QtGui.QBrush(QtGui.QColor(QtCore.Qt.transparent))
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        radius.setPen(pen)
        radius.setBrush(brush)

        if(classKirim.isActiveSimulasi == 1):
            self.deleteManualObs()
            if(new_obstacle not in self.scene.items()):
                self.scene.addItem(new_obstacle)
            if(radius not in self.scene.items()):
                self.scene.addItem(radius)

        self.obsOV.insert(index, new_obstacle)
        self.radiusObsOV.insert(index, radius)

        classKirim.obsO.insert(index, (float("inf"), float("inf")))

        self.updateBtnHardware()
        self.updateObsEvent()

    def updateBtnHardware(self):
        for i in range(len(self.clientV)):
            btn = self.clientV[i]["btn"]
            btn.disconnect()
            btn.clicked.connect(lambda _, x=i: self.changeActiveSocket(x))
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def deleteManualObs(self, mode=0):
        try:
            total = len(classKirim.obs) + len(classKirim.obsO)
            if(total >= classKirim.robotMax):
                if(len(classKirim.obs) < 0):
                    mode = -1
            else:
                mode = -1

            if(mode == 0):
                position = len(classKirim.obs) - 1
                classKirim.obs.pop(position)
                if(self.obsV[position] in self.scene.items()):
                    self.scene.removeItem(self.obsV[position])
                self.obsV.pop(position)
            elif(mode == 1):
                total -= classKirim.robotMax
                if(total >= len(classKirim.obs)):
                    total = len(classKirim.obs)

                i_pos = len(classKirim.obs) - 1
                for _ in range(total):
                    classKirim.obs.pop(i_pos)
                    if(self.obsV[i_pos] in self.scene.items()):
                        self.scene.removeItem(self.obsV[i_pos])
                    self.obsV.pop(i_pos)
                    i_pos -= 1
        except Exception as e:
            print("Error Clear: ", e)

    def changeActiveSocket(self, pos):
        lastIdx = 0
        c = 0
        if(classKirim.checkMaster[0] != pos):
            lastIdx = classKirim.checkMaster[0]
            if(classKirim.checkMaster[0] == -1):
                c = 1
            classKirim.checkMaster[0] = pos
            classKirim.checkMaster[1] = 1
        else:
            c = 1
            lastIdx = classKirim.checkMaster[0]
            classKirim.checkMaster[1] = int(not(classKirim.checkMaster[1]))

        if(c == 1):
            iChange = [self.clientV[classKirim.checkMaster[0]]["btn"]]
            condChange = [classKirim.checkMaster[1]]
        else:
            iChange = [self.clientV[classKirim.checkMaster[0]]
                       ["btn"], self.clientV[lastIdx]["btn"]]
            condChange = [classKirim.checkMaster[1],
                          not(classKirim.checkMaster[1])]

        for i in range(len(iChange)):
            iChange[i].setText(self.txtBtn[condChange[i]])
            iChange[i].setProperty(self.isActive[0][0],
                                   self.isActive[1][condChange[i]])
            iChange[i].style().unpolish(iChange[i])
            iChange[i].style().polish(iChange[i])
            iChange[i].update()

        stat = 0
        if(classKirim.checkMaster[1] == 0):
            self.deleteManualObs()
            classKirim.checkMaster[0] = -1
            classKirim.obsO.insert(pos, (float("inf"), float("inf")))
            self.scene.addItem(self.obsOV[pos])
            self.scene.addItem(self.radiusObsOV[pos])
        else:
            classKirim.obsO.pop(pos)
            self.scene.removeItem(self.radiusObsOV[pos])
            self.scene.removeItem(self.obsOV[pos])
            stat = 1

        self.clientV[pos]["id"].setText(self.statRobot[stat])
        self.updateObsEvent()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def changeDataSocket(self, text):
        view = "err"
        msg = ""
        self.isTrueSocket = False
        if(len(text) == 0):
            msg = "Port Tidak Boleh Kosong"
        else:
            try:
                text = int(text)
                if(text >= 0 and text <= 65535):
                    view = "scc"
                    msg = "Port Bisa Dikoneksikan"
                    self.isTrueSocket = True
                else:
                    msg = "Range Port 0-65535"
            except:
                msg = "Port Harus Integer"

        self.btnSocketConn.setCursor(
            self.changeCusr[int(self.isTrueSocket)])
        for i in range(len(self.alertSocket)):
            change = self.alertSocket[i]
            if(i == 0):
                change.setText(msg)
            change.setProperty(self.changeStyle[0][0], view)
            change.style().unpolish(change)
            change.style().polish(change)
            change.update()

    def start_socketServer(self):
        cond = True
        view = "Start: "
        if(self.isTrueSocket):
            if(classKirim.isLoopUDP == 0):
                classKirim.isLoopUDP = 1
                port = self.linePortSocket.text()
                port = int(port)
                self.socketUDP.setServer(port)
                cond = True
                date = datetime.now()
                timestamp = date.strftime('%H:%M:%S')
                view += timestamp
                classKirim.command = 1
            else:
                classKirim.isLoopUDP = 0
                self.clearLayout(self.verticalLayout_24)
                self.clientV = []
                cond = False
                view += "-"
                classKirim.command = 0
                classKirim.checkMaster[0] = -1
                classKirim.checkMaster[1] = 0
                for i in range(len(self.obsOV)):
                    self.scene.removeItem(self.obsOV[i])
                    self.scene.removeItem(self.radiusObsOV[i])
                self.obsOV = []
                classKirim.obsO = []
                self.radiusObsOV = []
        else:
            cond = False

            self.activateWindow(False)
            self.msgErr.setMsg("Koneksi Socket Gagal")
            self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()

        self.linePortSocket.setEnabled(not(int(cond)))
        self.btnSocketConn.setText(self.isConnectLabel[int(cond)])
        self.descServer.setText(view)

    def handle_simulasi(self, condition):
        self.lock = condition
        self.window.setEnabled(True)

        if(self.isdeleted == 1 and condition == 1):
            if(classKirim.isActiveSimulasi == 0):
                self.kinematic.counter = self.kinematic.length
            else:
                classKirim.command = 0
                self.socketUDP.stopData()
            index = self.indexHistoryV.index(self.index_deleted)
            self.indexHistoryV.pop(index)
            self.historyV.pop(index)
            self.presepsiV.pop(index)
            view_plan = [self.verticalLayout_91.takeAt(
                index), self.verticalLayout_116.takeAt(index)]
            for item in view_plan:
                w = item.widget()
                if(w):
                    w.deleteLater()

            db.delete_data("tbl_percobaan", "id_percobaan", self.index_deleted)
            if(self.index_deleted == self.handle_view):
                self.handle_view = 0
                self.get_historyV()
                self.stack_akurasi.setCurrentIndex(1)
            self.index_deleted = 0
            self.isdeleted = 0
            self.lock = 0
            self.btnStartSim.setText(self.btnText[self.lock])
        else:
            if(condition == 1):
                if(classKirim.isActiveSimulasi == 0):
                    self.insertDb()
                    self.path_metode.clear()
                    self.kinematic.setPose(self.pathSending)
                    self.kinematic.start()
                else:
                    if(classKirim.checkMaster[0] != -1):
                        self.insertDb()
                        self.path_metode.clear()
                        classKirim.command = 1
                        self.lastCnt = 0
                        self.socketUDP.kirimData(self.pathTransformation)
                    else:
                        self.path_metode.clear()
                        self.activateWindow(False)
                        self.msgErr.setMsg("Aktifkan Robot Metode")
                        self.msgErr.window.setWindowFlag(
                            QtCore.Qt.WindowStaysOnTopHint)
                        self.msgErr.window.show()
                        self.lock = 0
                        self.clearPathV()
            else:
                self.path_metode.clear()
                self.clearPathV()
                self.pathSending = []
                self.indexView = []
                self.isStart = 0
                self.lock = 0

    def insertDb(self):
        mode = "Simulasi Dummy"
        if(classKirim.isActiveSimulasi == 1):
            mode = "Simulasi Hardware"

        db.insert_data("tbl_percobaan", mode)
        db.insert_data("tbl_metode", self.path_metode)
        db.insert_data("tbl_start", [classKirim.start])
        db.insert_data("tbl_end", [classKirim.end])
        obstacle = classKirim.obs + classKirim.obsO
        if(len(obstacle) > 0):
            db.insert_data("tbl_obstacle", obstacle)
        self.get_historyV()

    def robot_simulasi_move(self, data, cond):
        t = False
        self.viewLoading += 1

        if(self.viewLoading >= 5):
            self.viewLoading = 0

        if(cond > -1):
            self.f_biaya.setEnabled(False)
            x = data[0, 0]
            y = data[1, 0]
            if(cond < len(self.indexView)):
                x_des = np.array(self.pathSending[cond])
                x_now = np.array([(x, y)])
                x_err = x_des - x_now
                enorm = np.linalg.norm(x_err)
                if(enorm <= 0.1):
                    if(len(self.pathV) > 0):
                        index = self.indexView[cond]
                        pathV = self.pathV[index]
                        pathV.setBrush(QtCore.Qt.green)

            cond = 2
            classKirim.start = (x, y)
            self.coor_x.setText("X: {} m.".format(
                round(classKirim.start[0], 3)))
            self.coor_y.setText("Y: {} m.".format(
                round(classKirim.start[1], 3)))
            self.coor_z.setText("Z: 0{}".format(self.derajatLogo))

            x_new = x * 100 / 2. - classKirim.cImgRobot[0]
            y_new = y * 100 / 2. - classKirim.cImgRobot[1]
            self.robot.setPos(x_new, y_new)
            self.lock = 4
            point = "Simulasi"
            point += " ." * self.viewLoading
            self.btnText[cond] = point
        else:
            self.f_biaya.setEnabled(True)
            cond = 0
            t = True
            self.lock = 0
            self.btnText[2] = "Simulasi"

        self.btnStartSim.setEnabled(t)
        self.btnStartSim.setText(self.btnText[cond])

    def key_astar(self, data, counter):
        self.isStart = 1
        self.lock = 1
        if(counter != -1):
            self.path_count[counter[0]].setText(str(counter[1]))
        if(data != -1):
            self.lock = 2
            self.btnStartSim.setText(self.btnText[data])
            new_time = time.time()
            if(data == 1 and counter[0] == 1):
                view_time = round(classKirim.timer[0], 3)
                view_time = ("Time: {} sec.").format(round(view_time, 2))
                self.astar_start.setText(view_time)
            elif(counter[0] == -1):
                self.time_calculate = new_time
        else:
            self.astar_start.setText("Time: -")

    def astar_result(self, data, counter):
        if(len(data) == 0):
            self.lock = 0
            self.activateWindow(False)
            self.msgErr.setMsg("Path Tidak Ditemukan")
            self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()
        elif(len(data) > 0):
            if(len(self.path_metode) >= 2):
                self.path_metode.clear()
            self.indexView.clear()
            if(counter == 0):
                self.pathSending = data
                self.path_metode.append(data)
                if(classKirim.isActiveSimulasi == 1):
                    self.pathTransformation = []
                    self.pathTransformation = copy(self.pathSending)
                    for new_path in data:
                        x = new_path[0]
                        y = new_path[1]
                        x_new = (classKirim.maxX / 2.) - x
                        y_new = ((classKirim.maxY / 2.) - y) * -1
                        point = (x_new, y_new)
                        self.pathTransformation.append(point)

                self.clearPathV()
                for i in range(0, len(data)):
                    radius = 0
                    pathV = QtWidgets.QGraphicsEllipseItem()
                    pathV.setRect(radius, radius, 10, 10)
                    pathV.setBrush(QtCore.Qt.red)
                    x = data[i][0] - 0.0950
                    y = data[i][1] - 0.085
                    x = x * 100 / 2
                    y = y * 100 / 2
                    pathV.setPos(x, y)
                    self.pathV.append(pathV)
                    if(pathV not in self.scene.items()):
                        self.scene.addItem(pathV)
            else:
                for i in range(len(self.pathSending)):
                    node_last = np.array(self.pathSending[i])
                    for j in range(len(data)):
                        node_new = np.array(data[j])
                        enorm = node_last - node_new
                        enorm_lock = np.linalg.norm(enorm)
                        if(enorm_lock == 0.):
                            if(i < len(self.pathV)):
                                self.indexView.append(i)
                                pathV = self.pathV[i]
                                pathV.setBrush(QtCore.Qt.blue)
                                break

                self.pathSending = data
                self.path_metode.append(data)
                if(classKirim.isActiveSimulasi == 1):
                    self.pathTransformation = []
                    for new_path in data:
                        x = new_path[0]
                        y = new_path[1]
                        x_new = (classKirim.maxX / 2.) - x
                        y_new = ((classKirim.maxY / 2.) - y) * -1
                        point = (x_new, y_new)
                        self.pathTransformation.append(point)

    def metode(self):
        if(classKirim.isActiveSimulasi != -1):
            if(self.lock == 0):
                self.pathSending = []
                self.indexView = []
                self.isStart = 0
                self.clearPathV()
                self.astarM.start()
            elif(self.lock == 2):
                self.activateWindow(False)
                self.question.setMsg("Apakah Data ingin Dikirim?")
                self.question.window.setWindowFlag(
                    QtCore.Qt.WindowStaysOnTopHint)
                self.question.window.show()
                self.lock = 0
                self.btnStartSim.setText(self.btnText[self.lock])
        else:

            self.activateWindow(False)
            self.msgErr.setMsg("Harap Memilih Metode")
            self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()

    def keyPressEvent(self, event):
        if(event.key() == QtCore.Qt.Key_1):
            self.trashCond = not(self.trashCond)
            self.itemTrash.setOpacity(int(self.trashCond))
        elif(event.key() == QtCore.Qt.Key_C):
            if(self.lock == 0):
                self.isStart = 0
                self.clearPathV()
                self.astar_start.setText("Time: -")
            elif(self.lock == 2):

                self.activateWindow(False)
                self.msgErr.setMsg("Harap Kirim Data Path Planning")
                self.msgErr.window.setWindowFlag(
                    QtCore.Qt.WindowStaysOnTopHint)
                self.msgErr.window.show()

        elif(event.key() == QtCore.Qt.Key_S):
            self.path_metode.clear()
            if(classKirim.isActiveSimulasi == 0):
                self.kinematic.counter = self.kinematic.length
            else:
                classKirim.command = 0
                self.socketUDP.stopData()

            if(self.lock > 0):
                try:
                    if(db.last_id > 0):
                        index = self.indexHistoryV.index(db.last_id)
                        self.indexHistoryV.pop(index)
                        self.historyV.pop(index)
                        item = self.verticalLayout_91.takeAt(index)
                        w = item.widget()
                        if(w):
                            w.deleteLater()
                        db.delete_data("tbl_percobaan",
                                       "id_percobaan", db.last_id)
                except:
                    pass
                self.get_historyV()

            self.pathSending = []
            self.pathTransformation = []
            self.indexView = []
            self.isStart = 0
            self.clearPathV()
            self.lock = 0
            self.btnStartSim.setText(self.btnText[self.lock])
            self.btnStartSim.setEnabled(True)

        elif(event.key() == QtCore.Qt.Key_K):
            if(self.lock == 1):
                self.socketUDP.kirimData(self.pathTransformation)

    def clearPathV(self):
        for i in range(len(self.pathV)):
            if(self.pathV[i] in self.scene.items()):
                self.scene.removeItem(self.pathV[i])
        self.pathV = []
        if(self.isStart == 0):
            self.astar_start.setText("Time: -")
            for i in range(len(self.path_count)):
                self.path_count[i].setText("0")

    def mouseReleaseEvent(self, e):
        if(classKirim.isActiveSimulasi == 0 and self.lock == 0):
            self.isMove = 0
            x = (self.robot.pos().x() + classKirim.cImgRobot[0]) / 100 * 2.
            y = (self.robot.pos().y() + classKirim.cImgRobot[1]) / 100 * 2.
            classKirim.start = (x, y)
            self.coor_x.setText("X: {} m.".format(
                round(classKirim.start[0], 3)))
            self.coor_y.setText("Y: {} m.".format(
                round(classKirim.start[1], 3)))
            self.coor_z.setText("Z: 0{}".format(self.derajatLogo))

    def mousePressEvent(self, e):
        if(classKirim.isActiveSimulasi == 0 and self.lock == 0):
            self.isMove = 1

    def mouseMoveEvent(self, e):
        if(classKirim.isActiveSimulasi == 0 and self.lock == 0):
            self.isMove = 1
            orig_cursor_position = e.lastScenePos()
            updated_cursor_position = e.scenePos()

            orig_position = self.robot.scenePos()

            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + \
                orig_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + \
                orig_position.y()

            keepW = updated_cursor_x >= classKirim.cImgRobot[0] * - \
                1. and updated_cursor_x <= self.frameLapangan.width() - \
                classKirim.cImgRobot[0]
            keepH = updated_cursor_y >= classKirim.cImgRobot[1] * - \
                1. and updated_cursor_y <= self.frameLapangan.height() - \
                classKirim.cImgRobot[1]
            cond = all((keepW, keepH))
            if(cond):
                self.robot.setPos(updated_cursor_x, updated_cursor_y)

    def hoverEnterEvent(self, e):
        if(classKirim.isActiveSimulasi == 0 and self.lock == 0):
            app.instance().setOverrideCursor(QtCore.Qt.OpenHandCursor)

    def hoverLeaveEvent(self, e):
        if(classKirim.isActiveSimulasi == 0 and self.lock == 0):
            app.instance().restoreOverrideCursor()

    def createObjImage(self, e):
        if(classKirim.isActiveSimulasi != -1):
            x = e.x()
            y = e.y()
            if(self.isMove == 0 and self.lock == 0):
                if(self.addObjectPos == 0):
                    total = len(classKirim.obs)
                    if(classKirim.isActiveSimulasi == 1):
                        total = len(classKirim.obs) + len(classKirim.obsO)
                    if(total < classKirim.robotMax):
                        point_x = x / 100 * 2
                        point_y = y / 100 * 2
                        x = x - classKirim.cImgRobot[0]
                        y = y - classKirim.cImgRobot[1]
                        point = np.array([point_x, point_y])
                        obs_point = np.array([x, y])
                        self.createObstacle(point, obs_point)
                    else:

                        self.activateWindow(False)
                        self.msgErr.setMsg("Robot Obstacle Maksimal 3")
                        self.msgErr.window.setWindowFlag(
                            QtCore.Qt.WindowStaysOnTopHint)
                        self.msgErr.window.show()

                elif(self.addObjectPos == 1):
                    point_x = x / 100 * 2
                    point_y = y / 100 * 2
                    x = x - classKirim.cImgBall[0]
                    y = y - classKirim.cImgBall[1]
                    self.ball.setPos(x, y)
                    classKirim.end = (point_x, point_y)
                else:

                    self.activateWindow(False)
                    self.msgErr.setMsg("Harap Memilih Update Posisi")
                    self.msgErr.window.setWindowFlag(
                        QtCore.Qt.WindowStaysOnTopHint)
                    self.msgErr.window.show()
            else:
                if(self.lock == 2):

                    self.activateWindow(False)
                    self.msgErr.setMsg("Harap Kirim Data Path Planning")
                    self.msgErr.window.setWindowFlag(
                        QtCore.Qt.WindowStaysOnTopHint)
                    self.msgErr.window.show()
        else:

            self.activateWindow(False)
            self.msgErr.setMsg("Harap Memilih Metode Simulasi")
            self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()

    def createObstacle(self, point, obstacleP):
        lock = 0
        obs_total = classKirim.obs
        if(classKirim.isActiveSimulasi == 1):
            obs_total = classKirim.obs + classKirim.obsO

        for obs in obs_total:
            obs_point = np.array(obs)
            pose = obs_point - point
            err = np.linalg.norm(pose)
            # Err Pose 50. cm Radius Titik Tengah Robot
            if(err <= 0.5):
                lock = 1
                break

        if(lock == 1):

            self.activateWindow(False)
            self.msgErr.setMsg("Radius Robot Baru Terlalu Dekat")
            self.msgErr.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.msgErr.window.show()
        else:
            img = QtGui.QPixmap("./assets/rObs.png")
            img = img.scaled(25, 35, QtCore.Qt.IgnoreAspectRatio,
                             QtCore.Qt.SmoothTransformation)
            new_obstacle = QtWidgets.QGraphicsPixmapItem()
            new_obstacle.setPixmap(img)
            new_obstacle.setPos(obstacleP[0], obstacleP[1])
            new_obstacle.setZValue(1)
            new_obstacle.setAcceptHoverEvents(True)
            new_obstacle.hoverEnterEvent = self.hoverEnterEventObs
            new_obstacle.hoverLeaveEvent = self.hoverLeaveEventObs
            radius = QtWidgets.QGraphicsEllipseItem()
            radius.setPos(obstacleP[0], obstacleP[1])
            x = classKirim.cImgRobot[0] / 2. * -1
            y = classKirim.cImgRobot[1] / 2. - 1.25
            radius.setRect(QtCore.QRectF(
                x, y, 2 * classKirim.radius, 2 * classKirim.radius))
            radius.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            radius.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
            brush = QtGui.QBrush(QtGui.QColor(QtCore.Qt.transparent))
            pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
            radius.setPen(pen)
            radius.setBrush(brush)
            self.radiusObsV.append(radius)
            if(radius not in self.scene.items()):
                self.scene.addItem(radius)
            self.obsV.append(new_obstacle)
            point = (point[0], point[1])
            classKirim.obs.append(point)
            if(new_obstacle not in self.scene.items()):
                self.scene.addItem(new_obstacle)
            self.updateObsEvent()

    def hoverEnterEventObs(self, e):
        if(self.lock == 0):
            app.instance().setOverrideCursor(QtCore.Qt.OpenHandCursor)

    def hoverLeaveEventObs(self, e):
        if(self.lock == 0):
            app.instance().restoreOverrideCursor()

    def updateObsEvent(self):
        for i in range(len(classKirim.obs)):
            self.obsV[i].mouseReleaseEvent = lambda event, x=i: self.mouseReleaseEventObs(
                event, x)
            self.obsV[i].mousePressEvent = lambda event, x=i: self.mousePressEventObs(
                event, x)
            self.obsV[i].mouseMoveEvent = lambda event, x=i: self.mouseMoveEventObs(
                event, x)

    def mouseReleaseEventObs(self, event, pos):
        if(self.lock == 0):
            position = self.obsV[pos].pos()
            x_new = (position.x() + classKirim.cImgRobot[0]) / 100 * 2.
            y_new = (position.y() + classKirim.cImgRobot[1]) / 100 * 2.
            maxX = classKirim.maxX
            maxY = classKirim.maxY
            x_new = (maxX + x_new) - maxX
            y_new = (maxY + y_new) - maxY
            classKirim.obs[pos] = (x_new, y_new)

            if(self.trashCond):
                trash_pos = self.trashPos / 100 * 2.
                poseD = trash_pos - np.array(classKirim.obs[pos])
                err = np.linalg.norm(poseD)
                if(err <= 0.75):
                    self.errorSound(0)
                    if(self.obsV[pos] in self.scene.items()):
                        self.scene.removeItem(self.obsV[pos])
                    if(self.radiusObsV[pos] in self.scene.items()):
                        self.scene.removeItem(self.radiusObsV[pos])
                    self.radiusObsV.pop(pos)
                    self.obsV.pop(pos)
                    classKirim.obs.pop(pos)
                    self.updateObsEvent()
                    app.instance().restoreOverrideCursor()

    def mousePressEventObs(self, event, pos):
        if(self.lock == 0):
            pass

    def errorSound(self, pos):
        url = ""
        if(pos == 0):
            url = "assets/trash.wav"
        elif(pos == 1):
            url = "assets/error.wav"

        QtMultimedia.QSound.play(url)

    def mouseMoveEventObs(self, event, pos):
        if(self.lock == 0):
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()

            orig_position = self.obsV[pos].scenePos()

            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + \
                orig_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + \
                orig_position.y()

            keepW = updated_cursor_x >= classKirim.cImgRobot[0] * - \
                1. and updated_cursor_x <= self.frameLapangan.width() - \
                classKirim.cImgRobot[0]
            keepH = updated_cursor_y >= classKirim.cImgRobot[1] * - \
                1. and updated_cursor_y <= self.frameLapangan.height() - \
                classKirim.cImgRobot[1]
            cond = all((keepW, keepH))
            if(cond):
                self.obsV[pos].setPos(updated_cursor_x, updated_cursor_y)
                self.radiusObsV[pos].setPos(updated_cursor_x, updated_cursor_y)

    def updatePosCond(self, pos):
        c = int(self.tglPos[pos].isChecked())
        if(c == 1):
            for i in range(len(self.tglPos)):
                if(i != pos):
                    self.tglPos[i].setChecked(False)
            self.addObjectPos = pos
        else:
            self.addObjectPos = -1

    def updateToogleMethode(self, pos):
        cond = False
        status = 0
        ch = int(self.toglleSimulasi[pos].isChecked())
        if(ch == 1):
            if(pos != classKirim.isActiveSimulasi):
                self.lock = 0
                self.clearPathV()

                classKirim.isActiveSimulasi = pos
                status = pos

                if(pos == 0):
                    classKirim.command = 0
                    if(classKirim.isLoopUDP == 1):
                        self.socketUDP.stopData()

                for i in range(len(self.toglleSimulasi)):
                    if(i != pos):
                        self.toglleSimulasi[i].setChecked(False)
                self.activeShowObs(pos)
        else:
            self.lock = 0
            self.clearPathV()

            if(pos == 1):
                self.changeMenu(0)
                self.activeShowObs(0)

            status = 0
            classKirim.isActiveSimulasi = -1
            self.addObjectPos = -1
            cond = True
            classKirim.command = 0
            for i in range(len(self.tglPos)):
                self.tglPos[i].setChecked(False)

        for i in range(len(self.condFrm)):
            self.saveTg[i].setHidden(cond)
        self.btnSocket.setHidden(not(status))

        if(pos == 0):
            self.changeMenu(0)

        self.btnStartSim.setCursor(self.changeCusr[not(int(cond))])
        self.btnStartSim.setText(self.btnText[self.lock])

        self.updateObsEvent()

    def activeShowObs(self, pos):
        self.deleteManualObs(mode=1)
        for i in range(len(self.obsOV)):
            item = self.scene.items()
            v_obs = self.obsOV[i]
            v_radius = self.radiusObsOV[i]
            if(pos == 0 and v_obs in item):
                self.scene.removeItem(self.obsOV[i])
            elif(pos == 1 and v_obs not in item):
                if(classKirim.checkMaster[0] == i):
                    continue
                self.scene.addItem(self.obsOV[i])

            if(pos == 0 and v_radius in item):
                self.scene.removeItem(self.radiusObsOV[i])
            elif(pos == 1 and v_radius not in item):
                if(classKirim.checkMaster[0] == i):
                    continue
                self.scene.addItem(self.radiusObsOV[i])

    def activateWindow(self, cond):
        self.window.setEnabled(cond)

    def eventApp(self, pos):
        if(pos == 0):
            self.window.showMinimized()
        else:
            self.activateWindow(False)
            self.taskQ.window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.taskQ.window.show()

    def keyRes(self, point):
        self.activateWindow(bool(not(point)))

    def changeMenu(self, pos):
        if(self.lastBtn != pos):
            if(pos == 1):
                obs_total = len(classKirim.obs) + len(classKirim.obsO)
                v_tot = "Total : {}".format(obs_total)
                self.descObs.setText(v_tot)
            elif(pos == 2):
                self.get_historyV()
            elif(pos == 3):
                self.clearLayout(self.verticalLayout_140)
                self.get_pengujianV()

            self.stackedWidget.setCurrentIndex(pos)
            self.labelPage.setText(
                "<strong>{}</strong>".format(self.menuTxt[0][pos]))
            self.labelDescPage.setText(
                "{}".format(self.menuDesc[0][pos]))
            self.ch = [[self.lastBtn, 0], [pos, 1]]
            for i in range(len(self.tempChange)):
                for j in range(len(self.ch)):
                    change = self.tempChange[i][self.ch[j][0]]
                    change.setProperty(
                        self.changeStyle[0][0], self.changeStyle[1][self.ch[j][1]])
                    change.style().unpolish(change)
                    change.style().polish(change)
                    change.update()
            self.lastBtn = pos

    def get_historyV(self):
        try:
            temp = db.get_data_percobaan()
            self.indexHistoryV.clear()
            self.historyV.clear()
            self.clearLayout(self.verticalLayout_91)
            self.clearLayout(self.verticalLayout_116)

            if(len(temp) > 0):
                no = 1
                for items in temp:
                    list_data = dict(items)
                    self.createV_history(list_data, no)
                    no += 1
        except Exception as e:
            print("History View Error: ", e)

    def get_pengujianV(self):
        try:
            index = self.chose_akurasi.currentIndex()
            query = ""
            if(index == 0):
                query = """SELECT * FROM tbl_percobaan"""
            else:
                txt = self.chose_akurasi.currentText()
                query = """SELECT * FROM tbl_percobaan WHERE mode = '{0}' """.format(
                    txt)
            result = db.get_manual_query(query)
            if(len(result) > 0):
                no = 1
                for items in result:
                    list_data = dict(items)
                    self.VAkurasi(list_data, no)
                    no += 1
        except Exception as e:
            print("Pengujian View Error: ", e)

    def createV_history(self, data, nomor):
        # Data
        id_percobaan = data["id_percobaan"]
        self.indexHistoryV.append(id_percobaan)
        self.VHistory(data, nomor)
        self.VPresepsi(data, nomor)
        self.updateBtnHistory()

    def VAkurasi(self, data, nomor):
        waktu_percobaan = data["time"]
        mode = data["mode"]
        id = data["id_percobaan"]
        self.frameHV = QtWidgets.QFrame(self.frame_akurasiV)
        self.frameHV.setMinimumSize(QtCore.QSize(0, 40))
        self.frameHV.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frameHV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameHV.setObjectName("frameHV")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.frameHV)
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.frame_76 = QtWidgets.QFrame(self.frameHV)
        self.frame_76.setMinimumSize(QtCore.QSize(80, 0))
        self.frame_76.setMaximumSize(QtCore.QSize(95, 16777215))
        self.frame_76.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_76.setObjectName("frame_76")
        self.verticalLayout_94 = QtWidgets.QVBoxLayout(self.frame_76)
        self.verticalLayout_94.setContentsMargins(24, 0, 0, 0)
        self.verticalLayout_94.setSpacing(0)
        self.verticalLayout_94.setObjectName("verticalLayout_94")
        self.no_history = QtWidgets.QLabel(self.frame_76)
        self.no_history.setMinimumSize(QtCore.QSize(50, 0))
        self.no_history.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.no_history.setFont(font)
        self.no_history.setStyleSheet("QLabel {\n"
                                      "    background:transparent;\n"
                                      "    color:rgb(136,149,169);\n"
                                      "}")
        self.no_history.setObjectName("no_history")
        self.verticalLayout_94.addWidget(self.no_history)
        self.horizontalLayout_30.addWidget(self.frame_76)
        self.frame_77 = QtWidgets.QFrame(self.frameHV)
        self.frame_77.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_77.setObjectName("frame_77")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_77)
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.mode_history = QtWidgets.QLabel(self.frame_77)
        self.mode_history.setMinimumSize(QtCore.QSize(160, 0))
        self.mode_history.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.mode_history.setFont(font)
        self.mode_history.setStyleSheet("QLabel {\n"
                                        "    background:transparent;\n"
                                        "    color:rgb(136,149,169);\n"
                                        "}")
        self.mode_history.setObjectName("mode_history")
        self.horizontalLayout_21.addWidget(self.mode_history)
        self.waktu_history = QtWidgets.QLabel(self.frame_77)
        self.waktu_history.setMinimumSize(QtCore.QSize(160, 0))
        self.waktu_history.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.waktu_history.setFont(font)
        self.waktu_history.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(136,149,169);\n"
                                         "}")
        self.waktu_history.setObjectName("waktu_history")
        self.horizontalLayout_21.addWidget(self.waktu_history)
        self.status = QtWidgets.QLabel(self.frame_77)
        self.status.setMinimumSize(QtCore.QSize(120, 0))
        self.status.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.status.setFont(font)
        self.status.setStyleSheet("QLabel {\n"
                                  "    background:transparent;\n"
                                  "    color:rgb(136,149,169);\n"
                                  "}")
        self.status.setObjectName("status")
        self.horizontalLayout_21.addWidget(self.status)
        self.btn_viewH = QtWidgets.QPushButton(self.frame_77)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_viewH.sizePolicy().hasHeightForWidth())
        self.btn_viewH.setSizePolicy(sizePolicy)
        self.btn_viewH.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_viewH.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(13)
        self.btn_viewH.setFont(font)
        self.btn_viewH.setStyleSheet("QPushButton {\n"
                                     "    background:transparent;\n"
                                     "    border: 1px solid rgb(255,255,255);\n"
                                     "    border-radius:7.5px;\n"
                                     "    color:rgb(255,255,255);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    color:rgba(255,255,255,255);\n"
                                     "    background-color:rgba(36,205,133,255);\n"
                                     "    border: 1px solid rgb(255,255,255);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color:rgba(36,205,133,255);\n"
                                     "    color:rgb(255,255,255);\n"
                                     "    border: 1.5px solid rgb(255,255,255);\n"
                                     "}\n"
                                     "")
        self.btn_viewH.setObjectName("btn_viewH")
        self.horizontalLayout_21.addWidget(self.btn_viewH)
        self.horizontalLayout_30.addWidget(self.frame_77)
        self.no_history.setText(str(nomor) + ".")
        self.btn_viewH.setText("Pengujian")
        cond = data["akurasi"]
        st = "Aman"
        if(cond == 0):
            st = "Tidak Aman"
        self.status.setText(st)
        self.mode_history.setText(mode)
        self.waktu_history.setText(str(waktu_percobaan))
        self.btn_viewH.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_140.addWidget(self.frameHV)
        self.btn_viewH.disconnect()
        self.btn_viewH.clicked.connect(
            lambda _, x=[0, 2, id]: self.functionV_History(x))

    def getValueAkurasi(self, id, e):
        query = """UPDATE tbl_percobaan SET akurasi = {0} WHERE id_percobaan = {1}""".format(
            e, id)
        db.get_manual_query(query)

    def VPresepsi(self, data, nomor):
        waktu_percobaan = data["time"]
        mode = data["mode"]
        self.frameHV = QtWidgets.QFrame(self.frame_presepsiV)
        self.frameHV.setMinimumSize(QtCore.QSize(0, 40))
        self.frameHV.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frameHV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameHV.setObjectName("frameHV")

        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.frameHV)
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.frame_76 = QtWidgets.QFrame(self.frameHV)
        self.frame_76.setMinimumSize(QtCore.QSize(85, 0))
        self.frame_76.setMaximumSize(QtCore.QSize(95, 16777215))
        self.frame_76.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_76.setObjectName("frame_76")
        self.verticalLayout_94 = QtWidgets.QVBoxLayout(self.frame_76)
        self.verticalLayout_94.setContentsMargins(24, 0, 0, 0)
        self.verticalLayout_94.setSpacing(0)
        self.verticalLayout_94.setObjectName("verticalLayout_94")
        self.no_history = QtWidgets.QLabel(self.frame_76)
        self.no_history.setMinimumSize(QtCore.QSize(50, 0))
        self.no_history.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.no_history.setFont(font)
        self.no_history.setStyleSheet("QLabel {\n"
                                      "    background:transparent;\n"
                                      "    color:rgb(136,149,169);\n"
                                      "}")
        self.no_history.setObjectName("no_history")
        self.verticalLayout_94.addWidget(self.no_history)
        self.horizontalLayout_30.addWidget(self.frame_76)
        self.frame_77 = QtWidgets.QFrame(self.frameHV)
        self.frame_77.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_77.setObjectName("frame_77")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout(self.frame_77)
        self.horizontalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_39.setSpacing(10)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.mode_history = QtWidgets.QLabel(self.frame_77)
        self.mode_history.setMinimumSize(QtCore.QSize(155, 0))
        self.mode_history.setMaximumSize(QtCore.QSize(155, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.mode_history.setFont(font)
        self.mode_history.setStyleSheet("QLabel {\n"
                                        "    background:transparent;\n"
                                        "    color:rgb(136,149,169);\n"
                                        "}")
        self.mode_history.setObjectName("mode_history")
        self.horizontalLayout_39.addWidget(self.mode_history)
        self.waktu_history = QtWidgets.QLabel(self.frame_77)
        self.waktu_history.setMinimumSize(QtCore.QSize(200, 0))
        self.waktu_history.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.waktu_history.setFont(font)
        self.waktu_history.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(136,149,169);\n"
                                         "}")
        self.waktu_history.setObjectName("waktu_history")
        self.horizontalLayout_39.addWidget(self.waktu_history)
        self.btn_viewH = QtWidgets.QPushButton(self.frame_77)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_viewH.sizePolicy().hasHeightForWidth())
        self.btn_viewH.setSizePolicy(sizePolicy)
        self.btn_viewH.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_viewH.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(13)
        self.btn_viewH.setFont(font)
        self.btn_viewH.setStyleSheet("QPushButton {\n"
                                     "    background:transparent;\n"
                                     "    border: 1px solid rgb(255,255,255);\n"
                                     "    border-radius:7.5px;\n"
                                     "    color:rgb(255,255,255);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    color:rgba(255,255,255,255);\n"
                                     "    background-color:rgba(36,205,133,255);\n"
                                     "    border: 1px solid rgb(255,255,255);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color:rgba(36,205,133,255);\n"
                                     "    color:rgb(255,255,255);\n"
                                     "    border: 1.5px solid rgb(255,255,255);\n"
                                     "}\n"
                                     "")
        self.btn_viewH.setObjectName("btn_viewH")
        self.horizontalLayout_39.addWidget(self.btn_viewH)
        self.btn_deleteH = QtWidgets.QPushButton(self.frame_77)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_deleteH.sizePolicy().hasHeightForWidth())
        self.btn_deleteH.setSizePolicy(sizePolicy)
        self.btn_deleteH.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_deleteH.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(13)
        self.btn_deleteH.setFont(font)
        self.btn_deleteH.setStyleSheet("QPushButton {\n"
                                       "    background:transparent;\n"
                                       "    border: 1px solid rgb(255,255,255);\n"
                                       "    border-radius:7.5px;\n"
                                       "    color:rgb(255,255,255);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover{\n"
                                       "    color:rgba(255,255,255,255);\n"
                                       "    background-color:rgba(240,79,43,255);\n"
                                       "    border: 1px solid rgb(255,255,255);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color:rgba(240,79,43,255);\n"
                                       "    color:rgb(255,255,255);\n"
                                       "    border: 1.5px solid rgb(255,255,255);\n"
                                       "}\n"
                                       "")
        self.btn_deleteH.setObjectName("btn_deleteH")
        self.horizontalLayout_39.addWidget(self.btn_deleteH)
        self.horizontalLayout_30.addWidget(self.frame_77)
        self.verticalLayout_116.addWidget(self.frameHV)
        self.no_history.setText(str(nomor) + ".")
        self.btn_deleteH.setText("Akurasi")
        self.btn_viewH.setText("Pengujian")
        self.mode_history.setText(mode)
        self.waktu_history.setText(str(waktu_percobaan))
        self.btn_deleteH.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_viewH.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        temp_view = {"frame": self.frameHV, "btn_del": self.btn_deleteH,
                     "btn_view": self.btn_viewH, "mode": self.mode_history, "waktu": self.waktu_history}

        self.presepsiV.append(temp_view)

    def VHistory(self, data, nomor):
        waktu_percobaan = data["time"]
        mode = data["mode"]
        self.frameHV = QtWidgets.QFrame(self.frame_historyV)
        self.frameHV.setMinimumSize(QtCore.QSize(0, 40))
        self.frameHV.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frameHV.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHV.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameHV.setObjectName("frameHV")

        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.frameHV)
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.frame_76 = QtWidgets.QFrame(self.frameHV)
        self.frame_76.setMinimumSize(QtCore.QSize(85, 0))
        self.frame_76.setMaximumSize(QtCore.QSize(95, 16777215))
        self.frame_76.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_76.setObjectName("frame_76")
        self.verticalLayout_94 = QtWidgets.QVBoxLayout(self.frame_76)
        self.verticalLayout_94.setContentsMargins(24, 0, 0, 0)
        self.verticalLayout_94.setSpacing(0)
        self.verticalLayout_94.setObjectName("verticalLayout_94")
        self.no_history = QtWidgets.QLabel(self.frame_76)
        self.no_history.setMinimumSize(QtCore.QSize(50, 0))
        self.no_history.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.no_history.setFont(font)
        self.no_history.setStyleSheet("QLabel {\n"
                                      "    background:transparent;\n"
                                      "    color:rgb(136,149,169);\n"
                                      "}")
        self.no_history.setObjectName("no_history")
        self.verticalLayout_94.addWidget(self.no_history)
        self.horizontalLayout_30.addWidget(self.frame_76)
        self.frame_77 = QtWidgets.QFrame(self.frameHV)
        self.frame_77.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_77.setObjectName("frame_77")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout(self.frame_77)
        self.horizontalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_39.setSpacing(10)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.mode_history = QtWidgets.QLabel(self.frame_77)
        self.mode_history.setMinimumSize(QtCore.QSize(155, 0))
        self.mode_history.setMaximumSize(QtCore.QSize(155, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.mode_history.setFont(font)
        self.mode_history.setStyleSheet("QLabel {\n"
                                        "    background:transparent;\n"
                                        "    color:rgb(136,149,169);\n"
                                        "}")
        self.mode_history.setObjectName("mode_history")
        self.horizontalLayout_39.addWidget(self.mode_history)
        self.waktu_history = QtWidgets.QLabel(self.frame_77)
        self.waktu_history.setMinimumSize(QtCore.QSize(200, 0))
        self.waktu_history.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.waktu_history.setFont(font)
        self.waktu_history.setStyleSheet("QLabel {\n"
                                         "    background:transparent;\n"
                                         "    color:rgb(136,149,169);\n"
                                         "}")
        self.waktu_history.setObjectName("waktu_history")
        self.horizontalLayout_39.addWidget(self.waktu_history)
        self.btn_viewH = QtWidgets.QPushButton(self.frame_77)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_viewH.sizePolicy().hasHeightForWidth())
        self.btn_viewH.setSizePolicy(sizePolicy)
        self.btn_viewH.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_viewH.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(13)
        self.btn_viewH.setFont(font)
        self.btn_viewH.setStyleSheet("QPushButton {\n"
                                     "    background:transparent;\n"
                                     "    border: 1px solid rgb(255,255,255);\n"
                                     "    border-radius:7.5px;\n"
                                     "    color:rgb(255,255,255);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    color:rgba(255,255,255,255);\n"
                                     "    background-color:rgba(36,205,133,255);\n"
                                     "    border: 1px solid rgb(255,255,255);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:pressed{\n"
                                     "    background-color:rgba(36,205,133,255);\n"
                                     "    color:rgb(255,255,255);\n"
                                     "    border: 1.5px solid rgb(255,255,255);\n"
                                     "}\n"
                                     "")
        self.btn_viewH.setObjectName("btn_viewH")
        self.horizontalLayout_39.addWidget(self.btn_viewH)
        self.btn_deleteH = QtWidgets.QPushButton(self.frame_77)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_deleteH.sizePolicy().hasHeightForWidth())
        self.btn_deleteH.setSizePolicy(sizePolicy)
        self.btn_deleteH.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_deleteH.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(13)
        self.btn_deleteH.setFont(font)
        self.btn_deleteH.setStyleSheet("QPushButton {\n"
                                       "    background:transparent;\n"
                                       "    border: 1px solid rgb(255,255,255);\n"
                                       "    border-radius:7.5px;\n"
                                       "    color:rgb(255,255,255);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover{\n"
                                       "    color:rgba(255,255,255,255);\n"
                                       "    background-color:rgba(240,79,43,255);\n"
                                       "    border: 1px solid rgb(255,255,255);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color:rgba(240,79,43,255);\n"
                                       "    color:rgb(255,255,255);\n"
                                       "    border: 1.5px solid rgb(255,255,255);\n"
                                       "}\n"
                                       "")
        self.btn_deleteH.setObjectName("btn_deleteH")
        self.horizontalLayout_39.addWidget(self.btn_deleteH)
        self.horizontalLayout_30.addWidget(self.frame_77)
        self.verticalLayout_91.addWidget(self.frameHV)

        self.no_history.setText(str(nomor) + ".")
        self.btn_deleteH.setText("Hapus")
        self.btn_viewH.setText("Lihat")
        self.mode_history.setText(mode)
        self.waktu_history.setText(str(waktu_percobaan))
        self.btn_deleteH.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_viewH.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        temp_view = {"frame": self.frameHV, "btn_del": self.btn_deleteH,
                     "btn_view": self.btn_viewH, "mode": self.mode_history, "waktu": self.waktu_history}

        self.historyV.append(temp_view)

    def updateBtnHistory(self):
        for i in range(len(self.historyV)):
            id_click = self.indexHistoryV[i]
            btn_del = self.historyV[i]["btn_del"]
            btn_view = self.historyV[i]["btn_view"]

            btn_pengujian = self.presepsiV[i]["btn_view"]
            btn_akurasi = self.presepsiV[i]["btn_del"]

            btn = [[btn_view, btn_del], [btn_pengujian, btn_akurasi]]

            inc = 0
            for item_btn in btn:
                index = 0
                for counter in item_btn:
                    counter.disconnect()
                    counter.clicked.connect(
                        lambda _, x=[index, inc, id_click]: self.functionV_History(x))
                    index += 1
                inc += 1

    def functionV_History(self, condition):
        id = condition[2]
        pos = condition[0]
        status = condition[1]

        if(pos == 0):
            if(self.lock > 0):
                self.activateWindow(False)
                self.msgErr.setMsg("Simulasi Sedang Berjalan")
                self.msgErr.window.setWindowFlag(
                    QtCore.Qt.WindowStaysOnTopHint)
                self.msgErr.window.show()
            else:
                if(status == 2):
                    self.id_statusJ = id
                    query = """SELECT akurasi FROM tbl_percobaan WHERE id_percobaan = {0}""".format(
                        id)
                    result = db.get_manual_query(query)
                    result = dict(result[0])
                    self.status_jalur.setCurrentIndex(result["akurasi"])
                self.changeMenuHistory(id, status)
        else:
            if(status == 0):
                self.index_deleted = id
                self.isdeleted = 1
                self.activateWindow(False)
                self.question.setMsg(
                    "Apakah Percobaan ID: {0} Ini Ingin Dihapus?".format(id))
                self.question.window.setWindowFlag(
                    QtCore.Qt.WindowStaysOnTopHint)
                self.question.window.show()
            else:
                if(self.lock > 0):
                    self.activateWindow(False)
                    self.msgErr.setMsg("Simulasi Sedang Berjalan")
                    self.msgErr.window.setWindowFlag(
                        QtCore.Qt.WindowStaysOnTopHint)
                    self.msgErr.window.show()
                else:
                    self.getViewChartAkurasi(id)
                    self.stack_akurasi.setCurrentIndex(3)

    def getViewChartAkurasi(self, id):
        self.plotV = HistoryPlotPresepsi(width=9.2, height=3, dpi=115, mode=0)
        self.toolbar = NavigationToolbar(self.plotV, self.frame_plot_presepsi)
        self.toolbar.setStyleSheet("background-color:transparent;")

        item = []
        for i in range(0, 2):
            item.append(self.plot_akurasi_presepsi.itemAt(i))

        for i in range(len(item)):
            if(item[i] != None):
                widget = item[i].widget()
                if(widget != None):
                    self.plot_akurasi_presepsi.removeWidget(widget)
                    widget.deleteLater()

        query = """SELECT COUNT(*) as total, (SELECT COUNT(*) FROM tbl_metode WHERE nilai == 1 AND id_percobaan = {0} AND mode LIKE '%{1}%') as efisien, (SELECT COUNT(*) FROM tbl_metode WHERE nilai == 0 AND id_percobaan = {2} AND mode LIKE '%{3}%') as tidak_efisien FROM tbl_metode WHERE id_percobaan = {4} AND mode LIKE '%{5}%'""".format(
                id, "Astar Search", id, "Astar Search", id, "Astar Search")
        astar_result = db.get_manual_query(query)
        astar_result = dict(astar_result[0])
        akurasi = (astar_result["efisien"] / astar_result["total"]) * 100

        e_mutlak = abs(astar_result["total"] - astar_result["efisien"])
        e_relatif = (e_mutlak / astar_result["total"]) * 100

        labels = ["Akurasi", "Error Relatif"]
        explode = (0., 0.125)
        colors = ["tab:green", "tab:red"]

        sizes = [akurasi, e_relatif]
        self.plotV.axes_astar.pie(sizes, explode=explode, labels=labels, colors=colors,
                                  autopct='%1.1f%%', shadow=True, startangle=240, textprops={'fontsize': 7})
        self.plotV.axes_astar.axis('equal')
        self.plotV.axes_astar.set_title("Presepsi A*", fontsize=10)

        query = """SELECT total_sebenarnya,total_presepsi FROM tbl_uji_presepsi WHERE id_percobaan = {0}""".format(
                id)
        improved_result = db.get_manual_query(query)
        improved_result = dict(improved_result[0])

        akurasi = (improved_result["total_presepsi"] /
                   improved_result["total_sebenarnya"]) * 100

        e_mutlak = abs(
            improved_result["total_sebenarnya"] - improved_result["total_presepsi"])
        e_relatif = (e_mutlak / improved_result["total_sebenarnya"]) * 100

        labels = ["Akurasi", "Error Relatif"]
        explode = (0., 0.125)
        colors = ["tab:orange", "tab:blue"]

        sizes = [akurasi, e_relatif]
        self.plotV.axes_imp.pie(sizes, explode=explode, labels=labels, colors=colors,
                                autopct='%1.1f%%', shadow=True, startangle=240, textprops={'fontsize': 7})
        self.plotV.axes_imp.axis('equal')
        self.plotV.axes_imp.set_title("Presepsi Improved A*", fontsize=10)

        self.plot_akurasi_presepsi.addWidget(self.plotV)
        self.plot_akurasi_presepsi.addWidget(self.toolbar)

    def changeMenuHistory(self, id, status):
        mode_v = [[self.frame_plot_history, self.plot_history],
                  [self.frame_plot_presepsi_v, self.plot_presepsi_v], [self.frame_plot_akurasi, self.plot_akurasi]]

        position = mode_v[status]

        mode_fCost = ""
        self.plotV = HistoryPlot(width=9.2, height=3, dpi=115)
        self.toolbar = NavigationToolbar(self.plotV, position[0])
        self.toolbar.setStyleSheet("background-color:transparent;")

        item = []
        for i in range(0, 2):
            item.append(position[1].itemAt(i))

        for i in range(len(item)):
            if(item[i] != None):
                widget = item[i].widget()
                if(widget != None):
                    position[1].removeWidget(widget)
                    widget.deleteLater()

        x_p = []
        y_p = []
        pose = db.get_query("tbl_history", id)
        for history in pose:
            pose_update = dict(history)
            x = pose_update["x"]
            y = pose_update["y"]
            z = pose_update["z"]
            self.plotV.axes.arrow(x, y, np.cos(z), np.sin(
                z), color='g', alpha=0.25, width=0.05, linewidth=1, label="arah hadap awal")
            x_p.append(x)
            y_p.append(y)
        self.plotV.axes.plot(x_p, y_p, color="#1B1B1B",
                             linestyle="-.", label="Perpindahan Robot")

        start_point = db.get_query("tbl_start", id)
        for start in start_point:
            pos_start = dict(start)
            x = pos_start["x"]
            y = pos_start["y"]
            z = pos_start["z"]
            self.plotV.axes.arrow(x, y, np.cos(z), np.sin(
                z), color='g', width=0.05, linewidth=1, label="arah hadap awal")
            self.plotV.axes.plot(
                x, y, color="g", marker="o", label="Titik Awal")

        end_point = db.get_query("tbl_end", id)
        for end in end_point:
            pose_end = dict(end)
            x = pose_end["x"]
            y = pose_end["y"]
            z = pose_end["z"]
            self.plotV.axes.arrow(x, y, np.cos(z), np.sin(
                z), color='b', width=0.05, linewidth=1, label="Titik Akhir")
            self.plotV.axes.plot(
                x, y, color="b", marker="o", label="Titik Akhir")

        astar_testing = []
        counter = 0
        astar_point = db.get_query_and(
            "tbl_metode", id, "mode LIKE '%{0}%'".format("Astar Search"))
        for astar in astar_point:
            pos_astar = dict(astar)
            astar_testing.append(pos_astar)
            x = pos_astar["x"]
            y = pos_astar["y"]
            z = pos_astar["z"]
            fScore = round(pos_astar["fScore"], 2)
            mode_fCost = pos_astar["mode_fCost"]
            text_v = "$A*^{{{0}}}$: {1}".format(counter, fScore)
            self.plotV.axes.scatter(
                x, y, marker='X', color="r", label=text_v)
            counter += 1

        improve_testing = []
        improve_point = db.get_query_and(
            "tbl_metode", id, "mode LIKE '%{0}%'".format("Improved Astar"))
        counter = 0
        for improve in improve_point:
            pos_improve = dict(improve)
            improve_testing.append(pos_improve)
            x = pos_improve["x"]
            y = pos_improve["y"]
            z = pos_improve["z"]
            fScore = round(pos_improve["fScore"], 2)
            text_v = "$Imp. A*^{{{0}}}$: {1}".format(counter, fScore)
            self.plotV.axes.scatter(
                x, y, marker='X', color="b", label=text_v)
            counter += 1

        obs_point = db.get_query("tbl_obstacle", id)
        for obstacle in obs_point:
            pos_obs = dict(obstacle)
            x = pos_obs["x"]
            y = pos_obs["y"]
            z = pos_obs["z"]
            self.plotV.axes.scatter(
                x, y, color="k", marker="h", s=225)

        lines, labels = self.plotV.figure.axes[-1].get_legend_handles_labels()
        line = []
        label = []
        for i in range(len(labels)):
            if(labels[i] not in label):
                label.append(labels[i])
                line.append(lines[i])

        self.plotV.figure.legend(line, label, prop={'size': 6})
        position[1].addWidget(self.plotV)
        position[1].addWidget(self.toolbar)
        timer = """SELECT WAKTU FROM tbl_waktu WHERE id_percobaan = {0}""".format(
            id)
        timer = db.get_manual_query(timer)[0]
        timer = dict(timer)
        timer = str(timer["waktu"]) + " sec"
        text_v = "<html><head/><body><p><span style=\" font-weight:600;\">History Percobaan Path Planning ID: {0} - <i>f(cost)</i> : {1} - {2}</span></p></body></html>".format(
            id, mode_fCost, timer)

        if(status == 0):
            self.history_id.setText(text_v)
            self.stack_history.setCurrentIndex(1)
        elif(status == 1):
            self.handle_view = id
            # Query
            query = """SELECT * FROM tbl_uji_presepsi WHERE id_percobaan = {0}""".format(
                id)
            query = db.get_manual_query(query)
            if(len(query) > 0):
                query = query[0]
                result = dict(query)
                total = result["total_presepsi"]
                self.txt_efisien_presepsi.setText(str(total))

            self.btn_submit_prespsi.disconnect()
            self.btn_submit_prespsi.clicked.connect(
                lambda _, x=id: self.changeUjiPresepsi(x))
            self.presepsi_id.setText(text_v)
            data = [astar_testing, improve_testing]
            self.createTableV(data)
            self.stack_akurasi.setCurrentIndex(2)
        elif(status == 2):
            self.stack_akurasi.setCurrentIndex(4)

    def createTableV(self, data):
        astar = data[0]
        improve = data[1]

        self.table_prespsi_improv.setRowCount(0)
        self.table_prespsi_astar.setRowCount(0)

        for i in range(len(astar)):
            self.table_prespsi_astar.insertRow(i)
            self.table_prespsi_astar.setRowHeight(i, 40)
            x = astar[i]["x"]
            y = astar[i]["y"]
            fCost = astar[i]["fScore"]
            x = round(x, 2)
            y = round(y, 2)
            fCost = round(fCost, 2)

            pos = [str(i+1) + ".", x, y, fCost]
            for j in range(len(pos)):
                self.table_prespsi_astar.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(pos[j])))
                self.table_prespsi_astar.item(
                    i, j).setTextAlignment(QtCore.Qt.AlignCenter)

            self.combo_box = QtWidgets.QComboBox()
            self.combo_box.setGeometry(QtCore.QRect(200, 60, 150, 33))
            self.combo_box.setMinimumSize(QtCore.QSize(92, 30))
            self.combo_box.setStyleSheet("QComboBox:focus {\n"
                                         "    border-color: #7cabf9;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox {\n"
                                         "    color: rgb(0,0,0);\n"
                                         "    background-color: rgb(255,255,255);\n"
                                         "    selection-color: black;\n"
                                         "    selection-background-color: #5e90fa;\n"
                                         "    border: 1px solid #b6b6b6;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-top-color: #a2a2a0;\n"
                                         "    padding: 2px 6px 2px 10px; \n"
                                         "    margin: 0px 2px 0px 2px;\n"
                                         "    min-width: 70px;\n"
                                         "    border-radius: 3px;\n"
                                         "    min-height: 24px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox:on {\n"
                                         "    color: black;\n"
                                         "    background-color: #b6b6b6;\n"
                                         "    border-color: #7cabf9;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::drop-down {\n"
                                         "    subcontrol-origin: margin;\n"
                                         "    subcontrol-position: top right;\n"
                                         "    width: 30px;\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: transparent;\n"
                                         "    border-left-style: solid;\n"
                                         "    border-top-right-radius: 3px;\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "    background-color: qlineargradient(spread:pad, x1:1, y1:0.8, x2:1,        y2:0, stop:0 #5e90fa, stop:1 #7cabf9);\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::down-arrow {\n"
                                         "    image: url(assets/down_arrow_light.png);\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::down-arrow:on,\n"
                                         "QComboBox::down-arrow:hover,\n"
                                         "QComboBox::down-arrow:focus {\n"
                                         "    image: url(assets/down_arrow_lighter.png);\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox QAbstractItemView {\n"
                                         "    color: #ffffff;\n"
                                         "    background-color: #828282;\n"
                                         "    border-radius: 3px;\n"
                                         "    margin: 0px;\n"
                                         "    padding: 0px;\n"
                                         "    border: none;\n"
                                         "    min-height: 30px;\n"
                                         "}\n"
                                         "")
            self.combo_box.setObjectName("combo_box")
            self.combo_box.setMaximumWidth(140)
            self.combo_box.setMaximumHeight(30)
            self.combo_box.addItems(["Tidak Efisien", "Efisien"])
            query = """SELECT id_metode,nilai FROM tbl_metode WHERE id_metode = {0}""".format(
                astar[i]["id_metode"])
            result = db.get_manual_query(query)[0]
            result = dict(result)
            self.combo_box.setCurrentIndex(result["nilai"])
            self.combo_box.setEditable(False)
            self.combo_box.currentIndexChanged.connect(
                lambda e, x=astar[i]["id_metode"]: self.getValuePresepsiT(x, e))
            w = QtWidgets.QWidget()
            hLayout = QtWidgets.QHBoxLayout()
            hLayout.addWidget(self.combo_box)
            hLayout.setContentsMargins(0, 0, 0, 0)
            hLayout.setAlignment(self.combo_box, QtCore.Qt.AlignCenter)
            w.setLayout(hLayout)
            self.table_prespsi_astar.setCellWidget(i, 4, w)

        for i in range(len(improve)):
            self.table_prespsi_improv.insertRow(i)
            self.table_prespsi_improv.setRowHeight(i, 40)
            x = improve[i]["x"]
            y = improve[i]["y"]
            fCost = improve[i]["fScore"]
            x = round(x, 5)
            y = round(y, 5)
            fCost = round(fCost, 5)

            pos = [str(i+1) + ".", x, y, fCost]
            for j in range(len(pos)):
                self.table_prespsi_improv.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(pos[j])))
                self.table_prespsi_improv.item(
                    i, j).setTextAlignment(QtCore.Qt.AlignCenter)

        row = self.table_prespsi_astar.rowHeight(0)
        row = row * (len(astar) + 1) - 13
        self.table_prespsi_astar.setMinimumHeight(row)
        row = self.table_prespsi_improv.rowHeight(0)
        row = row * (len(improve) + 1) - 13
        self.table_prespsi_improv.setMinimumHeight(row)

    def getValuePresepsiT(self, id, e):
        query = """UPDATE tbl_metode SET nilai = {0} WHERE id_metode = {1}""".format(
            e, id)
        db.get_manual_query(query)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.label.setText(_translate(
            "window", "<strong>Path Planning</strong>"))
        self.label_2.setText(_translate(
            "window", "<small>Politeknik Negeri Malang</small>"))
        self.labelCore.setText(_translate("window", "Core App"))
        self.labelSocket.setText(_translate("window", "Socket UDP"))
        self.labelHistory.setText(_translate("window", "History Path"))
        self.labelTesting.setText(_translate("window", "Testing"))
        self.labelPage.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Main App</span></p></body></html>"))
        self.labelDescPage.setText(_translate(
            "window", "Tampilan Utama Path Planning Apps"))
        self.label_14.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Update Posisi</span></p></body></html>"))
        self.label_26.setText(_translate("window", "Obstacle"))
        self.descServer_10.setText(_translate("window", "Robot Lawan"))
        self.label_27.setText(_translate("window", "End Point"))
        self.descServer_11.setText(_translate("window", "Titik Tujuan"))
        self.label_18.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Waktu Metode</span></p></body></html>"))
        self.label_30.setText(_translate("window", "Waktu Sampel"))
        self.astar_start.setText(_translate("window", "Time : -"))
        self.label_28.setText(_translate("window", "Path A*"))
        self.path_astar.setText(_translate("window", "0"))
        self.label_31.setText(_translate("window", "Path Improved A*"))
        self.path_imAstar.setText(_translate("window", "0"))
        self.label_9.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Tampilan Simulasi</span></p></body></html>"))
        self.btnStartSim.setText(_translate("window", "Start Simulasi"))
        self.label_15.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Informasi Path Planning</span></p></body></html>"))
        self.label_32.setText(_translate("window", "End Point"))
        self.astar_start_2.setText(_translate("window", "Titik Tujuan Robot"))
        self.label_33.setText(_translate("window", "Obstacle"))
        self.astar_start_3.setText(_translate("window", "Robot Lawan"))
        self.label_34.setText(_translate("window", "Node A*"))
        self.astar_start_4.setText(_translate("window", "Node Algoritma A*"))
        self.label_35.setText(_translate("window", "Node Improved A*"))
        self.astar_start_5.setText(_translate(
            "window", "Node Algoritma Improved A*"))
        self.label_39.setText(_translate("window", "Robot Asli"))
        self.astar_start_9.setText(_translate(
            "window", "Robot Asli Path Planning"))
        self.label_36.setText(_translate("window", "Node Success"))
        self.astar_start_6.setText(_translate(
            "window", "Node yang berhasil dilalui"))
        self.label_4.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Koneksi Socket UDP</span></p></body></html>"))
        self.groupPortSocket.setTitle(
            _translate("window", "Port Server UDP Socket"))
        self.linePortSocket.setPlaceholderText(
            _translate("window", "Port Socket Server"))
        self.btnSocketConn.setText(_translate("window", "Connect"))
        self.label_10.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Status Socket UDP</span></p></body></html>"))
        self.label_11.setText(_translate("window", "Server Conected"))
        self.descServer.setText(_translate("window", "Start : -"))
        self.label_13.setText(_translate("window", "Robot Obstacle"))
        self.descObs.setText(_translate("window", "Total : 0"))
        self.label_5.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">LIst User Socket Conection UDP</span></p></body></html>"))
        self.label_3.setText(_translate("window", "IP Address"))
        self.label_6.setText(_translate("window", "Status Robot"))
        self.label_7.setText(_translate("window", "Waktu Koneksi"))
        self.label_8.setText(_translate("window", "Detail"))
        self.label_17.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">History Percobaan Sistem Path Planning</span></p></body></html>"))
        self.label_19.setText(_translate("window", "No"))
        self.label_20.setText(_translate("window", "Mode Percobaan"))
        self.label_21.setText(_translate("window", "Waktu Percobaan"))
        self.label_22.setText(_translate("window", "Detail"))
        self.history_id.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">History Percobaan Path Planning ID: -</span></p></body></html>"))
        self.label_44.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Akurasi Metode</span></p></body></html>"))
        self.label_45.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Persepsi Manusia</span></p></body></html>"))
        self.label_59.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Pemilihan Model Akurasi</span></p></body></html>"))
        self.btn_vAkruasi.setText(_translate("window", "Lihat Akurasi"))
        self.label_60.setText(_translate("window", "No"))
        self.label_61.setText(_translate("window", "Mode Percobaan"))
        self.label_62.setText(_translate("window", "Waktu Percobaan"))
        self.label_63.setText(_translate("window", "Status Tabrakan"))
        self.label_64.setText(_translate("window", "Detail"))
        self.label_55.setText(_translate("window", "No"))
        self.label_56.setText(_translate("window", "Mode Percobaan"))
        self.label_57.setText(_translate("window", "Waktu Percobaan"))
        self.label_58.setText(_translate("window", "Detail"))
        self.presepsi_id.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Pengujian Percobaan Path Planning ID: -</span></p></body></html>"))
        self.presepsi_id_3.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Persepsi Algoritma A*</span></p></body></html>"))
        item = self.table_prespsi_astar.horizontalHeaderItem(0)
        item.setText(_translate("window", "no"))
        item = self.table_prespsi_astar.horizontalHeaderItem(1)
        item.setText(_translate("window", "x"))
        item = self.table_prespsi_astar.horizontalHeaderItem(2)
        item.setText(_translate("window", "y"))
        item = self.table_prespsi_astar.horizontalHeaderItem(3)
        item.setText(_translate("window", "f(cost)"))
        item = self.table_prespsi_astar.horizontalHeaderItem(4)
        item.setText(_translate("window", "status"))
        self.presepsi_id_2.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Persepsi Algoritma Improved A*</span></p></body></html>"))
        self.groupPortSocket_2.setTitle(_translate(
            "window", "Total Path Improved A* Yang Efisien"))
        self.txt_efisien_presepsi.setPlaceholderText(
            _translate("window", "Jumlah Path Efisien"))
        self.btn_submit_prespsi.setText(_translate("window", "Simpan"))
        item = self.table_prespsi_improv.horizontalHeaderItem(0)
        item.setText(_translate("window", "no"))
        item = self.table_prespsi_improv.horizontalHeaderItem(1)
        item.setText(_translate("window", "x"))
        item = self.table_prespsi_improv.horizontalHeaderItem(2)
        item.setText(_translate("window", "y"))
        item = self.table_prespsi_improv.horizontalHeaderItem(3)
        item.setText(_translate("window", "f(cost)"))
        self.history_id_2.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Akurasi Presepsi Manusia Terhadap Algoritma Path Planning</span></p></body></html>"))
        self.history_id_3.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Akurasi Metode Improved A* Terhadap Tabrakan</span></p></body></html>"))
        self.history_id_4.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Status Jalur Percobaan Improved A* : </span></p></body></html>"))
        self.history_id_5.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Akurasi Metode Improved A* terhadap Tabrakan</span></p></body></html>"))
        self.label_42.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Pemilihan Fungsi Biaya</span></p></body></html>"))
        self.label_43.setText(_translate("window", "Pemilihan <i>f(cost)</i>"))
        self.label_12.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Pemilihan Metode</span></p></body></html>"))
        self.label_23.setText(_translate("window", "Simulasi"))
        self.descServer_7.setText(_translate("window", "Simulasi Metode"))
        self.label_24.setText(_translate("window", "Hardware"))
        self.descServer_8.setText(_translate("window", "Simulasi Hardware"))
        self.label_16.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Posisi Robot Aktif</span></p></body></html>"))
        self.label_25.setText(_translate("window", "Posisi Koordinat X"))
        self.coor_x.setText(_translate("window", "X: 0 m."))
        self.label_29.setText(_translate("window", "Posisi Koordinat Y"))
        self.coor_y.setText(_translate("window", "Y: 0 m."))
        self.label_37.setText(_translate("window", "Posisi Koordinat Z"))
        self.coor_z.setText(_translate("window", "Z: 0"))


class TaskQuit(QtCore.QThread):

    key = QtCore.pyqtSignal(int)

    def __init__(self):
        super(TaskQuit, self).__init__()
        window = QtWidgets.QMainWindow()
        self.window = window
        window.setObjectName("window")
        window.resize(455, 175)
        window.setMinimumSize(QtCore.QSize(455, 175))
        window.setMaximumSize(QtCore.QSize(455, 175))
        window.setSizeIncrement(QtCore.QSize(0, 0))
        self.widgetMain = QtWidgets.QWidget(window)
        self.widgetMain.setStyleSheet("")
        self.widgetMain.setObjectName("widgetMain")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgetMain)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.widgetMain)
        self.frame.setStyleSheet("QFrame{\n"
                                 "    background-color:rgb(20,20,20);\n"
                                 "    border:0.50px solid rgb(215,215,215);\n"
                                 "    border-radius:20px;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("QFrame {\n"
                                   "    border:none;\n"
                                   "    background:transparent;\n"
                                   "}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setStyleSheet("QFrame {\n"
                                   "    background-color:rgb(44,44,44);\n"
                                   "    border-bottom-left-radius:0px;\n"
                                   "    border-bottom-right-radius:0px;\n"
                                   "}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_10.setMaximumSize(QtCore.QSize(30, 30))
        self.frame_10.setStyleSheet("QFrame {\n"
                                    "    background-color:transparent;\n"
                                    "    border-image: url(\"./assets/icon.png\") 0 0 0 0 strecth strecth;\n"
                                    "border-width:0px 0.75px 0px 0.75px\n"
                                    "}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout.addWidget(self.frame_10)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QFrame{\n"
                                   "    color:rgb(215,215,215);\n"
                                   "    background:transparent;\n"
                                   "    padding-left:0.5px;\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.btnCancel = QtWidgets.QPushButton(self.frame_3)
        self.btnCancel.setMinimumSize(QtCore.QSize(40, 40))
        self.btnCancel.setMaximumSize(QtCore.QSize(40, 40))
        self.btnCancel.setStyleSheet("QPushButton {\n"
                                     "    background-color:transparent;\n"
                                     "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width:8px 9px 8px 9px\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.btnCancel.setText("")
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setContentsMargins(12, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setMaximumSize(QtCore.QSize(40, 35))
        self.frame_5.setStyleSheet("QFrame {\n"
                                   "    background-color:transparent;\n"
                                   "    border-image: url(\"./assets/close_circle.png\") 0 0 0 0 strecth strecth;\n"
                                   "border-width:1.15px 4px 1.15px 4px;\n"
                                   "}")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3.addWidget(self.frame_5)
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(19)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QFrame{\n"
                                   "    color:rgb(215,215,215);\n"
                                   "    background:transparent;\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.verticalLayout_4.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setContentsMargins(25, 0, 25, 20)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnNo = QtWidgets.QPushButton(self.frame_7)
        self.btnNo.setMinimumSize(QtCore.QSize(0, 40))
        self.btnNo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.btnNo.setFont(font)
        self.btnNo.setStyleSheet("QPushButton {\n"
                                 "    background:transparent;\n"
                                 "    border: 1.5px solid rgb(215,215,215);\n"
                                 "    border-radius:7.5px;\n"
                                 "    color:rgb(215,215,215);\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover{\n"
                                 "    color:rgba(20,20,20,235);\n"
                                 "    background-color:rgb(215,215,215);\n"
                                 "    border:none;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:pressed{\n"
                                 "    background-color:rgb(28,28,28);\n"
                                 "    color:rgb(215,215,215);\n"
                                 "    border: 1.5px solid rgb(215,215,215);\n"
                                 "}\n"
                                 "")
        self.btnNo.setObjectName("btnNo")
        self.horizontalLayout_2.addWidget(self.btnNo)
        self.btnYes = QtWidgets.QPushButton(self.frame_7)
        self.btnYes.setMinimumSize(QtCore.QSize(0, 40))
        self.btnYes.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.btnYes.setFont(font)
        self.btnYes.setStyleSheet("QPushButton {\n"
                                  "    background:transparent;\n"
                                  "    border: 1.5px solid rgb(215,215,215);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(215,215,215);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:hover{\n"
                                  "    color:rgba(20,20,20,235);\n"
                                  "    background-color:rgb(215,215,215);\n"
                                  "    border:none;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:rgb(28,28,28);\n"
                                  "    color:rgb(215,215,215);\n"
                                  "    border: 1.5px solid rgb(215,215,215);\n"
                                  "}\n"
                                  "")
        self.btnYes.setObjectName("btnYes")
        self.horizontalLayout_2.addWidget(self.btnYes)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame)
        window.setCentralWidget(self.widgetMain)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.posEvent = [0, 0, 1]
        self.btnEvent = [self.btnCancel, self.btnNo, self.btnYes]

        for i in range(len(self.btnEvent)):
            self.btnEvent[i].setCursor(
                QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btnEvent[i].clicked.connect(
                lambda _, x=self.posEvent[i]: self.returnEvent(x))

    def returnEvent(self, pos):
        self.key.emit(pos)
        if(pos == 0):
            self.window.close()
        else:
            if(ui.lock > 0 and db.last_id > 0):
                db.delete_data("tbl_percobaan", "id_percobaan", db.last_id)
            self.window.close()
            os._exit(os.EX_OK)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.label_2.setText(_translate(
            "window", "<strong>Keluar Aplikasi ?</strong>"))
        self.label_3.setText(_translate(
            "window", "<small>Apakah kamu ingin keluar dari aplikasi ?</small>"))
        self.btnNo.setText(_translate("window", "No"))
        self.btnYes.setText(_translate("window", "Yes"))


class Astar(QtCore.QThread):

    node_search = QtCore.pyqtSignal(object, int)
    lock_key = QtCore.pyqtSignal(int, object)

    def __init__(self):
        super(Astar, self).__init__()
        self.path = []
        self.mode_fCost = 0

    def set_fCost(self, mode):
        self.mode_fCost = mode

    @QtCore.pyqtSlot()
    def run(self):
        last_time = time.time()
        self.path = []

        self.dir_row = [-0.5, -0.5, 0, +0.5, +0.5, +0.5, 0, -0.5]
        self.dir_col = [0, +0.5, +0.5, +0.5, 0, -0.5, -0.5, -0.5]

        self.cameFrom = {}

        self.startP = classKirim.start
        self.endP = classKirim.end
        # print(self.startP, self.endP)

        self.gScore = {self.startP: 0}
        self.fScore = {self.startP: self.heuristic(self.startP, self.endP)}
        self.openSet = []
        self.closedSet = set()
        self.openSet.append((self.startP, self.fScore[self.startP]))

        self.isLoop = 0

        fin = np.array(self.endP) - np.array(self.startP)
        fin = np.linalg.norm(fin)
        self.isCounter = [-1, len(self.path)]
        self.isIncrement = 0
        self.counter()

        if(fin <= 1.5):
            self.isLoop = 1
            self.path = [self.endP]
            tentative_gscore = self.gScore[self.startP] + \
                self.heuristic(self.startP, self.endP)
            self.fScore[self.endP] = tentative_gscore + \
                self.heuristic(self.startP, self.endP)

            classKirim.timer[0] = time.time() - last_time

            for i in range(2):
                self.isCounter = [i, len(self.path)]
                self.counter()
                self.isIncrement = i
                self.emitData()
        else:
            self.cond_break = False
            # Jarak Aman Terhadap Obstacle
            # enorm_locking = 0.6375 #0.75  # 0.6375
            enorm_locking = 0.70  # 75  # 0.75  # 0.75  # 0.6375
            # Jarak Minimum Terhadap Titik Tujuan Akhir
            erfin = 0.75

            while(self.isLoop == 0):
                if(len(self.openSet) > 0):
                    self.openSet.sort(reverse=False, key=lambda idx: idx[1])
                    cur = self.openSet.pop(0)[0]

                    fin = np.array(self.endP) - np.array(cur)
                    fin = np.linalg.norm(fin)
                    if(fin <= erfin):
                        self.cond_break = True

                    if(self.cond_break == True):
                        self.path = []
                        last_neighbour = cur
                        # Proses Looping Path A*
                        while(cur in self.cameFrom):
                            self.path.append(cur)
                            cur = self.cameFrom[cur]
                        self.path = self.path[::-1]
                        last_path = self.path[-1]
                        enorm_finish = np.array(
                            self.endP) - np.array(last_path)
                        enorm_error = np.linalg.norm(enorm_finish)
                        if(enorm_error <= 0.1975):
                            self.path.pop(len(self.path) - 1)
                        self.path += [self.endP]
                        self.isLoop = 1
                        tentative_gscore = self.gScore[last_neighbour] + \
                            self.heuristic(last_neighbour, self.endP)
                        self.fScore[self.endP] = tentative_gscore + \
                            self.heuristic(last_neighbour, self.endP)
                    else:
                        self.closedSet.add(cur)

                        for i in range(len(self.dir_col)):
                            rr = cur[0] + self.dir_row[i]
                            cc = cur[1] + self.dir_col[i]
                            neighbor = (rr, cc)

                            if(rr < 0 or cc < 0):
                                continue
                            if(rr > classKirim.maxX or cc > classKirim.maxY):
                                continue

                            # Perhitungan Jarak Terhadap Obstacle
                            conditional = False
                            obs_total = classKirim.obs
                            if(classKirim.isActiveSimulasi == 1):
                                obs_total = classKirim.obs + classKirim.obsO
                            for obs in obs_total:
                                new_point = np.array(obs)
                                now_node = np.array(neighbor)
                                enorm = new_point - now_node
                                enorm = np.linalg.norm(enorm)
                                if(enorm <= enorm_locking):
                                    conditional = True
                                    break

                            if(conditional):
                                continue

                            tentative_gscore = self.gScore[cur] + \
                                self.heuristic(cur, neighbor)

                            if(neighbor in self.closedSet and tentative_gscore >= self.gScore.get(neighbor, 0)):
                                continue

                            if(tentative_gscore < self.gScore.get(neighbor, 0) or neighbor not in [idx[0] for idx in self.openSet]):
                                self.cameFrom[neighbor] = cur
                                self.gScore[neighbor] = tentative_gscore
                                self.fScore[neighbor] = tentative_gscore + \
                                    self.heuristic(neighbor, self.endP)
                                self.openSet.append(
                                    (neighbor, self.fScore[neighbor]))
                else:
                    self.isLoop = -1
            else:
                # Norm Path
                self.emitData()
                self.isIncrement += 1
                if(self.isLoop == 1):
                    self.isCounter = [0, len(self.path)]
                    self.counter()
                    if(len(self.path) > 1):
                        improved = ImprovedAstar(self.path)
                        self.path = improved.path_normalize()
                    else:
                        self.path = [self.endP]
                    classKirim.timer[0] = time.time() - last_time
                    self.isCounter = [1, len(self.path)]
                    self.counter()
                self.emitData()
                #print(round(classKirim.timer[0], 5))

    @QtCore.pyqtSlot()
    def emitData(self):
        self.node_search.emit(self.path, self.isIncrement)

    @QtCore.pyqtSlot()
    def counter(self):
        self.lock_key.emit(self.isLoop, self.isCounter)

    def heuristic(self, start, end):
        start = np.array(start)
        end = np.array(end)

        res = 0.
        if(self.mode_fCost == 0):
            # Manhattan Distance
            res = np.sum(np.abs(end - start))
        elif(self.mode_fCost == 1):
            # Euclidiance Distance
            res = np.sqrt(np.sum((end - start)**2))

        return res


class ImprovedAstar():
    def __init__(self, path):
        # Jarak Aman Obstacle
        # self.error_obs = 0.6375 #0.810  # 0.6375 #0.810  # 0.825  # 0.6375
        self.error_obs = 0.675  # 375 #0.810

        self.startP = classKirim.start
        self.endP = classKirim.end
        self.last_path = copy(path)
        self.inc = 0
        self.new_path = [self.startP]
        self.length = len(self.last_path)
        self.last_inc = 0

    def path_normalize(self):
        while(self.inc < self.length):
            new_len = len(self.new_path) - 1
            start_point = self.new_path[new_len]
            end_point = self.last_path[self.inc]
            counter = self.dda_algorithm(start_point, end_point)
            if(counter):
                if(self.inc == 0 or self.last_inc == self.inc):
                    self.inc += 1

                new_node = self.last_path[self.inc - 1]
                self.new_path.append(new_node)
                self.inc = len(self.last_path) - \
                    (len(self.last_path) - self.inc)
                self.last_inc = self.inc
            else:
                self.inc += 1
        else:
            self.new_path.pop(0)
            self.new_path += [self.endP]
        return self.new_path

    def dda_algorithm(self, start_pt, end_pt):
        try:
            condition = False

            x1, y1 = start_pt
            x2, y2 = end_pt

            dx = x2-x1
            dy = y2-y1

            step = 0
            if(abs(dx) > abs(dy)):
                step = abs(dx)
            else:
                step = abs(dy)

            step = np.rint(step).astype(int)
            if(step <= 0.):
                step = 1

            xinc = dx/step
            yinc = dy/step

            for _ in range(step):
                x1 += xinc
                y1 += yinc
                point = (x1, y1)
                obs_total = classKirim.obs
                if(classKirim.isActiveSimulasi == 1):
                    obs_total = classKirim.obs + classKirim.obsO

                for obs in obs_total:
                    new_obs = np.array(obs)
                    new_point = np.array(point)
                    err = new_obs - new_point
                    err = np.linalg.norm(err)
                    if(err <= self.error_obs):
                        condition = True
                        break

            return condition
        except Exception as e:
            print(e)
            self.new_path.append(start_pt)


class MsgError(QtCore.QThread):

    key = QtCore.pyqtSignal(int)

    def __init__(self):
        super(MsgError, self).__init__()
        window = QtWidgets.QMainWindow()
        self.window = window
        self.msg = ""
        window.setObjectName("window")
        window.resize(455, 175)
        window.setMinimumSize(QtCore.QSize(455, 175))
        window.setMaximumSize(QtCore.QSize(455, 175))
        window.setSizeIncrement(QtCore.QSize(0, 0))
        self.widgetMain = QtWidgets.QWidget(window)
        self.widgetMain.setStyleSheet("")
        self.widgetMain.setObjectName("widgetMain")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgetMain)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.widgetMain)
        self.frame.setStyleSheet("QFrame{\n"
                                 "    background-color:rgb(20,20,20);\n"
                                 "    border:0.50px solid rgb(215,215,215);\n"
                                 "    border-radius:20px;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("QFrame {\n"
                                   "    border:none;\n"
                                   "    background:transparent;\n"
                                   "}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setStyleSheet("QFrame {\n"
                                   "    background-color:rgb(44,44,44);\n"
                                   "    border-bottom-left-radius:0px;\n"
                                   "    border-bottom-right-radius:0px;\n"
                                   "}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_10.setMaximumSize(QtCore.QSize(30, 30))
        self.frame_10.setStyleSheet("QFrame {\n"
                                    "    background-color:transparent;\n"
                                    "    border-image: url(\"./assets/icon.png\") 0 0 0 0 strecth strecth;\n"
                                    "border-width:0px 0.75px 0px 0.75px\n"
                                    "}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout.addWidget(self.frame_10)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QFrame{\n"
                                   "    color:rgb(215,215,215);\n"
                                   "    background:transparent;\n"
                                   "    padding-left:0.5px;\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.btnCancel = QtWidgets.QPushButton(self.frame_3)
        self.btnCancel.setMinimumSize(QtCore.QSize(40, 40))
        self.btnCancel.setMaximumSize(QtCore.QSize(40, 40))
        self.btnCancel.setStyleSheet("QPushButton {\n"
                                     "    background-color:transparent;\n"
                                     "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width:8px 9px 8px 9px\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.btnCancel.setText("")
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setContentsMargins(12, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setMaximumSize(QtCore.QSize(40, 35))
        self.frame_5.setStyleSheet("QFrame {\n"
                                   "    background-color:transparent;\n"
                                   "    border-image: url(\"./assets/warning_circle.png\") 0 0 0 0 strecth strecth;\n"
                                   "border-width:1.15px 4px 1.15px 4px;\n"
                                   "}")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3.addWidget(self.frame_5)
        self.msgLabel = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(19)
        self.msgLabel.setFont(font)
        self.msgLabel.setStyleSheet("QFrame{\n"
                                    "    color:rgb(215,215,215);\n"
                                    "    background:transparent;\n"
                                    "}")
        self.msgLabel.setObjectName("msgLabel")
        self.horizontalLayout_3.addWidget(self.msgLabel)
        self.verticalLayout_4.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setContentsMargins(25, 0, 25, 20)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnOk = QtWidgets.QPushButton(self.frame_7)
        self.btnOk.setMinimumSize(QtCore.QSize(70, 40))
        self.btnOk.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.btnOk.setFont(font)
        self.btnOk.setStyleSheet("QPushButton {\n"
                                 "    background:transparent;\n"
                                 "    border: 1.5px solid rgb(215,215,215);\n"
                                 "    border-radius:7.5px;\n"
                                 "    color:rgb(215,215,215);\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover{\n"
                                 "    color:rgba(20,20,20,235);\n"
                                 "    background-color:rgb(215,215,215);\n"
                                 "    border:none;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:pressed{\n"
                                 "    background-color:rgb(28,28,28);\n"
                                 "    color:rgb(215,215,215);\n"
                                 "    border: 1.5px solid rgb(215,215,215);\n"
                                 "}\n"
                                 "")
        self.btnOk.setObjectName("btnOk")
        self.horizontalLayout_2.addWidget(self.btnOk)
        self.verticalLayout_4.addWidget(self.frame_7, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame)
        window.setCentralWidget(self.widgetMain)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.btn = [self.btnCancel, self.btnOk]
        for i in range(len(self.btn)):
            self.btn[i].clicked.connect(lambda _, x=True: self.eventBtn(x))
            self.btn[i].setCursor(
                QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def eventBtn(self, e):
        self.key.emit(not(e))
        if(e == True):
            self.window.close()

    def setMsg(self, msg):
        self.msg = msg
        self.retranslateUi(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.label_2.setText(_translate(
            "window", "<html><head/><body><p><span style=\" font-weight:600;\">Pesan Peringatan !!!</span></p></body></html>"))
        self.btnOk.setText(_translate("window", "OK"))
        self.msgLabel.setText(_translate(
            "window", "<small>{}</small>").format(self.msg))


class KinematicsRobot(QtCore.QThread):

    realT_node = QtCore.pyqtSignal(object, int)

    def __init__(self):
        super(KinematicsRobot, self).__init__()
        self.alp = np.array(
            [np.radians(140.), np.radians(-140.), np.radians(-40.), np.radians(40.)])
        self.gamma = np.array([np.radians(50.), np.radians(
            130.), np.radians(-130.), np.radians(-50.)])
        self.l = 0.215
        self.r = 0.05
        self.Kp = 1.5
        self.Ts = 0.1
        self.node_awal = np.matrix([[0., 0., np.radians(0.)]]).T
        self.node_akhir = np.matrix([[0., 0., np.radians(0.)]]).T
        self.Ji = self.get_invers_jacobian()
        self.last_x = 0.
        self.last_y = 0.
        self.reset_variable()

    def reset_variable(self):
        self.last_x = 0.
        self.last_y = 0.
        self.length = 0
        self.counter = 0
        self.path = []
        self.node_awal = np.matrix([[0., 0., np.radians(0.)]]).T
        self.node_akhir = np.matrix([[0., 0., np.radians(0.)]]).T

    def get_invers_jacobian(self):
        Ji = np.matrix([[0., 0., 0.], [0., 0., 0.],
                        [0., 0., 0.], [0., 0., 0.]])
        Ji[0, 0] = np.cos(self.alp[0])
        Ji[0, 1] = np.sin(self.alp[0])
        Ji[0, 2] = (self.l*np.cos(self.gamma[0])*np.sin(self.alp[0])) - \
            (self.l*np.sin(self.gamma[0])*np.cos(self.alp[0]))
        Ji[1, 0] = np.cos(self.alp[1])
        Ji[1, 1] = np.sin(self.alp[1])
        Ji[1, 2] = (self.l*np.cos(self.gamma[1])*np.sin(self.alp[1])) - \
            (self.l*np.sin(self.gamma[1])*np.cos(self.alp[1]))
        Ji[2, 0] = np.cos(self.alp[2])
        Ji[2, 1] = np.sin(self.alp[2])
        Ji[2, 2] = (self.l*np.cos(self.gamma[2])*np.sin(self.alp[2])) - \
            (self.l*np.sin(self.gamma[2])*np.cos(self.alp[2]))
        Ji[3, 0] = np.cos(self.alp[3])
        Ji[3, 1] = np.sin(self.alp[3])
        Ji[3, 2] = (self.l*np.cos(self.gamma[3])*np.sin(self.alp[3])) - \
            (self.l*np.sin(self.gamma[3])*np.cos(self.alp[3]))
        return Ji/self.r

    def get_invers_jacobianW(self, Ji, theta):
        rot = np.matrix([[np.cos(theta), np.sin(theta), 0.],
                         [-np.sin(theta), np.cos(theta), 0.],
                         [0., 0., 1.]])
        return Ji*rot

    def setPose(self, path):
        self.reset_variable()
        self.path = path
        node_awal = classKirim.start
        self.node_awal[0, 0] = node_awal[0]
        self.node_awal[1, 0] = node_awal[1]
        self.length = len(self.path)

    @QtCore.pyqtSlot()
    def run(self):
        self.indexs = 0
        self.lock = 0
        self.last_counter = -1
        while(self.counter < self.length and classKirim.isActiveSimulasi == 0):
            end_node = self.path[self.counter]
            self.node_akhir[0, 0] = end_node[0]
            self.node_akhir[1, 0] = end_node[1]
            if(self.last_x != self.node_awal[0, 0] or self.last_y != self.node_awal[1, 0]):
                self.last_x = self.node_awal[0, 0]
                self.last_y = self.node_awal[1, 0]
                temp = [(self.node_awal[0, 0], self.node_awal[1, 0],
                         self.node_awal[2, 0])]
                db.insert_data("tbl_history", temp)

            Jinv = self.get_invers_jacobianW(self.Ji, self.node_awal[2, 0])
            J = np.linalg.pinv(Jinv)
            error = self.node_akhir - self.node_awal
            enorm = np.linalg.norm(error)
            w = Jinv*(self.Kp*error)

            e_lock = 0.
            if(self.counter < self.length - 1):
                if(self.last_counter < self.counter or self.last_counter != self.counter):
                    self.last_counter = self.counter
                e_lock = 0.075
            else:
                if(self.lock == 0):
                    self.lock = 1
                e_lock = 0.0075

            if(enorm < e_lock):
                self.counter += 1

            x_dot = J * w

            self.node_awal[0, 0] = self.node_awal[0, 0] + x_dot[0, 0]*self.Ts
            self.node_awal[1, 0] = self.node_awal[1, 0] + x_dot[1, 0]*self.Ts
            self.node_awal[2, 0] = self.node_awal[2, 0] + x_dot[2, 0]*self.Ts

            self.indexs += 1
            self.realT_node.emit(self.node_awal, self.counter)
            time.sleep(0.1)
        else:
            self.realT_node.emit(None, -1)
            self.reset_variable()


class KirimCond():
    def __init__(self):
        super(KirimCond, self).__init__()
        self.isActiveSimulasi = 0
        self.start = (0., 0.)
        self.end = (0., 0.)
        self.obs = []
        self.robotMax = 3
        self.maxX = 9
        self.maxY = 6
        self.cImgBall = [0., 0.]
        self.cImgRobot = [0., 0.]
        self.isLoopUDP = 0
        self.checkMaster = [-1, 0]
        self.obsO = []
        self.command = 0
        self.timer = [0.]
        self.radius = 18


class QuestionTask(QtCore.QThread):

    key = QtCore.pyqtSignal(int)

    def __init__(self):
        super(QuestionTask, self).__init__()
        self.msg = ""
        window = QtWidgets.QMainWindow()
        self.window = window
        window.setObjectName("window")
        window.resize(455, 175)
        window.setMinimumSize(QtCore.QSize(455, 175))
        window.setMaximumSize(QtCore.QSize(455, 175))
        window.setSizeIncrement(QtCore.QSize(0, 0))
        self.widgetMain = QtWidgets.QWidget(window)
        self.widgetMain.setStyleSheet("")
        self.widgetMain.setObjectName("widgetMain")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgetMain)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.widgetMain)
        self.frame.setStyleSheet("QFrame{\n"
                                 "    background-color:rgb(20,20,20);\n"
                                 "    border:0.50px solid rgb(215,215,215);\n"
                                 "    border-radius:20px;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("QFrame {\n"
                                   "    border:none;\n"
                                   "    background:transparent;\n"
                                   "}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setStyleSheet("QFrame {\n"
                                   "    background-color:rgb(44,44,44);\n"
                                   "    border-bottom-left-radius:0px;\n"
                                   "    border-bottom-right-radius:0px;\n"
                                   "}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_10.setMaximumSize(QtCore.QSize(30, 30))
        self.frame_10.setStyleSheet("QFrame {\n"
                                    "    background-color:transparent;\n"
                                    "    border-image: url(\"./assets/msg_err.png\") 0 0 0 0 strecth strecth;\n"
                                    "border-width:0px 0.75px 0px 0.75px\n"
                                    "}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout.addWidget(self.frame_10)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QFrame{\n"
                                   "    color:rgb(215,215,215);\n"
                                   "    background:transparent;\n"
                                   "    padding-left:0.5px;\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.btnCancel = QtWidgets.QPushButton(self.frame_3)
        self.btnCancel.setMinimumSize(QtCore.QSize(40, 40))
        self.btnCancel.setMaximumSize(QtCore.QSize(40, 40))
        self.btnCancel.setStyleSheet("QPushButton {\n"
                                     "    background-color:transparent;\n"
                                     "    border-image: url(\"./assets/close_grey.png\") 0 0 0 0 strecth strecth;\n"
                                     "    border-width:8px 9px 8px 9px\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    border-image: url(\"./assets/close_white.png\") 0 0 0 0 strecth strecth;\n"
                                     "}")
        self.btnCancel.setText("")
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setContentsMargins(12, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setMaximumSize(QtCore.QSize(40, 35))
        self.frame_5.setStyleSheet("QFrame {\n"
                                   "    background-color:transparent;\n"
                                   "    border-image: url(\"./assets/msg_err.png\") 0 0 0 0 strecth strecth;\n"
                                   "border-width:1.15px 4px 1.15px 4px;\n"
                                   "}")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3.addWidget(self.frame_5)
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(19)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QFrame{\n"
                                   "    color:rgb(215,215,215);\n"
                                   "    background:transparent;\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.verticalLayout_4.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setContentsMargins(25, 0, 25, 20)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnNo = QtWidgets.QPushButton(self.frame_7)
        self.btnNo.setMinimumSize(QtCore.QSize(0, 40))
        self.btnNo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.btnNo.setFont(font)
        self.btnNo.setStyleSheet("QPushButton {\n"
                                 "    background:transparent;\n"
                                 "    border: 1.5px solid rgb(215,215,215);\n"
                                 "    border-radius:7.5px;\n"
                                 "    color:rgb(215,215,215);\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover{\n"
                                 "    color:rgba(20,20,20,235);\n"
                                 "    background-color:rgb(215,215,215);\n"
                                 "    border:none;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:pressed{\n"
                                 "    background-color:rgb(28,28,28);\n"
                                 "    color:rgb(215,215,215);\n"
                                 "    border: 1.5px solid rgb(215,215,215);\n"
                                 "}\n"
                                 "")
        self.btnNo.setObjectName("btnNo")
        self.horizontalLayout_2.addWidget(self.btnNo)
        self.btnYes = QtWidgets.QPushButton(self.frame_7)
        self.btnYes.setMinimumSize(QtCore.QSize(0, 40))
        self.btnYes.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.btnYes.setFont(font)
        self.btnYes.setStyleSheet("QPushButton {\n"
                                  "    background:transparent;\n"
                                  "    border: 1.5px solid rgb(215,215,215);\n"
                                  "    border-radius:7.5px;\n"
                                  "    color:rgb(215,215,215);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:hover{\n"
                                  "    color:rgba(20,20,20,235);\n"
                                  "    background-color:rgb(215,215,215);\n"
                                  "    border:none;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed{\n"
                                  "    background-color:rgb(28,28,28);\n"
                                  "    color:rgb(215,215,215);\n"
                                  "    border: 1.5px solid rgb(215,215,215);\n"
                                  "}\n"
                                  "")
        self.btnYes.setObjectName("btnYes")
        self.horizontalLayout_2.addWidget(self.btnYes)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame)
        window.setCentralWidget(self.widgetMain)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.posEvent = [0, 0, 1]
        self.btnEvent = [self.btnCancel, self.btnNo, self.btnYes]

        for i in range(len(self.btnEvent)):
            self.btnEvent[i].setCursor(
                QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btnEvent[i].clicked.connect(
                lambda _, x=self.posEvent[i]: self.returnEvent(x))

    def returnEvent(self, pos):
        self.key.emit(pos)
        self.window.close()

    def setMsg(self, msg):
        self.msg = msg
        self.retranslateUi(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.label_2.setText(_translate(
            "window", "<strong>Pesan Pertanyaan!!</strong>"))
        self.label_3.setText(_translate(
            "window", "<small>{}</small>").format(self.msg))
        self.btnNo.setText(_translate("window", "No"))
        self.btnYes.setText(_translate("window", "Yes"))


class SocketUPDServer(QtCore.QThread):

    client_connect = QtCore.pyqtSignal(object, int)
    hapus_client = QtCore.pyqtSignal(int)
    path_hardware = QtCore.pyqtSignal(object)
    msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SocketUPDServer, self).__init__()
        self.port = 0
        self.server_udp = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.my_ip = []
        self.x_last = float("inf")
        self.y_last = float("inf")

    @QtCore.pyqtSlot()
    def kirimData(self, path):
        self.path = path
        classKirim.command = 1
        self.updateSend(self.path)

    def stopData(self):
        try:
            self.updateSend([])
        except socket.error as e:
            print("Send Stop: ", e)

    @QtCore.pyqtSlot()
    def setServer(self, port):
        self.server_udp = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.my_ip = []
        self.port = port
        self.clientAdd = 0
        self.isLoop = 1
        self.address = []
        self.index = 0
        self.start()

    @QtCore.pyqtSlot()
    def run(self):
        try:
            while(classKirim.isLoopUDP == 1):
                if(classKirim.isActiveSimulasi == 1):
                    if(self.clientAdd == 0):
                        self.server_udp.setsockopt(
                            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        self.server_udp.setsockopt(socket.SOL_SOCKET,
                                                   socket.SO_REUSEPORT, 1)
                        self.server_udp.setsockopt(socket.SOL_SOCKET,
                                                   socket.SO_BROADCAST, 1)
                        self.server_udp.bind(("", self.port))
                        self.clientAdd = 1
                        # self.my_ip = socket.gethostbyname_ex(
                        #     socket.gethostname())[-1]
                    else:
                        data, address = self.server_udp.recvfrom(1024)
                        temp_receive = pickle.loads(data)
                        try:
                            if(address[0] not in self.my_ip):
                                ext = temp_receive["exit"]
                                if(ext == 1):
                                    try:
                                        indeks = self.address.index(address[0])
                                        self.address.pop(indeks)
                                        self.pos = len(self.address)
                                        self.hapus_client.emit(indeks)
                                    except:
                                        pass
                                else:
                                    if(address[0] not in self.address):
                                        self.address.insert(
                                            self.index, address[0])
                                        date = datetime.now()
                                        timestamp = date.strftime(
                                            '%d %B %Y, %H:%M:%S')
                                        client = {
                                            "ip": address[0], "id": "Robot Lawan", "datetime": timestamp}
                                        self.client_connect.emit(
                                            client, self.index)
                                        self.index += 1
                                    if(len(self.address) > 0):
                                        x = temp_receive["pos"][0]
                                        y = temp_receive["pos"][1]
                                        z = temp_receive["pos"][2]

                                        x_transformation = (
                                            classKirim.maxX / 2.) - x
                                        y_transformation = (
                                            classKirim.maxY / 2.) - (y * -1)

                                        temp_receive["pos"] = (
                                            x_transformation, y_transformation, z)

                                        index = self.address.index(address[0])
                                        if(classKirim.checkMaster[0] == index):
                                            if(ui.lock > 0 and (self.x_last != x_transformation or self.y_last != y_transformation)):
                                                db.insert_data("tbl_history", [
                                                               temp_receive["pos"]])
                                                self.x_last = x_transformation
                                                self.y_last = y_transformation

                                        temp_receive["selected"] = index
                                        self.path_hardware.emit(temp_receive)
                        except:
                            pass
            else:
                classKirim.command = 0
                self.updateSend([])
                self.server_udp.close()
                self.clientAdd = 0

        except socket.error as e:
            print(e)
            self.server_udp.close()
            self.msg.emit(str(e))
            self.reset_data()

    @QtCore.pyqtSlot()
    def stopServer(self):
        self.server_udp.close

    def updateSend(self, path):
        msg = {"cmd": classKirim.command, "path": path}
        msg_picke = pickle.dumps(msg)
        self.server_udp.sendto(msg_picke, ('<broadcast>', self.port))

    def reset_data(self):
        self.isLoop = 0
        self.clientAdd = 0
        self.my_ip = []


class SqliteConfigure():
    def __init__(self, file):
        super(SqliteConfigure, self).__init__()
        self.file = file
        self.mydb = None
        self.cursor = None
        self.last_id = 0
        self.connect()

    def connect(self):
        try:
            self.mydb = sqlite3.connect(self.file, check_same_thread=False)
            self.mydb.row_factory = sqlite3.Row
            self.cursor = self.mydb.cursor()
            self.cursor_history = self.mydb.cursor()
            self.cursor_delete = self.mydb.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print("Database Error: ", e)

    def create_table(self):
        try:
            db_percobaan = "CREATE TABLE IF NOT EXISTS tbl_percobaan (id_percobaan INTEGER PRIMARY KEY AUTOINCREMENT, time DATETIME DEFAULT (datetime('now','localtime')), akurasi INTEGER DEFAULT 0, mode VARCHAR(255) NOT NULL)"
            db_start = "CREATE TABLE IF NOT EXISTS tbl_start (id_start INTEGER PRIMARY KEY AUTOINCREMENT, id_percobaan INTEGER, x DOUBLE DEFAULT 0.0, y DOUBLE DEFAULT 0.0, z DOUBLE DEFAULT 0.0, FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"
            db_obstacle = "CREATE TABLE IF NOT EXISTS tbl_obstacle (id_obs INTEGER PRIMARY KEY AUTOINCREMENT, id_percobaan INTEGER, x DOUBLE DEFAULT 0.0, y DOUBLE DEFAULT 0.0, z DOUBLE DEFAULT 0.0, FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"
            db_end = "CREATE TABLE IF NOT EXISTS tbl_end (id_end INTEGER PRIMARY KEY AUTOINCREMENT, id_percobaan INTEGER, x DOUBLE DEFAULT 0.0, y DOUBLE DEFAULT 0.0, z DOUBLE DEFAULT 0.0, FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"
            db_history = "CREATE TABLE IF NOT EXISTS tbl_history (id_history INTEGER PRIMARY KEY AUTOINCREMENT, id_percobaan INTEGER, x DOUBLE DEFAULT 0.0, y DOUBLE DEFAULT 0.0, z DOUBLE DEFAULT 0.0, FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"
            db_metode = "CREATE TABLE IF NOT EXISTS tbl_metode (id_metode INTEGER PRIMARY KEY AUTOINCREMENT, id_percobaan INTEGER, x DOUBLE DEFAULT 0.0, y DOUBLE DEFAULT 0.0, z DOUBLE DEFAULT 0.0, mode VARCHAR(255) NOT NULL, fScore DOUBLE DEFAULT 0.0, mode_fCost VARCHAR(255) NOT NULL, nilai INTEGER DEFAULT 0, FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"
            db_uji_prespsi = "CREATE TABLE IF NOT EXISTS tbl_uji_presepsi (id_presepsi INTEGER PRIMARY KEY AUTOINCREMENT,id_percobaan INTEGER,total_sebenarnya INTEGER DEFAULT 0, total_presepsi INTEGER DEFAULT 0, FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"
            db_waktu_metode = "CREATE TABLE IF NOT EXISTS tbl_waktu (id_waktu INTEGER PRIMARY KEY AUTOINCREMENT,id_percobaan INTEGER,waktu DOUBLE DEFAULT 0,FOREIGN KEY (id_percobaan) REFERENCES tbl_percobaan(id_percobaan) ON DELETE CASCADE ON UPDATE CASCADE)"

            create_db = [db_percobaan, db_start,
                         db_obstacle, db_end, db_history, db_metode, db_uji_prespsi, db_waktu_metode]
            for database in create_db:
                self.cursor.execute(database)
            self.cursor.execute("PRAGMA foreign_keys=ON")
            self.mydb.commit()
        except sqlite3.Error as e:
            print("Create Table Error: ", e)

    def insert_data(self, table_name, data):
        try:
            if(table_name == "tbl_percobaan"):
                query = """INSERT INTO "{0}"(mode) VALUES ('{1}')""".format(
                    table_name, data)
                self.cursor.execute(query)
                self.mydb.commit()
                self.last_id = self.cursor.lastrowid
            elif(table_name == "tbl_metode"):
                mode = ["Astar Search", "Improved Astar"]
                for counter in range(len(data)):
                    if(counter == 1):
                        query = """INSERT INTO tbl_uji_presepsi (id_percobaan,total_sebenarnya) VALUES ({0},{1})""".format(
                            self.last_id, len(data[counter]))
                        self.cursor.execute(query)
                        timer = round(classKirim.timer[0], 5)
                        query = """INSERT INTO tbl_waktu (id_percobaan,waktu) VALUES ({0},{1})""".format(
                            self.last_id, timer)
                        self.cursor.execute(query)
                    items = data[counter]
                    for path in items:
                        x = path[0]
                        y = path[1]
                        fScore = ui.astarM.fScore.get(path, 0)
                        insert_data = [(x, y, fScore)]
                        query = """INSERT INTO "{0}"(id_percobaan,x,y,fScore,mode,mode_fCost) VALUES ({1},?,?,?,'{2}','{3}')""".format(
                            table_name, self.last_id, mode[counter], ui.mode_fcost)
                        self.cursor.executemany(query, insert_data)
                    self.mydb.commit()
            elif(table_name == "tbl_start" or table_name == "tbl_end" or table_name == "tbl_obstacle"):
                query = """INSERT INTO "{0}"(id_percobaan,x,y) VALUES ({1},?,?)""".format(
                    table_name, self.last_id)
                self.cursor.executemany(query, data)
                self.mydb.commit()
            elif(table_name == "tbl_history"):
                query = """INSERT INTO "{0}"(id_percobaan,x,y,z) VALUES ({1},?,?,?)""".format(
                    table_name, self.last_id)
                if(classKirim.isActiveSimulasi == 0):
                    self.cursor.executemany(query, data)
                    self.mydb.commit()
                else:
                    try:
                        self.cursor_history.executemany(query, data)
                        self.mydb.commit()
                    except:
                        pass

        except sqlite3.Error as e:
            print("Insert Error: ", e)

    def get_data_percobaan(self):
        try:
            query = """SELECT * FROM tbl_percobaan ORDER BY id_percobaan ASC"""
            result = self.cursor.execute(query)
            self.mydb.commit()
            result = result.fetchall()
            return result
        except sqlite3.Error as e:
            print("Data View Percobaan Error: ", e)

    def delete_data(self, table_name, where, id):
        try:
            query = """DELETE FROM "{0}" WHERE "{1}" = {2} """.format(
                table_name, where, id)
            self.cursor_delete.execute(query)
            self.mydb.commit()
            self.last_id = 0
        except sqlite3.Error as e:
            print("Delete Error: ", e)

    def get_query(self, table_name, id):
        try:
            query = """SELECT * FROM "{0}" WHERE id_percobaan = {1}""".format(
                table_name, id)
            data = self.cursor.execute(query)
            data = data.fetchall()
            self.mydb.commit()
            return data
        except sqlite3.Error as e:
            print(e)

    def get_query_and(self, table_name, id, cond):
        try:
            query = """SELECT * FROM "{0}" WHERE id_percobaan = {1} AND {2}""".format(
                table_name, id, cond)
            data = self.cursor.execute(query)
            data = data.fetchall()
            self.mydb.commit()
            return data
        except sqlite3.Error as e:
            print(e)

    def get_manual_query(self, query):
        try:
            data = self.cursor.execute(query)
            data = data.fetchall()
            self.mydb.commit()
            return data
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        # Local
        directory = "database"
        path = os.path.join(os.getcwd(), directory)
        file = os.path.join(path, r'path_planning.db.algorithm_final')
        check_directory = os.path.isdir(path)
        if(check_directory == False):
            os.mkdir(path)

        # Desktop
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()

        # Class
        classKirim = KirimCond()
        db = SqliteConfigure(file)
        ui = MainApp()
        ui.setupUi(window)
        classKirim.end = ((ui.ball.x(
        ) + classKirim.cImgBall[0]) / 100. * 2, (ui.ball.y() + classKirim.cImgBall[1]) / 100. * 2)
        classKirim.start = ((ui.robot.x(
        ) + classKirim.cImgRobot[0]) / 100. * 2, (ui.robot.y() + classKirim.cImgRobot[1]) / 100. * 2)
        # UI
        ui.coor_x.setText("X: {} m.".format(round(classKirim.start[0], 3)))
        ui.coor_y.setText("Y: {} m.".format(round(classKirim.start[1], 3)))
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Main Error: ", e)
    except SystemExit:
        if(ui.lock > 0 and db.last_id > 0):
            db.delete_data("tbl_percobaan", "id_percobaan", db.last_id)
        print("Shutting Down ... !!!")
    except:
        pass
