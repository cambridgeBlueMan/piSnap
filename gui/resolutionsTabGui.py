# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resolutionsTabGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(596, 597)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 60, 391, 271))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.imgres = QtWidgets.QComboBox(self.formLayoutWidget)
        self.imgres.setObjectName("imgres")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.imgres)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.vidres = QtWidgets.QComboBox(self.formLayoutWidget)
        self.vidres.setObjectName("vidres")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.vidres)

        self.retranslateUi(Form)
        self.vidres.currentIndexChanged['int'].connect(Form.setVideoRes)
        self.imgres.currentIndexChanged['int'].connect(Form.setStillRes)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Still Resolutions"))
        self.label_2.setText(_translate("Form", "Video Resolutions     "))

