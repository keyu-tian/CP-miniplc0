import sys
import traceback
from typing import Callable

from vm.op import VM_OP_CLZ
from vm.err import VMAccessViolationErr, VMStackOverflowErr, VMErr, VMIllegalInstructionErr


class VM(object):
    STACK_SIZE = 1 << 10
    
    def __init__(self, instructions: str):
        self._code_seg, self._stack_seg = [], []
        for ins in instructions.splitlines():
            ops = ins.split()
            self._code_seg.append(VM_OP_CLZ[ops[0]]() if len(ops) == 1 else VM_OP_CLZ[ops[0]](int(ops[1])))
        self._ip = 0
    
    def run(self, peep: Callable = lambda _: _):
        for ip, op in enumerate(self._code_seg):
            self._ip = ip + 1
            try:
                op.exec(self)
                peep(self)
            except VMIllegalInstructionErr:
                break
            
            except VMErr:
                traceback.print_exc()
                self.render_segments(sys.stderr)
                break
    
    def render_segments(self, fp=sys.stdout):
        print('\n=== stack ====', file=fp)
        sp = self.sp
        sp_fmt = f'%{len(str(sp))}d'
        for i, val in enumerate(self._stack_seg):
            print(f'{sp_fmt % i} | {val:8x} |', file=fp)
        print(f'{sp} | {" " * 8} | <== sp', file=fp)
        print('==============', file=fp)
        
        print('\n======= code =======', file=fp)
        max_ip = len(self._code_seg)
        ip_fmt = f'%{len(str(max_ip))}d'
        for i, op in enumerate(self._code_seg):
            print(f'{ip_fmt % i} | {str(op):13s} | {"<== ip" if i == self._ip else ""}', file=fp)
        print(f'{max_ip} | {" " * 13} | {"<== ip" if max_ip == self._ip else ""}', file=fp)
        print('====================', file=fp)
    
    # interfaces
    @property
    def sp(self):
        return len(self._stack_seg)
    
    def push(self, val):
        if len(self._stack_seg) >= VM.STACK_SIZE:
            raise VMStackOverflowErr
        self._stack_seg.append(val)
    
    def top(self):
        try:
            val = self._stack_seg[-1]
        except IndexError:
            raise VMAccessViolationErr
        return val
    
    def pop(self):
        try:
            val = self._stack_seg.pop()
        except IndexError:
            raise VMAccessViolationErr
        return val
    
    def __getitem__(self, offset):
        if offset < 0:
            raise VMAccessViolationErr
        try:
            val = self._stack_seg[offset]
        except IndexError:
            raise VMAccessViolationErr
        return val
    
    def __setitem__(self, offset, val):
        if offset < 0:
            raise VMAccessViolationErr
        try:
            self._stack_seg[offset] = val
        except IndexError:
            raise VMAccessViolationErr
    
    @staticmethod
    def write(*args, **kwargs):
        kwargs.update(dict(file=sys.stdout))
        print(*args, **kwargs)


if __name__ == '__main__':
    VM(instructions=
        """
        LIT 1
        LIT 1
        LIT 1
        LIT 1
        LIT 1
        DIV
        WRT
        WRT
        WRT
        WRT
        """
    ).run()
