# SNIc_dependencies

## Table of contents
* [General info](#general-info)
* [Content](#content)

## General info

We extracted Type Ic Supernovae (SNe Ia) from the Open Supernova Catalog (OSC). Then, their light curves in V-band were fitted with the Bazin function ([Bazin G. et al., 2009](https://ui.adsabs.harvard.edu/abs/2009A%26A...499..653B/abstract)) to estimate the absolute magnitude at maximum light and the light curve shape parameters.


## Content

### Data

* `pre_max_photometry15_z0.03.csv` – file extacted from the Open Supernova Catalog with the following cuts: >15 photometrical points, pre-max photometry, z<=0.03 (V), "Ic" only.
* `sn_Ic_V.txt` – SN Ic list after the visual inspection.


### Code

* `SNIc_LC_dependences.ipynb` – approximation of SNe Ic extracted from the OSC with the Bazin function and the visialisation of M_V(delta_m15) dependency in comparison with luminosity-width relation for SNe Ia ([Phillips M., 1993](https://ui.adsabs.harvard.edu/abs/1993ApJ...413L.105P/abstract)).
* `snIc_list.py` – fast visial check of SN Ic light curves. 

### Plots
Output plots from Jupyter Notebooks with light curve fit.

`Mv_dm15.png` – M_V(delta_m15) dependency for SNe Ic.

