import argparse
import traceback

from lexical.err import TokenCompilationError
from lexical.tokenizer import LexicalTokenizer
from syntactic.analyzer import SyntacticAnalyzer
from syntactic.err import SyntacticCompilationError
from vm.impl import VM


def main():
    parser = argparse.ArgumentParser(description='python implementation of miniplc0 by Keyu Tian')
    parser.add_argument('--eval', action='store_true', default=False)
    parser.add_argument('-t', type=str, required=False, default=None)
    parser.add_argument('-l', type=str, required=False, default=None)
    parser.add_argument('-o', type=str, required=True)
    
    args: argparse.Namespace = parser.parse_args()
    
    if args.eval:
        with open(args.o, 'r') as fin:
            instructions = fin.read()
        vm = VM(instructions=instructions)
        vm.render_segments()
        vm.run()
        return

    fout = open(args.o, 'w')
    performing_syntactic_analysis = args.l is not None
    with open(args.t or args.l, 'r') as fin:
        full_text = fin.read()
    
    if performing_syntactic_analysis:
        try:
            tokens = LexicalTokenizer(full_text=full_text).parse_tokens()
            instructions = SyntacticAnalyzer(tokens=tokens).generate_instructions()
        except TokenCompilationError or SyntacticCompilationError:
            traceback.print_exc()
            instructions = []
        # inss = []
        for op in instructions:
            print(f'{op.get_clz_repr() + ("" if op.operand is None else f" {op.operand}")}', file=fout)
            # inss.append(f'{op.get_clz_repr() + ("" if op.operand is None else f" {op.operand}")}')
        # VM('\n'.join(inss)).run()
    else:
        try:
            tokens = LexicalTokenizer(full_text=full_text).parse_tokens()
        except TokenCompilationError or SyntacticCompilationError:
            traceback.print_exc()
            tokens = []
        for tok in tokens:
            print(f'{str(tok.token_type) + ("" if tok.val is None else f" {tok.val}")}', file=fout)
    
    fout.close()


if __name__ == '__main__':
    main()
