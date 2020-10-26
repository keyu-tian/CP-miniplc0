from vm.op import VMOperator
from typing import List

from lexical.meta import Token


class SyntacticAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.uninitialized_vars, self.initialized_vars, self.constant_vars = {}, {}, {}
    
    def generate_instructions(self) -> List[VMOperator]:
        return []
