# -*- coding: utf-8 -*-
import os, sys, yaml, importlib, signal, logging, output

class Mapper:

  def __init__(self, mapfile):
    self.mapping = yaml.load(open(mapfile))
    self.devices = {}
    
    logging.basicConfig(level=logging.INFO)
    print self.mapping
    
    for name in self.mapping['devices']:
      options = self.mapping['devices'][name]
      
      mod = importlib.import_module('devices.' + options['type'])
      klass = getattr(mod, options['type'])
      self.devices[name] = klass(options)
      print self.devices[name]
      
    self.output = output.output(self.devices, self.mapping)

def setup_bbb_serial():
  os.system("echo BB-UART2 > /sys/devices/bone_capemgr.*/slots")
  os.system("echo BB-UART4 > /sys/devices/bone_capemgr.*/slots")

if __name__ == "__main__":
  setup_bbb_serial()
  m = Mapper(sys.argv[1])
  signal.pause()
