from os import listdir, system
from os.path import dirname, basename, join
from sys import argv
from re import compile, match


def capture(pattern, string):
    if result := match(pattern, string):
        return result.group(1)
    return None

checked = []
def get_dependencies(path):
    if path in checked:
        return
    with open(path) as f:
        for line in f:
            if name := capture(re_header, line):
                for header_dir, header_files in search_dirs.items():
                    if name in header_files:
                        header_path = join(header_dir, name)
                        get_dependencies(header_path)
                        checked.append(header_path)
            elif name := capture(re_extern, line):
                externs.add(name)
            elif path[-1] == 'h' and (name := capture(re_definition, line)):
                externs.add(name)
            elif name := capture(re_source, line):
                for source_dir, source_files in search_dirs.items():
                    if name in source_files:
                        sources.add(join('' if source_dir == main_dir else source_dir, name))
                        source_path = join(source_dir, name)
                        try:
                            get_dependencies(source_path)
                        except RecursionError:
                            pass
                        checked.append(source_path)

def handle_externs():
    for dir, files in search_dirs.items():
        for file in files:
            if file[-1] == 'c':
                with open(join(dir, file)) as f:
                    for line in f:
                        for extern in externs:
                            if line.startswith(extern):
                                sources.add(join('' if dir == main_dir else dir, file))

def build_command():
    get_dependencies(main)
    if externs:
        handle_externs()
    dirs_repr = f' -I {" -I ".join(dirs)} ' if dirs else ' '
    sources_repr = f'{" ".join(sources)}' if sources else ''
    return f'gcc{dirs_repr}{sources_repr} -o {main_file[:-2]} {main_file}'


main, *dirs = argv[1:]
if dirs:
    dirs = dirs[0].split(';')
main_dir, main_file = dirname(main), basename(main)
search_dirs = {folder: listdir(folder) for folder in [main_dir] + dirs}
search_dirs[main_dir].remove(main_file)

re_header = compile('#include "(.*\.h)"')
re_definition = compile('(?!#)((?:(?!;).)*)(?:;|\s)')
re_extern = compile('extern (.*);')
re_source = compile('#include "(.*\.c)"')

sources, externs = set(), set()


system(build_command())
