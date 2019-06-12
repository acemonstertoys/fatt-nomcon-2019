#!/usr/bin/python
#
# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Basic Door controler

This utility provides basic relay triggering when an authorized tag has been
scanned.

The intention is that users will use the onboard 12v power in series with one of
the available relays:

+-----+      +-----+
|POWER|  12v |RELAY|
|     +------+     |
|     |      |     |
+-+---+      +--+--+
  |GND          |12v
  |     DOOR    |
  |    STRIKE   |
  |    +----+   |
  |    |    |   |
  |    |    |   |
  |    |    |   |
  +----+    +---+
       |    |
       |    |
       +----+

No other interaction besides the presentation of an RFID fob is required.

While this could potentially be powered by one of the 12v lines used by the
pushbutton LEDs, this avoids any need for a flyback diode on the relay.
"""

import atexit
import os
import sys
import subprocess
import shlex

from authbox.api import BaseDispatcher, GPIO
from authbox.config import Config
from authbox.timer import Timer

DEVNULL = open('/dev/null', 'r+')

class Dispatcher(BaseDispatcher):
  def __init__(self, config):
    super(Dispatcher, self).__init__(config)

    self.authorized = False
    self.load_config_object('badge_reader', on_scan=self.badge_scan)
    self.load_config_object('enable_output')
    self.load_config_object('buzzer')
    self.door_timer = Timer(self.event_queue, 'door_timer', self.abort)
    self.noise = None
    self.threads.extend([self.door_timer])

  def _get_command_line(self, section, key, format_args):
    """Constructs a command line, safely.

    The value can contain {key}, {}, and {5} style interpolation:
      - {key} will be resolved in the config.get; those are considered safe and
        spaces will separate args.
      - {} works on each arg independently (probably not what you want).
      - {5} works fine.
    """
    value = self.config.get(section, key)
    pieces = shlex.split(value)
    return [p.format(*format_args) for p in pieces]

  def badge_scan(self, badge_id):
    """Executes scanning of a users badge.

    Note:
        "command" below will execute a shell operation defined via the
        configuration option in authboxrc.  This script should exit with a zero
        error code on a successful authorization and non-zero on a failure.

    Args:
        badge_id: The badge value as passed directly by the reader.
    """

    print("Badge scanned - {}".format(badge_id))
    try:
        # Malicious badge "numbers" that contain spaces require this extra work.
        command = self._get_command_line('auth', 'command', [badge_id])
        rc = subprocess.call(command)
    except IOError as e:
        print("Error, command %s not found" % e.filename)
        # TODO timeout
        # TODO test with missing command
    
    if rc == 0:
      # If the return code on the previous command exited with a 0 error code,
      # then buzz the buzzer, set the authorized propety on our object to true
      # and the badge_id property to the value returned by the badge reader.
      self.authorized = True
      self.badge_id = badge_id
      # Read the "auth" section of authboxrc and retieve the duration setting.
      # If there is no value set, default to 30 seconds.
      self.door_timer.set(self.config.get_int_seconds('auth', 'duration', '30s'))
      # Enable the pin defined in our "enable_output" configuration definition
      # (defined in the __init__ of this class), setting it to an "on" value.
      self.enable_output.on()

    else:
      # If the command did not return a zero error code, then buzz the buzzer,
      # terminate any sounds which may be playing, determine from the "enable"
      # value in the "sounds" section of the authboxrc config if sounds should
      # be enabled.
      # If sounds are to be enabled, then also within the "sounds" section of
      # the authboxrc config file, determine the audio file based on the
      # value of "sad_filename" and supply it to the command defined by the
      # value of "command".
      if self.noise:
        self.noise.kill()
      if self.config.get('sounds', 'enable') == '1':
        sound_command = self._get_command_line('sounds', 'command', [self.config.get('sounds', 'sad_filename')])
        self.noise = subprocess.Popen(sound_command, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)

  def abort(self, source):
    """Perform operations on authorization timeout.

    Args:
        source: the device a user attempted to authorize for use, but was
            denied
    """
    print "Abort", source
    self.authorized = False
    self.enable_output.off()
    self.buzzer.off()
    if self.noise:
      self.noise.kill()
      self.noise = None



def main(args):
  atexit.register(GPIO.cleanup)

  if not args:
    root = '~'
  else:
    root = args[0]

  config = Config(os.path.join(root, 'doorauth.ini'))
  Dispatcher(config).run_loop()

if __name__ == '__main__':
  main(sys.argv[1:])
