# Filelister

### Filelister is a Python package that makes working with filelists (yes, lists of files) easy.

```python
import filelister as fs
```

### Contents
- [Basic Usage](#basic-usage)
- [Installation](#installation)
- [Contributors](#contributors)
- [API](#API)

# Basic Usage

## Creating a Filelist

### From Data
You can create a Filelist object from a list, set, tuple, Filelist object, or path to directory.

```python
my_filelist = fs.Filelist(['../file_01.jpg', '../file_02.jpg'])

my_other_filelist = fs.Filelist('path/to/directory')
```

### From System Files
You can also create a Filelist object by reading from a filelist saved on your system.

```python
my_filelist = fs.read_filelist('path/to/filelist.txt')
```


## Saving a Filelist
### Arguments
`outfile`: specify a path to the location in which to write the filelist.  
`output_type`: specify the type of filelist to write. Options include `'abs'`, `'rel'`, and `'na'`.  
`compressed`: accepts a boolean. Pass `compressed=True` to write a compressed filelist.  
`na` is used to save a list of filenames (or uncommon postfixes). Note that when saving a relative filelist, the filepaths are converted to be relative to the location of the filelist.
```python
my_filelist.save('filelists/my_filelist.txt', relative=True, compressed=True)
```

## Compression
A filelist can be stored using custom zlib compression by using
```python
my_filelist.save(outfile='compressed_filelist.zz', compressed=True)
```
This filelist can then be read using
```python
fs.read_filelist('compressed_filelist.zz', compressed=True)
```
Due to the nature of the compression, a compressed filelist should only be read by filelister.

## Working with Filelists

### Manipulating Filelists
Filelists support a number of conversions, including conversions to a native python list, to a relative filelist, and to an absolute filelist.
```python
my_filelist.to_list()

my_filelist.to_abs()

my_filelist.to_rel()
```
These commands can also be chained:
```python
my_filelist.to_abs().to_list()
```
Filelists support a cointains method, as well as the python `in` operator.
```python
my_filelist.contains('path/to/file')

'path/to/file' in my_filelist
```

A filelist can also be indexed and sliced like a normal python list. This will always return a native python list.
```python
my_filelist[1] == 'path/to/file.txt'

my_filelist[:3] == ['path/to/file00.txt', 'path/to/file01.txt', 'path/to/file02.txt']
```

# Installation

## pip (local)
You can install this package locally via Github and pip.

```bash
git clone https://github.com/burkecp/filelister.git
cd filelister
pip install -e .
```
## pip (PyPi)
*Coming soon*

## Anaconda
*Coming soon*

# Contributors

## Authors
Simon Burke
Christian Burke
Refik Anadol Studio

# API

## In Progress

### Arithmetic Operations

### Set Operations
