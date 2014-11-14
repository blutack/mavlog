# -*- coding: utf-8 -*-
from serial_generic import serial_generic

class aeroprobe_adc(serial_generic):
        
  def process(self, msg):
    try:
      chunks = [chunk.strip() for chunk in msg.split(",")]
      
      if len(chunks) != 7:
        raise ValueError
      
      checksum = int(chunks[7], 16)
      
      check = 0
      for char in msg[0:-2]:
        check ^= ord(char)
      
      if check != checksum:
        raise ValueError
        
      self.data['seq'] = int(chunks[0])
      self.data['tas'] = float(chunks[1])
      self.data['aoa'] = float(chunks[2])
      self.data['aos'] = float(chunks[3])
      self.data['palt'] = float(chunks[4])
      self.data['pstatic'] = float(chunks[5])
      self.data['ptotal'] = float(chunks[6])
      
    except ValueError:
      self.data['errors'] = 1