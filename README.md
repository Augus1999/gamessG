# gamessG

This script has been tested on `Python 3.7.3` ,`3.8.3`, and `3.8.6`

## usage

<div align=center><img src="https://github.com/Augus1999/gamessG/blob/master/ico/workspace.jpg" width="350" alt="workspace"/></div>

* Click add-icon <img src="https://github.com/Augus1999/gamessG/blob/master/ico/black-plus.png" width="20" alt="add"/> to add files for calculation.

* After calculations, click the water-molecule-icon <img src="ico/water_molecule.png" width="20" alt="icon"/> will open the molecule models in [wxMacMolplt.exe](https://github.com/brettbode/wxmacmolplt).

* Click clean-icon <img src="https://github.com/Augus1999/gamessG/blob/master/ico/clean_black.png" width="20" alt="clean"/> to delete all restart files in GAMESS root.

## settings

Settings are saved in [settings.json](https://github.com/Augus1999/gamessG/blob/master/settings.json) file.

```
{
  "GAMESSDIR": "C:\\Users\\Public\\gamess-64",
  "OUTDIR": "C:\\...\\GAMESS-log"
}
```
* GAMESSDIR: where the GAMESS program .EXE locates

* OUTDIR: where output files you wnat to be put
