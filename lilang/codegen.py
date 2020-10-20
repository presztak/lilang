import os
from os import path
from os.path import abspath, dirname, join


class CodeGenerator(object):

    def __init__(self):
        self.bin_path = self.default_bin_path()
        self.lib_path = self.default_lib_path()

    def compile(self, str_code, exec_name):
        raise NotImplementedError

    def gen_output_name(self, output_name, output_path):
        if output_path:
            head, tail = os.path.split(output_path)
            if head:
                self.bin_path = head
            if tail:
                output_name = tail
        return output_name

    def _compile(self, str_code, output_name, output_path):

        exec_name = self.gen_output_name(output_name, output_path)
        self.create_bin_dir()
        self.compile(str_code, exec_name)

    def compile_from_file(self, script, output_path=''):

        # Generate executable name from source file name
        output_name = script.split('/')[-1].split('.')[0]

        with open(script) as s:
            str_code = s.read()
        self._compile(str_code, output_name, output_path)

    def compile_from_str(self, str_code, output_path=''):
        self._compile(str_code, 'out', output_path)

    def default_lib_path(self):
        return join(dirname(abspath(__file__)), 'lib')

    def default_bin_path(self):
        return join(os.getcwd(), 'bin')

    def create_bin_dir(self):
        if not path.exists(self.bin_path):
            os.makedirs(self.bin_path)

    def generate_code(self, node):
        method_name = f'_generate_{node.__class__.__name__}'
        method = getattr(self, method_name)
        return method(node)
