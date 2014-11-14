# -*- coding: utf-8 -*-
import yaml, importlib, signal, logging, output

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
      
    self.output = output.output(self.devices)
    
if __name__ == "__main__":
  m = Mapper("testmap.yaml")
  signal.pause()
