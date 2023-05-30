# WRFcoordination

This repository is created for the coordination of the WRF simulations within the CORDEX FPS URB-RCC framework following [the simualtions protocol](https://docs.google.com/document/d/1R4O1x67Tpr-qcEPlkzKDvJP1itoxKPbaBZO9gpIfamc/edit).

At **STAGE 0** the test simulations will be performed in order to test RCMs and urban schemes, as well as model and domain set-up. For that, short-term simulations over the Paris region will be performed. Furthermore, the test simulations will cover two extreme events in 2020 (heat and heavy precipitation), which will allow for a coordinated analysis of these extreme events. 
In addition, these test simulations will prepare the ground for the coordinated evaluation simulations (**STAGE 1**). 

## WRF-FPS-URBAN CTRL simulations

The first test **STAGE 0** control (CTRL) run is set to be performed for 7 days, 01-08.04.2020, in order to check if the simulations can run successfully by all the WRF groups and how fast. All groups should perform the run with the same setting. For that reason all the necessary files can be downloaded from this [link](https://meteo.unican.es/work/josipa/fps_urban_file_urb3.tar), are the description of the files are provided below.

The zipped files necessary to perform test runs can be downloaded from here. The files included:
1. Geo_em files created with the new Copernicus LU data and added LCZ info with w2w tool, HWSD+BUK100 soil texture data, and SPOT LAI:
	<br /> geo_em.d01.nc
	<br /> geo_em.d02.nc
2. Files containing aerosol climatology for all domain:
	<br /> AOD202004_d01
	<br /> AOD202004_d02
3. File that deletes unnecessary variables and adds some that are not indicated in the Registry to be written out:
	<br /> varlist.txt
4. Input and boundary file to run the experiment
	<br /> wrfbdy_d01
	<br /> wrfinput_d01
	<br /> wrfinput_d02
	<br /> wrflowinp_d01
	<br /> wrflowinp_d02
    
5. namelist.input and namelist.wps, the 2 namelists necessary to run wrf and wps. The files are also available directly in the repository as well.

**namelist.wps** is set to run with the newest LU Copernicus dataset (with w2w tool applied), LAI map based on SPOT satellite data, and HWSD+BUK1000 soil texture data. The outer d01 domain is defined to fit the EUR-11 CODEX domain in Lambert Conformal projection named EUR-12 (i.e. at 12 km). The inner d02 domain is PAR-3 domain centered around Paris (check [the plotted domains](https://github.com/FPS-URB-RCC/WRFcoordination/blob/CTRL/domains_EP.png)) and which includes corners as defined in the CORDEX FPS URB-RCC simulation protocol [link](https://docs.google.com/document/d/1R4O1x67Tpr-qcEPlkzKDvJP1itoxKPbaBZO9gpIfamc/edit).

![the plotted domains](https://github.com/FPS-URB-RCC/WRFcoordination/blob/CTRL/domains_EP.png)

**namelist.input** is set to run with BouLac PBL scheme (option 8) and BEM urban scheme (option 3), with hybrid vertical levels and first level set to 35m (following the WRF setting for EURO-CORDEX simulations).

To run the simulations, place the files from (2), (3), (4) and namelist.input to the WRF/run directory and than run WRF:

	cp AOD202004_d01 AOD202004_d02 varlist.txt \
		wrfbdy_d01 wrfinput_d01 wrfinput_d02 wrflowinp_d01 wrflowinp_d02 \
		namelist.input WRF/run
	cd WRF/run
	ln -sf CAMtr_volume_mixing_ratio.SSP370 CAMtr_volume_mixing_ratio
	srun -n ${SLURM_NTASKS} ./wrf.exe   	  # Note that this should be adjusted to your system
