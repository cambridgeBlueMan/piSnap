# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adjustments.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_adjustments(object):
    def setupUi(self, adjustments):
        adjustments.setObjectName("adjustments")
        adjustments.resize(1026, 848)
        self.formLayoutWidget_3 = QtWidgets.QWidget(adjustments)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(110, 270, 721, 171))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.color_effects_v = CompositeSlider(self.formLayoutWidget_3)
        self.color_effects_v.setObjectName("color_effects_v")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.color_effects_v)
        self.label = QtWidgets.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label)
        self.color_effects_u = CompositeSlider(self.formLayoutWidget_3)
        self.color_effects_u.setObjectName("color_effects_u")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.color_effects_u)
        self.color_effects_none = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.color_effects_none.setChecked(True)
        self.color_effects_none.setObjectName("color_effects_none")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.color_effects_none)
        self.formLayoutWidget = QtWidgets.QWidget(adjustments)
        self.formLayoutWidget.setGeometry(QtCore.QRect(120, 460, 341, 252))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.awb_mode = QtWidgets.QComboBox(self.formLayoutWidget)
        self.awb_mode.setObjectName("awb_mode")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.awb_mode)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.drc_strength = QtWidgets.QComboBox(self.formLayoutWidget)
        self.drc_strength.setObjectName("drc_strength")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.drc_strength)
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.exposure_mode = QtWidgets.QComboBox(self.formLayoutWidget)
        self.exposure_mode.setObjectName("exposure_mode")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.exposure_mode)
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.flash_mode = QtWidgets.QComboBox(self.formLayoutWidget)
        self.flash_mode.setObjectName("flash_mode")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.flash_mode)
        self.label_11 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.meter_mode = QtWidgets.QComboBox(self.formLayoutWidget)
        self.meter_mode.setObjectName("meter_mode")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.meter_mode)
        self.image_effect = QtWidgets.QComboBox(self.formLayoutWidget)
        self.image_effect.setObjectName("image_effect")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.image_effect)
        self.formLayoutWidget_2 = QtWidgets.QWidget(adjustments)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(110, 70, 731, 191))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 3, 0, 3)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_12 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.sharpness = CompositeSlider(self.formLayoutWidget_2)
        self.sharpness.setObjectName("sharpness")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sharpness)
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.contrast = CompositeSlider(self.formLayoutWidget_2)
        self.contrast.setObjectName("contrast")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.contrast)
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.label_15 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.brightness = CompositeSlider(self.formLayoutWidget_2)
        self.brightness.setObjectName("brightness")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.brightness)
        self.saturation = CompositeSlider(self.formLayoutWidget_2)
        self.saturation.setObjectName("saturation")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.saturation)

        self.retranslateUi(adjustments)
        self.sharpness.lnValueChanged['int'].connect(adjustments.changeCameraValue)
        self.contrast.lnValueChanged['int'].connect(adjustments.changeCameraValue)
        self.saturation.lnValueChanged['int'].connect(adjustments.changeCameraValue)
        self.brightness.lnValueChanged['int'].connect(adjustments.changeCameraValue)
        self.color_effects_u.lnValueChanged['int'].connect(adjustments.doColorEffect)
        self.color_effects_v.lnValueChanged['int'].connect(adjustments.doColorEffect)
        self.color_effects_none.stateChanged['int'].connect(adjustments.doColorEffect)
        self.awb_mode.currentIndexChanged['QString'].connect(adjustments.setAwbMode)
        self.image_effect.currentIndexChanged['QString'].connect(adjustments.setImageEffect)
        self.drc_strength.currentIndexChanged['QString'].connect(adjustments.setDrcStrength)
        self.exposure_mode.currentIndexChanged['QString'].connect(adjustments.setExposureMode)
        self.flash_mode.currentIndexChanged['QString'].connect(adjustments.setFlashMode)
        self.meter_mode.currentIndexChanged['QString'].connect(adjustments.setMeterMode)
        QtCore.QMetaObject.connectSlotsByName(adjustments)

    def retranslateUi(self, adjustments):
        _translate = QtCore.QCoreApplication.translate
        adjustments.setWindowTitle(_translate("adjustments", "Form"))
        self.label_2.setText(_translate("adjustments", "U"))
        self.label_3.setText(_translate("adjustments", "V"))
        self.label.setText(_translate("adjustments", "Colour effects"))
        self.color_effects_none.setText(_translate("adjustments", "None"))
        self.label_6.setText(_translate("adjustments", "Image Effects"))
        self.label_7.setText(_translate("adjustments", "AWB Modes"))
        self.label_8.setText(_translate("adjustments", "DRC Strength"))
        self.label_9.setText(_translate("adjustments", "Exposure Mode"))
        self.label_10.setText(_translate("adjustments", "Flash Mode"))
        self.label_11.setText(_translate("adjustments", "Meter Mode"))
        self.label_12.setText(_translate("adjustments", "Sharpness"))
        self.label_13.setText(_translate("adjustments", "Contrast"))
        self.label_14.setText(_translate("adjustments", "Saturation"))
        self.label_15.setText(_translate("adjustments", "Brightness"))

from psSliders import CompositeSlider
