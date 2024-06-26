# Work to develop a WRF module specific to compute urban diagnostics

Following Martilli et al 2002, the urban scheme computes vertical profiles at a 'urban' vertical grid for momentum, temperature and TKE. The new diagnostics will be obtained following this urban vertical profiles.

The vertical profile of temperatures is called 'pt_u' inside the BEP1D subroutine (from phys/module_sf_bep.F) which computes all the terms in the column. We are going to get the values of this subroutine, since the outcome of the urban scheme is only at the surfaces of the buildings/roads and an averaged T2 following Monin-Obukhov theory (althougth recognized for not being fully correct).

Reference 
Martilli, A., Clappier, A., and Rotach, M. W. (2002). [An urban surface exchange parameterisation for mesoscale models](https://link.springer.com/article/10.1023/A:1016099921195). Boundary-Layer Meteorology, 104(2):261–304.

## Expanding WORK 
In order to be able to test sensitivity to soil infiltration additional modifications are performed in order to be able to change the soil-water capacity and infiltration for each LCZ. Therfore we could test the sensitivity to infiltration in two different (or simultaneous ways):
1. Changing maximum water capacity of the first layer of the soil (SMCMAX)
1. Changing the fraction of frozen impermeability (FCR)

In WRF ther are hard coded morphological values for soil characteristics specific for urban grid points found in `phys/module_sf_noahmpdrv.F` and `phys/module_sf_noahlsm.F`. NOTE: there are some discrepancies regarding hard coded values for urban grid points found in `phys/module_sf_urban.F` module (see table 9) used only for the _’green roof’_. (See partial analysis ![urban_infiltSens.pdf](./urban_infiltSens.pdf))

| Acronym   | value  | description |
| ---       | ----   | ---- |
| SHDFAC    |  0.05  | Vegetated area fraction <SUP>*</SUP>
| RSMIN     |  400   | Minimum stomatal resistance (VEGPARM.TBL) <SUP>*</SUP>
| SMCMAX    |  0.45  | Saturated soil moisture (seems to be MAXSMC from SOILPARM.TBL)
| SMCREF    |  0.42  | Reference soil moisture (seems to be REFSMC from SOILPARM.TBL)
| SMCWLT    |  0.40  | Wilting point (seems to be WLTSMC from SOILPARM.TBL)
| SMCDRY    |  0.40  | Residual soil moisture (seems to be DRYSMC from SOILPARM.TBL)
| DF1       |  3.24  | thermal diffusivity <SUP>*</SUP>
| CSOIL<SUP>a</SUP> |  3.0E6 | soil heat capacity (from GENPARM.TBL)
| FCR       |  0.95  | Impermeable fraction due to frozen soil ([fraction]) <SUP>@</SUP>

<SUP>*</SUP> not for Noah-MP lsm
<SUP>@</SUP> not for Noah lsm
<SUP>a</SUP> in subroutine `HRT`, `NOPAC`

### Values with modified values for urban grid points in Noah-MP
The Noah-MP land surface model has the following specific hard coded additional values for urban grid points (found in `phys/module_sf_noahmplsm.F` after `parameters%urban_flag = .TRUE.`):
- FVEG = 0.: green vegetation fraction [0.0-1.0]
- QSFC = QFX/(RHOAIR*CH) + QAIR: mixing ratio at lowest model layer, CH: sensible heat exchange coefficient, RHOAIR: density air (kg/m3), QAIR: specific humidity (kg/kg) (q2/(1+q2)), QFX: moisture flux
- Q2B = QSFC: bare ground heat conductance
- LAI  = 0.0: leaf area index
- SAI  = 0.0: stem area index?
- Z0MG = parameters%Z0MVT: z0 momentum, ground (m), Z0MVT: momentum roughness length (m)
- ZPDG  = 0.65 * parameters%HVT: zero plane displacement (m), HVT: top of canopy (m)
- Z0M  = Z0MG: z0 momentum (m)
- ZPD  = ZPDG: zero plane displacement (m)
- for SNOWH == 0.0; RSURF = 1.E6: ground surface resistance (s/m)
- DF(1:NSOIL) = 3.24: thermal conductivity [w/m/k]
- FCR = 0.95: Impermeable fraction due to frozen soil ([fraction])
- (carbon cycle related) XLAI = 0.0, XSAI = 0.0, GPP = 0.0, NPP = 0.0, NEE = 0.0, AUTORS = 0.0, HETERS = 0.0, TOTSC = 0.0, TOTLB = 0.0, LFMASS = 0.0, RTMASS = 0.0, STMASS = 0.0, WOOD = 0.0, STBLCP = 0.0,FASTCP = 0.0, GRAIN = 0.0

In order to achieve that:
1. New line will be introduced into `URBPARM_LCZ.TBL` with values of `SMCMAX` and `FCR` for each LCZ
1. Insert the reading of these values and pass them to the noah-MP lsm
