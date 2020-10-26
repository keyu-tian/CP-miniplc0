from abc import ABCMeta, abstractmethod

from utils.registry import Registry
from vm.err import VMIllegalInstruction, VMArithmeticOverflow, VMZeroDivision

VM_OP_CLZ = Registry()

__all__ = ['VM_OP_CLZ']


class VMOperator(metaclass=ABCMeta):
    def __init__(self, operand=None):
        self.operand = operand
    
    def __str__(self):
        return self.get_clz_repr() + (
            '' if self.operand is None
            else f'({self.operand:8x})'
        )
    
    @classmethod
    def get_clz_repr(cls):
        return [k for k, v in VM_OP_CLZ.items() if v == cls][0]
    
    @abstractmethod
    def exec(self, vm):
        pass


@VM_OP_CLZ.register('ILL')
class IllegalInstruction(VMOperator):
    def exec(self, vm):
        raise VMIllegalInstruction


@VM_OP_CLZ.register('LIT')
class LoadInt(VMOperator):
    def exec(self, vm):
        vm.push(self.operand)


@VM_OP_CLZ.register('LOD')
class Load(VMOperator):
    def exec(self, vm):
        val = vm[self.operand]
        vm.push(val)


@VM_OP_CLZ.register('STO')
class Store(VMOperator):
    def exec(self, vm):
        val = vm.top()
        vm[self.operand] = val
        vm.pop()


@VM_OP_CLZ.register('ADD')
class Add(VMOperator):
    def exec(self, vm):
        top, btm = vm.pop(), vm.pop()
        vm.push(_calc(btm, '+', top))


@VM_OP_CLZ.register('SUB')
class Subtract(VMOperator):
    def exec(self, vm):
        top, btm = vm.pop(), vm.pop()
        vm.push(_calc(btm, '-', top))


@VM_OP_CLZ.register('MUL')
class Multiply(VMOperator):
    def exec(self, vm):
        top, btm = vm.pop(), vm.pop()
        vm.push(_calc(btm, '*', top))


@VM_OP_CLZ.register('DIV')
class Divide(VMOperator):
    def exec(self, vm):
        top, btm = vm.pop(), vm.pop()
        vm.push(_calc(btm, '//', top))


@VM_OP_CLZ.register('WRT')
class Write(VMOperator):
    def exec(self, vm):
        vm.write(vm.pop())


def _calc(lhs, op, rhs):
    try:
        res = eval(f'{lhs}{op}{rhs}')
    except ZeroDivisionError:
        raise VMZeroDivision
    if res > 0x7fffffff or res < -0x80000000:
        raise VMArithmeticOverflow
    return res


if __name__ == '__main__':
    from pprint import pprint as pp
    
    pp(VM_OP_CLZ)
