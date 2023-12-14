import sys
from caie_vm import caie_vm
from caie_assembler import caie_assembler


args = sys.argv

test_assemble = caie_assembler(args[1], int(args[2]), int(args[3]))
exe = test_assemble.generate()
test_run = caie_vm(100, exe, ext=True)
test_run.execute()