import time
import board
import busio
import usb_hid

from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from digitalio import DigitalInOut, Direction, Pull
from constants import *
from keypad import *
from keyconfig.macos import *
from keyconfig.windows import *
from keyconfig.colorsoff import *
#------------------------------------
for _ in range(10):
    print(" ")
print("  ============ NEW EXECUTION ============  ")
#------------------------------------
interfaces = [ MacosKeypad ,WindowsKeypad, ColorsOffKeypad ]
currentInterface = -1
#------------------------------------

# CS  : GP17 - 22
# SCLK: GP18 - 24
# MOSI: GP19 - 25
# ----- I2C -----
# INT : GP3  - 05 ? Not used!
# SDA : GP4  - 06
# SCL : GP5  - 07
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, BUTTON_COUNT, brightness=0.2, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
#------------------------------------
picoLED = DigitalInOut(board.GP25)
picoLED.direction = Direction.OUTPUT
picoLED.value = 0
#------------------------------------
timeDown = [-1] * BUTTON_COUNT
timeUp = [-1] * BUTTON_COUNT
waiting = [False] * BUTTON_COUNT
keypadButtonStates = [ timeDown, timeUp, waiting ]
#------------------------------------
def setKeyColour(pixel, colour):
    pixels[pixel] = (((colour >> 16) & 255), (colour >> 8) & 255, colour & 255)

def swapLayout():
    global currentKeypadConfiguration
    global currentInterface
    currentInterface = (currentInterface + 1) % len(interfaces)
    currentKeypadConfiguration = interfaces[currentInterface](kbd, layout, setKeyColour)
    currentKeypadConfiguration.introduce()

def read_button_states(x, y):
    pressed = [0] * BUTTON_COUNT
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                pressed[i] = 1
            else:
                pressed[i] = 0
    return pressed
#------------------------------------
def checkHeldForFlash(heldDownStartMillis):
    if heldDownStartMillis > 0:
        downTime = timeInMillis() - heldDownStartMillis
        picoLED.value = (downTime >= LONG_HOLD and downTime <= LONG_HOLD + 100) or (downTime >= EXTRA_LONG_HOLD and downTime <= EXTRA_LONG_HOLD + 100)
    else:
        picoLED.value = 0
currentKeypadConfiguration = KeypadInterface(kbd, layout, setKeyColour)
currentKeypadConfiguration.introduce()
#------------------------------------
while True:
    currentKeypadConfiguration.loop()

    pressed = read_button_states(0, BUTTON_COUNT)

    for keyIndex in range(BUTTON_COUNT):
        event = checkButton(keyIndex, pressed[keyIndex], keypadButtonStates, checkHeldForFlash)
        if event & EVENT_DOUBLE_PRESS:
             if keyIndex == 15:
                  swapLayout()
       
        currentKeypadConfiguration.handleEvent(keyIndex, event)
