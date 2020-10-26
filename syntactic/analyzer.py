from typing import List

from lexical.meta import Token


class SyntacticAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
    
    
