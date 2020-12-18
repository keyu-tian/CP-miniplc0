class VMErr(Exception):
    pass


class VMIllegalInstructionErr(VMErr):
    pass


class VMAccessViolationErr(VMErr):
    pass


class VMStackOverflowErr(VMErr):
    pass


class VMArithmeticOverflowErr(VMErr):
    pass


class VMZeroDivisionErr(VMErr):
    pass
