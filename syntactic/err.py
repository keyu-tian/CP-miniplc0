class SyntacticCompilationError(Exception):
    pass


class SynProcessErr(SyntacticCompilationError):
    pass


class SynDeclarationErr(SyntacticCompilationError):
    pass


class SynStatementErr(SyntacticCompilationError):
    pass


class SynExpressionErr(SyntacticCompilationError):
    pass

