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
cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
cc = ConsumerControl(usb_hid.devices)
def colourwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
def read_button_states(x, y):
    pressed = [0] * 16
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
held = [0] * 16
while True:
    pressed = read_button_states(0, 16)

    if pressed[0]:
        pixels[0] = (255, 255, 255)  # Zoom open

        if not held[0]:
            kbd.send(Keycode.COMMAND, Keycode.SPACE)
            time.sleep(0.1)
            layout.write("ZOOM")
            kbd.send(Keycode.ENTER)
            time.sleep(5)
            
            kbd.send(Keycode.COMMAND, Keycode.LEFT_CONTROL, Keycode.V)
            held[0] = 1

    elif pressed[1]:
        pixels[1] = (255, 255, 255)  # zoom invite

        if not held[1]:  
            kbd.send(Keycode.COMMAND, Keycode.SPACE)
            time.sleep(0.1)
            layout.write("VISUAL STUDIO CODE")
            kbd.send(Keycode.ENTER)
            held[1] = 1

    elif pressed[2]:
        pixels[2] = (255, 255, 255)  # termianl

        if not held[2]:
            kbd.send(Keycode.COMMAND, Keycode.SPACE)
            time.sleep(0.1)
            layout.write("TERMINAL")
            kbd.send(Keycode.ENTER)
            held[2] = 1

    elif pressed[3]:
        pixels[3] = (255, 255, 255)  # calender

        if not held[3]:
            kbd.send(Keycode.COMMAND, Keycode.SPACE)
            time.sleep(0.1)
            layout.write("CALENDAR")
            kbd.send(Keycode.ENTER)
            held[3] = 1

    elif pressed[4]:
        pixels[4] = (255, 255, 255)  # volume increment

        if not held[4]:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            time.sleep(0.1)
            
    elif pressed[5]:
        pixels[5] = (255, 255, 255)  # volume decrement

        if not held[5]:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            time.sleep(0.1)

    elif pressed[6]:
        pixels[6] = (255, 255, 255)  # incrase brightness

        if not held[6]:
            kbd.send(Keycode.F15)
            time.sleep(0.1)
    
    elif pressed[7]:
        pixels[7] = (255, 255, 255)  # decresse brightness

        if not held[7]:
            kbd.send(Keycode.F14)
            time.sleep(0.1)

    elif pressed[8]:
        pixels[8] = (255, 255, 255)  # show empty main screen

        if not held[8]:
            kbd.send(Keycode.F11)
            held[8] = 1
            
    elif pressed[9]:
        pixels[9] = colourwheel(9 * 16)  # Map pixel index to 0-255 range

        if not held[9]:
            layout.write("mpc stop")
            kbd.send(Keycode.ENTER)
            held[9] = 1

    elif pressed[10]:
        pixels[10] = colourwheel(10 * 16)  # Map pixel index to 0-255 range

        if not held[10]:
            layout.write("rad2")
            kbd.send(Keycode.ENTER)
            held[10] = 1
            
    elif pressed[11]:
        pixels[11] = colourwheel(11 * 16)  # Map pixel index to 0-255 range

        if not held[11]:
            layout.write("mpc stop")
            kbd.send(Keycode.ENTER)
            held[11] = 1

    elif pressed[12]:
        pixels[12] = colourwheel(12 * 16)  # Map pixel index to 0-255 range

        if not held[12]:
            layout.write("ssh pi\"192.168.9.97 picade_switch")
            kbd.send(Keycode.ENTER)
            held[12] = 1
            
    elif pressed[13]:
        pixels[13] = colourwheel(13 * 16)  # Map pixel index to 0-255 range

        if not held[13]:
            layout.write("mpc toggle")
            kbd.send(Keycode.ENTER)
            held[13] = 1

    elif pressed[14]:
        pixels[14] = colourwheel(14 * 16)  # Map pixel index to 0-255 range

        if not held[14]:
            layout.write("rad1")
            kbd.send(Keycode.ENTER)
            held[14] = 1
            
    elif pressed[15]:
        pixels[15] = colourwheel(15 * 16)  # Map pixel index to 0-255 range

        if not held[15]:
            layout.write("mpc toggle")
            kbd.send(Keycode.ENTER)
            held[15] = 1
    
    else:  # Released state
        for i in range(16):
            # Turn pixels off
            pixels[i] = colourwheel(i * 16)
            held[i] = 0  # Set held states to off
        time.sleep(0.1) # Debounce
