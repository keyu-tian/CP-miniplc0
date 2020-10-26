import argparse

from lexical.tokenizer import LexicalTokenizer
from syntactic.analyzer import SyntacticAnalyzer


def main():
    parser = argparse.ArgumentParser(description='python implementation of miniplc0 by Keyu Tian')
    parser.add_argument('-t', type=str, required=False, default=None)
    parser.add_argument('-l', type=str, required=False, default=None)
    parser.add_argument('-o', type=str, required=True)
    
    args: argparse.Namespace = parser.parse_args()
    fout = open(args.o, 'w')

    performing_syntactic_analysis = args.l is not None
    with open(args.t or args.l, 'r') as fin:
        full_text = fin.read()
    
    if performing_syntactic_analysis:
        tokens = LexicalTokenizer(full_text=full_text).parse_tokens()
        instructions = SyntacticAnalyzer(tokens=tokens).generate_instructions()
        for op in instructions:
            print(f'{op.get_clz_repr() + ("" if op.operand is None else f" {op.operand}")}', file=fout)
    else:
        pass
    
    fout.close()


if __name__ == '__main__':
    main()
