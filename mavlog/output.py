# -*- coding: utf-8 -*-
import datetime, time
import logging, threading
from jinja2 import Template
import os

class output:
  def __init__(self, devices, mapping):
    self.running = True
    self.log_path = mapping['log_path']

    self.f_name = self.generate_filename()
    self.f = open(self.f_name, 'a+', 1)
    self.devices = devices
    self.rate = mapping['rate']
    self.template_string = mapping['template']
    
    self.f.write(self.template_string + "\n")
    self.logger = logging.getLogger(__name__)
    self.logger.info("Started with %s" % self.f_name)
    
    self.process()

  def stop(self):
    self.running = False
    self.logger.info(__name__ + " shutdown")
    
  def generate_filename(self):
    return self.log_path + "/" + "Log." + str(self.next_number()).zfill(3) + ".csv"

  def next_number(self):
    highest = 1

    for fn in os.listdir(self.log_path):
      current = int(fn.split('.')[1])
      if current >= highest:
        highest = current + 1
    
    return highest    

  def template(self, time, data):
    templ = Template(self.template_string)
    combined = {'time': time}
    for device in data:
      #print data[device].get_data()
      combined[device] = data[device].get_data()
    return templ.render(combined)
    
  def process(self):
    lastTick = time.time()
    while self.running:
      if (time.time() - lastTick) > (1.0/self.rate):
        self.f.write(self.template(time.time(), self.devices) + "\n")
        lastTick = time.time()
      
      time.sleep(0.001)
