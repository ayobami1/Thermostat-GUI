
" WE WILL IMPORT GPIO FOR RPI USE ONLY ! COMMENT THIS ALWAYS EXCEPT FOR OTHER OS"
# import RPi.GPIO as GPIO
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering
# GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initia

import qdarkstyle
# WE IMPORT PYSIDE2
from PySide2 import QtCore, QtGui, QtWidgets,QtUiTools
# WE IMPORT THE MAINWINDOW APLLICATION CLASS
from test_thermo_ui import*
# IMPORT SYSTEM TOOLS
import  sys
# IMPORT THE MQTT CLIENT
import paho.mqtt.client as mqqt
# IMPORT TIME FUNCTION TO HANDLE TRANSMISSION INTERVALS
from time import sleep

"NOW DECLARE GLOBAL VARIABLES"

# FOR CLIENT TO THROW DISCONNECTION ERROR THE BROKER MANAGES
# THE NOTIFICATION WILL BE TRIGGER IT AUTOMATIVALLY AFTER 1.5 TIMES THE
# KEEPALIVE IS INACTIVE
# THE BROKER MANAGE THE PINGRESP FROM PINGREQ PACKECT
keepalive = 40

# PUT YOUR BROKER IP / ADDRESS HERE
broker = "192.168.84.33"

# PORT NUMBER TO LISTEN TO
port = 1883

# WE SUBCRIBE TO GET TEMPERATURE DATAS
SubTempTopic = "Nymea/Temp"
# WE SUBSCRIBE TO GET HUMIDTY DATAS
SubHumTopic = "Nymea/Hum"
# WE PUBLISH TO THIS TO TURN ON THE TEMP RELAY
PubRly1Topic = "Nymea/Rly1/Pub"
# WE PUBLISH TO THIS TO TURN ON HUM RELAY
PubRly2Topic = "Nymea/Rly2/Pub"
# WE SUBSCRIBE TO CONFIRM IF TEMP RELAY IS WORKING FINE MAKE SURE YOU PUBLISH FROM THE DEVICE TO THIS TOPIC
SubRly1Topic = "Nymea/Rly1/Sub"
# WE SUBSCRIBE TO CONFIRM IF HUM RELAY IS WORKING FINE MAKE SURE YOU PUBLISH FROM THE OTHER DEVICE TO THIS TOPIC
SubRly2Topic = "Nymea/Rly2/Sub"
# WE SUBCRIBE TO MAKE SURE F1 WORKING BEFORE CHANGING STATE MAKE SURE YOU PUBLISH FROM THE OTHER DEVICE TO THIS TOPIC
F1_Sub_Topic = "Nymea/F1/Sub"
# WE PUBLISH WITH F1 BUTTON ( ANYTHING YOU LIKE )
F1_Pub_Topic = "Nymea/F1/LED"
#WE SUBSCRIBE TO GPI0_21 TO CHECK ITS STATE
GPIO_21 =  "GPIO21/msg/Sub"

#WE PUT ALL THE TOPICS TO SUBSCRIBE TO IN A LIST
sus_ = [SubTempTopic,SubHumTopic,SubRly2Topic,SubRly1Topic,
        F1_Sub_Topic,GPIO_21]


