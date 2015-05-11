# -*- coding: utf-8 -*-
"""
Mount.py

This is a very limited controller module for the Celestron SE mount.

Author: Kevin R. Johnson
        kevin.r.johnson6@navy.mil
        Naval Air Warfare Center Weapons Division, China Lake, CA.
"""
import serial
import sys

class Mount(object):

    print "Starting Mount.py\n"
    def __init__(self, init=0):
        # Mount data
        print "Establishing serial link."
        #self.MountLink = serial.Serial(4-1, 9600, timeout=5) # The serial connection to the mount.
        self.MountLink = serial.Serial('com4', 9600, timeout=5) # The serial connection to the mount.
        print "Link established with mount.\n"
        self.MaxSlewingRate = 9 # 9 slew rates and zero for stop.
        self.TermChar = '#' # Terminating character for mount reply.

    def GetAzmAlt(self):
        self.MountLink.write('Z')
        Azm = self.MountLink.read(4)
        junk = self.MountLink.read()
        Alt = self.MountLink.read(4)
        EOL = self.MountLink.read()
        Azm = 360.0 * int(Azm, 16) / 65536
        Alt = 360.0 * int(Alt, 16) / 65536
        #print "Relative to startup orientation:\nAlt: " + str(Alt) + " Azm: " + str(Azm)
        return([Azm,Alt])

    def SlewAzm(self, rate):
        if rate >= 0 and rate <= self.MaxSlewingRate:
            self.MountLink.write( 'P' + chr(2) + chr(16) + chr(36) + chr(int(rate)) + chr(0) + chr(0) + chr(0) )
            EOL = self.MountLink.read()
        elif rate < 0 and -rate <= self.MaxSlewingRate:
            self.MountLink.write( 'P' + chr(2) + chr(16) + chr(37) + chr(abs(int(rate))) + chr(0) + chr(0) + chr(0) )
            EOL = self.MountLink.read()
        else:
            sys.stderr.write("\nERROR SlewAzm(): Invalid rate.\n")
            sys.stderr.write("Acceptible rates: " + str(range(-self.MaxSlewingRate,self.MaxSlewingRate+1)))
            sys.stderr.write("\nRate commanded: " + str(int(rate)) + "\n")
    
    def SlewAlt(self, rate):
        if rate >= 0 and rate <= self.MaxSlewingRate:
            self.MountLink.write( 'P' + chr(2) + chr(17) + chr(36) + chr(int(rate)) + chr(0) + chr(0) + chr(0) )
            EOL = self.MountLink.read()
        elif rate < 0 and -rate <= self.MaxSlewingRate:
            self.MountLink.write( 'P' + chr(2) + chr(17) + chr(37) + chr(abs(int(rate))) + chr(0) + chr(0) + chr(0) )
            EOL = self.MountLink.read()
        else:
            sys.stderr.write("\nERROR SlewAlt(): Invalid rate.\n")
            sys.stderr.write("Acceptible rates: " + str(range(-self.MaxSlewingRate,self.MaxSlewingRate+1)))
            sys.stderr.write("\nRate commanded: " + str(int(rate)) + "\n")


        
        
        
        