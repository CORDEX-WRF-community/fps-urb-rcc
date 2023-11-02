# FPS on the Urban environment and Regional Climate Change (FPS-URB-RCC) 

This repository is created for the coordination of the WRF simulations within the CORDEX FPS URB-RCC framework following [The FPS-URB-RCC protocol](https://docs.google.com/document/d/1R4O1x67Tpr-qcEPlkzKDvJP1itoxKPbaBZO9gpIfamc/edit).

[**Test-7d**](./Test-7d) simulation, a short 7-day run, is set-up to test the stability and speed of the WRF model with the most complex urban scheme (BEP+BEM; `sf_urban_physics=3`) tuned on by different machines from all the involved [Institutions](https://docs.google.com/spreadsheets/d/1ZurcH982hepymMruHGPzQX-N55kWUXNc42RCE2pxgwg/edit#gid=0) running WRF.  

[**STAGE-0**](./STAGE-0) simulations proposed in the [The FPS-URB-RCC protocol](https://docs.google.com/document/d/1R4O1x67Tpr-qcEPlkzKDvJP1itoxKPbaBZO9gpIfamc/edit) will be performed in order to test RCMs and urban schemes, as well as the model and domain set-up. These simulations planned to be centered over the Paris region, and to simulate 5-month period covering two extreme events in 2020 (heat and heavy precipitation), in order to facilitate a coordinated analysis of the two extremes.  Furthermore, these test simulations will prepare the ground for the coordinated evaluation simulations (**STAGE-1**).

These experiments use CWC WRF v4.5.1.3
```bash
git clone --recurse-submodules -b v4.5.1.3 https://github.com/CORDEX-WRF-community/WRF.git
```
where `run/URBPARM_LCZ.TBL` is to be replaced by the file [URBPARM_LCZ-Madrid.TBL](./URBPARM_LCZ-Madrid.TBL) in this repo.

![WRF domains for CORDEX FPS-URB-RCC](https://github.com/FPS-URB-RCC/WRFcoordination/blob/main/domains_EP.png)

## Repository contents

| Folder | Description |
|--------|-------------|
| [meetings](./meetings) 	| Meeting agendas and presentations given during the meetings |
| [Test-7d](./Test-7d) 		| 7-day test simulation for STAGE-0. |
| [STAGE-0](./STAGE-0) 		| STAGE-0 configuration files and description. |
| [urbanModule](./urbanModule) 		| Modules and files to output the specific urban variables |

