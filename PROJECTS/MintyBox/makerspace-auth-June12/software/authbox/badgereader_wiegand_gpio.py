
# Copyright 2018 Ace Monster Toys. All Rights Reserved.
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

"""Wiegand based badge reader directly connected via GPIO
"""

from authbox.api import BaseDerivedThread, GPIO
import time

bits = ''
t = 15
timeout = t

# This new base class has been created because we need multiple input pins in use
# simultaneously.
class BaseGPIOPinThread(BaseDerivedThread):
  def __init__(self, event_queue, config_name, d0_pin, d1_pin, initial_output=GPIO.LOW):
    super(BaseGPIOPinThread, self).__init__(event_queue, config_name)

    self.d0_pin = d0_pin
    self.d1_pin = d1_pin

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)  # for reusing pins
    if self.d0_pin:
      GPIO.setup(self.d0_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if self.d1_pin:
      GPIO.setup(self.d1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class WiegandGPIOReader(BaseGPIOPinThread):
  """Badge reader hardware abstraction.

  A Wiegand GPIO badge reader is defined in config as:

    [pins]
    name = WiegandGPIOReader:3:5

  where 3 is the D0 pin (physical numbering), and 5 is the D1 pin (also 
  physical numbering).
  """
  def __init__(self, event_queue, config_name, d0_pin, d1_pin, on_scan=None):
    # presently, i've dropped bit_len as a parameter.  likely i'm going to
    # swap this around to make it so that you can pass a decoding format to
    # make it easier to work with different encoding schemes.
    super(WiegandGPIOReader, self).__init__(event_queue, config_name,
            int(d0_pin), int(d1_pin))
    self._on_scan = on_scan
    if self._on_scan:
        GPIO.add_event_detect(self.d0_pin, GPIO.FALLING, callback=self.decode)
        GPIO.add_event_detect(self.d1_pin, GPIO.FALLING, callback=self.decode)


  def _callback(self, unused_channel):
    """Wrapper to queue events instead of calling them directly."""
    if self._on_scan:
      self.event_queue.put((self._on_scan, self))

  def decode(self, channel):
      global bits
      global timeout
      # This was originally done using the bitstream package, but we've
      # switched back to this to minimize imports as well as calculate
      # arbitrary bit boundaries in the future.  bitstream also made
      # calculations more complex due to endianess issues.  When working
      # with the readers directly it's easier to just extract the stream
      # and then we can implement helper functions later to separate facility
      # code and id.
      if channel == self.d0_pin:
          bits = bits + "0"
      elif channel == self.d1_pin:
          bits = bits + "1"
      timeout = t


  def read_input(self):
    """

    Args:
      device: input device to listen to

    Returns:
      badge value as string
    """
    global bits
    global timeout

    while 1:
        if bits:
            timeout = timeout -1
            time.sleep(0.001)
            if len(bits) > 1 and timeout == 0:
                b = bits
                # As we use a global because of how we operate with interrupts
                # reset the value back when we are no longer grabbing input.
                bits = ''
                # With some wiegand readers it adds additional control parity
                # at the front/back of the stream, which are not used in our
                # code calculation, thus we need to strip the values
                start = 0 - len(bits) + 1

                # These are useful lines to expose for debugging problems in
                # the system
                #
                #Print out a visualization of the bitstream
                # print "Binary:",bits
                # print out a calculation of the value
                # print('Bits is {} bits in length'.format(len(bits)))
                # print('{:012X}'.format(int(b[start:-1], 2)))
                # print('{0:30b}'.format(int(b[start:-1], 2)))

                return '{:08X}'.format(int(b[start:-1], 2))
        else:
            time.sleep(0.001)


  def run_inner(self):
    line = self.read_input()
    self.event_queue.put((self._on_scan, line))
