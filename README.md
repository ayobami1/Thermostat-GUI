# Thermostat-GUI
install PyQt5 to run the code
i have created a Sample KPIs to test the input signals from an MQQT
Adjust each Functions of the KPIs to parse the signals datas
Pleaase go to the on_message method and check the Handle_GPIO_21 method
i want to make sure that if LOW message is receive it should not recurse
        # WE SUBSCRIBE TO GPIO_21 PIN FOR STATUS CHECK
        elif topic == GPIO_21:
            if message == "LOW":
                window.Handle_GPIO_21(message)
            window.Handle_GPIO_21(message)
        else:
            sleep(1)
