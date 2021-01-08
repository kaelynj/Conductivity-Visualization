

########################################################
#VPython Code to Visualize Conductivity in a Cubic Unit Cell
#Kaelyn Ferris
########################################################

'''Currently working on:
        -Get bonds drawn
        -Figuring out why bonds are VERY wrong
'''

from visual import *
import os
import sys
import time
import numpy
from numpy import *


############ Function Definitions ############

def GetLattConst(infile):
        iFile = open(idat, 'r')
        iFile.readline()
        data = float(iFile.readline())
        if (data == 1):
                data = map(float, iFile.readline().split())
                iFile.close()
                return data[0]  
        else:
                iFile.close()
                return data             

#Function to get atom positions
def GetAtoms(infile):
        lineskip = 5
        #Open the file to be read by Python
        iFile = open(infile, 'r')
        
        for i in xrange(lineskip):     #Skip the lines before atom types are defined
                iFile.readline()
        
        atomtypes = iFile.readline().split()            #Store atom types in string list
        numatoms = map(int, iFile.readline().split())   #Store number of each atom type in int list
        pos = []
        iFile.readline()       #Skip line specifying 'Direct'
        
        for i in xrange(0, len(atomtypes)):       #Loop over the number of atom types
                pos.append([])                    #Add a new list of atom positions for each atom type
                for j in xrange(numatoms[i]):     
                        data = map(float, iFile.readline().split())
                        pos[i].append(data)
        iFile.close()   
        return pos


#Function to return scaled conductivity array
def GetSigma(infile, scaling):
        lineskip = 5
        #Open the file to be read by Python
        iFile = open(infile, 'r')
        
        for i in xrange(lineskip):     #Skip the lines before atom types are defined
                iFile.readline()
        atomtypes = iFile.readline().split()            #Store atom types in string list
        numatoms = map(int, iFile.readline().split())   #Store number of each atom type in int list
        print atomtypes, numatoms
        iFile.readline()       #Skip line specifying 'Direct'
        
        #Skip over atom positions
        #  (eventually one should save this info)
        for i in xrange(sum(numatoms)+1):        #The +1 here is to skip over the blank line after atom positions,
                iFile.readline()                 #     this ensures the next readline obtains the number of grid points
        
        #Store number of grid points in int list as well as the total number of grid points
        gridpoints = map(int, iFile.readline().split())
        numpoints = sum(gridpoints)
        print "Number of grid points"
        print gridpoints[0], gridpoints[1], gridpoints[2]               #Assume ordering of npoints is z y x
        sigma = numpy.zeros((gridpoints[0],gridpoints[1],gridpoints[2])) #Assign sigma indices as z y x
        #Iterate over the rest of the file contents
        x = 0
        y = 0
        z = 0
        
        #Populate conductivity array
        for line in iFile:    
                datastr = line.split()
                for i in range(len(datastr)):
                        data = float(datastr[i])
                        #Iterate over x, y, z grid points and append conductivity array
                        if (x == gridpoints[0]-1):         #If x is at the numx grid point
                                if (y == gridpoints[0]-1): #If y is at the numy grid point
                                        #Append sigma, increment z, reset y and x
                                        sigma[z][y][x] = data
                                        z+=1
                                        y=0
                                        x=0
                                else:
                                        #Append sigma, increment y, reset x
                                        sigma[z][y][x] = data
                                        y+=1
                                        x=0
                        else:
                                #Append sigma, increment x
                                sigma[z][y][x] = data
                                x+=1
                        #print x, y, z 
        if (scaling=='max'):
        #Scale conductivity array by max
                sigmax = numpy.amax(sigma)
                sigma = numpy.divide(sigma, sigmax)

        elif (scaling=='mean'):
        #Scale conductivity array by mean
                sigmax = numpy.amax(sigma)
                sigmin = numpy.amin(sigma)
                sigmean = numpy.mean(sigma)
                sigma = numpy.divide(sigma, sigmax)
                sigma = numpy.multiply(sigma, sigmean)
        else:
                print 'You dunce, breaking program...'
                return 0
        iFile.close()
        return sigma

def getGridPoints(infile):
        lineskip = 5
        #Open the file to be read by Python
        iFile = open(infile, 'r')
        
        for i in xrange(lineskip):     #Skip the lines before atom types are defined
                iFile.readline()
        atomtypes = iFile.readline().split()            #Store atom types in string list
        numatoms = map(int, iFile.readline().split())   #Store number of each atom type in int list
        iFile.readline()       #Skip line specifying 'Direct'
        
        for i in xrange(sum(numatoms)+1):        #The +1 here is to skip over the blank line after atom positions,
                iFile.readline()                 #     this ensures the next readline obtains the number of grid points
        
        #Store number of grid points in int list as well as the total number of grid points
        gridpoints = map(int, iFile.readline().split())
        iFile.close()
        return gridpoints[0]

def CheckBonds(bonds, atom, atomcomp):
        check1 = [atom, atomcomp]
        check2 = [atomcomp, atom]
        true = 1
        if (bonds!=[0]):
                for i in xrange(len(bonds)):
                        if (bonds[i]==check1) or (bonds[i]==check2):
                                true = 0
        return true
 
