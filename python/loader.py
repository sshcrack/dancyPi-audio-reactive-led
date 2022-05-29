from controller.ledstrip.ledStripController import LEDStripController

controllerList = [
    LEDStripController
]

for controller in controllerList:
    classConstructed = controller("rpi", gui=True)
    while True:
        classConstructed.run()
