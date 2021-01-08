#==================================
#  Python file to extract xred data from output file
#   and append it to specified file
#==================================
import os
import sys
import time
from numpy import *

idat = raw_input("Enter the name of the output file: ")
odat = raw_input("Enter the name of the file to write E vs a2D data: ")
odat2 = raw_input("Enter the name of the file to write Z vs a2D data: ")
iFile = open(idat, 'r')
oFile = open(odat, 'a')
oFile2 = open(odat2, 'a')
Str = ''
acell = 0

#List variables
a2D = []
Etotal = []
ZoutOfPlane = []

#Boolean variables
START = False
write = False
END = False

##--> too much bureaucracy.  Doesn't compress anything.
#def AppendFloat(DatStr,myarray):
#	myarray.append(float(DatStr))
#        return myarray
#myarray = AppendFloat(DatStr,myarray)

def Append_Z(line1, line2):
	DatStr1 = line1.split()
	DatStr2 = line2.split()
	z1 = 0.0
	z2 = 0.0
	z = 0.0
	#EndofLine1 = len(DatStr1)
	#EndofLine2 = len(DatStr2)
	#z1 = float(DatStr1[EndofLine1 - 1])
	#z2 = float(DatStr2[EndofLine2 - 1])	
        ##--> Python is already on top of this, and cooler than you ;)  
	z1 = float(DatStr1[-1])
	z2 = float(DatStr2[-1])	
	#z = '4.0/sqrt(3) *' acell * abs(z2 - z1)
	z  = acell * abs(z2-z1)
	ZoutOfPlane.append(float(z))

def Append_a2D(line1, line2, acell):
	DatStr1 = line1.split()
	DatStr2 = line2.split()
	x1 = 0.0
	x2 = 0.0
	y1 = 0.0
	y2 = 0.0
	z1 = 0.0
	z2 = 0.0
	a = 0.0
	#x1 = float(DatStr1[1])
	#x2 = float(DatStr2[0])
	#y1 = float(DatStr1[2])
	#y2 = float(DatStr2[1])
        ##--> May be less error prone?  
	x1 = float(DatStr1[-3])
	x2 = float(DatStr2[-3])
	y1 = float(DatStr1[-2])
	y2 = float(DatStr2[-2])
	z1 = float(DatStr1[-1])
	z2 = float(DatStr2[-1])
        ##--> the GLOBAL value of acell is defined above, = 0.
        ##    Python doesn't know to update it because that occurs below this line.
	a = acell * math.sqrt((x1)**2 + (y1)**2 + (z1)**2)      ## a2D = sqrt( x1^2 + y1^2 + z1^2 )
	a2D.append(a)

def Write_Evsa2D():
        ## --> need carriage return
	oFile.write("#a2D   Etotal\n")
        ## --> you need the index here, not the item in Etotal.
        ##     Etotal[i], a2D[i].  And title is botched somehow.
        ## --> And reconvert E, a back to strings.
	for i in range(len(Etotal)):
		oFile.write(repr(a2D[i]) + '  ')
		oFile.write(repr(Etotal[i]) + '\n')

def Write_Zvsa2D():
	oFile2.write("#a2D     Z\n")
	for i in range(len(ZoutOfPlane)):
		oFile2.write(repr(a2D[i]) + '   ')
		oFile2.write(repr(ZoutOfPlane[i]) + '\n ')

while not END:
	line = iFile.readline()
	if "Calculation completed." in line:
		END = True
	if "END DATASET" in line:
		START = True
	if START:
		DatStr = line.split()
		if "acell" in line:
			acell = float(DatStr[1])
                        print line, acell

                ## --> forgot to "float" the data string.
		if "etotal" in line:
			Etotal.append(float(DatStr[1]))
                        print line, Etotal[-1]

		if "xred" in line:
			NextLine = iFile.readline()
			Append_Z(line, NextLine)
                        print line, NextLine, ZoutOfPlane[-1]
		if "rprim" in line:
			NextLine = iFile.readline()
			Append_a2D(line, NextLine, acell)
                        print line, NextLine, a2D[-1]

Write_Evsa2D()
Write_Zvsa2D()

'''
		for word in DatStr:
			#If current string in line doesn't contain "xred" cast it as a float
			if "xred" in word:
				oFile.write('\n \n' + word)
				write = True
			elif write:
				oFile.write('  ' + str(float(word)))
		if write:
			line = iFile.readline()
			DatStr = line.split()
		#	oFile.write('      \n')
			for word in DatStr:
				oFile.write('  ' + str(float(word)))
	write = False	

'''




print "Done.\n"
oFile.close()
iFile.close()

#try:
#Str = '  ' + str(float(DatStr[i]))	
#oFile.write(Str)
#except ValueError:
#continue 
		#	else:
		#		#oFile.write('\n')
		#		oFile.write(DatStr[i] + '?')
#		oFile.write('\n')



