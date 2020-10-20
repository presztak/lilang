from llvm_test_case import LLVMTestCase


class BinOpTestCase(LLVMTestCase):

    def test_add_numbers(self):
        code = '''
            printi(2 + 3);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '5')

    def test_sub_numbers(self):
        code = '''
            printi(21 - 3);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '18')

    def test_mul_numbers(self):
        code = '''
            printi(2 * 3);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '6')

    def test_div_numbers(self):
        code = '''
            printi(6 / 3);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '2')
