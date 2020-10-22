from llvm_test_case import LLVMTestCase


class AssignmentTestCase(LLVMTestCase):

    def test_int_assignment(self):
        code = '''
            int x = 5;
            printi(x);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '5')

    def test_array_assignment(self):
        code = '''
            int[] a = [1, 2, 3, 4];
            printi(a[3]);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '4')

    def test_int_plus_assignment(self):
        code = '''
            int x = 5;
            x += 5;
            printi(x);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '10')

    def test_array_plus_assignment(self):
        code = '''
            int[] a = [1, 2, 3, 4];
            a[3] += 5;
            printi(a[3]);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '9')

    def test_int_minus_assignment(self):
        code = '''
            int x = 5;
            x -= 5;
            printi(x);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '0')

    def test_array_minus_assignment(self):
        code = '''
            int[] a = [1, 2, 3, 4];
            a[2] -= 5;
            printi(a[2]);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '-2')

    def test_int_mul_assignment(self):
        code = '''
            int x = 5;
            x *= 5;
            printi(x);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '25')

    def test_array_mul_assignment(self):
        code = '''
            int[] a = [1, 2, 3, 4];
            a[2] *= 5;
            printi(a[2]);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '15')

    def test_int_div_assignment(self):
        code = '''
            int x = 5;
            x /= 5;
            printi(x);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')

    def test_array_div_assignment(self):
        code = '''
            int[] a = [1, 2, 3, 4];
            a[3] /= 4;
            printi(a[3]);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')
