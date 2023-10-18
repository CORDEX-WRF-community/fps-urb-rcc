# FPS-URB-RCC Test-7d WRF simulation

The first test **Test-7d** run is set to be performed for 7 days (i.e. 01-08.04.2020) prior to the [STAGE-0](./STAGE-0) simulation in order to verify if the WRF model with an urban scheme turned on and an updated land cover map with LCZ categories can be run successfully by all the [WRF groups](https://docs.google.com/spreadsheets/d/1ZurcH982hepymMruHGPzQX-N55kWUXNc42RCE2pxgwg/edit#gid=0) involved in the FPS-URB-RCC activities, and how fast. Each of the group should use the same setting to perform the run. For that reason all the files necessary to complete the run are prepared and can be downloaded at this [link](https://meteo.unican.es/work/josipa/fps_urban_file_urb3.tar). 

The downloaded file is a tar file and includes:
1. geo_em files created with the new Copernicus LU data and added LCZ categories with [w2w tool](https://github.com/matthiasdemuzere/w2w), [HWSD](https://www.wdc-climate.de/ui/entry?acronym=WRF_NOAH_HWSD_world_TOP_ST_v121)+[BUK100](https://www.wdc-climate.de/ui/entry?acronym=WRF_NOAH_BUK_Ger_top_SOILTYP) soil texture data, and [SPOT LAI](https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-lai-fapar?tab=overview): 
	<br />  *geo_em.d01.nc* 
	<br />  *geo_em.d02.nc*
2. Aerosol climatology for both domains: 
	<br />  *AOD202004_d01* 
	<br />  *AOD202004_d02*
3. I/O fields txt file that deletes/adds variables from/to the output if not changed in the Registry files (`iofields_filename` in namelist.input): 
	<br />  *varlist.txt*
4. Input and boundary files to run the experiment:
   	<br />  *wrfbdy_d01*
	<br />  *wrfinput_d01* 
	<br />  *wrfinput_d02* 
	<br />  *wrflowinp_d01* 
	<br />  *wrflowinp_d02*
6. Two namelists necessary to run WPS and WRF:
	<br />  *[namelist.wps](../namelist.wps)*
        <br /> Defines 2 [domains](../domains_EP.png): EUR-12 d01 - the outer domain to fit the EUR-11 CORDEX domain in Lambert Conformal projection named EUR-12, and 	PAR-3 d02 - the inner domain centered around Paris which includes the corners defined in The FPS-URB-RCC protocol.
       	<br />  *[namelist.input](./namelist.input)*
        <br />  Set to run with BouLac PBL scheme (`bl_pbl_physics = 8`) and BEP+BEM urban scheme (`sf_urban_physics = 3`), with hybrid vertical levels and first level set to 35m (`dzbot = 35`) as defind in the [EUR-CORDEX WRF setting](https://github.com/CORDEX-WRF-community/euro-cordex-cmip6/blob/main/namelist.input) for CORDEX-CMIP6 simulations. 
 	<br />
  
To run the simulations, place the files from (2), (3), (4) and namelist.input from (5) to the `WRF/run` directory, and then run `wrf.exe`:

	# Copy the provided files to the WRF/run directory
	cp AOD202004_d01 AOD202004_d02  \
 		varlist.txt \
		wrfbdy_d01 wrfinput_d01  \
  		wrfinput_d02 wrflowinp_d01 wrflowinp_d02 \
		namelist.input WRF/run
	cd WRF/run
 
 	# Link correct SSP370 GHG file to be used
	ln -sf CAMtr_volume_mixing_ratio.SSP370 CAMtr_volume_mixing_ratio
 
 	# Run wrf.exe (Note that this should be adjusted to your system)
	srun -n ${SLURM_NTASKS} ./wrf.exe


