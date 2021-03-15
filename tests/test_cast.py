from llvm_test_case import LLVMTestCase


class CastTestCase(LLVMTestCase):

    def test_cast_bool_int(self):
        code = '''
            printi(int(5));
            printi(int(6));
        '''
        result = self.run_code(code)
        self.assertEqual(result, '5\n6')

    def test_cast_int_bool(self):
        code = '''
            bool a = bool(1);
            if (a == true) {
                printi(1);
            }
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')
