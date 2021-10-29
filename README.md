# SNIc_dependencies

## Table of contents
* [General info](#general-info)
* [Content](#content)

## General info

Type Ia Supernovae are widely used to measure distances in the Universe. Despite the recent progress achieved in SN Ia standardization, the Hubble diagram still shows some remaining intrinsic dispersion. The remaining scatter in supernova luminosity could be due to the environmental effects.

In these Jupyter Notebooks we reproduce the Hubble diagram fit with Pantheon supernovae ([Scolnic et al., 2018](https://ui.adsabs.harvard.edu/abs/2018ApJ...859..101S/abstract)). We also study how the host morhology term and the galactocentric distance affect the supernova light-curve parameters and the Hubble diagram fit.


## Content

### Data

* `pre_max_photometry15_z0.03.csv` – file extacted from the Open Supernova Catalog with the following cuts: >15 photometrical points, pre-max photometry, z<=0.03 (V), "Ic" only.
* `sn_Ic_V.txt` – SN Ic list after the visual inspection.


### Code

* `SNIc_LC_dependences.ipynb` – approximation of SNe Ic extracted from the OSC with the Bazin function [Bazin G. et al., 2009](https://ui.adsabs.harvard.edu/abs/2009A%26A...499..653B/abstract) and the visialisation of M_V(delta_m15) dependency in comparison with luminosity-width relation for SNe Ia ([Phillips M., 1993](https://ui.adsabs.harvard.edu/abs/1993ApJ...413L.105P/abstract)).
* `snIc_list.py` – fast visial check of SN Ic light curves. 

### Plots
Output plots from Jupyter Notebooks with light curve fit.

`Mv_dm15.png` – M_V(delta_m15) dependency for SNe Ic.

