import re
from typing import List

from lexical.err import UnknownTokenErr, TokArithmeticOverflowErr
from lexical.meta import Token, TokenType, STR_TO_TOKEN_TYPE


class LexicalTokenizer(object):
    
    @staticmethod
    def isalpha(s: str):
        return all(
            ord('a') <= ord(ch) <= ord('z')
            or ord('A') <= ord(ch) <= ord('Z')
            for ch in s
        )
    
    @staticmethod
    def isdecimal(s: str):
        return all(
            ord('0') <= ord(ch) <= ord('9')
            for ch in s
        )
    
    @staticmethod
    def isalnum(s: str):
        return all(
            ord('a') <= ord(ch) <= ord('z')
            or ord('A') <= ord(ch) <= ord('Z')
            or ord('0') <= ord(ch) <= ord('9')
            for ch in s
        )
    
    @staticmethod
    def isidentifier(s: str):
        return LexicalTokenizer.isalpha(s[:1]) and LexicalTokenizer.isalnum(s[1:])
    
    def __init__(self, full_text: str):
        self.inputs = self.raw_inputs = full_text
        for w in STR_TO_TOKEN_TYPE.keys():
            if not LexicalTokenizer.isalpha(w):
                self.inputs = self.inputs.replace(w, f' {w} ')
        self.inputs: List[str] = self.inputs.split()
        
        self.tok_chk = lambda s: (
            re.findall(r'^[0-9]+|[A-Za-z0-9]+$', s) if (
                    LexicalTokenizer.isalnum(s)
                    and not LexicalTokenizer.isdecimal(s)
                    and not LexicalTokenizer.isidentifier(s)
            ) else [s]
        )
    
    def parse_tokens(self) -> List[Token]:
        strs, tokens = [], []
        [strs.extend(self.tok_chk(s)) for s in self.inputs]
        for nxt_str in strs:
            token_type = STR_TO_TOKEN_TYPE.get(nxt_str, None)
            if token_type is not None:
                tokens.append(Token(token_type=token_type, val=nxt_str))
            elif nxt_str.isdecimal():
                uint_val = int(nxt_str)
                if uint_val > 0x7fffffff:
                    raise TokArithmeticOverflowErr
                tokens.append(Token(token_type=TokenType.UNSIGNED_INTEGER, val=uint_val))
            elif nxt_str.isidentifier():
                tokens.append(Token(token_type=TokenType.IDENTIFIER, val=nxt_str))
            else:
                raise UnknownTokenErr(f'"{nxt_str}"')
        return tokens


if __name__ == '__main__':
    from pprint import pprint as pp
    
    pp(
        LexicalTokenizer(
            """
            begin
                var 00baad = 1;
                print(a);
            end
            """
        ).parse_tokens()
    )
