from llvm_test_case import LLVMTestCase


class FunctionTestCase(LLVMTestCase):

    def test_fun_simple(self):
        code = '''
            int f() {
                return 5;
            }
            printi(f());
        '''
        result = self.run_code(code)
        self.assertEqual(result, '5')

    def test_fun_with_args(self):
        code = '''
            int f(int a, int b) {
                return a + b;
            }
            printi(f(1, 3));
        '''
        result = self.run_code(code)
        self.assertEqual(result, '4')
