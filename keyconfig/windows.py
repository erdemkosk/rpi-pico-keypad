import time
import usb_hid
from constants import *
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

class WindowsKeypad():
    
    def openVisualStudioCodeApp(self):
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("VISUAL")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
    
    def openSteamApp(self):
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("STEAM")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def openEpicStoreApp(self):
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("EPIC")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def openWeModeApp(self):
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("WEM")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def openOpera(self):
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("OPERA")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def openTorrentApp(self):
        self.keyboard.send(Keycode.ALT, Keycode.SPACE)
        time.sleep(KEYBOARD_DELAY)
        self.keyboardLayout.write("QBIT")
        time.sleep(KEYBOARD_DELAY)
        self.keyboard.send(Keycode.ENTER)
        
    def closeAll(self):
        self.keyboard.send(Keycode.ALT, Keycode.F4)
        time.sleep(KEYBOARD_DELAY)
        
    def incrementVolume(self):
        self.cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        
    def decrementVolume(self):
        self.cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        
    def muteVolume(self):
        self.cc.send(ConsumerControlCode.MUTE)

    def windowsIntro(self, frame):
        if frame >= 4:
            return
        for row in range(4):
            index = (row * 4) + frame
            self.setKeyColour(index, self.IMAGE[index])
    #------------------------
    #--- REQUIRED METHODS ---
    IMAGE = [
        COLOUR_DARK_VIOLET, COLOUR_DARK_VIOLET, COLOUR_DARK_VIOLET, COLOUR_DARK_VIOLET,
        COLOUR_BLUE, COLOUR_GREEN, COLOUR_DARK_VIOLET, COLOUR_DARK_VIOLET,
        COLOUR_DARK_YELLOW, COLOUR_DARK_YELLOW, COLOUR_RED, COLOUR_RED,
        COLOUR_RED, COLOUR_RED, COLOUR_RED, COLOUR_RED
    ]

    def loop(self):
        if self.startAnimationTime > 0:
            estimatedFrame = int((timeInMillis() - self.startAnimationTime) / (ANIMATION_FRAME_MILLIS * 2))
            if estimatedFrame > self.currentFrame:
                # render new animation frame
                self.windowsIntro(self.frameIndex)
                self.frameIndex += 1
                # print("  ~~> Animation frame: ", estimatedFrame)
                self.currentFrame = estimatedFrame
                if self.frameIndex >= self.maxFrame:
                    self.startAnimationTime = -1



    def __init__(self, keyboard, keyboardLayout, setKeyColour):
        self.setKeyColour = setKeyColour
        self.keyboard = keyboard
        self.keyboardLayout = keyboardLayout
        self.cc = ConsumerControl(usb_hid.devices)

    def introduce(self):
        self.resetColours(COLOUR_OFF)
        self.startAnimationTime = timeInMillis()
        self.currentFrame = -1
        self.maxFrame = 4
        self.frameIndex = 0

    def resetColours(self, colours):
        for key in range(BUTTON_COUNT):
            if isinstance(colours, int):
                self.setKeyColour(key, colours)
            elif len(colours) == BUTTON_COUNT:
                self.setKeyColour(key, colours[key][0])

    def handleEvent(self, index, event):
        if event & EVENT_KEY_DOWN:
            if index == 8:
                self.incrementVolume()
            elif index == 9:
                self.decrementVolume()
                
        if event & EVENT_SINGLE_PRESS:
            if index == 4:
                self.muteVolume()
            if index == 5:
                self.closeAll()
            if index == 10:
                self.openSteamApp()
            if index == 11:
                self.openEpicStoreApp()
            if index == 12:
                self.openOpera()
            if index == 13:
                self.openTorrentApp()
            if index == 14:
                self.openWeModeApp()
            if index == 15:
                self.openVisualStudioCodeApp()
                
    #------------------------
