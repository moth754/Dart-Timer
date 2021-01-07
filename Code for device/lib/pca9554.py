################################################################################
# Author			: akael "ported" by theshade
# Creation date 		: 02.02.2019
# Langage			: microPython
# Filename			: pca9554.py
# Target		 		: Pycom pyscan
# Description		: PCA9554A GPIO Expander
################################################################################

import time
from machine import I2C


IN = const(1)
OUT = const(0)
#"""
#Pca9554 (8 bit I2C expander)
#"""
class PCA9554():
    #Define register
    Pca9554_IN_REG = const(0x00) #Input register
    Pca9554_OUT_REG = const(0x01) #Output register
    Pca9554_POL_REG = const(0x02) #Polarity inversion register (1=data inverted)
    Pca9554_DIR_REG = const(0x03) #Config register (0=output, 1=input)
    Pca9554_I2CADDR = const(0x20)
    i2c_bus=-1
    i2c_address=-1
    line=0xFF
	#def __init__(self, bus_id=0,address=0x39,line=0, direction="Null"):
    def __init__(self, line=0x00, direction=1, sda = 'P22', scl = 'P21'):
        #if pysense is not None:
        #   self.i2c = pyscan.i2c
        #else:
        self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl))
        #self.i2c_bus = smbus.SMBus(bus_id)
		#Pca9554_I2CADDR=address
        print(line)
        self.line=line
        print(self.line)
        print('setting direction')
        if direction == 1:
            self.setinput()
        if direction == 0:
            self.setoutput()

        time.sleep(0.01)

	def set_dir_reg(self, value):
		#"""set direction register : 0=output, 1=input"""
		self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_DIR_REG, value)

        #"""set bit as output"""
    def setoutput(self):
        print('setting output to')
        currentvalue = self.i2c.readfrom_mem(Pca9554_I2CADDR , Pca9554_DIR_REG, 1)
        print(currentvalue[0] | (0x01<<self.line))
        self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_DIR_REG , currentvalue[0] & 255-(1<<self.line))

        #"""set bit as input"""
    def setinput(self):
        print('setting input to')
        currentvalue = self.i2c.readfrom_mem(Pca9554_I2CADDR , Pca9554_DIR_REG, 1)
        print(currentvalue[0] | (0x01<<self.line))
        self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_DIR_REG ,currentvalue[0] | (0x01<<self.line))
        #self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_DIR_REG , self.line)

    def writebyte(self,value):
		#"""write output byte value"""
		self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_OUT_REG, value)
		return
    def readbyte(self):
		#"""read input byte value"""
        return self.i2c.readfrom_mem(Pca9554_I2CADDR, Pca9554_IN_REG,1)

    def set(self):
        #"""set output bit at 1"""
        currentvalue = self.i2c.readfrom_mem(Pca9554_I2CADDR, Pca9554_OUT_REG,1)
        #self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_OUT_REG, 1<<2)
        self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_OUT_REG, currentvalue[0] | 1<<self.line)

    def reset(self):
		#"""reset output bit at 0"""
		currentvalue = self.i2c.readfrom_mem(Pca9554_I2CADDR, Pca9554_OUT_REG,1)
		self.i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_OUT_REG, currentvalue[0] & (255-(1<<self.line)))
		return
    def get(self):
		#"""read input bit value"""
		linevalue = self.i2c.readfrom_mem(Pca9554_I2CADDR, Pca9554_IN_REG,1)
		ret = ((linevalue >> self.line) & 1 )
		return ret