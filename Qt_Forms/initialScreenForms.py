# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inicialScreen.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1133, 742)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Image/windowsIcon/images.jpg"), QtGui.QIcon.Active, QtGui.QIcon.On)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("b")
        self.draw_button = QtWidgets.QPushButton(Form)
        self.draw_button.setEnabled(True)
        self.draw_button.setGeometry(QtCore.QRect(530, 700, 151, 37))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.draw_button.setFont(font)
        self.draw_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.draw_button.setStyleSheet("background-color: gray")
        self.draw_button.setObjectName("draw_button")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(0, 47, 1131, 641))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1129, 639))
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setMinimumSize(QtCore.QSize(742, 621))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("../../sm_image_editor/edited.jpg"))
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.verticalLayout.addWidget(self.image)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.exit_button = QtWidgets.QPushButton(Form)
        self.exit_button.setGeometry(QtCore.QRect(1030, 10, 95, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.exit_button.setFont(font)
        self.exit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_button.setStyleSheet("background-color: gray")
        self.exit_button.setObjectName("exit_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cam view"))
        self.draw_button.setText(_translate("Form", "To Draw"))
        self.exit_button.setText(_translate("Form", "Exit"))


#if __name__ == "__main__":
 #   import sys
  #  app = QtWidgets.QApplication(sys.argv)
   # Form = QtWidgets.QWidget()
    #ui = Ui_Form()
   # ui.setupUi(Form)
   # Form.show()
   # sys.exit(app.exec_())
