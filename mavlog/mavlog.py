# -*- coding: utf-8 -*-

"""MAVLog.

Usage:
  mavlog.py --fcu <fcu_device> --log <log_device> --format <format>
  mavlog.py
  
Options:
  -h --help     Show this screen.
  --version     Show version.
  --fcu=<fcu_device>  Serial port for flight controller [default: /dev/ttyACM0].
  --log=<log_device>  Serial port to be logged [default: /dev/ttyUSB0].
  --format=<format>   Format for logged data [default: csv].

"""

from docopt import docopt
import logging, threading, signal, sys, time
from autopilot_device import AutopilotDevice
from log_device import LoggingDevice

class MAVLog:
  def __init__(self, fcu_device, log_device, format):
    self.format = format
    self.threads = []
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting MAVLog")
    logger.info("Autopilot on %s" % fcu_device)
    logger.info("Logged device is %s" % log_device)
    logger.info("Format is %s" % format)
    
    self.threads.append(AutopilotDevice(fcu_device))
    #self.threads.append(LoggingDevice(log_device))
    
    signal.signal(signal.SIGINT, self.signal_handler)
    signal.pause()
    
  def signal_handler(self, signal, frame):
    logger = logging.getLogger(__name__)
    logger.info("Shutting down...")
    [thread.stop() for thread in self.threads]
    time.sleep(0.1)
    sys.exit(0)

if __name__ == '__main__':
  arguments = docopt(__doc__, version='MAVLog 0.1')

  app = MAVLog(arguments['--fcu'], arguments['--log'], arguments['--format'])