class MainWindow(QMainWindow):

    "WE DECLARE GLOBAL VARIABLE WITHIN THE CLASS"

    # GLOBAL VARIABLE FOR TEMPERATURE SETTING
    tem_start = 0

    # GLOBAL VARIABLE FOR HUMIDITY SETTING
    hum_start =0



    # GLOBAL VARIABLE FOR TEMPERATURE SETTING STATUS BEFORE PUBLISHING IS ALWAYS BETWEEN (0 and 1)
    Temp_Status = 0
    # GLOBAL VARIABLE FOR HUMIDTY SETTING STATUS BEFORE PUBLISHING IS ALWAYS BETWEEN (0 and 1)
    Hum_Status = 0
    #print(HumValue(payload))









    def __init__(self):

        QMainWindow.__init__(self)
        self.ui = Ui_THERMOSTAT()
        self.ui.setupUi(self)


        # SHOW WINDOW APPLICATION
        self.show()

        # SET CURRENT PAGE TO HOME
        self.ui.home.setCurrentWidget(self.ui.Home)

        # SET THE HOME PAGE TITLE
        self.ui.home_title.setText("MQQT THERMO GUI")

        #SET THE SENSOR PAGE TITLE
        self.ui.sensor_title.setText("THERMOSTAT  SENSOR ")

        # SET THE  TEMPERATUURE LABEL TEXT
        self.ui.temp_label.setText("Food Area Fridge")
        self.ui.temp_label_2.setText(self.ui.temp_label.text())
        self.ui.temp_label_3.setText(self.ui.temp_label.text())

        # SET THE  HUMIDITY LABEL TEXT
        self.ui.hum_label.setText("Fridge Diary")
        self.ui.hum_label_2.setText(self.ui.hum_label.text())
        self.ui.hum_label_3.setText(self.ui.hum_label.text())

        # INSTANCE FOR BUTTON ACTION AND SIGNALS
        self.ui.NextBtn.clicked.connect(self.Next_page)
        self.ui.PreviuosBtn.clicked.connect(self.Previous_page)

        # ALWAYS DSIABLE THE PREVIOUS BUTTON ON START
        self.ui.PreviuosBtn.setDisabled(True)
        self.ui.PreviuosBtn.setStyleSheet('color: transparent')

        # CREATE FUNCTION FOR TEMP AND HUM BUTTON
        self.ui.Temp_btn.clicked.connect(self.Next_page)
        self.ui.Hum_btn.clicked.connect(self.Next_page)


        # DISABLE SET MAX AND MIN TEMP BTN AND ENABLE IT WITH SET BTN
        self.ui.SetMax_Temp_btn.setDisabled(True)
        self.ui.SetMin_Temp_btn.setDisabled(True)

        # DISABLE SET MAX AND MIN HUM BTN AND ENABLE IT WITH SET BTN
        self.ui.SetMax_Hum_btn.setDisabled(True)
        self.ui.SetMin_Hum_btn.setDisabled(True)


        # DISABLE THE TEMP AT THE START BTN AND RENABLE WITH SETHUM FUNCTON
        self.ui.Up_Temp_btn.setDisabled(True)
        self.ui.Down_Temp_btn.setDisabled(True)
        self.ui.SetMax_Temp_btn.clicked.connect(self.setMaxTemp)
        self.ui.SetMin_Temp_btn.clicked.connect(self.setMinTemp)


        # DISABLE THE HUMIDTY AT THE START BTN AND RENABLE WITH SETHUM FUNCTON
        self.ui.Up_Hum_btn.setDisabled(True)
        self.ui.Down_Hum_btn.setDisabled(True)
        self.ui.SetMax_Hum_btn.clicked.connect(self.setMaxHum)
        self.ui.SetMin_Hum_btn.clicked.connect(self.setMinHum)


        #  BTN MANAGMENT FOR HUMIDTY AND TEMPERATURE TRIGGER SETTING
        self.ui.Set_Temp_btn.clicked.connect(lambda :self.SetBtn("Temperature"))
        self.ui.Set_Hum_btn.clicked.connect(lambda :self.SetBtn('Humidity'))

        # CONNECT THE NAVIGATION BTN TO FUNCTION
        self.ui.Up_Hum_btn.clicked.connect(lambda :self.Hum_settings("Up"))
        self.ui.Down_Hum_btn.clicked.connect(lambda: self.Hum_settings("Down"))
        self.ui.Up_Temp_btn.clicked.connect(lambda :self.Temp_settings('Up'))
        self.ui.Down_Temp_btn.clicked.connect(lambda: self.Temp_settings("Down"))



       # SET THE BAR STYLE (Example: Donet, Line,Pie, Pizza,Pie,Hybrid1,Hybrid2
        self.ui.widget_5.rpb_setBarStyle('Hybrid1')
        self.ui.widget_6.rpb_setBarStyle('Hybrid1')

        # SET PROGRESS BAR LINE CAP
        self.ui.widget_5.rpb_setLineCap('SquareCap')
        self.ui.widget_6.rpb_setLineCap('SquareCap')

       # SET PROGRESS BAR LINE COLOR
        self.ui.widget_5.rpb_setLineColor ((255, 40, 43)) # ARGUMENT RGB AS TUPLE
        self.ui.widget_6.rpb_setLineColor((41, 66, 255))  # ARGUMENT RGB AS TUPLE

        # SET PROGRESS BAR PATH COLOR
        self.ui.widget_5.rpb_setPathColor((44, 44, 44))  # ARGUMENT RGB AS TUPLE
        self.ui.widget_6.rpb_setPathColor((44, 44, 44))

        # SET PROGRESS BAR LINE STYLE
        self.ui.widget_5.rpb_setLineStyle('DotLine')
        self.ui.widget_6.rpb_setLineStyle('DotLine')

        # SET BAR PATH WIDTH
        self.ui.widget_5.rpb_setLineWidth(10)  # ARGUMENT RGB AS TUPLE
        self.ui.widget_6.rpb_setLineWidth(10)

        # SET PROGRESS BAR LiNE WIDTH
        self.ui.widget_5.rpb_setPathWidth(10)  # ARGUMENT RGB AS TUPLE
        self.ui.widget_6.rpb_setPathWidth(10)

       # SET PROGRESS BAR Text COLOR
        self.ui.widget_5.rpb_setTextColor ((255, 255, 255)) # ARGUMENT RGB AS TUPLE
        self.ui.widget_6.rpb_setTextColor((255, 255, 255))


      # SET BAR PROGRESS TEXT TYPE : VALUE OR PERCENTAGE
        self.ui.widget_5.rpb_setTextFormat('Value')
        self.ui.widget_5.rpb_setTextFont('Arial')
        self.ui.widget_5.rpb_setCircleColor((28, 23, 36))  # ARGUMENT RGB AS A TUPLE
        self.ui.widget_6.rpb_setTextFormat('Value')
        self.ui.widget_6.rpb_setTextFont('Arial')
        self.ui.widget_6.rpb_setCircleColor((28, 23, 36))  # ARGUMENT RGB AS A TUPLE

        # Circle:
        self.ui.widget_5.rpb_setCircleColor((12, 2, 33))  # ARGUMENT RGB AS A TUPLE
        self.ui.widget_6.rpb_setCircleColor((12, 2, 33))



        # DISABLE PROGRESS BAR TEXT
        self.ui.widget_5.rpb_enableText(False)
        self.ui.widget_6.rpb_enableText(False)

        # SETTING THE RANGE : MIN-0 & MAX:360
        self.ui.widget_5.rpb_setRange(-30, 100)
        self.ui.widget_6.rpb_setRange(1, 100)

        # SET PROGRESS BAR STARTING POS EXAPAMPLE (West, South, East, North)
        self.ui.widget_5.rpb_setInitialPos('West')
        self.ui.widget_6.rpb_setInitialPos('West')

         # SET A DEFAULT VALUE FOR WIDGET_5 AND WIDGET__6
        self.ui.widget_5.rpb_setValue(0)
        self.ui.widget_6.rpb_setValue(0)

        # INITIALISE F1 AND F2 BUTTONS
        self.ui.F1btn.clicked.connect(self.checkF1Button)
        self.ui.F2btn.clicked.connect(self.checkF2Button)


    # CHECK F1 BUTTON WHEN IT IS PRESS TO PUBLISH AND CHANGE BUTTON STATE
    def checkF1Button(self):


        if self.ui.F1btn.isChecked():

            client.publish(F1_Pub_Topic,"ON", retain= True)


        else:
            self.ui.F1btn.setStyleSheet('border :2px ;background-color:transparent'
                                        'background-hover: yellow')
            client.publish(F1_Pub_Topic, "OFF",retain= True)


    """F2 Is USED TO ACTIVATE GPIO 20 USING BCM AS A GPIO SETUP PLEASE 
    COMMENT THIS SECTION WHEN RUNNING ON OTHER OS APART FROM RPI
    """
    def checkF2Button(self):
         pass
    #     if self.ui.F2btn.isChecked():
    #         GPIO.output(20, GPIO.HIGH)
    #         self.ui.F2btn.setStyleSheet(
    #             'border :2px ;background-color:rgb(0, 253, 82)')
    #     else:
    #         self.ui.F2btn.setStyleSheet('border :2px ;background-color:transparent'
    #                                     'background-hover: yellow')
    #         GPIO.output(20, GPIO.LOW)

        # THIS HANDLE THE PACKET DATAS FROM THE HUMIDITY SENSOR
    def Handle_Humidty(self, payload):
        print(payload)

        # CHECK IF THE MAX HUMIDTY VALUE MEETS THE CONDITION SET
        if int(payload) >= int(self.ui.MaxHumVal.text()) and self.Hum_Status == 0:
            self.Hum_Status = 1


        elif self.Hum_Status == 1 and int(payload) > int(self.ui.MinHumVal.text()):

            # TURN ON THE RELAY WHEN THE HUMIDTY VALUE REACHED THE MAX TRIGGER
            # THIS MEANS THAT FRIDGE WILL START WORKING BECAUSE IT IS HOT
            # WE WOULD PUBLISH ON TO THE BROKER AND THE CLIENT TEMPERATURE
            # RELAY WOULD SUBSCRIBE TO MAKE THE PIN HIGH
           # self.HumValue = self.HumValue - 1
            #self.RelayONStatus2()
            client.publish(PubRly2Topic, "ON",retain= True)
            self.ui.HumLcd.display(payload)
            self.ui.HumLcd_2.display(payload)
            self.ui.widget_6.rpb_setValue(payload)
            self.ui.HumValue.setText(f"{payload} %")

        # CHECK IF THE MIN HUMIDTY VALUE MEETS THE CONDITION SET
        elif payload <= int(self.ui.MinHumVal.text()) and self.Hum_Status == 1:

            self.Hum_Status = 0




        else:

            # TURN OFF THE RELAY WHEN THE HUMIDTY VALUE REACHED THE MAX TRIGGER
            # THIS MEANS THAT FRIDGE WILL START WORKING BECAUSE IT IS HOT
            # WE WOULD PUBLISH ON TO THE BROKER AND THE CLIENT TEMPERATURE
            # RELAY WOULD SUBSCRIBE TO MAKE THE PIN LOW
           # self.HumValue = self.HumValue + 1
            client.publish(PubRly2Topic, "OFF",retain= True)
            self.ui.HumLcd.display(payload)
            self.ui.HumLcd_2.display(payload)
            self.ui.widget_6.rpb_setValue(payload)
            self.ui.HumValue.setText(f"{payload} %")

    # THIS HANDLES THE PACKET DATAS FROM THE TEMPERATURE SENSORS
    def Handle_Temperature(self,payload):
        print(payload)



            # CHECK IF THE MAX TEMPERATURE VALUE MEETS THE CONDITION SET
        if  int(payload) >= int(self.ui.MaxTempVal.text()) and self.Temp_Status == 0:
            self.Temp_Status = 1

        elif self.Temp_Status ==1 and int(payload) > int(self.ui.MinTemVal.text()) :

             # TURN ON THE RELAY WHEN THE TEMPERATURE VALUE REACHED THE MAX TRIGGER
             # THIS MEANS THAT FRIDGE WILL START WORKING BECAUSE IT IS HOT
             # WE WOULD PUBLISH ON TO THE BROKER AND THE CLIENT TEMPERATURE
             # RELAY WOULD SUBSCRIBE TO MAKE THE PIN HIGH

            client.publish(PubRly1Topic, "ON",retain= True)

            """ ONCE THE CONDITIONS ARE MET WE USE 'self.publish(SubRly1Topic, "ON")' TO
             PUBLISH TO THE BROKER SO THAT IT CAN TRIGGER THE CONNECTED
              TEMPERATURE RELAY TO WORK, THEN GOTO THE ON_MESSAGE TO MAKE
              SURE THE RELAY HAS STATED WORKING
              """
            #self.RelayONStatus1()

            self.ui.TempLcd.display(payload)
            self.ui.TempLcd_2.display(payload)
            self.ui.widget_5.rpb_setValue(payload)
            self.ui.TempValue.setText(f"{payload} °C")

        # CHECK IF THE MIN TEMPERATURE VALUE MEETS THE CONDITION SET
        elif payload <= int(self.ui.MinTemVal.text()) and self.Temp_Status == 1:

            self.Temp_Status = 0




        else:

            # TURN OFF THE RELAY WHEN THE TEMPERATURE VALUE REACHED THE MAX TRIGGER
            # THIS MEANS THAT FRIDGE WILL START WORKING BECAUSE IT IS HOT
            # WE WOULD PUBLISH ON TO THE BROKER AND THE CLIENT TEMPERATURE
            # RELAY WOULD SUBSCRIBE TO MAKE THE PIN LOW
            #self.TempValue = self.TempValue + 1
            client.publish(PubRly1Topic, 'OFF',retain= True)
            self.ui.TempLcd.display(payload)
            self.ui.TempLcd_2.display(payload)
            self.ui.widget_5.rpb_setValue(payload)
            self.ui.TempValue.setText(f"{payload} °C")





    # SET TEMP MINIMUM TRIGGER VALUE
    def setMinTemp(self):
        msg = QMessageBox()
        msg.setWindowTitle(f" Alert")
        msg.setText("Are You Sure ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setInformativeText(f"Do you want to make changes to triggers threshold ?")
        msg.setDetailedText("Once you change the Min trigger threshold it will control the relay On/Off\n"
                            "make sure you what you are doing ! 🤓")
        msg.setIcon(QMessageBox.Question)
        ret = msg.exec_()

        if ret == QMessageBox.Yes:

            # CONFIRM IF MIN VALUE IS NOT EQUALS AND GREATER THAN MAX VALUE
            if int(self.ui.MaxTempVal.text())!= self.tem_start and self.tem_start < int(self.ui.MaxTempVal.text()):

                # IF IS NOT THEN SET MiN TRIGGER VALUE
                self.ui.MinTemVal.setText(f"{self.tem_start}")
                self.ui.Set_Temp_btn.setDisabled(False)
                self.ui.SetMin_Temp_btn.setDisabled(True)


            else:
                # IF IT IS  THEN DISPLAY POP UP MESSAGES AND DONT SET MIN TRIGGER VALUE
                msg.setText("MIN TRIGGER VALUE INVALID")
                msg.setWindowTitle(f" Alert")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setInformativeText(f"Hey the Min trigger value can't be equal or greater than max value")
                msg.setDetailedText("The Minimum Value should not be greater and equals to Max Value \n"
                                    "for example you can only set trigger value as \n MIN:2 AND MAX 4 ")
                msg.setIcon(QMessageBox.Warning)
                ret = msg.exec_()
        else:

            # DISABLE SET BUTTONS AFTER SUCCESSFULLY SET
            self.ui.Set_Temp_btn.setDisabled(True)
            self.ui.SetMin_Temp_btn.setDisabled(False)
            self.ui.MinTemVal.setText(self.ui.MinTemVal.text())

 # SET TEMPERATURE MAXIMUM VALUE
    def setMaxTemp(self):
        # ENABLE THE NAVIGATION TEMP BTN

        self.ui.Up_Temp_btn.setDisabled(False)
        self.ui.Down_Temp_btn.setDisabled(False)
        # ENABLE SET BTN
        self.ui.Set_Temp_btn.setDisabled(False)
        msg = QMessageBox()
        msg.setWindowTitle(f" Alert")
        msg.setText("Are You Sure ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setInformativeText(f"Do you want to make changes to triggers threshold ?")
        msg.setDetailedText("Once you change the Max trigger threshold it will control the relay On/Off\n"
                            "make sure you what you are doing ! 🤓")
        msg.setIcon(QMessageBox.Question)
        ret = msg.exec_()

        if ret == QMessageBox.Yes:

            # CONFIRM IF MIN VALUE IS NOT EQUALS AND GREATER THAN MAX VALUE
            if int(self.ui.MinTemVal.text()) != self.tem_start and self.tem_start > int(self.ui.MinTemVal.text()):

                # IF IS NOT THEN SET MAX TRIGGER VALUE
                self.ui.MaxTempVal.setText(f"{self.tem_start}")
                self.ui.Set_Temp_btn.setDisabled(False)
                self.ui.SetMax_Temp_btn.setDisabled(True)


            else:
                # IF IT IS  THEN DISPLAY POP UP MESSAGES AND DONT SET MIN TRIGGER VALUE
                msg.setText("MIN TRIGGER VALUE INVALID")
                msg.setWindowTitle(f" Alert")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setInformativeText(f"Hey the MAX trigger value can't be equal or Lesser than Min value")
                msg.setDetailedText("The Maximum Value should not be lesser and equals to Min Value \n"
                                    "for example you can only set trigger value as \n MIN:2 AND MAX 4 ")
                msg.setIcon(QMessageBox.Warning)
                ret = msg.exec_()


        else:
            # DISABLE SET BUTTONS AFTER SUCCESSFULLY SET
            self.ui.Set_Temp_btn.setDisabled(True)
            self.ui.SetMax_Temp_btn.setDisabled(False)
            self.ui.MaxTempVal.setText(self.ui.MaxTempVal.text())


 # SET HUMIDTY MAX TRIGGER VALUE
    def setMaxHum(self):
        msg = QMessageBox()
        msg.setWindowTitle(f" Alert")
        msg.setText("Are You Sure ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setInformativeText(f"Do you want to make changes to triggers threshold ?")
        msg.setDetailedText("Once you change the Min trigger threshold it will control the relay On/Off\n"
                            "make sure you what you are doing ! 🤓")
        msg.setIcon(QMessageBox.Question)
        ret = msg.exec_()

        if ret == QMessageBox.Yes:

            # CONFIRM IF MIN VALUE IS NOT EQUALS AND GREATER THAN MAX VALUE
            if int(self.ui.MinHumVal.text()) != self.hum_start and self.hum_start > int(self.ui.MinHumVal.text()):

                # IF IS NOT THEN SET MAX TRIGGER VALUE
                self.ui.MaxHumVal.setText(f"{self.hum_start}")
                self.ui.Set_Hum_btn.setDisabled(False)
                self.ui.SetMax_Hum_btn.setDisabled(True)


            else:
                # IF IT IS  THEN DISPLAY POP UP MESSAGES AND DONT SET MIN TRIGGER VALUE
                msg.setText("MIN TRIGGER VALUE INVALID")
                msg.setWindowTitle(f" Alert")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setInformativeText(f"Hey the MAX trigger value can't be equal or Lesser than min value")
                msg.setDetailedText("The Maximum Value should not be lesser and equals to Min Value \n"
                                    "for example you can only set the trigger value as \n MIN:20 AND MAX 50 ")
                msg.setIcon(QMessageBox.Warning)
                ret = msg.exec_()

        else:
            # DISABLE SET BUTTONS AFTER SUCCESSFULLY SET
            self.ui.MaxHumVal.setText(self.ui.MaxHumVal.text())
            self.ui.Set_Hum_btn.setDisabled(True)
            self.ui.SetMax_Hum_btn.setDisabled(False)

    # SET HUMIDTY MINIMUM TRIGGER VALUE
    def setMinHum(self):

        msg = QMessageBox()
        msg.setWindowTitle(f" Alert")
        msg.setText("Are You Sure ?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setInformativeText(f"Do you want to make changes to triggers threshold ?")
        msg.setDetailedText("Once you change the Min trigger threshold it will control the relay On/Off\n"
                            "make sure you what you are doing ! 🤓")
        msg.setIcon(QMessageBox.Question)
        ret = msg.exec_()

        if ret == QMessageBox.Yes:

            # CONFIRM IF MIN VALUE IS NOT EQUALS AND GREATER THAN MAX VALUE
            if int(self.ui.MaxHumVal.text()) != self.hum_start and self.hum_start < int(self.ui.MaxHumVal.text()):

                # SET MIN TRIGGER VALUE
                self.ui.MinHumVal.setText(f"{self.hum_start}")
                self.ui.Set_Hum_btn.setDisabled(False)
                self.ui.SetMin_Hum_btn.setDisabled(True)

            else:
                # IF IT IS  THEN DISPLAY POP UP MESSAGES AND DONT SET MIN TRIGGER VALUE
                msg.setText("MIN TRIGGER VALUE INVALID")
                msg.setWindowTitle(f" Alert")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setInformativeText(f"Hey the MAX trigger value can't be equal or Lesser than Min value")
                msg.setDetailedText("The Maximum Value should not be lesser and equals to Min Value \n"
                                    "for example you can only set to Trigger value as \n MIN:20 AND MAX 50 ")
                msg.setIcon(QMessageBox.Warning)
                ret = msg.exec_()
        else:
            # DISABLE SET BUTTONS AFTER SUCCESSFULLY SET
            self.ui.MinHumVal.setText(self.ui.MinHumVal.text())
            self.ui.Set_Hum_btn.setDisabled(True)
            self.ui.SetMin_Hum_btn.setDisabled(False)




   # CHECK IF THE CONDTION TO PUBLISH AND TURN ON RELAY 1
    def Temperature_Rly_On(self):

        # CHANGE TEXT STATUS OF RELAY 1 TO CONNECTED AND GREEN COLOR
        self.ui.Relay_1a.setStyleSheet("background:rgb(9, 255, 45)")
        self.ui.Relay_Status1a.setText("Connected !")
        self.ui.Relay_Status1a.setStyleSheet("color:rgb(9, 255, 45)")
        self.ui.Relay_1b.setStyleSheet("background:rgb(9, 255, 45)")
        self.ui.Relay_Status1b.setText("Connected !")
        self.ui.Relay_Status1b.setStyleSheet("color:rgb(9, 255, 45)")
    def Temperature_Rly_Off(self):

        # CHANGE TEXT STATUS OF RELAY 1 TO CONNECTED AND RED COLOR
        self.ui.Relay_1a.setStyleSheet("background:red")
        self.ui.Relay_Status1a.setText("Disconnected !")
        self.ui.Relay_Status1a.setStyleSheet("color:rgb(255, 238, 187)")
        self.ui.Relay_1b.setStyleSheet("background:red")
        self.ui.Relay_Status1b.setText("Disconnected !")
        self.ui.Relay_Status1b.setStyleSheet("color:rgb(255, 238, 187)")

    # CHECK IF THE CONDTION TO PUBLISH AND TURN ON RELAY 2
    def Humidity_Rly_On(self):
        # CHANGE TEXT STATUS OF RELAY 2 TO CONNECTED AND GREEN COLOR
        self.ui.Relay_2a.setStyleSheet("background:rgb(9, 255, 45)")
        self.ui.Relay_Status2a.setText("Connected")
        self.ui.Relay_Status2a.setStyleSheet("color:rgb(9, 255, 45)")
        self.ui.Relay_2b.setStyleSheet("background:rgb(9, 255, 45)")
        self.ui.Relay_Status2b.setText("Connected")
        self.ui.Relay_Status2b.setStyleSheet("color:rgb(9, 255, 45)")

    def Humidity_Rly_Off(self):
        # CHANGE TEXT STATUS OF RELAY 2 TO CONNECTED AND GREEN COLOR
        self.ui.Relay_2a.setStyleSheet("background:red")
        self.ui.Relay_Status2a.setText("Disconnected")
        self.ui.Relay_Status2a.setStyleSheet("color:rgb(255, 238, 187)")
        self.ui.Relay_2b.setStyleSheet("background:red")
        self.ui.Relay_Status2b.setText("Disconnected")
        self.ui.Relay_Status2b.setStyleSheet("color:rgb(255, 238, 187)")


    def setTemp(self):
        # ENABLE THE NAVIGATION TEMPERATURE  BTN
        self.ui.Up_Temp_btn.setDisabled(False)
        self.ui.Down_Temp_btn.setDisabled(False)

        # DISABLE THE SET BTN
        self.ui.SetMax_Temp_btn.setDisabled(True)
        # ENABLE THE OK BTN
        self.ui.Set_Temp_btn.setDisabled(False)

    # NAVIGATION BUTTON AND SET BUTTONS MANAGAEMENTS
    def SetBtn(self,press):

        if press == "Temperature":
            self.ui.Set_Temp_btn.setDisabled(True)
            self.ui.Up_Temp_btn.setDisabled(False)
            self.ui.Down_Temp_btn.setDisabled(False)
            self.ui.SetMax_Temp_btn.setDisabled(False)
            self.ui.SetMin_Temp_btn.setDisabled(False)
        else:
            self.ui.Set_Hum_btn.setDisabled(False)
            self.ui.Up_Hum_btn.setDisabled(False)
            self.ui.Down_Hum_btn.setDisabled(False)
            self.ui.SetMax_Hum_btn.setDisabled(False)
            self.ui.SetMin_Hum_btn.setDisabled(False)


   # ADDING NUMBER EVENT TO TEMP NAVIGATION BTN AND LCD DISPLAY

    def Temp_settings(self, nav):
        if nav == "Up":
            self.tem_start = self.tem_start + 1
            self.ui.lcdNumber.display(self.tem_start)
        else:
            self.tem_start = self.tem_start - 1
            self.ui.lcdNumber.display(self.tem_start)

        # ADDING NUMBER EVENT TO HUM NAVIGATION BTN AND LCD DISPLAY
    def Hum_settings(self, nav):
        if nav == "Up":
            self.hum_start = self.hum_start + 1
            self.ui.lcdNumber_2.display(self.hum_start)
        else:
            self.hum_start = self.hum_start - 1
            self.ui.lcdNumber_2.display(self.hum_start)

    def Previous_page(self):
        self.ui.home.setCurrentWidget(self.ui.Home)
        self.ui.PreviuosBtn.setDisabled(True)
        self.ui.NextBtn.setDisabled(False)
        self.ui.NextBtn.setStyleSheet('color: green')
        self.ui.PreviuosBtn.setStyleSheet('color: transparent')

    def Next_page(self):
        self.ui.PreviuosBtn.setDisabled(False)
        self.ui.NextBtn.setDisabled(True)
        self.ui.PreviuosBtn.setStyleSheet('color: green')
        self.ui.NextBtn.setStyleSheet('color: Transparent')
        self.ui.home.setCurrentWidget(self.ui.Sensor)

    def handleNoSignal(self):
        msg = QMessageBox()
        msg.setWindowTitle("No Signal")
        msg.setText(f"There have been no TCP packet transmisson since {1.5*keepalive} second")
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText(f"There have been no TCP packet transmisson since {1.5*keepalive} second")
        msg.setIcon(QMessageBox.Warning)
        app.exec_()

    def Handle_GPIO_21(self,payload):
        msg = QMessageBox()
        msg.setWindowTitle("GPIO 21 ALERT")
        msg.setText(f" GPIO_21 is  {payload}")
        msg.setInformativeText(f"There have been no TCP packet transmisson since {1.5 * keepalive} second")

        msg.setDefaultButton(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Critical)
        print(payload)
        app.exec_()



    # def read(self,pay):
    #    #self. GPIO_21(pay)
    # #    print(f"pay is {pay}")
    # #    self.thread = gpp()
    # def read(self,pay):
    #        print(f"my pay {pay}")
    #        worker = Worker()
    #        self.threadpool.start(worker)

if __name__ == "__main__":
    import PySide2
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()




    def on_connect(client, userdata, flag, rc):


        if rc == 0:

            print("Connected with result code" + str(rc) + str(flag))
            # IF CONNECTION IS CONFRIM THEN SUBSCRIBE TO ALL TOPIC
            for i in sus_:
                client.subscribe(i)
            # DELETE BEFORE DEPLOY JUST A TEST
            client.subscribe(PubRly1Topic)
            client.subscribe(PubRly2Topic)

        else:
            print("Bad Connection !!")


    def on_disconnect(client, userdata, rc):
            print("client disconnected" + str(rc))

            # THE METHOD WITH GIVE ALERT WHEN THERE IS NO SIGNAL AFTER
            #EXCEEDING THE KEEP ALIVE * 1.5
            window.handleNoSignal()
            #client.loop_stop()

    def on_message(client, userdata, message):

        topic = str(message.topic)
        message = str(message.payload.decode("utf-8"))
        print(topic + "-->" + message)

        if topic == "Nymea/Temp":
            window.Handle_Temperature(float(message))
        elif topic == "Nymea/Hum":
            window.Handle_Humidty(float(message))


        # BEFORE THE STATUS OF THE TEMPERATURE RELAY CHANGE ON THE GUI AFTER PUBLISH
        # WE NEED TO CONFIRM IF TRULY THE RELAY HAS STARTED WORKING
        # BY PUBLISHING TO THE BROKER WITH A  TOPIC
        # CHECK THE RELAY PIN STATE AND THEN PUBLISH TO THIS TOPIC
        # MAKE SURE TO PUBLISH "ON" or "OFF" FOR PIN CHECK  RESPECTIVELY

        elif topic == PubRly1Topic:
            if message == "ON":

                 window.Temperature_Rly_On()
                 print("TEMPERATURE RElAY HAS STARTED WORKING")
            else:

                window.Temperature_Rly_Off()
                print("TEMPERATURE RELAY HAS STOP WORKING")

        # BEFORE THE STATUS OF THE HUMIDTY RELAY CHANGE ON THE GUI AFTER PUBLISH
        # WE NEED TO CONFIRM IF TRULY THE RELAY HAS STARTED WORKING
        # BY PUBLISHING TO THE BROKER WITH A  TOPIC
        # CHECK THE RELAY PIN STATE AND THEN PUBLISH TO THIS TOPIC
        # MAKE SURE TO PUBLISH "ON" or "OFF" FOR PIN CHECK RESPECTIVELY
        elif topic == PubRly2Topic :
            if message == "ON":
                window.Humidity_Rly_On()
                print("HUMIDITY RElAY HAS STARTED WORKING")
            else:
                window.Humidity_Rly_Off()
                print("HUMIDITY RELAY HAS STOP WORKING")

        # WE NEED TO WAIT TO CONFIRM IF F1 RECEIVE FEEBACK
        # BEFORE THE BUTTON CHANGE  TO GREEN
        # YOU CALL A FUNCTION FROM OTHER CLIENT
        # OR USE A PAYLOAD LIKE "TRUE" TO CONFIRM
        elif topic == F1_Sub_Topic:
            #if message == "True"
                window.ui.F1btn.setStyleSheet(
                'border :2px ;background-color:rgb(0, 253, 82)')

        # WE SUBSCRIBE TO GPIO_21 PIN FOR STATUS CHECK
        elif topic == GPIO_21:
            if message == "LOW":
                window.Handle_GPIO_21(message)
            window.Handle_GPIO_21(message)
        else:
            sleep(1)


    def on_publish(client, userData, Mid):
        print("Publish successfully")

    def log(client, userdata,level,buf):
        print("log:", buf)


    try:

        client = mqqt.Client("Ayobami@")  # create a unique instance for your client
        # client.username_pw_set(user, password=password)    #set username and password
        client.on_connect = on_connect # attach function to callback
        client.on_log = log # attach function to callback
        client.on_disconnect = on_disconnect # attach function to callback
        client.on_message = on_message # attach function to callback
        client.on_publish = on_publish # attach function to callback
        client.connect(broker, port, keepalive)  # now connect

        client.loop_start() # make it continuous
    except:
        sleep(3)
        print("ERROR CONNECTING CHECK YOUR NETWORK AND BROKER SERVER")
    sys.exit(app.exec_())




