# Filelister
## Usage
```
import filelister as fs
```

###Creating a filelist
There are two main ways to create a filelist. The first is by passing a data argument to the Filelist class.
```
my_filelist = fs.Filelist(data)
```
There are many acceptable data types for this, including path-like strings, lists, sets, and tuples.

The other option is to read from an existing filelist.
```
my_filelist = fs.read_filelist(`tests/filelists/rel_filelist.txt')
```
The filelister will handle both relative and absolute paths in any data type.
###Using a Filelist
####Merging filelists
Two filelists can be merged with the + operator.
```
new_filelist = my_filelist1 + my_filelist2
my_filelist += my_filelist2
```


