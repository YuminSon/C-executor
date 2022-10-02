# C-executor
GCC command generator/executor for use with VSCode Code Runner

## Key Points
- Smart - Detects `#include`s, `extern`s, and declarations, then adds the required files to the command!
- Expandable - Lets you add custom include paths in a second!
- Convenient - One button away from executing your C code with the help of Code Runner! 

## Usage
0. You need to have VSCode, GCC, and Python>=3.8 configured.
1. Copy `executor.py` and save it on your system.
2. Install Code Runner from Marketplace and add the following to code-runner.executorMap.
```
"c": "cd $dir && python -u \"path_of_executor.py\" .\\$fileName \"custom_include_paths\" && $dir$fileNameWithoutExt",
```
3. Done! `path_of_executor.py` and `custom_include_paths` can either be absolute or relative to the C file, and you can add multiple include paths by separating them with semicolons.

## Warning
- Tested only on Windows 11.
- Definitions in source files should **exactly** look like their declarations in the header files. That is, you cannot add another space between the type and the name of a variable.
- Suitable for small projects. The executor handles `extern`s and declarations by reserving all files with their column-zero occurances for compilation. Better more than less, right?

## License
BSD 3-Clause
