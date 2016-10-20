try:
    from neopixel import *
except ImportError:
    from ...DummyLibrary.neopixel import *
from ..plugins import Animation, AnimationParameter
import json


class Fairy(Animation):
    
    def __init__(self, id, **kwargs):
        super().__init__(id, kwargs)
        self.start = kwargs['start']
        self.width = kwargs['width']
        self.speed = kwargs['speed']
        self.color = kwargs['color']

        self.tick = 0

    def animate(self, delta, strip):
        self.tick += delta
        dist = ((self.tick * self.speed) + self.start)
        fraction = dist - (int(dist))
        dist = int(dist)
        startfraction = 1 - fraction
        strip.setPixelColor(dist, rgb=[int(startfraction * x) for x in self.color])
        for i in range(1, self.width):
            strip.setPixelColor(dist + i, rgb=self.color)
        strip.setPixelColor(dist + self.width, rgb=[int(fraction * x) for x in self.color])

    @staticmethod
    def getparams():
        return [
            AnimationParameter('start', description="Location at which this fairy starts",
                               type='integer', default=0, optional=True),
            AnimationParameter('width', description="Width of the fairy, in number of pixels",
                               type='float', optional=False),
            AnimationParameter('speed', description="Speed of movement, in pixels per second",
                               type='float', optional=False),
            AnimationParameter('color', description='Color of the fairy',
                               type='color', optional=False)
        ]

    @staticmethod
    def getanimationinfo():
        return {
            'name': 'Fairy',
            'description': 'A light that moves continously around the LED strip'
        }