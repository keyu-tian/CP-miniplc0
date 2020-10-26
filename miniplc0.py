import argparse
import os
import sys

print(os.getcwd(), file=sys.stdout)
print(os.getcwd(), file=sys.stderr)

from lexical.tokenizer import LexicalTokenizer
from syntactic.analyzer import SyntacticAnalyzer
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
        tokens = LexicalTokenizer(full_text=full_text).parse_tokens()
        instructions = SyntacticAnalyzer(tokens=tokens).generate_instructions()
        inss = []
        for op in instructions:
            print(f'{op.get_clz_repr() + ("" if op.operand is None else f" {op.operand}")}', file=fout)
            inss.append(f'{op.get_clz_repr() + ("" if op.operand is None else f" {op.operand}")}')
        # VM('\n'.join(inss)).run()
    else:
        pass
    
    fout.close()


if __name__ == '__main__':
    main()
