# Work to develop a WRF module specific to compute urban diagnostics

Following Martilli et al 2002, the urban scheme computes vertical profiles at a 'urban' vertical grid for momentum, temperature and TKE. The new diagnostics will be obtained following this urban vertical profiles.

The vertical profile of temperatures is called 'pt_u' inside the BEP1D subroutine (from phys/module_sf_bep.F) which computes all the terms in the column. We are going to get the values of this subroutine, since the outcome of the urban scheme is only at the surfaces of the buildings/roads and an averaged T2 following Monin-Obukhov theory (althougth recognized for not being fully correct).

Reference 
Martilli, A., Clappier, A., and Rotach, M. W. (2002). An urban surface exchange parameterisation for mesoscale models. Boundary-Layer Meteorology, 104(2):261–304.

## Expanding WORK 
In order to be able to test sensitivity to soil infiltration additional modifications are performed in order to be able to change the soil-water capacity for each LCZ

In WRF ther are hard coded morphological values for soil moisture, specific for urban grid points found in `phys/module_sf_noahlsm.F`. NOTE: there are some discrepancies regarding hard coded values for urban grid points found in `phys/module_sf_urban.F` module (see table 9) used only for the _’green roof’_
| Acronym   | value  | description |
| ---       | ----   | ---- |
| SHDFAC    |  0.05  | Vegetated area fraction
| RSMIN     |  400   | Minimum stomatal resistance (VEGPARM.TBL)
| SMCMAX    |  0.45  | Saturated soil moisture (seems to be MAXSMC from SOILPARM.TBL)
| SMCREF    |  0.42  | Reference soil moisture (seems to be REFSMC from SOILPARM.TBL)
| SMCWLT    |  0.40  | Wilting point (seems to be WLTSMC from SOILPARM.TBL)
| SMCDRY    |  0.40  | Residual soil moisture (seems to be DRYSMC from SOILPARM.TBL)
| DF1       |  3.24  | thermal diffusivity
| CSOIL<SUP>a</SUP>    |  3.0E6 | soil heat capacity (from GENPARM.TBL)

<SUP>a</SUP> in subroutine `HRT`, `NOPAC`

In order to achieve that:
1. New line will be introduced into `URBPARM_LCZ.TBL` with values of `SMCMAX` for each LCZ
1. Insert the reading of these values and pass them to `phys/module_sf_noahlsm.F`
