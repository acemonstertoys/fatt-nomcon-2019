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

"""Example to test all the buttons.

"""

import sys
import time

from authbox.api import BaseDispatcher
from authbox.config import Config
from authbox.timer import Timer

DEVNULL = open('/dev/null', 'r+')

class Dispatcher(BaseDispatcher):
  def __init__(self, config):
    super(Dispatcher, self).__init__(config)
    self.load_config_object('badge_reader', on_scan=self.badge_scan)

  def badge_scan(self, badge_id):
    print "Card ID:", badge_id
    return badge_id

def main(args):
  if not args:
    config_filename = 'RFID_Scanner.ini'
  else:
    config_filename = args[0]

  config = Config(config_filename)
  Dispatcher(config).run_loop()

if __name__ == '__main__':
  main(sys.argv[1:])

