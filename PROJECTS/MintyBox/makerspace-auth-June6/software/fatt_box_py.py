#!/usr/bin/python
#
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import JSON
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

import subprocess

from authbox.api import *
from authbox.config import Config
from authbox.timer import Timer

from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

DEVNULL = open('/dev/null', 'r+')


GPIO.setup(11, GPIO.IN)
GPIO.setup(38, GPIO.IN)


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/100.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)



class Dispatcher(BaseDispatcher):
  def __init__(self, config):
    super(Dispatcher, self).__init__(config)

    self.load_config_object('j1', on_down=self.on_button_down)
    self.load_config_object('badge_reader', on_scan=self.badge_scan)

    self.load_config_object('buzzer')
    self.load_config_object('relays')
    # This may be a MultiProxy, which makes this easier.
    self.relays.on()
    self.relay_value = True

    # Run fans for 10 seconds on startup
    #self.relay_timer = Timer(self.event_queue, 'relay_timer', self.toggle_relays)
    #self.relay_toggle_interval = 10
    #self.relay_timer.set(self.relay_toggle_interval)
    #self.threads.extend([self.relay_timer])





  def badge_scan(self, badge_id):
    badge_hex = badge_id
    badge_int = int(badge_hex, 16)
    print "Badge ID", badge_int
    theaterChase(strip, Color(255,0,0), 50, 50)
    colorWipe(strip, Color(0,0,0),1)
    

  def toggle_relays(self, source):
    #print "Toggle relay value", self.relay_value
    if self.relay_value:
      print "self.relay_value:", self.relay_value
      colorWipe(strip, Color(0,255,0), 10)
      self.relays.off()
      self.relay_value = False
    else:
      print "self.relay_value:", self.relay_value
      colorWipe(strip, Color(0,0,0), 5)
      self.relays.on()
      self.relay_value = True
    #self.relay_timer.set(self.relay_toggle_interval)


  def on_button_down(self, source):
    print "Button down", source
    self.toggle_relays(source)
    source.on()
    time.sleep(0.3)
    source.off()


def main(args):
  config_filename = 'qa.ini'
  config = Config(config_filename)
  Dispatcher(config).run_loop()
  
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()
  


if __name__ == '__main__':
  # Process arguments

  # Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  strip.begin()
  

  main(sys.argv[1:])

  
  colorWipe(strip, Color(0,0,0),1)
  GPIO.cleanup()
    
