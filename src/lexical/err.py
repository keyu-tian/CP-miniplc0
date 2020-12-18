class TokenCompilationError(Exception):
    pass


class UnknownTokenErr(TokenCompilationError):
    pass


class TokArithmeticOverflowErr(TokenCompilationError):
    pass
