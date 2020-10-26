class VMErr(Exception):
    pass


class VMIllegalInstruction(VMErr):
    pass


class VMAccessViolation(VMErr):
    pass


class VMStackOverflow(VMErr):
    pass


class VMArithmeticOverflow(VMErr):
    pass


class VMZeroDivision(VMErr):
    pass
