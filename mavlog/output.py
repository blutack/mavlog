# -*- coding: utf-8 -*-
import datetime, time
import logging, threading

class output:
  def __init__(self, devices, rate=10):
    self.running = True
    self.f_name = self.generate_filename()
    self.f = open(self.f_name, 'a+')
    self.devices = devices
    self.rate = rate
    
    self.logger = logging.getLogger(__name__)
    self.logger.info("Started with %s" % self.f_name)
    
    self.process()

  def stop(self):
    self.running = False
    self.logger.info(__name__ + " shutdown")
    
  def generate_filename(self):
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + " Log.csv"
    
  def template(self):
    pass
    
  def process(self):
    lastTick = time.time()
    while self.running:
      if (time.time() - lastTick) > (1.0/self.rate):
        print time.time()
        lastTick = time.time()
      
      time.sleep(0.001)