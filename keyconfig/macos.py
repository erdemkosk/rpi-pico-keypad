import time
import usb_hid
from constants import *
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

class MacosKeypad():
    #--- OPTIONAL METHODS ---
    def openTerminal(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("TERMINAL")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        time.sleep(KEYBOARD_DELAY)
        
    def openZoomApp(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("ZOOM")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        time.sleep(5)
        self.keyboard.send(Keycode.COMMAND, Keycode.LEFT_CONTROL, Keycode.V)
        
    def openDiscordApp(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("DISCORD")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def openCalendarApp(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("CALENDAR")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def openVisualStudioCodeApp(self):
        self.keyboard.send(Keycode.COMMAND, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("VISUAL STUDIO CODE")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def incrementVolume(self):
        self.cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        
    def decrementVolume(self):
        self.cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        
    def muteVolume(self):
        self.cc.send(ConsumerControlCode.MUTE)
        
    def incrementBrightness(self):
        self.keyboard.send(Keycode.F15)
        time.sleep(KEYBOARD_DELAY)
        
    def decrementBrightness(self):
        self.keyboard.send(Keycode.F14)
        time.sleep(KEYBOARD_DELAY)
        
    def moveMainScreen(self):
        self.keyboard.send(Keycode.F11)
        time.sleep(KEYBOARD_DELAY)
        
    def macosIntro(self, frameIndex):
        global image
        frameArray = [10, 9, 5, 6, 7, 11, 15, 14, 13, 12, 8, 4, 0, 1, 2, 3]
        if frameIndex >= len(frameArray):
            return
        index = frameArray[frameIndex]
        self.setKeyColour(index, self.IMAGE[index])

    #------------------------
    #--- REQUIRED METHODS ---
    IMAGE = [
        COLOUR_RED, COLOUR_RED, COLOUR_RED, COLOUR_RED,
        COLOUR_DARK_YELLOW, COLOUR_DARK_YELLOW, COLOUR_DARK_VIOLET, COLOUR_DARK_VIOLET,
        COLOUR_DARK_BLUE, COLOUR_DARK_GREEN, COLOUR_WHITE, COLOUR_WHITE,
        COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE
    ]

    def loop(self):
        if self.startAnimationTime > 0:
            estimatedFrame = int((timeInMillis() - self.startAnimationTime) / (ANIMATION_FRAME_MILLIS * 2))
            if estimatedFrame > self.currentFrame:
                # render new animation frame
                self.macosIntro(self.frameIndex)
                self.frameIndex += 1
                # print("  ~~> Animation frame: ", estimatedFrame)
                self.currentFrame = estimatedFrame
                if self.frameIndex > self.maxFrame:
                    self.startAnimationTime = -1

    def __init__(self, keyboard, keyboardLayout, setKeyColour):
        self.setKeyColour = setKeyColour
        self.keyboard = keyboard
        self.keyboardLayout= keyboardLayout
        self.cc = ConsumerControl(usb_hid.devices)

    def introduce(self):
        self.resetColours(COLOUR_OFF)
        self.startAnimationTime = timeInMillis()
        self.currentFrame = -1
        self.maxFrame = 16
        self.frameIndex = 0

    def resetColours(self, colours):
        for key in range(BUTTON_COUNT):
            if isinstance(colours, int):
                self.setKeyColour(key, colours)
            elif len(colours) == BUTTON_COUNT:
                self.setKeyColour(key, colours[key][0])

    def handleEvent(self, index, event):
        if event & EVENT_SINGLE_PRESS:
            if index == 0:
                self.openZoomApp()
            elif index == 1:
                self.openVisualStudioCodeApp()
            elif index == 2:
                self.openTerminal()
            elif index == 3:
                self.openCalendarApp()
            elif index == 4:
                self.incrementVolume()
            elif index == 5:
                self.decrementVolume()
            elif index == 6:
                self.incrementBrightness()
            elif index == 7:
                self.decrementBrightness()
            elif index == 8:
                self.muteVolume()
            elif index == 9:
                self.moveMainScreen()
    #------------------------
