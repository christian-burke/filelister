# Filelister
## Usage
```
import filelister as fs
```
### Creating a filelist
There are two main ways to create a filelist. The first is by passing a data argument to the Filelist class. This function has 3 arguments, `data`, `allowed_exts`, and `check_exists`. Data is the data contained in the Filelist, which can be a list, set, tuple, another filelist object, or a path to a single file or a directory. The `allowed_exts` argument is optional and allows the user to select specific file extensions that will be read into a flist. It defaults to allowing .jpg, .png, and .txt files. This is especially helpful when reading an existing filelist. `check_exists` checks that each filepath in the data corresponds to an existing file on the user's system.
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
The filelister will handle both relative and absolute paths in any accepted data type.
###Saving a Filelist
Filelists can be written to local files in two ways, the primary way being the `Filelist.save()` function. This function takes two parameters, `outfile`, the path to the location in which to store the filelist, and `relative=False`, an optional value to determine whether to write an absolute or relative Filelist, which is useful when working in shared directories. A relative filelist will always store filepaths relative to the location of the outfile.
```
my_filelist.save('tests/filelists/my_filelist.txt', relative=True)
filelist written to tests/filelists/my_filelist.txt
```
The other way to write a filelist is using `fs.write_filelist(data, outfile, allowed_exts=['.jpg', '.png', '.txt'], relative=True)```, a shortcut for quickly writing filelists directly from the data. 
```
fs.write_filelist('tests/data', 'tests/filelists/my_filelist.txt')
filelist written to tests/filelists/my_filelist.txt
```

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
Filelists are also available to all of the standard set operations, such as ```union()```, ```difference()```, and ```intersection()```, as well as a custom function, ```Filelist.compare()``` which prints the difference between two filelists and returns a dictionary of all files added and removed between the two lists.
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
```
my_filelist1.compare(my_filelist2)
[ + ] tests/data/sample_01.txt
[ - ] tests/data/sample_03.txt
[ - ] tests/data/sample_04.txt
[ - ] tests/data/sample_05.txt
```

