from vm.op import VMOperator, VM_OP_CLZ
from typing import List

from lexical.meta import Token, TokenType
from syntactic.err import SynProcessErr, SynDeclarationErr, SynStatementErr, SynExpressionErr


class SyntacticAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.tokens.append(Token(TokenType.NULL_TOKEN, None))
        self.uninitialized_vars, self.initialized_vars, self.constant_vars = {}, {}, {}
        self.instructions = []
        self.cur = 0
    
    def has_var_named(self, name):
        return any((
            name in self.uninitialized_vars.keys(),
            name in self.initialized_vars.keys(),
            name in self.constant_vars.keys(),
        ))
    
    @property
    def get(self):
        tok = self.tokens[self.cur]
        self.cur += 1
        return tok
    
    @property
    def peek(self):
        return self.tokens[self.cur]
    
    def unget(self):
        self.cur -= 1
    
    def generate_instructions(self) -> List[VMOperator]:
        self.instructions.clear()
        if self.get.token_type != TokenType.BEGIN:
            raise SynProcessErr('"begin" missing')
        self.parse_main_process()
        if self.get.token_type != TokenType.END:
            raise SynProcessErr('"end" missing')
        if self.get.token_type != TokenType.NULL_TOKEN:
            raise SynProcessErr('trails after the "end"')
        return self.instructions

    # <main_process> ::= {<const_decl>}{<var_decl>}{<clause>}
    def parse_main_process(self):
        while self.peek.token_type == TokenType.CONST:
            self.parse_const_decl()
        while self.peek.token_type == TokenType.VAR:
            self.parse_var_decl()
        while self.peek.token_type != TokenType.NULL_TOKEN:
            self.parse_clause()

    # <const_decl> ::= 'const'<identifier>'='<const_expr>';'
    def parse_const_decl(self):
        if self.get.token_type != TokenType.CONST:
            raise SynDeclarationErr('"const" missing')
        
        ident = self.get
        if ident.token_type != TokenType.IDENTIFIER:
            raise SynDeclarationErr('identifier missing')
        if self.has_var_named(ident.val):
            raise SynDeclarationErr('redeclaration')
        
        if self.get.token_type != TokenType.EQUAL_SIGN:
            raise SynDeclarationErr('"=" missing')
        val = self.parse_const_expr()
        self.constant_vars[ident.val] = val
        if self.get.token_type != TokenType.SEMICOLON:
            raise SynDeclarationErr('";" missing')

    # <const_expr> ::= [<sign>]<unsigned_int>
    def parse_const_expr(self) -> int:
        tok = self.get
        sign = 1
        if tok.token_type in {TokenType.PLUS_SIGN, TokenType.MINUS_SIGN}:
            sign = 1 if tok.token_type == TokenType.PLUS_SIGN else -1
            tok = self.get
        if tok.token_type != TokenType.UNSIGNED_INTEGER:
            raise SynExpressionErr('unsigned int missing')
        return sign * tok.val

    # <var_decl> ::= 'var'<identifier>['='<expr>]';'
    def parse_var_decl(self):
        if self.get.token_type != TokenType.VAR:
            raise SynDeclarationErr('"var" missing')
    
        ident = self.get
        if ident.token_type != TokenType.IDENTIFIER:
            raise SynDeclarationErr('identifier missing')
        if self.has_var_named(ident.val):
            raise SynDeclarationErr('redeclaration')
    
        tok = self.get
        if tok.token_type == TokenType.EQUAL_SIGN:
            val = self.parse_expr()
            self.initialized_vars[ident.val] = val
            if self.get.token_type != TokenType.SEMICOLON:
                raise SynDeclarationErr('";" missing')
        elif tok.token_type == TokenType.SEMICOLON:
            self.uninitialized_vars[ident.val] = 0
            return
        else:
            raise SynDeclarationErr('"=" or ";" missing')

    # <clause> ::= <assign> | <output> | ';'
    def parse_clause(self):
        pass

    # <assign> ::= <identifier>'='<expr>';'
    def parse_assign(self):
        pass

    # <output> ::= 'print''(' <expr> ')'';'
    def parse_output(self):
        pass

    # <expr> ::= <term>{'+'|'-'<term>}
    def parse_expr(self) -> int:
        pass

    # <term> ::= <factor>{'*'|'/'<factor>}
    def parse_term(self) -> int:
        pass

    # <factor> ::= [<sign>]( <identifier> | <unsigned_int> | '('<expr>')' )
    def parse_factor(self) -> int:
        pass


