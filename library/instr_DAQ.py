# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:25:15 2019

@author: IonTrap
"""

import ctypes

class DAQ():
    
    def __init__(self):
        
        '''load DAQ dll'''
        self.dll_DAQ = ctypes.windll.LoadLibrary('C:\\Users\\IonTrap\\code\\python\\dll\\PCI-Dask64.dll')

        '''register card'''
        self.dll_DAQ.Register_Card.restype = ctypes.c_int16

        cardType = ctypes.c_uint16(1)
        card_num = ctypes.c_uint16(0)
        self.cardNumber = self.dll_DAQ.Register_Card(cardType, card_num)


    def set_voltage(self, channel, param):

        self.dll_DAQ.AO_VWriteChannel.restype = ctypes.c_int16
        chan = ctypes.c_uint16(channel)
        voltage = ctypes.c_double(param)

        error = self.dll_DAQ.AO_VWriteChannel(self.cardNumber, chan, voltage)
