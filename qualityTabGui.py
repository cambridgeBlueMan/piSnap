# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qualityTab.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(863, 661)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(30, 30, 241, 171))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 251, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.audioBitRate = QtWidgets.QComboBox(self.formLayoutWidget)
        self.audioBitRate.setObjectName("audioBitRate")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.audioBitRate)
        self.audioSampleRate = QtWidgets.QComboBox(self.formLayoutWidget)
        self.audioSampleRate.setObjectName("audioSampleRate")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.audioSampleRate)
        self.audioFileFormat = QtWidgets.QComboBox(self.formLayoutWidget)
        self.audioFileFormat.setObjectName("audioFileFormat")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.audioFileFormat)
        self.mux = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.mux.setEnabled(True)
        self.mux.setChecked(False)
        self.mux.setObjectName("mux")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.mux)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 250, 251, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 221, 148))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.videoBitRate = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.videoBitRate.setObjectName("videoBitRate")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.videoBitRate)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.videoQuality = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.videoQuality.setObjectName("videoQuality")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.videoQuality)
        self.videoProfile = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.videoProfile.setObjectName("videoProfile")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.videoProfile)
        self.videoLevel = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.videoLevel.setObjectName("videoLevel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.videoLevel)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.audioActive = QtWidgets.QCheckBox(Form)
        self.audioActive.setGeometry(QtCore.QRect(40, 210, 141, 27))
        self.audioActive.setObjectName("audioActive")

        self.retranslateUi(Form)
        self.audioBitRate.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.audioSampleRate.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.audioFileFormat.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.videoBitRate.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.videoQuality.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.audioActive.clicked['bool'].connect(Form.isAudioActive)
        self.videoProfile.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.videoLevel.currentIndexChanged['QString'].connect(Form.setCamValFromCombo)
        self.mux.clicked['bool'].connect(Form.doMux)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "audio"))
        self.label.setText(_translate("Form", "bit rate"))
        self.label_2.setText(_translate("Form", "sample rate"))
        self.label_3.setText(_translate("Form", "file format"))
        self.mux.setText(_translate("Form", "mux after record"))
        self.groupBox_2.setTitle(_translate("Form", "video"))
        self.label_4.setText(_translate("Form", "bit rate"))
        self.label_5.setText(_translate("Form", "Quality"))
        self.label_6.setText(_translate("Form", "Profiles"))
        self.label_7.setText(_translate("Form", "Levels"))
        self.audioActive.setText(_translate("Form", "audio is active"))

