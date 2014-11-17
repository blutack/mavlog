# -*- coding: utf-8 -*-
import datetime, time
import logging, threading
from jinja2 import Template

class output:
  def __init__(self, devices, mapping):
    self.running = True
    self.f_name = self.generate_filename()
    self.f = open(self.f_name, 'a+')
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
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + " Log.csv"
    
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
        print self.template(time.time(), self.devices)
        lastTick = time.time()
      
      time.sleep(0.001)
