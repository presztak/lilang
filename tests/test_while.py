from llvm_test_case import LLVMTestCase


class WhileTestCase(LLVMTestCase):

    def test_if_base_true(self):
        code = '''
            int x = 10;
            int counter = 0;
            while (x > 0) {
                counter = counter + 1;
                x = x - 1;
            }
            printi(counter);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '10')
