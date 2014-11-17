# -*- coding: utf-8 -*-
from serial_generic import serial_generic

class gascard(serial_generic):
  def process(self, msg):
    try:
      raw_value = int(msg.strip().split(' ')[7], 16)
      self.data['co2_ppm'] = (raw_value/10000.0)*3000
      
    except ValueError:
      self.data['errors'] = 1
