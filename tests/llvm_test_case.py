import unittest
import subprocess
from lilang.codegen_llvm import LLVMCodeGenerator
import os


class LLVMTestCase(unittest.TestCase):

    output_path = 'tests/bin/test'

    def setUp(self):
        self.llvm_cg = LLVMCodeGenerator()

    def tearDown(self):
        os.remove(self.output_path)

    def run_code(self, code):
        self.llvm_cg.compile_from_str(code, output_path=self.output_path)
        try:
            result = subprocess.check_output([
                self.output_path,
            ])
        except subprocess.CalledProcessError as e:
            result = e.output.decode('utf-8')[:-1]
        return result

    def run_file(self, f):
        current_path = os.path.dirname(os.path.realpath(__file__))
        test_file_path = os.path.join(current_path, 'programs', f)
        self.llvm_cg.compile_from_file(
            test_file_path, output_path=self.output_path
        )
        try:
            result = subprocess.check_output([
                self.output_path,
            ])
        except subprocess.CalledProcessError as e:
            result = e.output.decode('utf-8')[:-1]
        return result
