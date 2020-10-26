from vm.op import VMOperator, VM_OP_CLZ
from typing import List

from lexical.meta import Token, TokenType
from syntactic.err import SynProcessErr, SynDeclarationErr, SynStatementErr, SynExpressionErr, SynAssignErr, SynOutputErr, SynFactorErr


class SyntacticAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens + [Token(TokenType.NULL_TOKEN, None)]
        self.uninitialized_vars, self.initialized_vars, self.constant_vars = {}, {}, {}
        self.all_vars = {}
        self.instructions = []
        self.cur = 0
        self.stack_offset = 0

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
        [c.clear() for c in [
            self.uninitialized_vars,
            self.initialized_vars,
            self.constant_vars,
            self.all_vars,
            self.instructions
        ]]
        self.cur = self.stack_offset = 0
        if self.get.token_type != TokenType.BEGIN:
            raise SynProcessErr('"begin" missing')
        self.parse_main_process()
        if self.get.token_type != TokenType.END:
            raise SynProcessErr('"end" missing')
        if self.get.token_type != TokenType.NULL_TOKEN:
            raise SynProcessErr('trails after the "end"')
        return self.instructions

    # <main_process> ::= {<const_decl>}{<var_decl>}{<statement>}
    def parse_main_process(self):
        # parse <const_decls>
        while self.peek.token_type == TokenType.CONST:
            self.parse_const_decl()
        # parse <var_decls>
        while self.peek.token_type == TokenType.VAR:
            self.parse_var_decl()
        # parse <statements>
        while self.peek.token_type != TokenType.END:
            self.parse_statement()

    # <const_decl> ::= 'const'<identifier>'='<const_expr>';'
    def parse_const_decl(self):
        # parse 'const'
        if self.get.token_type != TokenType.CONST:
            raise SynDeclarationErr('"const" missing')
        # parse <identifier>
        ident = self.get
        if ident.token_type != TokenType.IDENTIFIER:
            raise SynDeclarationErr('identifier missing')
        # parse '='
        if self.get.token_type != TokenType.EQUAL_SIGN:
            raise SynDeclarationErr('"=" missing')
        # parse <const_expr>
        self.parse_const_expr()
        # parse ';'
        if self.get.token_type != TokenType.SEMICOLON:
            raise SynDeclarationErr('";" missing')
        # performing
        self._declare_var(var_name=ident.val, initialized=True, const=True)

    # <const_expr> ::= [<sign>]<unsigned_int>
    def parse_const_expr(self):
        # parse [<sign>]
        sign = 1
        tok = self.get
        if tok.token_type in {TokenType.PLUS_SIGN, TokenType.MINUS_SIGN}:
            sign = 1 if tok.token_type == TokenType.PLUS_SIGN else -1
            tok = self.get
        # parse <unsigned_int>
        if tok.token_type != TokenType.UNSIGNED_INTEGER:
            raise SynExpressionErr('unsigned int missing')
        # performing
        self.instructions.append(VM_OP_CLZ['LIT'](sign * tok.val))

    # <var_decl> ::= 'var'<identifier>['='<expr>]';'
    def parse_var_decl(self):
        # parse 'var'
        if self.get.token_type != TokenType.VAR:
            raise SynDeclarationErr('"var" missing')
        # parse <identifier>
        ident = self.get
        if ident.token_type != TokenType.IDENTIFIER:
            raise SynDeclarationErr('identifier missing')
        tok = self.get
        # parse '=', <expr>, ';'
        if tok.token_type == TokenType.EQUAL_SIGN:
            initialized = True
            self.parse_expr()
            if self.get.token_type != TokenType.SEMICOLON:
                raise SynDeclarationErr('";" missing')
        # parse ';'
        elif tok.token_type == TokenType.SEMICOLON:
            initialized = False
        else:
            raise SynDeclarationErr(f'"=" or ";" missing in the declaration of var "{ident.val}"')
        # performing
        self._declare_var(var_name=ident.val, initialized=initialized, const=False)

    # <statement> ::= <assign> | <output> | ';'
    def parse_statement(self):
        # parse <assign>
        if self.peek.token_type == TokenType.IDENTIFIER:
            self.parse_assign()
        # parse <output>
        elif self.peek.token_type == TokenType.PRINT:
            self.parse_output()
        # parse ';'
        elif self.peek.token_type == TokenType.SEMICOLON:
            _ = self.get
        else:
            raise SynStatementErr(f'unknown statement (starts with {self.peek.token_type})')

    # <assign> ::= <identifier>'='<expr>';'
    def parse_assign(self):
        # parse <identifier>
        ident = self.get
        if ident.token_type != TokenType.IDENTIFIER:
            raise SynAssignErr('identifier missing')
        var_name = ident.val
        if var_name in self.constant_vars.keys():
            raise SynAssignErr(f'assignment of read-only var "{var_name}"')
        var_offset = self.all_vars.get(var_name, None)
        if var_offset is None:
            raise SynAssignErr(f'assignment of undefined var "{var_name}"')
        # parse '='
        if self.get.token_type != TokenType.EQUAL_SIGN:
            raise SynAssignErr('"=" missing')
        # parse <expr>
        self.parse_expr()
        # parse ';'
        if self.get.token_type != TokenType.SEMICOLON:
            raise SynDeclarationErr('";" missing')
        # performing
        if var_name in self.uninitialized_vars.keys():
            self.initialized_vars[var_name] = var_offset
            self.uninitialized_vars.pop(var_name)
        self.instructions.append(VM_OP_CLZ['STO'](var_offset))

    # <output> ::= 'print''(' <expr> ')'';'
    def parse_output(self):
        # parse 'print'
        if self.get.token_type != TokenType.PRINT:
            raise SynOutputErr('"print" missing')
        # parse '('
        if self.get.token_type != TokenType.LEFT_BRACKET:
            raise SynOutputErr('"(" missing')
        # parse <expr>
        self.parse_expr()
        # parse ')'
        if self.get.token_type != TokenType.RIGHT_BRACKET:
            raise SynOutputErr('")" missing')
        # parse ';'
        if self.get.token_type != TokenType.SEMICOLON:
            raise SynOutputErr('";" missing')
        # performing
        self.instructions.append(VM_OP_CLZ['WRT']())

    # <expr> ::= <term>{'+'|'-'<term>}
    # NOTE: the result will be stored at the top of vm.stack
    def parse_expr(self):
        self.parse_term()
        while self.peek.token_type in [TokenType.PLUS_SIGN, TokenType.MINUS_SIGN]:
            pm = self.get
            self.parse_term()
            self.instructions.append(VM_OP_CLZ['ADD' if pm.token_type == TokenType.PLUS_SIGN else 'SUB']())

    # <term> ::= <factor>{'*'|'/'<factor>}
    # NOTE: the result will be stored at the top of vm.stack
    def parse_term(self):
        self.parse_factor()
        while self.peek.token_type in [TokenType.MULTIPLICATION_SIGN, TokenType.DIVISION_SIGN]:
            md = self.get
            self.parse_factor()
            self.instructions.append(VM_OP_CLZ['MUL' if md.token_type == TokenType.MULTIPLICATION_SIGN else 'DIV']())

    # <factor> ::= [<sign>]( <identifier> | <unsigned_int> | '('<expr>')' )
    # NOTE: the result will be stored at the top of vm.stack
    def parse_factor(self):
        tok = self.get
        signed = None
        if tok.token_type in [TokenType.PLUS_SIGN, TokenType.MINUS_SIGN]:
            signed = 1 if tok.token_type == TokenType.PLUS_SIGN else -1
            tok = self.get
        if tok.token_type == TokenType.IDENTIFIER:
            var_name = tok.val
            var_offset = self.all_vars.get(var_name, None)
            if var_offset is None:
                raise SynFactorErr(f'reference of undefined var "{var_name}"')
            if var_name in self.uninitialized_vars.keys():
                raise SynFactorErr(f'reference of uninitialized var "{var_name}"')
            self.instructions.append(VM_OP_CLZ['LOD'](var_offset))
        elif tok.token_type == TokenType.UNSIGNED_INTEGER:
            self.instructions.append(VM_OP_CLZ['LIT'](tok.val))
        elif tok.token_type == TokenType.LEFT_BRACKET:
            self.parse_expr()
            if self.get.token_type != TokenType.RIGHT_BRACKET:
                raise SynFactorErr('")" missing')
        else:
            raise SynFactorErr(f'identifier or uint or (expr) missing')
        
        if signed is not None:
            self.instructions.append(VM_OP_CLZ['LIT'](signed))
            self.instructions.append(VM_OP_CLZ['MUL']())

    def _declare_var(self, var_name: str, initialized: bool, const: bool):
        if var_name in self.all_vars:
            raise SynDeclarationErr(f'redeclaration of var "{var_name}"')
        if const:
            vs = self.constant_vars
        else:
            vs = self.initialized_vars if initialized else self.uninitialized_vars
        self.all_vars[var_name] = vs[var_name] = self.stack_offset
        self.stack_offset += 1
