# -*- coding: utf-8 -*-
import serial
import logging, threading

class serial_generic:
  
  def __init__(self, options):
    self.stopped = threading.Event()
    self.data = {}
    self.data['errors'] = 0
    
    options['baud'] = 115200 if not 'baud' in options else options['baud']

    self.conn = serial.serial_for_url(options['port'], options['baud'], timeout=0.1)
    
    self.thread = threading.Thread(target = self.read)
    self.thread.daemon = True
    self.thread.start()
    
  def get_data(self, blocking = False):
    # Not recommended for use outside testing
    if blocking:
      while self.data == {'errors': 0}:
        pass
        
    return self.data
    
  def stop(self):
    self.stopped.set()
    self.thread.join()
    
  def read(self):
    logger = logging.getLogger(__name__)
    
    while not self.stopped.is_set():
      msg = self.conn.readline().strip()
      if msg:
        self.process(msg)
      
    logger.info("Serial device shutdown")
    
  def process(self, msg):
    # In python this is atomic
    pass