#Function to return list of pairs of atoms 
def DrawBonds(atompos, atom, a0):
        rcut = 3.5/a0
        ratom = sqrt(atom[0]**2 + atom[1]**2 + atom[2]**2)
        bonds = []
        for i in xrange(len(atompos)):
                for j in xrange(len(atompos[i])):
                        rcomp = sqrt(atompos[i][j][0]**2 + atompos[i][j][1]**2 + atompos[i][j][2]**2)
                        if (abs(rcomp - ratom) < rcut) and (ratom != rcomp):
                                if (CheckBonds(bonds, atom, atompos[i][j]) > 0):
                                        bonds.append([atom, atompos[i][j]])

        return bonds

def FindBonds(atompos, a0):
        bondlist = []
        for i in xrange(len(atompos)):
                for j in xrange(len(atompos[i])):
                        if (DrawBonds(atompos,atompos[i][j],a0)!=[]):
                                bondlist.append(DrawBonds(atompos,atompos[i][j],a0))
        return bondlist


################### Initialize Drawing Scene ###################

scene1 = display(title='Conductivity visualization in Real Space', background=color.white)
scene1.fullscreen = True
scene1.range = 2.8
forward = scene1.forward
print 'X forward:',forward[0]
rcut=0.001 #Radius of 0.01 is about as small as can be while still being visible

###Note: most of these values should eventually be pulled from the conductivity file being used
colorlist = [color.red, color.blue, color.green, color.cyan, color.magenta,color.orange, color.yellow]
op=0.3 #Opacity of 0.3 is enough that we can still see what's inside easily: might not even be needed with this technique
axesorig = 1

idat = raw_input("Enter the name of the conductivity file: ")
scaling = raw_input("How would you like to scale? (mean/max)")
a0 = GetLattConst(idat)
L = 2.   #Length of unit cell (in Python units)
N = getGridPoints(idat)  #Number of grid points in each direction
l = L/N  #Length per grid point
rmax = 0.25*l
offsetx = -L/2   #Offset to put origin in corner of cube
offsety = -L/2
offsetz = -L/2


################### Start Drawing Scene ###################

#Create axes
zarrow = arrow(pos=(offsetx, offsety, offsetz), axis=(0,0,0.5), color=color.green)
yarrow = arrow(pos=(offsetx, offsety, offsetz), axis=(0,0.5,0), color=color.blue)
xarrow = arrow(pos=(offsetx, offsety, offsetz), axis=(0.5,0,0), color=color.red)

#testsphere = sphere(pos=(0,0, 0), radius=1, color=color.white, opacity=0.4)
#smallbox = box(length=L, height=L, width=L, color=color.red)
#testsphere = sphere(pos=(0, 0, 0), radius=rmax, color=color.red)

#Draw unit cell
facez1 = curve(pos=[(-1,-1, 1),(-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)], color=color.black)
facez2 = curve(pos=[(-1, -1, -1),(-1,1,-1),(1,1, -1),(1,-1,-1),(-1,-1,-1)], color=color.black)

facey1 = curve(pos=[(-1, -1, 1),(-1,-1,-1),(-1,1,-1),(-1,1,1),(-1,-1,1)], color=color.black)
facey2 = curve(pos=[(1, -1, 1),(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)], color=color.black)

#facex1   Can put these in for completeness if you like, but uncessary to visualize stuff
#facex2
#Get atom positions
atompos = GetAtoms(idat)
if (len(atompos) < len(colorlist)):
        #Loop runs over atomtypes
        for i in xrange(len(atompos)):
                #Loop runs over atoms of type i
            for j in xrange(len(atompos[i])):
                posx = atompos[i][j][0]*L + offsetx
                posy = atompos[i][j][1]*L + offsety
                posz = atompos[i][j][2]*L + offsetz
                sphere(pos=(posx, posy, posz), radius=3*rmax, color=colorlist[i])
else:
        print 'Too many atom types, ignoring colors...'
        for i in xrange(len(atompos)):
            for j in xrange(len(atompos[i])):
                posx = atompos[i][j][0]*L + offsetx
                posy = atompos[i][j][1]*L + offsety
                posz = atompos[i][j][2]*L + offsetz
                sphere(pos=(posx, posy, posz), radius=3*rmax, color=color.blue)
        
bonds = FindBonds(atompos, a0)
#Loop runs over atoms
##for i in xrange(len(bonds)):
##        #Loop runs over bonds of atom i
##        for j in xrange(len(bonds[i])):
##                pos1 = vector(bonds[i][j][0][0]*L+offsetx, bonds[i][j][0][1]*L+offsety, bonds[i][j][0][2]*L+offsetz)
##                pos2 = vector(bonds[i][j][1][0]*L+offsetx, bonds[i][j][1][1]*L+offsety, bonds[i][j][1][2]*L+offsetz)
##                curve(pos=[pos1, pos2], color=color.blue)
#Create conductivity array
conduct = GetSigma(idat, scaling)

#####Loop to run over each grid point
for z in range(1, N):
    for y in range(1, N):
        for x in range(1, N):
            posx = x*l + offsetx
            posy = y*l + offsety
            posz = z*l + offsetz
            rsphere = conduct[z][y][x]*rmax
            #if (rsphere > rcut):
            sphere(pos=(posx, posy, posz), radius=rmax*2, color=(1-conduct[z][y][x],1-conduct[z][y][x],1-conduct[z][y][x]),opacity=conduct[x][y][z])



print "done"

            
