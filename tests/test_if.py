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

    def test_if_else_true(self):
        code = '''
            int x = 3;
            if (x == 3) {
                printi(1);
            } else {
                printi(2);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')

    def test_if_else_false(self):
        code = '''
            int x = 3;
            if (x == 4) {
                printi(1);
            } else {
                printi(2);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '2')

    def test_if_else_if_true(self):
        code = '''
            int x = 3;
            if (x == 4) {
                printi(1);
            } else if (x == 3) {
                printi(2);
            } else {
                printi(3);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '2')

    def test_if_else_if_false(self):
        code = '''
            int x = 3;
            if (x == 4) {
                printi(1);
            } else if (x == 5) {
                printi(2);
            } else {
                printi(3);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '3')

    def test_if_if_else1(self):
        code = '''
            int x = 3;
            if (x == 4) {
                printi(1);
            } if (x == 3) {
                printi(2);
            } else {
                printi(3);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '2')
