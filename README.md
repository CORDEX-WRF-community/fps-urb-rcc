### Manual for the WRF-FPS-URBAN test simulations ###

The first control (CTRL) run is set to be performed for 7 days, 01-08.04.2020, in order to check if the simulations can run successfully by all the WRF groups and how fast. All groups should perform the run with the same setting. For that reason all the necessary files are provided below.

The zipped files necessary to perform test runs can be downloaded from here. The files included:
1. Geo_em files created with the new Copernicus LU data and added LCZ info with w2w tool, HWSD+BUK100 soil texture data, and SPOT LAI:
	geo_em.d01.nc
	geo_em.d02.nc
2. Files containing aerosol climatology for all domain:
	AOD202004_d01
	AOD202004_d02
3. File that deletes unnecessary variables and adds some that are not indicated in the Registry to be written out:
	varlist.txt
4. Input and boundary file to run the experiment
	wrfbdy_d01
	wrfinput_d01
	wrfinput_d02
	wrflowinp_d01
	wrflowinp_d02
    
5. namelist.input and namelist.wps, the 2 namelists necessary to run wrf and wps. The files are also available directly in the repository as well.

namelist.wps is set to run with the newest LU Copernicus dataset (with w2w tool applied), LAI map based on SPOT satellite data, and HWSD+BUK1000 soil texture data. The outer d01 domain is defined to fit the EUR-11 CODEX domain in Lambert Conformal projection named EUR-12 (i.e. at 12 km). The inner d02 domain is PAR-3 domain centered around Paris (check the plotted domains) and which includes corners as defined in the CORDEX FPS URB-RCC simulation protocol (link).

namelist.input is set to run with BouLac PBL scheme (option 8) and BEM urban scheme (option 3), with hybrid vertical levels and first level set to 35m (following the WRF setting for EURO-CORDEX simulations).

To run the simulations, place the files from (2), (3), (4) and namelist.input to the WRF/run directory and than run WRF:

	cp AOD202004_d01 AOD202004_d02 varlist.txt wrfbdy_d01 wrfinput_d01 wrfinput_d02 wrflowinp_d01 wrflowinp_d02 namelist.input WRF/run
	cd WRF/run
	ln -sf CAMtr_volume_mixing_ratio.SSP370 CAMtr_volume_mixing_ratio
	srun -n ${SLURM_NTASKS} ./wrf.exe   	  # should be adjusted to your system
