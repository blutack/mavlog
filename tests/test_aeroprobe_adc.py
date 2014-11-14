#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_aeroprobe_adc
----------------------------------

Tests for `mavlog` module.
"""

import unittest
import serial
import time

from mavlog.devices.aeroprobe_adc import aeroprobe_adc
import aeroprobe_single_line
import aeroprobe_incorrect_line
import aeroprobe_incorrect_checksum

class TestAeroprobeADC(unittest.TestCase):

  def setUp(self):
    self.ap = aeroprobe_adc("loop://")
    self.test_port = self.ap.conn

  def test_single_line(self):
    self.test_port.write(aeroprobe_single_line.sample)
    data = self.ap.get_data(blocking=True)

    self.assertTrue(data['seq']     == 9385)
    self.assertTrue(data['tas']     == 3.92)
    self.assertTrue(data['aoa']     == -3.5)
    self.assertTrue(data['aos']     == 8.55)
    self.assertTrue(data['palt']    == 55)
    self.assertTrue(data['pstatic'] == 100655)
    self.assertTrue(data['ptotal']  == 100664)
    self.assertTrue(data['errors']  == 0)
    
  def test_incorrect_line(self):
    self.test_port.write(aeroprobe_incorrect_line.sample)
    data = self.ap.get_data(blocking=True)
    self.assertTrue(data['errors']  == 1)
    
  def test_incorrect_checksum(self):
    self.test_port.write(aeroprobe_incorrect_checksum.sample)
    data = self.ap.get_data(blocking=True)
    self.assertTrue(data['errors']  == 1)
    
  def tearDown(self):
    self.ap.stop()

if __name__ == '__main__':
  unittest.main()