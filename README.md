
# Tuberculosis Project [[Project Page]](https://github.com/marinadominguez/TBProject)

---

### Data

Data should be saved under
```
TB_sample/
```

---

### Run Project

To run the project, run

```
python3 project.py configs/thresholding.yaml
```

All parameters can be changed from the config file available in configs/thresholding.yaml or using the interactive interface.

---

# Package the project
### Make sure you have an upgraded version of pip
Windows
```
py -m pip install --upgrade pip
```

Linux/MAC OS
```
python3 -m pip install --upgrade pip
```

### Create a project with the following structure
```
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.cfg
├── src/
│   └── example_package/
│       ├── __init__.py
│       └── example.py
└── tests/
```

### pyproject.toml setup

This file tells tools like pip and build how to create your project:

```
[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
```
build-system.requires gives a list of packages that are needed to build your package. Listing something here will only make it available during the build, not after it is installed.

build-system.build-backend is the name of Python object that will be used to perform the build. If you were to use a different build system, such as flit or poetry, those would go here, and the configuration details would be completely different than the setuptools configuration described below.


### Setup.cfg setup
Using setup.cfg is a best practice, but you could have a dynamic setup file using setup.py.

```
[metadata]
name = example-pkg-YOUR-USERNAME-HERE
version = 0.0.1
author = Example Author
author_email = author@example.com
description = A small example package
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/pypa/sampleproject
project_urls =
    Bug Tracker = https://github.com/pypa/sampleproject/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.6

[options.packages.find]
where = src

```

### Make sure your build tool is up to date
Windows
```
py -m pip install --upgrade build
```
Linux/MAC OS
```
python3 -m pip install --upgrade build
```


### Create the build
```
py -m build
```


### Install the package
```
pip install -e .
```













### References
https://packaging.python.org/tutorials/packaging-projects/
