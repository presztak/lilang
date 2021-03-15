from llvm_test_case import LLVMTestCase


class ArrayTestCase(LLVMTestCase):

    def test_multi_arr(self):
        code = '''
            int b(int[][] b) {
                return b[0][0] + b[1][0];
            }
            int[][] a = [[1,2], [3,4]];
            printi(b(a));
        '''
        result = self.run_code(code)
        self.assertEqual(result, '4')
