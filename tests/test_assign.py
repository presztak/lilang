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

    def test_int_decl_multi(self):
        code = '''
            int x = 5, y = 6;
            printi(x);
            printi(y);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '5\n6')

    def test_array_decl_multi(self):
        code = '''
            int[] a = [1, 2, 3, 4], b = [1, 10];
            printi(a[3]);
            printi(b[1]);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '4\n10')

    def test_bool_assignment(self):
        code = '''
            bool x = true;
            if (x == true) {
                printi(1);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')

    def test_bool_array_assignment(self):
        code = '''
            bool[] a = [true, false, false, true];
            bool x = a[3];
            if (a[3] == true) {
                printi(2);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '2')
