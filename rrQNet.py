#!/usr/bin/python

#  rrQNet: Residue-residue quality estimation net
#
#  Copyright (C) Bhattacharya Laboratory 2021
#
#  rrQNet is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  rrQNet is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with DConStruct.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

import os,sys
import tensorflow as tf
from numpy import loadtxt
from tensorflow.keras.layers import *
from tensorflow.keras.models import load_model
import optparse
import numpy as np
import os
from tensorflow.keras.models import model_from_json
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

#header

print("\n*****************************************************************")
print("*                          rrQNet                               *")
print("*         Residue-residue quality estimation net                *")
print("*  For comments, please email to bhattacharyad@auburn.edu       *")
print("*****************************************************************\n")

parser=optparse.OptionParser()
parser.add_option('-p', dest='pre',
        default= '',    #default empty!'
        help= 'precision matrix (npy format)')
parser.add_option('-r', dest='rr',
        default= '',    #default empty!'
        help= 'residue-residue contact map (rr format)')
parser.add_option('-m', dest='model',
        default= '',    #default empty!'
        help= 'path to the model')
parser.add_option('-L', dest='xL',
        default= '1',    #default L'
        help= 'top xL contacts in the contact matrix (default = 1)')

parser.add_option('-t', dest='tgt',
        default= 'target',    #default target
        help= 'name of target')


(options,args) = parser.parse_args()

tgt = options.tgt
xL = options.xL
pre = options.pre
lmodel = options.model
rr = options.rr

def print_usage():
    print("\nUsage: rrQNet.py [options]\n")

    print("Options:")
    print("  -h, --help  show this help message and exit")
    print("  -p PRE      precision matrix (npy format)")
    print("  -r RR       residue-residue contact map (rr format)")
    print("  -m MODEL    path to the model")
    print("  -L XL       top xL contacts in the contact matrix (default = 1)")
    print("  -t TGT      name of target")
    
#basic input check
if (pre == ''):
    print ('Error! precision matrix file must be provided. Exiting ...')
    print_usage()
    sys.exit()
if (rr == ''):
    print ('Error! contact map must be provided. Exiting ...')
    print_usage()
    sys.exit()
if (lmodel == ''):
    print ('Error! contact path to the trained model must be provided. Exiting ...')
    print_usage()
    sys.exit()


#existence check
if not os.path.exists(pre):
    print ('Error! No such precision matrix file found. Exiting ...')
    print_usage()
    sys.exit()
if not os.path.exists(rr):
    print ('Error! No such contact map file found. Exiting ...')
    print_usage()
    sys.exit()
if not os.path.exists(lmodel):
    print ('Error! No such trained model file found. Exiting ...')
    print_usage()
    sys.exit()


# load top L contacts in contact matrix
f = open(rr, 'r')
lines = f.readlines()
N = len(lines[0].strip())
arr = [[0 for x in range(N)] for y in range(N)]
for line in lines[1:]:
    res1 = int(line.strip().split()[0]) - 1
    res2 = int(line.strip().split()[1]) - 1
    arr[res1][res2] = 1
    arr[res2][res1] = 1
x2 = np.array(arr)
f.close()

#load precision matrix
x1 = np.load(pre)
l_s = x1.shape[1]
L = float(xL) * l_s
xx = np.zeros((l_s, l_s, 441))

# reshaping
for ii in range(l_s):
    for jj in range(l_s):
        xx[ii,jj,:] = x1[:,ii,jj]
    
X_test = xx
X_test = X_test.reshape(1, l_s, l_s, 441)
X2_test = x2.reshape(1, l_s, l_s, 1)

# loading model
json_file = open(lmodel + '/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(lmodel + '/modelw.h5') 
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])

# prediction
yhat = loaded_model.predict([X_test,X2_test])  
cmo = 0.0    
Y1 = yhat[0, 0:l_s, 0:l_s]

rr_map = []
for i in range(l_s):
    for j in range(i+1,l_s):
        ij = (Y1[i,j] + Y1[j,i])/2
        if(ij > 0.5):
            cmo += 1
            rr_map.append([i, j, ij[0]])

print(tgt + '-score: ' + str(float(cmo)/L))
print('The score is based on the following contacts: \n')
for r in range(len(rr_map)):
    i,j,p = rr_map[r]
    print(str(i) + ' ' + str(j) + ' ' + '0 ' + '8 ' + str(p))
