from llvm_test_case import LLVMTestCase


class ForTestCase(LLVMTestCase):

    def test_for(self):
        code = '''
            int counter = 0;
            for (int i = 0; i < 10; i += 1;) {
                counter = counter + 1;
            }
            printi(counter);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '10')
