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
