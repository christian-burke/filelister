# Filelister
## Usage
```
import filelister as fs
```
### Creating a filelist
There are two main ways to create a filelist. The first is by passing a data argument to the Filelist class. This function has 3 arguments, `data`, `allowed_exts`, and `check_exists`. Data is the data contained in the Filelist, which can be a list, another filelist object, or a path to a single file or a directory. the `allowed_exts` argument is optional and allows the user to select specific file extensions that will be read into a flist. This is especially helpful when reading an existing filelist. `check_exists` checks that each filepath in the data corresponds to an existing file on the user's system.
```
my_filelist = fs.Filelist(['tests/data/sample_01.txt', 'tests/data/sample_02.txt'])
```
The other option is to read from an existing filelist. This takes in the same parameters and returns a Filelist object.
```
my_filelist2 = fs.read_filelist(`tests/filelists/rel_filelist.txt', allowed_exts=['.txt'], check_exists=False )
print(my_filelist)
tests/data/sample_02.txt
tests/data/sample_03.txt
tests/data/sample04.txt
tests/data/sample05.txt
```
The filelister will handle both relative and absolute paths in any data type.
### Using a Filelist
#### Merging filelists
Two filelists can be merged with the + operator.
```
new_filelist = my_filelist1 + my_filelist2
print(new_filelist)
tests/data/sample_01.txt
tests/data/sample_02.txt
tests/data/sample_03.txt
tests/data/sample_04.txt
tests/data/sample_05.txt
```
```
my_filelist += my_filelist2
print(my_filelist)
tests/data/sample_01.txt
tests/data/sample_02.txt
tests/data/sample_03.txt
tests/data/sample_04.txt
tests/data/sample_05.txt
```
Similarly, the - operator will remove the contents of one filelist from another.
```
new_filelist = my_filelist1 - my_filelist2
print(new_filelist)
tests/data/sample_01.txt
```
```
my_filelist -= my_filelist2
print(my_filelist)
tests/data/sample_01.txt
```
#### Set comparisons
Filelists are also available to all of the standard set operations, such as ```union()```, ```difference()```, and ```intersection()```, as well as a custom function, ```filelist.compare()``` which prints the difference between two filelists and returns a dictionary of all files added and removed between the two lists.
```my_filelist1 = (['tests/data/sample_01.txt', 'tests/data/sample_02.txt'])
my_filelist2 = fs.read_filelists('tests/fileists/rel_filelist.txt')
new_filelist = my_filelist1.union(my_filelist2)
print(new_filelist)
tests/data/sample_01.txt
...
tests/data/sample_05.txt
```
```
new_filelist = my_filelist2.intersection(['tests/data/sample_01.txt', 'tests/data/sample_05.txt'])
print(new_filelist)
tests/data/sample_05.txt
```
```my_filelist1.compare(my_filelist2)
[ + ] tests/data/sample_01.txt
[ - ] tests/data/sample_03.txt
[ - ] tests/data/sample_04.txt
[ - ] tests/data/sample_05.txt
```

