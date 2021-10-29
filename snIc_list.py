#!/usr/bin/env python3
# Criterias: >15(V)/10(R) photometrical points, pre-max photometry, z cut (V: z<=0.03; R: 0.15=<z<=0.25), "Ic" only
from __future__ import print_function
import numpy as np
import os
import matplotlib.pyplot as plt
import json
from snad.load.curves import OSCCurve
from astropy.io import ascii


data = ascii.read("pre_max_photometry15_z0.03.csv")

sn = []
fail = []

for i in data['Name']:
    try:
        passbands = OSCCurve.from_name(i).bands
        print(i)

        if 'V' in passbands:
            print('Yes')
            xdata = OSCCurve.from_name(i).odict['V'].x
            ydata = OSCCurve.from_name(i).odict['V'].y
            plt.plot(xdata, ydata, 'go')
            plt.show()
            if input("Do You Want To Keep This Supernova? [y/n] ") == "y":
                sn.append(i)
            else:
                continue
        else:
            continue
    except:
        fail.append(i)
        print('Error: fail for: ',i)

with open('sn_Ic_V.txt', 'w') as f:
    for line in sn:
        f.write(line)
        f.write('\n')
