
from animations.stars import Stars
from animations.staticlight import StaticLight
from neopixel import *
from animations.fire import Fire
from animations.strobe import Strobe
from animations.fairy import Fairy
from constants import *
from wraparoundstrip import WrapAroundStrip
import time

print LED_COUNT
#millis = lambda: int(round(time.time() * 1000))

ticks = 0

# Create NeoPixel object with appropriate configuration.
strip = WrapAroundStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

stars = Stars(strip, 15, 1, 255, 255, 255)
#150-225
#light = StaticLight(strip, 150, 225, 255, 150, 150)
light = StaticLight(strip, 0, LED_COUNT, 200, 160, 160)
#light = StaticLight(strip, 0, LED_COUNT, 63, 12, 0)
fire = Fire(strip, 0.1, 1, 3, 6)
fire2 = Fire(strip, 1, 100, 7, 10)
fire3 = Fire(strip, 1, 250, 15, 20)
strobe = Strobe(strip, 0, LED_COUNT, 1, 1, 255, 255, 255)
fairy = Fairy(strip, 430, 50, 10.5, 255, 180, 0)
fairy2 = Fairy(strip, 10, 5, 0.1, 100, 100, 255)
absoluteStart = time.time()
totalSleepTime = 0
#for i in range(0, 300):
while 1:
    start = time.time()
    light.animate()
    #stars.animate()
    #light.animate()
    #fire.animate()
    #fire2.animate()
    #fire3.animate()
    #strobe.animate()
    #fairy.animate()
    #fairy2.animate()

    strip.show()
    ticks += 1
    sleepTime = 0.033 - (time.time() - start)
    if(sleepTime < 0):
        sleepTime = 0
    totalSleepTime += sleepTime
    time.sleep(sleepTime)
    
absoluteEnd = time.time()
print "Ticks per second: " + str(ticks / (absoluteEnd - absoluteStart))
print "Proportion spent sleeping: " + str(totalSleepTime / (absoluteEnd - absoluteStart))
