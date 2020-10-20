from llvm_test_case import LLVMTestCase


class IfTestCase(LLVMTestCase):

    def test_if_base_true(self):
        code = '''
            int x = 3;
            if (x > 1) {
                printi(1);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')

    def test_if_base_false(self):
        code = '''
            int x = 3;
            if (x < 1) {
                printi(1);
            }
            printi(1);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')

    def test_if_and(self):
        code = '''
            int x = 3;
            if (x < 5 && x > 2) {
                printi(1);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')

    def test_if_or(self):
        code = '''
            int x = 3;
            if (x < 1 || x > 2) {
                printi(1);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')
