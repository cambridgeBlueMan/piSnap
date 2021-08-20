# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zoomTabGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(537, 653)
        self.getZoom = KeyboardSlider(Form)
        self.getZoom.setGeometry(QtCore.QRect(0, 410, 501, 21))
        self.getZoom.setMinimum(1920)
        self.getZoom.setMaximum(3470)
        self.getZoom.setSingleStep(1)
        self.getZoom.setProperty("value", 3470)
        self.getZoom.setOrientation(QtCore.Qt.Horizontal)
        self.getZoom.setObjectName("getZoom")
        self.start = QtWidgets.QPushButton(Form)
        self.start.setGeometry(QtCore.QRect(20, 430, 61, 20))
        self.start.setObjectName("start")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(670, 30, 91, 22))
        self.label_3.setObjectName("label_3")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 507, 380))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.adjustZoom = DragButton(self.frame)
        self.adjustZoom.setGeometry(QtCore.QRect(0, 0, 22, 22))
        self.adjustZoom.setObjectName("adjustZoom")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 390, 68, 22))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 430, 81, 22))
        self.label_2.setObjectName("label_2")
        self.getSpeed = QtWidgets.QSlider(Form)
        self.getSpeed.setGeometry(QtCore.QRect(170, 430, 131, 26))
        self.getSpeed.setMinimum(100)
        self.getSpeed.setMaximum(900)
        self.getSpeed.setProperty("value", 600)
        self.getSpeed.setOrientation(QtCore.Qt.Horizontal)
        self.getSpeed.setObjectName("getSpeed")
        self.zoomTableView = QtWidgets.QTableView(Form)
        self.zoomTableView.setGeometry(QtCore.QRect(10, 470, 501, 181))
        self.zoomTableView.setObjectName("zoomTableView")
        self.delRow = QtWidgets.QPushButton(Form)
        self.delRow.setGeometry(QtCore.QRect(430, 430, 51, 21))
        self.delRow.setObjectName("delRow")
        self.playRows = QtWidgets.QPushButton(Form)
        self.playRows.setGeometry(QtCore.QRect(320, 430, 31, 31))
        self.playRows.setWhatsThis("")
        self.playRows.setCheckable(False)
        self.playRows.setObjectName("playRows")
        self.nextZoom = QtWidgets.QPushButton(Form)
        self.nextZoom.setGeometry(QtCore.QRect(370, 430, 31, 30))
        self.nextZoom.setWhatsThis("")
        self.nextZoom.setObjectName("nextZoom")

        self.retranslateUi(Form)
        self.start.clicked.connect(Form.doSetStart)
        self.getZoom.valueChanged['int'].connect(Form.setZoom)
        self.adjustZoom.posChanged['int','int'].connect(Form.setZoomWithButton)
        self.getSpeed.sliderMoved['int'].connect(Form.setSpeed)
        self.delRow.clicked.connect(Form.deleteSelectedRow)
        self.playRows.clicked['bool'].connect(Form.playSelectedRows)
        self.nextZoom.clicked.connect(Form.doNextZoom)
        self.zoomTableView.clicked['QModelIndex'].connect(Form.showThisZoomStart)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.start.setText(_translate("Form", "add"))
        self.label_3.setText(_translate("Form", "zoom"))
        self.adjustZoom.setText(_translate("Form", "b"))
        self.label.setText(_translate("Form", "Set Zoom"))
        self.label_2.setText(_translate("Form", "Set Speed"))
        self.delRow.setText(_translate("Form", "del row"))
        self.playRows.setToolTip(_translate("Form", "play or abandon zoom"))
        self.playRows.setText(_translate("Form", "*"))
        self.nextZoom.setToolTip(_translate("Form", "while playing move to next zoom"))
        self.nextZoom.setText(_translate("Form", "*"))

from dragbutton import DragButton
from keyboardslider import KeyboardSlider
