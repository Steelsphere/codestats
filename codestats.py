import argparse
import matplotlib.pyplot as plt
import os


class CodeParser:

    def __init__(self, pfiles):
        self.keywords = []
        self.keywords_count = {}
        self.filetxt = {}
        self.files = pfiles
        self.numlines = 0
        self.comment = ''
        self.file_extensions = ()
        self.endchar = ''
        self.exclusions = []

        for i in self.keywords:
            self.keywords_count[i] = 0

        for i in self.files:
            self.filetxt[i] = ''

    def run(self):
        print('Starting the parsing of files')
        self.read_files()
        print('Finished reading all files\nStarting analysis')
        for i in self.filetxt:
            self.remove_comments(i)
            self.count_keywords(i)
            print(i, ' --> Done')

    def read_files(self):
        for i in self.files:
            with open(i, 'r') as f:
                self.filetxt[i] = f.read()

    def get_keywords_from_file(self, file):
        with open(file, 'r') as f:
            data = f.readlines()
            data = [n.strip('\n') for n in data]
        return data

    def count_keywords(self, file):
        data = self.filetxt[file].split()
        for i in data:
            for j in self.keywords:
                if i == j or i == j + self.endchar:
                    self.keywords_count[j] += 1
        k = sorted(self.keywords_count, key=self.keywords_count.get, reverse=True)
        v = sorted(self.keywords_count.values(), reverse=True)
        newdict = {}
        for i, j in enumerate(k):
            newdict[j] = v[i]
        self.keywords_count = newdict

    def remove_comments(self, file):
        data = self.filetxt[file]
        data = data.splitlines()
        self.numlines += len(data)
        data = [n.split(self.comment)[0] for n in data]
        self.filetxt[file] = '\n'.join(data)

    def generate_keyword_graph(self):
        plt.bar(range(len(self.keywords_count)), self.keywords_count.values(), align='center')
        plt.xticks(range(len(self.keywords_count)), list(self.keywords_count.keys()), rotation=90)
        plt.show()

    def get_all_files_in_dir(self, d=('.',)):
        files = []
        print('Getting every file in the directory...')
        for i in d:
            for dirpath, directory, filesin in os.walk(i):
                if not [n for n in self.exclusions if n in dirpath]:
                    for file in filesin:
                        if file.endswith(self.file_extensions) and not [n for n in self.exclusions if file == n]:
                            files.append(os.path.join(dirpath, file))
        self.files = files


class PythonParser(CodeParser):

    def __init__(self, pfiles):
        CodeParser.__init__(self, pfiles)
        self.comment = '#'
        self.file_extensions = ('.py', '.pyw')
        self.keywords = self.get_keywords_from_file('keywords\\python keywords.txt')
        self.endchar = ':'

        for i in self.keywords:
            self.keywords_count[i] = 0


class CPPParser(CodeParser):

    def __init__(self, pfiles):
        CodeParser.__init__(self, pfiles)
        self.comment = '\\\\'
        self.file_extensions = ('.cpp', '.h', '.hpp')
        self.keywords = self.get_keywords_from_file('keywords\\c++ keywords.txt')
        self.endchar = ';'

        for i in self.keywords:
            self.keywords_count[i] = 0


def main():
    arg_parser = argparse.ArgumentParser(description='Generates statistics from code files')
    arg_parser.add_argument('dir', help='Files to parse', nargs='+')
    arg_parser.add_argument('--exclude', help='Files/Directories to exclude', nargs='+')
    arg_parser.add_argument('-f', help='Specifies that the directory is a folder and not a file.', action='store_true')
    arg_parser.add_argument('--lang', help='Language to parse. Currently supported: Python and C++', default='python')
    arg_parser.add_argument('--wdir', help='Changes the working directory')

    args = vars(arg_parser.parse_args())
    print('Args: ', args)

    if args['lang'] == 'python':
        python_main(args)

    if args['lang'] == 'c++':
        cpp_main(args)


def python_main(args):
    c = PythonParser(args['dir'])

    if args['wdir']:
        os.chdir(args['wdir'])

    if args['exclude']:
        c.exclusions = args['exclude']

    if args['f'] and args['dir'] != ['.']:
        c.get_all_files_in_dir(args['dir'])

    if args['dir'] == ['.']:
        c.get_all_files_in_dir()

    c.run()

    print(c.keywords_count)
    print('Number of lines: ', c.numlines)

    c.generate_keyword_graph()


def cpp_main(args):
    c = CPPParser(args['dir'])

    if args['wdir']:
        os.chdir(args['wdir'])

    if args['exclude']:
        c.exclusions = args['exclude']

    if args['f'] and args['dir'] != ['.']:
        c.get_all_files_in_dir(args['dir'])

    if args['dir'] == ['.']:
        c.get_all_files_in_dir()

    c.run()

    print(c.keywords_count)
    print('Number of lines: ', c.numlines)

    c.generate_keyword_graph()

if __name__ == "__main__":
    main()
