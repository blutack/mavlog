# -*- coding: utf-8 -*-
from pymavlink import mavutil
import logging, threading

class mavlink_ap:
  
  def __init__(self, options):
    self.running = True
    self.conn = mavutil.mavlink_connection(options['port'], baud=options['baud'])
    
    self.messages = options['messages']
    self.data = {}
    
    logger = logging.getLogger(__name__)
    logger.info("Started on %s" % options['port'])
    
    self.thread = threading.Thread(target = self.process)
    self.thread.daemon = True
    self.thread.start()
    
  def get_data(self, blocking = False):
    # Not recommended for use outside testing
    if blocking:
      while self.data == {'errors': 0}:
        pass
        
    return self.data
    
  def stop(self):
    self.running = False
    
  def process(self):
    logger = logging.getLogger(__name__)
    
    while self.running:
      msg = self.conn.recv_msg()
      if msg:
        self.post_process(msg)
      
    logger.info(__name__ + " shutdown")
    
  def post_process(self, msg): 
    if msg.get_type() in self.messages.keys():
      for item in self.messages[msg.get_type()]:
	tag = self.messages[msg.get_type()][item]
	self.data[tag] = getattr(msg, item)
        #setattr(self, self.messages[item], getattr(msg, item))
