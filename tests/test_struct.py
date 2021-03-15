from llvm_test_case import LLVMTestCase


class StructTestCase(LLVMTestCase):

    def test_simple_struct(self):
        code = '''
            struct A {
                int a;
                int b;
                bool c;
            }

            struct A t = {1,2,true};
            printi(t.a);
        '''
        result = self.run_code(code)
        self.assertEqual(result, '1')
