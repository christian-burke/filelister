# Filelister

### Filelister is a Python package that makes working with filelists (yes, lists of files) easy.

```python
import filelister as fs
```

# Basic Usage

## Creating a Filelist

### From Data
You can create a Filelist object from a `list`, `set`, `tuple`, `Filelist` object, or `path` to directory.

```python
my_filelist = fs.Filelist(['../file_01.jpg', '../file_02.jpg'])

my_other_filelist = fs.Filelist('path/to/directory/')
```

### From System Files
You can also create a Filelist object by reading from a filelist saved on your system.

```python
my_filelist = fs.read_filelist('path/to/filelist.txt')
```

## Working with Filelists

### Manipulating a Filelist
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

### In and Contains
Filelists support a cointains method, as well as the python `in` operator.
```python
my_filelist.contains('path/to/file')

'path/to/file' in my_filelist
```

### Indexing and Slicing
A filelist can also be indexed and sliced like a normal python list. This will always return a native python list.
```python
my_filelist[1] == 'path/to/file.txt'

my_filelist[:3] == ['path/to/file01.txt', 'path/to/file02.txt', 'path/to/file03.txt']
```

## Saving a Filelist

### Arguments
`outfile`: specify a path to the location in which to write the filelist.
`output_type`: specify the type of filelist to write. Options include `'abs'`, `'rel'`, and `'na'` (see below).
`compressed`: accepts a boolean. Pass `compressed=True` to write a compressed filelist.

### Usage
```python
my_filelist.save('filelists/my_filelist.txt', output_type='abs', compressed=True)
```
Note that when saving a relative filelist, the filepaths are converted to be relative to the location of the filelist.


### Compression
A filelist can be stored using custom zlib compression by using
```python
my_filelist.save(outfile='compressed_filelist.zz', compressed=True)
```
This filelist can then be read using
```python
fs.read_filelist('compressed_filelist.zz', compressed=True)
```
Due to the nature of the compression, a compressed filelist should only be read by filelister.

### Types of Filelists
Filelister supports three formats of filelists: Absolute, Relative, and "na"
#### Absolute
 `abs` refers to an absolute filelist
```python
['path/to/file_01.txt', 'path/to/file_02.txt', 'path/to/file_03.txt']
```
#### Relative
`rel` refers to a relative filelists

```python
['../file_01.txt', '../file_02.txt', '../file_03.txt']
```
#### na
`na` refers to a filelist that is stored with no context, where filepaths are ignored and only filenames are stored
```python
['file_01.txt', 'file_02.txt', 'file_03.txt']
```


# Installation

## pip (PyPi)
```bash
pip install filelister
```

## Anaconda
*Coming soon*
