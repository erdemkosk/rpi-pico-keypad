import time
from constants import *
from adafruit_hid.keycode import Keycode

class ColorsOffKeypad():
    #--- OPTIONAL METHODS ---

    def colorsIntro(self, frame):
        if frame >= 4:
            return
        for row in range(4):
            index = (frame * 4) + row
            self.setKeyColour(index, self.IMAGE[index])

    #------------------------
    #--- REQUIRED METHODS ---
    IMAGE = [
            COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF,
            COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF,
            COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF,
            COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF
        ]

    def loop(self):
        if self.startAnimationTime > 0:
            estimatedFrame = int((timeInMillis() - self.startAnimationTime) / (ANIMATION_FRAME_MILLIS * 2))
            if estimatedFrame > self.currentFrame:
                # render new animation frame
                self.colorsIntro(self.frameIndex)
                self.frameIndex += 1
                # print("  ~~> Animation frame: ", estimatedFrame)
                self.currentFrame = estimatedFrame
                if self.frameIndex >= self.maxFrame:
                    self.startAnimationTime = -1

    def __init__(self, keyboard, keyboardLayout, setKeyColour):
        self.setKeyColour = setKeyColour
        self.keyboard = keyboard
        self.keyboardLayout= keyboardLayout

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
        if not event & EVENT_SINGLE_PRESS:
            return

    #------------------------
