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

![the plotted domains](https://github.com/FPS-URB-RCC/WRFcoordination/blob/main/domains_EP.png)

**namelist.input** is set to run with BouLac PBL scheme (option 8) and BEM urban scheme (option 3), with hybrid vertical levels and first level set to 35m (following the WRF setting for EURO-CORDEX simulations).

To run the simulations, place the files from (2), (3), (4) and namelist.input to the WRF/run directory and than run WRF:

	cp AOD202004_d01 AOD202004_d02 varlist.txt \
		wrfbdy_d01 wrfinput_d01 wrfinput_d02 wrflowinp_d01 wrflowinp_d02 \
		namelist.input WRF/run
	cd WRF/run
	ln -sf CAMtr_volume_mixing_ratio.SSP370 CAMtr_volume_mixing_ratio
	srun -n ${SLURM_NTASKS} ./wrf.exe   	  # Note that this should be adjusted to your system

 ## WRF-FPS-URBAN stage-0 simulations
For the stage-0 simulations it is suggested to have the lowest vertical model level within the urban canopy (dzbot=10). The default [namelist.input](https://github.com/FPS-URB-RCC/WRFcoordination/blob/main/namelist.input) differs from the CTRL [namelist.input_test](https://github.com/FPS-URB-RCC/WRFcoordination/blob/main/namelist.input_test) by the lowest model level (dzbot=10 instead 35), and the number of vertical levels for that reason needs to be increased (e_vert=60). Each group can make changes in the namelist.input for a specific sensitivty study they want to perform (e.g. sensitivity to land use data, sensitivity do the PBL scheme, to the number of vertical levels, to urban parameters etc.). 

A common tar file that includes geo_em files (without urban category, urban LU with LCZ, extended LU urban category over LCZ, and urban from LU map) and aerosol files for the stage-0 simuations is available for all the groups to be downloaded rom this [link](https://meteo.unican.es/work/josipa/WRF-FPS-URB-RCC/WRF-FPS-URB-RCC_stage0_v0.tar). 

The downloaded **WRF-FPS-URB-RCC_stage0_v0.tar** file contains:
1. geo_em files: The files are created for our EUR-12 and PAR-3 domains. During our meetings it has been agreed to use land cover map based on LANDMATE PFT data in order to be consistend with the EUR-11 CMIP6 CORDEX runs. More datails on the LU dataset can be found in [Reinhart et al.(2022)](https://doi.org/10.5194/essd-14-1735-2022). 
The raw LANDMATE PFT [data](https://www.wdc-climate.de/ui/entry?acronym=LM_PFT_LandCov_EUR2015_v1.0). Three variables have been updated in the geo_em files: LU_INDEX, LANDUSEF, and LANDMASK. 
LAI map is based on [SPOTv1](https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-lai-fapar?tab=form) satellite data, and [HWSD](https://www.wdc-climate.de/ui/entry?acronym=WRF_NOAH_HWSD_world_TOP_ST_v121)+[BUK1000](https://www.wdc-climate.de/ui/entry?acronym=WRF_NOAH_BUK_Ger_top_SOILTYP) data are used for the soil texture data. The outer d01 domain is defined to fit the EUR-11 CODEX domain in Lambert Conformal projection named EUR-12 (i.e. at 12 km). 
The list of the geo_em files:
	<br /> geo_em.d01_NoUrban.nc
	<br /> geo_em.d01_UrbanWithLCZ.nc
	<br /> geo_em.d01_UrbanExtended2LCZ.nc
	<br /> geo_em.d01_UrbanFromLU.nc
	<br /> geo_em.d02_NoUrban.nc
	<br /> geo_em.d02_UrbanWithLCZ.nc
	<br /> geo_em.d02_UrbanExtended2LCZ.nc
	<br /> geo_em.d02_UrbanFromLU.nc


	<br /> **NOTE:** Default geo_em files for the stage-0 simualtions are **geo_em.d01_UrbanWithLCZ.nc** and **geo_em.d02_UrbanWithLCZ.nc**.

2. Aerosol climatology data (variable AOD550) are extracted from the MERRA2 reanalysis raw data files downloaded from this [link](https://b2share.fz-juelich.de/records/?community=a140d3f3-0117-4665-9945-4c7fcb9afb51&sort=mostrecent&page=1&size=10). It is consistent with the EUR-11 CORDEX CMIP6 protocol, where it is agreed to use these data for the evaluation run.
The list of the AOD files:
	<br /> AOD_20200301_20200901_d01
	<br /> AOD_20200301_20200901_d02


	<br /> **NOTE:** Make sure that this files are taken into account as *auxinput15* by indicating it in the namelist.input, for example:
	<br /> `auxinput15_inname = "AOD_20200301_20200901_d<domain>"`
	<br /> In case you cannot run the complete period without performing the restart of the simuation, you need to adjust AOD file, so that the initial day in the AOD files corresponds to the restart day. This can be 	done using e.g. the [nco](http://research.jisao.washington.edu/data_sets/nco/) tool and the command:
	<br /> `ncks -h -d Times,restart_day,ndays_in_AOD_infile AOD_infile AOD_outfile`
