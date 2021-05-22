import time
from constants import *
from adafruit_hid.keycode import Keycode

class WindowsKeypad():

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
        COLOUR_DARK_YELLOW, COLOUR_DARK_YELLOW, COLOUR_DARK_VIOLET, COLOUR_DARK_VIOLET,
        COLOUR_DARK_BLUE, COLOUR_WHITE, COLOUR_DARK_YELLOW, COLOUR_WHITE,
        COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE, COLOUR_DARK_YELLOW
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
        if event & EVENT_SINGLE_PRESS:
            if index == 0:
                print("test")
                
    #------------------------
