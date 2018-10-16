
import ustruct
from machine import ADC, Pin, PWM, UART
import utime

uart = UART(2) # UART(2) RX16 TX17
uart.init(38400, bits=8, parity=None, stop=1)

input, servomotor, pwm, digital= 0, 1, 2, 3 # pinType

lastDataReceivedTime, timerCheckUpdate = utime.ticks_ms(), utime.ticks_ms()

class ArduinoPin:
    def __init__(self, index, type, state = False):
        self.pin = None
        self.index = index
        self.type = type
        self.state = state

    def pulse(self, pulseWidth):
        self.pin.value(1)
        utime.sleep_ms(pulseWidth)
        self.pin.value(0)

    def servo(self, angle):
        if (angle != 255):
            self.pulse((angle * 10) + 600);

arduinoPins = [
    ArduinoPin(21, input),
    ArduinoPin(22, input),
    ArduinoPin(2, input),
    ArduinoPin(4, input),
    ArduinoPin(15, servomotor),
    ArduinoPin(13, pwm),
    ArduinoPin(12, pwm),
    ArduinoPin(14, servomotor),
    ArduinoPin(25, servomotor),
    ArduinoPin(26, pwm),
    ArduinoPin(05, digital),
    ArduinoPin(23, digital),
    ArduinoPin(19, digital),
    ArduinoPin(18, digital),
]

arduinoAdcs = [
    [ADC(Pin(36)), 0], 
    [ADC(Pin(39)), 0], 
    [ADC(Pin(32)), 0], 
    [ADC(Pin(33)), 0], 
    [ADC(Pin(34)), 0], 
    [ADC(Pin(35)), 0]
]

def resetPins():
    for ArduinoPin in arduinoPins:
        if ArduinoPin.type != input:
            ArduinoPin.pin = Pin(ArduinoPin.index, Pin.OUT);
            if (ArduinoPin.type == servomotor):
                ArduinoPin.state = 255
                ArduinoPin.servo(255)
            else:
                ArduinoPin.state = 0
                ArduinoPin.pin.value(0)
        else:
            ArduinoPin.pin = Pin(ArduinoPin.index, Pin.IN);

def ScratchBoardSensorReport(sensor, value):
    buf = bytearray(1)
    ustruct.pack_into("B", buf, 0, 128 | ((sensor & 15) << 3) | ((value >> 7) & 7))
    uart.write(buf)
    ustruct.pack_into("B", buf, 0, value & 127)
    uart.write(buf)

def sendSensorValues():
    # ADC 去噪
    for adc in arduinoAdcs:
        readings = []
        for i in range(5):
            readings.append(adc[0].read())
        readings.sort(reverse=True)
        adc[1] = readings[2]
    
    # Report All
    for i in range(len(arduinoAdcs)):
        ScratchBoardSensorReport(i, arduinoAdcs[i][1])
        
    if arduinoPins[2].pin.value() == 1:
        ScratchBoardSensorReport(6, 1023)
    else:
        ScratchBoardSensorReport(6, 0)
        
    if arduinoPins[3].pin.value() == 1:
        ScratchBoardSensorReport(7, 1023)
    else:
        ScratchBoardSensorReport(7, 0)
        
def sendUpdateServomotors():
    for ArduinoPin in arduinoPins:
        if (ArduinoPin.type == servomotor):
            ArduinoPin.servo(ArduinoPin.state)

def updateActuator(index):
    if (arduinoPins[index].type == digital):
        arduinoPins[index].pin.value(arduinoPins[index].state)
    elif (arduinoPins[index].type == pwm):
        PWM(arduinoPins[index].pin, freq = 50000, duty = arduinoPins[index].state)

def checkScratchDisconnection():
    global lastDataReceivedTime
    if (utime.ticks_ms() - lastDataReceivedTime > 1000):
        resetPins()
        sendSensorValues()
        lastDataReceivedTime = utime.ticks_ms()

actuatorHighByte, actuatorLowByte, readingSM = 0, 0, 0

def readSerialPort():
    global actuatorHighByte, actuatorLowByte, readingSM
    recvlen = uart.any()
    if recvlen > 0:
        char = uart.read(1)
        if (readingSM == 0):
            actuatorHighByte = char[0]
            if (actuatorHighByte >= 128):
                readingSM = 1
        elif (readingSM == 1):
            actuatorLowByte = char[0]
            if (actuatorLowByte < 128):
                readingSM = 2
            else:
                readingSM = 0

        if(readingSM == 2):
            lastDataReceivedTime = utime.ticks_ms()
            pinPos = ((actuatorHighByte >> 3) & 0x0F)
            newVal = ((actuatorHighByte & 0x07) << 7) | (actuatorLowByte & 0x7F)

            if(arduinoPins[pinPos].state != newVal):
                arduinoPins[pinPos].state = newVal
                updateActuator(pinPos)

            readingSM = 0
    else:
        checkScratchDisconnection()

resetPins()

while True:
    readSerialPort()
    if (utime.ticks_ms() - timerCheckUpdate >= 250):
        sendUpdateServomotors()
        sendSensorValues()
        timerCheckUpdate = utime.ticks_ms()
        


