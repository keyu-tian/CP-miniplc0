import sys
import traceback
from typing import Callable

from vm.err import VMAccessViolation, VMStackOverflow, VMErr, VMIllegalInstruction


class VM(object):
    STACK_SIZE = 1 << 10
    
    def __init__(self, instructions):
        self._code_seg, self._stack_seg = instructions, []
        self._ip = 0
    
    def run(self, peep: Callable = lambda _: _):
        for ip, op in enumerate(self._code_seg):
            self._ip = ip + 1
            try:
                op.exec(self)
                peep(self)
            except VMIllegalInstruction:
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
            raise VMStackOverflow
        self._stack_seg.append(val)
    
    def top(self):
        try:
            val = self._stack_seg[-1]
        except IndexError:
            raise VMAccessViolation
        return val
    
    def pop(self):
        try:
            val = self._stack_seg.pop()
        except IndexError:
            raise VMAccessViolation
        return val
    
    def __getitem__(self, offset):
        if offset < 0:
            raise VMAccessViolation
        try:
            val = self._stack_seg[offset]
        except IndexError:
            raise VMAccessViolation
        return val
    
    def __setitem__(self, offset, val):
        if offset < 0:
            raise VMAccessViolation
        try:
            self._stack_seg[offset] = val
        except IndexError:
            raise VMAccessViolation
    
    @staticmethod
    def write(*args, **kwargs):
        kwargs.update(dict(file=sys.stdout))
        print(*args, **kwargs)


if __name__ == '__main__':
    from vm.op import VM_OP_CLZ
    
    VM(instructions=[
        VM_OP_CLZ['LIT'](1),
        VM_OP_CLZ['LIT'](2),
        VM_OP_CLZ['LIT'](0),
        VM_OP_CLZ['LIT'](0),
        VM_OP_CLZ['LIT'](0),
        VM_OP_CLZ['DIV'](),
        VM_OP_CLZ['WRT'](),
        VM_OP_CLZ['WRT'](),
        VM_OP_CLZ['WRT'](),
        VM_OP_CLZ['WRT'](),
    ]).run()
