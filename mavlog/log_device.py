# -*- coding: utf-8 -*-
import serial
import logging, threading

class LoggingDevice:
  
  def __init__(self, device, baud=115200):
    self.running = True
    self.conn = serial.Serial(device, baud, timeout=1)
    self.thread = threading.Thread(target = self.process)
    self.thread.daemon = True
    self.thread.start()
    
  def stop(self):
    self.running = False
    
  def process(self):
    logger = logging.getLogger(__name__)
    
    while self.running:
      msg = self.conn.readline()
      if msg:
        logger.info(msg)
      
    logger.info("Logging device shutdown")