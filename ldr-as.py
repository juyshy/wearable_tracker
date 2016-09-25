"""
ldr.py
https://gist.githubusercontent.com/electronut/7d7d8ad371e71cad6b82/raw/d0c7c6b638d3a0256af193f04349380ac840ed6d/ldr-as.py
Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in

modification: Jukka Y
website: juy.fi

Display accelometer values from
Adafruit 10-DOF IMU Breakout


"""

import sys, serial, argparse, os
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort = "COM3", maxLen =100, baudRate =  115200):
      # open serial port
      self.ser = serial.Serial(strPort, baudRate)

      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.maxLen = maxLen
      self.ofile = open('test.txt','w')

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      assert(len(data) == 2)
      self.addToBuf(self.ax, data[0])
      self.addToBuf(self.ay, data[1])

  # update plot
  def update(self, frameNum, a0, a1):
      try:
          line = self.ser.readline()
          if "Adafruit" in line:
              line = line.replace("Adafruit 10DOF Tester", "")
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 2):
              self.add(data)
              #print line
              self.ofile.write(line)
              a0.set_data(range(self.maxLen), self.ax)
              a1.set_data(range(self.maxLen), self.ay)
      except KeyboardInterrupt:
          print('exiting')

      return a0,

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()
      self.ofile.close()

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)
  parser.add_argument('--baud', dest='baud', required=True)

  # parse args
  args = parser.parse_args()

  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort =  args.port # "COM3"
  baudRate =  int(args.baud)
  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, 100, baudRate )

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(-1100, 1100))
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update,
                                 fargs=(a0, a1),
                                 interval=30)

  # show plot
  plt.show()

  # clean up
  analogPlot.close()

  print('exiting.')


# call main
if __name__ == '__main__':
  main()
#  print os.getcwd()