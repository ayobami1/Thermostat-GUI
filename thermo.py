# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/user/Thermostat_control/dialog3.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as mqtt

connectionObj = {
    "clientName": "AYnaBabaProgrammer",
    "host": "broker.hivemq.com",
    "port": 1883,
}
publishTopic = "my/topic"
subscribeTopicTemp = "my/topic/temp"
subscribeTopicHum = "my/topic/hum"

subscribeList = [subscribeTopicTemp, subscribeTopicHum]




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(510, 395)
        Dialog.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setStyleSheet("rgb (23, 29, 116)")
        Dialog.setSizeGripEnabled(True)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(19, 10, 471, 361))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.humLabel = QtWidgets.QLabel(self.frame)
        self.humLabel.setGeometry(QtCore.QRect(280, 10, 181, 21))
        font = QtGui.QFont()
        font.setBold(True)
        self.humLabel.setFont(font)
        self.humLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.humLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.humLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.humLabel.setWordWrap(True)
        self.humLabel.setObjectName("humLabel")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(30, 49, 141, 91))
        self.label_5.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(280, 30, 181, 141))
        #self.label_8.setStyleSheet('border :2px solid black;')
        self.label_8.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_8.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_8.setText("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setWordWrap(False)
        self.label_8.setObjectName("label_8")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(310, 50, 141, 91))
        self.label_6.setStyleSheet('border :4px solid black; background-color:rgb(239, 239, 197); ')
        self.label_6.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.bar_1 = QtWidgets.QProgressBar(self.frame)
        self.bar_1.setGeometry(QtCore.QRect(40, 29, 111, 20))
        self.bar_1.setProperty("value", 24)
        self.bar_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bar_1.setObjectName("bar_1")
        self.tempLabel = QtWidgets.QLabel(self.frame)
        self.tempLabel.setGeometry(QtCore.QRect(10, 10, 181, 21))
        font = QtGui.QFont()
        font.setBold(True)
        self.tempLabel.setFont(font)
        self.tempLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tempLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tempLabel.setWordWrap(True)
        self.tempLabel.setObjectName("tempLabel")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(10, 29, 181, 141))
        self.label_7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_7.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_7.setText("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setWordWrap(False)
        self.label_7.setObjectName("label_7")
        self.lcd_2 = QtWidgets.QLCDNumber(self.frame)
        self.lcd_2.setGeometry(QtCore.QRect(300, 10, 111, 161))
        self.lcd_2.setMaximumSize(QtCore.QSize(16777214, 16777215))
        self.lcd_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd_2.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcd_2.setLineWidth(0)
        self.lcd_2.setMidLineWidth(0)
        self.lcd_2.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_2.setObjectName("lcd_2")
        self.lcd_1 = QtWidgets.QLCDNumber(self.frame)
        self.lcd_1.setGeometry(QtCore.QRect(20, 10, 111, 161))
        self.lcd_1.setMaximumSize(QtCore.QSize(16777214, 16777215))
        self.lcd_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd_1.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcd_1.setLineWidth(0)
        self.lcd_1.setMidLineWidth(0)
        self.lcd_1.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcd_1.setFont(font)
        self.lcd_1.setObjectName("lcd_1")
        self.bar_2 = QtWidgets.QProgressBar(self.frame)
        self.bar_2.setGeometry(QtCore.QRect(320, 30, 111, 20))
        self.bar_2.setProperty("value", 24)
        self.bar_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bar_2.setObjectName("bar_2")
        self.statusLabel_2 = QtWidgets.QLabel(self.frame)
        self.statusLabel_2.setGeometry(QtCore.QRect(160, 150, 10, 10))
        self.statusLabel_2.setFrameShape(QtWidgets.QFrame.Box)
        self.statusLabel_2.setText("")
        self.statusLabel_2.setObjectName("statusLabel_2")
        self.tempUnitLable = QtWidgets.QLabel(self.frame)
        self.tempUnitLable.setGeometry(QtCore.QRect(130, 70, 21, 21))
        font = QtGui.QFont()
        font.setBold(True)
        self.tempUnitLable.setFont(font)
        self.tempUnitLable.setObjectName("tempUnitLable")
        self.humUnitLabel = QtWidgets.QLabel(self.frame)
        self.humUnitLabel.setGeometry(QtCore.QRect(410, 70, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.humUnitLabel.setFont(font)
        self.humUnitLabel.setObjectName("humUnitLabel")
        self.statusLabel_1 = QtWidgets.QLabel(self.frame)
        self.statusLabel_1.setGeometry(QtCore.QRect(30, 150, 110, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.statusLabel_1.setFont(font)
        self.statusLabel_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.statusLabel_1.setObjectName("statusLabel_1")
        self.statusLabel_4 = QtWidgets.QLabel(self.frame)
        self.statusLabel_4.setGeometry(QtCore.QRect(430, 150, 10, 10))
        self.statusLabel_4.setFrameShape(QtWidgets.QFrame.Box)
        self.statusLabel_4.setText("")
        self.statusLabel_4.setObjectName("statusLabel_4")
        self.btn = QtWidgets.QPushButton(self.frame, clicked= lambda: self.handleClick() )
        self.btn.setGeometry(QtCore.QRect(190, 230, 100, 100))
        self.btn.setStyleSheet(
            'border-radius : 50 ; border :2px solid black; font: 18pt \'Trebuchet MS\'; color: rgb(38, 33, 228); background-color:rgb(248, 246, 232);')

        self.btn.setCheckable(True)
        self.btn.setObjectName("btn")
        self.statusLabel_3 = QtWidgets.QLabel(self.frame)
        self.statusLabel_3.setGeometry(QtCore.QRect(310, 150, 110, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.statusLabel_3.setFont(font)
        self.statusLabel_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.statusLabel_3.setObjectName("statusLabel_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def butColor(self):
        if self.btn.isChecked():

            self.btn.setText("ON")
            self.btn.setStyleSheet(
                'border-radius : 50 ; border :2px solid black; font: 18pt \'Trebuchet MS\'; color: rgb(38, 33, 228);background-color:rgb(0, 253, 82)')
        else:
            self.btn.setStyleSheet(
                'border-radius : 50 ; border :2px solid black; font: 18pt \'Trebuchet MS\'; color: rgb(38, 33, 228); background-color:rgb(248, 0, 97);')

    start = 0
    def handleClick(self):
        if self.btn.isChecked():
            client.publish(publishTopic, "ON")
        else:
            client.publish(publishTopic, "OFF")
        self.checkState(f'{self.Cal()}')

    def handleHumidity(self, payload):
        self.lcd_1.display(payload)
    def Cal(self):
        self.start = self.start + 1

        return self.start

    def checkState(self, press):

        if press == 'c':
            #self.label.setText('')
            self.start = 0


        else:
            self.btn.setText("OFF")
            # self.lcd_1.display(f'{int(press) -30}')
            self.lcd_2.display(press)
            #self.label.setText(f"{self.label.text()}{press}")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MQQT Thermostat GUI"))
        self.humLabel.setText(_translate("Dialog", "HUMIDITY"))
        self.tempLabel.setText(_translate("Dialog", "TEMPERATURE"))
        self.tempUnitLable.setText(_translate("Dialog", "°C"))
        self.humUnitLabel.setText(_translate("Dialog", "%"))
        self.statusLabel_1.setText(_translate("Dialog", "Relay  Disconected"))
        self.btn.setText(_translate("Dialog", "PRESS"))
        self.btn.clicked.connect(self.butColor)
        self.statusLabel_3.setText(_translate("Dialog", "Relay  Disconected"))
        self.lcd_1.display(f'{27}')
        self.lcd_2.display(90)

if __name__ == "__main__":
    import sys
    # Connecting
    client = mqtt.Client(connectionObj["clientName"])
    client.connect(connectionObj["host"], connectionObj["port"])
    for i in subscribeList:
        client.subscribe(i)

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    def on_message(client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        if (message.topic == subscribeTopicHum):
            ui.handleHumidity(int(message.payload))
    client.on_message = on_message
    client.loop_start()
    sys.exit(app.exec_())
