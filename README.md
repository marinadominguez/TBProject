
# Tuberculosis Project [[Project Page]](https://github.com/marinadominguez/TBProject)

## Installation

Create an empty environment specifying the python version as "python=3.8" and run
```
pip install -r requirements.txt
```
in order to install all packages required for the package `tbdetect`.


### Install the package `tbdetect`

`tbdetect` can be pip-installed by running
```
pip install -e .
```
This ensures the scripts are present locally, which enables you to run the provided Python scripts. Additionally, this allows you to modify the baseline solutions due to the `-e` option. Furthermore, this ensures the latest version is installed.


### Import project

To import the project, run

```
from tbdetect import project
```

## Run project

To run the project, run
```
project.main()
```

All parameters can be changed using the interactive interface.


## Data

Data should be saved under
```
TB_sample/
```














### References
https://packaging.python.org/tutorials/packaging-projects/
