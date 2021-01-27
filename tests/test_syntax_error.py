from llvm_test_case import LLVMTestCase


class SyntaxErrorTestCase(LLVMTestCase):

    def test_illegal_character(self):
        code = """\\"""
        result = self.run_code(code)
        self.assertEqual(
            result,
            'Illegal character \\ in line 1 column 1\n'
            'Syntax error at EOF'
        )

    def test_syntax_error(self):
        code = """int k = p0;"""
        result = self.run_code(code)
        self.assertEqual(
            result,
            "Syntax error near '0' at line 1 column 10\n"
            "Syntax error near ';' at line 1 column 11\n"
            "Syntax error at EOF"
        )
