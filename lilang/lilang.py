import click

from .codegen_llvm import LLVMCodeGenerator
from .lexer import LilangLexer
from .parser import LilangParser


class Lilang(object):

    def __init__(self, generator):
        self.generator = generator

    def compile_from_file(self, script, output_path):
        self.generator.compile_from_file(script, output_path)

    def compile_from_str(self, code, output_path):
        self.generator.compile_from_str(code, output_path)


def get_code(code, filename):
    if code:
        return code
    with open(filename) as s:
        return s.read()


@click.command()
@click.option('-l', '--lexer', is_flag=True, help='Lexer output')
@click.option('-p', '--parser', is_flag=True, help='Parser output')
@click.option('-c', '--code', help='Code to run')
@click.option('-o', '--output_path', help='Executable path')
@click.argument('filename', required=False)
def main(lexer, parser, code, output_path, filename):
    if lexer is True:
        code = get_code(code, filename)
        lexer = LilangLexer(code)
        for tok in lexer.tokenize(code):
            print('type=%r, value=%r' % (tok.type, tok.value))
    elif parser is True:
        code = get_code(code, filename)
        lexer = LilangLexer(code)
        parser = LilangParser(code)
        result = parser.parse(lexer.tokenize(code))
        print(result)
    elif code:
        lilang = Lilang(LLVMCodeGenerator())
        lilang.compile_from_str(code, output_path)
    else:
        if not filename:
            raise click.UsageError("Missing argument 'FILENAME'.")
        lilang = Lilang(LLVMCodeGenerator())
        lilang.compile_from_file(filename, output_path)
