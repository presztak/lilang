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
        code = """in k = 0;"""
        result = self.run_code(code)
        self.assertEqual(
            result,
            "Syntax error near 'k' at line 1 column 4\n"
            "Syntax error near '=' at line 1 column 6"
        )
