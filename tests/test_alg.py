from llvm_test_case import LLVMTestCase


class AlgTestCase(LLVMTestCase):

    def test_fibonacci(self):
        result = self.run_file('fibo.li')
        self.assertEqual(result, '8')

    def test_bubble_sort(self):
        result = self.run_file('bubble_sort.li')
        self.assertEqual(result, '1\n3')

    def test_quicksort(self):
        result = self.run_file('quicksort.li')
        self.assertEqual(result, '1\n3')

    def test_break(self):
        result = self.run_file('break.li')
        self.assertEqual(result, '0\n2\n1')

    def test_continue(self):
        result = self.run_file('continue.li')
        self.assertEqual(result, '0\n4\n45')
